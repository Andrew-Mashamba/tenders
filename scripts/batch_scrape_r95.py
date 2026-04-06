#!/usr/bin/env python3
"""Process 25 institutions for run_20260313_205329_batch95."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch95"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

INSTITUTIONS = [
    {"slug": "raktizm", "name": "RAKTIZM GROUP LIMITED", "url": "https://raktizm.co.tz/", "emails": ["info@raktizm.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "ram", "name": "RAM - Tanzania", "url": "https://www.ram.co.tz/", "emails": [], "tenders": 0, "docs": 0, "error": None},
    {"slug": "ramadagroup", "name": "For Domain Registration and Host", "url": "http://ramadagroup.co.tz/", "emails": [], "tenders": 0, "docs": 0, "error": None},
    {"slug": "ramfs", "name": "Home Default - RAM", "url": "https://ramfs.co.tz/", "emails": ["info@ramfs.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "randacottages", "name": "Kilimanjaro Hotel - Randa Cottages Moshi", "url": "https://randacottages.co.tz/", "emails": ["info@randacottages.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "raphaelholdings", "name": "Account Suspended", "url": "https://raphaelholdings.co.tz/", "emails": ["webmaster@raphaelholdings.co.tz"], "tenders": 0, "docs": 0, "error": "Account suspended"},
    {"slug": "raphaellogistics", "name": "Raphael Logistics (T) Limited", "url": "https://raphaellogistics.co.tz/", "emails": ["info@raphaellogistics.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "raqeeb", "name": "Raqeeb's Royal", "url": "https://raqeeb.co.tz/", "emails": ["info@raqeeb.com"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "rasimamd", "name": "Rasima Md", "url": "https://rasimamd.co.tz/", "emails": ["Info@rasimamd.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "ratego", "name": "Ratego Freight Forwarders", "url": "https://ratego.co.tz/", "emails": ["info@ratego.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "ravenai", "name": "ravenai", "url": "https://ravenai.co.tz/", "emails": ["info@ravenai.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "ravens", "name": "Ravens Technologies", "url": "https://ravens.co.tz/", "emails": [], "tenders": 0, "docs": 0, "error": None},
    {"slug": "ravji", "name": "ravji.co.tz", "url": "https://ravji.co.tz/", "emails": ["dsm@ravji.co.tz", "moshi@ravji.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "rayoconsultants", "name": "Rayo Consultant", "url": "https://rayoconsultants.co.tz/", "emails": [], "tenders": 0, "docs": 0, "error": None},
    {"slug": "raysofhope", "name": "Rays of Hope College", "url": "https://raysofhope.ac.tz/", "emails": ["info@raysofhope.ac.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "razaq", "name": "Razaq Innovations", "url": "https://razaq.co.tz/", "emails": ["info@razaq.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "rcenterprises", "name": "RC Business Enterprises Limited", "url": "https://rcenterprises.co.tz/", "emails": ["info@rcenterprises.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "rcl", "name": "Redemptive Capital", "url": "https://rcl.co.tz/", "emails": [], "tenders": 0, "docs": 0, "error": None},
    {"slug": "rdo", "name": "RDO Tanzania", "url": "https://www.rdo.or.tz/", "emails": ["rdomdabulo2012@gmail.com"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "rea", "name": "REA", "url": "https://rea.go.tz/", "emails": ["dg@rea.go.tz", "webmaster@rea.go.tz", "pmu@rea.go.tz", "info@rea.go.tz"], "tenders": 0, "docs": 0, "error": "Fetch timeout"},
    {"slug": "realtech", "name": "Realtech", "url": "https://realtech.co.tz/", "emails": ["info@realtech.co.tz"], "tenders": 0, "docs": 0, "error": None},
    {"slug": "recoda", "name": "RECODA", "url": "https://recoda.or.tz/", "emails": ["info@recoda.or.tz"], "tenders": 1, "docs": 1, "error": None},
    {"slug": "redbull", "name": "Red Bull Energy Drink", "url": "https://www.redbull.com/", "emails": [], "tenders": 0, "docs": 0, "error": None},
    {"slug": "reddot", "name": "Red Dot Distribution", "url": "https://www.reddotdistribution.com/", "emails": [], "tenders": 0, "docs": 0, "error": None},
    {"slug": "redeso", "name": "Relief to Development Society (REDESO)", "url": "https://www.redeso.or.tz/", "emails": ["redeso-hq@redeso.or.tz", "kibondo@redeso.or.tz", "redesongara@gmail.com", "redesokishapu@gmail.com"], "tenders": 0, "docs": 0, "error": None},
]

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


def main():
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    for inst in INSTITUTIONS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)

        status = "error" if inst.get("error") else ("success" if inst["tenders"] > 0 else "no_tenders")
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW,
            "active_tenders_count": inst["tenders"],
            "status": status,
            "error": inst.get("error"),
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log_path = inst_dir / "scrape_log.json"
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": status,
            "tenders_found": inst["tenders"],
            "documents_downloaded": inst["docs"],
            "errors": [inst["error"]] if inst.get("error") else [],
        }
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_data = json.load(f)
            runs = log_data.get("runs", [])
        else:
            runs = []
        runs.append(log_entry)
        with open(scrape_log_path, "w") as f:
            json.dump({"runs": runs}, f, indent=2)

        if inst["tenders"] == 0 and slug not in ("rea",):
            lead = {
                "institution_slug": slug,
                "institution_name": inst["name"],
                "website_url": inst["url"],
                "emails": inst.get("emails", []),
                "opportunity_type": "sell",
                "opportunity_description": "No formal tenders found on {} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.".format(inst["name"]),
                "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & {}".format(inst["name"]),
                "draft_email_body": DRAFT_BODY.format(institution_name=inst["name"]),
                "created_at": NOW,
                "status": "pending",
            }
            existing_slugs = {l.get("institution_slug") for l in leads}
            if slug not in existing_slugs:
                leads.append(lead)

        doc_count = inst["docs"]
        print(f"RESULT|{slug}|{status}|{inst['tenders']}|{doc_count}")

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2)

    print("\nLeads appended. Running sync_leads_csv.py...")
    import subprocess
    subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=str(PROJECT), check=True)


if __name__ == "__main__":
    main()
