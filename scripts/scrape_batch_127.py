#!/usr/bin/env python3
"""
Scrape 25 institutions for batch 127.
For each: fetch, parse, extract tenders or create opportunity lead.
"""
import json
import re
import os
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse
import urllib.request
import ssl

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch127"
INSTITUTIONS = [
    "unitedinfrastructures", "unity", "untamedsafaris", "upendomedia", "urasaccos",
    "urbanmegastore", "ursa", "urusecondary", "ushirika", "ussl", "utegitechnical",
    "utel", "utpc", "uttamis", "utumefmradio", "utv", "uvinzafm", "uwezeshaji",
    "uwezofinancial", "uwodo", "uwp", "uyuidc", "valleyviewschools", "vaniagroup", "vcc",
]

TENDER_KEYWORDS = re.compile(
    r"tender|zabuni|procurement|manunuzi|rfp|rfq|eoi|expression\s+of\s+interest|"
    r"bid|bidding|supply|procure|vacancy|nafasi|ajira",
    re.I
)
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

def fetch_url(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TenderScraper/1.0)"})
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read().decode("utf-8", errors="replace"), None
    except Exception as e:
        # Fallback: try without SSL verification (some Tanzanian sites have cert issues)
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TenderScraper/1.0)"})
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                return r.read().decode("utf-8", errors="replace"), None
        except Exception as e2:
            return None, str(e2)

def extract_emails(html):
    return list(set(EMAIL_PATTERN.findall(html)))

def has_tender_content(html):
    if not html:
        return False
    return bool(TENDER_KEYWORDS.search(html))

def extract_tender_items(html, base_url):
    """Simple extraction of potential tender items from HTML."""
    items = []
    # Look for links to PDF/DOC
    doc_links = re.findall(r'href=["\']([^"\']*\.(?:pdf|doc|docx|xls|xlsx|zip))["\']', html, re.I)
    for href in doc_links:
        full = urljoin(base_url, href)
        items.append({"url": full, "type": "document"})
    # Look for tender-like headings/sections
    for m in re.finditer(r'<h[2-4][^>]*>([^<]{10,80})</h[2-4]>', html):
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if TENDER_KEYWORDS.search(title):
            items.append({"title": title, "type": "heading"})
    return items

def get_tender_url(slug):
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return f"https://{slug.replace('_','')}.co.tz/"
    text = readme.read_text(encoding="utf-8")
    m = re.search(r'tender_url:\s*["\']?([^"\'\s]+)', text)
    if m:
        return m.group(1).strip()
    m = re.search(r'homepage:\s*["\']?([^"\'\s]+)', text)
    if m:
        return m.group(1).strip()
    return f"https://{slug}.co.tz/"

def get_institution_name(slug):
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return slug.replace("-", " ").title()
    text = readme.read_text(encoding="utf-8")
    m = re.search(r'name:\s*["\']([^"\']+)["\']', text)
    if m:
        return m.group(1).strip()
    return slug.replace("-", " ").title()

def update_last_scrape(slug, status, tender_count=0, error=None):
    inst_dir = PROJECT / "institutions" / slug
    data = {
        "institution": slug,
        "last_scrape": datetime.now(timezone.utc).isoformat(),
        "next_scrape": datetime.now(timezone.utc).isoformat(),
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
        "run_id": RUN_ID,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

def append_scrape_log(slug, status, tender_count, doc_count, error=None):
    inst_dir = PROJECT / "institutions" / slug
    log_file = inst_dir / "scrape_log.json"
    entry = {
        "run_id": RUN_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    }
    if log_file.exists():
        data = json.loads(log_file.read_text(encoding="utf-8"))
        runs = data.get("runs", [])
    else:
        runs = []
    runs.append(entry)
    log_file.write_text(json.dumps({"runs": runs[-100:]}, indent=2), encoding="utf-8")

def append_lead(lead):
    leads_file = PROJECT / "opportunities" / "leads.json"
    if leads_file.exists():
        data = json.loads(leads_file.read_text(encoding="utf-8"))
        leads = data if isinstance(data, list) else data.get("leads", [])
    else:
        leads = []
    slugs = {l.get("institution_slug") for l in leads}
    if lead["institution_slug"] not in slugs:
        leads.append(lead)
        leads_file.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

def create_opportunity_lead(slug, name, url, emails, html):
    draft_subject = f"Partnership Opportunity – ZIMA Solutions & {name}"
    draft_body = f"""Dear {name} Team,

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
    return {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails[:5],
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": draft_subject,
        "draft_email_body": draft_body,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }

def main():
    results = []
    for slug in INSTITUTIONS:
        url = get_tender_url(slug)
        name = get_institution_name(slug)
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)

        html, err = fetch_url(url)
        if err:
            update_last_scrape(slug, "error", 0, err)
            append_scrape_log(slug, "error", 0, 0, err)
            results.append((slug, "error", 0, 0))
            print(f"RESULT|{slug}|error|0|0  # {err[:60]}")
            continue

        tender_items = extract_tender_items(html, url)
        doc_links = [x for x in tender_items if x.get("type") == "document"]
        # Tenders: doc links (PDF/DOC etc) on page, or tender keywords in content with structure
        has_tenders = (len(doc_links) > 0) or (has_tender_content(html) and len(tender_items) > 0)

        if has_tenders and (doc_links or tender_items):
            # Save tender JSON for each found item
            year = datetime.now().year
            for i, item in enumerate(tender_items[:10], 1):
                tid = f"{slug.upper().replace('-','')[:12]}-{year}-{i:03d}"
                tender_json = {
                    "tender_id": tid,
                    "institution": slug,
                    "title": item.get("title", f"Tender {i}"),
                    "source_url": url,
                    "documents": [{"url": item["url"], "type": item.get("type", "document")}] if item.get("url") else [],
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                }
                (inst_dir / "tenders" / "active" / f"{tid}.json").write_text(
                    json.dumps(tender_json, indent=2), encoding="utf-8"
                )
            tender_count = len(tender_items[:10])
            doc_count = len(doc_links)
            update_last_scrape(slug, "success", tender_count)
            append_scrape_log(slug, "success", tender_count, doc_count)
            results.append((slug, "success", tender_count, doc_count))
            print(f"RESULT|{slug}|success|{tender_count}|{doc_count}")
        else:
            # No tenders: create opportunity lead
            emails = extract_emails(html)
            lead = create_opportunity_lead(slug, name, url, emails, html)
            append_lead(lead)
            update_last_scrape(slug, "no_tenders", 0)
            append_scrape_log(slug, "no_tenders", 0, 0)
            results.append((slug, "no_tenders", 0, 0))
            print(f"RESULT|{slug}|no_tenders|0|0")

    # Sync leads CSV
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        os.system(f"python3 {sync_script}")
    return results

if __name__ == "__main__":
    main()
