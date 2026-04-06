#!/usr/bin/env python3
"""Append leads for batch22 institutions with no tenders."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"

# institution_slug, institution_name, website_url, emails[]
LEADS_DATA = [
    ("chinyami", "Chinyami Limited", "https://chinyami.co.tz/", ["info@chinyami.co.tz"]),
    ("cholemjini", "Chole Mjini Treehouse Lodge", "https://www.cholemjini.com/", []),
    ("chora-interiors", "Chora Interiors", "https://chora-interiors.co.tz/", ["info@chora-interiors.co.tz"]),
    ("chragg", "Commission for Human Rights and Good Governance", "https://chragg.go.tz/", ["info@chragg.go.tz"]),
    ("christadelphian", "Wakristadelfiani wa Tanzania", "https://www.christadelphian.or.tz/", []),
    ("church", "Church.co.tz - CDMS", "https://church.co.tz/", ["info@church.co.tz"]),
    ("chuwaadvocates", "Chuwa Advocates", "https://chuwaadvocates.co.tz/", ["e.chuwa@chuwaadvocates.co.tz"]),
    ("cib", "Corporate Insurance Brokers Ltd", "https://cib.co.tz/", ["info@cib.co.tz"]),
    ("cit", "Creative Inter Traders", "https://cit.co.tz/", ["info@cit.co.tz"]),
    ("citigroup-suppliers", "Citigroup Global Suppliers Portal", "https://www.citigroup.com/global/our-impact/suppliers", []),
    ("cits", "Flex Corporate Services Limited", "https://www.flex.co.tz/", ["frontdesk@flex.co.tz"]),
    ("city-tech", "City-Tech Engineering Co.Ltd", "https://city-tech.co.tz/", ["sales@city-tech.co.tz"]),
    ("citycom", "Citycom", "https://citycom.co.tz/", []),
    ("citylinkhotel", "City Link Pentagon Hotel", "https://citylinkhotel.co.tz/", []),
    ("claretianpublications", "Claretian Publications (CCC)", "https://claretianpublications.or.tz/", []),
    ("clarion", "Clarion Advisory", "https://clarion.co.tz/", ["info@clarion.co.tz"]),
    ("clasktanzania", "Clask Tanzania", "https://clasktanzania.co.tz/", ["info@clasktanzania.co.tz"]),
    ("clc", "Common Law Chambers", "https://clc.co.tz/", ["info@clc.co.tz"]),
    ("cleaningmaster", "Cleaning Master Co. Ltd", "https://cleaningmaster.co.tz/", ["info@cleaningmaster.co.tz"]),
    ("clickpayafrica", "Click Pay Africa", "https://clickpayafrica.co.tz/", []),
    ("climateair", "Climate Air Limited", "https://climateair.co.tz/", []),
    ("climbkilimanjaro", "Shah Tours - Climb Kilimanjaro", "https://www.shah-tours.com/", ["info@shah-tours.com"]),
    ("climtech", "Climtech", "https://climtech.co.tz/", ["info@climtech.co.tz"]),
    ("cmadvocates", "C&M Advocates", "https://cmadvocates.co.tz/", []),
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
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    existing_slugs = {l.get("institution_slug") for l in leads}
    created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    added = 0
    for slug, name, url, emails in LEADS_DATA:
        if slug in existing_slugs:
            continue
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on {} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.".format(name),
            "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & {}".format(name.split(" - ")[0].split(" | ")[0]),
            "draft_email_body": DRAFT_BODY.format(name=name.split(" - ")[0].split(" | ")[0]),
            "created_at": created_at,
            "status": "pending",
        }
        leads.append(lead)
        added += 1

    with open(LEADS_JSON, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"Appended {added} new leads to leads.json")

if __name__ == "__main__":
    main()
