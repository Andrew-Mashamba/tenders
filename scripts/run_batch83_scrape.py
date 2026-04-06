#!/usr/bin/env python3
"""Process batch83 scrape results for 25 institutions."""
import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch83"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Scrape results: slug -> (status, tender_count, doc_count, tenders_data, emails, opportunity_info)
RESULTS = {
    "ngare-sero-lodge": ("no_tenders", 0, 0, [], ["reservations@ngaresero.com"], "Lodge/tourism - digital systems for reservations"),
    "ngilisho": ("no_tenders", 0, 0, [], ["info@ngilisho.co.tz"], "Electrical contractor - ICT/automation"),
    "ngogoengineering": ("no_tenders", 0, 0, [], ["info@ngogoenginearing.co.tz"], "Engineering - software/ICT systems"),
    "ngomesaccos": ("no_tenders", 0, 0, [], ["info@ngomesaccos.co.tz", "poncekihaga@gmail.com"], "SACCO - management systems"),
    "ngoteyawild": ("error", 0, 0, [], [], "Site timeout"),
    "ngsinvestments": ("no_tenders", 0, 0, [], ["info@ngsinvestments.co.tz"], "Investment/logistics - digital systems"),
    "nhbra": ("error", 0, 0, [], ["dg@nhbra.go.tz", "dawatilamsaada@nhbra.go.tz"], "Site timeout"),
    "nhc": ("no_tenders", 0, 0, [], [], "Housing corp - no tender page on homepage"),
    "nhlqatc": ("no_tenders", 0, 0, [], [], "Tourism - African Rhino Adventure"),
    "nibplan": ("no_tenders", 0, 0, [], ["info@nibplan.co.tz"], "Engineering consultancy"),
    "nicecatering": ("no_tenders", 0, 0, [], [], "Catering - no emails on main page"),
    "nictanzania": ("no_tenders", 0, 0, [], ["rector@waterinstitute.ac.tz"], "Water Institute - training"),
    "nictbb": ("error", 0, 0, [], ["sales@nictbb.co.tz"], "404 - tenders.php not found"),
    "nida": ("no_tenders", 0, 0, [], ["info@nida.go.tz"], "NIDA - application forms not tenders"),
    "nidc": ("error", 0, 0, [], ["commercial@nidc.co.tz"], "Site timeout"),
    "nilefishnetmotors": ("error", 0, 0, [], ["info@nilefishnetmotors.co.tz"], "Site timeout"),
    "nimeta": ("no_tenders", 0, 0, [], ["nimeta@nimetaconsult.co.tz", "inquiry@nimetaconsult.co.tz"], "Engineering consultancy"),
    "nimetaconsult": ("no_tenders", 0, 0, [], ["nimeta@nimetaconsult.co.tz", "inquiry@nimetaconsult.co.tz"], "Engineering consultancy"),
    "nirc": ("tenders", 2, 2, [
        {"title": "EOI Buigiri, Ikowa, Dabalo and Hombolo Dams and Associated Flood Control Works", "date": "2025-12-22",
         "url": "https://nirc.go.tz/uploads/documents/sw-1765963698-EOI%20Buigiri,%20Ikowa,%20Dabalo%20and%20Hombolo%20Dams%20and%20Associated%20Flood-Control%20Works.pdf"},
        {"title": "EOI Kidete and Kimagai Dams and Associated Flood Control Works", "date": "2025-12-22",
         "url": "https://nirc.go.tz/uploads/documents/sw-1765963776-EOI%20Kidete%20and%20Kimagai%20Dams%20and%20Associated%20Flood-Control%20Works.pdf"}
    ], [], None),
    "nishati": ("error", 0, 0, [], ["ps@nishati.go.tz"], "Site timeout - nest.go.tz"),
    "nissi": ("no_tenders", 0, 0, [], ["contact@nissi.co.tz"], "Stationery supplier"),
    "nit": ("no_tenders", 0, 0, [], ["rector@nit.ac.tz"], "NIT - training announcements not procurement"),
    "nivea": ("no_tenders", 0, 0, [], [], "Skincare brand - Kenya"),
    "nivexassurance": ("no_tenders", 0, 0, [], ["info@nivex.co.tz"], "Audit/accounting firm"),
    "nje": ("no_tenders", 0, 0, [], ["dodoma@nje.go.tz", "nje@nje.go.tz"], "Ministry of Foreign Affairs"),
}

INST_NAMES = {
    "ngare-sero-lodge": "Ngare Sero Mountain Lodge",
    "ngilisho": "Ngilisho Electrical Contractors",
    "ngogoengineering": "Ngogo Engineering",
    "ngomesaccos": "NGOME SACCOS LTD",
    "ngoteyawild": "Ngoteya Wild",
    "ngsinvestments": "NGS Group of Companies",
    "nhbra": "NHBRA",
    "nhc": "National Housing Corporation",
    "nhlqatc": "African Rhino Adventure",
    "nibplan": "NIB Plan Consult",
    "nicecatering": "Nice Catering",
    "nictanzania": "Water Institute Tanzania",
    "nictbb": "NICTBB",
    "nida": "NIDA",
    "nidc": "NIDC",
    "nilefishnetmotors": "Nile Fishnet Motors",
    "nimeta": "NIMETA Consult",
    "nimetaconsult": "NIMETA Consult",
    "nirc": "National Irrigation Commission",
    "nishati": "Nishati (Energy Ministry)",
    "nissi": "Nissi GmbH",
    "nit": "National Institute of Transport",
    "nivea": "NIVEA",
    "nivexassurance": "Nivex Assurance",
    "nje": "Ministry of Foreign Affairs",
}

WEBSITE_URLS = {
    "ngare-sero-lodge": "https://ngare-sero-lodge.co.tz/",
    "ngilisho": "https://ngilisho.co.tz/",
    "ngogoengineering": "https://ngogoengineering.co.tz/",
    "ngomesaccos": "https://ngomesaccos.co.tz/tender_vacancies",
    "ngoteyawild": "https://ngoteyawild.co.tz/",
    "ngsinvestments": "https://ngsinvestments.co.tz/",
    "nhbra": "https://nhbra.go.tz/",
    "nhc": "https://nhc.co.tz/",
    "nhlqatc": "https://africanrhinoadventure.com/",
    "nibplan": "https://nibplan.co.tz/",
    "nicecatering": "https://www.nicecatering.co.tz/",
    "nictanzania": "https://nictanzania.co.tz/",
    "nictbb": "http://nictbb.co.tz/tenders.php",
    "nida": "https://nida.go.tz/",
    "nidc": "https://nidc.co.tz/tenders",
    "nilefishnetmotors": "https://nilefishnetmotors.co.tz/",
    "nimeta": "https://nimetaconsult.co.tz/",
    "nimetaconsult": "https://nimetaconsult.co.tz/",
    "nirc": "https://nirc.go.tz/documents/tenders",
    "nishati": "https://nest.go.tz/tenders/published-tenders",
    "nissi": "https://nissi.co.tz/",
    "nit": "https://nit.ac.tz/",
    "nivea": "https://www.nivea.co.ke/",
    "nivexassurance": "https://www.nivexassurance.co.tz/",
    "nje": "https://www.foreign.go.tz/",
}


def download_file(url: str, dest: Path) -> bool:
    try:
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "TENDERS-Scraper/1.0"})
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.read())
            return True
    except Exception as e:
        print(f"  Download error {url}: {e}")
        return False


def extract_text_pdf(pdf_path: Path) -> str:
    try:
        result = subprocess.run(
            ["python3", "-m", "tools", "pdf", "read", str(pdf_path)],
            cwd=PROJECT, capture_output=True, text=True, timeout=30
        )
        return result.stdout if result.returncode == 0 else ""
    except Exception:
        return ""


def process_nirc_tenders():
    """Create NIRC tender JSONs and download documents."""
    inst_dir = PROJECT / "institutions" / "nirc"
    tenders_dir = inst_dir / "tenders" / "active"
    tenders_dir.mkdir(parents=True, exist_ok=True)

    docs_downloaded = 0
    for i, t in enumerate(RESULTS["nirc"][3], 1):
        tender_id = f"NIRC-2026-{i:03d}"
        download_dir = inst_dir / "downloads" / tender_id / "original"
        extract_dir = inst_dir / "downloads" / tender_id / "extracted"
        download_dir.mkdir(parents=True, exist_ok=True)
        extract_dir.mkdir(parents=True, exist_ok=True)

        filename = t["url"].split("/")[-1]
        filename = urllib.parse.unquote(filename)
        dest = download_dir / filename
        if download_file(t["url"], dest):
            docs_downloaded += 1
            if filename.lower().endswith(".pdf"):
                txt = extract_text_pdf(dest)
                if txt:
                    (extract_dir / (Path(filename).stem + ".txt")).write_text(txt, encoding="utf-8")

        tender_json = {
            "tender_id": tender_id,
            "institution": "nirc",
            "title": t["title"],
            "description": f"EOI for dams and flood control works - {t['title']}",
            "published_date": t["date"],
            "closing_date": None,
            "category": "Construction",
            "status": "active",
            "source_url": "https://nirc.go.tz/documents/tenders",
            "documents": [{"filename": filename, "original_url": t["url"], "local_path": f"./downloads/{tender_id}/original/{filename}"}],
            "contact": {"email": "info@nirc.go.tz", "phone": "+255 22 2127314"},
            "scraped_at": NOW,
            "last_checked": NOW,
        }
        (tenders_dir / f"{tender_id}.json").write_text(json.dumps(tender_json, indent=2), encoding="utf-8")

    return docs_downloaded


def update_institution_state(slug: str, status: str, tender_count: int, doc_count: int, error_msg: str = None):
    inst_dir = PROJECT / "institutions" / slug
    inst_dir.mkdir(parents=True, exist_ok=True)

    last_scrape = {
        "institution": slug,
        "last_scrape": NOW,
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error_msg,
        "documents_downloaded": doc_count,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")

    scrape_log_path = inst_dir / "scrape_log.json"
    log_entry = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error_msg] if error_msg else [],
    }
    if scrape_log_path.exists():
        log = json.loads(scrape_log_path.read_text(encoding="utf-8"))
        runs = log if isinstance(log, list) else log.get("runs", [])
    else:
        runs = []
    runs.append(log_entry)
    scrape_log_path.write_text(json.dumps({"runs": runs[-50:]}, indent=2), encoding="utf-8")


def append_leads(leads_to_add: list):
    leads_path = PROJECT / "opportunities" / "leads.json"
    if leads_path.exists():
        data = json.loads(leads_path.read_text(encoding="utf-8"))
        leads = data if isinstance(data, list) else data.get("leads", [])
    else:
        leads = []
    leads.extend(leads_to_add)
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    summaries = []
    nirc_docs = 0

    if RESULTS["nirc"][0] == "tenders":
        nirc_docs = process_nirc_tenders()
        update_institution_state("nirc", "success", 2, nirc_docs)
        summaries.append(f"RESULT|nirc|success|2|{nirc_docs}")

    leads_to_add = []
    for slug, (status, tender_count, doc_count, tenders_data, emails, opp_info) in RESULTS.items():
        if slug == "nirc":
            continue
        if status == "error":
            update_institution_state(slug, "error", 0, 0, opp_info)
            summaries.append(f"RESULT|{slug}|error|0|0")
        else:
            update_institution_state(slug, "no_tenders", 0, 0)
            summaries.append(f"RESULT|{slug}|no_tenders|0|0")

        if status in ("no_tenders", "error"):
            emails_clean = [e for e in (emails or []) if e and "@" in str(e) and not str(e).endswith(".jpg") and not str(e).endswith(".js")]
            lead = {
                "institution_slug": slug,
                "institution_name": INST_NAMES.get(slug, slug),
                "website_url": WEBSITE_URLS.get(slug, ""),
                "emails": emails_clean[:5],
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found. {opp_info}. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {INST_NAMES.get(slug, slug)}",
                "draft_email_body": f"Dear {INST_NAMES.get(slug, slug)} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {INST_NAMES.get(slug, slug)}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
                "created_at": NOW,
                "status": "pending",
            }
            leads_to_add.append(lead)

    if leads_to_add:
        append_leads(leads_to_add)
        subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=PROJECT, check=True)

    for s in sorted(summaries):
        print(s)


if __name__ == "__main__":
    main()
