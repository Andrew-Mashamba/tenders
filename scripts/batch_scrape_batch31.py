#!/usr/bin/env python3
"""
Batch scrape run_20260313_205329_batch31 - Process 25 institutions.
Creates last_scrape.json, scrape_log.json, tenders, downloads, and opportunity leads.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch31"
NOW_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

INSTITUTIONS = [
    {"slug": "duxte", "name": "Duxte", "url": "https://duxte.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "dws", "name": "DELTA WEB SERVICE", "url": "https://www.dws.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "dxe", "name": "DXE Associates", "url": "https://dxe.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "dynamicexperience", "name": "Dynamic Experience", "url": "https://dynamicexperience.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "dynatech", "name": "Dynatech Solutions", "url": "https://dynatech.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "dynatech-africa", "name": "Dynatech Africa", "url": "https://dynatech-africa.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "e-com", "name": "e-com", "url": "https://e-com.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "e-mazao", "name": "E-MAZAO", "url": "https://www.e-mazao.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "e1", "name": "E1 Limited", "url": "https://e1.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "eabrothers", "name": "EA Brothers Contractors", "url": "https://eabrothers.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "eaglesconsultants", "name": "Eagles Consultants", "url": "https://www.eaglesconsultants.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "eajess", "name": "eajess.ac.tz", "url": "https://eajess.ac.tz/tenders?i=1", "tenders": 0, "docs": 0, "status": "error", "error": "Site requires JavaScript"},
    {"slug": "eas", "name": "Epinav Agricultural Solutions", "url": "https://www.eas.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "easternarc", "name": "Eastern Arc Mountains Conservation Fund", "url": "https://easternarc.or.tz/", "tenders": 1, "docs": 0, "status": "success", "error": None},
    {"slug": "eastwoodsattorneys", "name": "Eastwoods Attorneys", "url": "https://eastwoodsattorneys.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "easylawyer", "name": "A Billion Startups", "url": "https://abillionstartups.com/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "easytech", "name": "EasyTech Company Limited", "url": "https://easytech.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "easytravel", "name": "Easy Travel", "url": "https://www.easytravel.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "eba", "name": "Executive Business Attorneys", "url": "https://eba.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ebiz", "name": "E-BIZ SOLUTIONS LTD", "url": "https://ebiz.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ebmaritime", "name": "EB Maritime Group", "url": "https://ebmaritime.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ecaconsultants", "name": "ECA Consultants", "url": "https://ecaconsultants.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ecam", "name": "East Coast Africa Music", "url": "https://ecam.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ecantz", "name": "ECAN(T)", "url": "https://ecantz.or.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "echat", "name": "Echat Limited", "url": "http://echat.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
]

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
            entries = json.load(f)
    entries.append({
        "run_id": RUN_ID,
        "scraped_at": NOW_ISO,
        "status": inst["status"],
        "tender_count": inst["tenders"],
        "doc_count": inst["docs"],
        "error": inst.get("error"),
    })
    with open(log_file, "w") as f:
        json.dump(entries[-100:], f, indent=2)  # Keep last 100

def create_easternarc_tender(inst_dir: Path):
    tender_id = "EASTERNARC-2026-001"
    tender = {
        "tender_id": tender_id,
        "title": "Invitation for Bids: Sale of EAMCEF Used Motor Vehicles",
        "description": "EAMCEF intends to sale by competitive tender its 5 units of USED Toyota Land Cruisers. Interested bidders can inspect vehicles during bidding period.",
        "published_date": "2025-06-23",
        "closing_date": "2025-07-24",
        "category": "Asset Sale",
        "document_links": [],
        "contact_info": {"email": "eamcef@easternarc.or.tz", "phone": "+255 755 330 558"},
        "source_url": "https://easternarc.or.tz/invitation-for-bids-sale-of-eamcef-used-motor-vehicles/",
        "scraped_at": NOW_ISO,
    }
    ensure_dirs(inst_dir)
    with open(inst_dir / "tenders" / "active" / f"{tender_id}.json", "w") as f:
        json.dump(tender, f, indent=2)

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
        emails = []
        if inst["slug"] == "dws":
            emails = ["info@dws.co.tz"]
        elif inst["slug"] == "e-com":
            emails = ["info@e-com.co.tz"]
        elif inst["slug"] == "e-mazao":
            emails = ["info@andreross.co.tz"]
        elif inst["slug"] == "e1":
            emails = ["info@e1.co.tz"]
        elif inst["slug"] == "eabrothers":
            emails = ["info@eabrothers.co.tz"]
        elif inst["slug"] == "eaglesconsultants":
            emails = ["info@eaglesconsultants.co.tz"]
        elif inst["slug"] == "eas":
            emails = ["info@eas.co.tz"]
        elif inst["slug"] == "eastwoodsattorneys":
            emails = ["info@eastwoodsattorneys.co.tz"]
        elif inst["slug"] == "easylawyer":
            emails = ["admin@abillionstartups.com"]
        elif inst["slug"] == "eba":
            emails = ["info@eba.co.tz"]
        elif inst["slug"] == "ebmaritime":
            emails = ["info@ebmaritime.co.tz"]
        elif inst["slug"] == "ecaconsultants":
            emails = ["info@ecaconsultants.co.tz"]
        elif inst["slug"] == "ecantz":
            emails = ["info@ecantz.or.tz"]
        elif inst["slug"] == "echat":
            emails = ["info@echat.co.tz", "hello@purityiv.com"]
        elif inst["slug"] == "dynatech":
            emails = ["info@dynatech.co.tz"]
        elif inst["slug"] == "dynatech-africa":
            emails = ["sales@dynatech-africa.co.tz"]
        elif inst["slug"] == "duxte":
            emails = []
        elif inst["slug"] == "dxe":
            emails = []
        elif inst["slug"] == "dynamicexperience":
            emails = []
        elif inst["slug"] == "easytravel":
            emails = ["info@easytravel.co.tz"]
        elif inst["slug"] == "ebiz":
            emails = []
        elif inst["slug"] == "ecam":
            emails = []

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

        if inst["slug"] == "easternarc":
            create_easternarc_tender(inst_dir)

        if inst["status"] == "no_tenders":
            no_tender_insts.append(inst)

    append_leads(no_tender_insts)

    for inst in INSTITUTIONS:
        status = inst["status"]
        if status == "no_tenders":
            status = "opportunity"
        print(f"RESULT|{inst['slug']}|{status}|{inst['tenders']}|{inst['docs']}")

if __name__ == "__main__":
    main()
