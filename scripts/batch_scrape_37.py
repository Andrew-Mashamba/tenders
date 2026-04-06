#!/usr/bin/env python3
"""Process batch 37 scrape results: update last_scrape, scrape_log, append leads."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch37"
INST_DIR = PROJECT / "institutions"
LEADS_JSON = PROJECT / "opportunities" / "leads.json"

# Scrape results: slug -> (status, tender_count, doc_count, error?, emails[], institution_name, website_url)
RESULTS = [
    ("eya", "error", 0, 0, "Account suspended", [], "Account Suspended", "https://eya.co.tz/"),
    ("eyecuemedia", "no_tenders", 0, 0, None, ["sales@eyecuemedia.co.tz"], "Eyecuemedia Solutions", "https://eyecuemedia.co.tz/"),
    ("f21c", "no_tenders", 0, 0, None, ["info@f21c.co.tz", "fidelity21century@outlook.com"], "F21 Century", "https://f21c.co.tz/"),
    ("fabcars", "no_tenders", 0, 0, None, ["chauffeur@fabcars.co.tz"], "Fab Cars", "https://fabcars.co.tz/"),
    ("fadeco", "no_tenders", 0, 0, None, ["projects@fadeco.co.tz", "sekiku2018@gmail.com"], "Fadeco", "https://www.fadeco.co.tz/"),
    ("fadhiliteenstanzania", "no_tenders", 0, 0, None, ["fadhiliteens@yahoo.com"], "Fadhili Teens Organization", "https://fadhiliteenstanzania.or.tz/"),
    ("faharimotors", "no_tenders", 0, 0, None, [], "Fahari Motors", "https://faharimotors.co.tz/"),
    ("fakhrigroup", "no_tenders", 0, 0, None, ["sales@fakhrigroup.co.tz"], "Fakhri Group Tanzania Ltd", "https://fakhrigroup.co.tz/"),
    ("falcon", "no_tenders", 0, 0, None, [], "Falcon Plastics Ltd", "https://falcon.co.tz/"),
    ("fandomcars", "no_tenders", 0, 0, None, ["info@fandomcars.co.tz"], "Fandom Cars", "https://fandomcars.com/"),
    ("fanikiwa", "no_tenders", 0, 0, None, [], "Fanikiwa MicroFinance", "https://fanikiwa.co.tz/"),
    ("fantuzzi", "no_tenders", 0, 0, None, ["administrator@fantuzz.co.tz", "info@fantuzzi.co.tz", "administrator@fantuzzi.co.tz"], "Fantuzzi Investment Ltd", "https://fantuzzi.co.tz/"),
    ("farm", "no_tenders", 0, 0, None, [], "FARM Co. Ltd", "https://farm.co.tz/"),
    ("farmaccess", "no_tenders", 0, 0, None, ["info@farmaccess.co.tz"], "FarmAccess", "https://www.farmaccess.co.tz/"),
    ("farmbase", "no_tenders", 0, 0, "Site compromised (darknet links)", ["info@farmbase.co.tz"], "Farmbase Limited", "https://farmbase.co.tz/"),
    ("faruconsulting", "error", 0, 0, "Fetch timeout", ["md@faruconsulting.co.tz"], "Faru Consulting International", "https://faruconsulting.co.tz/"),
    ("fasthub", "no_tenders", 0, 0, None, ["business@fasthub.co.tz"], "FastHub Solutions", "https://fasthub.co.tz/"),
    ("fastliner", "no_tenders", 0, 0, None, ["info@fastliner.co.tz"], "Fastliner Company Limited", "https://fastliner.co.tz/"),
    ("fatemadewji", "no_tenders", 0, 0, None, ["fatema@fatemadewji.co.tz"], "Fatema Dewji", "https://fatemadewji.com/"),
    ("fauluhost", "no_tenders", 0, 0, None, ["support@fauluhost.co.tz"], "FauluHost", "https://fauluhost.co.tz/"),
    ("fawetanzania", "no_tenders", 0, 0, None, ["info@fawetanzania.or.tz"], "FAWETZ", "https://fawetanzania.or.tz/"),
    ("fazaldad", "no_tenders", 0, 0, None, ["haider@biosustain.de", "info@fazaldad.co.tz"], "Fazal Dad Tanzania Limited", "https://fazaldad.co.tz/"),
    ("fbattorneys", "no_tenders", 0, 0, None, [], "FB Attorneys", "https://fbattorneys.co.tz/"),
    ("fcl", "no_tenders", 0, 0, None, [], "Fesam Construction Limited", "https://fcl.co.tz/"),
    ("fece", "no_tenders", 0, 0, None, ["info@fece.or.tz"], "FECE", "https://fece.or.tz/"),
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
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    iso_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Load existing leads
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}

    summaries = []

    for slug, status, tender_count, doc_count, error, emails, inst_name, website_url in RESULTS:
        inst_path = INST_DIR / slug
        inst_path.mkdir(parents=True, exist_ok=True)
        (inst_path / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "next_scrape": now,
            "active_tenders_count": tender_count,
            "status": "success" if status != "error" else "error",
            "error": error,
        }
        with open(inst_path / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json
        scrape_log_path = inst_path / "scrape_log.json"
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_data = json.load(f)
            runs = log_data.get("runs", [])
        else:
            runs = []

        run_entry = {
            "run_id": RUN_ID,
            "timestamp": now,
            "duration_seconds": 0,
            "status": "success" if status != "error" else "error",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [error] if error else [],
        }
        runs.append(run_entry)
        with open(scrape_log_path, "w") as f:
            json.dump({"runs": runs}, f, indent=2)

        # Append lead for no_tenders; skip eya (site suspended - couldn't scrape)
        if status == "no_tenders" or (status == "error" and slug == "faruconsulting"):
            if slug not in existing_slugs:
                opp_desc = "No formal tenders found"
                if error:
                    opp_desc += f". Note: {error}"
                else:
                    opp_desc += ". ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."

                lead = {
                    "institution_slug": slug,
                    "institution_name": inst_name,
                    "website_url": website_url,
                    "emails": [e for e in emails if e and "@" in e],
                    "opportunity_type": "sell",
                    "opportunity_description": opp_desc,
                    "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
                    "draft_email_body": DRAFT_BODY.format(name=inst_name),
                    "created_at": iso_now,
                    "status": "pending",
                }
                leads.append(lead)
                existing_slugs.add(slug)

        # Summary line
        summaries.append(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Save leads
    with open(LEADS_JSON, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    for s in summaries:
        print(s)


if __name__ == "__main__":
    main()
