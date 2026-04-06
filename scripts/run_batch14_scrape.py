#!/usr/bin/env python3
"""Process 25 institutions: parse HTML, extract tenders or create leads, update scrape state."""
import json
import re
import os
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch14"
HTML_DIR = Path("/tmp/tender_scrape_run14")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"

# Tender keywords (case-insensitive)
TENDER_KEYWORDS = [
    "tender", "zabuni", "procurement", "manunuzi", "bid", "eoi", "rfp", "rfq", "rfi",
    "expression of interest", "request for proposal", "request for quotation",
    "invitation to bid", "tender notice", "tangazo la zabuni"
]

# Document extensions
DOC_EXTS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")

# Institution config: slug -> (name, tender_url, website_url)
INST_CONFIG = {
    "behobeho": ("Beho Beho", "https://www.behobeho.co.tz/", "https://www.behobeho.co.tz/"),
    "beibamartravel": ("Beibamar travel", "https://beibamartravel.co.tz/", "https://beibamartravel.co.tz/"),
    "beiyako": ("Beiyako", "https://beiyako.co.tz/", "https://beiyako.co.tz/"),
    "belfort": ("Belfort Tanzania", "https://www.belfort.co.tz/", "https://www.belfort.co.tz/"),
    "belva": ("Belva Consult Ltd", "https://www.belva.co.tz/", "https://www.belva.co.tz/"),
    "benison": ("Benison", "https://benison.co.tz/", "https://benison.co.tz/"),
    "bensonandcompany": ("Benson & Company", "https://bensonandcompany.com/", "https://bensonandcompany.com/"),
    "best": ("Best", "https://best.co.tz/", "https://best.co.tz/"),
    "besta": ("Besta", "https://besta.co.tz/", "https://besta.co.tz/"),
    "bestone": ("BEST ONE", "https://bestone.co.tz/", "https://bestone.co.tz/"),
    "bet": ("Leading Tanzania Sports Betting", "https://bet.co.tz/", "https://bet.co.tz/"),
    "bet22": ("22Bet Tanzania", "https://bet22.co.tz/", "https://bet22.co.tz/"),
    "betalaw": ("BETA Law", "https://betalaw.co.tz/", "https://betalaw.co.tz/"),
    "betaomega-agrib": ("Beta Omega Agribusiness", "https://betaomega-agrib.co.tz/", "https://betaomega-agrib.co.tz/"),
    "bethelservices": ("Bethel Services", "https://bethelservices.co.tz/", "https://bethelservices.co.tz/"),
    "bethlehemstar": ("Bethlehem Star School", "https://bethlehemstar.ac.tz/", "https://bethlehemstar.ac.tz/"),
    "beyond": ("Beyond Nature Ltd", "https://beyond.co.tz/", "https://beyond.co.tz/"),
    "bfi": ("BareFoot International", "https://bfi.co.tz/huduma-na-bidhaa", "https://bfi.co.tz/"),
    "bhti": ("BHTI", "https://bhti.ac.tz/", "https://bhti.ac.tz/"),
    "bhusene": ("Bhusene Store", "https://bhusene.co.tz/", "https://bhusene.co.tz/"),
    "biclimited": ("BIC Limited", "https://biclimited.co.tz/", "https://biclimited.co.tz/"),
    "bidvest": ("Bidvest Group", "https://bidvest.com/", "https://bidvest.com/"),
    "bigw": ("BIG W", "https://bigw.co.tz/", "https://bigw.co.tz/"),
    "biharamulodc": ("Biharamulo District Council", "https://biharamulodc.go.tz/tenders", "https://biharamulodc.go.tz/"),
    "bihas": ("BUKUMBI Institute", "https://bihas.ac.tz/", "https://bihas.ac.tz/"),
}


def has_tender_content(text):
    """Check if text contains tender/procurement keywords."""
    if not text or len(text) < 50:
        return False
    lower = text.lower()
    return any(kw in lower for kw in TENDER_KEYWORDS)


def extract_emails(html):
    """Extract email addresses from HTML."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = set(re.findall(pattern, html))
    # Filter out common false positives
    skip = {"example.com", "domain.com", "email.com", "test.com", "yoursite.com", "sentry.io", "wixpress.com", "gstatic.com", "googleapis.com", "facebook.com", "schema.org"}
    return [e for e in sorted(emails) if not any(s in e.lower() for s in skip)][:10]


def parse_biharamulodc(html, base_url):
    """Parse biharamulodc tenders table."""
    tenders = []
    # Match table rows: <tr><td>Title</td><td>pub_date</td><td>close_date</td><td><a href="...">Download</a></td></tr>
    pattern = r'<tr><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td><a href="([^"]+)"[^>]*>Download</a></td></tr>'
    for m in re.finditer(pattern, html):
        title, pub_date, close_date, doc_url = m.groups()
        doc_url = urljoin(base_url, doc_url)
        tenders.append({
            "title": title.strip(),
            "published_date": pub_date.strip(),
            "closing_date": close_date.strip(),
            "document_links": [doc_url],
        })
    return tenders


def extract_doc_links(html, base_url):
    """Extract document links (pdf, doc, docx, xls, xlsx, zip) from HTML."""
    links = set()
    for ext in DOC_EXTS:
        pattern = rf'href=["\']([^"\']*\{re.escape(ext)}[^"\']*)["\']'
        for m in re.finditer(pattern, html, re.I):
            url = urljoin(base_url, m.group(1).split("?")[0])
            if url and not url.startswith("data:"):
                links.add(url)
    return list(links)


def parse_date(s):
    """Parse date string to datetime for comparison."""
    from datetime import datetime
    fmts = ["%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%Y-%m-%d", "%d/%m/%Y"]
    for fmt in fmts:
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    return None


def is_active_tender(closing_date_str):
    """Check if tender is still active (closing date in future)."""
    d = parse_date(closing_date_str)
    if not d:
        return True  # Assume active if we can't parse
    return d.date() >= datetime.now().date()


def process_institution(slug):
    """Process one institution. Returns (status, tender_count, doc_count, error). tender_count = total tenders found."""
    inst_dir = PROJECT / "institutions" / slug
    html_path = HTML_DIR / f"{slug}.html"
    
    if slug not in INST_CONFIG:
        return ("error", 0, 0, "Unknown institution")
    
    name, tender_url, website_url = INST_CONFIG[slug]
    
    # Check if HTML was fetched
    if not html_path.exists() or html_path.stat().st_size < 100:
        return ("error", 0, 0, "Page not fetched or empty")
    
    html = html_path.read_text(errors="replace")
    
    # Check for error pages
    if "Not Acceptable" in html or "404" in html[:500] or "403" in html[:500]:
        return ("error", 0, 0, "Site blocked or error page")
    
    # Special handling for biharamulodc - has tender table
    if slug == "biharamulodc":
        tenders = parse_biharamulodc(html, "https://biharamulodc.go.tz")
    else:
        # Generic: check if page has tender content
        if not has_tender_content(html):
            # No tenders - create lead
            emails = extract_emails(html)
            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": website_url,
                "emails": emails,
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": f"Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
                "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
                "status": "pending",
            }
            # Append to leads.json
            leads = []
            if LEADS_JSON.exists():
                try:
                    leads = json.loads(LEADS_JSON.read_text())
                except Exception:
                    leads = []
            if not isinstance(leads, list):
                leads = leads.get("leads", []) if isinstance(leads, dict) else []
            # Check if already in leads
            if not any(l.get("institution_slug") == slug for l in leads):
                leads.append(lead)
                LEADS_JSON.parent.mkdir(parents=True, exist_ok=True)
                LEADS_JSON.write_text(json.dumps(leads, indent=2, ensure_ascii=False))
            return ("no_tenders", 0, 0, None)
        
        # Has tender keywords - extract doc links only (no structured tender list)
        doc_links = extract_doc_links(html, website_url)
        tenders = []
        if doc_links:
            tenders = [{"title": "Tender documents", "document_links": doc_links, "published_date": "", "closing_date": ""}]
    
    # Process tenders
    tender_count = 0
    doc_count = 0
    active_dir = inst_dir / "tenders" / "active"
    closed_dir = inst_dir / "tenders" / "closed"
    active_dir.mkdir(parents=True, exist_ok=True)
    closed_dir.mkdir(parents=True, exist_ok=True)
    
    for i, t in enumerate(tenders):
        closing = t.get("closing_date", "") or ""
        is_active = is_active_tender(closing) if closing else False
        target_dir = active_dir if is_active else closed_dir
        tender_id = f"{slug.upper().replace('-','')[:12]}-2026-{i+1:03d}"
        
        doc_links = t.get("document_links", [])
        for doc_url in doc_links:
            if any(doc_url.lower().endswith(ext) for ext in DOC_EXTS):
                doc_count += 1
                # Download document
                download_dir = inst_dir / "downloads" / tender_id / "original"
                extract_dir = inst_dir / "downloads" / tender_id / "extracted"
                download_dir.mkdir(parents=True, exist_ok=True)
                extract_dir.mkdir(parents=True, exist_ok=True)
                fname = doc_url.split("/")[-1].split("?")[0] or "document.pdf"
                local_path = download_dir / fname
                try:
                    import urllib.request
                    import ssl
                    req = urllib.request.Request(doc_url, headers={"User-Agent": "Mozilla/5.0"})
                    ctx = ssl.create_default_context()
                    if ".go.tz" in doc_url or "biharamulodc" in doc_url:
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                        local_path.write_bytes(resp.read())
                except Exception:
                    pass  # Log but continue
        
        tender_count += 1  # Count all tenders found
        
        tender_json = {
            "tender_id": tender_id,
            "institution": slug,
            "title": t.get("title", ""),
            "description": "",
            "published_date": t.get("published_date", ""),
            "closing_date": closing,
            "category": "General",
            "status": "active" if is_active else "closed",
            "source_url": tender_url,
            "documents": [{"original_url": u, "local_path": f"./downloads/{tender_id}/original/{u.split('/')[-1].split('?')[0]}"} for u in doc_links],
            "contact": {},
            "scraped_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        (target_dir / f"{tender_id}.json").write_text(json.dumps(tender_json, indent=2, ensure_ascii=False))
    
    return ("success", tender_count, doc_count, None)


def main():
    run_ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    results = []
    
    for slug in INST_CONFIG:
        try:
            status, tender_count, doc_count, err = process_institution(slug)
            if err:
                status = "error"
            results.append((slug, status, tender_count, doc_count))
            print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
        except Exception as e:
            results.append((slug, "error", 0, 0))
            print(f"RESULT|{slug}|error|0|0")
        
        # Update last_scrape.json and scrape_log.json for this institution
        inst_dir = PROJECT / "institutions" / slug
        last_scrape = {
            "institution": slug,
            "last_scrape": run_ts,
            "next_scrape": run_ts,
            "active_tenders_count": results[-1][2] if results else 0,
            "status": results[-1][1] if results else "error",
            "error": None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2))
        
        log_path = inst_dir / "scrape_log.json"
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": run_ts,
            "status": results[-1][1] if results else "error",
            "tenders_found": results[-1][2] if results else 0,
            "documents_downloaded": results[-1][3] if results else 0,
        }
        if log_path.exists():
            try:
                log_data = json.loads(log_path.read_text())
                runs = log_data.get("runs", [])
            except Exception:
                runs = []
        else:
            runs = []
        runs.append(log_entry)
        log_path.write_text(json.dumps({"runs": runs[-50:]}, indent=2))
    
    # Run sync_leads_csv if we added any leads
    if any(r[1] == "no_tenders" for r in results):
        import subprocess
        subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=str(PROJECT), check=False)


if __name__ == "__main__":
    main()
