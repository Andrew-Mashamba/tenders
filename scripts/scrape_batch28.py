#!/usr/bin/env python3
"""Scrape batch 28: dexter through diversey (25 institutions)."""

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import urllib.request
import urllib.error

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = sys.argv[1] if len(sys.argv) > 1 else "run_20260313_205329_batch28"

# slug, tender_url, institution_name, homepage
INSTITUTIONS = [
    ("dexter", "https://dexter.co.tz/", "Dexter Attorneys", "https://dexter.co.tz/"),
    ("dextra", "https://dextra.co.tz/", "DEXTRA PHARMA LTD", "https://dextra.co.tz/"),
    ("dfc", "https://dfc.co.tz/", "DFC", "https://dfc.co.tz/"),
    ("dfd", "https://dfd.or.tz/", "DFD Global Centre", "https://dfd.or.tz/"),
    ("dflex", "https://dflex.co.tz/", "Dflex International Limited", "https://dflex.co.tz/"),
    ("dfnr", "https://dfnr.go.tz/", "DFNR", "https://dfnr.go.tz/"),
    ("dgt", "https://dgt.co.tz/", "DERICK GLOBAL TRADING", "https://dgt.co.tz/"),
    ("dhl", "https://www.dhl.com/", "DHL", "https://www.dhl.com/"),
    ("dhow", "https://www.dhow.co.tz/", "Dhow Furniture", "https://www.dhow.co.tz/"),
    ("diami", "https://diami.co.tz/", "Diami Company Limited", "https://diami.co.tz/"),
    ("diamondcement", "https://diamondcement.co.tz/", "Diamond Cement", "https://diamondcement.co.tz/"),
    ("diamondopticals", "https://diamondopticals.co.tz/", "Diamond Opticals Limited", "https://diamondopticals.co.tz/"),
    ("dianaroselogistics", "https://www.dianaroselogistics.co.tz/", "Dianarose Logistics", "https://www.dianaroselogistics.co.tz/"),
    ("dides", "https://dides.ac.tz/", "DIDES", "https://dides.ac.tz/"),
    ("digicom", "https://www.digicom.co.tz/", "Adams Digicom", "https://www.digicom.co.tz/"),
    ("digimatic", "https://digimatic.co.tz/", "Digimatic Tanzania", "https://digimatic.co.tz/"),
    ("diginect", "https://diginect-tz.com/", "Diginect", "https://diginect-tz.com/"),
    ("digitalchampions", "https://digitalchampions.co.tz/", "Digital Champions", "https://digitalchampions.co.tz/"),
    ("digitalplanet", "https://www.digitalplanet.co.tz/", "Digital Planet", "https://www.digitalplanet.co.tz/"),
    ("dilosinvestmentltd", "https://dilosinvestmentltd.co.tz/", "Dilos", "https://dilosinvestmentltd.co.tz/"),
    ("diramakini", "https://www.diramakini.co.tz/", "DIRAMAKINI", "https://www.diramakini.co.tz/"),
    ("dirmgroup", "https://dirmgroup.co.tz/", "DIRM GROUP", "https://dirmgroup.co.tz/"),
    ("dis", "https://dis.ac.tz/", "DIS", "https://dis.ac.tz/"),
    ("dit", "https://dit.ac.tz/", "Dar es Salaam Institute of Technology", "https://dit.ac.tz/"),
    ("diversey", "https://www.solenis.com/link/5723ead4cf9044cca31ead1849606616.aspx?type=procurement", "Diversey/Solenis", "https://www.solenis.com/"),
]

TENDER_KEYWORDS = re.compile(
    r'\b(tender|tenders|procurement|rfp|rfq|rfi|eoi|bidding|zabuni|manunuzi|'
    r'expression of interest|invitation to bid|request for proposal|'
    r'quotation|prequalification|invitation to tender)\b',
    re.I
)

DOC_EXT = re.compile(r'\.(pdf|doc|docx|xls|xlsx|zip)(?:\?|$)', re.I)
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def extract_yaml_field(content: str, key: str) -> str | None:
    m = re.search(rf'^\s*{re.escape(key)}:\s*["\']?([^"\'\n]+)', content, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def fetch_url(url: str, timeout: int = 15) -> tuple[str | None, str | None]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TenderBot/1.0)"})
        with urllib.request.urlopen(req, timeout=timeout) as f:
            body = f.read().decode("utf-8", errors="replace")
            return body, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, str(e.reason) if e.reason else str(e)
    except Exception as e:
        return None, str(e)


def extract_doc_links(html: str, base_url: str) -> list[tuple[str, str]]:
    links = []
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', html, re.I | re.S):
        href, text = m.group(1), m.group(2)
        if DOC_EXT.search(href):
            full = urljoin(base_url, href)
            links.append((full, (text or href).strip()[:80]))
    for m in re.finditer(r'href=["\']([^"\']*\.(?:pdf|doc|docx|xls|xlsx|zip)(?:\?[^"\']*)?)["\']', html, re.I):
        full = urljoin(base_url, m.group(1))
        if full not in [u for u, _ in links]:
            links.append((full, Path(urlparse(full).path).name or "document"))
    seen = set()
    out = []
    for u, t in links:
        if u not in seen and not u.startswith("mailto:"):
            seen.add(u)
            out.append((u, t))
    return out


def extract_emails(html: str) -> list[str]:
    return list(dict.fromkeys(EMAIL_RE.findall(html)))


def has_tender_content(html: str) -> bool:
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.I | re.S)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.I | re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    return bool(TENDER_KEYWORDS.search(text))


def is_tender_listing(html: str, doc_links: list) -> bool:
    return has_tender_content(html) and len(doc_links) > 0


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def slug_to_short(slug: str) -> str:
    parts = slug.replace("-", "").upper()
    if len(parts) > 6:
        parts = "".join(w[0] for w in slug.split("-")[:3]).upper() or parts[:6]
    return parts[:8]


def download_file(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TenderBot/1.0)"})
        with urllib.request.urlopen(req, timeout=60) as f:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(f.read())
            return True
    except Exception:
        return False


def process_institution(slug: str, tender_url: str, name: str, homepage: str) -> dict:
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    year = datetime.now().year

    html, err = fetch_url(tender_url)
    if err:
        entry = {"status": "error", "tender_count": 0, "doc_count": 0, "error": err}
        # Fall through to write last_scrape and scrape_log
        doc_links = []
        tenders_found = False
    else:
        doc_links = extract_doc_links(html, tender_url)
        tenders_found = is_tender_listing(html, doc_links)
    short = slug_to_short(slug)
    tender_count = 0
    doc_count = 0

    if tenders_found and doc_links:
        active_dir = inst_dir / "tenders" / "active"
        existing = list(active_dir.glob("*.json"))
        seq = len(existing) + 1
        tender_id = f"{short}-{year}-{seq:03d}"

        download_dir = inst_dir / "downloads" / tender_id / "original"
        extract_dir = inst_dir / "downloads" / tender_id / "extracted"
        download_dir.mkdir(parents=True, exist_ok=True)
        extract_dir.mkdir(parents=True, exist_ok=True)

        docs_meta = []
        for url, label in doc_links[:20]:
            fname = Path(urlparse(url).path).name or "document.pdf"
            fname = re.sub(r'[^\w.\-]', '_', fname)
            if not fname:
                fname = "document.pdf"
            dest = download_dir / fname
            if download_file(url, dest):
                doc_count += 1
                docs_meta.append({
                    "filename": fname,
                    "original_url": url,
                    "local_path": f"downloads/{tender_id}/original/{fname}",
                    "downloaded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                })
                ext_path = extract_dir / (Path(fname).stem + ".txt")
                try:
                    if fname.lower().endswith(".pdf"):
                        from tools.pdf.reader import extract_text
                        text = extract_text(str(dest))
                        ext_path.write_text(text or "", encoding="utf-8")
                    elif fname.lower().endswith((".docx", ".doc")):
                        from tools.docx.reader import extract_text
                        text = extract_text(str(dest))
                        ext_path.write_text(text or "", encoding="utf-8")
                except Exception:
                    pass

        tender_json = {
            "tender_id": tender_id,
            "institution": slug,
            "title": f"Tender/Procurement - {name}",
            "description": "Scraped from website. See documents.",
            "published_date": "",
            "closing_date": "",
            "category": "Procurement",
            "status": "active",
            "source_url": tender_url,
            "documents": docs_meta,
            "contact": {},
            "scraped_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "last_checked": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        (active_dir / f"{tender_id}.json").write_text(json.dumps(tender_json, indent=2), encoding="utf-8")
        tender_count = 1
        entry = {"status": "tenders", "tender_count": tender_count, "doc_count": doc_count}

    elif not err:
        emails = extract_emails(html)
        if not emails:
            for m in re.finditer(r'[\w.-]+@[\w.-]+\.\w+', html):
                e = m.group(0)
                if e not in emails and not e.startswith("example") and "@" in e:
                    emails.append(e)
        emails = list(dict.fromkeys(e for e in emails if len(e) > 5 and "." in e))
        contact_emails = []
        if (inst_dir / "README.md").exists():
            rm = (inst_dir / "README.md").read_text(encoding="utf-8")
            contact_emails.append(extract_yaml_field(rm, "email"))
            for m in re.finditer(r'[Ee]mail:\s*([^\s<>\n]+@[^\s<>\n]+)', rm):
                contact_emails.append(m.group(1).strip())
        contact_emails = [e for e in contact_emails if e]
        all_emails = list(dict.fromkeys(emails + contact_emails))

        opp_type = "sell"
        opp_desc = f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."

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

        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": homepage or tender_url,
            "emails": all_emails[:10],
            "opportunity_type": opp_type,
            "opportunity_description": opp_desc,
            "draft_email_subject": draft_subject,
            "draft_email_body": draft_body,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "pending",
        }

        leads_path = PROJECT / "opportunities" / "leads.json"
        leads = []
        if leads_path.exists():
            data = json.loads(leads_path.read_text(encoding="utf-8"))
            leads = data if isinstance(data, list) else data.get("leads", [])
        if not any(l.get("institution_slug") == slug for l in leads):
            leads.append(lead)
            leads_path.parent.mkdir(parents=True, exist_ok=True)
            leads_path.write_text(json.dumps(leads, indent=2), encoding="utf-8")

        entry = {"status": "opportunity", "tender_count": 0, "doc_count": 0, "lead_added": True}

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    last_scrape = {
        "institution": slug,
        "last_scrape": now,
        "next_scrape": now,
        "active_tenders_count": entry.get("tender_count", 0),
        "status": "success" if not entry.get("error") else "error",
        "error": entry.get("error"),
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")

    log_path = inst_dir / "scrape_log.json"
    log_data = {"runs": []}
    if log_path.exists():
        try:
            raw = json.loads(log_path.read_text(encoding="utf-8"))
            log_data["runs"] = raw.get("runs", raw) if isinstance(raw, dict) else raw
        except Exception:
            pass
    if not isinstance(log_data.get("runs"), list):
        log_data["runs"] = []
    short = slug_to_short(slug)
    log_data["runs"].append({
        "run_id": RUN_ID,
        "timestamp": now,
        "duration_seconds": 0,
        "status": "success" if not entry.get("error") else "error",
        "tenders_found": entry.get("tender_count", 0),
        "new_tenders": entry.get("tender_count", 0),
        "documents_downloaded": entry.get("doc_count", 0),
        "tender_ids": [f"{short}-{year}-001"] if entry.get("tender_count") else [],
        "errors": [entry["error"]] if entry.get("error") else [],
    })
    log_data["runs"] = log_data["runs"][-50:]
    log_path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

    return entry


def main():
    to_process = INSTITUTIONS
    for arg in sys.argv[1:]:
        if arg.startswith("--only="):
            only_slugs = set(arg.replace("--only=", "").split(","))
            to_process = [(s, u, n, h) for s, u, n, h in INSTITUTIONS if s in only_slugs]
            break
    for i, (slug, url, name, homepage) in enumerate(to_process):
        if i > 0:
            time.sleep(10)
        inst_dir = PROJECT / "institutions" / slug
        try:
            entry = process_institution(slug, url, name, homepage)
        except Exception as e:
            entry = {"status": "error", "tender_count": 0, "doc_count": 0, "error": str(e)}
            ensure_dirs(inst_dir)
            now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            (inst_dir / "last_scrape.json").write_text(json.dumps({
                "institution": slug,
                "last_scrape": now,
                "status": "error",
                "error": str(e),
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
                "status": "error",
                "errors": [str(e)],
            })
            log_path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

        status = "tenders" if entry.get("tender_count") else ("opportunity" if entry.get("lead_added") else "error")
        if entry.get("error"):
            status = "error"
        tc = entry.get("tender_count", 0)
        dc = entry.get("doc_count", 0)
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")

    leads_added = sum(1 for (slug, _, _, _) in INSTITUTIONS
                      if (PROJECT / "opportunities" / "leads.json").exists()
                      and slug in str((PROJECT / "opportunities" / "leads.json").read_text()))
    import subprocess
    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=PROJECT, check=False)


if __name__ == "__main__":
    main()
