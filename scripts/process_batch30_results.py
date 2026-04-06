#!/usr/bin/env python3
"""Process scrape results for batch30 institutions and update state."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch30"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Results: slug -> (status, tender_count, doc_count, emails[], institution_name, website_url)
# status: success|error|no_tenders
RESULTS = {
    "dowelef": ("no_tenders", 0, 0, ["info@dowelef.co.tz", "info@dowelef.com"], "DOW ELEF", "https://www.dowelef.co.tz/"),
    "doz-pie": ("no_tenders", 0, 0, [], "Doz-Pie Investment Co Ltd", "https://doz-pie.co.tz/"),
    "dpl": ("no_tenders", 0, 0, ["dpl.dsm@gmail.com", "sales@dpl.co.tz"], "Daya Premji Ltd", "https://dpl.co.tz/"),
    "dppznz": ("no_tenders", 0, 0, ["dpp@dppznz.go.tz"], "dpp znz", "https://dppznz.go.tz/"),
    "dreamchasers": ("no_tenders", 0, 0, ["support@dreamchasers.co.tz", "hello@dreamchasers.co.tz"], "DSL – ICT Service Providers", "https://dreamchasers.co.tz/"),
    "dreamdestinationsafaris": ("no_tenders", 0, 0, [], "Dream Destination Safaris", "https://dreamdestinationsafaris.co.tz/"),
    "drive": ("no_tenders", 0, 0, ["support@zanzibarcarrent.co.tz", "info@zanzibarcarrent.co.tz"], "Zanzibar Car Rental", "https://drive.co.tz/"),
    "drivechangefoundation": ("no_tenders", 0, 0, ["info@drivechangefoundation.co.tz"], "Drive Change Foundation", "https://drivechangefoundation.co.tz/"),
    "drrec": ("no_tenders", 0, 0, ["doris@drrec.co.tz", "dorismarealle@yahoo.co.uk"], "DRREC Catering", "https://drrec.co.tz/"),
    "drtc": ("error", 0, 0, ["info@drtc.co.tz"], "DRTC Trading Company", "https://www.drtc.co.tz/"),
    "dse": ("error", 0, 0, ["complains@dse.co.tz", "info@dse.co.tz"], "Dar es Salaam Stock Exchange", "https://dse.co.tz/"),
    "dsfa": ("error", 0, 0, ["info@dsfa.go.tz"], "DSFA", "https://dsfa.go.tz/"),
    "dsm": ("error", 0, 0, ["ras@dsm.go.tz"], "Mkoa wa Dar es Salaam", "https://dsm.go.tz/"),
    "dsmcorridor": ("no_tenders", 0, 0, ["dcg@dsmcorridor.co.tz"], "DSM Corridor Group", "https://www.dsmcorridor.com/"),
    "dsmglass": ("no_tenders", 0, 0, ["sales@dsmglass.co.tz"], "Dar es Salaam Glass Works", "https://www.dsmglass.co.tz/"),
    "dsouza": ("no_tenders", 0, 0, [], "Dsouza Advocates Arusha", "https://dsouza.co.tz/"),
    "dtcl": ("no_tenders", 0, 0, ["info@dtcl.co.tz", "fredy55@gmail.com", "georgemajwalla@gmail.com"], "Dodoma Data Tech Co Ltd", "https://dtcl.co.tz/"),
    "duce": ("no_tenders", 0, 0, ["principal@duce.ac.tz"], "Dar es Salaam University College of Education", "https://duce.ac.tz/"),
    "duhosting": ("no_tenders", 0, 0, ["info@duhosting.tz", "info@mycompany.tz"], "DUHosting", "https://duhosting.tz/"),
    "duhosting.tz": ("no_tenders", 0, 0, ["info@duhosting.tz", "info@mycompany.tz"], "DUHosting", "https://duhosting.tz/"),
    "dukalangu": ("no_tenders", 0, 0, ["info@dukalangu.co.tz", "support@dukalangu.co.tz"], "DukaLangu", "https://dukalangu.co.tz/"),
    "dukanikwetu": ("no_tenders", 0, 0, [], "DukaniKwetu", "https://www.dukanikwetu.co.tz/"),
    "durbantz": ("no_tenders", 0, 0, ["administration@durbantz.co.tz", "coolwanglu@gmail.com"], "Durban Investment Company", "https://durbantz.co.tz/"),
    "duthebest": ("no_tenders", 0, 0, ["bethebesttz@gmail.com"], "BeTheBestTZ", "https://duthebest.co.tz/"),
    "duwasa": ("error", 0, 0, ["md@duwasa.go.tz"], "DUWASA", "https://duwasa.go.tz/"),
}

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
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}

    for slug, (status, tender_count, doc_count, emails, inst_name, website_url) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        # Ensure tenders dirs exist
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "status": "success" if status != "error" else "error",
            "error": "Site down or blocked" if status == "error" else None,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json
        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_data = json.load(f)
            runs = log_data.get("runs", [])
        else:
            runs = []

        runs.append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": "success" if status != "error" else "error",
            "tenders_found": tender_count,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": ["Site down or blocked"] if status == "error" else [],
        })
        with open(scrape_log_path, "w") as f:
            json.dump({"runs": runs}, f, indent=2)

        # Append lead for no_tenders and error (opportunity outreach)
        if slug not in existing_slugs and status in ("no_tenders", "error"):
            # Filter to valid emails only
            valid_emails = [e for e in emails if e and "@" in str(e) and not str(e).endswith((".jpg", ".png", ".pdf"))]
            lead = {
                "institution_slug": slug,
                "institution_name": inst_name,
                "website_url": website_url,
                "emails": valid_emails,
                "opportunity_type": "sell",
                "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services." if status == "no_tenders" else "Site inaccessible. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
                "draft_email_body": DRAFT_BODY.format(name=inst_name),
                "created_at": NOW,
                "status": "pending",
            }
            leads.append(lead)
            existing_slugs.add(slug)

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
