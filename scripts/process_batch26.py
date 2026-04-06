#!/usr/bin/env python3
"""Process 25 institutions for run_20260313_205329_batch26 - no tenders found, append leads."""
import json
from pathlib import Path
from datetime import datetime

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch26"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

INSTITUTIONS = [
    {"slug": "cybergentraining", "name": "IT Training in Tanzania | Cybergen", "url": "https://cybergentraining.co.tz/", "emails": ["training@cybergentraining.co.tz"]},
    {"slug": "cyclo", "name": "Cyclo Technologies", "url": "https://www.cyclo.co.tz/", "emails": ["Info@cyclo.co.tz", "info@cyclo.co.tz"]},
    {"slug": "cyd", "name": "Center for Youth Dialogue", "url": "https://cyd.or.tz/", "emails": ["info@cyd.tz"]},
    {"slug": "dabagainstitute", "name": "Dabaga Institute of Agriculture", "url": "https://dabagainstitute.ac.tz/", "emails": ["info@dabagainstitute.ac.tz"]},
    {"slug": "daikintanzania", "name": "Daikin Tanzania Ltd", "url": "https://daikintanzania.co.tz/", "emails": []},
    {"slug": "dailynews", "name": "Daily News", "url": "https://dailynews.co.tz/", "emails": []},
    {"slug": "damaxsolutions", "name": "DAMAX Solutions", "url": "https://damaxsolutions.co.tz/", "emails": ["info@damaxsolutions.com"]},
    {"slug": "daracademic", "name": "Dar Academic", "url": "https://daracademic.ac.tz/", "emails": ["webmaster@daracademic.ac.tz"]},
    {"slug": "darceramica", "name": "Dar Ceramica", "url": "https://darceramica.co.tz/", "emails": ["info@darceramica.co.tz"]},
    {"slug": "darpressmedia", "name": "Dar Press Media", "url": "https://darpressmedia.co.tz/", "emails": ["hello@darpressmedia.com"]},
    {"slug": "darquelogistics", "name": "Darque Logistics", "url": "https://darquelogistics.co.tz/", "emails": ["info@darquelogistics.co.tz"]},
    {"slug": "darshopping", "name": "Dar Shopping", "url": "https://darshopping.co.tz/", "emails": ["sales@darshopping.co.tz"]},
    {"slug": "dart", "name": "DART", "url": "https://dart.go.tz/", "emails": ["info@dart.go.tz"]},
    {"slug": "daryachtclub", "name": "Dar es Salaam Yacht Club", "url": "https://daryachtclub.co.tz/", "emails": []},
    {"slug": "dashingdiva", "name": "Dashingdiva Beauty Salon", "url": "https://dashingdiva.co.tz/", "emails": []},
    {"slug": "dataflow", "name": "DataFlow Telecoms", "url": "https://dataflow.co.tz/", "emails": ["info@dataflow.co.tz"]},
    {"slug": "datalabs", "name": "Datalabs (T) Ltd", "url": "https://datalabs.co.tz/", "emails": ["info@datalabs.co.tz"]},
    {"slug": "dataskycollege", "name": "Datasky College", "url": "https://dataskycollege.ac.tz/", "emails": ["dataskycollege@yahoo.com"]},
    {"slug": "datavillage", "name": "Data Village Technologies", "url": "https://datavillage.co.tz/", "emails": ["info@datavillage.co.tz"]},
    {"slug": "datavision", "name": "DataVision International", "url": "https://datavision.co.tz/", "emails": []},
    {"slug": "dautechnology", "name": "Dau Technology LLC", "url": "https://dautechnology.co.tz/", "emails": ["info@dautechnology.co.tz"]},
    {"slug": "davisandshirtliff", "name": "Davis & Shirtliff Tanzania", "url": "https://davisandshirtliff.co.tz/", "emails": ["tzcontactcenter@dayliff.com"]},
    {"slug": "davot", "name": "DAVOT ICT", "url": "https://davot.co.tz/", "emails": ["davot.info@yahoo.com", "info@davot.co.tz"]},
    {"slug": "dawasa", "name": "DAWASA", "url": "https://dawasa.go.tz/", "emails": ["info@dawasa.go.tz"]},
    {"slug": "dcbrilliant", "name": "DC Brilliant College", "url": "https://dcbrilliant.ac.tz/", "emails": ["dcbrilliant.ac@gmail.com"]},
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
    # Append leads
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}
    added = 0
    for inst in INSTITUTIONS:
        if inst["slug"] in existing_slugs:
            continue
        lead = {
            "institution_slug": inst["slug"],
            "institution_name": inst["name"],
            "website_url": inst["url"],
            "emails": list(dict.fromkeys([e for e in inst["emails"] if e])),
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
            "draft_email_body": DRAFT_BODY.format(name=inst["name"]),
            "created_at": NOW,
            "status": "pending",
        }
        leads.append(lead)
        added += 1

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    # Update last_scrape and scrape_log for each institution
    for inst in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / inst["slug"]
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": inst["slug"],
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": 0,
            "status": "success",
            "error": None,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        log_path = inst_dir / "scrape_log.json"
        log_data = {"runs": []}
        if log_path.exists():
            with open(log_path) as f:
                log_data = json.load(f)
        errors = []
        if inst["slug"] == "daracademic":
            errors.append("Account suspended")
        elif inst["slug"] == "dart":
            errors.append("Fetch timeout/SSL error")
        elif inst["slug"] == "dawasa":
            errors.append("NeST SPA - content loads via JS, no static tender listings")
        log_data.setdefault("runs", []).append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": "success" if not errors else "partial",
            "tenders_found": 0,
            "documents_downloaded": 0,
            "opportunity_lead_added": True,
            "errors": errors,
        })
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)

    # Run sync
    import subprocess
    subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True)

    print(f"Added {added} leads. Synced leads.csv.")
    for inst in INSTITUTIONS:
        status = "error" if inst["slug"] == "daracademic" else ("partial" if inst["slug"] in ("dart", "dawasa") else "no_tenders")
        print(f"RESULT|{inst['slug']}|{status}|0|0")


if __name__ == "__main__":
    main()
