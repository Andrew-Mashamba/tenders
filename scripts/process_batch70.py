#!/usr/bin/env python3
"""Process scrape results for batch70 - 25 institutions."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch70"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

INSTITUTIONS = [
    {"slug": "marscommunications", "name": "Mars Communications Limited", "url": "https://marscomm.co.tz/", "emails": ["info@MarsComm.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "maruco", "name": "St. Augustine University - Marian University College", "url": "https://maruco.ac.tz/", "emails": ["principal@maruco.ac.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "marungu", "name": "Marungu Sisal Plantation", "url": "http://junacogroup.com/", "emails": ["info.marungu@junacogroup.com", "info@junacogroup.com"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "masaa", "name": "MASAA IT Consultants", "url": "https://masaa.co.tz/", "emails": ["arnold.shirima@gmail.com"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "masaimaragardens", "name": "Masai Mara Gardening Co. Ltd", "url": "https://masaimaragardens.co.tz/", "emails": ["maxbizz@mail.com", "murwa@masaimara.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "masasi", "name": "Masasi District Council", "url": "https://masasi.go.tz/", "emails": ["ded@masasi.go.tz"], "tenders": 0, "docs": 0, "status": "error", "error": "SSL/certificate error - site unreachable"},
    {"slug": "maseaa", "name": "MASEAA", "url": "https://maseaa.or.tz/", "emails": [], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "masseyferguson", "name": "Massey Ferguson Tanzania", "url": "https://www.masseyferguson.co.tz/", "emails": ["info@masseyferguson.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "mastek", "name": "Mastek IT Ltd", "url": "https://mastek.co.tz/", "emails": ["sales@mastek.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "masumin", "name": "Masumin Printways & Stationers LTD", "url": "https://masumin.co.tz/", "emails": ["info@masumin.co.tz", "sales@masumin.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "masumintours", "name": "Masumin Tours", "url": "https://masumintours.co.tz/", "emails": [], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "maswadc", "name": "Halmashauri ya Wilaya ya Maswa", "url": "https://maswadc.go.tz/ugavi-na-manunuzi", "emails": ["ded@maswadc.go.tz"], "tenders": 0, "docs": 0, "status": "error", "error": "Site unreachable (timeout/SSL)"},
    {"slug": "mat", "name": "Medical Association of Tanzania", "url": "https://mat.or.tz/", "emails": ["info@mat.or.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "matembezi", "name": "Matembezi - Luxury Tours", "url": "https://matembezi.co.tz/", "emails": ["hagai@matembezi.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "mattytech", "name": "MattyTech", "url": "https://mattytech.co.tz/", "emails": [], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "matvillabeach", "name": "Matvilla Beach Lodge & Campsite", "url": "https://matvillabeach.co.tz/", "emails": [], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "mawalla", "name": "Mawalla", "url": "https://mawalla.co.tz/", "emails": [], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "mawallaadventuresafari", "name": "Mawalla Adventure Safari", "url": "https://mawallaadventuresafari.co.tz/", "emails": ["info@mawallaadventuresafari.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "mawasiliano", "name": "Ministry of Communication and Information Technology", "url": "https://mawasiliano.go.tz/", "emails": ["ps@mawasiliano.go.tz"], "tenders": 0, "docs": 0, "status": "error", "error": "Site timeout"},
    {"slug": "maxesh", "name": "Maxesh Company Limited", "url": "https://maxesh.co.tz/", "emails": [], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "maxima", "name": "MAXIMA Clearing & Forwarding", "url": "https://maxima.co.tz/", "emails": ["info@maxima.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "maxipro", "name": "Maxi Pro Company Limited", "url": "https://maxipro.co.tz/", "emails": ["info@maxipro.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "maxons", "name": "Maxons Paper Converters Ltd", "url": "https://maxons.co.tz/", "emails": ["sales@maxons.org", "info@maxons.org"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "maycom", "name": "Maycom Solution", "url": "https://maycom.co.tz/", "emails": [], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "mayer", "name": "Mayer & Co", "url": "https://mayer.co.tz/", "emails": ["info@mayer.co.tz", "sarah@mayer.co.tz", "john@mayer.co.tz", "diana@mayer.co.tz", "catherine@mayer.co.tz"], "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
]

DRAFT_BODY = """Dear {name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions, government agencies, and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

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
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}

    new_leads = []
    for inst in INSTITUTIONS:
        slug = inst["slug"]
        if slug in existing_slugs:
            continue
        opp_desc = "No formal tenders or procurement notices found."
        if inst.get("error"):
            opp_desc += f" Site status: {inst['error']}."
        opp_desc += " ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."
        new_leads.append({
            "institution_slug": slug,
            "institution_name": inst["name"],
            "website_url": inst["url"],
            "emails": inst["emails"],
            "opportunity_type": "sell",
            "opportunity_description": opp_desc,
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
            "draft_email_body": DRAFT_BODY.format(name=inst["name"]),
            "created_at": NOW,
            "status": "pending",
        })

    leads.extend(new_leads)
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    for inst in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / inst["slug"]
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
        (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": inst["slug"],
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": inst["tenders"],
            "status": inst["status"],
            "error": inst.get("error"),
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        log_path = inst_dir / "scrape_log.json"
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": inst["status"],
            "tenders_found": inst["tenders"],
            "documents_downloaded": inst["docs"],
            "errors": [inst["error"]] if inst.get("error") else [],
        }
        if log_path.exists():
            with open(log_path) as f:
                log_data = json.load(f)
            runs = log_data.get("runs", [])
        else:
            runs = []
        runs.append(log_entry)
        with open(log_path, "w") as f:
            json.dump({"runs": runs}, f, indent=2)

    for inst in INSTITUTIONS:
        status = inst["status"]
        if inst.get("error"):
            status = "error"
        print(f"RESULT|{inst['slug']}|{status}|{inst['tenders']}|{inst['docs']}")

    print(f"\nAppended {len(new_leads)} new leads. Total leads: {len(leads)}")


if __name__ == "__main__":
    main()
