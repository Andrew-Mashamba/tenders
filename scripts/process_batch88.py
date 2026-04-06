#!/usr/bin/env python3
"""Process scrape results for batch88 - 25 institutions with no tenders, add leads."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch88"
NOW = datetime.now(timezone.utc).isoformat()

INSTITUTIONS = [
    {"slug": "osiligilaimaasailodge", "name": "Osiligi-Lai Masai Lodge", "url": "https://www.masailodge.com/", "emails": []},
    {"slug": "osp", "name": "Oysterbay Soccer Pitch (OSP)", "url": "https://osp.co.tz/", "emails": []},
    {"slug": "otapp", "name": "Otapp", "url": "https://otapp.co.tz/", "emails": ["info@otapp.co.tz"]},
    {"slug": "outdoorcatering", "name": "Outdoor Catering LTD", "url": "https://outdoorcatering.co.tz/", "emails": ["info@outdoorcatering.co.tz", "support@outdoorcatering.com"]},
    {"slug": "overland", "name": "Overland Group", "url": "https://www.overland.co.tz/", "emails": ["info@overlandlogistics.com"]},
    {"slug": "ovifocus", "name": "OVIFOCUS", "url": "http://ovifocus.co.tz/", "emails": ["info@ovifocus.co.tz"]},
    {"slug": "oxley", "name": "Oxley Limited", "url": "https://www.oxley.co.tz/", "emails": []},
    {"slug": "oyorealestate", "name": "Oyo Real Estate", "url": "https://oyorealestate.co.tz/", "emails": ["info@oyorealestate.co.tz"]},
    {"slug": "oysterbay", "name": "Pearl @ Oysterbay", "url": "https://www.oysterbay.co.tz/", "emails": []},
    {"slug": "ozti", "name": "OZTI East Africa", "url": "https://ozti.co.tz/", "emails": ["sales@ozti.co.tz"]},
    {"slug": "paaadventures", "name": "Paa Adventures", "url": "https://paaadventures.co.tz/", "emails": []},
    {"slug": "pace", "name": "PaCe Informatics Limited", "url": "https://pace.co.tz/", "emails": ["jatin@pace.co.tz"]},
    {"slug": "packway", "name": "Packway LTD", "url": "https://packway.co.tz/", "emails": ["info@packway.co.tz"]},
    {"slug": "pad", "name": "PAD Technologies", "url": "https://pad.co.tz/", "emails": ["info@pad.co.tz", "support@pad.co.tz"]},
    {"slug": "padeco", "name": "PADECO", "url": "https://padeco.or.tz/", "emails": ["contact@savior.com", "info@savior.com"]},
    {"slug": "padsons", "name": "Padsons", "url": "https://padsons.co.tz/", "emails": ["info@padsons.co.tz"]},
    {"slug": "pagt", "name": "PAG(T)", "url": "https://pagt.or.tz/", "emails": ["info@pagt.or.tz"]},
    {"slug": "palacehotelarusha", "name": "Palace Hotel Arusha", "url": "https://palacehotelarusha.co.tz/", "emails": ["info@palacehotelarusha.com", "reservations@palacehotelarusha.com", "marketing@palacehotelarusha.com"]},
    {"slug": "palmresidence", "name": "The Palm Residence", "url": "https://amazingzanzibar.co.tz/", "emails": []},
    {"slug": "pamojastationery", "name": "PAMOJA STATIONERY", "url": "https://pamojastationery.co.tz/", "emails": ["info@pamojastationery.co.tz"]},
    {"slug": "panafrica", "name": "Panafrica (Comfy)", "url": "https://panafrica.co.tz/", "emails": ["panafrica@bellafrica.com", "Panafrica@bellafrica.com"]},
    {"slug": "panafricanauditors", "name": "Pan Africa Auditors", "url": "http://panafricanauditors.co.tz/", "emails": ["webmaster@panafricanauditors.co.tz"], "status": "site_down"},
    {"slug": "panamagardenresort", "name": "Panama Garden Resort", "url": "https://panamagardenresort.co.tz/", "emails": ["reservation@panamagardenresort.co.tz", "info@panamagardenresort.co.tz"]},
    {"slug": "panamainn", "name": "Panama Inn", "url": "https://panamainn.co.tz/", "emails": ["info@panamainn.co.tz", "reservation@panamainn.co.tz"]},
    {"slug": "panamwetours", "name": "Panamwe Tours", "url": "https://www.panamwetours.co.tz/", "emails": ["info@panamwetours.co.tz"]},
]

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


def main():
    for inst in INSTITUTIONS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)

        status = inst.get("status", "no_tenders")
        if status == "site_down":
            status = "site_down"
        else:
            status = "no_tenders"

        last_scrape = {
            "run_id": RUN_ID,
            "slug": slug,
            "status": status,
            "tender_count": 0,
            "doc_count": 0,
            "scraped_at": NOW,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log_path = inst_dir / "scrape_log.json"
        log_entry = {**last_scrape}
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log = json.load(f)
        else:
            log = []
        log.append(log_entry)
        with open(scrape_log_path, "w") as f:
            json.dump(log, f, indent=2)

        print(f"RESULT|{slug}|{status}|0|0")

    # Append leads
    leads_path = PROJECT / "opportunities" / "leads.json"
    with open(leads_path) as f:
        leads = json.load(f)
    if not isinstance(leads, list):
        leads = leads.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}
    new_leads = []
    for inst in INSTITUTIONS:
        if inst["slug"] in existing_slugs:
            continue
        emails = [e for e in inst["emails"] if "@" in e and "." in e]
        lead = {
            "institution_slug": inst["slug"],
            "institution_name": inst["name"],
            "website_url": inst["url"],
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
            "draft_email_body": DRAFT_BODY.format(institution_name=inst["name"]),
            "created_at": NOW,
            "status": "pending",
        }
        new_leads.append(lead)

    leads.extend(new_leads)
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"\nAppended {len(new_leads)} new leads to leads.json")


if __name__ == "__main__":
    main()
