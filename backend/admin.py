"""
Admin API endpoints — system management for admin users.
All endpoints require admin authentication.
"""
import re
import secrets
import subprocess
from datetime import datetime, date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth import require_admin, hash_password, user_to_dict
from database import get_db, User, UserInstitution, UserApplication, Plan

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
INSTITUTIONS_DIR = PROJECT / "institutions"
LOGS_DIR = PROJECT / "logs"
SCRIPTS_DIR = PROJECT / "scripts"

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_admin)])


# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_json(path, default=None):
    import json
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else []


def _parse_readme_frontmatter(readme_path: Path) -> dict:
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


# ── Dashboard Stats ──────────────────────────────────────────────────────────

@router.get("/stats")
def admin_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()

    # Users by plan
    plan_counts = {}
    for plan_id, count in db.query(User.plan, func.count(User.id)).group_by(User.plan).all():
        plan_counts[plan_id or "free"] = count

    # MRR calculation
    plans = {p.id: p for p in db.query(Plan).all()}
    mrr = 0
    for plan_id, count in plan_counts.items():
        plan = plans.get(plan_id)
        if plan and plan.price_monthly > 0:
            active_paying = db.query(User).filter(
                User.plan == plan_id,
                User.subscription_status == "active",
            ).count()
            mrr += plan.price_monthly * active_paying

    # Active subscriptions
    active_subs = db.query(User).filter(
        User.subscription_status == "active",
        User.plan != "free",
    ).count()

    # Recent signups (last 10)
    recent = db.query(User).order_by(User.created_at.desc()).limit(10).all()
    recent_signups = [
        {
            "id": u.id, "email": u.email, "name": u.name,
            "plan": u.plan, "company": u.company,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in recent
    ]

    # Scraper health
    state = _load_json(SCRIPTS_DIR / ".smart_scrape_state.json", {})
    pid_file = LOGS_DIR / "scraper.pid"
    scraper_running = False
    if pid_file.exists():
        try:
            import os
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)
            scraper_running = True
        except (ProcessLookupError, ValueError):
            pass

    # Institution counts
    total_institutions = sum(
        1 for d in INSTITUTIONS_DIR.iterdir()
        if d.is_dir() and (d / "README.md").exists()
    )
    enabled_institutions = 0
    total_active_tenders = 0
    for d in INSTITUTIONS_DIR.iterdir():
        if not d.is_dir() or not (d / "README.md").exists():
            continue
        info = _parse_readme_frontmatter(d / "README.md")
        if info.get("enabled", True):
            enabled_institutions += 1
        active_dir = d / "tenders" / "active"
        if active_dir.exists():
            total_active_tenders += len(list(active_dir.glob("*.json")))

    return {
        "total_users": total_users,
        "users_by_plan": plan_counts,
        "mrr": mrr,
        "active_subscriptions": active_subs,
        "recent_signups": recent_signups,
        "scraper_running": scraper_running,
        "last_scrape": state.get("date"),
        "last_scrape_stats": state.get("stats", {}),
        "total_institutions": total_institutions,
        "enabled_institutions": enabled_institutions,
        "total_active_tenders": total_active_tenders,
    }


# ── Users ────────────────────────────────────────────────────────────────────

@router.get("/users")
def admin_list_users(
    search: Optional[str] = None,
    plan: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(User)
    if search:
        q = q.filter(
            (User.email.ilike(f"%{search}%")) |
            (User.name.ilike(f"%{search}%")) |
            (User.company.ilike(f"%{search}%"))
        )
    if plan:
        q = q.filter(User.plan == plan)
    if status:
        q = q.filter(User.subscription_status == status)

    total = q.count()
    users = q.order_by(User.created_at.desc()).offset(offset).limit(limit).all()

    results = []
    for u in users:
        inst_count = db.query(UserInstitution).filter(UserInstitution.user_id == u.id).count()
        app_count = db.query(UserApplication).filter(UserApplication.user_id == u.id).count()
        results.append({
            "id": u.id, "email": u.email, "name": u.name,
            "company": u.company, "plan": u.plan,
            "subscription_status": u.subscription_status,
            "is_admin": u.is_admin, "email_verified": u.email_verified,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "institutions_count": inst_count,
            "applications_count": app_count,
        })

    return {"total": total, "users": results, "offset": offset, "limit": limit}


@router.get("/users/{user_id}")
def admin_get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    user_dict = user_to_dict(user, db)

    # Followed institutions
    follows = db.query(UserInstitution).filter(UserInstitution.user_id == user.id).all()
    user_dict["followed_institutions_list"] = [
        {"slug": f.institution_slug, "followed_at": f.followed_at.isoformat() if f.followed_at else None}
        for f in follows
    ]

    # Applications
    apps = db.query(UserApplication).filter(UserApplication.user_id == user.id).order_by(
        UserApplication.created_at.desc()
    ).all()
    user_dict["applications_list"] = [
        {
            "id": a.id, "tender_id": a.tender_id,
            "institution_slug": a.institution_slug,
            "status": a.status, "notes": a.notes,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in apps
    ]

    return user_dict


class AdminUpdateUserRequest(BaseModel):
    plan: Optional[str] = None
    is_admin: Optional[bool] = None
    subscription_status: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None


@router.put("/users/{user_id}")
def admin_update_user(user_id: int, req: AdminUpdateUserRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    if req.plan is not None:
        # Validate plan exists
        if not db.query(Plan).filter(Plan.id == req.plan).first():
            raise HTTPException(400, f"Plan '{req.plan}' does not exist")
        user.plan = req.plan
    if req.is_admin is not None:
        user.is_admin = req.is_admin
    if req.subscription_status is not None:
        user.subscription_status = req.subscription_status
    if req.name is not None:
        user.name = req.name
    if req.company is not None:
        user.company = req.company

    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)

    return user_to_dict(user, db)


@router.post("/users/{user_id}/reset-password")
def admin_reset_password(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    temp_password = secrets.token_urlsafe(12)
    user.password_hash = hash_password(temp_password)
    user.updated_at = datetime.utcnow()
    db.commit()

    return {"status": "ok", "temp_password": temp_password}


# ── Institutions ─────────────────────────────────────────────────────────────

# Track background institution creation jobs
_create_jobs = {}


def _url_to_slug(url: str) -> str:
    """Derive a slug from a URL: https://www.whizztanzania.com/ → whizztanzania"""
    domain = url.replace("https://", "").replace("http://", "").rstrip("/")
    # Strip www.
    if domain.startswith("www."):
        domain = domain[4:]
    # Take the domain name part (before TLD)
    slug = domain.split(".")[0]
    slug = re.sub(r'[^a-z0-9-]', '', slug.lower())
    return slug


def _run_create_institution(job_id: str, slug: str, homepage: str):
    """Background task: create institution folder, let AI visit the site and generate full README."""
    import os

    try:
        _create_jobs[job_id]["status"] = "creating_folder"

        inst_dir = INSTITUTIONS_DIR / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
        (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)

        # Run Agent CLI to visit the website and create the full README
        _create_jobs[job_id]["status"] = "analyzing"

        agent_bin = "/Users/andrewmashamba/.local/bin/claude"
        if not os.path.isfile(agent_bin):
            agent_bin = "/Users/andrewmashamba/.local/bin/agent"

        # Read a reference README so the AI knows the exact format
        reference_readme = INSTITUTIONS_DIR / "crdb-bank" / "README.md"
        ref_note = ""
        if reference_readme.exists():
            ref_note = f"\n\nUse this existing README as the FORMAT REFERENCE (same YAML structure, same sections):\n{reference_readme}\nRead it first to understand the exact format expected."

        readme_path = inst_dir / "README.md"
        prompt = f"""You are a website analysis agent. Your task is to create a complete institution README.md for the TENDERS scraper system.

## Website to analyze
{homepage}

## Output file
Write the complete README.md to: {readme_path}

## What to do

1. Fetch {homepage} using curl or WebFetch
2. Explore the website to find:
   - The institution's ACTUAL name (from the page title, header, or about page)
   - What category they are (Commercial Bank, Microfinance, SACCO, Government, Insurance, NGO, or Commercial / Private Sector)
   - The tender/procurement page URL (look for links like "Tenders", "Procurement", "Careers", "Notices" etc.)
   - If no dedicated tender page exists, use the homepage as tender_url
3. Analyze the tender page HTML to find:
   - CSS selectors for the tender listing container
   - CSS selectors for individual tender items
   - CSS selectors for tender titles, dates, and document links
   - Pagination selectors if pagination exists
   - Document download paths and URL patterns
   - Whether the site requires JavaScript (SPA/React/Angular/Vue)
4. Write a complete README.md to {readme_path} with all this information{ref_note}

## Required YAML frontmatter fields
- institution.name — the ACTUAL institution name from the website
- institution.slug — "{slug}"
- institution.category — determined from the website content
- institution.status — "active"
- institution.country — "Tanzania"
- website.homepage — "{homepage}"
- website.tender_url — the actual tender page URL you found (or homepage if none)
- scraping.enabled — true (or false if site is down/no procurement section)
- scraping.method — "http_get"
- scraping.strategy — specific, actionable scraping instructions for THIS site
- scraping.selectors — ACTUAL CSS selectors from the real HTML (not generic placeholders)
- scraping.schedule — "daily"
- scraping.anti_bot — actual values (requires_javascript, has_captcha, rate_limit_seconds)
- scraping.documents — download settings with actual file types found
- scraping.output — format and fields

## Rules
- Use ONLY information from the ACTUAL website — do not guess or use placeholders
- If you cannot reach the site, set enabled: false and note why
- If no tender page exists, note this in the strategy and set tender_url to homepage
- The README must be complete and ready for the scraper to use immediately

Project directory: {PROJECT}"""

        env = {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE")}
        env["PATH"] = os.environ.get("PATH", "/usr/bin:/usr/local/bin")

        cmd = [agent_bin, '-p', '--force', '--trust', '--model', 'sonnet', prompt]

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600,
            cwd=str(PROJECT), env=env,
        )

        _create_jobs[job_id]["enrich_returncode"] = result.returncode
        _create_jobs[job_id]["enrich_log"] = (result.stdout or "")[-3000:]

        if result.returncode == 0 and readme_path.exists():
            # Read back what AI wrote to report the name
            info = _parse_readme_frontmatter(readme_path)
            _create_jobs[job_id]["institution_name"] = info.get("name", slug)

            # Check if scraping is enabled before auto-scraping
            if info.get("enabled", True):
                _create_jobs[job_id]["status"] = "scraping"

                script = SCRIPTS_DIR / "scrape_single.sh"
                if script.exists():
                    scrape_result = subprocess.run(
                        ["bash", str(script), slug],
                        capture_output=True, text=True, timeout=600,
                        cwd=str(PROJECT), env=env,
                    )
                    _create_jobs[job_id]["scrape_returncode"] = scrape_result.returncode
                    if scrape_result.returncode == 0:
                        _create_jobs[job_id]["status"] = "completed"
                    else:
                        # Scrape failed but institution was created successfully
                        _create_jobs[job_id]["status"] = "completed"
                        _create_jobs[job_id]["scrape_error"] = "Initial scrape failed, you can retry manually"
                else:
                    _create_jobs[job_id]["status"] = "completed"
                    _create_jobs[job_id]["scrape_error"] = "scrape_single.sh not found"
            else:
                # AI set enabled: false (site down, no procurement section)
                _create_jobs[job_id]["status"] = "completed"
                _create_jobs[job_id]["scrape_skipped"] = True
        else:
            _create_jobs[job_id]["status"] = "failed"
            _create_jobs[job_id]["error"] = "Agent failed to create README"

    except subprocess.TimeoutExpired:
        # Check which phase timed out
        if _create_jobs[job_id].get("status") == "scraping":
            _create_jobs[job_id]["status"] = "completed"
            _create_jobs[job_id]["scrape_error"] = "Initial scrape timed out, you can retry manually"
        else:
            _create_jobs[job_id]["status"] = "failed"
            _create_jobs[job_id]["error"] = "Agent timed out (10 min limit)"
    except Exception as e:
        _create_jobs[job_id]["status"] = "failed"
        _create_jobs[job_id]["error"] = str(e)


class CreateInstitutionRequest(BaseModel):
    url: str


def _find_existing_by_domain(homepage: str) -> Optional[str]:
    """Check if any existing institution already has this domain/homepage in its README."""
    # Extract domain for comparison (strip scheme, www, trailing slash)
    domain = homepage.replace("https://", "").replace("http://", "").rstrip("/")
    domain_bare = domain.lstrip("www.")

    for d in INSTITUTIONS_DIR.iterdir():
        if not d.is_dir() or not (d / "README.md").exists():
            continue
        info = _parse_readme_frontmatter(d / "README.md")
        for field in ("homepage", "tender_url", "domain"):
            val = info.get(field, "")
            if not val:
                continue
            val_clean = val.replace("https://", "").replace("http://", "").rstrip("/").lstrip("www.")
            if val_clean == domain_bare:
                return d.name
    return None


@router.post("/institutions")
def admin_create_institution(
    req: CreateInstitutionRequest,
    background_tasks: BackgroundTasks,
):
    homepage = req.url.strip().rstrip("/")
    if not homepage.startswith("http"):
        homepage = "https://" + homepage

    slug = _url_to_slug(homepage)
    if not slug:
        raise HTTPException(400, "Could not derive slug from URL")

    # Check by slug
    inst_dir = INSTITUTIONS_DIR / slug
    if inst_dir.exists() and (inst_dir / "README.md").exists():
        raise HTTPException(409, f"Institution already exists as '{slug}'")

    # Check by domain across all existing institutions
    existing_slug = _find_existing_by_domain(homepage)
    if existing_slug:
        raise HTTPException(409, f"Institution already exists as '{existing_slug}'")

    job_id = f"create_{slug}_{datetime.now().strftime('%H%M%S')}"
    _create_jobs[job_id] = {"status": "queued", "slug": slug, "url": homepage}

    background_tasks.add_task(_run_create_institution, job_id, slug, homepage)

    return {"status": "creating", "slug": slug, "job_id": job_id}


@router.get("/institutions/jobs/{job_id}")
def admin_get_create_job(job_id: str):
    job = _create_jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job


@router.get("/institutions")
def admin_list_institutions(
    search: Optional[str] = None,
    enabled: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    institutions = []

    for d in sorted(INSTITUTIONS_DIR.iterdir()):
        if not d.is_dir() or not (d / "README.md").exists():
            continue

        slug = d.name
        info = _parse_readme_frontmatter(d / "README.md")
        info["slug"] = slug

        is_enabled = info.get("enabled", True)
        if enabled is not None and is_enabled != enabled:
            continue
        if search and search.lower() not in f"{slug} {info.get('name', '')}".lower():
            continue

        active_dir = d / "tenders" / "active"
        info["active_tenders"] = len(list(active_dir.glob("*.json"))) if active_dir.exists() else 0

        last_scrape = _load_json(d / "last_scrape.json", {})
        info["last_scraped"] = last_scrape.get("last_scrape")
        info["last_scrape_status"] = last_scrape.get("status")

        # Followers count
        followers = db.query(UserInstitution).filter(
            UserInstitution.institution_slug == slug
        ).count()
        info["followers_count"] = followers

        institutions.append(info)

    total = len(institutions)
    return {"total": total, "institutions": institutions[offset:offset + limit], "offset": offset, "limit": limit}


@router.put("/institutions/{slug}/toggle")
def admin_toggle_institution(slug: str):
    readme_path = INSTITUTIONS_DIR / slug / "README.md"
    if not readme_path.exists():
        raise HTTPException(404, f"Institution '{slug}' not found")

    content = readme_path.read_text(encoding="utf-8")
    match = re.search(r"(enabled:\s*)(true|false)", content, re.IGNORECASE)
    if not match:
        raise HTTPException(400, "No 'enabled' field found in README.md")

    current = match.group(2).lower() == "true"
    new_value = "false" if current else "true"
    new_content = content[:match.start(2)] + new_value + content[match.end(2):]
    readme_path.write_text(new_content, encoding="utf-8")

    return {"slug": slug, "enabled": not current}


@router.post("/institutions/{slug}/scrape")
def admin_trigger_scrape(slug: str):
    inst_dir = INSTITUTIONS_DIR / slug
    if not inst_dir.exists():
        raise HTTPException(404, f"Institution '{slug}' not found")

    script = SCRIPTS_DIR / "scrape_single.sh"
    if not script.exists():
        raise HTTPException(500, "scrape_single.sh not found")

    try:
        import os
        env = {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE")}
        env["PATH"] = os.environ.get("PATH", "/usr/bin:/usr/local/bin")

        proc = subprocess.Popen(
            ["bash", str(script), slug],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, cwd=str(PROJECT), env=env,
        )
        return {"status": "started", "slug": slug, "pid": proc.pid}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/institutions/{slug}/logs")
def admin_institution_logs(slug: str):
    log_path = INSTITUTIONS_DIR / slug / "scrape_log.json"
    return {"slug": slug, "logs": _load_json(log_path, [])}


# ── Subscriptions ────────────────────────────────────────────────────────────

@router.get("/subscriptions")
def admin_subscriptions(db: Session = Depends(get_db)):
    plans = {p.id: p for p in db.query(Plan).all()}

    # MRR
    mrr = 0
    subscribers_by_plan = {}
    for plan_id, plan in plans.items():
        count = db.query(User).filter(
            User.plan == plan_id,
            User.subscription_status == "active",
        ).count()
        subscribers_by_plan[plan_id] = {
            "name": plan.name,
            "count": count,
            "price": plan.price_monthly,
            "revenue": plan.price_monthly * count,
        }
        mrr += plan.price_monthly * count

    total_paying = db.query(User).filter(
        User.plan != "free",
        User.subscription_status == "active",
    ).count()
    free_users = db.query(User).filter(User.plan == "free").count()

    # Paying subscribers list
    paying = db.query(User).filter(
        User.plan != "free",
        User.subscription_status == "active",
    ).order_by(User.created_at.desc()).all()

    paying_list = [
        {
            "id": u.id, "email": u.email, "name": u.name,
            "plan": u.plan, "subscription_status": u.subscription_status,
            "subscription_ends_at": u.subscription_ends_at.isoformat() if u.subscription_ends_at else None,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in paying
    ]

    return {
        "mrr": mrr,
        "total_paying": total_paying,
        "free_users": free_users,
        "subscribers_by_plan": subscribers_by_plan,
        "paying_subscribers": paying_list,
    }


# ── Tenders (global, no user scoping) ────────────────────────────────────────

@router.get("/tenders")
def admin_list_tenders(
    status: str = "active",
    search: Optional[str] = None,
    institution: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    tenders = []
    glob_pattern = f"tenders/{status}/*.json"

    for tender_file in INSTITUTIONS_DIR.rglob(glob_pattern):
        slug = str(tender_file).split("/institutions/")[1].split("/")[0]
        t = _load_json(tender_file, {})
        if not t:
            continue

        t["institution_slug"] = slug

        if institution and slug != institution:
            continue
        if category and t.get("category", "").lower() != category.lower():
            continue
        if search:
            haystack = f"{t.get('title', '')} {t.get('description', '')} {t.get('institution', '')}".lower()
            if search.lower() not in haystack:
                continue

        tenders.append(t)

    tenders.sort(key=lambda x: x.get("closing_date") or "9999-12-31")
    total = len(tenders)
    return {"total": total, "tenders": tenders[offset:offset + limit], "offset": offset, "limit": limit}
