#!/usr/bin/env python3
"""Process 25 institutions for run_20260315_060430_batch56 - update scrape state and leads."""
import json
import os
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch56"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

INSTITUTIONS = [
    ("joeladvocates", "https://joeladvocates.co.tz/", 0, 0, "no_tenders"),
    ("joglo", "https://joglo.co.tz/", 0, 0, "no_tenders"),
    ("johatrust", "https://www.johatrust.ac.tz/", 0, 0, "no_tenders"),
    ("johmsasuperforce", "https://johmsasuperforce.co.tz/", 0, 0, "no_tenders"),
    ("jollie", "https://jollie.co.tz/", 0, 0, "no_tenders"),
    ("jonzlogistics", "http://jonzlogistics.co.tz/", 0, 0, "no_tenders"),
    ("jpglobalco", "https://jpglobalco.co.tz/", 0, 0, "no_tenders"),
    ("jpgroup", "https://jpgroup.co.tz/", 0, 0, "no_tenders"),
    ("jselectromec", "https://jselectromec.co.tz/", 0, 0, "no_tenders"),
    ("jt-consulting", "https://jt-consulting.co.tz/", 0, 0, "no_tenders"),
    ("jtelimited", "https://jtelimited.co.tz/", 0, 0, "no_tenders"),
    ("jtsltd", "https://jtsltd.co.tz/", 0, 0, "no_tenders"),
    ("juco", "https://juco.ac.tz/", 0, 0, "no_tenders"),
    ("judiciary", "https://judiciary.go.tz/", 0, 0, "no_tenders"),  # Table shows "No Recent Data!"
    ("judiciaryzanzibar", "https://judiciaryzanzibar.go.tz/", 0, 0, "no_tenders"),
    ("jumanjiwildlife", "https://jumanjiwildlife.co.tz/", 0, 0, "no_tenders"),
    ("jumbo", "https://jumbo.co.tz/", 0, 0, "no_tenders"),
    ("jumintech", "https://jumintech.co.tz/", 0, 0, "no_tenders"),
    ("junaco", "http://www.junacogroup.com/", 0, 0, "no_tenders"),
    ("jvaa", "https://jvaa.co.tz/", 0, 0, "no_tenders"),
    ("jvspek", "https://jvspek.co.tz/", 0, 0, "no_tenders"),
    ("jwempo", "https://jwempo.ac.tz/", 0, 0, "no_tenders"),
    ("jwt", "https://jwt.or.tz/", 0, 0, "no_tenders"),
    ("k2technology", "https://k2technology.co.tz/", 0, 0, "no_tenders"),
    ("kacce", "https://kacce.or.tz/", 0, 0, "no_tenders"),
]

# Institutions NOT yet in leads.json - need to append
NEW_LEADS_SLUGS = {"jonzlogistics", "jpglobalco", "jtsltd", "juco", "junaco", "jvaa", "jvspek", "jwempo"}

# Lead template from zima README
LEAD_TEMPLATE = {
    "opportunity_type": "sell",
    "opportunity_description": "No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
    "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & {name}",
    "draft_email_body": "Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
    "status": "pending",
}

# Name mapping for new leads
INST_NAMES = {
    "jonzlogistics": "JONZ Express Logistics",
    "jpglobalco": "J & P GLOBAL ROLL COMPANY LIMITED",
    "jtsltd": "Jendele Technology Solutions Company LTD",
    "juco": "Jordan University College",
    "junaco": "JUNACO",
    "jvaa": "JV ADVISORY & ADVOCATES",
    "jvspek": "JV SPEK",
    "jwempo": "Journal of Water Resources, Engineering, Management and Policy",
}

INST_EMAILS = {
    "jonzlogistics": ["johnes.mukyanuzi@jonzlogistics.co.tz", "info@jonzlogistics.co.tz"],
    "jpglobalco": [],
    "jtsltd": ["info@kodeforest.com"],
    "juco": ["admission@juco.ac.tz", "info@juco.ac.tz"],
    "junaco": ["info@junacogroup.com"],
    "jvaa": ["info@jvaa.co.tz"],
    "jvspek": ["info@spek.co.tz"],
    "jwempo": [],
}


def main():
    results = []
    for slug, url, tender_count, doc_count, status in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "documents_downloaded": doc_count,
            "status": "success" if status != "error" else "error",
            "error": None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2))

        scrape_log_path = inst_dir / "scrape_log.json"
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": "success",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "tender_ids": [],
            "errors": [],
        }
        if scrape_log_path.exists():
            data = json.loads(scrape_log_path.read_text())
            runs = data.get("runs", [])
            runs.append(log_entry)
            data["runs"] = runs[-50:]  # Keep last 50
        else:
            data = {"runs": [log_entry]}
        scrape_log_path.write_text(json.dumps(data, indent=2))

        results.append((slug, status, tender_count, doc_count))

    # Append new leads
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        leads = json.loads(leads_path.read_text())
    existing_slugs = {l.get("institution_slug") for l in leads}

    for slug in NEW_LEADS_SLUGS:
        if slug in existing_slugs:
            continue
        name = INST_NAMES.get(slug, slug.replace("-", " ").title())
        url = next((u for s, u, _, _, _ in INSTITUTIONS if s == slug), "")
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": INST_EMAILS.get(slug, []),
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": f"Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": NOW,
            "status": "pending",
        }
        leads.append(lead)

    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False))

    # Run sync
    os.chdir(PROJECT)
    import subprocess
    subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True)

    # Print RESULT lines
    for slug, status, tc, dc in results:
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")


if __name__ == "__main__":
    main()
