#!/usr/bin/env python3
"""Process batch74 scrape results for 26 institutions."""
import json
import os
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch74"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

INSTITUTIONS = [
    ("mexicoconsulate", "Secretaría de Relaciones Exteriores | Gobierno | gob.mx", "https://www.gob.mx/", "error", 0, 0, "403 Forbidden"),
    ("mezani", "Home | Mezani", "https://www.mezani.co.tz/", "no_tenders", 0, 0, None),
    ("mfgroup", "MF Group – Freight Forwarding & Logistics", "https://mfgroup.co.tz/", "no_tenders", 0, 0, None),
    ("mfhsti", "MKOLANI FOUNDATION HEALTH SCIENCES TRAINING INSTITUTE", "https://mfhsti.ac.tz/", "no_tenders", 0, 0, None),
    ("mfinangacargo", "MCGT", "https://mfinangacargo.co.tz/", "no_tenders", 0, 0, None),
    ("mfukowamisitu", "TaFF | MFUKO WA MISITU TANZANIA", "https://mfukowamisitu.go.tz/", "error", 0, 0, "Timeout/SSL"),
    ("mgentanzania", "Mgen Tanzania – Insurance company", "https://mgentanzania.co.tz/", "no_tenders", 0, 0, None),
    ("mgl", "mgl.co.tz", "https://mgl.co.tz/", "error", 0, 0, "Timeout"),
    ("mgt", "MTEWELE GENERAL TRADERS", "https://mgt.co.tz/", "no_tenders", 0, 0, None),
    ("mhalobeachlodge", "Mhalo Beach Lodge", "https://mhalobeachlodge.co.tz/", "no_tenders", 0, 0, None),
    ("mhangolegalconsultants", "MHANGO Legal Consultants", "https://mhangolegalconsultants.co.tz/", "no_tenders", 0, 0, None),
    ("mhbbank", "Mwanga Hakika Bank Limited", "https://mhbbank.co.tz/", "no_tenders", 0, 0, None),
    ("mhondatc", "Ministry of Water Water Institute", "https://mhondatc.ac.tz/", "error", 0, 0, "Timeout"),
    ("mhti", "Machame Health Training Institute", "https://mhti.ac.tz/procurement/", "no_tenders", 0, 0, None),
    ("micglobalrisks", "MIC GLOBAL RISKS", "https://www.micglobalrisks.co.tz/", "no_tenders", 0, 0, None),
    ("michezo", "WHUSM | Ministry of Sports", "https://michezo.go.tz/", "error", 0, 0, "Timeout"),
    ("michezozanzibar", "Idara ya Michezo Zanzibar", "https://michezozanzibar.go.tz/", "no_tenders", 0, 0, None),
    ("micrence", "Account Suspended", "https://micrence.co.tz/", "error", 0, 0, "Account suspended"),
    ("microsafi", "Portal Home - microsafi.com", "https://dhs.microsafi.com/", "no_tenders", 0, 0, None),
    ("mifugouvuvi", "MLF | Wizara ya Mifugo na Uvuvi", "https://mifugouvuvi.go.tz/", "no_tenders", 0, 0, None),
    ("mighty", "Mighty Logistics Tanzania Limited", "https://mighty.co.tz/", "no_tenders", 0, 0, None),
    ("migotechnologies", "miGO Technologies EA Limited", "https://migotechnologies.co.tz/", "no_tenders", 0, 0, None),
    ("mihas", "MLIMBA INSTITUTE OF HEALTH AND ALLIED SCIENCE", "https://mihas.ac.tz/", "no_tenders", 0, 0, None),
    ("mikonoyetu", "MikonoYetu", "https://mikonoyetu.or.tz/", "no_tenders", 0, 0, None),
    ("mil", "Multiplier International Ltd", "http://mil.co.tz/", "no_tenders", 0, 0, None),
]

# Emails scraped from each site (from READMEs and fetched content)
EMAILS = {
    "mexicoconsulate": ["atencionciudadana@sre.gob.mx"],
    "mezani": ["mezanimkahawa@gmail.com"],
    "mfgroup": ["info@mfgroup.co.tz"],
    "mfhsti": ["mkolanifoundation@yahoo.com"],
    "mfinangacargo": [],
    "mfukowamisitu": ["info@mfukowamisitu.go.tz"],
    "mgentanzania": ["info@mgentanzania.co.tz"],
    "mgl": ["info@mgl.co.tz", "Info@mgl.co.tz"],
    "mgt": ["info@mgt.co.tz"],
    "mhalobeachlodge": ["info@mhalobeachlodge.co.tz", "mhalobeachlodge@gmail.com"],
    "mhangolegalconsultants": ["info@muhangolegalconsultants.co.tz", "jeme@jeme.it"],
    "mhbbank": ["info@mhbbank.co.tz"],
    "mhondatc": ["rector@waterinstitute.ac.tz"],
    "mhti": ["info@mhti.ac.tz", "admission@mhti.ac.tz"],
    "micglobalrisks": [],
    "michezo": ["km@michezo.go.tz"],
    "michezozanzibar": ["info@michezozanzibar.go.tz"],
    "micrence": ["webmaster@micrence.co.tz"],
    "microsafi": [],
    "mifugouvuvi": ["barua@mlf.go.tz"],
    "mighty": ["info@mighty.co.tz"],
    "migotechnologies": ["info@migotechnologies.co.tz"],
    "mihas": ["mlimbacollege@gmail.com", "info@mlimba.ac.tz"],
    "mikonoyetu": ["mikonoyeu@gmail.com"],
    "mil": ["kroger@mil.co.tz"],
}

def valid_email(e):
    return e and "@" in e and not any(x in e.lower() for x in [".jpg", ".png", "profile.php", "sharer"])

def main():
    leads_to_append = []
    summaries = []

    for slug, name, url, status, tender_count, doc_count, err in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "status": "success" if status == "no_tenders" or status == "tenders" else "error",
            "error": err,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json
        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log = json.load(f)
        else:
            log = {"runs": []}
        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": "success" if status != "error" else "error",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "error": err,
        })
        with open(scrape_log_path, "w") as f:
            json.dump(log, f, indent=2)

        # For no_tenders: append to leads
        if status == "no_tenders":
            emails = [e for e in EMAILS.get(slug, []) if valid_email(e)]
            if not emails and slug in EMAILS:
                emails = [e for e in EMAILS[slug] if valid_email(e)]
            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": url,
                "emails": list(set(emails)),
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, ICT services, or partnership opportunities.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name[:40]}",
                "draft_email_body": f"""Dear {name} Team,

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
""",
                "created_at": NOW,
                "status": "pending",
            }
            leads_to_append.append(lead)

        # Summary line
        status_str = status if status != "no_tenders" else "no_tenders"
        summaries.append(f"RESULT|{slug}|{status_str}|{tender_count}|{doc_count}")

    # Append to leads.json
    if leads_to_append:
        leads_path = PROJECT / "opportunities" / "leads.json"
        with open(leads_path) as f:
            leads = json.load(f)
        leads.extend(leads_to_append)
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)

    # Print summaries
    for s in summaries:
        print(s)

if __name__ == "__main__":
    main()
