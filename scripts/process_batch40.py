#!/usr/bin/env python3
"""Process scrape results for run_20260313_205329_batch40 - 25 institutions."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch40"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Scrape results: slug -> (status, tender_count, doc_count, error?)
# status: success|no_tenders|error
RESULTS = [
    ("furahahospital", "no_tenders", 0, 0, None),
    ("fursacredit", "no_tenders", 0, 0, None),
    ("futureworld", "no_tenders", 0, 0, None),
    ("g-tech", "no_tenders", 0, 0, None),
    ("g7group", "no_tenders", 0, 0, None),
    ("gaaws", "error", 0, 0, "Site timeout/SSL"),
    ("gabeco", "error", 0, 0, "Webmail login page - not tender site"),
    ("gabsons", "no_tenders", 0, 0, None),
    ("gadgetronix", "no_tenders", 0, 0, None),
    ("gaia", "no_tenders", 0, 0, None),
    ("gailnet", "no_tenders", 0, 0, None),
    ("game", "no_tenders", 0, 0, None),
    ("gardenmarket", "no_tenders", 0, 0, None),
    ("gas", "no_tenders", 0, 0, None),
    ("gasco", "error", 0, 0, "Site timeout"),
    ("gash", "no_tenders", 0, 0, None),
    ("gatewaylogistics", "no_tenders", 0, 0, None),
    ("gazetini", "error", 0, 0, "Site timeout"),
    ("gcl", "no_tenders", 0, 0, None),
    ("gcla", "error", 0, 0, "Site timeout"),
    ("gcli", "no_tenders", 0, 0, None),
    ("gcmmarketing", "no_tenders", 0, 0, None),
    ("gctl", "no_tenders", 0, 0, None),
    ("geamos", "no_tenders", 0, 0, None),
    ("geas", "no_tenders", 0, 0, None),
]

# Institution metadata from READMEs
INST_META = {
    "furahahospital": ("Furaha Hospital", "https://furahahospital.co.tz/", ["info@furahahospital.co.tz"], "Healthcare"),
    "fursacredit": ("Fursa Credit Services", "https://fursacredit.co.tz/", [], "Real Estate"),
    "futureworld": ("Futureworld Vocational Institute", "https://futureworld.ac.tz/", ["info@futureworld.ac.tz"], "Educational"),
    "g-tech": ("Guzzer Technologies Ltd", "https://www.g-tech.co.ke/", ["info@g-tech.co.ke"], "ICT"),
    "g7group": ("G7 International Ltd", "https://g7group.co.tz/", [], "Logistics"),
    "gaaws": ("Government Agency for Automobile Workshop Services", "https://gaaws.go.tz/", ["info@gaaws.go.tz"], "Government"),
    "gabeco": ("Gabeco", "https://gabeco.co.tz/", [], "Commercial"),  # tender_url was webmail :2096
    "gabsons": ("Gabsons (T) Limited", "https://gabsons.co.tz/", ["info@gabsons.co.tz"], "Fire/ICT/Chemicals"),
    "gadgetronix": ("Gadgetronix", "https://gadgetronix.net/", ["sales@gadgetronix.net"], "Energy/Security"),
    "gaia": ("Gaia", "https://gaia.co.tz/", [], "Commercial"),
    "gailnet": ("Gailnet Company Limited", "https://gailnet.co.tz/", ["sales@gailnet.co.tz"], "ICT"),
    "game": ("Game Tanzania", "http://www.game.co.tz/", [], "Retail"),
    "gardenmarket": ("Garden Market", "https://gardenmarket.co.tz/", ["gm@gardenmarket.co.tz", "hello@gardenmarket.co.tz"], "Retail"),
    "gas": ("Guardian Angels Schools", "https://gas.ac.tz/", ["info@gas.ac.tz"], "Educational"),
    "gasco": ("Gas Company Tanzania", "https://gasco.co.tz/", ["gascotz@tpdc.co.tz"], "Energy"),
    "gash": ("Gupta Auto Spares & Hardware", "https://gash.co.tz/", ["info@gash.co.tz", "info.dar@gash.co.tz"], "Auto Parts"),
    "gatewaylogistics": ("Gateway Logistics Services Ltd", "https://gatewaylogistics.co.tz/", [], "Logistics"),
    "gazetini": ("Gazetini", "https://gazetini.co.tz/", ["support@bluepearlhost.com"], "Media"),
    "gcl": ("Gonelemale Company Limited", "https://gcl.co.tz/", ["sales@gcl.co.tz", "director@gcl.co.tz"], "Building Materials"),
    "gcla": ("GCLA - Government Chemist Lab", "https://gcla.go.tz/", ["gcla@gcla.go.tz"], "Government"),
    "gcli": ("GCL Insurance Assessors", "https://gcli.co.tz/", ["info@gcli.co.tz"], "Insurance"),
    "gcmmarketing": ("GCM Innovation & Marketing Consultancy", "https://gcmmarketing.co.tz/", ["info@gcmmarketing.co.tz", "info@landmarine.org"], "Marketing"),
    "gctl": ("GOPA Contractors Tanzania Ltd", "https://gctl.co.tz/", ["info@gctl.co.tz"], "Construction"),
    "geamos": ("Geamos Company Limited", "https://geamos.co.tz/", [], "Logistics"),
    "geas": ("GEAS Company Limited", "https://geas.co.tz/", ["info@geas.co.tz"], "Security/Fire/IT"),
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
    for slug, status, tender_count, doc_count, err in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "documents_downloaded": doc_count,
            "status": "success" if status == "success" else ("error" if status == "error" else "no_tenders"),
            "error": err,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log_path = inst_dir / "scrape_log.json"
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": last_scrape["status"],
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        }
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_data = json.load(f)
            runs = log_data.get("runs", [])
        else:
            runs = []
        runs.append(log_entry)
        with open(scrape_log_path, "w") as f:
            json.dump({"runs": runs}, f, indent=2)

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Append leads for all 25 (no tenders found)
    leads_path = PROJECT / "opportunities" / "leads.json"
    with open(leads_path) as f:
        leads = json.load(f)
    if not isinstance(leads, list):
        leads = leads.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}
    added = 0
    for slug, status, _, _, _ in RESULTS:
        if slug in existing_slugs:
            continue
        meta = INST_META.get(slug, (slug, "", [], ""))
        name, url, emails, category = meta
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(name=name),
            "created_at": NOW,
            "status": "pending",
        }
        leads.append(lead)
        added += 1

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"\nAppended {added} leads to opportunities/leads.json")


if __name__ == "__main__":
    main()
