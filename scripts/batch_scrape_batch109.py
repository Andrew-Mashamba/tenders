#!/usr/bin/env python3
"""Process scrape results for run_20260315_060430_batch109 - 25 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch109"
NOW = datetime.now(timezone.utc).isoformat()

# Results from manual scrape
RESULTS = [
    # (slug, status, tender_count, doc_count, error?)
    ("spicenet", "error", 0, 0, "README not found"),
    ("spidertours", "no_tenders", 0, 0, None),
    ("spiknspan", "no_tenders", 0, 0, None),
    ("spil", "error", 0, 0, "README not found"),
    ("spinandwin", "no_tenders", 0, 0, None),
    ("splashmedia", "no_tenders", 0, 0, None),  # Facebook - no tenders
    ("sportpesa", "error", 0, 0, "README not found"),
    ("sportspesa", "error", 0, 0, "README not found"),
    ("spotify", "error", 0, 0, "README not found"),
    ("spotileo", "error", 0, 0, "README not found"),
    ("sprf", "no_tenders", 0, 0, None),
    ("springtech", "error", 0, 0, "README not found"),
    ("sprinters", "no_tenders", 0, 0, None),
    ("srilanka", "error", 0, 0, "Account suspended"),
    ("srl", "error", 0, 0, "README not found"),
    ("sstapes", "error", 0, 0, "Account suspended"),
    ("st-jbcottolengo", "error", 0, 0, "README not found"),
    ("st-thomasnyabula", "success", 2, 2, None),  # Existing tenders
    ("stamico", "error", 0, 0, "README not found"),
    ("stamigold", "error", 0, 0, "Tender URL 404"),
    ("standard-chartered", "no_tenders", 0, 0, None),
    ("stanha", "no_tenders", 0, 0, None),
    ("stanthonys", "error", 0, 0, "README not found"),
    ("starattorneys", "error", 0, 0, "README not found"),
    ("starcity", "error", 0, 0, "README not found"),
]

# Institutions needing new leads (no tenders, not yet in leads)
NEW_LEADS = [
    {
        "institution_slug": "srilanka",
        "institution_name": "Account Suspended (srilanka.co.tz)",
        "website_url": "https://srilanka.co.tz/",
        "emails": ["webmaster@srilanka.co.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Site suspended. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services when site is restored.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions",
        "draft_email_body": "Dear Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support your organisation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "sstapes",
        "institution_name": "Account Suspended (sstapes.co.tz)",
        "website_url": "https://sstapes.co.tz/",
        "emails": ["webmaster@sstapes.co.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Site suspended. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services when site is restored.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions",
        "draft_email_body": "Dear Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support your organisation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "stamigold",
        "institution_name": "STAMIGOLD Company Limited",
        "website_url": "https://stamigold.co.tz/",
        "emails": ["info@stamigold.co.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found. Mining company with procurement department. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & STAMIGOLD",
        "draft_email_body": "Dear STAMIGOLD Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support STAMIGOLD. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
]


def main():
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}

    # Append new leads
    for lead in NEW_LEADS:
        if lead["institution_slug"] not in existing_slugs:
            leads.append(lead)
            existing_slugs.add(lead["institution_slug"])
            print(f"Added lead: {lead['institution_slug']}")

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    # Update each institution's last_scrape.json and scrape_log.json
    for slug, status, tender_count, doc_count, err in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        if not inst_dir.exists():
            inst_dir.mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "documents_downloaded": doc_count,
            "status": "success" if status in ("success", "no_tenders") else "error",
            "error": err,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": status,
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "error": err,
        }
        scrape_log = inst_dir / "scrape_log.json"
        log_runs = []
        if scrape_log.exists():
            with open(scrape_log) as f:
                data = json.load(f)
                log_runs = data.get("runs", data) if isinstance(data, dict) else data
        log_runs.append(log_entry)
        with open(scrape_log, "w") as f:
            json.dump({"runs": log_runs[-100:]}, f, indent=2)  # Keep last 100

        # Print summary
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Run sync_leads_csv
    import subprocess
    subprocess.run(
        ["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=str(PROJECT),
        check=True,
    )
    print("Synced leads.csv")


if __name__ == "__main__":
    main()
