#!/usr/bin/env python3
"""Scrape batch 48: iae through ids (25 institutions)."""

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import urllib.request
import urllib.error
import ssl

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = sys.argv[1] if len(sys.argv) > 1 else "run_20260313_205329_batch48"

# slug, tender_url, institution_name
INSTITUTIONS = [
    ("iae", "https://iae.ac.tz/", "TEWW | Mwanzo"),
    ("iamorganic", "https://iamorganic.co.tz/", "I am Organic"),
    ("ibes", "http://ibes.co.tz/", "IBES Tanzania"),
    ("ibmtelecenter", "https://ibmtelecenter.co.tz/", "IBMTELECENTER"),
    ("ibn-tv", "https://ibn-tv.co.tz/", "IBN TV"),
    ("ibunjazar", "https://ibunjazar.or.tz/", "Ibun Jazar"),
    ("icare", "https://icare.co.tz/", "iCare Technologies"),
    ("ice", "https://ice.co.tz/", "ICE Project Services Limited"),
    ("icealion", "https://icealion.co.tz/", "ICEA LION Group"),
    ("icedrop", "https://www.icedrop.co.tz/", "Ice Drop Tanzania"),
    ("icltz", "https://icltz.co.tz/", "ICL - Grobal Digital Marketing"),
    ("icomnet", "https://icomnet.co.tz/", "iCOMNET Technologies Ltd"),
    ("icot", "https://icot.ac.tz/", "ICoT"),
    ("icps", "https://icps.ac.tz/", "ICPS"),
    ("ict-pros", "https://ict-pros.co.tz/", "ICT-Pros"),
    ("ictpack", "https://ictpack.com/", "ICTPACK SOLUTIONS LTD"),
    ("idbwb", "https://idbwb.go.tz/", "IDBWB"),
    ("idcardsolutions", "https://idcardsolutions.co.tz/", "ID Card Solutions"),
    ("idea", "https://idea.co.tz/", "IDEA"),
    ("idealofficesupplies", "https://idealofficesupplies.co.tz/", "Ideal Office Supplies"),
    ("identity", "http://www.identitytz.com/", "Identity"),
    ("idev", "https://idev.co.tz/", "iDev Tanzania"),
    ("idodoe", "https://idodoe.co.tz/", "Idodoe"),
    ("idpress", "http://www.idpress.co.tz/", "ID Press Limited"),
    ("ids", "https://ids.co.tz/", "Information Development Service"),
]

TENDER_KEYWORDS = re.compile(
    r'\b(tender|tenders|procurement|rfp|rfq|rfi|eoi|bidding|zabuni|manunuzi|'
    r'expression of interest|invitation to bid|request for proposal|'
    r'quotation|prequalification|invitation to tender|tender announcement)\b',
    re.I
)

DOC_EXT = re.compile(r'\.(pdf|doc|docx|xls|xlsx|zip)(?:\?|$)', re.I)
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def extract_yaml_field(content: str, key: str) -> str | None:
    m = re.search(rf'^\s*{re.escape(key)}:\s*["\']?([^"\'\n]+)', content, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def fetch_url(url: str, timeout: int = 20, verify_ssl: bool = True) -> tuple[str | None, str | None]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TenderBot/1.0)"})
        kw = {"timeout": timeout}
        if not verify_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            kw["context"] = ctx
        with urllib.request.urlopen(req, **kw) as f:
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
    return has_tender_content(html) and (len(doc_links) > 0 or "request for proposal" in html.lower() or "rfp" in html.lower() or "tender announcement" in html.lower())


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


def process_institution(slug: str, tender_url: str, name: str) -> dict:
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    year = datetime.now().year

    html, err = fetch_url(tender_url)
    if err and "SSL" in str(err):
        html, err = fetch_url(tender_url, verify_ssl=False)
    if err:
        entry = {"status": "error", "tender_count": 0, "doc_count": 0, "error": err}
        doc_links = []
        tenders_found = False
    else:
        doc_links = extract_doc_links(html, tender_url)
        tenders_found = is_tender_listing(html, doc_links)
    short = slug_to_short(slug)
    tender_count = 0
    doc_count = 0

    if tenders_found:
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

        title = f"Tender/Procurement - {name}"
        tender_json = {
            "tender_id": tender_id,
            "institution": slug,
            "title": title,
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
            "website_url": tender_url.rstrip("/"),
            "emails": all_emails[:5],
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
        leads.append(lead)
        leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
        entry = {"status": "no_tenders", "tender_count": 0, "doc_count": 0, "lead_added": True}
    else:
        entry = {"status": "error", "tender_count": 0, "doc_count": 0, "error": err}

    last_scrape = {
        "institution": slug,
        "last_scrape": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "documents_downloaded": doc_count,
        "status": "success" if not entry.get("error") else "error",
        "error": entry.get("error"),
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")

    scrape_log_path = inst_dir / "scrape_log.json"
    log_entry = {
        "run_id": RUN_ID,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "success" if not entry.get("error") else "error",
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "tender_ids": [f"{short}-{year}-001"] if tender_count else [],
        "errors": [entry["error"]] if entry.get("error") else [],
    }
    if scrape_log_path.exists():
        data = json.loads(scrape_log_path.read_text(encoding="utf-8"))
        runs = data.get("runs", [])
    else:
        runs = []
    runs.append(log_entry)
    scrape_log_path.write_text(json.dumps({"runs": runs}, indent=2), encoding="utf-8")

    status = "tenders" if tender_count else ("error" if entry.get("error") else "no_tenders")
    print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
    return entry


def main():
    for slug, url, name in INSTITUTIONS:
        try:
            process_institution(slug, url, name)
        except Exception as e:
            inst_dir = PROJECT / "institutions" / slug
            ensure_dirs(inst_dir)
            (inst_dir / "last_scrape.json").write_text(json.dumps({
                "institution": slug,
                "last_scrape": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "run_id": RUN_ID,
                "active_tenders_count": 0,
                "documents_downloaded": 0,
                "status": "error",
                "error": str(e),
            }, indent=2), encoding="utf-8")
            scrape_log_path = inst_dir / "scrape_log.json"
            if scrape_log_path.exists():
                data = json.loads(scrape_log_path.read_text(encoding="utf-8"))
                runs = data.get("runs", [])
            else:
                runs = []
            runs.append({
                "run_id": RUN_ID,
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "status": "error",
                "tenders_found": 0,
                "documents_downloaded": 0,
                "tender_ids": [],
                "errors": [str(e)],
            })
            scrape_log_path.write_text(json.dumps({"runs": runs}, indent=2), encoding="utf-8")
            print(f"RESULT|{slug}|error|0|0")
        time.sleep(2)

    # Sync leads CSV
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(sync_script)], cwd=str(PROJECT), check=False)


if __name__ == "__main__":
    main()
