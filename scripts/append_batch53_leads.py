#!/usr/bin/env python3
"""Append batch53 leads to opportunities/leads.json"""
import json
from pathlib import Path
from datetime import datetime

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"
RUN_ID = "run_20260313_205329_batch53"

# Lead data: slug, name, url, emails[], opportunity_type, opportunity_description
LEADS = [
    ("itrack", "Home - My Blog", "https://itrack.co.tz/", [], "sell", "No tenders. AI/tech blog. ZIMA could offer AI strategy, ML solutions, NLP."),
    ("itransport", "Account Suspended", "https://itransport.co.tz/", ["webmaster@itransport.co.tz"], "sell", "Site suspended. Transport/logistics. ZIMA could offer fleet management, digital transformation."),
    ("itss", "I T S S – IT Sales and Services", "https://itss.co.tz/", [], "sell", "No tenders. IT company Dar es Salaam. ZIMA could partner on ICT solutions."),
    ("itstars", "IT Stars Enterprises", "https://itstars.co.tz/", ["info@itstars.co.tz"], "sell", "No tenders. IT company: web hosting, software dev, training. ZIMA could partner on fintech/SACCO systems."),
    ("itsupport", "Account Suspended", "https://itsupport.co.tz/", ["webmaster@itsupport.co.tz"], "sell", "Site suspended. IT support. ZIMA could offer digital transformation."),
    ("itv", "ITV - Independent Television", "https://www.itv.co.tz/", [], "sell", "No tenders. TV broadcaster. ZIMA could offer media tech, digital platforms."),
    ("iyangroup", "IYAN GROUP", "https://iyangroup.co.tz/", ["info@yourbusiness.com"], "sell", "No tenders. Freight, insurance, logistics. ZIMA could offer fleet IoT, digital systems."),
    ("jadon", "Jadon Limited", "https://jadon.co.tz/", ["info@jadon.co.tz", "cinfo@jadon.co.tz"], "sell", "No tenders. Civil, electrical, telecom contractors. ZIMA could offer ICT/security systems integration."),
    ("jafferyacademy", "Jaffery Academy", "https://jafferyacademy.co.tz/", [], "sell", "No tenders. International school Arusha. ZIMA could offer school management system."),
    ("jafrexsystems", "JAFREX Systems", "https://jafrexsystems.co.tz/", ["support@jafrexsystems.co.tz", "info@jafrexsystems.co.tz"], "sell", "No tenders. Electronics, telecom, ICT. ZIMA could partner on fintech, IoT."),
    ("jaire", "Jaire Company Ltd", "http://jaire.co.tz/", [], "sell", "No tenders. ICT consultancy, catering, office supplies. ZIMA could partner on software development."),
    ("jamaap", "Jamaap Co. LTD", "https://jamaap.co.tz/", ["info@jamaap.co.tz"], "sell", "No tenders. Freight forwarding, customs. ZIMA could offer logistics digital systems."),
    ("jambo", "Jambo TV Online", "https://jambo.co.tz/", ["moidinya@gmail.com"], "sell", "No tenders. TV/news. ZIMA could offer media tech, digital platforms."),
    ("jambotelematics", "JAMBO TELEMATICS", "https://jambotelematics.co.tz/", ["info@jambotelematics.co.tz"], "partner", "No tenders. IoT fleet management. ZIMA could partner on BOT/fintech integrations."),
    ("jamhurimedia", "Gazeti la Jamhuri", "https://www.jamhurimedia.co.tz/", [], "sell", "No tenders. News/media. ZIMA could offer digital publishing, media tech."),
    ("jamhuristationers", "Jamhuri Stationery", "https://jamhuristationers.co.tz/", ["sales@jamhuristationers.co.tz"], "sell", "No tenders. Stationery, IT products. ZIMA could offer POS, inventory systems."),
    ("jamii", "MoCDGWSG - Ministry of Community Development", "https://jamii.go.tz/publications/tenders", ["ps@jamii.go.tz"], "sell", "Tender page timed out. Government ministry. ZIMA could offer digital systems for community development."),
    ("jamiimedia", "Jamii Media Tanzania", "https://jamiimedia.co.tz/", [], "sell", "No tenders. Media/development. ZIMA could offer tech adoption, digital solutions."),
    ("jamsolutions", "JamSolutions", "https://jamsolutions.co.tz/", ["info@jamsolutions.co.tz"], "sell", "No tenders. ICT, catering, train parts. ZIMA could partner on software, GoT revenue systems."),
    ("janstevensinternational", "JANSTEVENS INTERNATIONAL LIMITED", "https://janstevensinternational.co.tz/", ["info@janstevensinternational.co.tz"], "sell", "No tenders. Piping, mechanical, fire systems. ZIMA could offer project management software."),
    ("jaomaffl", "Jaoma Freight Forwarders Limited", "https://jaomaffl.co.tz/", [], "sell", "No tenders. Customs clearing, freight. ZIMA could offer logistics digital systems."),
    ("jasecinvestment", "Jasec Investment", "https://jasecinvestment.co.tz/", ["info@jasecinvestment.co.tz"], "sell", "No tenders. Gypsum, agricultural products. ZIMA could offer supply chain, ERP."),
    ("jasmai", "Jasmai Media Solutions", "https://jasmai.co.tz/", ["info@jasmai.co.tz"], "sell", "No tenders. Web, mobile, graphics, printing. ZIMA could partner on fintech apps."),
    ("jassociates", "Jonas & Associates Law Chamber", "https://jassociates.co.tz/", ["info@jassociates.co.tz"], "sell", "No tenders. Law firm. ZIMA could offer legal practice management, document systems."),
    ("jaynir", "JAYNIR – CREATIVE . WEB . GRAPHIC . AUDIO . VIDEO", "https://jaynir.co.tz/", ["info@jaynir.com"], "sell", "No tenders. Creative, web, graphics. ZIMA could partner on digital solutions."),
]

DRAFT_BODY = """Dear {name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions, government agencies, and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

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
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    for slug, name, url, emails, otype, desc in LEADS:
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": otype,
            "opportunity_description": desc,
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name.split(' - ')[0].split(' |')[0]}",
            "draft_email_body": DRAFT_BODY.format(name=name.split(' - ')[0].split(' |')[0]),
            "created_at": now,
            "status": "pending",
        }
        leads.append(lead)

    with open(LEADS_JSON, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print(f"Appended {len(LEADS)} leads. Total: {len(leads)}")

if __name__ == "__main__":
    main()
