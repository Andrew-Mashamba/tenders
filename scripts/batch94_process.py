#!/usr/bin/env python3
"""Process batch94 scrape results: add leads for no-tender institutions, update scrape state."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"
RUN_ID = "run_20260313_205329_batch94"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Institutions with NO tenders - add as leads (slug, name, url, emails)
NO_TENDER = [
    ("qualitywater", "Quality Water & Sanitation", "https://qualitywater.co.tz/", ["info@qualitywater.co.tz"]),
    ("qualtrust", "Qualtrust Company Limited", "http://www.qualtrust.co.tz/", ["info@qualtrust.co.tz"]),
    ("quantum", "QI Group", "https://qigroup.tz/", ["info@qigroup.tz"]),
    ("quantumarchitects", "Quantum Space Architects", "https://quantumarchitects.co.tz/", ["info@quantumarchitects.co.tz"]),
    ("quantumresearch", "quantumresearch", "https://quantumresearch.co.tz/", ["info@quantumresearch.co.tz"]),
    ("queensgem", "Queens Gem & Jewellery", "https://www.queensgem.co.tz/", ["sales@queensgem.co.tz"]),
    ("quickstepinvestment", "Quick Step Investment", "https://quickstepinvestment.co.tz/", ["info@quickinvestment.co.tz"]),
    ("quixgroup", "Quix Group", "https://quixgroup.co.tz/", ["info@quixgroup.co.tz", "edyson@quixgroup.co.tz"]),
    ("raawu", "RAAWU", "https://raawu.or.tz/", ["info@raawu.or.tz"]),
    ("rabikafarm", "Rabika Farm", "https://rabikafarm.co.tz/", ["zahor@rabikafarm.co.tz"]),
    ("radarsecurity", "Radar Security Tanzania", "https://radarsecurity.co.tz/", ["info@radarsecurity.co.tz", "support@radarsecurity.co.tz"]),
    ("radian", "Radian", "https://www.radian.co.tz/", ["info@radian.co.tz"]),
    ("radio1", "RadioOne", "https://radio1.co.tz/", []),
    ("radio5fm", "RADIO 5 FM", "https://www.radio5fm.co.tz/", ["info@radio5fm.co.tz"]),
    ("radiojoyfm", "JOY FM", "https://radiojoyfm.co.tz/", ["producer@radiojoy.co.tz", "admin@radiojoyfm.co.tz"]),
    ("radiokicheko", "Radio Kicheko Live", "https://radiokicheko.co.tz/", ["info@radiokicheko.co.tz"]),
    ("radiokwizera", "radiokwizera", "https://radiokwizera.co.tz/", []),
    ("radiowave", "Radiowave Communications LTD", "https://radiowave.co.tz/", ["sales@radiowave.co.tz", "salescentre@radiowave.co.tz"]),
    ("rafikiattorneys", "Rafiki Attorneys", "https://rafikiattorneys.co.tz/", ["info@rafikiattorneys.co.tz"]),
    ("rahamiagri", "Rahami Agri Group", "https://www.rahamiagri.co.tz/", ["info@rahamiagri.co.tz"]),
    ("rai", "Rai", "https://rai.co.tz/", []),
    ("rainoenterprise", "Raino Enterprise", "https://rainoenterprise.co.tz/", []),
    ("raissa", "Raissa Company Limited", "https://www.raissa.co.tz/", []),
    ("raitech", "Rai Technologies", "https://raitech.co.tz/", ["info@raitech.co.tz"]),
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


def lead_exists(leads: list, slug: str) -> bool:
    return any(l.get("institution_slug") == slug for l in leads)


def main():
    # Load leads
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    added = 0
    for slug, name, url, emails in NO_TENDER:
        if lead_exists(leads, slug):
            continue
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(name=name),
            "created_at": NOW,
            "status": "pending",
        }
        leads.append(lead)
        added += 1

    with open(LEADS_JSON, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print(f"Added {added} leads to {LEADS_JSON}")


if __name__ == "__main__":
    main()
