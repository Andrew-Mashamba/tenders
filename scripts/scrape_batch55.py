#!/usr/bin/env python3
"""Scrape 25 institutions (batch55): tenders or leads. Run ID: run_20260315_060430_batch55."""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Ensure project tools are importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch55"
LEADS_JSON = PROJECT / "opportunities" / "leads.json"

INSTITUTIONS = [
    "jetnsons", "jewelery", "jewellery", "jfc", "jhnservices", "jhtechnologies",
    "jiaoyangsteel", "jiba", "jifunzeujasiriamali", "jikite", "jikosokoni",
    "jitegemeeholdings", "jiuzie", "jkci", "jkplug", "jkt", "jlchris",
    "jlohay", "jmb", "jmecl", "jml", "jmp", "jntanzania", "jobplan", "jobs",
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|procurement|zabuni|manunuzi|rfi|rfp|rfq|eoi|bid|bids)\b", re.I
)
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
DOC_EXT = re.compile(r"\.(pdf|doc|docx|xls|xlsx|zip)(\?|$)", re.I)


def load_config(slug):
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return {}
    text = readme.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    try:
        import yaml
        parts = text.split("---", 2)
        return yaml.safe_load(parts[1]) or {}
    except Exception:
        return {}


def get_url(config):
    w = config.get("website") or {}
    url = w.get("tender_url") or w.get("homepage") or ""
    # jikite has invalid data:image tender_url - use homepage
    if url.startswith("data:"):
        url = w.get("homepage") or ""
    return url


def get_institution_name(config):
    inst = config.get("institution") or {}
    return inst.get("name") or inst.get("slug") or ""


def fetch(url, timeout=30):
    try:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"},
            timeout=timeout,
            allow_redirects=True,
        )
        r.raise_for_status()
        return r.text, r.url, None
    except Exception as e:
        return None, url, str(e)


def extract_tenders(html, base_url, config):
    """Parse HTML for tender items. Returns list of dicts with title, date, doc_links."""
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    sel = (config.get("scraping") or {}).get("selectors") or {}
    container_sel = sel.get("container") or "main, .content, article, body"
    item_sel = sel.get("tender_item") or "article, .tender-item, .card, tr, li"
    title_sel = sel.get("title") or "h2, h3, h4, .tender-title, a"
    date_sel = sel.get("date") or ".date, .closing-date, time"
    doc_sel = sel.get("document_link") or 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'

    tenders = []
    containers = soup.select(container_sel) if container_sel else [soup]
    for container in containers:
        items = container.select(item_sel) if item_sel else []
        for item in items:
            text = item.get_text(separator=" ", strip=True)
            if not TENDER_KEYWORDS.search(text) and len(text) < 30:
                continue
            title_el = item.select_one(title_sel) if title_sel else item
            title = (title_el.get_text(strip=True) if title_el else "")[:200] or text[:200]
            date_el = item.select_one(date_sel) if date_sel else None
            date_val = date_el.get_text(strip=True) if date_el else ""
            doc_links = []
            for a in item.select(doc_sel) if doc_sel else item.find_all("a", href=True):
                href = a.get("href", "")
                if DOC_EXT.search(href):
                    full = urljoin(base_url, href)
                    doc_links.append(full)
            for a in item.find_all("a", href=True):
                href = a.get("href", "")
                if any(href.lower().endswith(x) for x in [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip"]):
                    full = urljoin(base_url, href)
                    if full not in doc_links:
                        doc_links.append(full)
            # Also check whole page for document links (e.g. JKT has PDF in different section)
            if not doc_links:
                for a in soup.find_all("a", href=True):
                    href = a.get("href", "")
                    if DOC_EXT.search(href):
                        full = urljoin(base_url, href)
                        if full not in doc_links:
                            doc_links.append(full)
            strong_terms = re.compile(r"\b(tender|tenders|zabuni|manunuzi|procurement|taarifa)\b", re.I)
            if doc_links or strong_terms.search(text):
                if title or len(text) > 50:
                    tenders.append({
                        "title": title or "Untitled",
                        "date": date_val,
                        "doc_links": list(set(doc_links)),
                        "snippet": text[:300],
                    })
    # JKT-style: single PDF announcement on page
    if not tenders:
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if DOC_EXT.search(href) and TENDER_KEYWORDS.search(html[:5000]):
                full = urljoin(base_url, href)
                tenders.append({
                    "title": a.get_text(strip=True) or "Announcement",
                    "date": "",
                    "doc_links": [full],
                    "snippet": "",
                })
                break
    return tenders


def extract_emails(html):
    return list(set(EMAIL_PATTERN.findall(html or "")))


def download_doc(url, dest_path, timeout=60):
    try:
        r = requests.get(
            url,
            headers={"User-Agent": "TendersBot/1.0"},
            timeout=timeout,
            stream=True,
        )
        r.raise_for_status()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True, None
    except Exception as e:
        return False, str(e)


def create_lead(slug, config, url, html):
    raw_name = get_institution_name(config) or slug
    inst_name = re.sub(r"&#\d+;", "", raw_name).strip()[:80] or slug
    emails = extract_emails(html or "")
    emails = [e for e in emails if not any(x in e.lower() for x in ["example.com", "domain.com", "yoursite", "sentry", "wixpress", "gravatar", "schema.org", ".png", ".jpg", ".jpeg", ".gif"])]
    if not emails and config.get("contact"):
        c = config["contact"]
        if isinstance(c.get("email"), str) and "@" in str(c["email"]) and "." in str(c["email"]):
            emails.append(c["email"])
        for alt in c.get("alternate_emails") or []:
            if isinstance(alt, str) and "@" in alt and "." in alt and not any(x in alt.lower() for x in [".png", ".jpg"]):
                emails.append(alt)
    emails = list(dict.fromkeys(emails))[:5]

    body = f"""Dear {inst_name} Team,

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
    return {
        "institution_slug": slug,
        "institution_name": inst_name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
        "draft_email_body": body,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    }


def append_lead(lead):
    leads = []
    if LEADS_JSON.exists():
        try:
            with open(LEADS_JSON) as f:
                data = json.load(f)
            leads = data if isinstance(data, list) else data.get("leads", [])
        except Exception:
            pass
    slugs = {x.get("institution_slug") for x in leads}
    if lead["institution_slug"] not in slugs:
        leads.append(lead)
        with open(LEADS_JSON, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)


def update_inst(slug, status, tenders, docs, err=None):
    inst = PROJECT / "institutions" / slug
    inst.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    (inst / "last_scrape.json").write_text(json.dumps({
        "institution": slug, "last_scrape": now, "next_scrape": now,
        "active_tenders_count": tenders, "status": status, "error": err,
    }, indent=2))
    log = inst / "scrape_log.json"
    data = {"runs": []}
    if log.exists():
        try:
            data = json.loads(log.read_text())
        except Exception:
            pass
    data["runs"].insert(0, {
        "run_id": RUN_ID, "timestamp": now, "duration_seconds": 0,
        "status": status, "tenders_found": tenders, "new_tenders": tenders,
        "updated_tenders": 0, "documents_downloaded": docs, "errors": [err] if err else [],
    })
    log.write_text(json.dumps(data, indent=2))


def main():
    leads_added = 0
    for slug in INSTITUTIONS:
        cfg = load_config(slug)
        url = get_url(cfg)
        if not url:
            update_inst(slug, "error", 0, 0, "No URL")
            print(f"RESULT|{slug}|error|0|0")
            continue
        if "facebook" in url or "instagram" in url or url.startswith("data:"):
            update_inst(slug, "skipped", 0, 0, "Invalid/social URL")
            print(f"RESULT|{slug}|skipped|0|0")
            continue

        html, final_url, err = fetch(url)
        if err:
            update_inst(slug, "error", 0, 0, err[:80])
            print(f"RESULT|{slug}|error|0|0")
            continue

        tenders = extract_tenders(html, final_url, cfg)
        if tenders:
            inst_dir = PROJECT / "institutions" / slug
            active_dir = inst_dir / "tenders" / "active"
            active_dir.mkdir(parents=True, exist_ok=True)
            doc_count = 0
            year = datetime.now().year
            for i, t in enumerate(tenders):
                tid = f"{slug.upper().replace('-', '')[:8]}-{year}-{i+1:03d}"
                tender_json = {
                    "tender_id": tid,
                    "institution": slug,
                    "title": t["title"],
                    "description": t.get("snippet", ""),
                    "published_date": t.get("date", ""),
                    "closing_date": t.get("date", ""),
                    "documents": [{"original_url": u, "filename": Path(urlparse(u).path).name} for u in t.get("doc_links", [])],
                    "source_url": final_url,
                    "scraped_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                }
                (active_dir / f"{tid}.json").write_text(json.dumps(tender_json, indent=2))
                downloads_dir = inst_dir / "downloads" / tid / "original"
                extracted_dir = inst_dir / "downloads" / tid / "extracted"
                for link in t.get("doc_links", []):
                    try:
                        fname = Path(urlparse(link).path).name or "document.pdf"
                        fname = re.sub(r"[^\w.\-]", "_", fname)[:100]
                        dest = downloads_dir / fname
                        ok, _ = download_doc(link, dest)
                        if ok:
                            doc_count += 1
                            extracted_dir.mkdir(parents=True, exist_ok=True)
                            txt_path = extracted_dir / (Path(fname).stem + ".txt")
                            try:
                                if dest.suffix.lower() == ".pdf":
                                    from tools.pdf.reader import extract_text
                                    txt_path.write_text(extract_text(str(dest)), encoding="utf-8")
                            except Exception:
                                pass
                    except Exception:
                        pass
            update_inst(slug, "success", len(tenders), doc_count)
            print(f"RESULT|{slug}|success|{len(tenders)}|{doc_count}")
        else:
            lead = create_lead(slug, cfg, final_url, html)
            append_lead(lead)
            leads_added += 1
            update_inst(slug, "success", 0, 0)
            print(f"RESULT|{slug}|no_tenders|0|0")

        time.sleep(10)  # Rate limit per anti_bot

    if leads_added > 0:
        try:
            subprocess.run(
                [sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")],
                cwd=PROJECT,
                capture_output=True,
                timeout=120,
            )
        except Exception:
            pass


if __name__ == "__main__":
    main()
