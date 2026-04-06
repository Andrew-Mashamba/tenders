#!/usr/bin/env python3
"""Process 25 institutions for run_20260313_205329_batch110.
For each: update last_scrape.json, scrape_log.json; if no tenders, append lead to leads.json.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch110"
INSTITUTIONS = [
    ("stjcs", "ST. JOSEPH'S COLLEGE SHINYANGA", "http://stjcs.ac.tz/", ["mchomoka@gmail.com"]),
    ("stjosephs", "Account Suspended (stjosephs)", "https://stjosephs.co.tz/", ["webmaster@stjosephs.co.tz"]),
    ("stmatthews", "St. Matthews Schools", "https://www.stmatthews.ac.tz/", ["admission@stmatthewsschools.ac.tz"]),
    ("stpamachiusinclusive", "St.Pamachius Inclusive", "https://stpamachiusinclusive.ac.tz/", ["st.pamachiusinclusive2019@gmail.com"]),
    ("strategicagility", "Strategic Agility", "https://www.strategicagility.co.tz/", ["info@strategicagility.co.tz"]),
    ("strategis", "Strategis Insurance", "https://www.strategis.co.tz/", ["insurance@strategis.co.tz"]),
    ("striderengineering", "Strider Engineering", "https://striderengineering.co.tz/", []),
    ("stzelephants", "STEP Southern Tanzania Elephant Program", "https://www.stzelephants.or.tz/", ["info@stzelephants.or.tz", "applications@stzelephants.or.tz"]),
    ("sua", "Sokoine University of Agriculture", "https://sua.ac.tz/", []),
    ("suanet", "Sokoine University of Agriculture", "https://www.sua.ac.tz/", []),
    ("subehude", "SuBeHuDe", "https://subehude.or.tz/", ["info@subehude.or.tz"]),
    ("subtech", "Substation Technology Engineering", "https://subtech.co.tz/", ["info@subtech.co.tz"]),
    ("sugeco", "SUGECO", "https://sugeco.or.tz/", ["info@sugeco.or.tz"]),
    ("sullivanprovostschools", "Sullivan Provost Schools", "https://www.sullivanprovostschools.ac.tz/", ["admin@sullivanprovostschools.ac.tz"]),
    ("sumait", "SUMAIT", "https://sumait.ac.tz/", ["info@sumait.ac.tz", "info@eduker.com"]),
    ("sumajkt", "SUMAJKT", "https://sumajkt.go.tz/", ["info@sumajkt.go.tz"]),
    ("sumatrasaccos", "SUMATRA SACCOS", "https://sumatra.bunisoft.co.tz/", []),
    ("sumbawangarrh", "Sumbawanga RRH", "https://sumbawangarrh.go.tz/", ["barua@sumbawangarrh.go.tz"]),
    ("sunbirdtours", "Sunbird Tours", "https://sunbirdtours.co.tz/", ["reviews@sunbirdtours.co.tz", "contact@tembeatanzania.com", "info@sunbirdtours.com"]),
    ("sundymerchants", "Sundy Merchants", "https://sundymerchants.co.tz/", ["team@latofonts.com"]),
    ("sunego", "Account Suspended (sunego)", "https://sunego.co.tz/", ["webmaster@sunego.co.tz"]),
    ("sunnyadventures", "Sunny Adventure Safaris", "https://sunnyadventures.co.tz/", []),
    ("supercom", "Supercom Tanzania", "https://supercom.co.tz/", ["Info@supercom.co.tz", "info@supercom.co.tz"]),
    ("superstore", "Superstore Tanzania", "https://superstore.co.tz/", []),
    ("supplyandfix", "Supply And Fix", "https://supplyandfix.co.tz/", ["moses@supplyandfix.co.tz", "nyari@supplyandfix.co.tz"]),
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
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}

    results = []
    for slug, name, url, emails in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # Scrape result: no tenders found for any (per fetch analysis)
        tender_count = 0
        doc_count = 0
        status = "ok"
        error_msg = None

        if "Account Suspended" in name or slug in ("stjosephs", "sunego"):
            status = "error"
            error_msg = "Account suspended / site down"

        last_scrape = {
            "run_id": RUN_ID,
            "scraped_at": now,
            "tender_url": url,
            "tender_count": tender_count,
            "doc_count": doc_count,
            "status": status,
            "error": error_msg,
        }

        scrape_log_entry = {
            "run_id": RUN_ID,
            "scraped_at": now,
            "tender_count": tender_count,
            "doc_count": doc_count,
            "status": status,
            "error": error_msg,
        }

        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log_path = inst_dir / "scrape_log.json"
        log_entries = []
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_entries = json.load(f)
        log_entries.append(scrape_log_entry)
        with open(scrape_log_path, "w") as f:
            json.dump(log_entries, f, indent=2)

        # Opportunities: append lead if no tenders and not already in leads
        if tender_count == 0 and slug not in existing_slugs:
            display_name = name.replace("Account Suspended (stjosephs)", "stjosephs.co.tz").replace("Account Suspended (sunego)", "sunego.co.tz")
            lead = {
                "institution_slug": slug,
                "institution_name": display_name,
                "website_url": url,
                "emails": [e for e in emails if e and "@" in e and not e.endswith(".jpg")],
                "opportunity_type": "sell",
                "opportunity_description": "No formal tenders found on " + display_name + " website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {display_name}",
                "draft_email_body": DRAFT_BODY.format(name=display_name),
                "created_at": now,
                "status": "pending",
            }
            leads.append(lead)
            existing_slugs.add(slug)

        results.append((slug, status, tender_count, doc_count))
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    # Run sync
    import subprocess
    subprocess.run(
        ["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=str(PROJECT),
        check=True,
    )
    print("\nSync complete.")


if __name__ == "__main__":
    main()
