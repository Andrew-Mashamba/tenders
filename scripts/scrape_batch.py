#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.
Run ID: run_20260315_060430_batch22
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch22"
INSTITUTIONS = [
    "chinyami", "cholemjini", "chora-interiors", "chragg", "christadelphian",
    "chunyadc", "church", "chuwaadvocates", "cib", "cit", "citigroup-suppliers",
    "cits", "city-tech", "citycom", "citylinkhotel", "claretianpublications",
    "clarion", "clasktanzania", "clc", "cleaningmaster", "clickpayafrica",
    "climateair", "climbkilimanjaro", "climtech", "cmadvocates",
]

TENDER_KEYWORDS = re.compile(
    r"zabuni|tender|procurement|manunuzi|rfp|rfq|rfi|eoi|bid\s+(invitation|notice)|"
    r"expression\s+of\s+interest|request\s+for\s+(proposal|quotation)",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug):
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return None
    text = readme.read_text(encoding="utf-8")
    # Parse YAML frontmatter
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
    # Fallback: extract tender_url from markdown
    m = re.search(r"tender_url:\s*[\"']?([^\"'\s]+)", text)
    if m:
        return {"website": {"tender_url": m.group(1)}}
    m = re.search(r"\*\*Tender Page:\*\*\s*(https?://[^\s]+)", text)
    if m:
        return {"website": {"tender_url": m.group(1).rstrip("/")}}
    return None


def fetch_url(url, use_insecure=False):
    cmd = ["curl", "-sL", "-A", "Mozilla/5.0", "--connect-timeout", "15", "--max-time", "30"]
    if use_insecure or ".go.tz" in url or ".co.tz" in url or ".or.tz" in url:
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


def parse_chunyadc_tenders(html, base_url):
    """Chunya DC has table: Jina la Zabuni | date | date | Download link"""
    tenders = []
    if not html or "Jina la Zabuni" not in html:
        return tenders
    parsed = urlparse(base_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    # Match <tr><td>TITLE</td><td>date</td><td>date</td><td><a href="...">Download</a></td></tr>
    pat = re.compile(
        r'<tr><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td><a\s+href="([^"]+)"[^>]*>Download</a></td></tr>',
        re.I
    )
    for i, m in enumerate(pat.finditer(html)):
        title, pub_date, close_date, doc_url = m.groups()
        if doc_url.startswith("/"):
            doc_url = base + doc_url
        year = "2022" if "2022" in close_date else "2017" if "2017" in close_date else "2026"
        tender_id = f"CHUNYADC-{year}-{i+1:03d}"
        tenders.append({
            "tender_id": tender_id,
            "title": title.strip(),
            "published_date": pub_date.strip(),
            "closing_date": close_date.strip(),
            "document_links": [doc_url],
            "source_url": base_url,
        })
    return tenders


def parse_generic_tenders(html, slug, base_url):
    """Generic: look for tender-like items with doc links."""
    tenders = []
    doc_links = extract_doc_links(html, base_url)
    if not doc_links and not has_tender_content(html):
        return tenders
    # If we have doc links but no structured tenders, create one meta-tender
    if doc_links and not tenders:
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
    if use_insecure or ".go.tz" in url:
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
    emails_from_readme.extend(contact.get("alternate_emails", []))

    # chunyadc: tenders are at /tenders not procurement-and-supply
    fetch_url_actual = tender_url
    if slug == "chunyadc":
        parsed = urlparse(tender_url)
        fetch_url_actual = f"{parsed.scheme}://{parsed.netloc}/tenders"
    html = fetch_url(fetch_url_actual)
    if not html:
        return "error", 0, 0, "Fetch failed or empty"

    # Institution-specific parsing
    if slug == "chunyadc":
        tenders = parse_chunyadc_tenders(html, fetch_url_actual)
    else:
        tenders = parse_generic_tenders(html, slug, tender_url)

    # Check for tender content even if no structured parse
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

            downloaded = []
            for url in docs:
                fname = url.split("/")[-1].split("?")[0] or "document.pdf"
                dest = download_dir / fname
                if download_doc(url, dest, use_insecure=".go.tz" in url):
                    downloaded.append(str(dest))
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
                "documents": [{"original_url": u, "local_path": str(inst_dir / "downloads" / tid / "original" / (u.split("/")[-1].split("?")[0] or "doc.pdf"))} for u in docs],
                "contact": {"email": contact.get("email", ""), "phone": contact.get("phone", "")},
                "scraped_at": now_iso,
                "last_checked": now_iso,
            }
            # Move to closed if closing_date passed
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
        # No tenders: create lead
        all_emails = list(set(extract_emails(html) + emails_from_readme))
        all_emails = [e for e in all_emails if "example" not in e.lower() and "sitename" not in e.lower() and "yoursite" not in e.lower()]
        if not all_emails and contact.get("email"):
            all_emails = [contact["email"]]

        lead = {
            "institution_slug": slug,
            "institution_name": inst_name,
            "website_url": tender_url.rstrip("/"),
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
        # Append if not already present
        if not any(l.get("institution_slug") == slug for l in leads_data):
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
            "lead_created": True,
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
            log_data.setdefault("runs", []).append(log_entry)
        except Exception:
            log_data = {"runs": [log_entry]}
    else:
        log_data = {"runs": [log_entry]}
    scrape_log.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

    status = "tenders" if tenders else "no_tenders"
    return status, len(tenders), doc_count, None


def main():
    for slug in INSTITUTIONS:
        try:
            status, tc, dc, err = process_institution(slug)
            if err:
                print(f"RESULT|{slug}|error|0|0  # {err}")
            else:
                print(f"RESULT|{slug}|{status}|{tc}|{dc}")
        except Exception as e:
            print(f"RESULT|{slug}|error|0|0  # {e}")
    # Sync leads to CSV after all institutions processed
    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=str(PROJECT), check=False)


if __name__ == "__main__":
    main()
