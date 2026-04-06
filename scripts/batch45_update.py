#!/usr/bin/env python3
"""Update last_scrape, scrape_log, and leads for batch45 run."""
import json
from pathlib import Path
from datetime import datetime

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch45"
TS = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# Results: slug -> (status, tender_count, doc_count)
RESULTS = {
    "hawa": ("error", 0, 0),  # Site suspended
    "hawaii": ("success", 0, 0),
    "haydom": ("success", 1, 1),
    "hbtattorneys": ("success", 0, 0),
    "head2toeclinic": ("success", 0, 0),
    "heavengates": ("success", 0, 0),
    "heckilimanjarosafaris": ("success", 0, 0),
    "heet": ("success", 0, 0),
    "hekimawaldorfschool": ("success", 0, 0),
    "hellotz": ("success", 0, 0),
    "heritagefinancing": ("success", 0, 0),
    "heritageinsurance": ("success", 0, 0),
    "hertufarms": ("success", 0, 0),
    "heslb": ("success", 0, 0),
    "hesu": ("success", 0, 0),
    "hexad": ("success", 0, 0),
    "hexagon": ("success", 0, 0),
    "hibas": ("success", 0, 0),
    "hibiscus": ("success", 0, 0),
    "highmountschools": ("success", 0, 0),
    "hihs": ("success", 0, 0),
    "hillcrestauditors": ("success", 0, 0),
    "hillsidehotel": ("success", 0, 0),
    "hillviewhotel": ("success", 0, 0),
    "hilti": ("success", 0, 0),
}

INST_INFO = {
    "hawa": ("Account Suspended", "https://hawa.or.tz/", ["webmaster@hawa.or.tz"]),
    "hawaii": ("Hawaii Products Supplies Limited", "https://hawaii.co.tz/", ["Sales@hawaii.co.tz"]),
    "hbtattorneys": ("HBT Attorneys", "https://hbtattorneys.co.tz/", ["info@hbtattorneys.co.tz"]),
    "head2toeclinic": ("Jobama Head 2 Toe Physiotherapy Clinic", "https://head2toeclinic.co.tz/", ["info@head2toeclinic.co.tz"]),
    "heavengates": ("Heaven Gates Funeral Services", "http://heavengates.co.tz/", []),
    "heckilimanjarosafaris": ("HEC Kilimanjaro Safaris", "https://heckilimanjarosafaris.co.tz/", ["info@heckilimanjarosafaris.co.tz"]),
    "heet": ("HEET Tanzania", "https://heet.co.tz/", []),
    "hekimawaldorfschool": ("Hekima Waldorf School", "https://hekimawaldorfschool.ac.tz/", ["hekimawaldorfschool@gmail.com"]),
    "hellotz": ("Hellotz", "https://hellotz.co.tz/", ["info@hellotz.com", "karibu@hellotz.co.tz"]),
    "heritagefinancing": ("Heritage Financing Company Ltd", "https://heritagefinancing.co.tz/", []),
    "heritageinsurance": ("THE HERITAGE INSURANCE COMPANY TANZANIA LIMITED", "https://heritageinsurance.co.tz/", ["info@heritageinsurance.co.tz"]),
    "hertufarms": ("Hertu Mushrooms", "https://hertufarms.co.tz/", []),
    "heslb": ("HESLB", "https://www.heslb.go.tz/", ["info@heslb.go.tz"]),
    "hesu": ("Hesu | Integrated Logistics System", "https://hesu.co.tz/", ["info@hesu.co.tz"]),
    "hexad": ("Hexad", "https://hexad.co.tz/", ["contact@hexad.co.tz", "info@hexad.co.tz"]),
    "hexagon": ("Hexagon Consulting Limited", "https://hexagon.co.tz/", ["hello@hexagon.co.tz", "cloude@hexagon.co.tz"]),
    "hibas": ("Hibas Tanzania", "https://hibas.co.tz/", []),
    "hibiscus": ("Hibiscus Tours & Safari", "https://hibiscus.co.tz/", ["reservations@hibiscus.co.tz", "info@hibiscus.co.tz"]),
    "highmountschools": ("High Mount/High View Schools", "https://www.highmountschools.sc.tz/", []),
    "hihs": ("HIHS - Haydom Institute of Health Sciences", "https://hihs.ac.tz/", []),
    "hillcrestauditors": ("Hill Crest Auditors", "https://hillcrestauditors.co.tz/", ["info@hillcrestauditors.co.tz"]),
    "hillsidehotel": ("Hillside Hotel", "https://www.hillsidehotel.co.tz/", []),
    "hillviewhotel": ("Hill View Hotel", "https://hillviewhotel.co.tz/", ["info@hillview-hotel.com"]),
    "hilti": ("Hilti Tanzania", "https://www.hilti.co.tz/", []),
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
    inst_dir = PROJECT / "institutions"
    for slug, (status, tender_count, doc_count) in RESULTS.items():
        d = inst_dir / slug
        d.mkdir(parents=True, exist_ok=True)

        last = {
            "institution": slug,
            "last_scrape": TS,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "documents_downloaded": doc_count,
            "status": status,
            "error": "Site suspended" if slug == "hawa" else None,
        }
        (d / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

        log = {"runs": [{"run_id": RUN_ID, "timestamp": TS, "status": status, "tenders_found": tender_count, "documents_downloaded": doc_count, "errors": [last["error"]] if last["error"] else []}]}
        log_path = d / "scrape_log.json"
        if log_path.exists():
            data = json.loads(log_path.read_text(encoding="utf-8"))
            data["runs"].insert(0, log["runs"][0])
            log_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        else:
            log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Append leads for no-tender sites (all except haydom)
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = json.loads(leads_path.read_text(encoding="utf-8")) if leads_path.exists() else []
    existing_slugs = {l["institution_slug"] for l in leads}

    for slug in RESULTS:
        if slug == "haydom":
            continue
        if slug in existing_slugs:
            continue
        name, url, emails = INST_INFO.get(slug, (slug.replace("_", " ").title(), f"https://{slug}.co.tz/", []))
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on " + name + " website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(name=name),
            "created_at": TS,
            "status": "pending",
        }
        leads.append(lead)
        print(f"LEAD|{slug}|appended")

    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Leads saved.")


if __name__ == "__main__":
    main()
