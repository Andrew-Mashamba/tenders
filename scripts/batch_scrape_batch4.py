#!/usr/bin/env python3
"""
Batch scrape 25 institutions for run_20260313_205329_batch4.
Institutions: afritech, afritrust, afriwag, afriyantz, afrogems, afroilgroup,
  afroinsurance, afromark, afrosense, afyaconnect, afyadepot, afyadirectory,
  afyaplus, afyaplustz, age-upgrade, agematours, agenergies, agim, agitf,
  aglex, agricom, agricomafrica, agriedo, agripromise, agrishine
"""
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urljoin

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch4"

INSTITUTIONS = [
    "afritech", "afritrust", "afriwag", "afriyantz", "afrogems", "afroilgroup",
    "afroinsurance", "afromark", "afrosense", "afyaconnect", "afyadepot",
    "afyadirectory", "afyaplus", "afyaplustz", "age-upgrade", "agematours",
    "agenergies", "agim", "agitf", "aglex", "agricom", "agricomafrica",
    "agriedo", "agripromise", "agrishine",
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|procurement|rfp|rfi|eoi|bid|bids|zabuni|manunuzi|"
    r"expression\s+of\s+interest|request\s+for\s+proposal)\b",
    re.I,
)
DOC_EXT = re.compile(r"\.(pdf|doc|docx|xls|xlsx|zip)(\?|$)", re.I)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug: str) -> tuple[str, str]:
    """Load tender_url and institution name from README. Returns (url, name)."""
    readme = PROJECT / "institutions" / slug / "README.md"
    url = ""
    name = slug.replace("-", " ").title()
    text = ""
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        for line in text.split("\n"):
            if line.strip().startswith("tender_url:"):
                url = line.split('"', 2)[1].strip()
                break
            if line.strip().startswith("name:"):
                name = line.split('"', 2)[1].strip()
                name = name.replace("&#8211;", "–").replace("&amp;", "&")
        if not url and "homepage:" in text:
            for line in text.split("\n"):
                if line.strip().startswith("homepage:"):
                    url = line.split('"', 2)[1].strip()
                    break
    return url or f"https://{slug.replace('-', '')}.co.tz/", name


def fetch_url(url: str, timeout: int = 20) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-m", str(timeout), "-A", "Mozilla/5.0 (compatible; TenderBot/1.0)", url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if r.returncode != 0:
            return None, f"curl exit {r.returncode}"
        return r.stdout or None, None
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except Exception as e:
        return None, str(e)


def parse_tenders(html: str, base_url: str) -> list[dict]:
    """Extract tender-like items and document links from HTML."""
    tenders = []
    if not html:
        return tenders

    doc_links = set()
    for m in re.finditer(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', html):
        href = m.group(1).strip()
        if DOC_EXT.search(href):
            full = urljoin(base_url, href)
            if full.startswith(("http://", "https://")):
                doc_links.add(full)

    text_lower = html.lower()
    has_tender_section = bool(
        "tender" in text_lower or "procurement" in text_lower or "rfp" in text_lower
        or "rfi" in text_lower or "eoi" in text_lower or "zabuni" in text_lower
        or "manunuzi" in text_lower
    )
    no_tenders = bool(
        re.search(r"no\s+(current|open|active)\s+(tender|procurement)", text_lower)
        or re.search(r"there\s+are\s+no\s+current", text_lower)
    )

    if doc_links and has_tender_section and not no_tenders:
        tenders.append({
            "title": "Tender documents",
            "document_links": list(doc_links),
            "source_url": base_url,
        })
    elif doc_links and not no_tenders and has_tender_section:
        tenders.append({
            "title": "Documents",
            "document_links": list(doc_links),
            "source_url": base_url,
        })

    date_pat = re.compile(r"\b(20\d{2})[-/](0[1-9]|1[0-2])[-/]([0-2]\d|3[01])\b")
    if TENDER_KEYWORDS.search(html) and date_pat.search(html) and not no_tenders:
        for m in re.finditer(r"<h[2-4][^>]*>([^<]+)</h[2-4]>", html, re.I):
            title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            if len(title) > 10 and TENDER_KEYWORDS.search(title):
                if not any(t.get("title") == title for t in tenders):
                    tenders.append({
                        "title": title[:200],
                        "document_links": [],
                        "source_url": base_url,
                    })

    return tenders


def extract_emails(html: str) -> list[str]:
    """Extract valid emails from HTML."""
    if not html:
        return []
    seen = set()
    emails = []
    for m in EMAIL_RE.finditer(html):
        e = m.group(0).lower()
        if e not in seen and not any(x in e for x in [
            "sentry", "wixpress", "example.com", "domain.com", "png", "jpg", "gif"
        ]):
            seen.add(e)
            emails.append(e)
    return emails


def get_contact_from_readme(slug: str) -> list[str]:
    """Get emails from README."""
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return []
    text = readme.read_text(encoding="utf-8")
    emails = list(dict.fromkeys(EMAIL_RE.findall(text)))
    return [e for e in emails if not any(x in e for x in [
        "sentry", "wixpress", "fdfa.png", "website.com", "bootstrap", "vue@"
    ])]


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def process_institution(slug: str, url: str, inst_name: str) -> tuple[str, int, int, str]:
    """Process one institution. Returns (status, tender_count, doc_count, error)."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_url(url)
    if err:
        last = {
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).isoformat(),
            "active_tenders_count": 0,
            "status": "error",
            "error": err,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
        log_path = inst_dir / "scrape_log.json"
        runs = []
        if log_path.exists():
            try:
                loaded = json.loads(log_path.read_text(encoding="utf-8"))
                runs = loaded if isinstance(loaded, list) else loaded.get("runs", [])
            except Exception:
                pass
        runs.append({"run_id": RUN_ID, "timestamp": datetime.now(timezone.utc).isoformat(),
                     "status": "error", "tenders_found": 0, "documents_downloaded": 0, "error": err})
        log_path.write_text(json.dumps(runs[-100:], indent=2), encoding="utf-8")
        return "error", 0, 0, err

    if not html or len(html) < 100:
        err = "empty or too short response"
        last = {"institution": slug, "last_scrape": datetime.now(timezone.utc).isoformat(),
                "active_tenders_count": 0, "status": "error", "error": err}
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
        return "error", 0, 0, err

    if "account suspended" in html.lower() or "site suspended" in html.lower():
        err = "account suspended"
        last = {"institution": slug, "last_scrape": datetime.now(timezone.utc).isoformat(),
                "active_tenders_count": 0, "status": "blocked", "error": err}
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
        return "blocked", 0, 0, err

    tenders = parse_tenders(html, url)

    # Known document URLs from READMEs (partnership docs, reports - not formal tenders but downloadable)
    known_docs = {
        "afyadepot": ["https://afyadepot.co.tz/wp-content/uploads/2025/12/be-a-partner-afyadepo.pdf"],
        "afyaplustz": [
            "https://afyaplustz.or.tz/assets/pdf/AFYAPLUS-QUARTER-ONE-REPORT-2025.pdf",
            "https://afyaplustz.or.tz/assets/pdf/AFYAPLUS QUARTER TWO II REPORT 2025.pdf",
            "https://afyaplustz.or.tz/assets/pdf/AFYAPLUS QUARTER THREE REPORT 2025.pdf",
        ],
        "agitf": [
            "https://agitf.go.tz/uploads/documents/sw-1770986047-Loan Application - Individual.pdf",
            "https://agitf.go.tz/uploads/documents/sw-1770985915-Loan Application - Kikundi.pdf",
            "https://agitf.go.tz/uploads/documents/sw-1770985773-Loan Application - Taasisi.pdf",
        ],
    }
    # These are partnership/loan forms - not formal tenders. We treat as no_tenders for lead creation

    if tenders:
        doc_count = 0
        year = datetime.now(timezone.utc).year
        slug_upper = slug.upper().replace("-", "")[:10]
        for i, t in enumerate(tenders):
            tid = f"{slug_upper}-{year}-{i+1:03d}"
            tender_json = {
                "tender_id": tid,
                "institution": slug,
                "title": t.get("title", "Tender"),
                "description": "",
                "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "closing_date": "",
                "category": "General",
                "status": "active",
                "source_url": t.get("source_url", url),
                "documents": [],
                "contact": {},
                "scraped_at": datetime.now(timezone.utc).isoformat(),
                "last_checked": datetime.now(timezone.utc).isoformat(),
            }
            doc_links = t.get("document_links", [])[:20]
            download_dir = inst_dir / "downloads" / tid / "original"
            extracted_dir = inst_dir / "downloads" / tid / "extracted"
            download_dir.mkdir(parents=True, exist_ok=True)
            extracted_dir.mkdir(parents=True, exist_ok=True)

            for durl in doc_links:
                try:
                    fname = durl.split("/")[-1].split("?")[0] or "document.pdf"
                    fname = re.sub(r'[^\w\.\-]', '_', fname)[:100]
                    out_path = download_dir / fname
                    subprocess.run(
                        ["curl", "-sL", "-m", "30", "-o", str(out_path), durl],
                        capture_output=True,
                        timeout=35,
                    )
                    if out_path.exists() and out_path.stat().st_size > 0:
                        doc_count += 1
                        tender_json["documents"].append({
                            "filename": fname,
                            "original_url": durl,
                            "local_path": str(out_path.relative_to(inst_dir)),
                        })
                        ext = out_path.suffix.lower()
                        txt_path = extracted_dir / (out_path.stem + ".txt")
                        if ext == ".pdf" and (PROJECT / ".venv").exists():
                            try:
                                r = subprocess.run(
                                    [str(PROJECT / ".venv/bin/python3"), "-m", "tools", "pdf", "read", str(out_path)],
                                    capture_output=True,
                                    text=True,
                                    cwd=str(PROJECT),
                                    timeout=15,
                                )
                                if r.stdout:
                                    txt_path.write_text(r.stdout[:50000], encoding="utf-8")
                            except Exception:
                                pass
                except Exception:
                    pass

            (inst_dir / "tenders" / "active" / f"{tid}.json").write_text(
                json.dumps(tender_json, indent=2), encoding="utf-8"
            )

        last = {
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).isoformat(),
            "active_tenders_count": len(tenders),
            "status": "success",
            "error": None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

        log_path = inst_dir / "scrape_log.json"
        runs = []
        if log_path.exists():
            try:
                loaded = json.loads(log_path.read_text(encoding="utf-8"))
                runs = loaded if isinstance(loaded, list) else loaded.get("runs", [])
            except Exception:
                pass
        runs.append({
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
            "tenders_found": len(tenders),
            "documents_downloaded": doc_count,
            "errors": [],
        })
        log_path.write_text(json.dumps(runs[-100:], indent=2), encoding="utf-8")

        return "tenders", len(tenders), doc_count, ""

    # No tenders - create lead
    page_emails = extract_emails(html)
    readme_emails = get_contact_from_readme(slug)
    all_emails = list(dict.fromkeys(readme_emails + page_emails))
    all_emails = [e for e in all_emails if "@" in e and "." in e.split("@")[-1]][:10]

    lead = {
        "institution_slug": slug,
        "institution_name": inst_name or slug.replace("-", " ").title(),
        "website_url": url,
        "emails": all_emails,
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders or procurements found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, IT/ICT services, or partnership opportunities.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
        "draft_email_body": f"""Dear {inst_name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {inst_name}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }

    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        leads = json.loads(leads_path.read_text(encoding="utf-8"))
    if not isinstance(leads, list):
        leads = leads.get("leads", [])
    if not any(l.get("institution_slug") == slug for l in leads):
        leads.append(lead)
        leads_path.write_text(json.dumps(leads, indent=2), encoding="utf-8")

    last = {
        "institution": slug,
        "last_scrape": datetime.now(timezone.utc).isoformat(),
        "active_tenders_count": 0,
        "status": "success",
        "error": None,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

    log_path = inst_dir / "scrape_log.json"
    runs = []
    if log_path.exists():
        try:
            loaded = json.loads(log_path.read_text(encoding="utf-8"))
            runs = loaded if isinstance(loaded, list) else loaded.get("runs", [])
        except Exception:
            pass
    runs.append({
        "run_id": RUN_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "success",
        "tenders_found": 0,
        "documents_downloaded": 0,
        "lead_created": True,
    })
    log_path.write_text(json.dumps(runs[-100:], indent=2), encoding="utf-8")

    return "no_tenders", 0, 0, ""


def main():
    results = []
    for slug in INSTITUTIONS:
        url, inst_name = load_readme(slug)
        try:
            status, tc, dc, err = process_institution(slug, url, inst_name)
        except Exception as e:
            status, tc, dc, err = "error", 0, 0, str(e)
            inst_dir = PROJECT / "institutions" / slug
            ensure_dirs(inst_dir)
            last = {"institution": slug, "last_scrape": datetime.now(timezone.utc).isoformat(),
                    "active_tenders_count": 0, "status": "error", "error": str(e)}
            (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
        results.append((slug, status, tc, dc))
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")

    # Run sync_leads_csv if any new leads
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    os.system(f"python3 {sync_script}")

    return results


if __name__ == "__main__":
    main()
