#!/usr/bin/env python3
"""
Scrape 25 institutions (batch 16): bmtelecomms through bradda.
Updates last_scrape.json, scrape_log.json; appends leads when no tenders; runs sync.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch16"
NOW = datetime.now(timezone.utc).isoformat()

INSTITUTIONS = [
    {"slug": "bmtelecomms", "name": "BM Telecomms", "url": "https://bmtelecomms.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bmz", "name": "ZEC (BMZ)", "url": "https://eprocurement.zppda.go.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Fetch timed out"},
    {"slug": "bnc", "name": "BNC", "url": "https://bnc.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bnhchs", "name": "BNHCHS", "url": "https://bnhchs.ac.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bnmgeneral", "name": "BNM GENERAL", "url": "http://bnmgeneral.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "boatanzania", "name": "Bank of Africa Tanzania", "url": "https://boatanzania.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "boavida", "name": "Boavida", "url": "https://boavida.co.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Fetch timed out"},
    {"slug": "bobgrow", "name": "BOB-GROW", "url": "https://bobgrow.co.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Fetch timed out"},
    {"slug": "bogach", "name": "BOGACH Finance", "url": "https://bogach.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "boitanzania", "name": "BOI Tanzania", "url": "https://boitanzania.co.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "reCAPTCHA/Cloudflare blocked"},
    {"slug": "bongonews", "name": "Bongo News", "url": "https://bongonews.co.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Fetch timed out"},
    {"slug": "bongovip", "name": "BongoVIP", "url": "https://bongovip.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "boraagrica", "name": "BORA Kilimo", "url": "https://www.boraagrica.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "borderless", "name": "Borderless Solutions", "url": "https://borderless.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bosch-professional", "name": "Bosch Professional", "url": "https://www.bosch-professional.com/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bosch-pt", "name": "Bosch Power Tools", "url": "https://www.bosch-pt.com/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "boss", "name": "Boss Limited", "url": "https://boss.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "boston", "name": "Boston City Campus", "url": "https://www.boston.ac.za/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bot", "name": "Bank of Tanzania", "url": "https://www.bot.go.tz/CallsforTender", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bpc", "name": "Brain Power Consultancy", "url": "https://bpc.co.tz/services.php", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bphacoh", "name": "BPHACOH", "url": "https://bphacoh.ac.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bpra", "name": "BPRA", "url": "https://www.bpra.go.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "brac-etender", "name": "BRAC e-Tender", "url": "https://tender.brac.net/", "tenders": 0, "docs": 0, "status": "error", "error": "Fetch timed out"},
    {"slug": "brac-tanzania", "name": "BRAC Tanzania", "url": "https://procurement.brac.net/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "bradda", "name": "Bradda", "url": "https://bradda.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
]

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


def get_emails_from_readme(slug: str) -> list:
    """Extract emails from institution README contact section."""
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return []
    text = readme.read_text(encoding="utf-8")
    emails = []
    import re
    for m in re.finditer(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
        e = m.group(0).lower()
        if e not in emails and "example" not in e and "png" not in e and "jpg" not in e:
            emails.append(e)
    return emails[:5]  # cap at 5


def ensure_dirs(inst_dir: Path):
    for d in ["tenders/active", "tenders/closed", "tenders/archive", "downloads"]:
        (inst_dir / d).mkdir(parents=True, exist_ok=True)


def main():
    results = []
    leads_to_append = []

    for inst in INSTITUTIONS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        ensure_dirs(inst_dir)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW,
            "active_tenders_count": inst["tenders"],
            "status": "success" if inst["error"] is None else "error",
            "error": inst["error"],
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")

        # scrape_log.json - append run
        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            scrape_log = json.loads(scrape_log_path.read_text(encoding="utf-8"))
        else:
            scrape_log = {"runs": []}
        run_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": "success" if inst["error"] is None else "error",
            "tenders_found": inst["tenders"],
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": inst["docs"],
            "errors": [inst["error"]] if inst["error"] else [],
        }
        scrape_log["runs"].append(run_entry)
        scrape_log_path.write_text(json.dumps(scrape_log, indent=2), encoding="utf-8")

        # Lead for no_tenders (skip if already in leads)
        if inst["status"] == "no_tenders" or inst["error"]:
            emails = get_emails_from_readme(slug)
            lead = {
                "institution_slug": slug,
                "institution_name": inst["name"],
                "website_url": inst["url"],
                "emails": emails,
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {inst['name']} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
                "draft_email_body": DRAFT_BODY.format(name=inst["name"]),
                "created_at": NOW,
                "status": "pending",
            }
            leads_to_append.append(lead)

        status = inst["status"] if inst["status"] != "no_tenders" else "no_tenders"
        results.append((slug, status, inst["tenders"], inst["docs"]))

    # Append new leads only if slug not already in leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    existing_slugs = set()
    if leads_path.exists():
        data = json.loads(leads_path.read_text(encoding="utf-8"))
        leads_list = data if isinstance(data, list) else data.get("leads", [])
        existing_slugs = {l.get("institution_slug") for l in leads_list}
    else:
        leads_list = []

    appended = 0
    for lead in leads_to_append:
        if lead["institution_slug"] not in existing_slugs:
            leads_list.append(lead)
            existing_slugs.add(lead["institution_slug"])
            appended += 1

    if appended > 0:
        leads_path.write_text(json.dumps(leads_list, indent=2, ensure_ascii=False), encoding="utf-8")

    # Sync CSV
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        os.chdir(PROJECT)
        os.system(f"python3 {sync_script}")

    # Print summary
    print("\n" + "=" * 60)
    print(f"TENDER SCRAPE BATCH 16 — {RUN_ID}")
    print("=" * 60)
    for slug, status, tender_count, doc_count in results:
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
    print("=" * 60)
    print(f"Total: {len(results)} institutions | Leads appended: {appended}")
    print("=" * 60)


if __name__ == "__main__":
    main()
