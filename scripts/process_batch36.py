#!/usr/bin/env python3
"""Process scrape results for run_20260313_205329_batch36 - 25 institutions."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch36"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Scrape results: slug -> (status, tender_count, doc_count, error?, emails[])
RESULTS = {
    "ethicscommission": ("error", 0, 0, "Fetch timed out", []),
    "ethicssecretariat": ("no_tenders", 0, 0, None, ["ec@maadili.go.tz"]),
    "eto": ("no_tenders", 0, 0, None, ["info@eto.co.tz"]),
    "etumbi": ("no_tenders", 0, 0, None, []),  # protected
    "eurovision": ("no_tenders", 0, 0, None, ["info@eurovision.co.tz"]),
    "eventplannerstanzania": ("no_tenders", 0, 0, None, []),  # Instagram
    "evergrowing": ("no_tenders", 0, 0, None, ["evergrowing100@gmail.com"]),
    "everwellcable": ("no_tenders", 0, 0, None, ["info@everwellcable.co.tz", "info@everwellcable.com.cn"]),
    "everylivingthing": ("no_tenders", 0, 0, None, ["info@everylivingthing.or.tz"]),
    "evk": ("no_tenders", 0, 0, None, ["info@evk.co.tz"]),
    "evma": ("no_tenders", 0, 0, None, ["info@evma.co.tz", "Info@evma.co.tz"]),
    "evmak": ("no_tenders", 0, 0, None, []),
    "evolve": ("no_tenders", 0, 0, None, []),
    "ewallet": ("no_tenders", 0, 0, None, ["info@ewallet.co.tz"]),
    "ewura": ("error", 0, 0, "Fetch timed out", []),
    "exactehrm": ("no_tenders", 0, 0, None, []),
    "exactmanpower": ("no_tenders", 0, 0, None, []),
    "excelinternationalschool": ("no_tenders", 0, 0, None, ["info@excelinternationalschool.co.tz"]),
    "excellent-college": ("no_tenders", 0, 0, None, []),
    "eximbank": ("no_tenders", 0, 0, None, []),
    "explore": ("no_tenders", 0, 0, None, ["info@explore.co.tz"]),
    "exprimir": ("no_tenders", 0, 0, None, ["info@exprimir.co.tz"]),
    "extentadvisory": ("no_tenders", 0, 0, None, ["info@extentadvisory.co.tz"]),
    "extramile": ("error", 0, 0, "Account suspended", ["webmaster@extramile.co.tz"]),
    "extrateq": ("no_tenders", 0, 0, None, []),
}

INST_NAMES = {
    "ethicscommission": "Zanzibar Public Leaders' Ethics Commission",
    "ethicssecretariat": "Ethics Secretariat (Maadili)",
    "eto": "ETO (T) LTD",
    "etumbi": "Etumbi & Company",
    "eurovision": "EURO VISION COMPANY LTD",
    "eventplannerstanzania": "Event Planners Tanzania",
    "evergrowing": "Ever Growing Company Limited",
    "everwellcable": "Everwell Cables",
    "everylivingthing": "Every Living Thing",
    "evk": "EVK Certified Public Accountants",
    "evma": "EVMA Company Ltd",
    "evmak": "EvMak Tanzania",
    "evolve": "Evolve Technologies LTD",
    "ewallet": "eWallet Services Tanzania",
    "ewura": "EWURA",
    "exactehrm": "Exact - Human Resource Management System",
    "exactmanpower": "Exactmanpower",
    "excelinternationalschool": "Excel International School",
    "excellent-college": "Excellent College of Health and Allied Sciences",
    "eximbank": "Exim Bank Tanzania",
    "explore": "Explore Africa Travel",
    "exprimir": "Exprimir Company Limited",
    "extentadvisory": "Extent Corporate Advisory",
    "extramile": "Extramile",
    "extrateq": "Extrateq Company LTD",
}

WEBSITE_URLS = {
    "ethicscommission": "https://ethicscommission.go.tz/",
    "ethicssecretariat": "https://www.maadili.go.tz/",
    "eto": "https://eto.co.tz/",
    "etumbi": "https://etumbi.co.tz/",
    "eurovision": "https://eurovision.co.tz/",
    "eventplannerstanzania": "https://www.instagram.com/eventplannerstanzania",
    "evergrowing": "https://evergrowing.co.tz/",
    "everwellcable": "https://everwellcable.co.tz/",
    "everylivingthing": "https://www.everylivingthing.or.tz/",
    "evk": "https://evk.co.tz/",
    "evma": "https://evma.co.tz/",
    "evmak": "https://evmak.com/",
    "evolve": "https://evolve.co.tz/",
    "ewallet": "https://www.ewallet.co.tz/",
    "ewura": "https://ewura.go.tz/",
    "exactehrm": "https://exactehrm.co.tz/",
    "exactmanpower": "https://exactmanpower.co.tz/",
    "excelinternationalschool": "https://excelinternationalschool.co.tz/",
    "excellent-college": "https://excellent-college.ac.tz/",
    "eximbank": "https://eximbank.co.tz/tenders",
    "explore": "https://explore.co.tz/",
    "exprimir": "https://exprimir.co.tz/",
    "extentadvisory": "https://extentadvisory.co.tz/",
    "extramile": "https://extramile.co.tz/",
    "extrateq": "https://extrateq.co.tz/",
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
    new_leads = []
    summaries = []

    for slug, (status, tender_count, doc_count, error, emails) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": None,
            "active_tenders_count": tender_count,
            "status": "success" if status != "error" else "error",
            "error": error,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json
        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_data = json.load(f)
        else:
            log_data = {"runs": []}
        log_data["runs"].append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": "success" if status != "error" else "error",
            "tenders_found": tender_count,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [error] if error else [],
        })
        with open(scrape_log_path, "w") as f:
            json.dump(log_data, f, indent=2)

        # Summary line
        line = f"RESULT|{slug}|{status}|{tender_count}|{doc_count}"
        if error:
            line += f"|{error}"
        summaries.append(line)

        # Lead for no_tenders (with at least one email, or we add with empty emails)
        if status == "no_tenders":
            name = INST_NAMES.get(slug, slug)
            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": WEBSITE_URLS.get(slug, ""),
                "emails": list(dict.fromkeys(e for e in emails if e)),
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": DRAFT_BODY.format(name=name),
                "created_at": NOW,
                "status": "pending",
            }
            new_leads.append(lead)

    # Append to leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            leads = json.load(f)
    leads.extend(new_leads)
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    # Print summaries
    for s in summaries:
        print(s)
    print(f"\nAdded {len(new_leads)} new leads. Total leads: {len(leads)}")


if __name__ == "__main__":
    main()
