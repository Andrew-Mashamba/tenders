#!/usr/bin/env python3
"""Process scrape results for batch19 - 25 institutions with no tenders, add leads."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch19"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

INSTITUTIONS = [
    ("buy4me", "Buy For Me - Buy 4 Me Powered by Proship Logistics", "https://buy4me.co.tz/"),
    ("buyforme", "Buy For Me - Buy 4 Me Powered by Proship Logistics", "https://buy4me.co.tz/"),
    ("bvk", "BVK Logistics", "https://bvk.co.tz/"),
    ("bytrade", "ByTrade Tanzania", "https://bytrade.or.tz/"),
    ("c-labs", "C-Labs", "https://c-labs.co.tz/"),
    ("cacla", "Cacla Engineering Limited", "https://www.cacla.co.tz/"),
    ("calfoniahills", "Calfonia Hills Secondary School", "https://calfoniahills.ac.tz/"),
    ("camara", "Camara Education Tanzania", "https://camara.or.tz/"),
    ("camartec", "CAMARTEC", "https://www.camartec.go.tz/"),
    ("candorventure", "Candor Venture", "https://candorventure.co.tz/"),
    ("canocity", "Canocity - Canon Dealers", "https://canocity.co.tz/"),
    ("canossa", "Canossa High School", "https://canossa.ac.tz/"),
    ("capitalcitymarathon", "Capital City Marathon", "https://capitalcitymarathon.co.tz/"),
    ("capitaltechnologies", "Capital Technologies", "https://www.capitaltechnologies.co.tz/"),
    ("caps", "Caps Limited Tanzania", "http://caps.co.tz/"),
    ("capuchin", "Capuchin Franciscans Tanzania", "https://capuchin.or.tz/"),
    ("cardiocare", "Cardiocare Tanzania Limited", "https://cardiocare.co.tz/"),
    ("caretech", "CARETECH IT SOLUTIONS", "https://caretech.co.tz/"),
    ("careworth", "Careworth Limited", "https://careworth.co.tz/"),
    ("cargopoint", "CARGO POINT", "https://cargopoint.co.tz/"),
    ("carhouse", "Carhouse", "https://carhouse.co.tz/"),
    ("carjunction", "Car Junction Tanzania", "https://carjunction.co.tz/"),
    ("carnivoressafaris", "Carnivores Safaris", "https://carnivoressafaris.co.tz/"),
    ("cartrack", "Cartrack Tanzania", "https://cartrack.co.tz/"),
    ("casco", "CASCO Construction LTD", "https://casco.co.tz/"),
]

# Emails scraped from READMEs / sites
EMAILS = {
    "buy4me": [],
    "buyforme": [],
    "bvk": ["info@bvk.co.tz"],
    "bytrade": ["info@bytrade.or.tz"],
    "c-labs": ["c.labstz@gmail.com", "info@C-Labs.co.tz"],
    "cacla": ["md@cacla.co.tz"],
    "calfoniahills": ["info@calfoniahills.ac.tz"],
    "camara": [],
    "camartec": ["dg@camartec.go.tz"],
    "candorventure": [],
    "canocity": ["sales@canocity.co.tz"],
    "canossa": ["info@canossa.ac.tz", "canossahighsch@gmail.com"],
    "capitalcitymarathon": ["webmaster@capitalcitymarathon.co.tz"],
    "capitaltechnologies": ["info@capitaltechnologies.co.tz"],
    "caps": ["admin@caps.co.tz"],
    "capuchin": ["capuchindsm@gmail.com"],
    "cardiocare": ["info@cardiocare.co.tz"],
    "caretech": ["info@caretech.co.tz"],
    "careworth": ["info@careworth.co.tz"],
    "cargopoint": ["info@cargopoint.co.tz"],
    "carhouse": ["info@carhouse.co.tz"],
    "carjunction": ["info@carjunction.co.tz"],
    "carnivoressafaris": ["info@carnivoressafaris.co.tz"],
    "cartrack": ["sales@cartrack.co.tz"],
    "casco": ["info@casco.co.tz"],
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

# Sites with known fetch issues (suspended, timeout, empty)
FETCH_ERRORS = {
    "capitalcitymarathon": "Account suspended",
    "candorventure": "Fetch timeout",
    "canocity": "Fetch timeout",
    "caps": "Empty page",
}


def main():
    leads_to_append = []
    
    for slug, name, url in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        
        fetch_err = FETCH_ERRORS.get(slug)
        status = "error" if fetch_err else "success"
        
        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": 0,
            "status": status,
            "error": fetch_err,
            "tenders_found": 0,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)
        
        # scrape_log.json - append
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            with open(log_path) as f:
                log = json.load(f)
        else:
            log = {"runs": []}
        
        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": status,
            "tenders_found": 0,
            "new_tenders": 0,
            "documents_downloaded": 0,
            "errors": [fetch_err] if fetch_err else [],
        })
        with open(log_path, "w") as f:
            json.dump(log, f, indent=2)
        
        # Lead for opportunities
        emails = EMAILS.get(slug, [])
        if "|" in name:
            short_name = name.split("|")[0].strip()
        elif " - " in name or " – " in name:
            short_name = name.split(" - ")[0].split(" – ")[0].strip()
        else:
            short_name = " ".join(name.split()[:3]) if name else name
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {short_name}",
            "draft_email_body": DRAFT_BODY.format(name=short_name),
            "created_at": NOW,
            "status": "pending",
        }
        leads_to_append.append(lead)
        
        result_status = "error" if fetch_err else "no_tenders"
        print(f"RESULT|{slug}|{result_status}|0|0")
    
    # Append to leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    if leads_path.exists():
        with open(leads_path) as f:
            leads = json.load(f)
    else:
        leads = []
    
    if not isinstance(leads, list):
        leads = leads.get("leads", [])
    
    leads.extend(leads_to_append)
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    
    print(f"\nAppended {len(leads_to_append)} leads. Running sync_leads_csv.py...")
    
    import subprocess
    subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True)


if __name__ == "__main__":
    main()
