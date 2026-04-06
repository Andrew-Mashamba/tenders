#!/usr/bin/env python3
"""Append leads for batch10 institutions that had errors or need opportunity capture."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# New leads for institutions with errors (site down/offline) - only add if not already present
NEW_LEADS = [
    {
        "institution_slug": "ask",
        "institution_name": "Ask Website",
        "website_url": "https://ask.or.tz/",
        "emails": [],
        "opportunity_type": "sell",
        "opportunity_description": "Site https://ask.or.tz/ offline/maintenance. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services when site is back.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Ask",
        "draft_email_body": "Dear Ask Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support Ask. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "asa",
        "institution_name": "Agricultural Seed Agency",
        "website_url": "https://asa.go.tz/",
        "emails": ["info@asa.go.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Site https://asa.go.tz/ timed out. ZIMA Solutions could offer digital transformation for government agencies.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & ASA",
        "draft_email_body": "Dear ASA Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions, government agencies, and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support ASA. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "atc",
        "institution_name": "Arusha Technical College",
        "website_url": "https://atc.ac.tz/",
        "emails": ["rector@atc.ac.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Site https://atc.ac.tz/ timed out. ATC has procurement documents - ZIMA could offer tender notification or procurement system.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Arusha Technical College",
        "draft_email_body": "Dear Arusha Technical College Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your procurement activities and believe we could support your technology goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support ATC. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
]

# Actually arushameat has 1 tender - we should NOT add leads for institutions with tenders.
# Per instruction: "If NO tenders or procurements found" - add lead. So remove arushameat from NEW_LEADS.
# Keep ask, asa, atc. ask.tz - same URL as ask, skip duplicate.
def main():
    with open(LEADS_JSON) as f:
        leads = json.load(f)
    existing = {l["institution_slug"] for l in leads}
    to_add = [l for l in NEW_LEADS if l["institution_slug"] not in existing]
    if to_add:
        leads.extend(to_add)
        with open(LEADS_JSON, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        print(f"Appended {len(to_add)} leads: {[l['institution_slug'] for l in to_add]}")
    else:
        print("No new leads to append")


if __name__ == "__main__":
    main()
