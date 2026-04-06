#!/usr/bin/env python3
"""Process 25 institutions (rfl through rorica): update scrape state, create leads if no tenders."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch97"

INSTITUTIONS = [
    ("rfl", "Royal Furnishers", "https://royalfurnisherstz.com/", ["info@royalfurnisherstz.com", "info@rfl.co.tz"]),
    ("rgsgroup", "RGS Group of Companies", "https://rgsgroup.co.tz/", ["info@rgsgroup.co.tz", "sales@rgsgroup.co.tz"]),
    ("rhotiahealthcentre", "Rhotia Health Centre", "https://rhotiahealthcentre.or.tz/", ["webmaster@rhotiahealthcentre.or.tz"]),
    ("ricattorneys", "RIC Attorneys", "https://ricattorneys.co.tz/", ["ricattorneys2012@gmail.com", "mccctz@gmail.com"]),
    ("richiedady", "Richie Dady Limited", "https://richiedady.co.tz/", []),
    ("rickmedia", "RICKMEDIA", "https://rickmedia.co.tz/", ["saraphinajerry17@gmail.com", "hello@rickmedia.co.tz", "rickmediatanzania@gmail.com"]),
    ("ricobed", "RICOBED", "https://ricobed.ac.tz/", ["info@ricobed.ac.tz", "directorricobed@gmail.com"]),
    ("riftvalleylodge", "Rift Valley Lodge", "https://riftvalleylodge.co.tz/", ["reservations@riftvalleylodge.co.tz"]),
    ("rightclicksolutions", "Right Click Solutions Tanzania", "https://rightclicksolutions.co.tz/", ["sales@rightclicksolutions.co.tz"]),
    ("rightwayschools", "Rightwayschools", "https://rightwayschools.ac.tz/", ["rightway@rightwayschools.ac.tz"]),
    ("rimzone", "RIM ZONE TRADING CO. LTD", "https://rimzone.co.tz/", ["rimzonetz@gmail.com", "operations@rimzone.co.tz"]),
    ("risoncompany", "Rison Company Limited", "https://risoncompany.co.tz/", ["info@risoncompany.co.tz"]),
    ("rita", "RITA", "https://rita.go.tz/", ["info@rita.go.tz"]),
    ("riverstonesafaris", "RiverStone Safaris", "https://riverstonesafaris.co.tz/", ["info@riverstonesafaris.co.tz", "rngusaru@riverstonesafaris.co.tz"]),
    ("riverton", "Riverton Africa Limited", "https://riverton.co.tz/", ["sales@riverton.co.tz", "info@riverton.co.tz"]),
    ("rjitsolutions", "RJ IT Solutions", "https://rjitsolutions.co.tz/", ["sales@rjitsolutions.co.tz", "info@rjitsolutions.co.tz"]),
    ("rkgroup", "RK Group", "https://rkgroup.co.tz/", ["info@rkgroup.co.tz"]),
    ("rmb", "RMB", "https://grid.rmb.co.za/Default.aspx?tabid=57&returnurl=%2f", ["info@rmb.co.za"]),
    ("rmholdings", "RM Holdings Limited", "https://rmholdings.co.tz/", ["info@rmholdings.co.tz", "ebemuguli@gmail.com"]),
    ("roadsfund", "Roads Fund Board", "https://roadsfund.go.tz/", ["info@roadsfund.go.tz"]),
    ("rocksolutionlimited", "Rock Solution Limited", "https://rocksolutionlimited.co.tz/", []),
    ("rockson", "Rockson Engineers", "https://rockson.co.tz/", []),
    ("rolinternational", "ROL International", "https://rolinternational.ac.tz/", []),
    ("rookconsultants", "Rook Consultants Limited", "https://rookconsultants.co.tz/", ["info@rookconsultants.co.tz"]),
    ("rorica", "RORICA ENGINEERING", "https://www.rorica.co.tz/", []),
]

# Scrape results: slug -> (status, tender_count, doc_count, error?)
RESULTS = {
    "rfl": ("no_tenders", 0, 0, None),
    "rgsgroup": ("no_tenders", 0, 0, None),
    "rhotiahealthcentre": ("error", 0, 0, "Account suspended"),
    "ricattorneys": ("no_tenders", 0, 0, None),
    "richiedady": ("no_tenders", 0, 0, None),
    "rickmedia": ("no_tenders", 0, 0, None),
    "ricobed": ("no_tenders", 0, 0, None),
    "riftvalleylodge": ("no_tenders", 0, 0, None),
    "rightclicksolutions": ("no_tenders", 0, 0, None),
    "rightwayschools": ("no_tenders", 0, 0, None),
    "rimzone": ("no_tenders", 0, 0, None),
    "risoncompany": ("no_tenders", 0, 0, None),
    "rita": ("error", 0, 0, "Fetch timeout/connection failed"),
    "riverstonesafaris": ("no_tenders", 0, 0, None),
    "riverton": ("no_tenders", 0, 0, None),
    "rjitsolutions": ("no_tenders", 0, 0, None),
    "rkgroup": ("no_tenders", 0, 0, None),
    "rmb": ("error", 0, 0, "Fetch timeout"),
    "rmholdings": ("no_tenders", 0, 0, None),
    "roadsfund": ("error", 0, 0, "Fetch timeout"),
    "rocksolutionlimited": ("no_tenders", 0, 0, None),
    "rockson": ("no_tenders", 0, 0, None),
    "rolinternational": ("error", 0, 0, "Account suspended"),
    "rookconsultants": ("no_tenders", 0, 0, None),
    "rorica": ("no_tenders", 0, 0, None),
}

DRAFT_BODY = """Dear {institution_name} Team,

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


def extract_emails_from_site(emails_from_readme):
    """Use README emails; could extend to scrape site."""
    return [e for e in emails_from_readme if e and "@" in str(e) and "your@email.com" not in str(e)]


def main():
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    leads_to_append = []

    for slug, name, url, emails in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)

        status, tender_count, doc_count, err = RESULTS.get(slug, ("no_tenders", 0, 0, None))
        if err:
            status = "error"

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "status": "success" if status != "error" else "error",
            "error": err,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json
        log_file = inst_dir / "scrape_log.json"
        log_data = {"runs": []}
        if log_file.exists():
            with open(log_file) as f:
                log_data = json.load(f)
        log_data["runs"].append({
            "run_id": RUN_ID,
            "timestamp": now,
            "status": "success" if status != "error" else "error",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        })
        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=2)

        # Create lead for no_tenders or error (opportunity)
        if status in ("no_tenders", "error"):
            extracted = extract_emails_from_site(emails)
            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": url,
                "emails": extracted,
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services." if status == "no_tenders" else f"Site error or suspended: {err}. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": DRAFT_BODY.format(institution_name=name),
                "created_at": now,
                "status": "pending",
            }
            leads_to_append.append(lead)

        # Print RESULT line
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Append leads to leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    leads.extend(leads_to_append)
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"\nAppended {len(leads_to_append)} leads. Running sync_leads_csv.py...")
    import subprocess
    subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True, cwd=str(PROJECT))


if __name__ == "__main__":
    main()
