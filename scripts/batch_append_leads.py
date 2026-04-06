#!/usr/bin/env python3
"""Append batch of leads to opportunities/leads.json and update institution scrape state."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"
RUN_ID = "run_20260313_205329_batch65"

# 25 institutions: slug, name, website_url, emails (from README contact)
INSTITUTIONS = [
    ("lembainvestments", "Lemba Investment Company limited", "https://lembainvestments.co.tz/",
     ["info@lembainvestments.co.tz", "lemba@lembainvestment.co.tz", "info@lembainvestment.co.tz"]),
    ("lenic", "Lenic Tanzania Limited", "https://lenic.co.tz/", ["info@lenic.co.tz"]),
    ("lensgroup", "Len's Group", "https://lensgroup.co.tz/", ["info@lensgroup.co.tz"]),
    ("leotours", "LEO TOURS | Leo Tours Co.Ltd", "https://leotours.co.tz/", ["info@leotours.co.tz"]),
    ("lesasaccos", "Lesa Saccos Ltd", "https://lesasaccos.or.tz/", []),
    ("lesotech", "Lesotech", "https://lesotech.co.tz/", ["info@lesotech.co.tz"]),
    ("levictronics", "Levi Electronics", "https://levictronics.co.tz/", ["sales@levictronics.co.tz"]),
    ("lexacto", "Lexacto Attorneys", "https://www.lexacto.co.tz/", ["info@lexacto.co.tz"]),
    ("lhc", "London Health Centre", "https://www.lhc.co.tz/", []),
    ("libegreeninnovation", "Libe Green Innovation", "https://libegreeninnovation.co.tz/", ["info@libegreeninnovation.co.tz"]),
    ("libertygroup", "Liberty Group", "https://libertygroup.co.tz/", ["fc@libertygrouptz.com", "info@libertygrouptz.com"]),
    ("liebherr", "Liebherr", "https://www.liebherr.com/", []),
    ("lifehope", "Life and Hope Rehabilitation Organization", "https://lifehope.or.tz/", []),
    ("lilac", "LILAC", "https://lilac.co.tz/", ["znhellar@lilac.co.tz", "onanyaro@lilac.co.tz", "info@lilac.co.tz"]),
    ("linexattorneys", "Linex Attorneys", "https://www.linexattorneys.co.tz/", ["info@linexattorneys.co.tz"]),
    ("linktech", "Link-Tech Company Ltd", "https://www.linktech.co.tz/", ["info@linktech.co.tz"]),
    ("lipaz", "LIPAZ Consultants Limited", "https://lipaz.co.tz/", ["info@divilayouts.store", "info@lipaz.co.tz"]),
    ("liquidhome", "Liquid Home Tanzania", "https://www.liquidhome.co.tz/", []),
    ("lita", "LITA (Livestock Training Agency)", "https://lita.go.tz/", ["daniel.chikaka@ega.go.tz", "info@lita.go.tz"]),
    ("litcotattorneys", "Litcot Attorneys", "https://litcotattorneys.co.tz/", ["info@litcotattorneys.co.tz"]),
    ("liz-wachuka", "Liz H. Wachuka", "https://www.liz-wachuka.co.tz/", []),
    ("lmc", "LMC (Lutheran Mission Cooperation)", "https://lmc.or.tz/", []),
    ("locktechsolutions", "Locktech Security Systems", "https://locktechsolutions.co.tz/", []),
    ("logistixware", "LogistixWare", "https://logistixware.co.tz/", ["info@logistixware.co.tz"]),
    ("loliondocoach", "Loliondo Coach", "https://loliondocoach.co.tz/", ["loliondocoach559@gmail.com"]),
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
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Load existing leads
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    # Append new leads
    for slug, name, url, emails in INSTITUTIONS:
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(institution_name=name),
            "created_at": now,
            "status": "pending",
        }
        leads.append(lead)

    with open(LEADS_JSON, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"Appended {len(INSTITUTIONS)} leads to {LEADS_JSON}")

    # Update last_scrape.json and scrape_log.json for each institution
    for slug, name, url, _ in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "next_scrape": now,
            "active_tenders_count": 0,
            "status": "success",
            "error": None,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json - append
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            with open(log_path) as f:
                log_data = json.load(f)
            runs = log_data.get("runs", [])
        else:
            runs = []

        runs.append({
            "run_id": RUN_ID,
            "timestamp": now,
            "duration_seconds": 0,
            "status": "success",
            "tenders_found": 0,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": 0,
            "errors": [],
        })

        with open(log_path, "w") as f:
            json.dump({"runs": runs}, f, indent=2)

    print(f"Updated last_scrape.json and scrape_log.json for {len(INSTITUTIONS)} institutions")


if __name__ == "__main__":
    main()
