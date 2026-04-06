#!/usr/bin/env python3
"""Process 25 institutions for run_20260313_205329_batch23 - no tenders found, create leads."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch23"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

INSTITUTIONS = [
    {"slug": "cmggroup", "name": "CMG GROUP", "url": "http://cmggroup.co.tz/", "emails": [], "status": "success", "error": None},
    {"slug": "cmsa", "name": "Capital Market and Securities Authority", "url": "https://cmsa.go.tz/", "emails": ["info@cmsa.go.tz", "barua@cmsa.go.tz"], "status": "error", "error": "Fetch timed out"},
    {"slug": "cmtl", "name": "CMTL Logistics", "url": "https://cmtllogistics.com/", "emails": [], "status": "success", "error": None},
    {"slug": "cmtllogistics", "name": "CMTL Logistics", "url": "https://cmtllogistics.com/", "emails": [], "status": "success", "error": None},
    {"slug": "cnet", "name": "C-Net Technologies Tanzania Ltd", "url": "https://www.onet.co.tz/", "emails": [], "status": "success", "error": None},
    {"slug": "cntech", "name": "Computer Networks & Technology", "url": "https://cntech.co.tz/", "emails": ["info@cntech.co.tz", "cntech@cntech.co.tz"], "status": "success", "error": None},
    {"slug": "coastalholidays", "name": "Coastal Holidays", "url": "https://coastalholidays.co.tz/", "emails": ["safari@coastalholidays.co.tz"], "status": "success", "error": None},
    {"slug": "cobwebtanzania", "name": "Cobweb Tanzania Limited", "url": "https://cobwebtanzania.co.tz/", "emails": ["info@cobwebtanzania.co.tz", "edwin@cobwebtanzania.co.tz"], "status": "success", "error": None},
    {"slug": "cocoda", "name": "COCODA Tanzania", "url": "https://cocoda.or.tz/", "emails": ["cocoda_ngo@yahoo.com"], "status": "success", "error": None},
    {"slug": "codelab", "name": "CodeLab Tanzania", "url": "https://codelab.co.tz/", "emails": ["hello@codelab.co.tz"], "status": "success", "error": None},
    {"slug": "codenet", "name": "Codenet Family", "url": "https://codenet.co.tz/", "emails": ["info@codenet.co.tz"], "status": "success", "error": None},
    {"slug": "codestudios", "name": "Code Studios", "url": "https://codestudios.co.tz/", "emails": ["jerry@codestudios.co.tz"], "status": "success", "error": None},
    {"slug": "coffee", "name": "TCB - Tanzania Coffee Board", "url": "https://coffee.go.tz/", "emails": ["info@coffee.go.tz"], "status": "error", "error": "Fetch timed out"},
    {"slug": "coffeecuring", "name": "Mbinga Coffee Curing Company", "url": "https://coffeecuring.co.tz/", "emails": ["mbinga@coffeecuring.co.tz"], "status": "success", "error": None},
    {"slug": "coherent", "name": "Coherent", "url": "https://coherent.co.tz/", "emails": ["webmaster@coherent.co.tz"], "status": "error", "error": "Account suspended"},
    {"slug": "colbaconsulting", "name": "COLBA Consulting Ltd", "url": "https://colbaconsulting.co.tz/", "emails": ["info@colbaconsulting.co.tz"], "status": "success", "error": None},
    {"slug": "colorplus", "name": "Safintra / Colorplus", "url": "https://www.safintra.co.za/", "emails": [], "status": "error", "error": "Fetch timed out"},
    {"slug": "colours", "name": "Colours & Compounds", "url": "https://www.colours.co.tz/", "emails": ["info@colours.co.tz"], "status": "success", "error": None},
    {"slug": "colvislogistics", "name": "Colvis Logistics", "url": "https://colvislogistics.co.tz/", "emails": ["info@colvislogistics.co.tz", "ceo@colvislogistics.co.tz"], "status": "success", "error": None},
    {"slug": "compact-energies", "name": "Compact Energies", "url": "https://compactenergies.co.tz/", "emails": ["info@compactenergies.co.tz", "info@compactenergies.tz"], "status": "success", "error": None},
    {"slug": "computer", "name": "Capricorn Technologies", "url": "https://computer.co.tz/", "emails": ["sales@computer.co.tz"], "status": "success", "error": None},
    {"slug": "comsec", "name": "ComSec Security Systems", "url": "https://comsec.co.tz/", "emails": ["sales@comsec.co.tz"], "status": "success", "error": None},
    {"slug": "connectioninv", "name": "Connection Investment Tanzania", "url": "https://connectioninv.co.tz/", "emails": ["info@connectioninv.co.tz"], "status": "success", "error": None},
    {"slug": "constructsyafrica", "name": "Constructsy Africa", "url": "https://constructsyafrica.co.tz/", "emails": ["info@constructsyafrica.co.tz", "themeht23@gmail.com"], "status": "success", "error": None},
    {"slug": "controller", "name": "Controller (Aircraft)", "url": "https://www.controller.com/", "emails": ["feedback@controller.com"], "status": "success", "error": None},
]

DRAFT_BODY = """Dear {name} Team,

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


def main():
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            leads = json.load(f)
    if not isinstance(leads, list):
        leads = leads.get("leads", []) if isinstance(leads, dict) else []

    existing_slugs = {l.get("institution_slug") for l in leads}
    new_leads_count = 0

    for inst in INSTITUTIONS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": None,
            "active_tenders_count": 0,
            "status": inst["status"],
            "error": inst["error"],
            "run_id": RUN_ID,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json
        scrape_log_path = inst_dir / "scrape_log.json"
        scrape_log = {"runs": []}
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                scrape_log = json.load(f)
        scrape_log["runs"] = scrape_log.get("runs", []) + [{
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": inst["status"],
            "tenders_found": 0,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": 0,
            "errors": [inst["error"]] if inst["error"] else [],
        }]
        with open(scrape_log_path, "w") as f:
            json.dump(scrape_log, f, indent=2)

        # Lead (only if not already in leads)
        if slug not in existing_slugs:
            emails = [e for e in inst["emails"] if e and "@" in e and not e.startswith("%")]
            lead = {
                "institution_slug": slug,
                "institution_name": inst["name"],
                "website_url": inst["url"],
                "emails": emails,
                "opportunity_type": "sell",
                "opportunity_description": "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
                "draft_email_body": DRAFT_BODY.format(name=inst["name"]),
                "created_at": NOW,
                "status": "pending",
            }
            leads.append(lead)
            existing_slugs.add(slug)
            new_leads_count += 1

        # Print result
        err_str = f" | {inst['error']}" if inst["error"] else ""
        print(f"RESULT|{slug}|{inst['status']}|0|0{err_str}")

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"\nAdded {new_leads_count} new leads. Total leads: {len(leads)}")


if __name__ == "__main__":
    main()
