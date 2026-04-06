#!/usr/bin/env python3
"""
Batch scrape run_20260313_205329_batch33 - Process 25 institutions (eight through elm).
Creates last_scrape.json, scrape_log.json, and opportunity leads for no-tender sites.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch33"
NOW_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

INSTITUTIONS = [
    {"slug": "eight", "name": "Techy8 – IT Products and Services", "url": "https://www.techy8.com/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "eisttechnology", "name": "Eist Technology", "url": "https://eisttechnology.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ejcomputer", "name": "EJ Computer", "url": "https://ejcomputer.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ejsolution", "name": "EJ's Solutions", "url": "https://www.ejsolution.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elbaliz", "name": "Elbaliz Holdings Ltd", "url": "https://elbaliz.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elctnwd", "name": "NWDELCT", "url": "https://elctnwd.or.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "electricool", "name": "Electricool Tanzania Limited", "url": "https://electricool.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "electrocom", "name": "MP Electrocom", "url": "https://electrocom.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elegexlogistics", "name": "Elegex Logistics Limited", "url": "https://elegexlogistics.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elements", "name": "Elements Limited", "url": "https://elements.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elemielectrical", "name": "Elemi Electrical Company Limited", "url": "https://www.elemielectrical.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elevatedesignstudio", "name": "Elevate Design Studio", "url": "https://elevatedesignstudio.co.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Account suspended"},
    {"slug": "elijerrytc", "name": "Elijerry College of Health and Allied Sciences", "url": "https://elijerrytc.ac.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elimu", "name": "elimu community light", "url": "https://elimu.or.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Fetch timeout"},
    {"slug": "elimusaccos", "name": "ELIMU SACCOS LTD", "url": "https://elimusaccos.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elinkconsult", "name": "E-link Consult Limited", "url": "https://elinkconsult.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elique", "name": "Elique financial consultants", "url": "https://elique.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elite", "name": "Elite", "url": "https://elite.co.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Account suspended"},
    {"slug": "eliteagro", "name": "Elite Agro Cooperative Limited", "url": "https://eliteagro.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elitedental", "name": "Elite Dental Clinic", "url": "https://elitedental.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elitedigital", "name": "Elite Digital", "url": "https://elitedigital.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elitestore", "name": "Elite Bookstore", "url": "https://elitestore.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ellion", "name": "Ellion (T) Limited", "url": "https://ellion.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ellipsis", "name": "Ellipsis Digital", "url": "https://ellipsis.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "elm", "name": "ELM Microfinance", "url": "https://www.elm.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
]

EMAILS_BY_SLUG = {
    "eight": ["info@techy8.com"],
    "eisttechnology": ["info@eisttechnology.co.tz"],
    "ejcomputer": ["info@ejcomputer.co.tz"],
    "ejsolution": ["info@ejsolution.co.tz"],
    "elbaliz": ["liz@elbaliz.com"],
    "elctnwd": ["elct-nwd@hotmail.com"],
    "electricool": [],
    "electrocom": ["info@electrocom.co.tz"],
    "elegexlogistics": ["info@elegexlogistics.co.tz", "info@esoftech.co.tz"],
    "elements": ["info@elements.co.tz"],
    "elemielectrical": ["elemicompany19@gmail.com", "info@elemielectrical.co.tz"],
    "elevatedesignstudio": ["webmaster@elevatedesignstudio.co.tz"],
    "elijerrytc": ["info@elijerrytc.ac.tz"],
    "elimu": [],
    "elimusaccos": ["info@elimusaccos.co.tz"],
    "elinkconsult": ["info@elinkconsult.co.tz"],
    "elique": ["info@elique.co.tz", "enkumbi@elique.co.tz"],
    "elite": ["webmaster@elite.co.tz"],
    "eliteagro": ["info@eliteagro.co.tz"],
    "elitedental": ["info.eliteclinic@gmail.com"],
    "elitedigital": [],
    "elitestore": ["info@elitestore.co.tz"],
    "ellion": ["info@ellion.co.tz"],
    "ellipsis": ["jobs@ellipsis.co.tz"],
    "elm": ["info@elm.co.tz"],
}


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def write_last_scrape(inst_dir: Path, inst: dict):
    last = {
        "run_id": RUN_ID,
        "scraped_at": NOW_ISO,
        "status": inst["status"],
        "tender_count": inst["tenders"],
        "doc_count": inst["docs"],
        "error": inst.get("error"),
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(last, f, indent=2)


def append_scrape_log(inst_dir: Path, inst: dict):
    log_file = inst_dir / "scrape_log.json"
    entries = []
    if log_file.exists():
        with open(log_file) as f:
            data = json.load(f)
            entries = data if isinstance(data, list) else data.get("runs", [])
    entries.append({
        "run_id": RUN_ID,
        "scraped_at": NOW_ISO,
        "status": inst["status"],
        "tender_count": inst["tenders"],
        "doc_count": inst["docs"],
        "error": inst.get("error"),
    })
    with open(log_file, "w") as f:
        json.dump(entries[-100:], f, indent=2)


def append_leads(insts_no_tenders: list):
    leads_file = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_file.exists():
        with open(leads_file) as f:
            leads = json.load(f)
    existing_slugs = {l.get("institution_slug") for l in leads}

    for inst in insts_no_tenders:
        if inst["slug"] in existing_slugs:
            continue
        emails = EMAILS_BY_SLUG.get(inst["slug"], [])

        lead = {
            "institution_slug": inst["slug"],
            "institution_name": inst["name"],
            "website_url": inst["url"],
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {inst['name']} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
            "draft_email_body": f"Dear {inst['name']} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {inst['name']}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": NOW_ISO,
            "status": "pending",
        }
        leads.append(lead)

    with open(leads_file, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


def main():
    no_tender_insts = []
    for inst in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / inst["slug"]
        ensure_dirs(inst_dir)
        write_last_scrape(inst_dir, inst)
        append_scrape_log(inst_dir, inst)

        if inst["status"] in ("no_tenders", "error"):
            no_tender_insts.append(inst)

    append_leads(no_tender_insts)

    for inst in INSTITUTIONS:
        status = inst["status"]
        if status == "no_tenders":
            status = "opportunity"
        print(f"RESULT|{inst['slug']}|{status}|{inst['tenders']}|{inst['docs']}")


if __name__ == "__main__":
    main()
