#!/usr/bin/env python3
"""
TENDERS Dashboard — FastAPI Backend (SaaS)
Multi-tenant tender tracking with auth, billing, and plan-based feature gating.
"""

import json
import os
import re
import subprocess
import signal
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Body, Depends, UploadFile, File as FastAPIFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import CORS_ORIGINS
from database import create_tables, get_db, User, UserInstitution, UserApplication, Plan
from auth import router as auth_router, get_current_user, get_optional_user, require_admin, user_to_dict
from stripe_billing import router as billing_router
from admin import router as admin_router
from plan_limits import (
    check_institution_limit, check_application_limit,
    check_download_access, check_scraper_access, get_user_plan_info,
)

PROJECT = Path(os.getenv("TENDERS_PROJECT_ROOT", "/var/www/html/tenders"))
INSTITUTIONS_DIR = PROJECT / "institutions"
APPLICATIONS_DIR = PROJECT / "applications"
COMPANY_DOCS_BASE = PROJECT / "frontend" / "public" / "company_documents"
OPPORTUNITIES_DIR = PROJECT / "opportunities"
CONFIG_DIR = PROJECT / "config"
LOGS_DIR = PROJECT / "logs"
NOTIFICATIONS_DIR = PROJECT / "notifications"
SCRIPTS_DIR = PROJECT / "scripts"

app = FastAPI(title="TENDERS Dashboard API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register auth + billing routers
app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(admin_router)


# ── Startup ─────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup():
    create_tables()


# ── Helpers ──────────────────────────────────────────────────────────────────

def parse_date(s):
    if not s:
        return None
    s = str(s).strip()
    try:
        if "T" in s:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def days_until(closing_date_str):
    d = parse_date(closing_date_str)
    if not d:
        return None
    return (d - date.today()).days


def load_json(path: Path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else []


def parse_readme_frontmatter(readme_path: Path) -> dict:
    try:
        content = readme_path.read_text(encoding="utf-8")
    except Exception:
        return {}

    info = {}
    for key, pattern in [
        ("name", r"name:\s*[\"']?([^\"'\n]+)"),
        ("category", r"category:\s*[\"']?([^\"'\n]+)"),
        ("domain", r"domain:\s*[\"']?([^\"'\n]+)"),
        ("tender_url", r"tender_url:\s*[\"']?([^\"'\n]+)"),
        ("homepage", r"homepage:\s*[\"']?([^\"'\n]+)"),
        ("enabled", r"enabled:\s*(true|false)"),
        ("method", r"method:\s*[\"']?([^\"'\n]+)"),
        ("schedule", r"schedule:\s*[\"']?([^\"'\n]+)"),
    ]:
        m = re.search(pattern, content, re.IGNORECASE)
        if m:
            val = m.group(1).strip().strip("'\"")
            if key == "enabled":
                val = val.lower() == "true"
            info[key] = val

    return info


def _get_user_slugs(user: User, db: Session) -> set:
    """Get the set of institution slugs the user follows."""
    rows = db.query(UserInstitution.institution_slug).filter(
        UserInstitution.user_id == user.id
    ).all()
    return {r[0] for r in rows}


# ── User Institution Following ──────────────────────────────────────────────

@app.get("/api/me/institutions")
def get_my_institutions(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's followed institutions."""
    follows = db.query(UserInstitution).filter(
        UserInstitution.user_id == user.id
    ).all()
    slugs = [f.institution_slug for f in follows]

    institutions = []
    for slug in slugs:
        inst_dir = INSTITUTIONS_DIR / slug
        if not inst_dir.exists():
            continue
        info = parse_readme_frontmatter(inst_dir / "README.md")
        info["slug"] = slug
        active_dir = inst_dir / "tenders" / "active"
        info["active_tenders"] = len(list(active_dir.glob("*.json"))) if active_dir.exists() else 0
        last_scrape = load_json(inst_dir / "last_scrape.json", {})
        info["last_scraped"] = last_scrape.get("last_scrape")
        info["followed"] = True
        institutions.append(info)

    return {"institutions": institutions, "total": len(institutions)}


class FollowRequest(BaseModel):
    slug: str


@app.post("/api/me/institutions")
def follow_institution(
    req: FollowRequest,
    user: User = Depends(check_institution_limit),
    db: Session = Depends(get_db),
):
    """Follow an institution."""
    inst_dir = INSTITUTIONS_DIR / req.slug
    if not inst_dir.exists():
        raise HTTPException(404, f"Institution '{req.slug}' not found")

    existing = db.query(UserInstitution).filter(
        UserInstitution.user_id == user.id,
        UserInstitution.institution_slug == req.slug,
    ).first()
    if existing:
        return {"status": "already_following"}

    db.add(UserInstitution(user_id=user.id, institution_slug=req.slug))
    db.commit()
    return {"status": "followed", "slug": req.slug}


@app.delete("/api/me/institutions/{slug}")
def unfollow_institution(
    slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Unfollow an institution."""
    row = db.query(UserInstitution).filter(
        UserInstitution.user_id == user.id,
        UserInstitution.institution_slug == slug,
    ).first()
    if row:
        db.delete(row)
        db.commit()
    return {"status": "unfollowed", "slug": slug}


# ── User Applications (Phase 4) ────────────────────────────────────────────

class CreateApplicationRequest(BaseModel):
    tender_id: str
    institution_slug: str
    status: str = "interested"
    notes: Optional[str] = None


class UpdateApplicationRequest(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


@app.get("/api/me/applications")
def get_my_applications(
    status: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's tracked applications."""
    q = db.query(UserApplication).filter(UserApplication.user_id == user.id)
    if status:
        q = q.filter(UserApplication.status == status)
    if search:
        q = q.filter(UserApplication.tender_id.contains(search))

    total = q.count()
    apps = q.order_by(UserApplication.created_at.desc()).offset(offset).limit(limit).all()

    results = []
    for app_row in apps:
        # Enrich with tender data from filesystem
        tender_data = {}
        for tender_file in INSTITUTIONS_DIR.rglob(f"tenders/*/{app_row.tender_id}.json"):
            tender_data = load_json(tender_file, {})
            break

        results.append({
            "id": app_row.id,
            "tender_id": app_row.tender_id,
            "institution_slug": app_row.institution_slug,
            "status": app_row.status,
            "notes": app_row.notes,
            "submitted_at": app_row.submitted_at.isoformat() if app_row.submitted_at else None,
            "created_at": app_row.created_at.isoformat() if app_row.created_at else None,
            "title": tender_data.get("title", ""),
            "closing_date": tender_data.get("closing_date"),
            "days_remaining": days_until(tender_data.get("closing_date")),
            "category": tender_data.get("category"),
        })

    return {"total": total, "applications": results, "offset": offset, "limit": limit}


@app.post("/api/me/applications")
def create_application(
    req: CreateApplicationRequest,
    user: User = Depends(check_application_limit),
    db: Session = Depends(get_db),
):
    """Track a tender application."""
    existing = db.query(UserApplication).filter(
        UserApplication.user_id == user.id,
        UserApplication.tender_id == req.tender_id,
    ).first()
    if existing:
        raise HTTPException(409, "Already tracking this tender")

    app_row = UserApplication(
        user_id=user.id,
        tender_id=req.tender_id,
        institution_slug=req.institution_slug,
        status=req.status,
        notes=req.notes,
    )
    db.add(app_row)
    user.applications_this_month += 1
    db.commit()
    db.refresh(app_row)

    return {"id": app_row.id, "status": "created"}


@app.put("/api/me/applications/{app_id}")
def update_application(
    app_id: int,
    req: UpdateApplicationRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a tracked application."""
    app_row = db.query(UserApplication).filter(
        UserApplication.id == app_id,
        UserApplication.user_id == user.id,
    ).first()
    if not app_row:
        raise HTTPException(404, "Application not found")

    if req.status is not None:
        app_row.status = req.status
        if req.status in ("submitted", "sent"):
            app_row.submitted_at = datetime.utcnow()
    if req.notes is not None:
        app_row.notes = req.notes
    app_row.updated_at = datetime.utcnow()
    db.commit()

    return {"status": "updated"}


@app.delete("/api/me/applications/{app_id}")
def delete_application(
    app_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a tracked application."""
    app_row = db.query(UserApplication).filter(
        UserApplication.id == app_id,
        UserApplication.user_id == user.id,
    ).first()
    if not app_row:
        raise HTTPException(404, "Application not found")

    db.delete(app_row)
    db.commit()
    return {"status": "deleted"}


# ── Company Documents ────────────────────────────────────────────────────────

@app.get("/api/me/company-docs")
def list_company_docs(user: User = Depends(get_current_user)):
    """List files in user's company documents folder."""
    docs_dir = _get_company_docs_dir(user)
    files = []
    for f in sorted(docs_dir.iterdir()):
        if f.is_file() and not f.name.startswith('.'):
            files.append({
                "filename": f.name,
                "size": f.stat().st_size,
                "uploaded_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })
    return {"docs_dir": str(docs_dir), "files": files}


@app.post("/api/me/company-docs")
async def upload_company_doc(
    file: UploadFile = FastAPIFile(...),
    user: User = Depends(get_current_user),
):
    """Upload a document to the user's company folder."""
    ALLOWED_EXT = {'.pdf', '.doc', '.docx', '.txt', '.md', '.jpg', '.jpeg', '.png', '.xlsx', '.xls'}
    MAX_SIZE = 20 * 1024 * 1024  # 20MB

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"File type {ext} not allowed. Allowed: {', '.join(ALLOWED_EXT)}")

    docs_dir = _get_company_docs_dir(user)
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "File too large (max 20MB)")

    dest = docs_dir / file.filename
    dest.write_bytes(content)
    return {"filename": file.filename, "size": len(content), "path": str(dest)}


@app.delete("/api/me/company-docs/{filename}")
def delete_company_doc(
    filename: str,
    user: User = Depends(get_current_user),
):
    """Delete a document from the user's company folder."""
    docs_dir = _get_company_docs_dir(user)
    filepath = docs_dir / filename
    if not filepath.exists() or not filepath.is_file():
        raise HTTPException(404, "File not found")
    # Security: ensure file is actually inside the docs dir
    if not str(filepath.resolve()).startswith(str(docs_dir.resolve())):
        raise HTTPException(403, "Access denied")
    filepath.unlink()
    return {"status": "deleted", "filename": filename}


@app.get("/api/me/company-docs/{filename}")
def download_company_doc(
    filename: str,
    user: User = Depends(get_current_user),
):
    """Download a document from the user's company folder."""
    docs_dir = _get_company_docs_dir(user)
    filepath = docs_dir / filename
    if not filepath.exists() or not filepath.is_file():
        raise HTTPException(404, "File not found")
    if not str(filepath.resolve()).startswith(str(docs_dir.resolve())):
        raise HTTPException(403, "Access denied")
    return FileResponse(filepath, filename=filename)


# ── Stats ────────────────────────────────────────────────────────────────────

@app.get("/api/stats")
def get_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Dashboard overview stats — scoped to user's followed institutions."""
    active_tenders = []
    for tender_file in INSTITUTIONS_DIR.rglob("tenders/active/*.json"):
        slug = str(tender_file).split("/institutions/")[1].split("/")[0]
        t = load_json(tender_file, {})
        if t:
            t["_file"] = str(tender_file)
            t["institution_slug"] = slug
            active_tenders.append(t)

    total_institutions = sum(
        1 for d in INSTITUTIONS_DIR.iterdir()
        if d.is_dir() and (d / "README.md").exists()
    )
    closing_soon = []
    for t in active_tenders:
        dr = days_until(t.get("closing_date"))
        if dr is not None and 0 <= dr <= 7:
            t["days_remaining"] = dr
            closing_soon.append(t)
    closing_soon.sort(key=lambda x: x.get("days_remaining", 999))

    # User's applications from DB
    user_apps = db.query(UserApplication).filter(UserApplication.user_id == user.id).all()
    submitted = sum(1 for a in user_apps if a.status in ("submitted", "sent"))
    pending = sum(1 for a in user_apps if a.status not in ("submitted", "sent"))

    leads = load_json(OPPORTUNITIES_DIR / "leads.json", [])
    pending_leads = sum(1 for l in leads if l.get("status") == "pending")

    categories = {}
    for t in active_tenders:
        cat = t.get("category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1

    inst_with_tenders = len(set(
        t.get("institution_slug", "") for t in active_tenders
    ))

    state_file = SCRIPTS_DIR / ".smart_scrape_state.json"
    last_scrape = load_json(state_file, {})

    # Plan info
    plan_info = get_user_plan_info(user, db)

    return {
        "active_tenders": len(active_tenders),
        "total_institutions": total_institutions,
        "followed_institutions": len(_get_user_slugs(user, db)),
        "institutions_with_tenders": inst_with_tenders,
        "closing_soon": len(closing_soon),
        "closing_soon_tenders": closing_soon[:10],
        "applications_submitted": submitted,
        "applications_pending": pending,
        "total_applications": len(user_apps),
        "total_leads": len(leads),
        "pending_leads": pending_leads,
        "categories": dict(sorted(categories.items(), key=lambda x: -x[1])),
        "last_scrape": last_scrape.get("stats", {}),
        "last_scrape_date": last_scrape.get("date"),
        "plan": plan_info,
    }


# ── Tenders ──────────────────────────────────────────────────────────────────

@app.get("/api/tenders")
def list_tenders(
    status: Optional[str] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return tenders with a status field. If status param given, returns only
    that status (backward compat). Otherwise returns all statuses."""
    tenders = []
    statuses = [status] if status else ["active", "closed", "archive"]

    for status_dir in statuses:
        if status_dir not in ("active", "closed", "archive"):
            continue
        for tender_file in INSTITUTIONS_DIR.rglob(f"tenders/{status_dir}/*.json"):
            slug = str(tender_file).split("/institutions/")[1].split("/")[0]
            t = load_json(tender_file, {})
            if not t:
                continue
            t["institution_slug"] = slug
            t["status"] = status_dir
            t["days_remaining"] = days_until(t.get("closing_date"))
            tenders.append(t)

    tenders.sort(key=lambda x: x.get("closing_date") or "9999-12-31")
    return {"tenders": tenders}


@app.get("/api/tenders/{tender_id}")
def get_tender(
    tender_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific tender by ID."""
    for tender_file in INSTITUTIONS_DIR.rglob(f"tenders/*/{tender_id}.json"):
        slug = str(tender_file).split("/institutions/")[1].split("/")[0]

        t = load_json(tender_file, {})
        if t:
            t["institution_slug"] = slug
            t["days_remaining"] = days_until(t.get("closing_date"))

            download_dir = INSTITUTIONS_DIR / slug / "downloads" / tender_id / "original"
            if download_dir.exists():
                t["local_files"] = [f.name for f in download_dir.iterdir() if f.is_file()]

            extract_dir = INSTITUTIONS_DIR / slug / "downloads" / tender_id / "extracted"
            if extract_dir.exists():
                t["extracted_files"] = [f.name for f in extract_dir.iterdir() if f.is_file()]

            # Check if user is tracking this tender
            app_row = db.query(UserApplication).filter(
                UserApplication.user_id == user.id,
                UserApplication.tender_id == tender_id,
            ).first()
            if app_row:
                t["user_application"] = {
                    "id": app_row.id,
                    "status": app_row.status,
                    "notes": app_row.notes,
                }

            # Check for prepared application PDF (user-scoped)
            user_pdf_dir = APPLICATIONS_DIR / "pdfs" / f"user_{user.id}"
            t["application_pdf"] = None
            if user_pdf_dir.exists():
                for f in user_pdf_dir.glob(f"*{tender_id}*"):
                    if f.suffix.lower() == ".pdf":
                        t["application_pdf"] = {
                            "filename": f.name,
                            "size": f.stat().st_size,
                            "url": f"/api/applications/pdfs/{tender_id}",
                        }
                        break

            # Check for cached pitch (user-scoped)
            user_pitch_file = user_pdf_dir / "pitches" / f"{tender_id}_pitch.json"
            t["pitch"] = None
            if user_pitch_file.exists():
                t["pitch"] = load_json(user_pitch_file, {})

            # Build downloadable document URLs
            if t.get("local_files"):
                t["downloadable_docs"] = [
                    {
                        "filename": fname,
                        "url": f"/api/documents/{slug}/{tender_id}/{fname}",
                    }
                    for fname in t["local_files"]
                ]

            return t

    raise HTTPException(404, f"Tender {tender_id} not found")


# ── Applications (legacy + user-scoped) ──────────────────────────────────────

@app.get("/api/applications")
def list_applications(
    status: Optional[str] = None,
    urgency: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = "closing_date",
    limit: int = 100,
    offset: int = 0,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List user's applications from DB, enriched with tender data."""
    return get_my_applications(status=status, search=search, limit=limit, offset=offset, user=user, db=db)


@app.get("/api/sent-log")
def get_sent_log(
    limit: int = 50,
    user: User = Depends(get_current_user),
):
    log = load_json(APPLICATIONS_DIR / "sent_log.json", [])
    log.sort(key=lambda x: x.get("sent_at", ""), reverse=True)
    return {"total": len(log), "entries": log[:limit]}


# ── Application Preparation & Sending ────────────────────────────────────────

_active_jobs = {}


def _get_company_docs_dir(user: User) -> Path:
    """Get or create the company documents directory for a user under frontend/public/company_documents/."""
    profile = {}
    if user.company_profile:
        try:
            profile = json.loads(user.company_profile) if isinstance(user.company_profile, str) else user.company_profile
        except Exception:
            pass

    # Derive folder name from company name or user ID
    company_name = profile.get("company_name") or user.company or f"user_{user.id}"
    folder_name = re.sub(r'[^a-zA-Z0-9]+', '_', company_name).strip('_').lower()
    docs_dir = COMPANY_DOCS_BASE / folder_name
    docs_dir.mkdir(parents=True, exist_ok=True)
    return docs_dir


def _write_company_profile(user: User) -> Optional[Path]:
    """Write user's company profile to a temp JSON file for the generate script."""
    if not user.company_profile:
        return None
    try:
        profile = json.loads(user.company_profile) if isinstance(user.company_profile, str) else user.company_profile
        # Merge user name/email/company into profile for convenience
        profile.setdefault("contact_email", user.email)
        if user.name:
            profile.setdefault("contact_person", user.name)
        if user.company:
            profile.setdefault("company_name", user.company)

        # Set company documents directory
        docs_dir = _get_company_docs_dir(user)
        profile["company_docs_dir"] = str(docs_dir)

        profile_path = APPLICATIONS_DIR / "profiles" / f"user_{user.id}_profile.json"
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        profile_path.write_text(json.dumps(profile, indent=2))
        return profile_path
    except Exception:
        return None


def _run_job(job_id: str, cmd: list, tender_ids: list):
    try:
        env = {k: v for k, v in os.environ.items()
               if not k.startswith("CLAUDE")}
        env["PATH"] = os.environ.get("PATH", "/usr/bin:/usr/local/bin")

        _active_jobs[job_id]["status"] = "running"
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600,
            cwd=str(PROJECT), env=env
        )

        def sanitize(s):
            if not s:
                return ""
            import re as _re
            return _re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', s)

        _active_jobs[job_id]["stdout"] = sanitize(result.stdout[-5000:])
        _active_jobs[job_id]["stderr"] = sanitize(result.stderr[-2000:])
        _active_jobs[job_id]["returncode"] = result.returncode
        _active_jobs[job_id]["status"] = "completed" if result.returncode == 0 else "failed"
    except subprocess.TimeoutExpired:
        _active_jobs[job_id]["status"] = "timeout"
    except Exception as e:
        _active_jobs[job_id]["status"] = "error"
        _active_jobs[job_id]["error"] = str(e)


@app.post("/api/applications/prepare")
def prepare_applications(
    background_tasks: BackgroundTasks,
    tender_ids: List[str] = Body(..., embed=True),
    user: User = Depends(check_application_limit),
):
    job_id = f"prepare_{datetime.now().strftime('%H%M%S')}"
    results = []

    # Write user's company profile to a temp file for the script
    profile_path = _write_company_profile(user)

    # Each user gets their own output directory
    user_pdf_dir = APPLICATIONS_DIR / "pdfs" / f"user_{user.id}"
    user_pdf_dir.mkdir(parents=True, exist_ok=True)

    for tid in tender_ids:
        sub_job_id = f"{job_id}_{tid}"
        _active_jobs[sub_job_id] = {
            "type": "prepare", "status": "queued",
            "tender_id": tid, "results": []
        }
        cmd = [
            "python3", str(APPLICATIONS_DIR / "generate_and_send.py"),
            "--tender-id", tid, "--pdf-only",
            "--output-dir", str(user_pdf_dir),
        ]
        if profile_path:
            cmd.extend(["--company-profile", str(profile_path)])
        background_tasks.add_task(_run_job, sub_job_id, cmd, [tid])
        results.append({"tender_id": tid, "job_id": sub_job_id, "status": "queued"})

    return {"status": "started", "jobs": results, "total": len(tender_ids)}


@app.post("/api/applications/apply")
def apply_to_tenders(
    background_tasks: BackgroundTasks,
    tender_ids: List[str] = Body(..., embed=True),
    dry_run: bool = Body(False, embed=True),
    user: User = Depends(check_application_limit),
):
    job_id = f"apply_{datetime.now().strftime('%H%M%S')}"
    results = []

    profile_path = _write_company_profile(user)
    user_pdf_dir = APPLICATIONS_DIR / "pdfs" / f"user_{user.id}"
    user_pdf_dir.mkdir(parents=True, exist_ok=True)

    for tid in tender_ids:
        sub_job_id = f"{job_id}_{tid}"
        _active_jobs[sub_job_id] = {
            "type": "apply", "status": "queued",
            "tender_id": tid, "results": []
        }
        cmd = [
            "python3", str(APPLICATIONS_DIR / "generate_and_send.py"),
            "--tender-id", tid,
            "--output-dir", str(user_pdf_dir),
        ]
        if profile_path:
            cmd.extend(["--company-profile", str(profile_path)])
        if dry_run:
            cmd.append("--dry-run")
        background_tasks.add_task(_run_job, sub_job_id, cmd, [tid])
        results.append({"tender_id": tid, "job_id": sub_job_id, "status": "queued"})

    return {"status": "started", "jobs": results, "total": len(tender_ids)}


@app.get("/api/applications/jobs")
def list_jobs(user: User = Depends(get_current_user)):
    return {
        "jobs": {k: {kk: vv for kk, vv in v.items() if kk != "process"}
                 for k, v in _active_jobs.items()}
    }


@app.get("/api/applications/jobs/{job_id}")
def get_job(job_id: str, user: User = Depends(get_current_user)):
    job = _active_jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return {k: v for k, v in job.items() if k != "process"}


@app.get("/api/applications/pdfs/{tender_id}")
def get_application_pdf(
    tender_id: str,
    user: User = Depends(get_current_user),
):
    user_pdf_dir = APPLICATIONS_DIR / "pdfs" / f"user_{user.id}"
    if user_pdf_dir.exists():
        for f in user_pdf_dir.glob(f"*{tender_id}*"):
            if f.suffix.lower() == ".pdf":
                return FileResponse(f, media_type="application/pdf", filename=f.name)

    raise HTTPException(404, f"No PDF found for {tender_id}")


@app.get("/api/applications/pdf-exists/{tender_id}")
def check_pdf_exists(
    tender_id: str,
    user: User = Depends(get_current_user),
):
    user_pdf_dir = APPLICATIONS_DIR / "pdfs" / f"user_{user.id}"
    if user_pdf_dir.exists():
        for f in user_pdf_dir.glob(f"*{tender_id}*"):
            if f.suffix.lower() == ".pdf":
                return {"exists": True, "filename": f.name}

    return {"exists": False}


@app.get("/api/applications/{tender_id}")
def get_application(
    tender_id: str,
    user: User = Depends(get_current_user),
):
    db = load_json(APPLICATIONS_DIR / "requirements_database.json", [])
    for r in db:
        if r.get("tender_id") == tender_id:
            r["days_remaining"] = days_until(r.get("closing_date"))
            return r
    raise HTTPException(404, f"Application for {tender_id} not found")


# ── Opportunities ────────────────────────────────────────────────────────────

@app.get("/api/opportunities")
def list_opportunities(
    status: Optional[str] = None,
    opportunity_type: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List all opportunities (admin only)."""
    leads = load_json(OPPORTUNITIES_DIR / "leads.json", [])

    if status:
        leads = [l for l in leads if l.get("status", "").lower() == status.lower()]
    if opportunity_type:
        leads = [l for l in leads if l.get("opportunity_type", "").lower() == opportunity_type.lower()]
    if search:
        leads = [l for l in leads if search.lower() in
                 f"{l.get('institution_name','')} {l.get('opportunity_description','')}".lower()]

    total = len(leads)
    return {"total": total, "leads": leads[offset:offset + limit], "offset": offset, "limit": limit}


# ── Institutions ─────────────────────────────────────────────────────────────

@app.get("/api/institutions")
def list_institutions(
    enabled: Optional[bool] = None,
    category: Optional[str] = None,
    has_tenders: Optional[bool] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all institutions with followed status."""
    user_slugs = _get_user_slugs(user, db)
    institutions = []

    for d in sorted(INSTITUTIONS_DIR.iterdir()):
        if not d.is_dir() or not (d / "README.md").exists():
            continue

        slug = d.name
        info = parse_readme_frontmatter(d / "README.md")
        info["slug"] = slug

        active_dir = d / "tenders" / "active"
        active_count = len(list(active_dir.glob("*.json"))) if active_dir.exists() else 0
        closed_dir = d / "tenders" / "closed"
        closed_count = len(list(closed_dir.glob("*.json"))) if closed_dir.exists() else 0
        info["active_tenders"] = active_count
        info["closed_tenders"] = closed_count

        last_scrape = load_json(d / "last_scrape.json", {})
        info["last_scraped"] = last_scrape.get("last_scrape")
        info["last_scrape_status"] = last_scrape.get("status")
        info["followed"] = slug in user_slugs

        is_enabled = info.get("enabled", True)
        if enabled is not None and is_enabled != enabled:
            continue
        if category and info.get("category", "").lower() != category.lower():
            continue
        if has_tenders is True and active_count == 0:
            continue
        if has_tenders is False and active_count > 0:
            continue
        if search and search.lower() not in f"{slug} {info.get('name','')} {info.get('category','')}".lower():
            continue

        institutions.append(info)

    total = len(institutions)
    return {"total": total, "institutions": institutions[offset:offset + limit], "offset": offset, "limit": limit}


@app.get("/api/institutions/{slug}")
def get_institution(
    slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    inst_dir = INSTITUTIONS_DIR / slug
    if not inst_dir.exists():
        raise HTTPException(404, f"Institution {slug} not found")

    user_slugs = _get_user_slugs(user, db)
    info = parse_readme_frontmatter(inst_dir / "README.md")
    info["slug"] = slug
    info["followed"] = slug in user_slugs

    active_dir = inst_dir / "tenders" / "active"
    info["active_tenders"] = []
    if active_dir.exists():
        for f in active_dir.glob("*.json"):
            t = load_json(f, {})
            if t:
                t["days_remaining"] = days_until(t.get("closing_date"))
                info["active_tenders"].append(t)

    info["last_scrape"] = load_json(inst_dir / "last_scrape.json", {})

    return info


# ── Plans ────────────────────────────────────────────────────────────────────

@app.get("/api/plans")
def list_plans(db: Session = Depends(get_db)):
    """List all available plans (public endpoint)."""
    plans = db.query(Plan).all()
    return {
        "plans": [
            {
                "id": p.id,
                "name": p.name,
                "price_monthly": p.price_monthly,
                "max_institutions": p.max_institutions,
                "max_applications_per_month": p.max_applications_per_month,
                "can_download_documents": p.can_download_documents,
                "can_control_scraper": p.can_control_scraper,
                "has_api_access": p.has_api_access,
                "has_email_alerts": p.has_email_alerts,
            }
            for p in plans
        ]
    }


# ── Scraper Controls ─────────────────────────────────────────────────────────

class ScrapeRequest(BaseModel):
    slug: Optional[str] = None
    agent_batch: int = 8
    workers: int = 1


_scrape_process = None


@app.post("/api/scrape/start")
def start_scrape(
    req: ScrapeRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(require_admin),
):
    global _scrape_process

    pid_file = LOGS_DIR / "scraper.pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)
            return {"status": "already_running", "pid": pid}
        except (ProcessLookupError, ValueError):
            pid_file.unlink(missing_ok=True)

    cmd = ["python3", str(SCRIPTS_DIR / "smart_scrape.py"),
           "--agent-batch", str(req.agent_batch),
           "--workers", str(req.workers)]
    if req.slug:
        cmd.extend(["--slug", req.slug])

    _scrape_process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    return {"status": "started", "pid": _scrape_process.pid}


@app.get("/api/scrape/status")
def scrape_status(user: User = Depends(require_admin)):
    pid_file = LOGS_DIR / "scraper.pid"
    running = False
    pid = None

    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)
            running = True
        except (ProcessLookupError, ValueError):
            pass

    state = load_json(SCRIPTS_DIR / ".smart_scrape_state.json", {})

    log_file = LOGS_DIR / f"scrape_master_{date.today().strftime('%Y%m%d')}.log"
    last_lines = []
    if log_file.exists():
        lines = log_file.read_text().strip().split("\n")
        last_lines = lines[-10:]

    return {
        "running": running,
        "pid": pid,
        "state": state,
        "last_log_lines": last_lines,
    }


@app.post("/api/scrape/stop")
def stop_scrape(user: User = Depends(require_admin)):
    pid_file = LOGS_DIR / "scraper.pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            return {"status": "stopped", "pid": pid}
        except (ProcessLookupError, ValueError):
            return {"status": "not_running"}
    return {"status": "not_running"}


# ── Notifications ────────────────────────────────────────────────────────────

@app.get("/api/notifications")
def list_notifications(
    limit: int = 20,
    user: User = Depends(get_current_user),
):
    sent_dir = NOTIFICATIONS_DIR / "sent"
    pending_dir = NOTIFICATIONS_DIR / "pending"

    notifications = []
    if sent_dir.exists():
        for f in sorted(sent_dir.glob("*.json"), reverse=True)[:limit]:
            n = load_json(f, {})
            if n:
                n["_type"] = "sent"
                n["_file"] = f.name
                notifications.append(n)

    if pending_dir.exists():
        for f in sorted(pending_dir.glob("*.json"), reverse=True)[:limit]:
            n = load_json(f, {})
            if n:
                n["_type"] = "pending"
                n["_file"] = f.name
                notifications.append(n)

    return {"notifications": notifications[:limit]}


# ── Document Access ──────────────────────────────────────────────────────────

@app.get("/api/documents/{slug}/{tender_id}/{filename}")
def get_document(
    slug: str,
    tender_id: str,
    filename: str,
    user: User = Depends(check_download_access),
):
    file_path = INSTITUTIONS_DIR / slug / "downloads" / tender_id / "original" / filename
    if not file_path.exists():
        raise HTTPException(404, "Document not found")
    return FileResponse(file_path)


@app.get("/api/documents/{slug}/{tender_id}/{filename}/text")
def get_document_text(
    slug: str,
    tender_id: str,
    filename: str,
    user: User = Depends(get_current_user),
):
    txt_name = Path(filename).stem + ".txt"
    text_path = INSTITUTIONS_DIR / slug / "downloads" / tender_id / "extracted" / txt_name
    if text_path.exists():
        return {"text": text_path.read_text(errors="ignore")}

    orig = INSTITUTIONS_DIR / slug / "downloads" / tender_id / "original" / filename
    if orig.exists() and orig.suffix.lower() == ".pdf":
        try:
            result = subprocess.run(
                ["python3", "-m", "tools", "pdf", "read", str(orig)],
                capture_output=True, text=True, timeout=30,
                cwd=str(PROJECT)
            )
            if result.returncode == 0:
                return {"text": result.stdout}
        except Exception:
            pass

    raise HTTPException(404, "Extracted text not found")


# ── Serve Frontend ───────────────────────────────────────────────────────────

FRONTEND_DIST = Path(__file__).parent.parent / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        return FileResponse(FRONTEND_DIST / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
