#!/usr/bin/env python3
"""Process scrape results for batch59 (25 institutions)."""
import json
import os
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch59"
NOW = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# Scrape results: slug -> (status, tender_count, doc_count, error?)
RESULTS = [
    ("kavutacontractors", "no_tenders", 0, 0, None),
    ("kazi", "no_tenders", 0, 0, None),
    ("kazibox", "blocked", 0, 0, "Mod_Security 406"),
    ("kaziconnect", "no_tenders", 0, 0, None),
    ("kbl", "no_tenders", 0, 0, None),
    ("kcb-bank", "down", 0, 0, "503 Service Unavailable"),
    ("kcbbank", "no_tenders", 0, 0, None),
    ("kcmc", "no_tenders", 0, 0, None),  # Job/course announcements, not procurement
    ("kdworkshop", "no_tenders", 0, 0, None),
    ("kea", "no_tenders", 0, 0, None),
    ("kec", "timeout", 0, 0, "Fetch timeout"),
    ("kekogarage", "no_tenders", 0, 0, None),
    ("kekopharma", "error", 0, 0, "SSL/certificate error"),
    ("kelmpowersystems", "no_tenders", 0, 0, None),
    ("kenbright", "no_tenders", 0, 0, None),
    ("kenonkeconsulting", "no_tenders", 0, 0, None),
    ("kenosis", "no_tenders", 0, 0, None),
    ("kentanuga", "down", 0, 0, "Account suspended"),
    ("kepler", "no_tenders", 0, 0, None),
    ("kfinance", "no_tenders", 0, 0, None),
    ("kgc", "no_tenders", 0, 0, None),
    ("kgginvestment", "no_tenders", 0, 0, None),
    ("kgs", "no_tenders", 0, 0, None),
    ("khabar", "no_tenders", 0, 0, None),
    ("kiangazi", "no_tenders", 0, 0, None),
]

# Institution metadata for leads
INST_META = {
    "kavutacontractors": ("Kavuta Contractors (KCC)", "https://kavutacontractors.co.tz/", ["mangewkavuta@yahoo.co.uk", "info@kavutacontractors.co.tz"]),
    "kazi": ("PMO-LER", "https://kazi.go.tz/", ["ps@kazi.go.tz"]),
    "kazibox": ("KAZI BOX", "https://kazibox.co.tz/", ["docs@kazibox.co.tz"]),
    "kaziconnect": ("KAZICONNECT", "https://kaziconnect.co.tz/", ["helpdesk@kaziconnect.co.tz"]),
    "kbl": ("KBL", "https://www.kbl.co.tz/", []),
    "kcb-bank": ("KCB Bank Tanzania", "https://tz.kcbgroup.com/about-us/suppliers", []),
    "kcbbank": ("KCB Bank Tanzania", "https://kcbbank.co.tz/", []),
    "kcmc": ("KCMC", "https://kcmc.ac.tz/", ["kcmcadmin@kcmc.ac.tz"]),
    "kdworkshop": ("K.D Workshop", "https://www.kdworkshop.co.tz/", ["sales@kdworkshop.co.tz"]),
    "kea": ("Kea Company Ltd", "https://www.kea.co.tz/", ["info@keacompany.co.tz"]),
    "kec": ("KEC", "https://kec.or.tz/", ["kec@kec.or.tz"]),
    "kekogarage": ("Keko Garage", "https://kekogarage.co.tz/", ["info@kekogarage.co.tz"]),
    "kekopharma": ("KPI/Kekopharma", "https://kekopharma.co.tz/publications/tender", ["priva.shayo@kekopharma.co.tz", "info@kekopharma.co.tz"]),
    "kelmpowersystems": ("Kelm Power Systems", "https://www.kelmpowersystems.co.tz/", ["info@kelmpowersystems.co.tz"]),
    "kenbright": ("KenbrightTZ", "https://kenbright.co.tz/", []),
    "kenonkeconsulting": ("Kenonke Consulting", "https://kenonkeconsulting.co.tz/", ["kenonkeconsulting@gmail.com"]),
    "kenosis": ("KENOSIS TECHNOLOGIES", "https://kenosis.co.tz/", ["support@kenosis.co.tz"]),
    "kentanuga": ("Kentanuga", "https://kentanuga.co.tz/", ["webmaster@kentanuga.co.tz"]),
    "kepler": ("Kepler Consultant", "https://kepler.co.tz/", ["info@keplerafrica.com"]),
    "kfinance": ("K-FINANCE", "https://kfinance.co.tz/tender-loan/", []),
    "kgc": ("NAJUNA General Supplies", "https://kgc.co.tz/", ["najunasupplies@kgc.co.tz"]),
    "kgginvestment": ("KGG Investment", "https://kgginvestment.co.tz/", ["kggcontructors@gmail.com"]),
    "kgs": ("KAJOTE General Superintendence", "https://kgs.co.tz/", ["info@kgs.co.tz", "port.operations@kgs.co.tz"]),
    "khabar": ("The Ismaili Khabar", "https://www.khabar.co.tz/", []),
    "kiangazi": ("Kiangazi Properties", "https://www.kiangazi.co.tz/", ["info@kiangazi.co.tz"]),
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


def update_institution(slug, status, tender_count, doc_count, error):
    inst_dir = PROJECT / "institutions" / slug
    inst_dir.mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

    last_scrape = {
        "institution": slug,
        "last_scrape": NOW,
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "documents_downloaded": doc_count,
        "status": "success" if status in ("tenders", "no_tenders") and not error else "error",
        "error": error,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(last_scrape, f, indent=2)

    scrape_log_path = inst_dir / "scrape_log.json"
    log_entry = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "status": "success" if not error else "error",
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    }
    if scrape_log_path.exists():
        with open(scrape_log_path) as f:
            data = json.load(f)
        runs = data.get("runs", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
    else:
        runs = []
    runs.append(log_entry)
    with open(scrape_log_path, "w") as f:
        json.dump({"runs": runs[-100:]}, f, indent=2)


def append_leads():
    leads_path = PROJECT / "opportunities" / "leads.json"
    if leads_path.exists():
        with open(leads_path) as f:
            leads = json.load(f)
    else:
        leads = []
    existing_slugs = {l.get("institution_slug") for l in leads}

    new_leads = []
    for slug, status, _, _, error in RESULTS:
        if slug in existing_slugs:
            continue
        meta = INST_META.get(slug, (slug, "", []))
        name, url, emails = meta
        if not emails and status not in ("blocked", "down", "timeout", "error"):
            emails = []
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services." + (f" Scrape note: {error}" if error else ""),
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(name=name),
            "created_at": NOW,
            "status": "pending",
        }
        new_leads.append(lead)
        leads.append(lead)

    if new_leads:
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        print(f"Appended {len(new_leads)} new leads to leads.json")
    return len(new_leads)


def main():
    for slug, status, tc, dc, err in RESULTS:
        update_institution(slug, status, tc, dc, err)
        st = "error" if err else status
        print(f"RESULT|{slug}|{st}|{tc}|{dc}")

    n = append_leads()
    # Sync CSV
    import subprocess
    subprocess.run(["/usr/bin/env", "python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True)
    print(f"Synced leads.csv ({n} new leads)")


if __name__ == "__main__":
    main()
