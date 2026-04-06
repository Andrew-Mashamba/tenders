#!/usr/bin/env python3
"""
Scrape batch 8 institutions: ancassociates through apsp.
Process tenders or create leads for no-tender sites.
"""
import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch8"

INSTITUTIONS = [
    ("ancassociates", "ANC Associates", "https://ancassociates.co.tz/"),
    ("ando", "Ando Roofing", "https://ando.co.tz/"),
    ("andreross", "ANDRE & ROSS", "https://www.andreross.co.tz/"),
    ("angazatechnology", "Angaza Technology", "https://angazatechnology.co.tz/"),
    ("angkol", "Angkol Creatives", "https://angkol.co.tz/"),
    ("anjitafoundation", "Anjita Foundation", "https://anjitafoundation.or.tz/"),
    ("anovaconsult", "Anova Consult", "https://anovaconsult.co.tz/"),
    ("anovelidea", "A Novel Idea", "https://anovelidea.co.tz/"),
    ("ansaf", "ANSAF", "https://ansaf.or.tz/tender/"),
    ("antelopesafaris", "Antelope Safaris", "https://antelopesafaris.com/"),
    ("antivirus", "Antivirus Tanzania", "https://antivirus.co.tz/"),
    ("antojam", "ANTOJAM", "https://antojam.co.tz/"),
    ("anytechcomputers", "AnyTech Computers", "https://anytechcomputers.co.tz/"),
    ("apchotelandconferencecentre", "APC Hotel", "https://apchotelandconferencecentre.co.tz/"),
    ("apex", "Apex Attorneys", "http://apex.co.tz/"),
    ("apexauditors", "APEX Auditors", "https://apexauditors.co.tz/"),
    ("apexeng", "Apex Engineering", "https://apexeng.co.tz/"),
    ("apexqs", "Apex Quantity Surveyors", "https://apexqs.co.tz/"),
    ("apm", "APM Construction", "https://apm.co.tz/"),
    ("apollomedicalcentre", "Apollo Medical Centre", "https://apollomedicalcentre.co.tz/"),
    ("applefreight", "Apple Freight", "https://applefreight.co.tz/"),
    ("applemacbooks", "AppleMacbooks", "https://www.applemacbooks.co.tz/"),
    ("appleprint", "The Appleprint", "https://appleprint.co.tz/"),
    ("apsis", "Apsis", "https://apsis.co.tz/"),
    ("apsp", "APSP", "https://apsp.or.tz/"),
]

# ANSAF has tender documents on its tender page
ANSAF_TENDERS = [
    {
        "tender_id": "ANSAF-2026-001",
        "title": "2023 TENDER - Extension Study",
        "document_links": ["https://ansaf.or.tz/wp-content/uploads/2023/07/FINAL-REPORT-EXTENSION-STUDY-30.7.17-SL.pdf"],
        "published_date": "2023-07-30",
        "closing_date": None,
    },
    {
        "tender_id": "ANSAF-2026-002",
        "title": "2023-2024 consultancy tenders - Cooperatives Analysis",
        "document_links": ["https://ansaf.or.tz/wp-content/uploads/2023/07/ANSAF-Analysis-on-Cooperatives-Final-Report.pdf"],
        "published_date": "2023-07-01",
        "closing_date": None,
    },
]

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TENDERS-Scraper/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return True
    except Exception as e:
        print(f"  Download failed {url}: {e}")
        return False


def extract_text_pdf(path: Path) -> str:
    try:
        result = subprocess.run(
            ["python3", "-m", "tools", "pdf", "read", str(path)],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout or ""
    except Exception:
        return ""


def extract_emails_from_text(text: str) -> list:
    emails = set(EMAIL_PATTERN.findall(text))
    return sorted([e for e in emails if not e.endswith((".png", ".jpg", ".gif"))])


def process_ansaf_tenders():
    """Process ANSAF - has 2 tender documents."""
    inst_dir = PROJECT / "institutions" / "ansaf"
    ensure_dirs(inst_dir)
    doc_count = 0

    for t in ANSAF_TENDERS:
        tender_id = t["tender_id"]
        tender_json = {
            "tender_id": tender_id,
            "title": t["title"],
            "description": "",
            "published_date": t["published_date"],
            "closing_date": t["closing_date"],
            "category": "consultancy",
            "document_links": t["document_links"],
            "contact_info": {"email": "info@ansaf.or.tz", "phone": "0717403032"},
            "source_url": "https://ansaf.or.tz/tender/",
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }
        (inst_dir / "tenders" / "active" / f"{tender_id}.json").write_text(
            json.dumps(tender_json, indent=2), encoding="utf-8"
        )

        download_dir = inst_dir / "downloads" / tender_id
        (download_dir / "original").mkdir(parents=True, exist_ok=True)
        (download_dir / "extracted").mkdir(parents=True, exist_ok=True)

        for url in t["document_links"]:
            fname = url.split("/")[-1].split("?")[0] or "document.pdf"
            dest = download_dir / "original" / fname
            if download_file(url, dest):
                doc_count += 1
                txt_path = download_dir / "extracted" / (Path(fname).stem + ".txt")
                txt_content = extract_text_pdf(dest)
                if txt_content:
                    txt_path.write_text(txt_content, encoding="utf-8")

    return len(ANSAF_TENDERS), doc_count


def create_lead(slug: str, name: str, url: str, emails: list, category: str = "sell") -> dict:
    inst_name = name
    return {
        "institution_slug": slug,
        "institution_name": inst_name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": category,
        "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
        "draft_email_body": f"""Dear {inst_name} Team,

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
""",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    }


def get_contact_emails(slug: str, name: str, url: str) -> list:
    """Get emails from README contact section."""
    readme = PROJECT / "institutions" / slug / "README.md"
    emails = []
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        for m in EMAIL_PATTERN.finditer(text):
            e = m.group(0)
            if e and not e.endswith((".png", ".jpg")):
                emails.append(e)
    # Add known contacts from READMEs
    known = {
        "ancassociates": ["info@ancassociates.co.tz"],
        "ando": ["sales@ando.co.tz"],
        "andreross": ["info@andreross.co.tz", "collin@andreross.co.tz"],
        "angazatechnology": ["info@angazatechnology.co.tz"],
        "angkol": ["leslie@angkol.co.tz"],
        "anjitafoundation": [],
        "anovaconsult": ["info@anovaconsult.co.tz"],
        "anovelidea": ["info@anovelidea.co.tz"],
        "antelopesafaris": [],
        "antivirus": [],
        "antojam": ["info@antojam.co.tz"],
        "anytechcomputers": ["md@anytechcomputers.co.tz", "info@anytechcomputers.co.tz"],
        "apchotelandconferencecentre": ["reservations@apchotelandconferencecentre.co.tz", "info@apchotelandconferencecentre.co.tz"],
        "apex": ["bricks@gmail.com", "aaa@apex.co.tz"],
        "apexauditors": ["info@apexauditors.co.tz"],
        "apexeng": [],
        "apexqs": ["Info@apexqs.co.tz", "info@apexqs.co.tz"],
        "apm": ["apmconstructionmasters@gmail.com"],
        "apollomedicalcentre": ["hr@apollomedicalcentre.co.tz", "apollo@apollomedicalcentre.co.tz"],
        "applefreight": ["info@applefreight.co.tz"],
        "applemacbooks": ["info@applemacbooks.co.tz"],
        "appleprint": ["appleprint.ars@gmail.com", "marketing@appleprint.co.tz"],
        "apsis": ["info@apsis.co.tz"],
        "apsp": ["info@apsp.or.tz"],
    }
    if slug in known and known[slug]:
        for e in known[slug]:
            if e not in emails:
                emails.append(e)
    return list(dict.fromkeys(emails))


def update_last_scrape(inst_dir: Path, status: str, tender_count: int, doc_count: int, error: str = None):
    data = {
        "run_id": RUN_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "tender_count": tender_count,
        "doc_count": doc_count,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def append_scrape_log(inst_dir: Path, status: str, tender_count: int, doc_count: int, error: str = None):
    log_file = inst_dir / "scrape_log.json"
    entry = {
        "run_id": RUN_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "tender_count": tender_count,
        "doc_count": doc_count,
        "error": error,
    }
    logs = []
    if log_file.exists():
        try:
            logs = json.loads(log_file.read_text(encoding="utf-8"))
            if not isinstance(logs, list):
                logs = []
        except Exception:
            logs = []
    logs.append(entry)
    log_file.write_text(json.dumps(logs[-100:], indent=2), encoding="utf-8")


def main():
    results = []
    new_leads = []

    # 1. Process ANSAF (has tenders)
    print("Processing ansaf (tenders found)...")
    try:
        tc, dc = process_ansaf_tenders()
        inst_dir = PROJECT / "institutions" / "ansaf"
        update_last_scrape(inst_dir, "ok", tc, dc)
        append_scrape_log(inst_dir, "ok", tc, dc)
        results.append(("ansaf", "ok", tc, dc))
        print(f"  RESULT|ansaf|ok|{tc}|{dc}")
    except Exception as e:
        inst_dir = PROJECT / "institutions" / "ansaf"
        update_last_scrape(inst_dir, "error", 0, 0, str(e))
        append_scrape_log(inst_dir, "error", 0, 0, str(e))
        results.append(("ansaf", "error", 0, 0))
        print(f"  RESULT|ansaf|error|0|0  # {e}")

    # 2. Process all other institutions (no tenders -> leads)
    for slug, name, url in INSTITUTIONS:
        if slug == "ansaf":
            continue
        inst_dir = PROJECT / "institutions" / slug
        ensure_dirs(inst_dir)
        try:
            emails = get_contact_emails(slug, name, url)
            lead = create_lead(slug, name, url, emails)
            new_leads.append(lead)
            update_last_scrape(inst_dir, "no_tenders", 0, 0)
            append_scrape_log(inst_dir, "no_tenders", 0, 0)
            results.append((slug, "no_tenders", 0, 0))
            print(f"  RESULT|{slug}|no_tenders|0|0")
        except Exception as e:
            update_last_scrape(inst_dir, "error", 0, 0, str(e))
            append_scrape_log(inst_dir, "error", 0, 0, str(e))
            results.append((slug, "error", 0, 0))
            print(f"  RESULT|{slug}|error|0|0  # {e}")

    # 3. Append new leads to leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    existing = []
    if leads_path.exists():
        try:
            data = json.loads(leads_path.read_text(encoding="utf-8"))
            existing = data if isinstance(data, list) else data.get("leads", [])
        except Exception:
            existing = []
    existing_slugs = {l.get("institution_slug") for l in existing}
    for lead in new_leads:
        if lead["institution_slug"] not in existing_slugs:
            existing.append(lead)
            existing_slugs.add(lead["institution_slug"])
    leads_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Run sync_leads_csv.py
    subprocess.run(
        ["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=PROJECT,
        check=True,
    )

    # 5. Print final summary
    print("\n--- FINAL RESULTS ---")
    for slug, status, tc, dc in results:
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")


if __name__ == "__main__":
    main()
