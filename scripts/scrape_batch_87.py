#!/usr/bin/env python3
"""
Scrape batch 87: observer, ocagz, oceanspa, ocode, offradar, ogmconsultants, oilcom,
okelectrical, olasitiinvestment, olazanzibar, olbongo, oleco, ollahost, olmesera,
olotutrading, omar.tz, omarawadhtransport, omegaviewhotel, omis, omkr, omni, ompr,
oneclickafrica, onestopzanzibar, onet.
"""
import json
import re
import os
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch87"
INSTITUTIONS = [
    ("observer", "Observer Africa", "https://observer.co.tz/"),
    ("ocagz", "OCAGZ", "https://eprocurement.zppda.go.tz/"),
    ("oceanspa", "Ocean Spa", "https://oceanspa.co.tz/"),
    ("ocode", "OCODE", "https://ocode.or.tz/"),
    ("offradar", "Offradar Medicare Limited", "https://offradar.co.tz/services/medical-procurement-supply/"),
    ("ogmconsultants", "OGM Consultants", "https://ogmconsultants.co.tz/"),
    ("oilcom", "OILCOM Tanzania Limited", "https://oilcom.co.tz/"),
    ("okelectrical", "OK Electrical and Electronics", "https://okelectrical.co.tz/"),
    ("olasitiinvestment", "Olasiti Investment Co. LTD", "https://olasitiinvestment.co.tz/"),
    ("olazanzibar", "Ola Zanzibar Car Rental", "https://olazanzibar.co.tz/"),
    ("olbongo", "Olbongo", "https://olbongo.co.tz/"),
    ("oleco", "Oleco Limited", "http://oleco.co.tz/"),
    ("ollahost", "Olla Host", "https://ollahost.co.tz/"),
    ("olmesera", "Ol Mesera African Restaurant", "https://olmeserarestaurant.com/"),
    ("olotutrading", "Olotu Trading Company Limited", "https://olotutrading.co.tz/"),
    ("omar.tz", "Omar Tazi", "https://omar.tz/"),
    ("omarawadhtransport", "Omarawadh Transport", "https://omarawadhtransport.co.tz/"),
    ("omegaviewhotel", "Omega View Hotel", "https://omegaviewhotel.co.tz/"),
    ("omis", "OMIS", "https://omis.co.tz/"),
    ("omkr", "OMKR", "https://omkr.go.tz/event/makabidhiano-ya-gari/"),
    ("omni", "Omni Computers Ltd", "https://omni.co.tz/"),
    ("ompr", "OMPR", "https://ompr.go.tz/ufunguzi-wa-mfumo-wa-manunuzi-mtandao/"),
    ("oneclickafrica", "Oneclick Africa", "https://oneclickafrica.co.tz/"),
    ("onestopzanzibar", "One Stop Zanzibar", "http://onestopzanzibar.co.tz/"),
    ("onet", "Onet", "https://www.onet.co.tz/"),
]

# Email patterns from READMEs
INST_EMAILS = {
    "observer": [],
    "ocagz": ["info@ocagz.go.tz"],
    "oceanspa": ["info@oceanspa.co.tz"],
    "ocode": ["info@ocode.or.tz"],
    "offradar": ["info@offradar.co.tz", "info@apexa.com"],
    "ogmconsultants": ["info@company.com"],
    "oilcom": ["info@oilcom.co.tz"],
    "okelectrical": ["info@okelectrical.co.tz", "webmaster@okelectrical.co.tz"],
    "olasitiinvestment": ["info@olasitiinvestment.co.tz", "onfo@olasiti-investment.co.tz"],
    "olazanzibar": ["info@olazanzibar.co.tz"],
    "olbongo": [],
    "oleco": ["info@oleco.co.tz"],
    "ollahost": [],
    "olmesera": ["info@olmeserarestaurant.com"],
    "olotutrading": ["olotutrading@gmail.com"],
    "omar.tz": ["amandasmith@mail.com", "contact@omartazi.com"],
    "omarawadhtransport": ["info@omarawadhtransport.co.tz"],
    "omegaviewhotel": ["info@omegaviewhotel.co.tz"],
    "omis": ["info@omis.co.tz"],
    "omkr": ["info@omkr.go.tz"],
    "omni": ["sales@omni.co.tz", "info@omni.co.tz"],
    "ompr": ["info@ompr.go.tz"],
    "oneclickafrica": ["info@oneclickafrica.co.tz"],
    "onestopzanzibar": [],
    "onet": [],
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


def extract_emails_from_html(html: str) -> list:
    """Extract email addresses from HTML."""
    if not html:
        return []
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    found = set(re.findall(pattern, html))
    # Filter out common non-contact emails
    skip = {"example.com", "email.com", "domain.com", "sentry.io", "wixpress.com", "google.com"}
    return [e for e in found if not any(s in e.lower() for s in skip)]


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def update_last_scrape(inst_dir: Path, slug: str, status: str, tender_count: int, error: str = None):
    now = datetime.now(timezone.utc).isoformat()
    data = {
        "institution": slug,
        "last_scrape": now,
        "next_scrape": now,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(data, f, indent=2)


def append_scrape_log(inst_dir: Path, run_id: str, status: str, tender_count: int, doc_count: int, error: str = None):
    log_path = inst_dir / "scrape_log.json"
    if log_path.exists():
        with open(log_path) as f:
            log = json.load(f)
    else:
        log = {"runs": []}
    # Handle legacy format where log is a list
    if isinstance(log, list):
        log = {"runs": log}
    if "runs" not in log:
        log["runs"] = []
    log["runs"].append({
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tender_count,
        "new_tenders": 0,
        "updated_tenders": 0,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    })
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)


def append_lead(slug: str, name: str, url: str, emails: list, opportunity_type: str, description: str):
    leads_path = PROJECT / "opportunities" / "leads.json"
    if leads_path.exists():
        with open(leads_path) as f:
            leads = json.load(f)
    else:
        leads = []
    lead = {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": list(set(emails))[:10],
        "opportunity_type": opportunity_type,
        "opportunity_description": description,
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
        "draft_email_body": DRAFT_BODY.format(institution_name=name),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }
    # Check if already exists
    existing = [l for l in leads if l.get("institution_slug") == slug]
    if not existing:
        leads.append(lead)
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        return True
    return False


def process_institution(slug: str, name: str, url: str, tender_count: int, doc_count: int, status: str, error: str = None):
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    update_last_scrape(inst_dir, slug, status, tender_count, error)
    append_scrape_log(inst_dir, RUN_ID, status, tender_count, doc_count, error)
    print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")


def main():
    # Based on fetch results: no formal tenders found on any of the 25
    # observer=news, ocagz/oceanspa/offradar/olbongo/olotutrading/omkr=timeout,
    # okelectrical=suspended, rest=no tenders
    results = [
        ("observer", "Observer Africa", "https://observer.co.tz/", "no_tenders", "News/media site"),
        ("ocagz", "OCAGZ", "https://eprocurement.zppda.go.tz/", "timeout", "Site timeout"),
        ("oceanspa", "Ocean Spa", "https://oceanspa.co.tz/", "timeout", "Site timeout"),
        ("ocode", "OCODE", "https://ocode.or.tz/", "no_tenders", "NGO, no tenders"),
        ("offradar", "Offradar Medicare Limited", "https://offradar.co.tz/services/medical-procurement-supply/", "timeout", "Site timeout"),
        ("ogmconsultants", "OGM Consultants", "https://ogmconsultants.co.tz/", "no_tenders", "Construction, no tenders"),
        ("oilcom", "OILCOM Tanzania Limited", "https://oilcom.co.tz/", "no_tenders", "Petroleum, no tenders"),
        ("okelectrical", "OK Electrical and Electronics", "https://okelectrical.co.tz/", "error", "Account suspended"),
        ("olasitiinvestment", "Olasiti Investment Co. LTD", "https://olasitiinvestment.co.tz/", "no_tenders", "Investment, no tenders"),
        ("olazanzibar", "Ola Zanzibar Car Rental", "https://olazanzibar.co.tz/", "no_tenders", "Car rental, no tenders"),
        ("olbongo", "Olbongo", "https://olbongo.co.tz/", "timeout", "Site timeout"),
        ("oleco", "Oleco Limited", "http://oleco.co.tz/", "no_tenders", "Electrical services, no tenders"),
        ("ollahost", "Olla Host", "https://ollahost.co.tz/", "no_tenders", "Domain hosting, no tenders"),
        ("olmesera", "Ol Mesera African Restaurant", "https://olmeserarestaurant.com/", "no_tenders", "Restaurant, no tenders"),
        ("olotutrading", "Olotu Trading Company Limited", "https://olotutrading.co.tz/", "timeout", "Site timeout"),
        ("omar.tz", "Omar Tazi", "https://omar.tz/", "no_tenders", "Personal CV site, no tenders"),
        ("omarawadhtransport", "Omarawadh Transport", "https://omarawadhtransport.co.tz/", "no_tenders", "Transport, no tenders"),
        ("omegaviewhotel", "Omega View Hotel", "https://omegaviewhotel.co.tz/", "no_tenders", "Hotel, no tenders"),
        ("omis", "OMIS", "https://omis.co.tz/", "no_tenders", "Tendering consultancy, no active tenders"),
        ("omkr", "OMKR", "https://omkr.go.tz/event/makabidhiano-ya-gari/", "timeout", "Site timeout"),
        ("omni", "Omni Computers Ltd", "https://omni.co.tz/", "no_tenders", "Computer retail, no tenders"),
        ("ompr", "OMPR", "https://ompr.go.tz/ufunguzi-wa-mfumo-wa-manunuzi-mtandao/", "no_tenders", "Government news, no tenders"),
        ("oneclickafrica", "Oneclick Africa", "https://oneclickafrica.co.tz/", "no_tenders", "ICT services, no tenders"),
        ("onestopzanzibar", "One Stop Zanzibar", "http://onestopzanzibar.co.tz/", "no_tenders", "Domain hosting, no tenders"),
        ("onet", "Onet", "https://www.onet.co.tz/", "no_tenders", "E-commerce, no tenders"),
    ]
    new_leads = 0
    for slug, name, url, outcome, desc in results:
        inst_dir = PROJECT / "institutions" / slug
        ensure_dirs(inst_dir)
        tender_count = 0
        doc_count = 0
        if outcome == "error":
            status = "error"
            error = desc
        elif outcome == "timeout":
            status = "timeout"
            error = desc
        else:
            status = "success"
            error = None
        update_last_scrape(inst_dir, slug, status, tender_count, error)
        append_scrape_log(inst_dir, RUN_ID, status, tender_count, doc_count, error)
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
        # Opportunity workflow for no-tender cases
        if outcome in ("no_tenders", "timeout") and outcome != "error":
            emails = INST_EMAILS.get(slug, [])
            if not emails and slug in ["olbongo", "onestopzanzibar", "observer", "onet"]:
                emails = []  # Will use generic
            opp_type = "sell"
            opp_desc = f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."
            if appended := append_lead(slug, name, url, emails, opp_type, opp_desc):
                new_leads += 1
    return new_leads


if __name__ == "__main__":
    new_leads = main()
    print(f"LEADS_APPENDED|{new_leads}")
