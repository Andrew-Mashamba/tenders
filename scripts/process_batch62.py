#!/usr/bin/env python3
"""
Process scrape results for batch62 - 25 institutions.
Based on fetch results: most have no tenders; kitetodc may have tenders but site unreachable.
"""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch62"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Scrape results: slug -> (status, tender_count, doc_count, error?)
# status: success|no_tenders|error
# Based on fetch: kitetodc/kitikai/kitotech/kitukiblu/kividea/kiwaleis/kliktech = timeout/unreachable
RESULTS = {
    "kitetodc": ("error", 0, 0, "Site unreachable (SSL/timeout)"),
    "kitikai": ("error", 0, 0, "Fetch timeout"),
    "kitm": ("no_tenders", 0, 0, None),
    "kitotech": ("error", 0, 0, "Fetch timeout"),
    "kitukiblu": ("error", 0, 0, "Fetch timeout"),
    "kiut": ("no_tenders", 0, 0, None),
    "kividea": ("error", 0, 0, "Fetch timeout"),
    "kivulini": ("no_tenders", 0, 0, None),
    "kiwaleis": ("error", 0, 0, "Fetch timeout"),
    "kiwamwaku": ("no_tenders", 0, 0, None),
    "kjfoundation": ("no_tenders", 0, 0, None),
    "kjro": ("no_tenders", 0, 0, None),
    "kkbattorneys": ("no_tenders", 0, 0, None),
    "kkcompany": ("no_tenders", 0, 0, None),
    "kkiniconsulting": ("no_tenders", 0, 0, None),
    "kktoursafaris": ("no_tenders", 0, 0, None),
    "kleafastcouriers": ("no_tenders", 0, 0, None),
    "kleenair": ("no_tenders", 0, 0, None),
    "kliktech": ("error", 0, 0, "Fetch timeout"),
    "kmj": ("no_tenders", 0, 0, None),
    "knauf": ("no_tenders", 0, 0, None),
    "knightfrank": ("no_tenders", 0, 0, None),
    "knospe": ("no_tenders", 0, 0, None),
    "kns": ("no_tenders", 0, 0, None),
    "kodaklens": ("no_tenders", 0, 0, None),
}

# Institution metadata for leads (no_tenders only)
INST_META = {
    "kitm": ("Kilimanjaro Institute of Technology and Management (KITM)", "https://www.kitm.ac.tz/", ["info@kitm.ac.tz"]),
    "kiut": ("KIUT", "https://kiut.ac.tz/", ["admissions@kiut.ac.tz", "info@kiut.ac.tz"]),
    "kivulini": ("Kivulini Womens Empowerment", "https://kivulini.or.tz/", ["info@kivulini.or.tz"]),
    "kiwamwaku": ("KIWAMWAKU Foundation", "https://kiwamwaku.or.tz/", ["info@kiwamwaku.or.tz"]),
    "kjfoundation": ("Karimjee Foundation", "https://www.karimjee.com/", []),
    "kjro": ("Kijana Jasiri Resilience Organization", "https://kjro.or.tz/", ["info@kjro.or.tz"]),
    "kkbattorneys": ("KKB Attorneys At Law", "https://kkbattorneys.co.tz/", ["info@kkbattorneys.co.tz"]),
    "kkcompany": ("K & K Company Ltd", "https://kkcompany.co.tz/", ["info@kkcompany.co.tz"]),
    "kkiniconsulting": ("Kuyonza Kini Consulting Engineers", "https://kkiniconsulting.co.tz/", ["info@kkiniconsulting.co.tz"]),
    "kktoursafaris": ("KK Tours Safaris", "https://kktoursafaris.co.tz/", ["info@kktoursafaris.co.tz"]),
    "kleafastcouriers": ("Kleafast Couriers & Logistics", "https://kleafastcouriers.co.tz/", ["info@kleafastcouriers.co.tz"]),
    "kleenair": ("Kleenair Tanzania", "https://www.kleenair.co.tz/", ["info@kleenair.co.tz"]),
    "kmj": ("KMJ Group", "https://kmj.co.tz/", ["info@kmj.co.tz"]),
    "knauf": ("Knauf Gypsum Tanzania", "https://knauf.com/", ["info-tz@knauf.com"]),
    "knightfrank": ("Knight Frank Tanzania", "https://www.knightfrank.co.tz/", []),
    "knospe": ("Knospe Group Ltd", "https://knospe.co.tz/", ["info@knospe.co.tz"]),
    "kns": ("Kilombero Northern Safaris", "https://kns.co.tz/", ["info@kns.co.tz"]),
    "kodaklens": ("Kodak Lens Tanzania", "https://kodaklenses.tz/", []),
}


def update_last_scrape(inst_dir: Path, status: str, error: str | None, tender_count: int):
    data = {
        "institution": inst_dir.name,
        "last_scrape": NOW,
        "next_scrape": ((datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat() + "T06:00:00Z"),
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
        "run_id": RUN_ID,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def append_scrape_log(inst_dir: Path, status: str, tender_count: int, doc_count: int, error: str | None):
    log_path = inst_dir / "scrape_log.json"
    if log_path.exists():
        data = json.loads(log_path.read_text(encoding="utf-8"))
    else:
        data = {"runs": []}
    data["runs"].append({
        "run_id": RUN_ID,
        "timestamp": NOW,
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tender_count,
        "new_tenders": 0,
        "updated_tenders": 0,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    })
    log_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def append_lead(slug: str, name: str, url: str, emails: list[str]):
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        raw = json.loads(leads_path.read_text(encoding="utf-8"))
        leads = raw if isinstance(raw, list) else raw.get("leads", [])
    # Skip if already present
    if any(l.get("institution_slug") == slug for l in leads):
        return
    lead = {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, ICT services, or partnership opportunities.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
        "draft_email_body": f"""Dear {name} Team,

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
""",
        "created_at": NOW,
        "status": "pending",
    }
    leads.append(lead)
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    for slug, (status, tender_count, doc_count, err) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        ls_status = "success" if status == "no_tenders" or status == "success" else "error"
        update_last_scrape(inst_dir, ls_status, err, tender_count)
        append_scrape_log(inst_dir, ls_status, tender_count, doc_count, err)

        if status == "no_tenders" and slug in INST_META:
            name, url, emails = INST_META[slug]
            append_lead(slug, name, url, emails)

        # RESULT|slug|status|tender_count|doc_count
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Sync leads CSV
    import subprocess
    subprocess.run(
        ["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=str(PROJECT),
        check=True,
    )


if __name__ == "__main__":
    main()
