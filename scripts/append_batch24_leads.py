#!/usr/bin/env python3
"""Append opportunity leads for batch24 institutions with no tenders."""
import json
from pathlib import Path
from datetime import datetime

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"

# 22 institutions with no tenders - from READMEs
LEADS = [
    {"slug": "conveyance", "name": "Conveyance - Logistics & Containers", "url": "https://conveyance.co.tz/", "emails": ["info@conveyance.co.tz", "sales@conveyance.co.tz"]},
    {"slug": "cordex", "name": "Cordex – Softwares Products", "url": "https://cordex.co.tz/", "emails": []},
    {"slug": "coreit", "name": "coreit.co.tz", "url": "https://coreit.co.tz/", "emails": []},
    {"slug": "coresecurities", "name": "CORE Securities Ltd", "url": "https://www.coresecurities.co.tz/", "emails": ["info@coresecurities.co.tz"]},
    {"slug": "cornerstone", "name": "Cornerstone Solution", "url": "https://cornerstone.co.tz/", "emails": []},
    {"slug": "cosota", "name": "COSOTA", "url": "https://cosota.go.tz/", "emails": ["barua@cosota.go.tz"]},
    {"slug": "costbenchmark", "name": "Costbenchmark", "url": "https://costbenchmark.co.tz/", "emails": ["info@costbenchmark.co.tz"]},
    {"slug": "cotech", "name": "Cotech Developers", "url": "https://cotech.co.tz/", "emails": ["info@cotech.co.tz"]},
    {"slug": "cottonclub", "name": "Cotton Club", "url": "https://cottonclub.co.tz/", "emails": ["cotton@cottonclubtz.com"]},
    {"slug": "coyesa", "name": "Coyesa", "url": "https://coyesa.co.tz/", "emails": ["coyesa2015@gmail.com", "info@coyesa.co.tz"]},
    {"slug": "coyeta", "name": "CoYETa", "url": "https://coyeta.ac.tz/", "emails": ["nyehunge@gmail.com"]},
    {"slug": "cpat", "name": "CPA Associates", "url": "https://cpat.co.tz/", "emails": ["info@cpat.co.tz"]},
    {"slug": "cpb", "name": "CPB", "url": "https://cpb.go.tz/", "emails": ["info@cpb.go.tz"]},
    {"slug": "cpctanzania", "name": "CPC Tanzania Limited", "url": "https://cpctanzania.co.tz/", "emails": ["info@cpctanzania.co.tz"]},
    {"slug": "cpi", "name": "Comenius Polytechnic Institute", "url": "https://cpi.ac.tz/", "emails": []},
    {"slug": "cps", "name": "CPS Limited", "url": "https://www.cps.co.tz/", "emails": ["info@cps.co.tz"]},
    {"slug": "cqs", "name": "CQS", "url": "https://cqs.co.tz/", "emails": ["info@cqs.co.tz", "tangojt@cqs.co.tz"]},
    {"slug": "craftmasterbuilders", "name": "Craft Master Builders Limited", "url": "https://craftmasterbuilders.co.tz/", "emails": ["info@craftmasterbuilders.co.tz"]},
    {"slug": "cranetrader", "name": "CraneTrader.com", "url": "https://www.cranetrader.com/", "emails": ["feedback@cranetrader.com"]},
    {"slug": "cravason", "name": "Cravason & Associates", "url": "https://cravason.co.tz/", "emails": ["info@cravason.co.tz"]},
    {"slug": "crb", "name": "Contractors Registration Board", "url": "https://crb.go.tz/", "emails": ["crbhq@crbtz.org", "crbhq@crb.go.tz"]},
    {"slug": "crbafricalegal", "name": "CRB Africa Legal", "url": "https://crbafricalegal.co.tz/", "emails": ["info@crbafricalegal.co.tz"]},
]

def main():
    with open(LEADS_JSON) as f:
        leads = json.load(f)
    
    created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000000Z")
    body = """Dear {name} Team,

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
    
    existing_slugs = {l.get("institution_slug") for l in leads}
    added = 0
    for l in LEADS:
        if l["slug"] in existing_slugs:
            continue
        lead = {
            "institution_slug": l["slug"],
            "institution_name": l["name"],
            "website_url": l["url"],
            "emails": l["emails"],
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {l['name']}",
            "draft_email_body": body.format(name=l["name"]),
            "created_at": created,
            "status": "pending"
        }
        leads.append(lead)
        added += 1
    
    with open(LEADS_JSON, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    
    print(f"Appended {added} new leads to leads.json")

if __name__ == "__main__":
    main()
