#!/usr/bin/env python3
"""Process scrape results for run_20260315_060430_batch90 - 25 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch90"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Scrape results: slug -> (status, tender_count, doc_count)
# status: success|error|no_tenders
# Based on fetch results: panganibasin/panganidc=error (timeout/SSL), parakito=error (suspended),
# parliament/pbpa/zppda=timeout, rest=no_tenders or success
RESULTS = [
    ("panganibasin", "error", 0, 0),      # Fetch timeout/SSL
    ("panganidc", "error", 0, 0),        # Fetch timeout/SSL
    ("pangisha", "no_tenders", 0, 0),    # Property site
    ("panita", "no_tenders", 0, 0),      # EOI 2021 closed
    ("panoceanic", "no_tenders", 0, 0),  # Insurance broker
    ("paragon", "no_tenders", 0, 0),     # Gem retailer
    ("parakito", "error", 0, 0),         # Account suspended
    ("parliament", "error", 0, 0),      # Fetch timeout
    ("pasada", "no_tenders", 0, 0),      # All tenders closed (2023-2024)
    ("pass", "no_tenders", 0, 0),        # RFPs closed (June 2025)
    ("passlease", "no_tenders", 0, 0),   # "No active tenders"
    ("patanditc", "no_tenders", 0, 0),   # Water Institute - no tenders
    ("patmosislandschool", "no_tenders", 0, 0),
    ("pattersongroup", "no_tenders", 0, 0),
    ("pawahost", "no_tenders", 0, 0),
    ("payless", "no_tenders", 0, 0),
    ("pbpa", "error", 0, 0),            # Fetch timeout
    ("pbz-bank", "error", 0, 0),         # ZPPDA timeout
    ("pbzbank", "no_tenders", 0, 0),     # Bank - tenders via ZPPDA
    ("pc", "no_tenders", 0, 0),          # Pharmacy Council - not available
    ("pcohas", "no_tenders", 0, 0),
    ("pctl", "no_tenders", 0, 0),
    ("peacetraveltz", "no_tenders", 0, 0),
    ("peerlink", "no_tenders", 0, 0),
    ("pegasuslegal", "no_tenders", 0, 0),
]

# Institutions needing NEW lead (not already in leads.json)
INST_CONFIG = {
    "panganibasin": ("PBWB | Mwanzo", "https://panganibasin.go.tz/", ["basins.pangani@panganibasin.go.tz"]),
    "panganidc": ("Pangani District Council", "https://panganidc.go.tz/", ["ded@panganidc.go.tz"]),
    "panita": ("PANITA", "https://panita.or.tz/", ["info@panita.co.tz", "info@panita.or.tz"]),
    "parliament": ("Bunge Tanzania", "https://parliament.go.tz/", ["cna@bunge.go.tz"]),
    "pasada": ("PASADA", "https://pasada.or.tz/", ["procurement@pasada.or.tz", "info@pasada.or.tz"]),
    "pass": ("PASS Trust", "https://pass.or.tz/", ["info@pass.or.tz"]),
    "passlease": ("PASS Leasing", "https://passlease.co.tz/", ["info@passlease.co.tz"]),
    "patanditc": ("Water Institute", "https://patanditc.ac.tz/", ["rector@waterinstitute.ac.tz"]),
    "pbpa": ("PBPA", "https://pbpa.go.tz/", ["info@pbpa.go.tz"]),
    "pbz-bank": ("Peoples Bank of Zanzibar", "http://www.tenders.zppda.go.tz/entities/view/peoples-bank-of-zanzibar-pbz", []),
    "pc": ("Pharmacy Council", "https://pc.go.tz/", ["barua@pc.go.tz", "info@pc.go.tz"]),
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
    # Load existing leads
    leads_path = PROJECT / "opportunities" / "leads.json"
    with open(leads_path) as f:
        leads = json.load(f)
    existing_slugs = {l["institution_slug"] for l in leads}

    # Process each institution
    for slug, status, tender_count, doc_count in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": "2026-03-16T06:00:00Z",
            "active_tenders_count": tender_count,
            "status": "success" if status != "error" else "error",
            "error": "Fetch timeout or site unavailable" if status == "error" else None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2))

        # scrape_log.json - append
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            log = json.loads(log_path.read_text())
        else:
            log = {"runs": []}
        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": "success" if status != "error" else "error",
            "tenders_found": tender_count,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [last_scrape["error"]] if last_scrape["error"] else [],
        })
        log_path.write_text(json.dumps(log, indent=2))

        # Add lead if no tenders and not in leads (for institutions that need new lead)
        if status in ("no_tenders", "error") and slug in INST_CONFIG and slug not in existing_slugs:
            name, url, emails = INST_CONFIG[slug]
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
            leads.append(lead)
            existing_slugs.add(slug)

        # Print RESULT line
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Save leads
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
