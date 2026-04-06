#!/usr/bin/env python3
"""Process 25 institutions: update scrape state, add leads for no-tender cases."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch14"
NOW = datetime.now(timezone.utc).isoformat()

INSTITUTIONS = [
    ("behobeho", "Beho Beho", "https://www.behobeho.co.tz/", ["reservations@africa-reps.com", "reservations@behobeho.com"]),
    ("beibamartravel", "Beibamar Travel", "https://beibamartravel.co.tz/", []),
    ("beiyako", "Beiyako", "https://beiyako.co.tz/", []),
    ("belfort", "Belfort Tanzania", "https://www.belfort.co.tz/", ["business@belfort.co.tz"]),
    ("belva", "Belva Consult", "https://www.belva.co.tz/", []),
    ("benison", "Benison", "https://benison.co.tz/", ["hello@benison.co.tz"]),
    ("bensonandcompany", "Benson & Company", "https://bensonandcompany.com/", ["info@bensonandcompany.co.tz"]),
    ("best", "Best Ltd", "https://best.co.tz/", ["info@best.co.tz"]),
    ("besta", "Besta", "https://besta.co.tz/", ["admin@besta.co.tz", "contact@besta.co.tz"]),
    ("bestone", "Best One", "https://bestone.co.tz/", ["info@bestone.co.tz"]),
    ("bet", "Bet Tanzania", "https://bet.co.tz/", []),
    ("bet22", "22Bet Tanzania", "https://bet22.co.tz/", ["support-en@22bet.com"]),
    ("betalaw", "BETA Law", "https://betalaw.co.tz/", ["info@betalaw.co.tz"]),
    ("betaomega-agrib", "Beta Omega Agribusiness", "https://betaomega-agrib.co.tz/", ["info@betaomega-agrib.co.tz"]),
    ("bethelservices", "Bethel Services", "https://bethelservices.co.tz/", ["info@bethelservices.co.tz"]),
    ("bethlehemstar", "Bethlehem Star School", "https://bethlehemstar.ac.tz/", ["info@bethlehemstar.ac.tz"]),
    ("beyond", "Beyond Nature Ltd", "https://beyond.co.tz/", ["info@beyond.or.tz"]),
    ("bfi", "BareFoot International", "https://bfi.co.tz/", ["info@bfi.co.tz"]),
    ("bhti", "BESHA Health Training Institute", "https://bhti.ac.tz/", ["besha.bhti@gmail.com"]),
    ("bhusene", "Bhusene Store", "https://bhusene.co.tz/", []),
    ("biclimited", "Buruburu Investment", "https://biclimited.co.tz/", ["info@biclimited.co.tz"]),
    ("bidvest", "Bidvest Group", "https://bidvest.com/", []),
    ("bigw", "BIG W", "https://bigw.co.tz/", ["bigw-inquries@bigw.co.tz"]),
    ("biharamulodc", "Biharamulo District Council", "https://biharamulodc.go.tz/", ["ded@biharamulodc.go.tz"]),
    ("bihas", "BUKUMBI Institute", "https://bihas.ac.tz/", ["bukumbinursing@yahoo.com"]),
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
    leads_to_append = []
    results = []

    for slug, name, url, emails in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)

        # All 25: no tenders found (from fetch analysis)
        tender_count = 0
        doc_count = 0
        status = "no_tenders"

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW,
            "active_tenders_count": 0,
            "status": status,
            "error": None,
            "run_id": RUN_ID,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2))

        scrape_log_path = inst_dir / "scrape_log.json"
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": 0,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": 0,
            "errors": [],
        }
        if scrape_log_path.exists():
            data = json.loads(scrape_log_path.read_text())
            runs = data.get("runs", []) if isinstance(data, dict) else data
            if not isinstance(runs, list):
                runs = [runs]
        else:
            runs = []
        runs.append(log_entry)
        scrape_log_path.write_text(json.dumps({"runs": runs}, indent=2))

        # Lead for no-tender case
        if not emails:
            emails = []
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(name=name),
            "created_at": NOW,
            "status": "pending",
        }
        leads_to_append.append(lead)

        results.append(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Append leads
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        data = json.loads(leads_path.read_text())
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}
    for lead in leads_to_append:
        if lead["institution_slug"] not in existing_slugs:
            leads.append(lead)
            existing_slugs.add(lead["institution_slug"])
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False))

    for r in results:
        print(r)


if __name__ == "__main__":
    main()
