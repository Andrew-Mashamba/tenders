#!/usr/bin/env python3
"""Append missing leads for 7skiesenterprises, abitat, ableservices."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"

NEW_LEADS = [
    {
        "institution_slug": "7skiesenterprises",
        "institution_name": "7 Skies Enterprises",
        "website_url": "https://7skiesenterprises.co.tz/",
        "emails": ["webmaster@7skiesenterprises.co.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Site suspended. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services when site is restored.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & 7 Skies Enterprises",
        "draft_email_body": "Dear 7 Skies Enterprises Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support 7 Skies Enterprises. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
        "status": "pending",
    },
    {
        "institution_slug": "abitat",
        "institution_name": "TAGBI / Tanzania and Global Business Initiatives",
        "website_url": "https://abitat.or.tz/",
        "emails": [],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found on TAGBI website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & TAGBI",
        "draft_email_body": "Dear TAGBI Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support TAGBI. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
        "status": "pending",
    },
    {
        "institution_slug": "ableservices",
        "institution_name": "Able Services",
        "website_url": "https://www.ableservices.co.tz/",
        "emails": ["info@ableservices.co.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found on Able Services website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Able Services",
        "draft_email_body": "Dear Able Services Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support Able Services. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
        "status": "pending",
    },
]

def main():
    with open(LEADS_JSON) as f:
        leads = json.load(f)
    existing = {l["institution_slug"] for l in leads}
    added = 0
    for lead in NEW_LEADS:
        if lead["institution_slug"] not in existing:
            leads.append(lead)
            existing.add(lead["institution_slug"])
            added += 1
    if added:
        with open(LEADS_JSON, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        added_slugs = [l["institution_slug"] for l in NEW_LEADS if l["institution_slug"] in existing]
        print(f"Appended {added} new leads")
    else:
        print("All leads already exist.")

if __name__ == "__main__":
    main()
