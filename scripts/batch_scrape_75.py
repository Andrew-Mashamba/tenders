#!/usr/bin/env python3
"""Batch scrape 25 institutions for tenders. Run ID: run_20260313_205329_batch75"""
import json
import os
import re
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import urllib.request
import urllib.error

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch75"

INSTITUTIONS = [
    ("mkulimamakini", "Home - Mkulima Makini", "https://www.mkulimamakini.co.tz/"),
    ("mkurabita", "MKURABITA", "https://mkurabita.go.tz/pages/tenders"),
    ("mkuzachicksltd", "Mkuza Chicks Ltd", "https://www.mkuzachicksltd.co.tz/"),
    ("mkwabi", "Mkwabi Enterprises Limited", "https://mkwabi.co.tz/"),
    ("mlc", "MLC - MYLOGISTICS COMPANY LIMITED", "https://mlc.co.tz/"),
    ("mlg", "MLG - Mashiba Law Group", "https://mlg.co.tz/financial-procurement-regulatory-and-compliance-laws/"),
    ("mlimanicity", "Mlimani City shopping mall", "https://mlimanicity.co.tz/"),
    ("mlimaniholdings", "Mlimani Holdings", "https://mlimanicity.co.tz/"),
    ("mloganzila", "Muhimbili National Hospital - Mloganzila", "https://www.mloganzila.or.tz/tenders/"),
    ("mm-safaris", "MM Safaris", "https://mm-safaris.co.tz/"),
    ("mmgroup", "MM Group of Companies", "https://mmgroup.co.tz/"),
    ("mnkanda", "MNKANDA ELECTRICAL SERVICES LIMITED", "https://www.mnkanda.co.tz/"),
    ("mnma", "MNMA - MAIN CAMPUS", "https://www.mnma.ac.tz/"),
    ("moassurance", "MO Assurance", "https://moassurance.co.tz/"),
    ("mobikey", "Mobikey", "https://www.mobikey.co.tz/"),
    ("mobilepower", "Mobile Power Co Ltd", "https://mobilepower.co.tz/"),
    ("moccobeachvilla", "Mocco Beach Villa", "https://moccobeachvilla.co.tz/"),
    ("modans", "Wizara ya Ulinzi na Jeshi la Kujenga Taifa", "https://modans.go.tz/tenders"),
    ("modelltransport", "Modell Transport", "https://www.modelltransport.co.tz/"),
    ("moe", "Wizara ya Elimu, Sayansi na Teknolojia", "https://moe.go.tz/sw/manunuzi-na-ugavi"),
    ("moez", "MOEVT - Ministry of Education Zanzibar", "https://eprocurement.zppda.go.tz"),
    ("mof", "Ministry of Finance", "https://mof.go.tz/pages/tenders"),
    ("mofzanzibar", "Wizara ya Fedha na Mipango - Zanzibar", "https://eprocurement.zppda.go.tz"),
    ("moh", "Ministry of Health", "https://moh.go.tz/procurement"),
    ("moha", "MOHA - Ministry of Home Affairs", "https://moha.go.tz/"),
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|procurement|manunuzi|rfp|rfi|eoi|bid|expression of interest|"
    r"request for proposal|request for quotation|tangazo|mnada|tor|terms of reference)\b",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
USER_AGENT = "Mozilla/5.0 (compatible; TenderBot/1.0)"


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        ctx = ssl.create_default_context()
        if ".go.tz" in url or "zppda" in url:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read().decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, str(e.reason) if e.reason else str(e)
    except Exception as e:
        return None, str(e)


def extract_emails(html):
    if not html:
        return []
    found = set()
    for m in EMAIL_RE.finditer(html):
        e = m.group(0).lower()
        if not any(x in e for x in ["example.com", "domain.com", "wixpress", "sentry", "gravatar"]):
            found.add(e)
    return list(found)


def extract_doc_links(html, base_url):
    if not html:
        return []
    links = []
    for m in re.finditer(r'href=["\']([^"\']+\.(?:pdf|doc|docx|xls|xlsx|zip))["\']', html, re.I):
        url = m.group(1)
        if url.startswith("//"):
            url = "https:" + url
        elif url.startswith("/"):
            parsed = urlparse(base_url)
            url = f"{parsed.scheme}://{parsed.netloc}{url}"
        elif not url.startswith("http"):
            url = urljoin(base_url, url)
        if any(url.lower().endswith(ext) for ext in DOC_EXT):
            links.append(url)
    return list(dict.fromkeys(links))


def has_tender_content(html, url):
    if not html:
        return False
    text = re.sub(r"<[^>]+>", " ", html).lower()
    url_lower = url.lower()
    if "zabuni" in url_lower or "tender" in url_lower or "manunuzi" in url_lower or "procurement" in url_lower:
        return True
    if TENDER_KEYWORDS.search(text):
        return True
    if "zabuni" in text or "tender" in text or "procurement" in text or "manunuzi" in text:
        return True
    return False


def download_file(url, dest_path, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        ctx = ssl.create_default_context()
        if ".go.tz" in url or "zppda" in url:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            data = r.read()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


def save_tender(inst_dir, slug, tender_id, tender_data, doc_urls, base_url):
    tenders_dir = inst_dir / "tenders" / "active"
    tenders_dir.mkdir(parents=True, exist_ok=True)
    downloads_base = inst_dir / "downloads" / tender_id
    orig_dir = downloads_base / "original"
    ext_dir = downloads_base / "extracted"
    orig_dir.mkdir(parents=True, exist_ok=True)
    ext_dir.mkdir(parents=True, exist_ok=True)

    docs = []
    for i, url in enumerate(doc_urls[:10]):
        fname = url.split("/")[-1].split("?")[0] or f"doc_{i}.pdf"
        if not any(fname.lower().endswith(ext) for ext in DOC_EXT):
            fname += ".pdf"
        dest = orig_dir / fname
        if download_file(url, dest):
            docs.append({"url": url, "local_path": str(dest.relative_to(inst_dir)), "filename": fname})

    tender_data["tender_id"] = tender_id
    tender_data["institution"] = slug
    tender_data["source_url"] = base_url
    tender_data["documents"] = docs
    tender_data["scraped_at"] = datetime.now(timezone.utc).isoformat()

    out_path = tenders_dir / f"{tender_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tender_data, f, indent=2, ensure_ascii=False)
    return len(docs)


def append_lead(slug, name, url, emails, opportunity_type, description, subject, body):
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    lead = {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails[:5],
        "opportunity_type": opportunity_type,
        "opportunity_description": description,
        "draft_email_subject": subject,
        "draft_email_body": body,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }
    leads.append(lead)
    with open(leads_path, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


def update_scrape_state(inst_dir, slug, status, tender_count, doc_count, error=None):
    now = datetime.now(timezone.utc).isoformat()
    last = {
        "institution": slug,
        "last_scrape": now,
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "documents_downloaded": doc_count,
        "status": status,
        "error": error,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(last, f, indent=2)

    log_path = inst_dir / "scrape_log.json"
    log = {"runs": []}
    if log_path.exists():
        with open(log_path) as f:
            log = json.load(f)
    log["runs"].append({
        "run_id": RUN_ID,
        "timestamp": now,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    })
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)


def main():
    results = []
    for slug, name, url in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        time.sleep(2)
        html, err = fetch(url)
        if err:
            update_scrape_state(inst_dir, slug, "error", 0, 0, err)
            print(f"RESULT|{slug}|error|0|0")
            results.append((slug, "error", 0, 0))
            continue

        doc_links = extract_doc_links(html, url)
        has_tenders = has_tender_content(html, url)

        if has_tenders and doc_links:
            year = datetime.now().year
            existing = list((inst_dir / "tenders" / "active").glob("*.json"))
            seq = len(existing) + 1
            prefix = slug.upper().replace("-", "")[:12]
            tender_id = f"{prefix}-{year}-{seq:03d}"
            tender_data = {
                "title": f"Tender from {name}",
                "description": "Scraped from website",
                "published_date": datetime.now().strftime("%Y-%m-%d"),
                "closing_date": "",
                "category": "General",
                "contact_info": {"email": extract_emails(html)[:3]},
            }
            doc_count = save_tender(inst_dir, slug, tender_id, tender_data, doc_links, url)
            update_scrape_state(inst_dir, slug, "success", 1, doc_count)
            print(f"RESULT|{slug}|tenders|1|{doc_count}")
            results.append((slug, "tenders", 1, doc_count))
        elif has_tenders and not doc_links:
            update_scrape_state(inst_dir, slug, "success", 0, 0)
            print(f"RESULT|{slug}|tenders_no_docs|0|0")
            results.append((slug, "tenders_no_docs", 0, 0))
        else:
            emails = extract_emails(html)
            append_lead(
                slug, name, url, emails, "sell",
                f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                f"Partnership Opportunity – ZIMA Solutions & {name}",
                f"Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            )
            update_scrape_state(inst_dir, slug, "no_tenders", 0, 0)
            print(f"RESULT|{slug}|no_tenders|0|0")
            results.append((slug, "no_tenders", 0, 0))

    print("\n--- BATCH COMPLETE ---")
    for slug, status, tc, dc in results:
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")


if __name__ == "__main__":
    main()
