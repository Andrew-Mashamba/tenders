#!/usr/bin/env python3
"""Process scrape results for run_20260313_205329_batch124 - 25 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch124"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z")

# Scrape results: slug -> (status, tender_count, doc_count, error?)
# All had 0 tenders based on fetch analysis
RESULTS = [
    ("ufertilizers", "success", 0, 0, None, "United Fertilizer Company Ltd", "https://ufertilizers.com/", ["info@ufertilizers.com"]),
    ("ufugaji", "success", 0, 0, None, "Jifunze mbinu za kisasa za ufugaji", "https://ufugaji.co.tz/", []),
    ("ufxc", "error", 0, 0, "Fetch timed out", "Universal FX Consultants", "https://ufxc.co.tz/", []),
    ("uhuden", "success", 0, 0, None, "Universal Human Development", "https://uhuden.or.tz/", ["info@uhuden.or.tz"]),
    ("uhuruauditors", "success", 0, 0, None, "Uhuru Auditors", "https://uhuruauditors.co.tz/", ["info@uhuruauditors.co.tz"]),
    ("uhurumusic", "success", 0, 0, None, "Uhuru Music", "https://uhurumusic.co.tz/", ["info@uhurumusic.co.tz", "maneno.sanga@yahoo.com", "maneno.sanga@uhurumusic.co.tz"]),
    ("uid", "success", 0, 0, None, "UPI Innovations and Developments", "http://uid.co.tz/", ["info@uid.co.tz", "info@UPI.co.tz", "UPIeconomicltd@gmail.com"]),
    ("ujenziandpaints", "success", 0, 0, None, "Ujenzi And Paints", "https://ujenziandpaints.co.tz/", ["info@ujenziandpaints.com"]),
    ("ukarimusafarisandtours", "success", 0, 0, None, "Ukarimu Safaris and Tours", "https://ukarimusafarisandtours.co.tz/", ["omary.salum98@gmail.com", "ukarimusafarisandtours@gmail.com", "info@ukarimusafarisandtours.co.tz", "tkondo@ukarimusafarisandtours.co.tz", "salum.omary@ymail.com"]),
    ("ukerewedc", "error", 0, 0, "Fetch timed out / SSL", "Ukerewe District Council", "https://ukerewedc.go.tz/tenders", []),
    ("ulfaplant", "error", 0, 0, "Fetch timed out", "ULFA Plant", "https://ulfaplant.co.tz/", []),
    ("ulizasheria", "success", 0, 0, None, "Uliza Sheria", "https://ulizasheria.co.tz/", []),
    ("ultimatefinance", "success", 0, 0, None, "Ultimate Finance", "https://ultimatefinance.co.tz/", ["info@ultimatefinance.co.tz"]),
    ("ultimateserengeti", "success", 0, 0, None, "Ultimate Serengeti", "https://ultimateserengeti.co.tz/", []),
    ("ultratec", "success", 0, 0, None, "Ultratec Investment Ltd", "https://ultratec.co.tz/", []),
    ("umg", "success", 0, 0, None, "UMG", "https://umg.co.tz/", []),
    ("unforgettableadventures", "success", 0, 0, None, "Unforgettable Adventures", "https://unforgettableadventures.co.tz/", ["info@unforgettableadventures.co.tz", "info@travolo.com"]),
    ("unicool", "success", 0, 0, None, "Unicool Ltd", "https://unicool.co.tz/", ["info@unicool.co.tz"]),
    ("unifiedafrica", "success", 0, 0, None, "Unified Africa", "https://unifiedafrica.co.tz/", ["info@unifiedafrica.co.tz"]),
    ("uniontrust", "success", 0, 0, None, "Union Trust Investments", "https://uniontrust.co.tz/", ["admin@uniontrust.co.tz"]),
    ("uniplaces", "success", 0, 0, None, "Uniplaces", "https://uniplaces.co.tz/", ["info@uniplaces.co.tz"]),
    ("unique", "success", 0, 0, None, "Unique Academy", "https://unique.ac.tz/", ["training@unique.ac.tz"]),
    ("uniquesafaris", "error", 0, 0, "Account suspended", "Unique Safaris", "https://uniquesafaris.co.tz/", ["webmaster@uniquesafaris.co.tz"]),
    ("unisoft", "success", 0, 0, None, "Unisoft Technologies", "https://unisoft.co.tz/", ["info@unisoft.co.tz"]),
    ("unitedinfrastructures", "error", 0, 0, "Account suspended", "United Infrastructures", "https://www.unitedinfrastructures.co.tz/", ["webmaster@unitedinfrastructures.co.tz"]),
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

    existing_slugs = {l.get("institution_slug") for l in leads}

    summaries = []

    for slug, status, tender_count, doc_count, err, name, url, emails in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "run_id": RUN_ID,
            "last_scrape": NOW,
            "status": status,
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json - append
        scrape_log_path = inst_dir / "scrape_log.json"
        log_entries = []
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_entries = json.load(f)
        log_entries.append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": status,
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "tender_ids": [],
            "errors": [err] if err else [],
            "notes": err or "No tenders or procurements found",
        })
        with open(scrape_log_path, "w") as f:
            json.dump(log_entries, f, indent=2)

        # If no tenders: add lead
        if tender_count == 0 and slug not in existing_slugs:
            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": url,
                "emails": [e for e in emails if "@" in e and "." in e],
                "opportunity_type": "sell",
                "opportunity_description": "No formal tenders found on " + name + " website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": DRAFT_BODY.format(institution_name=name),
                "created_at": NOW,
                "status": "pending",
            }
            leads.append(lead)
            existing_slugs.add(slug)

        summaries.append(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Save leads
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    for s in summaries:
        print(s)


if __name__ == "__main__":
    main()
