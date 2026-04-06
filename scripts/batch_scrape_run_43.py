#!/usr/bin/env python3
"""Process scrape results for run_20260315_060430_batch43 - 25 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch43"
NOW = datetime.now(timezone.utc).isoformat()

# Scrape results: slug -> (status, tender_count, doc_count, error?)
RESULTS = {
    "globe": ("error", 0, 0, "503 Service Unavailable"),
    "globetrotters": ("no_tenders", 0, 0, None),
    "gncsolutions": ("no_tenders", 0, 0, None),
    "go-vacation": ("no_tenders", 0, 0, None),
    "gochconsult": ("no_tenders", 0, 0, None),
    "godwinattorneys": ("no_tenders", 0, 0, None),
    "gofinventures": ("no_tenders", 0, 0, None),
    "gogam": ("no_tenders", 0, 0, None),
    "goldeneagletravel": ("no_tenders", 0, 0, None),
    "goldenpot": ("no_tenders", 0, 0, None),
    "goldstarpaints": ("error", 0, 0, "Fetch timed out"),
    "goldzone": ("error", 0, 0, "500 Internal Server Error"),
    "gonuts": ("no_tenders", 0, 0, None),
    "gonuts4donuts": ("no_tenders", 0, 0, None),
    "goodlifereflexology": ("error", 0, 0, "Fetch timed out"),
    "goodsamaritan": ("no_tenders", 0, 0, None),
    "goproperty": ("no_tenders", 0, 0, None),
    "gordhangarage": ("no_tenders", 0, 0, None),
    "goshenischool": ("no_tenders", 0, 0, None),
    "gospelclinic": ("no_tenders", 0, 0, None),
    "gpitg": ("no_tenders", 0, 0, None),
    "gps": ("no_tenders", 0, 0, None),
    "grand": ("no_tenders", 0, 0, None),
    "grandhire": ("no_tenders", 0, 0, None),
    "granocoffee": ("error", 0, 0, "Account Suspended"),
}

# Institution metadata for new leads (slug -> (name, url)); emails extracted from README
INST_META = {
    "goodsamaritan": ("Good Samaritan English Medium School", "https://goodsamaritan.ac.tz/"),
    "goproperty": ("goproperty – property manager & Auctioneer", "https://goproperty.co.tz/"),
    "gordhangarage": ("Gordhan Garage", "https://www.gordhangarage.co.tz/"),
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
    leads_added = 0
    for slug, (status, tender_count, doc_count, err) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        if not inst_dir.exists():
            continue

        # last_scrape.json
        last = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
            "error": err,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2))

        # scrape_log.json - append
        log_path = inst_dir / "scrape_log.json"
        log_entries = []
        if log_path.exists():
            raw = json.loads(log_path.read_text())
            if isinstance(raw, list):
                log_entries = raw
            elif isinstance(raw, dict) and "runs" in raw:
                log_entries = raw["runs"]
            else:
                log_entries = [raw] if raw else []
        new_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
        }
        log_entries.append(new_entry)
        # Preserve structure: use list format (common) or runs wrapper
        out = log_entries
        log_path.write_text(json.dumps(out, indent=2))

        # Append new leads for goodsamaritan, goproperty, gordhangarage (not yet in leads.json)
        if slug in INST_META and status in ("no_tenders", "error"):
            import re
            name, url = INST_META[slug]
            emails = []
            readme = inst_dir / "README.md"
            if readme.exists():
                text = readme.read_text()
                found = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
                emails = list(dict.fromkeys([e for e in found if "example" not in e.lower()]))

            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": url,
                "emails": emails,
                "opportunity_type": "sell",
                "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": DRAFT_BODY.format(name=name),
                "created_at": NOW,
                "status": "pending",
            }
            leads_path = PROJECT / "opportunities" / "leads.json"
            leads = json.loads(leads_path.read_text())
            if not isinstance(leads, list):
                leads = leads.get("leads", [])
            # Avoid duplicate
            if not any(l.get("institution_slug") == slug for l in leads):
                leads.append(lead)
                leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False))
                leads_added += 1

        # Print summary
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    if leads_added:
        import subprocess
        subprocess.run(
            ["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")],
            cwd=str(PROJECT),
            check=True,
        )
        print(f"\nAppended {leads_added} new leads, ran sync_leads_csv.py")


if __name__ == "__main__":
    main()
