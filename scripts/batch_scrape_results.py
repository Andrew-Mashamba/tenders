#!/usr/bin/env python3
"""Apply scrape results for batch88 - update last_scrape, scrape_log, append new leads."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch88"
NOW = datetime.now(timezone.utc).isoformat()

# Results: slug -> (status, tender_count, doc_count)
# status: no_tenders | error | tenders_found
RESULTS = [
    ("oneway", "no_tenders", 0, 0),
    ("onewaycarriers", "no_tenders", 0, 0),
    ("oneworld", "no_tenders", 0, 0),
    ("onlinecasinobonus", "no_tenders", 0, 0),
    ("onlinemedia", "no_tenders", 0, 0),
    ("opestechnologies", "no_tenders", 0, 0),
    ("oppah", "no_tenders", 0, 0),
    ("opportunityeducation", "no_tenders", 0, 0),
    ("optimacorporate", "no_tenders", 0, 0),
    ("optin", "no_tenders", 0, 0),
    ("optioncouriers", "no_tenders", 0, 0),
    ("orbit-tz", "no_tenders", 0, 0),
    ("orchid", "no_tenders", 0, 0),
    ("orci", "no_tenders", 0, 0),  # tender page compromised
    ("organichillfarming", "no_tenders", 0, 0),
    ("origintrails", "no_tenders", 0, 0),
    ("orkonerei", "no_tenders", 0, 0),
    ("orpp", "error", 0, 0),  # timeout
    ("ortus", "no_tenders", 0, 0),
    ("osaka", "no_tenders", 0, 0),
    ("osborn", "no_tenders", 0, 0),
    ("osg", "error", 0, 0),  # timeout
    ("osha", "error", 0, 0),  # timeout
    ("oshi", "no_tenders", 0, 0),
    ("osiligilaimaasailodge", "no_tenders", 0, 0),
]

# New leads to append (not already in leads.json)
NEW_LEADS = [
    {
        "institution_slug": "orchid",
        "institution_name": "Orchid Investment Limited",
        "website_url": "https://orchid.co.tz/",
        "emails": ["info@orchid.co.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found on Orchid Investment Limited website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Orchid Investment Limited",
        "draft_email_body": "Dear Orchid Investment Limited Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support Orchid Investment Limited. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "orci",
        "institution_name": "Ocean Road Cancer Institute",
        "website_url": "https://www.orci.or.tz/",
        "emails": ["info@orci.or.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found on Ocean Road Cancer Institute tender page (page may be compromised). ZIMA Solutions could offer digital transformation, healthcare systems, or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Ocean Road Cancer Institute",
        "draft_email_body": "Dear Ocean Road Cancer Institute Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support Ocean Road Cancer Institute. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "origintrails",
        "institution_name": "Origin Trails",
        "website_url": "https://origintrails.co.tz/",
        "emails": ["info@origintrails.co.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found on Origin Trails website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Origin Trails",
        "draft_email_body": "Dear Origin Trails Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support Origin Trails. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "orpp",
        "institution_name": "ORPP (Office of the Registrar of Political Parties)",
        "website_url": "https://orpp.go.tz/",
        "emails": ["info@orpp.go.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Site timed out during scrape. ORPP is a government agency that may post zabuni. ZIMA Solutions could offer digital transformation or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & ORPP",
        "draft_email_body": "Dear ORPP Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support ORPP. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "osg",
        "institution_name": "Ofisi ya Wakili Mkuu wa Serikali (OSG)",
        "website_url": "https://osg.go.tz/",
        "emails": ["info@osg.go.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Site timed out during scrape. OSG is a government agency that may post zabuni. ZIMA Solutions could offer digital transformation or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & OSG",
        "draft_email_body": "Dear OSG Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support OSG. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "osha",
        "institution_name": "Occupational Safety and Health Authority",
        "website_url": "https://osha.go.tz/",
        "emails": ["info@osha.go.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Site timed out during scrape. OSHA is a government agency that may post zabuni. ZIMA Solutions could offer digital transformation or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & OSHA",
        "draft_email_body": "Dear OSHA Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support OSHA. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
]


def main():
    inst_dir = PROJECT / "institutions"
    leads_json = PROJECT / "opportunities" / "leads.json"

    # Load existing leads to get slugs
    leads = []
    if leads_json.exists():
        with open(leads_json) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}

    # Append new leads
    for lead in NEW_LEADS:
        if lead["institution_slug"] not in existing_slugs:
            leads.append(lead)
            existing_slugs.add(lead["institution_slug"])
            print(f"Appended lead: {lead['institution_slug']}")

    with open(leads_json, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    # Update last_scrape.json and scrape_log.json for each institution
    for slug, status, tender_count, doc_count in RESULTS:
        inst_path = inst_dir / slug
        if not inst_path.exists():
            inst_path.mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "run_id": RUN_ID,
            "slug": slug,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
            "scraped_at": NOW,
        }
        (inst_path / "last_scrape.json").write_text(
            json.dumps(last_scrape, indent=2), encoding="utf-8"
        )

        scrape_log_path = inst_path / "scrape_log.json"
        log_entries = []
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_entries = json.load(f)
        log_entries.append(
            {
                "run_id": RUN_ID,
                "slug": slug,
                "status": status,
                "tender_count": tender_count,
                "doc_count": doc_count,
                "scraped_at": NOW,
            }
        )
        with open(scrape_log_path, "w") as f:
            json.dump(log_entries, f, indent=2)

    print("Updated last_scrape.json and scrape_log.json for all 25 institutions.")


if __name__ == "__main__":
    main()
