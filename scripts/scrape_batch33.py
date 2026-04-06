#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.
Run ID: run_20260315_060430_batch33
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch33"
INSTITUTIONS = [
    "eight", "eisttechnology", "ejcomputer", "ejsolution", "elbaliz", "elctnwd",
    "electricool", "electrocom", "elegexlogistics", "elements", "elemielectrical",
    "elevatedesignstudio", "elijerrytc", "elimu", "elimusaccos", "elinkconsult",
    "elique", "elite", "eliteagro", "elitedental", "elitedigital", "elitestore",
    "ellion", "ellipsis", "elm",
]

TENDER_KEYWORDS = re.compile(
    r"zabuni|tender|procurement|manunuzi|rfp|rfq|rfi|eoi|bid\s+(invitation|notice)|"
    r"expression\s+of\s+interest|request\s+for\s+(proposal|quotation)|closing\s+date",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug):
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return None
    text = readme.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                cfg = yaml.safe_load(parts[1])
                if cfg:
                    return cfg
            except Exception:
                pass
    m = re.search(r"tender_url:\s*[\"']?([^\"'\s]+)", text)
    if m:
        return {"website": {"tender_url": m.group(1)}}
    m = re.search(r"\*\*Tender Page:\*\*\s*(https?://[^\s]+)", text)
    if m:
        return {"website": {"tender_url": m.group(1).rstrip("/")}}
    return None


def fetch_url(url, use_insecure=False):
    cmd = ["curl", "-sL", "-A", "Mozilla/5.0 (compatible; TenderScraper/1.0)", "--connect-timeout", "15", "--max-time", "30"]
    if use_insecure or ".go.tz" in url or ".co.tz" in url or ".or.tz" in url or ".ac.tz" in url:
        cmd.append("-k")
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def extract_emails(html):
    if not html:
        return []
    return list(set(EMAIL_RE.findall(html)))


def has_tender_content(html):
    if not html:
        return False
    return bool(TENDER_KEYWORDS.search(html))


def extract_doc_links(html, base_url):
    if not html:
        return []
    links = []
    for ext in DOC_EXT:
        pat = re.compile(rf'href=["\']([^"\']*\{re.escape(ext)})["\']', re.I)
        for m in pat.finditer(html):
            href = m.group(1)
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                parsed = urlparse(base_url)
                href = f"{parsed.scheme}://{parsed.netloc}{href}"
            elif not href.startswith("http"):
                href = urljoin(base_url, href)
            if href and href not in [l["url"] for l in links]:
                links.append({"url": href, "filename": href.split("/")[-1].split("?")[0]})
    return links


def parse_generic_tenders(html, slug, base_url):
    tenders = []
    doc_links = extract_doc_links(html, base_url)
    tender_doc_pattern = re.compile(r"(tender|procurement|rfp|rfq|rfi|eoi|bid|zabuni|advert)", re.I)
    tender_docs = [d for d in doc_links if tender_doc_pattern.search(d["url"]) or tender_doc_pattern.search(d.get("filename", ""))]
    if not doc_links and not has_tender_content(html):
        return tenders
    docs_to_use = tender_docs if tender_docs else doc_links
    if docs_to_use and not tenders:
        prefix = slug.upper().replace("-", "")[:10]
        tenders.append({
            "tender_id": f"{prefix}-2026-001",
            "title": f"Documents from {slug}",
            "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "closing_date": "",
            "document_links": [d["url"] for d in docs_to_use],
            "source_url": base_url,
        })
    return tenders


def download_doc(url, dest_path, use_insecure=False):
    cmd = ["curl", "-sL", "-A", "Mozilla/5.0", "-o", str(dest_path), "--connect-timeout", "20", "--max-time", "45"]
    if use_insecure or ".go.tz" in url or ".co.tz" in url or ".or.tz" in url or ".ac.tz" in url:
        cmd.append("-k")
    cmd.append(url)
    try:
        r = subprocess.run(cmd, timeout=50)
        return r.returncode == 0 and dest_path.exists() and dest_path.stat().st_size > 0
    except Exception:
        return False


def extract_text_from_doc(filepath):
    ext = filepath.suffix.lower()
    try:
        if ext == ".pdf":
            sys.path.insert(0, str(PROJECT))
            from tools.pdf.reader import extract_text
            return extract_text(str(filepath))
        elif ext in (".docx", ".doc"):
            from tools.docx.reader import extract_text
            return extract_text(str(filepath))
        elif ext in (".xlsx", ".xls"):
            from tools.xlsx.reader import extract_data
            data = extract_data(str(filepath))
            return json.dumps(data, indent=2) if data else ""
    except Exception:
        pass
    return ""


def process_institution(slug):
    cfg = load_readme(slug)
    if not cfg:
        return "error", 0, 0, "No README config"
    website = cfg.get("website", {})
    tender_url = website.get("tender_url") or website.get("homepage")
    if not tender_url:
        return "error", 0, 0, "No tender_url"
    inst_name = cfg.get("institution", {}).get("name", slug)
    contact = cfg.get("contact", {})
    emails_from_readme = []
    if contact.get("email"):
        emails_from_readme.append(contact["email"])
    emails_from_readme.extend(contact.get("alternate_emails", []) or [])

    html = fetch_url(tender_url)
    if not html:
        return "error", 0, 0, "Fetch failed or empty"

    tenders = parse_generic_tenders(html, slug, tender_url)
    if not tenders and has_tender_content(html):
        tenders = parse_generic_tenders(html, slug, tender_url)

    inst_dir = PROJECT / "institutions" / slug
    inst_dir.mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)

    doc_count = 0
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if tenders:
        for t in tenders:
            tid = t.get("tender_id", f"{slug.upper()}-2026-001")
            docs = t.get("document_links", [])
            download_dir = inst_dir / "downloads" / tid / "original"
            extracted_dir = inst_dir / "downloads" / tid / "extracted"
            download_dir.mkdir(parents=True, exist_ok=True)
            extracted_dir.mkdir(parents=True, exist_ok=True)

            for url in docs:
                fname = url.split("/")[-1].split("?")[0] or "document.pdf"
                fname = fname.replace("%20", "_").replace("%2F", "_")
                dest = download_dir / fname
                if download_doc(url, dest, use_insecure=".go.tz" in url or ".or.tz" in url):
                    doc_count += 1
                    txt = extract_text_from_doc(dest)
                    if txt:
                        (extracted_dir / (Path(fname).stem + ".txt")).write_text(txt, encoding="utf-8")

            tender_json = {
                "tender_id": tid,
                "institution": slug,
                "title": t.get("title", ""),
                "description": "",
                "published_date": t.get("published_date", ""),
                "closing_date": t.get("closing_date", ""),
                "category": "General",
                "status": "active",
                "source_url": t.get("source_url", tender_url),
                "documents": [{"original_url": u, "local_path": str(inst_dir / "downloads" / tid / "original" / (u.split("/")[-1].split("?")[0].replace("%20", "_").replace("%2F", "_") or "doc.pdf"))} for u in docs],
                "contact": {"email": contact.get("email", ""), "phone": contact.get("phone", "")},
                "scraped_at": now_iso,
                "last_checked": now_iso,
            }
            closing = t.get("closing_date", "")
            is_closed = False
            try:
                if closing and len(closing) >= 8:
                    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d/%m/%Y"):
                        try:
                            close_dt = datetime.strptime(closing.strip()[:20], fmt)
                            if close_dt.date() < datetime.now().date():
                                is_closed = True
                            break
                        except ValueError:
                            continue
            except Exception:
                pass
            if is_closed:
                (inst_dir / "tenders" / "closed" / f"{tid}.json").write_text(json.dumps(tender_json, indent=2, ensure_ascii=False), encoding="utf-8")
            else:
                (inst_dir / "tenders" / "active" / f"{tid}.json").write_text(json.dumps(tender_json, indent=2, ensure_ascii=False), encoding="utf-8")

        active_count = len(list((inst_dir / "tenders" / "active").glob("*.json")))
        last_scrape = {
            "institution": slug,
            "last_scrape": now_iso,
            "next_scrape": now_iso,
            "active_tenders_count": active_count,
            "status": "success",
            "error": None,
            "run_id": RUN_ID,
            "documents_downloaded": doc_count,
        }
    else:
        all_emails = list(set(extract_emails(html) + emails_from_readme))
        all_emails = [e for e in all_emails if "example" not in e.lower() and "sitename" not in e.lower() and "yoursite" not in e.lower() and "ajax-loader" not in e.lower()]
        if not all_emails and contact.get("email"):
            all_emails = [contact["email"]]

        lead = {
            "institution_slug": slug,
            "institution_name": inst_name,
            "website_url": tender_url.rstrip("/").split("#")[0],
            "emails": all_emails[:5],
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
            "draft_email_body": f"Dear {inst_name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {inst_name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": now_iso,
            "status": "pending",
        }
        leads_path = PROJECT / "opportunities" / "leads.json"
        leads_data = []
        if leads_path.exists():
            try:
                leads_data = json.loads(leads_path.read_text(encoding="utf-8"))
            except Exception:
                leads_data = []
        if not isinstance(leads_data, list):
            leads_data = leads_data.get("leads", []) or []
        lead_created = not any(l.get("institution_slug") == slug for l in leads_data)
        if lead_created:
            leads_data.append(lead)
            leads_path.parent.mkdir(parents=True, exist_ok=True)
            with open(leads_path, "w", encoding="utf-8") as f:
                json.dump(leads_data, f, indent=2, ensure_ascii=False)

        last_scrape = {
            "institution": slug,
            "last_scrape": now_iso,
            "next_scrape": now_iso,
            "active_tenders_count": 0,
            "status": "success",
            "error": None,
            "run_id": RUN_ID,
            "lead_created": lead_created,
        }
        tenders = []
        active_count = 0

    (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")
    scrape_log = inst_dir / "scrape_log.json"
    log_entry = {
        "run_id": RUN_ID,
        "timestamp": now_iso,
        "status": "success",
        "tenders_found": len(tenders),
        "documents_downloaded": doc_count,
    }
    if scrape_log.exists():
        try:
            log_data = json.loads(scrape_log.read_text(encoding="utf-8"))
            if isinstance(log_data, list):
                log_data = {"runs": log_data}
            log_data.setdefault("runs", []).append(log_entry)
        except Exception:
            log_data = {"runs": [log_entry]}
    else:
        log_data = {"runs": [log_entry]}
    scrape_log.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

    status = "tenders" if tenders else "no_tenders"
    return status, len(tenders), doc_count, None


def main():
    lead_updated = False
    for slug in INSTITUTIONS:
        try:
            status, tc, dc, err = process_institution(slug)
            if err:
                print(f"RESULT|{slug}|error|0|0  # {err}")
            else:
                print(f"RESULT|{slug}|{status}|{tc}|{dc}")
                lead_updated = True
        except Exception as e:
            print(f"RESULT|{slug}|error|0|0  # {e}")
    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=str(PROJECT), check=False)


if __name__ == "__main__":
    main()
