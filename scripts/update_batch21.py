#!/usr/bin/env python3
"""Update scrape states and add leads for run_20260315_060430_batch21."""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch21"

# Scrape results: (slug, status, tender_count, doc_count)
RESULTS = [
    ("cgscollateral", "success", 0, 0),
    ("chadema", "success", 0, 0),
    ("chafils", "success", 0, 0),
    ("chaibora", "error", 0, 0),  # timeout
    ("chaliwasa", "error", 0, 0),  # timeout
    ("chandoconsultants", "success", 0, 0),
    ("chap", "success", 0, 0),
    ("chapakazi", "success", 0, 0),
    ("chapalink", "error", 0, 0),  # timeout
    ("chatocolleges", "success", 0, 0),
    ("chatozrh", "error", 0, 0),  # 500 or timeout
    ("chavita", "success", 0, 0),
    ("chayiloilfield", "success", 0, 0),
    ("cheche", "success", 0, 0),
    ("cheerstour", "success", 0, 0),
    ("chemchemsafari", "success", 0, 0),
    ("chemicotex", "success", 0, 0),
    ("chessleague", "error", 0, 0),  # timeout
    ("chi-temu", "success", 0, 0),
    ("chiefbaru", "success", 0, 0),
    ("childrencompanion", "error", 0, 0),  # timeout
    ("childrenconcern", "success", 0, 0),
    ("chilliandlime", "error", 0, 0),  # timeout
    ("chilunga", "success", 0, 0),
    ("chinadashengbank", "success", 1, 1),  # has EOI tender
]

# New leads to add (not already in leads.json)
NEW_LEADS = [
    {
        "institution_slug": "chaliwasa",
        "institution_name": "CHALIWASA",
        "website_url": "https://chaliwasa.go.tz/",
        "emails": [],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found on CHALIWASA (water utility) website. ZIMA Solutions could offer digital transformation, GePG, or ICT for utility billing.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & CHALIWASA",
        "draft_email_body": "Dear CHALIWASA Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support CHALIWASA. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    },
    {
        "institution_slug": "chapakazi",
        "institution_name": "Chapakazi",
        "website_url": "https://chapakazi.co.tz/",
        "emails": [],
        "opportunity_type": "partner",
        "opportunity_description": "No formal tenders found. Chapakazi offers Bulk SMS platform. ZIMA could partner on SMS/API integrations.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Chapakazi",
        "draft_email_body": "Dear Chapakazi Team,\n\nZIMA Solutions Limited specialises in digital transformation and API integrations. We noticed your Bulk SMS platform and believe we could explore partnership opportunities.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• API Gateway and integrations\n• AI-powered customer engagement\n\nWe would welcome a conversation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    },
    {
        "institution_slug": "chapalink",
        "institution_name": "Chapa Link",
        "website_url": "https://chapalink.com/",
        "emails": [],
        "opportunity_type": "partner",
        "opportunity_description": "No formal tenders found. Chapa Link offers website services. ZIMA could partner on web/ICT projects.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Chapa Link",
        "draft_email_body": "Dear Chapa Link Team,\n\nZIMA Solutions Limited specialises in digital transformation. We noticed your website services and believe we could explore partnership opportunities.\n\nWe would welcome a conversation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    },
    {
        "institution_slug": "chatozrh",
        "institution_name": "Chato Zonal Referral Hospital",
        "website_url": "https://chatozrh.go.tz/procurement",
        "emails": ["chatozrh@afya.go.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "Procurement page exists but returned error. ZIMA could offer healthcare ICT, GePG, or digital systems.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Chato ZRH",
        "draft_email_body": "Dear Chato Zonal Referral Hospital Team,\n\nZIMA Solutions Limited specialises in digital transformation for institutions. We noticed your procurement page and believe we could support your technology goals.\n\nOur offerings include:\n• GePG integration\n• Healthcare/Zahanati systems\n• HR and management systems\n\nWe would welcome a conversation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    },
    {
        "institution_slug": "childrenconcern",
        "institution_name": "Children Concern Foundation",
        "website_url": "https://www.childrenconcern.or.tz/",
        "emails": ["childrenconcern@outlook.com", "childrenconcern6@gmail.com"],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found. NGO - ZIMA could offer digital systems for donor management, HR.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Children Concern Foundation",
        "draft_email_body": "Dear Children Concern Foundation Team,\n\nZIMA Solutions Limited specialises in digital transformation for organisations. We noticed your foundation and believe we could support your technology goals.\n\nWe would welcome a conversation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    },
    {
        "institution_slug": "chilliandlime",
        "institution_name": "Chilli and Lime",
        "website_url": "https://chilliandlime.co.tz/",
        "emails": [],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found. Site timed out. ZIMA could offer digital transformation.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Chilli and Lime",
        "draft_email_body": "Dear Chilli and Lime Team,\n\nZIMA Solutions Limited specialises in digital transformation. We would welcome a conversation about how we might support your organisation.\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    },
]


def main():
    run_start = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    for slug, status, tender_count, doc_count in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        last = {
            "institution": slug,
            "last_scrape": run_start,
            "next_scrape": run_start,
            "active_tenders_count": tender_count,
            "status": status,
            "error": None if status == "success" else "fetch_timeout_or_error",
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

        log_path = inst_dir / "scrape_log.json"
        log_data = {"runs": []}
        if log_path.exists():
            try:
                log_data = json.loads(log_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        log_data["runs"] = log_data.get("runs", []) + [{
            "run_id": RUN_ID,
            "timestamp": run_start,
            "status": status,
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [] if status == "success" else ["fetch_timeout_or_error"],
        }]
        log_path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Append new leads
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = json.loads(leads_path.read_text(encoding="utf-8"))
    existing_slugs = {l["institution_slug"] for l in leads}
    for lead in NEW_LEADS:
        if lead["institution_slug"] not in existing_slugs:
            leads.append(lead)
            existing_slugs.add(lead["institution_slug"])
            print(f"ADDED_LEAD|{lead['institution_slug']}")
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

    # Sync CSV
    subprocess.run(
        [sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=PROJECT,
        check=True,
    )
    print("SYNCED leads.csv")


if __name__ == "__main__":
    main()
