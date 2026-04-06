#!/usr/bin/env python3
"""Regenerate opportunities/leads.csv from opportunities/leads.json."""
import csv
import json
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"
LEADS_CSV = PROJECT / "opportunities" / "leads.csv"

HEADERS = [
    "institution_slug", "institution_name", "website_url", "emails",
    "opportunity_type", "opportunity_description", "draft_email_subject",
    "draft_email_body", "created_at", "status",
]


def main():
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    with open(LEADS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        for lead in leads:
            emails = "; ".join(lead.get("emails", []))
            w.writerow([
                lead.get("institution_slug", ""),
                lead.get("institution_name", ""),
                lead.get("website_url", ""),
                emails,
                lead.get("opportunity_type", ""),
                lead.get("opportunity_description", ""),
                lead.get("draft_email_subject", ""),
                lead.get("draft_email_body", ""),
                lead.get("created_at", ""),
                lead.get("status", "pending"),
            ])


if __name__ == "__main__":
    main()
