#!/usr/bin/env python3
"""Batch scrape 26 institutions for run_20260313_205329_batch105."""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch105"

INSTITUTIONS = [
    "simbanet", "simbaoil", "simbatechnology", "simera", "simiyu",
    "simplyit", "simusolar", "sincro", "sinetamer", "singida",
    "singidadc", "singidamc", "singoadvocates", "sinologistics", "siringit",
    "sisal", "sisalana", "sisalboard", "sistl", "siteium",
    "siteweavers", "situslaw", "sjuit", "sjut", "skonga",
]

# Tender URLs from READMEs
TENDER_URLS = {
    "simbanet": "https://www.simbanet.net/",
    "simbaoil": "https://simbaoil.co.tz/",
    "simbatechnology": "https://simbatechnology.co.tz/",
    "simera": "https://simera.co.tz/",
    "simiyu": "https://simiyu.go.tz/tenders",
    "simplyit": "https://simplyit.co.tz/",
    "simusolar": "https://simusolar.com/",
    "sincro": "http://www.sincro.co.tz/",
    "sinetamer": "https://www.sinetamer.co.tz/",
    "singida": "https://singida.go.tz/procurement-and-supply",
    "singidadc": "https://singidadc.go.tz/tenders",
    "singidamc": "https://singidamc.go.tz/tenders",
    "singoadvocates": "https://singoadvocates.co.tz/",
    "sinologistics": "https://sinologistics.co.tz/index.php/quotation",
    "siringit": "https://www.siringit.co.tz/",
    "sisal": "https://www.sisal.co.tz/",
    "sisalana": "https://sisalana.co.tz/",
    "sisalboard": "https://sisalboard.go.tz/",
    "sistl": "https://www.sistl.co.tz/",
    "siteium": "https://siteium.com/",
    "siteweavers": "https://www.siteweavers.co.tz/",
    "situslaw": "https://www.situslaw.co.tz/",
    "sjuit": "https://sjuit.ac.tz/",
    "sjut": "https://sjut.ac.tz/",
    "skonga": "https://skonga.co.tz/",
}


def fetch_url(url: str) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-k", "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
             "--connect-timeout", "20", "--max-time", "45", url],
            capture_output=True, text=True, timeout=50, cwd=str(PROJECT)
        )
        if r.returncode != 0:
            return None, f"curl exit {r.returncode}"
        return r.stdout or "", None
    except Exception as e:
        return None, str(e)


def has_tender_content(html: str, slug: str, url: str) -> bool:
    """Check if HTML contains tender-like content."""
    if not html or len(html) < 200:
        return False
    html_lower = html.lower()
    url_lower = url.lower()
    # Tender/procurement page URLs
    if "/tenders" in url_lower or "/procurement" in url_lower or "zabuni" in url_lower:
        if "display all tenders" in html_lower or "zabuni" in html_lower or "procurement" in html_lower:
            return True
    # Tender keywords in content
    if "display all tenders" in html_lower:
        return True
    if "zabuni" in html_lower and ("ads-listing" in html or "home-page-title" in html):
        return True
    if "procurement" in html_lower and "manunuzi" in html_lower:
        return True
    if any(kw in html_lower for kw in ["rfp", "rfq", "request for proposal", "request for quotation"]):
        return True
    return False


def extract_tenders_from_gov_site(html: str, slug: str, base_url: str) -> list[dict]:
    """Extract tender items from gov site HTML."""
    tenders = []
    # Look for ads-listing with tender items
    li_match = re.findall(
        r'<li[^>]*>.*?<a\s+href="([^"]+)"[^>]*>.*?<h4[^>]*>([^<]+)</h4>',
        html, re.DOTALL | re.IGNORECASE
    )
    for href, title in li_match:
        if any(x in title.lower() for x in ["zabuni", "tender", "procurement", "nafasi"]):
            full_url = urljoin(base_url, href)
            tenders.append({
                "title": title.strip(),
                "source_url": full_url,
                "document_links": [],
            })
    # Also look for PDF links
    pdf_links = re.findall(r'href="([^"]+\.pdf[^"]*)"', html, re.IGNORECASE)
    if tenders and pdf_links:
        for t in tenders:
            t["document_links"] = [urljoin(base_url, u) for u in pdf_links[:5]]
    elif not tenders and pdf_links:
        for i, pl in enumerate(pdf_links[:5]):
            tenders.append({
                "title": f"Tender document {i+1}",
                "source_url": base_url,
                "document_links": [urljoin(base_url, pl)],
            })
    return tenders


def update_institution(slug: str, status: str, tender_count: int, doc_count: int, error: str | None = None):
    """Update last_scrape.json and scrape_log.json."""
    inst_dir = PROJECT / "institutions" / slug
    inst_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    last = {
        "institution": slug,
        "last_scrape": now,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

    log_path = inst_dir / "scrape_log.json"
    log = {"runs": []}
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
    log["runs"].append({
        "run_id": RUN_ID,
        "timestamp": now,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
    })
    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")


def append_lead(slug: str, name: str, url: str, emails: list[str], opportunity_type: str, description: str):
    """Append lead to opportunities/leads.json."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        data = json.loads(leads_path.read_text(encoding="utf-8"))
        leads = data if isinstance(data, list) else data.get("leads", [])

    # Check if already exists
    if any(l.get("institution_slug") == slug for l in leads):
        return

    subject = f"Partnership Opportunity – ZIMA Solutions & {name}"
    body = f"""Dear {name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {name}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
"""

    lead = {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": opportunity_type,
        "opportunity_description": description,
        "draft_email_subject": subject,
        "draft_email_body": body,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }
    leads.append(lead)
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")


def extract_emails(html: str) -> list[str]:
    """Extract email addresses from HTML."""
    if not html:
        return []
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
    return list(dict.fromkeys(e.lower() for e in emails if "example" not in e and "domain" not in e))


def get_contact_emails(slug: str) -> list[str]:
    """Get known contact emails from README."""
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return []
    text = readme.read_text(encoding="utf-8")
    emails = re.findall(r'email:\s*["\']?([^"\'\s\n]+@[^"\'\s\n]+)', text, re.IGNORECASE)
    alt = re.findall(r'alternate_emails:\s*\n\s*-\s*["\']?([^"\'\s\n]+)', text)
    return list(dict.fromkeys(emails + alt))


def main():
    results = []
    for slug in INSTITUTIONS:
        url = TENDER_URLS.get(slug, "")
        if not url:
            print(f"RESULT|{slug}|error|0|0  # No URL")
            continue

        html, err = fetch_url(url)
        if err:
            update_institution(slug, "error", 0, 0, err)
            append_lead(slug, slug.replace("-", " ").title(), url, [], "sell",
                       f"Site unreachable: {err}. ZIMA could offer digital transformation.")
            print(f"RESULT|{slug}|error|0|0  # {err}")
            continue

        if not has_tender_content(html, slug, url):
            emails = extract_emails(html) or get_contact_emails(slug)
            name = slug.replace("-", " ").replace("_", " ").title()
            append_lead(slug, name, url, emails, "sell",
                       "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.")
            update_institution(slug, "no_tenders", 0, 0)
            print(f"RESULT|{slug}|no_tenders|0|0")
            continue

        # Has tender content - extract tenders
        tenders = extract_tenders_from_gov_site(html, slug, url)
        if not tenders:
            tenders = [{"title": "Tender page", "source_url": url, "document_links": []}]

        # Save tender JSONs
        active_dir = PROJECT / "institutions" / slug / "tenders" / "active"
        active_dir.mkdir(parents=True, exist_ok=True)
        doc_count = 0
        for i, t in enumerate(tenders[:10], 1):
            tid = f"{slug.upper().replace('-', '')}-2026-{i:03d}"
            tj = {
                "tender_id": tid,
                "institution": slug,
                "title": t.get("title", "Tender"),
                "description": t.get("title", ""),
                "source_url": t.get("source_url", url),
                "document_links": t.get("document_links", []),
                "contact": {},
                "scraped_at": datetime.now(timezone.utc).isoformat(),
                "documents": [],
                "status": "active",
            }
            (active_dir / f"{tid}.json").write_text(json.dumps(tj, indent=2), encoding="utf-8")
            doc_count += len(t.get("document_links", []))

        update_institution(slug, "success", len(tenders), doc_count)
        print(f"RESULT|{slug}|success|{len(tenders)}|{doc_count}")

    # Sync leads CSV
    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=str(PROJECT), check=False)


if __name__ == "__main__":
    main()
