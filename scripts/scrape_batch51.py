#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.
Run ID: run_20260315_060430_batch51
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch51"
INSTITUTIONS = [
    "imperialmedia", "imperialsecurity", "imperium", "index", "indianschooldsm",
    "infinicare", "infinitecleaners", "influencers", "infoage", "infogear",
    "infosec", "infosoftconsult", "infosoftz", "infotaaluma", "infotech",
    "infowise", "ingenuityworks", "innoafrica", "innovex", "innovo",
    "inqababiotec", "insight", "insignia", "inspire", "inspirehatua",
]

TENDER_KEYWORDS = re.compile(
    r"zabuni|tender|procurement|manunuzi|rfp|rfq|rfi|eoi|bid\s+(invitation|notice)|"
    r"expression\s+of\s+interest|request\s+for\s+(proposal|quotation)|bidding",
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
        return {"website": {"tender_url": m.group(1)}, "institution": {"name": slug}}
    m = re.search(r"\*\*Tender Page:\*\*\s*(https?://[^\s]+)", text)
    if m:
        return {"website": {"tender_url": m.group(1).rstrip("/")}, "institution": {"name": slug}}
    return None


def fetch_url(url, use_insecure=False):
    cmd = ["curl", "-sL", "-A", "Mozilla/5.0", "--connect-timeout", "15", "--max-time", "30"]
    if use_insecure or ".go.tz" in url or ".co.tz" in url or ".or.tz" in url or ".ac.tz" in url or ".co.za" in url:
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
    # Only create meta-tender if docs look like tender docs (not admission results, company profiles)
    skip_doc_patterns = ["admission", "result", "profile", "company-profile", "consolidated"]
    tender_doc_links = []
    for d in doc_links:
        url_lower = d["url"].lower()
        fname = d.get("filename", "").lower()
        if any(p in url_lower or p in fname for p in skip_doc_patterns):
            continue
        tender_doc_links.append(d["url"])
    if tender_doc_links and has_tender_content(html):
        prefix = slug.upper().replace("-", "")[:8]
        tenders.append({
            "tender_id": f"{prefix}-2026-001",
            "title": f"Documents from {slug}",
            "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "closing_date": "",
            "document_links": tender_doc_links,
            "source_url": base_url,
        })
    elif doc_links and has_tender_content(html) and not any(
        p in doc_links[0]["url"].lower() for p in skip_doc_patterns
    ):
        prefix = slug.upper().replace("-", "")[:8]
        tenders.append({
            "tender_id": f"{prefix}-2026-001",
            "title": f"Documents from {slug}",
            "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "closing_date": "",
            "document_links": [d["url"] for d in doc_links],
            "source_url": base_url,
        })
    return tenders


def download_doc(url, dest_path, use_insecure=False):
    cmd = ["curl", "-sL", "-A", "Mozilla/5.0", "-o", str(dest_path), "--connect-timeout", "20", "--max-time", "45"]
    if use_insecure or ".go.tz" in url or ".co.tz" in url or ".ac.tz" in url or ".co.za" in url:
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


def append_lead_if_new(slug, inst_name, website_url, emails, opportunity_type, opportunity_desc, draft_subj, draft_body):
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads_data = []
    if leads_path.exists():
        try:
            leads_data = json.loads(leads_path.read_text(encoding="utf-8"))
        except Exception:
            leads_data = []
    if not isinstance(leads_data, list):
        leads_data = leads_data.get("leads", [])
    if any(l.get("institution_slug") == slug for l in leads_data):
        return
    lead = {
        "institution_slug": slug,
        "institution_name": inst_name,
        "website_url": website_url,
        "emails": emails,
        "opportunity_type": opportunity_type,
        "opportunity_description": opportunity_desc,
        "draft_email_subject": draft_subj,
        "draft_email_body": draft_body,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    }
    leads_data.append(lead)
    leads_path.parent.mkdir(parents=True, exist_ok=True)
    leads_path.write_text(json.dumps(leads_data, indent=2, ensure_ascii=False), encoding="utf-8")


def update_scrape_state(inst_dir, slug, status, tender_count, doc_count, error=None):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (inst_dir / "last_scrape.json").write_text(json.dumps({
        "institution": slug,
        "last_scrape": now,
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }, indent=2), encoding="utf-8")
    log_path = inst_dir / "scrape_log.json"
    log_data = {"runs": []}
    if log_path.exists():
        try:
            log_data = json.loads(log_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    log_data.setdefault("runs", []).append({
        "run_id": RUN_ID,
        "timestamp": now,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    })
    log_path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")


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
    emails_from_readme.extend(contact.get("alternate_emails", []))

    use_insecure = ".go.tz" in tender_url or ".co.tz" in tender_url or ".ac.tz" in tender_url or ".co.za" in tender_url
    html = fetch_url(tender_url, use_insecure=use_insecure)
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
                dest = download_dir / fname
                if download_doc(url, dest, use_insecure=use_insecure):
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
                "document_links": docs,
                "contact_info": {"email": emails_from_readme[0] if emails_from_readme else ""},
                "source_url": t.get("source_url", tender_url),
            }
            (inst_dir / "tenders" / "active" / f"{tid}.json").write_text(
                json.dumps(tender_json, indent=2), encoding="utf-8"
            )
        update_scrape_state(inst_dir, slug, "success", len(tenders), doc_count)
        return "success", len(tenders), doc_count, None

    # No tenders: add lead if new, update state
    emails = extract_emails(html)
    if not emails:
        emails = emails_from_readme
    website_url = tender_url.rstrip("/")
    draft_subj = f"Partnership Opportunity – ZIMA Solutions & {inst_name}"
    draft_body = f"""Dear {inst_name} Team,

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
"""
    append_lead_if_new(
        slug, inst_name, website_url, emails, "sell",
        "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        draft_subj, draft_body
    )
    update_scrape_state(inst_dir, slug, "success", 0, 0)
    return "no_tenders", 0, 0, None


def main():
    for slug in INSTITUTIONS:
        try:
            status, tender_count, doc_count, err = process_institution(slug)
            if err:
                inst_dir = PROJECT / "institutions" / slug
                inst_dir.mkdir(parents=True, exist_ok=True)
                update_scrape_state(inst_dir, slug, "error", 0, 0, err)
            print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
        except Exception as e:
            inst_dir = PROJECT / "institutions" / slug
            inst_dir.mkdir(parents=True, exist_ok=True)
            update_scrape_state(inst_dir, slug, "error", 0, 0, str(e))
            print(f"RESULT|{slug}|error|0|0")
    subprocess.run(
        [sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=str(PROJECT),
        check=False,
    )


if __name__ == "__main__":
    main()
