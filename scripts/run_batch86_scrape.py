#!/usr/bin/env python3
"""
Process 25 institutions for run_20260313_205329_batch86.
No tenders found on any site - create opportunity leads for all.
"""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch86"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

INSTITUTIONS = [
    {"slug": "obp-tanzania", "name": "Ocean Business Partners", "url": "https://obp-tanzania.co.tz/", "emails": ["info@obp-tanzania.co.tz"], "fetch_ok": True},
    {"slug": "observer", "name": "Observer Africa", "url": "https://observer.co.tz/", "emails": [], "fetch_ok": True},
    {"slug": "ocagz", "name": "OCAGZ", "url": "https://eprocurement.zppda.go.tz/", "emails": ["info@ocagz.go.tz"], "fetch_ok": False},
    {"slug": "oceanspa", "name": "Ocean Spa", "url": "https://oceanspa.co.tz/", "emails": ["info@oceanspa.co.tz"], "fetch_ok": True},
    {"slug": "ocode", "name": "OCODE", "url": "https://ocode.or.tz/", "emails": ["info@ocode.or.tz"], "fetch_ok": True},
    {"slug": "offradar", "name": "Offradar Medicare Limited", "url": "https://offradar.co.tz/", "emails": ["info@offradar.co.tz", "info@apexa.com"], "fetch_ok": True},
    {"slug": "ogmconsultants", "name": "OGM Consultants", "url": "https://ogmconsultants.co.tz/", "emails": ["info@ogmconsultants.co.tz"], "fetch_ok": True},  # README had info@company.com
    {"slug": "oilcom", "name": "OILCOM Tanzania Limited", "url": "https://oilcom.co.tz/", "emails": ["info@oilcom.co.tz"], "fetch_ok": True},
    {"slug": "okelectrical", "name": "OK Electrical and Electronics", "url": "https://okelectrical.co.tz/", "emails": ["info@okelectrical.co.tz"], "fetch_ok": True},
    {"slug": "olasitiinvestment", "name": "Olasiti Investment Co. LTD", "url": "https://olasitiinvestment.co.tz/", "emails": ["info@olasitiinvestment.co.tz"], "fetch_ok": True},
    {"slug": "olazanzibar", "name": "Ola Zanzibar Car Rental", "url": "https://olazanzibar.co.tz/", "emails": ["info@olazanzibar.co.tz"], "fetch_ok": True},
    {"slug": "olbongo", "name": "Olbongo", "url": "https://olbongo.co.tz/", "emails": [], "fetch_ok": False},
    {"slug": "oleco", "name": "Oleco Limited", "url": "http://oleco.co.tz/", "emails": ["info@oleco.co.tz"], "fetch_ok": True},
    {"slug": "ollahost", "name": "Olla Host", "url": "https://ollahost.co.tz/", "emails": [], "fetch_ok": True},
    {"slug": "olmesera", "name": "Ol Mesera African Restaurant", "url": "https://olmeserarestaurant.com/", "emails": ["info@olmeserarestaurant.com"], "fetch_ok": True},
    {"slug": "olotutrading", "name": "Olotu Trading Company Limited", "url": "https://olotutrading.co.tz/", "emails": ["olotutrading@gmail.com"], "fetch_ok": False},
    {"slug": "omar.tz", "name": "Omar Tazi", "url": "https://omar.tz/", "emails": ["contact@omartazi.com"], "fetch_ok": True},
    {"slug": "omarawadhtransport", "name": "Omarawadh Transport", "url": "https://omarawadhtransport.co.tz/", "emails": ["info@omarawadhtransport.co.tz"], "fetch_ok": True},
    {"slug": "omegaviewhotel", "name": "Omega View Hotel", "url": "https://omegaviewhotel.co.tz/", "emails": ["info@omegaviewhotel.co.tz"], "fetch_ok": True},
    {"slug": "omis", "name": "OM Innovation Solutions (OMIS)", "url": "https://omis.co.tz/", "emails": ["info@omis.co.tz"], "fetch_ok": True},
    {"slug": "omkr", "name": "Ofisi ya Makamo wa Kwanza wa Rais Zanzibar", "url": "https://omkr.go.tz/", "emails": ["info@omkr.go.tz"], "fetch_ok": False},
    {"slug": "omni", "name": "Omni Computers Ltd", "url": "https://omni.co.tz/", "emails": ["sales@omni.co.tz", "info@omni.co.tz"], "fetch_ok": True},
    {"slug": "ompr", "name": "Ofisi ya Makamu wa Pili wa Rais Zanzibar", "url": "https://ompr.go.tz/", "emails": ["info@ompr.go.tz"], "fetch_ok": True},
    {"slug": "oneclickafrica", "name": "Oneclick Africa", "url": "https://oneclickafrica.co.tz/", "emails": ["info@oneclickafrica.co.tz"], "fetch_ok": True},
    {"slug": "onestopzanzibar", "name": "One Stop Zanzibar", "url": "http://onestopzanzibar.co.tz/", "emails": [], "fetch_ok": True},
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


def main():
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    # Check which slugs already exist
    existing_slugs = {l.get("institution_slug") for l in leads}

    results = []
    new_leads = []

    for inst in INSTITUTIONS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # Determine status
        if inst["fetch_ok"]:
            status = "success"
            error_msg = None
        else:
            status = "error"
            error_msg = "Site timeout or unreachable"

        tender_count = 0
        doc_count = 0

        # Create lead if no tenders and not already in leads
        if slug not in existing_slugs:
            lead = {
                "institution_slug": slug,
                "institution_name": inst["name"],
                "website_url": inst["url"],
                "emails": inst["emails"],
                "opportunity_type": "sell",
                "opportunity_description": "No formal tenders found on {} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.".format(inst["name"]),
                "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & {}".format(inst["name"]),
                "draft_email_body": DRAFT_BODY.format(name=inst["name"]),
                "created_at": NOW,
                "status": "pending",
            }
            new_leads.append(lead)
            existing_slugs.add(slug)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW[:10] + "T06:00:00Z",
            "active_tenders_count": 0,
            "status": status,
            "error": error_msg,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json
        scrape_log_path = inst_dir / "scrape_log.json"
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": 0,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": 0,
            "errors": [error_msg] if error_msg else [],
        }
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_data = json.load(f)
            runs = log_data.get("runs", [])
        else:
            runs = []
        runs.append(log_entry)
        with open(scrape_log_path, "w") as f:
            json.dump({"runs": runs[-100:]}, f, indent=2)

        results.append((slug, status, tender_count, doc_count))
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Append new leads
    if new_leads:
        leads.extend(new_leads)
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        print(f"\nAppended {len(new_leads)} leads to leads.json")

    return results


if __name__ == "__main__":
    main()
