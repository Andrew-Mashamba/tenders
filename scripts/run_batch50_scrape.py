#!/usr/bin/env python3
"""Process 25 institutions for run_20260313_205329_batch50 - no tenders found, create leads."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch50"

# Institution data: slug, name, website_url, emails[], fetch_error (None or str)
INSTITUTIONS = [
    ("immaculateconsulting", "Immaculate Consulting Tanzania Ltd", "https://immaculateconsulting.co.tz/", ["info@immaculateconsulting.co.tz"], None),
    ("immigration", "Tanzania Immigration Department", "https://immigration.go.tz/", ["proznz@immigration.go.tz", "info@immigration.go.tz"], None),
    ("imori", "IMORI International", "https://imori.co.tz/", ["info@imori.co.tz"], None),
    ("impactlogistics", "Impact Logistics", "https://impactlogistics.co.tz/", ["info@impactlogitstics.co.tz"], None),
    ("impala", "Impala Online Shopping", "https://impala.co.tz/", [], None),
    ("impatienstours", "Impatiens Tours and Safaris", "https://impatienstours.co.tz/", ["info@impatienstours.co.tz"], None),
    ("imperial", "Imperial Schools Tanzania", "https://imperial.ac.tz/", ["info@imperial.ac.tz"], None),
    ("imperialconstruction", "Imperial Construction Company", "https://imperialconstruction.co.tz/", [], None),
    ("imperialinnovations", "Imperial Innovations", "https://imperialinnovations.co.tz/", ["md@imperialinnovations.co.tz"], None),
    ("imperialmedia", "Imperial Media", "https://imperialmedia.co.tz/", ["info@imperialmedia.co.tz"], None),
    ("imperialsecurity", "Imperial Security Company Limited", "https://imperialsecurity.co.tz/", ["info@imperialsecurity.co.tz"], None),
    ("imperium", "Imperium Insurance Brokers", "https://imperium.co.tz/", ["info@imperium.co.tz"], None),
    ("index", "Index Technology Tanzania", "http://eastenderstours.com/", ["sales@index.co.tz", "info@index.co.tz"], "Site returned 503 Service Unavailable"),
    ("indianschooldsm", "Indian School Dar es Salaam", "https://indianschooldsm.ac.tz/", ["indianschooldsm@gmail.com"], None),
    ("infinicare", "Infinicare", "https://infinicare.co.tz/", ["info@infinicare.co.tz", "sales@infinicare.co.tz"], None),
    ("infinitecleaners", "Infinite Cleaners Limited", "https://infinitecleaners.co.tz/", ["info@cleaningmaster.co.tz"], None),
    ("influencers", "Influencer Awards Tanzania", "https://influencers.co.tz/", [], None),
    ("infoage", "Infoage Technologies", "https://infoage.co.tz/", [], None),
    ("infogear", "Infogear Technology", "https://infogear.co.tz/", ["Sales@infogear.co.tz"], None),
    ("infosec", "Infosec Cybersecurity", "https://www.infosec.co.tz/", ["info@infosec.co.tz", "info@infosec.co.rw"], None),
    ("infosoftconsult", "Infosoft Consult", "https://infosoftconsult.co.tz/", ["info@infosoftconsult.co.tz"], None),
    ("infosoftz", "Infosoftz Company Limited (ICL)", "https://infosoftz.co.tz/", ["info@infosoftz.co.tz"], None),
    ("infotaaluma", "InfoTaaluma App", "https://infotaaluma.co.tz/", ["info@infotaaluma.co.tz"], None),
    ("infotech", "Infotech Investment Group", "https://infotech.co.tz/", ["info@infotech.co.tz"], "Fetch timed out"),
    ("infowise", "InfoWise Systems Ltd", "http://infowise.tz/", [], None),
]

DRAFT_EMAIL_SUBJECT = "Partnership Opportunity – ZIMA Solutions & {name}"
DRAFT_EMAIL_BODY = """Dear {name} Team,

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
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    leads_to_append = []

    for slug, name, website_url, emails, fetch_error in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        status = "error" if fetch_error else "success"
        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "run_id": RUN_ID,
            "active_tenders_count": 0,
            "documents_downloaded": 0,
            "status": status,
            "error": fetch_error,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json - append this run
        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                scrape_log = json.load(f)
        else:
            scrape_log = {"runs": []}

        scrape_log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": now,
            "status": status,
            "tenders_found": 0,
            "documents_downloaded": 0,
            "tender_ids": [],
            "errors": [fetch_error] if fetch_error else [],
        })
        with open(scrape_log_path, "w") as f:
            json.dump(scrape_log, f, indent=2)

        # Lead for opportunities
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": website_url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on " + name + " website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": DRAFT_EMAIL_SUBJECT.format(name=name),
            "draft_email_body": DRAFT_EMAIL_BODY.format(name=name),
            "created_at": now,
            "status": "pending",
        }
        leads_to_append.append(lead)

        print(f"RESULT|{slug}|{status}|0|0")

    # Append to leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    with open(leads_path) as f:
        leads_data = json.load(f)
    leads_list = leads_data if isinstance(leads_data, list) else leads_data.get("leads", [])
    leads_list.extend(leads_to_append)
    with open(leads_path, "w") as f:
        json.dump(leads_list, f, indent=2, ensure_ascii=False)

    print(f"\nAppended {len(leads_to_append)} leads. Running sync_leads_csv.py...")
    import subprocess
    subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True)
    print("Done.")


if __name__ == "__main__":
    main()
