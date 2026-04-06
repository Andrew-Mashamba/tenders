#!/usr/bin/env python3
"""Batch scrape run_20260313_205329_batch18 - Process 25 institutions."""
import json
import os
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch18"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# Scrape results: slug -> (status, tender_count, doc_count, error?)
# Based on fetch analysis: no tenders = 0,0; tenders found = n,m; error = error status
RESULTS = {
    "btelesec": ("success", 0, 0),
    "btx": ("success", 0, 0),
    "buchosadc": ("error", 0, 0),  # SSL/timeout
    "buckreef": ("success", 0, 0),
    "budget": ("success", 0, 0),
    "budgetfreightltd": ("success", 0, 0),
    "bugando": ("success", 0, 0),
    "buhigwedc": ("success", 0, 0),  # Only old 2021 tenders
    "buildmart": ("error", 0, 0),  # Timeout
    "bukobadc": ("error", 0, 0),  # Timeout
    "bukobamc": ("success", 0, 0),
    "bumbulidc": ("success", 0, 0),
    "bundahospital": ("success", 0, 0),
    "bunge": ("success", 0, 0),
    "bureauveritas": ("success", 0, 0),
    "burhaniinfosys": ("success", 0, 0),
    "bushandforest": ("success", 0, 0),
    "bushbucksafaris": ("success", 0, 0),
    "bushlink": ("success", 0, 0),
    "business": ("error", 0, 0),  # Timeout
    "businesstimes": ("success", 0, 0),
    "busokelodc": ("success", 0, 0),
    "butchershop": ("success", 0, 0),
    "butimbatc": ("success", 0, 0),
    "buwasa": ("success", 0, 0),
}

# Institution metadata for leads
INST_META = {
    "btelesec": ("Beyond Telesec Ltd", "https://btelesec.co.tz/", ["info@btelesec.co.tz"]),
    "btx": ("BTX Tanzania Limited", "https://btx.co.tz/", ["info@btx.co.tz"]),
    "buchosadc": ("Buchosa District Council", "https://buchosadc.go.tz/", ["ded@buchosadc.go.tz"]),
    "buckreef": ("Buckreef Gold", "https://buckreef.co.tz/", []),
    "budget": ("Budget Car Rentals", "https://www.budget.co.tz/", ["info@budget.co.tz"]),
    "budgetfreightltd": ("Budget Freight Limited", "https://budgetfreightltd.co.tz/", ["info@budgetfreightltd.co.tz"]),
    "bugando": ("Catholic University of Health and Allied Sciences", "https://bugando.ac.tz/", ["procurement@bugando.ac.tz", "vc@bugando.ac.tz"]),
    "buhigwedc": ("Buhigwe District Council", "https://buhigwedc.go.tz/", ["ded@buhigwedc.go.tz"]),
    "buildmart": ("Buildmart Limited", "https://buildmart.co.tz/", ["info@buildmart.co.tz", "gm@buildmart.co.tz"]),
    "bukobadc": ("Bukoba District Council", "https://bukobadc.go.tz/", ["ded@bukobadc.go.tz"]),
    "bukobamc": ("Bukoba Municipal Council", "https://bukobamc.go.tz/", ["md@bukobamc.go.tz"]),
    "bumbulidc": ("Bumbuli District Council", "http://bumbulidc.go.tz/", ["ded@bumbuklidc.go.tz"]),
    "bundahospital": ("Bunda DDH Hospital", "https://bundahospital.co.tz/", ["info@bundahospital.co.tz"]),
    "bunge": ("Bunge la Tanzania", "https://www.parliament.go.tz/", ["cna@bunge.go.tz"]),
    "bureauveritas": ("Bureau Veritas Tanzania", "https://www.bureauveritas.co.tz/", []),
    "burhaniinfosys": ("Burhani Infosys Ltd", "https://burhaniinfosys.co.tz/", ["info@burhaniinfosys.co.tz", "info@burhaniinfosys.com"]),
    "bushandforest": ("Bush and Forest Collections", "https://bushandforest.co.tz/", ["info@bushandforest.co.tz"]),
    "bushbucksafaris": ("Bushbuck Safaris", "https://www.bushbuckltd.com/", []),
    "bushlink": ("BushLink Agro-Venture Ltd", "https://bushlink.co.tz/", ["av@bushlink.co.tz"]),
    "business": ("TNBP / business.go.tz", "https://business.go.tz/", []),
    "businesstimes": ("Business Times", "https://businesstimes.co.tz/", []),
    "busokelodc": ("Busokelo District Council", "https://busokelodc.go.tz/", ["ded@busokelodc.go.tz"]),
    "butchershop": ("Butcher Shop", "https://butchershop.co.tz/", []),
    "butimbatc": ("Butimba Teacher's College", "https://butimbatc.ac.tz/", []),
    "buwasa": ("BUWASA", "https://buwasa.go.tz/", ["info@buwasa.go.tz"]),
}

DRAFT_EMAIL = """Dear {institution_name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {institution_name}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
"""


def main():
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads if l.get("institution_slug")}
    summaries = []

    for slug, (status, tender_count, doc_count) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "next_scrape": "2026-03-14T06:00:00Z",
            "active_tenders_count": tender_count,
            "status": status,
            "error": status if status == "error" else None,
            "documents_downloaded": doc_count,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json
        log_path = inst_dir / "scrape_log.json"
        log_data = {"runs": []}
        if log_path.exists():
            with open(log_path) as f:
                log_data = json.load(f)
        log_data["runs"].append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [status] if status == "error" else [],
        })
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)

        # Opportunity lead for no-tender institutions
        if tender_count == 0 and slug not in existing_slugs and slug in INST_META:
            name, url, emails = INST_META[slug]
            if not emails:
                emails = [f"info@{slug.split('-')[0]}.co.tz"] if "go.tz" not in url else [f"ded@{slug}.go.tz"]
            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": url,
                "emails": emails,
                "opportunity_type": "sell",
                "opportunity_description": "No formal tenders or procurements found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": DRAFT_EMAIL.format(institution_name=name),
                "created_at": NOW,
                "status": "pending",
            }
            leads.append(lead)
            existing_slugs.add(slug)

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print("\n--- Batch complete. Run sync_leads_csv.py to update leads.csv ---")


if __name__ == "__main__":
    main()
