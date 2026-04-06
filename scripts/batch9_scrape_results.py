#!/usr/bin/env python3
"""Apply batch9 scrape results: last_scrape.json, scrape_log.json, leads.json."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch9"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# (slug, status, tender_count, doc_count, institution_name, website_url, emails[], opportunity_type)
RESULTS = [
    ("aqeel", "no_tenders", 0, 0, "AQEEL TRADERS LTD", "https://aqeel.co.tz/", []),
    ("aquacom", "no_tenders", 0, 0, "Aquacom", "https://www.aquacom.co.tz/", ["info@aquacom.co.tz", "mwanza@aquacom.co.tz"]),
    ("aquacool", "no_tenders", 0, 0, "Kisima Pure Drinking Water / Aqua Cool", "https://kisimawater.com/", ["info@kisimawater.com", "kiscafe@kisimawater.com"]),
    ("aquila", "no_tenders", 0, 0, "Aquila", "https://www.aquila.co.tz/", []),
    ("aquilaventure", "no_tenders", 0, 0, "Aquila Venture", "https://aquilaventure.co.tz/", ["info@aquilaventure.co.tz", "Booking@aquilaventure.co.tz"]),
    ("archco", "no_tenders", 0, 0, "Archco", "https://www.archco.co.tz/", []),
    ("archotel", "no_tenders", 0, 0, "Arc Hotel", "https://www.archotel.co.tz/", ["booking@archotel.co.tz"]),
    ("archvistaconsults", "no_tenders", 0, 0, "Archvista Consults", "https://archvistaconsults.co.tz/", ["info@archvistaconsults.co.tz", "masunga@archvistaconsults.co.tz", "busanya@archvistaconsults.co.tz", "fatuma@archvistaconsults.co.tz"]),
    ("ardeanattorneys", "no_tenders", 0, 0, "Ardean Law Chambers", "https://www.ardeanattorneys.co.tz/", ["info@ardeanattorneys.co.tz"]),
    ("ardeanlawchambers", "no_tenders", 0, 0, "Ardean Law Chambers", "https://www.ardeanlawchambers.co.tz/", ["info@ardeanlawchambers.co.tz"]),
    ("ardhismz", "error", 0, 0, "Wizara ya Ardhi na Maendeleo ya Makaazi", "https://ardhismz.go.tz/", ["info@ardhismz.go.tz"]),
    ("arepta", "no_tenders", 0, 0, "AREPTA", "https://arepta.or.tz/", ["info@arepta.or.tz", "valuation@arepta.or.tz", "refi@arepta.or.tz", "pfm@arepta.or.tz", "landadmin@arepta.or.tz"]),
    ("areteafrigroup", "no_tenders", 0, 0, "Arete Afrigroup", "https://areteafrigroup.co.tz/", ["info@areteafrigroup.co.tz"]),
    ("arfracompanyltd", "error", 0, 0, "Arfra Company Ltd", "https://arfracompanyltd.co.tz/", ["webmaster@arfracompanyltd.co.tz"]),
    ("arimo", "error", 0, 0, "Ardhi Institute Morogoro", "https://arimo.ac.tz/", ["daniel.chikaka@ega.go.tz"]),
    ("aris", "no_tenders", 0, 0, "ARiS Risk & Insurance Solutions", "https://aris-world.com/", ["tanzania@aris.co.tz", "arusha@aris.co.tz", "uganda@aris-world.com", "kenya@aris-world.com"]),
    ("arita", "error", 0, 0, "ARITA", "https://arita.ac.tz/", ["arita@arita.ac.tz"]),
    ("armadatech", "no_tenders", 0, 0, "Armada Tech", "https://armadatech.co.tz/", ["sales@armadatech.co.tz"]),
    ("armor", "no_tenders", 0, 0, "Armor Security Ltd", "https://www.armor.co.tz/", ["info@armor.co.tz"]),
    ("aru", "error", 0, 0, "Ardhi University", "https://aru.ac.tz/", ["aru@aru.ac.tz"]),
    ("arusha-archdiocese", "no_tenders", 0, 0, "Jimbo Kuu Katoliki Arusha", "https://arusha-archdiocese.or.tz/", ["carchd@arusha-archdiocese.or.tz"]),
    ("arushaart", "error", 0, 0, "Arusha Art Ltd", "https://arushaart.co.tz/", []),
    ("arushacarrental", "no_tenders", 0, 0, "Arusha Car Rental & Safaris", "https://arushacarrental.co.tz/", ["info@arushacarrental.co.tz"]),
    ("arushacitycollege", "no_tenders", 0, 0, "Arusha City Training College", "https://arushacitycollege.ac.tz/", ["info@arushacitycollege.ac.tz"]),
    ("arushafair", "no_tenders", 0, 0, "Arusha Christmas Fair", "https://www.arushafair.com/", ["info@arushafair.com"]),
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
    leads_to_append = []
    for slug, status, tender_count, doc_count, inst_name, website_url, emails in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last = {
            "run_id": RUN_ID,
            "scraped_at": NOW,
            "tender_url": website_url,
            "tender_count": tender_count,
            "doc_count": doc_count,
            "status": status,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last, f, indent=2)

        # scrape_log.json
        log_path = inst_dir / "scrape_log.json"
        log_entries = []
        if log_path.exists():
            with open(log_path) as f:
                log_entries = json.load(f)
        log_entries.append({
            "run_id": RUN_ID,
            "scraped_at": NOW,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
        })
        with open(log_path, "w") as f:
            json.dump(log_entries, f, indent=2)

        # leads for no_tenders (skip error/site down - still add for outreach potential)
        if status in ("no_tenders", "error") and emails:
            leads_to_append.append({
                "institution_slug": slug,
                "institution_name": inst_name,
                "website_url": website_url,
                "emails": [e for e in emails if "@" in e and ".jpg" not in e],
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
                "draft_email_body": DRAFT_BODY.format(institution_name=inst_name),
                "created_at": NOW,
                "status": "pending",
            })
        elif status in ("no_tenders", "error"):
            leads_to_append.append({
                "institution_slug": slug,
                "institution_name": inst_name,
                "website_url": website_url,
                "emails": [],
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
                "draft_email_body": DRAFT_BODY.format(institution_name=inst_name),
                "created_at": NOW,
                "status": "pending",
            })

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Append to leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}
    appended = 0
    for lead in leads_to_append:
        if lead["institution_slug"] not in existing_slugs:
            leads.append(lead)
            existing_slugs.add(lead["institution_slug"])
            appended += 1
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"\nAppended {appended} new leads. Total leads: {len(leads)}")


if __name__ == "__main__":
    main()
