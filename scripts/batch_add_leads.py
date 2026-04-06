#!/usr/bin/env python3
"""Append opportunity leads for institutions with no tenders found."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"
INST = PROJECT / "institutions"

DRAFT_BODY = """Dear {institution_name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {institution_name}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
"""

INSTITUTIONS = [
    ("ghems", "Ghems African Traders Ltd", "https://ghems.co.tz/", ["info@ghems.co.tz"]),
    ("gie", "Genuine Luxury Travel Company", "https://gie.co.tz/", ["info@gie.co.tz"]),
    ("gigatec", "Gigatec", "https://gigatec.co.tz/", []),
    ("gimena", "Gimena Enterprises", "https://gimena.co.tz/", []),
    ("giovanni", "Giovanni", "https://giovanni.co.tz/", []),
    ("gisengineering", "GIS Engineering", "https://www.gisengineering.co.tz/", ["info@gisengineering.co.tz"]),
    ("gjb", "GJB Group", "https://gjb.co.tz/", ["info@gjb.co.tz"]),
    ("glasswin", "Glasswin Limited", "https://www.glasswin.co.tz/", ["glasswintz@gmail.com"]),
    ("glintacon", "Glintacon", "https://glintacon.co.tz/", ["info@glintacon.co.tz", "ceo@glintacon.co.tz"]),
    ("globalpackaging", "Global Packaging (T) Ltd", "https://globalpackaging.co.tz/", ["info@globalpackaging.co.tz"]),
    ("globalpublishers", "Global Publishers", "https://globalpublishers.co.tz/", []),
    ("globaltech", "GLOBAL TECH", "https://globaltech.co.tz/", ["info@globaltech.co.tz"]),
    ("globe", "Globe Accountancy", "https://www.globe.co.tz/", ["mmm@globe.co.tz"]),
    ("globetrotters", "Globe Trotters", "https://www.globetrotters.co.tz/", ["info@globetrotters.co.tz"]),
    ("gncsolutions", "GNC Solutions", "https://gncsolutions.co.tz/", ["info@gncsolutions.co.tz"]),
    ("go-vacation", "GOVACATION AFRICA", "https://www.go-vacation.co.za/", ["sblehle@go-vacation.co.za", "sbullerdiek@go-vacation.co.za"]),
    ("gochconsult", "GOCH Consult", "https://gochconsult.co.tz/", ["info@gochconsult.co.tz"]),
    ("godwinattorneys", "Godwin Attorneys", "https://godwinattorneys.co.tz/", ["info@godwinattorneys.co.tz"]),
    ("gofinventures", "Gofin Ventures Ltd", "https://www.gofinventure.com/", []),
    ("gogam", "Gogam Construction", "https://gogam.co.tz/", ["info@gogam.co.tz"]),
    ("goldeneagletravel", "Golden Eagle", "https://goldeneagletravel.co.tz/", ["info@goldeneagletravel.co.tz"]),
    ("goldenpot", "Goldenpot", "https://goldenpot.co.tz/", ["info@goldenpot.co.tz"]),
    ("goldstarpaints", "Goldstar Paints", "https://goldstarpaints.co.tz/", ["info@goldstarpaints.co.tz"]),
    ("goldzone", "Gold Zone Contractor", "https://goldzone.co.tz/", ["goldzonetz48@gmail.com"]),
    ("gonuts", "Go Nuts 4 Donuts", "https://gonuts.co.tz/", ["info@gonuts4donuts.co.tz"]),
]

def main():
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}
    added = 0
    for slug, name, url, emails in INSTITUTIONS:
        if slug in existing_slugs:
            continue
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(institution_name=name),
            "created_at": now,
            "status": "pending",
        }
        leads.append(lead)
        existing_slugs.add(slug)
        added += 1

    with open(LEADS_JSON, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    # Update last_scrape.json and scrape_log.json for each institution
    run_id = "run_20260313_205329_batch42"
    for slug, name, url, _ in INSTITUTIONS:
        inst_dir = INST / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "run_id": run_id,
            "timestamp": now,
            "status": "no_tenders",
            "tender_count": 0,
            "doc_count": 0,
            "error": None,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log_path = inst_dir / "scrape_log.json"
        log_entries = []
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_entries = json.load(f)
        if not isinstance(log_entries, list):
            log_entries = []
        log_entries.append({
            "run_id": run_id,
            "timestamp": now,
            "status": "no_tenders",
            "tender_count": 0,
            "doc_count": 0,
        })
        with open(scrape_log_path, "w") as f:
            json.dump(log_entries[-100:], f, indent=2)  # Keep last 100

    print(f"Added {added} leads to leads.json")
    return added

if __name__ == "__main__":
    main()
