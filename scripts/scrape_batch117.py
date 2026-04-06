#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.
Run ID: run_20260313_205329_batch117
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch117"

INSTITUTIONS = [
    "technoauditors", "technodrillers", "technoimage", "technosolutions", "technotion",
    "techup", "techy8", "tecomatetours", "teea", "tef", "teiti", "teknicon",
    "teletronics", "tellysafaris", "temboadventure", "temboni", "temdo", "temekemc",
    "temesa", "tendampya", "tenders", "tendersoko", "tenmet", "tepu", "tervisflink",
]

DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|rfp|rfq|eoi|rfi|manunuzi|invitation to bid|procurement)\b",
    re.I
)


def load_readme(slug):
    path = PROJECT / "institutions" / slug / "README.md"
    if not path.exists():
        return None, None, None
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                fm = yaml.safe_load(parts[1])
                inst = fm.get("institution", {}) or {}
                web = fm.get("website", {}) or {}
                return (
                    web.get("tender_url") or web.get("homepage", ""),
                    inst.get("name", slug),
                    fm.get("contact", {}) or {}
                )
            except Exception:
                pass
            # Fallback: regex parse without yaml
            fm = parts[1]
            tender_url = None
            homepage = None
            for m in re.finditer(r"tender_url:\s*[\"']?([^\"'\n]+)[\"']?", fm):
                tender_url = m.group(1).strip()
                break
            for m in re.finditer(r"homepage:\s*[\"']?([^\"'\n]+)[\"']?", fm):
                homepage = m.group(1).strip()
                break
            name = slug
            for m in re.finditer(r"name:\s*[\"']([^\"']+)[\"']", fm):
                name = m.group(1).strip()
                break
            return (tender_url or homepage, name, {})
    return None, None, None


def fetch_url(url, timeout=30):
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0 (compatible; TendersBot/1.0)", "--max-time", str(timeout), url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        return None
    return None


def extract_emails(html):
    if not html:
        return []
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html))
    return sorted([e for e in emails if not any(x in e.lower() for x in ["example.com", "sentry.io", "wixpress", "schema.org", "yimg.com", "google.com", "facebook.com", "twitter.com", "linkedin.com", "youtube.com", "gravatar", "w3.org", "png", "gif", "jpg"])])


def extract_doc_links(html, base_url):
    if not html:
        return []
    from html.parser import HTMLParser
    links = []
    class LinkParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "a":
                for k, v in attrs:
                    if k == "href" and v:
                        v = v.strip()
                        if any(v.lower().endswith(ext) for ext in DOC_EXTENSIONS):
                            full = urljoin(base_url, v)
                            if base_url in full or urlparse(base_url).netloc in full:
                                links.append(full)
    try:
        p = LinkParser()
        p.feed(html)
    except Exception:
        pass
    return list(dict.fromkeys(links))


def has_tender_content(html):
    if not html:
        return False
    return bool(TENDER_KEYWORDS.search(html))


def scrape_institution(slug):
    tender_url, inst_name, contact = load_readme(slug)
    if not tender_url:
        return "error", 0, 0, "No README or tender_url"
    html = fetch_url(tender_url)
    if not html:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "last_scrape.json").write_text(json.dumps({
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "run_id": RUN_ID,
            "active_tenders_count": 0,
            "status": "error",
            "error": "Fetch failed or timeout",
        }, indent=2), encoding="utf-8")
        scrape_log = {"runs": []}
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            scrape_log = json.loads(log_path.read_text(encoding="utf-8"))
        scrape_log["runs"].append({"run_id": RUN_ID, "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "status": "error", "tenders_found": 0, "documents_downloaded": 0})
        log_path.write_text(json.dumps(scrape_log, indent=2), encoding="utf-8")
        return "error", 0, 0, "Fetch failed or timeout"
    emails = extract_emails(html)
    doc_links = extract_doc_links(html, tender_url)
    has_tenders = has_tender_content(html)
    inst_dir = PROJECT / "institutions" / slug
    inst_dir.mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)
    contact_emails = []
    if isinstance(contact, dict):
        if contact.get("email"):
            contact_emails.append(contact["email"])
        contact_emails.extend(contact.get("alternate_emails", []))
    all_emails = list(dict.fromkeys([e for e in (contact_emails + emails) if isinstance(e, str) and "@" in e and "." in e.split("@")[-1]]))
    if has_tenders and doc_links:
        seq = 1
        tender_id = f"{slug.upper().replace('-','')[:12]}-2026-{seq:03d}"
        tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
        download_dir = inst_dir / "downloads" / tender_id / "original"
        extracted_dir = inst_dir / "downloads" / tender_id / "extracted"
        download_dir.mkdir(parents=True, exist_ok=True)
        extracted_dir.mkdir(parents=True, exist_ok=True)
        docs_saved = []
        for url in doc_links[:20]:
            try:
                out_name = url.split("/")[-1].split("?")[0] or "document"
                if not any(out_name.lower().endswith(ext) for ext in DOC_EXTENSIONS):
                    out_name += ".pdf"
                out_path = download_dir / out_name
                subprocess.run(
                    ["curl", "-s", "-L", "-o", str(out_path), "-A", "Mozilla/5.0", "--max-time", "60", url],
                    capture_output=True,
                    timeout=65,
                )
                if out_path.exists() and out_path.stat().st_size > 0:
                    docs_saved.append({"filename": out_name, "original_url": url})
            except Exception:
                pass
        tender_data = {
            "tender_id": tender_id,
            "institution": slug,
            "title": inst_name or slug,
            "description": "",
            "published_date": None,
            "closing_date": None,
            "category": "General",
            "status": "active",
            "source_url": tender_url,
            "documents": docs_saved,
            "contact": {"email": all_emails[0] if all_emails else None},
            "scraped_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        tender_path.write_text(json.dumps(tender_data, indent=2), encoding="utf-8")
        for doc in docs_saved:
            orig = download_dir / doc["filename"]
            if orig.exists():
                ext = Path(doc["filename"]).suffix.lower()
                txt_path = extracted_dir / (Path(doc["filename"]).stem + ".txt")
                try:
                    if ext == ".pdf":
                        r = subprocess.run(
                            [sys.executable, "-m", "tools", "pdf", "read", str(orig)],
                            cwd=PROJECT,
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )
                        if r.returncode == 0 and r.stdout:
                            txt_path.write_text(r.stdout[:50000], encoding="utf-8")
                    elif ext in (".docx", ".doc"):
                        r = subprocess.run(
                            [sys.executable, "-m", "tools", "docx", "read", str(orig)],
                            cwd=PROJECT,
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )
                        if r.returncode == 0 and r.stdout:
                            txt_path.write_text(r.stdout[:50000], encoding="utf-8")
                except Exception:
                    pass
        last_scrape = {
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "run_id": RUN_ID,
            "active_tenders_count": 1,
            "status": "success",
            "error": None,
        }
        scrape_log = {"runs": []}
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            scrape_log = json.loads(log_path.read_text(encoding="utf-8"))
        scrape_log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "success",
            "tenders_found": 1,
            "documents_downloaded": len(docs_saved),
        })
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")
        log_path.write_text(json.dumps(scrape_log, indent=2), encoding="utf-8")
        return "tenders", 1, len(docs_saved), None
    else:
        lead = {
            "institution_slug": slug,
            "institution_name": inst_name or slug.replace("-", " ").title(),
            "website_url": tender_url,
            "emails": all_emails[:5],
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {inst_name or slug} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name or slug}",
            "draft_email_body": f"Dear {inst_name or slug} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {inst_name or slug}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
            "status": "pending",
        }
        leads_path = PROJECT / "opportunities" / "leads.json"
        leads = []
        if leads_path.exists():
            leads = json.loads(leads_path.read_text(encoding="utf-8"))
            if not isinstance(leads, list):
                leads = leads.get("leads", [])
        existing_slugs = {l.get("institution_slug") for l in leads}
        if slug not in existing_slugs:
            leads.append(lead)
            leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
        last_scrape = {
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "run_id": RUN_ID,
            "active_tenders_count": 0,
            "status": "success",
            "error": None,
        }
        scrape_log = {"runs": []}
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            scrape_log = json.loads(log_path.read_text(encoding="utf-8"))
        scrape_log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "success",
            "tenders_found": 0,
            "documents_downloaded": 0,
        })
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")
        log_path.write_text(json.dumps(scrape_log, indent=2), encoding="utf-8")
        return "no_tenders", 0, 0, None


def main():
    import time
    for slug in INSTITUTIONS:
        try:
            status, tc, dc, err = scrape_institution(slug)
            if err:
                status = "error"
            print(f"RESULT|{slug}|{status}|{tc}|{dc}")
        except Exception as e:
            print(f"RESULT|{slug}|error|0|0")
            inst_dir = PROJECT / "institutions" / slug
            if inst_dir.exists():
                last_scrape = {
                    "institution": slug,
                    "last_scrape": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "run_id": RUN_ID,
                    "active_tenders_count": 0,
                    "status": "error",
                    "error": str(e),
                }
                (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")
        time.sleep(2)
    subprocess.run(
        [sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=PROJECT,
        capture_output=True,
    )
    print("\n--- BATCH COMPLETE ---")


if __name__ == "__main__":
    main()
