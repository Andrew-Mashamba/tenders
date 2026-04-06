#!/usr/bin/env python3
"""Append leads for batch 122 institutions (no tenders found)."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"

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

LEADS = [
    ("transafrica", "Trans Africa Insurance Brokers", "https://transafrica.co.tz/", []),
    ("transec", "Transec", "https://transec.co.tz/", ["enquiries@transec-tz.com"]),
    ("transpac", "Transpac Logistics", "https://transpac.co.tz/", ["info@transpac.co.tz"]),
    ("transplant", "Transplant Consultants (T) Ltd", "https://transplant.co.tz/", ["sales@transplant.co.tz"]),
    ("trantruck", "TranTruck Limited", "https://trantruck.co.tz/", []),
    ("travelhype", "Travel Hype Adventures", "https://travelhype.co.tz/", []),
    ("traveltrack", "Travel Track", "https://traveltrack.co.tz/", ["airport@traveltrack.co.tz", "info@traveltrack.co.tz", "bookings@traveltrack.co.tz"]),
    ("trc", "TRC (Tanzania Railways)", "https://trc.co.tz/", []),
    ("trendymedia", "Trendy Media", "https://trendymedia.co.tz/", ["sales@trendymedia.co.tz"]),
    ("triniti", "Triniti", "https://triniti.co.tz/", []),
    ("trinitylogistics", "Trinity Logistics", "https://trinitylogistics.co.tz/", []),
    ("trinityschools", "Trinity Pre and Primary School", "https://trinityschools.ac.tz/", ["Info@trinityschools.ac.tz"]),
    ("trinitysolar", "Trinity Solar Energy", "https://trinitysolar.co.tz/", ["info@trinitysolar.co.tz"]),
    ("tripleafricaadventures", "Triple Africa Adventures", "https://tripleafricaadventures.co.tz/", []),
    ("trisoftnet", "Trisoftnet", "https://trisoftnet.co.tz/", []),
    ("trix", "Trix Furniture", "https://trix.co.tz/", ["sales@trix.co.tz"]),
    ("trmega", "TRMEGA", "https://trmega.or.tz/", ["info@trmega.or.tz"]),
    ("tro", "Office of the Registrar of Organizations (TRO)", "https://tro.go.tz/", ["info@tro.go.tz"]),
    ("trueimage", "True Image Undertaking Investment", "https://trueimage.co.tz/", []),
    ("truemaisha", "TrueMaisha Consulting Group", "https://truemaisha.co.tz/", ["info@truemaisha.co.tz"]),
    ("tutume", "Tutume", "https://tutume.co.tz/", ["welcome@tutume.co.tz"]),
    ("tva", "Tanzania Veterinary Association", "https://www.tva.or.tz/", []),
    ("tvla", "Tanzania Veterinary Laboratory Agency", "https://tvla.go.tz/", ["info@tvla.go.tz"]),
]


def main():
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing = {l.get("institution_slug") for l in leads}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    added = 0
    for slug, name, url, emails in LEADS:
        if slug in existing:
            continue
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(name=name),
            "created_at": now,
            "status": "pending",
        }
        leads.append(lead)
        existing.add(slug)
        added += 1
    with open(LEADS_JSON, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print(f"Appended {added} new leads to leads.json")


if __name__ == "__main__":
    main()
