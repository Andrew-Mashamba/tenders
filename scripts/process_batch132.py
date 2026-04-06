#!/usr/bin/env python3
"""Process run_20260315_060430_batch132 - update last_scrape, scrape_log, add missing leads."""
import json
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch132"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# Scrape results: slug -> (status, tender_count, doc_count)
# status: success|error|blocked|no_tenders
RESULTS = [
    ("wildaftanzania", "no_tenders", 0, 0),
    ("wildernessencounters", "error", 0, 0),  # timeout
    ("wildernessexpedition", "no_tenders", 0, 0),
    ("willy", "error", 0, 0),  # account suspended
    ("winglink", "no_tenders", 0, 0),
    ("winnet", "no_tenders", 0, 0),
    ("wintender", "blocked", 0, 0),  # login required
    ("winther", "no_tenders", 0, 0),
    ("wipahs", "no_tenders", 0, 0),
    ("wisefutures", "no_tenders", 0, 0),
    ("wizdon", "no_tenders", 0, 0),
    ("wleetngo", "no_tenders", 0, 0),
    ("wma", "no_tenders", 0, 0),
    ("wmpso", "no_tenders", 0, 0),
    ("wodsta", "no_tenders", 0, 0),
    ("wonderland", "no_tenders", 0, 0),
    ("worf", "no_tenders", 0, 0),
    ("workforce", "no_tenders", 0, 0),
    ("workoutzone", "no_tenders", 0, 0),
    ("world-vision-global", "no_tenders", 0, 0),
    ("world-vision-tanzania", "error", 0, 0),  # timeout
    ("worldoil", "no_tenders", 0, 0),
    ("wrifom", "no_tenders", 0, 0),
    ("wrrb", "error", 0, 0),  # timeout
    ("wsphelp", "no_tenders", 0, 0),
]

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def main():
    for slug, status, tender_count, doc_count in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        ensure_dir(inst_dir)
        ensure_dir(inst_dir / "tenders" / "active")
        ensure_dir(inst_dir / "tenders" / "closed")
        ensure_dir(inst_dir / "downloads")

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW,
            "active_tenders_count": tender_count,
            "status": "success" if status in ("no_tenders", "success") else "error",
            "error": None if status != "error" else "Site timeout/blocked",
            "run_id": RUN_ID,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2))

        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            log = json.loads(scrape_log_path.read_text())
        else:
            log = {"runs": []}
        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 5,
            "status": "success" if status in ("no_tenders", "success") else "error",
            "tenders_found": tender_count,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [] if status != "error" else ["Site timeout or blocked"],
        })
        scrape_log_path.write_text(json.dumps(log, indent=2))

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Add missing leads: wrrb, world-vision-tanzania
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = json.loads(leads_path.read_text()) if leads_path.exists() else []
    slugs_in_leads = {l.get("institution_slug") for l in leads}

    new_leads = []
    if "wrrb" not in slugs_in_leads:
        new_leads.append({
            "institution_slug": "wrrb",
            "institution_name": "WRRB - Water Resources Regulatory Board",
            "website_url": "https://wrrb.go.tz/",
            "emails": [],
            "opportunity_type": "sell",
            "opportunity_description": "Site timed out. WRRB is government water regulator. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & WRRB",
            "draft_email_body": "Dear WRRB Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support WRRB. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": NOW,
            "status": "pending",
        })
    if "world-vision-tanzania" not in slugs_in_leads:
        new_leads.append({
            "institution_slug": "world-vision-tanzania",
            "institution_name": "World Vision Tanzania",
            "website_url": "https://www.wvi.org/tanzania/tenders",
            "emails": [],
            "opportunity_type": "sell",
            "opportunity_description": "Site timed out. World Vision Tanzania posts tenders. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & World Vision Tanzania",
            "draft_email_body": "Dear World Vision Tanzania Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support World Vision Tanzania. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": NOW,
            "status": "pending",
        })

    if new_leads:
        leads.extend(new_leads)
        leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False))
        print(f"\nAdded {len(new_leads)} new leads: {[l['institution_slug'] for l in new_leads]}")

if __name__ == "__main__":
    main()
