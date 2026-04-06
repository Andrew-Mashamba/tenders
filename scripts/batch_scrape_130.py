#!/usr/bin/env python3
"""Process scrape results for batch 130 - 25 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch130"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Scrape results: slug -> (tender_count, doc_count, status, error?)
# Based on web fetch analysis - NO institutions had formal tender listings
RESULTS = {
    "wonderland": (0, 0, "no_tenders", None),
    "worf": (0, 0, "no_tenders", None),
    "workforce": (0, 0, "no_tenders", None),
    "workoutzone": (0, 0, "no_tenders", None),
    "world-vision-global": (0, 0, "no_tenders", None),  # Page has header only, no listings
    "world-vision-tanzania": (0, 0, "error", "403 Forbidden"),
    "worldoil": (0, 0, "no_tenders", None),
    "wrifom": (0, 0, "no_tenders", None),
    "wrrb": (0, 0, "error", "SSL/certificate error"),
    "wsphelp": (0, 0, "no_tenders", None),
    "wss": (0, 0, "no_tenders", None),
    "www": (0, 0, "no_tenders", None),
    "wyi": (0, 0, "no_tenders", None),
    "xperiencetourstravel": (0, 0, "no_tenders", None),
    "yagete": (0, 0, "no_tenders", None),
    "yajukiinvestment": (0, 0, "no_tenders", None),
    "yamala": (0, 0, "no_tenders", None),
    "yandztechnology": (0, 0, "no_tenders", None),
    "yawe": (0, 0, "no_tenders", None),
    "yellow": (0, 0, "no_tenders", None),
    "yetuafrica": (0, 0, "no_tenders", None),
    "yid": (0, 0, "no_tenders", None),
    "yohannes": (0, 0, "no_tenders", None),  # School forms, not tenders
    "younginvestors": (0, 0, "no_tenders", None),
    "youngscientists": (0, 0, "no_tenders", None),
}

INST_CONFIG = {
    "wonderland": ("Wonderland Tours & Safaris", "https://wonderland.co.tz/", ["info@wonderland.co.tz", "tourism@wonderland.co.tz", "travel@wonderland.co.tz"]),
    "worf": ("Women In Recycling Foundation", "https://worf.or.tz/", ["info@worf.or.tz"]),
    "workforce": ("WORKFORCE", "https://workforce.co.tz/", []),
    "workoutzone": ("Workout Zone", "https://www.workoutzone.co.tz/", ["info@workoutzone.co.tz"]),
    "world-vision-global": ("World Vision International", "https://www.wvi.org/suppliers/tenders", []),
    "world-vision-tanzania": ("World Vision Tanzania", "https://www.wvi.org/tanzania/tenders", []),
    "worldoil": ("WORLD OIL LTD.", "https://worldoil.co.tz/", ["info@worldoil.co.tz"]),
    "wrifom": ("WRIFOM", "https://www.wrifom.or.tz/", ["info@wrifom.or.tz"]),
    "wrrb": ("WRRB", "https://wrrb.go.tz/", ["info@wrrb.go.tz"]),
    "wsphelp": ("WSP Tanzania", "https://wsphelp.or.tz/", ["info@wsphelp.or.tz"]),
    "wss": ("WSS", "https://wss.co.tz/", ["info@wss.co.tz"]),
    "www": ("www.co.tz | fruits", "https://www.co.tz/", ["hello@fruits.co"]),
    "wyi": ("Women and Youth Initiatives", "https://wyi.or.tz/", []),
    "xperiencetourstravel": ("Xperience Tours and Travels", "https://xperiencetourstravel.co.tz/", ["info@xperiencetourstravel.co.tz"]),
    "yagete": ("Yagete Group", "https://yagete.co.tz/", ["support@yagete.co.tz"]),
    "yajukiinvestment": ("YAJUKI", "https://yajukiinvestment.co.tz/", ["info@yajukiinvestment.co.tz"]),
    "yamala": ("Yamala Multimedia", "https://yamala.co.tz/", ["info@yamala.co.tz"]),
    "yandztechnology": ("Y AND Z TECHNOLOGY", "https://yandztechnology.co.tz/", []),
    "yawe": ("YAWE", "http://yawe.or.tz/", ["info@yawe.or.tz"]),
    "yellow": ("Yellow Tanzania", "https://yellow.co.tz/", ["jobs@yellowpageskenya.com", "info@yellowpageskenya.com"]),
    "yetuafrica": ("YetuAfrica", "https://yetuafrica.co.tz/", []),
    "yid": ("Youth Inclusion and Development", "https://www.yid.or.tz/", ["echizupa@gmail.com", "chairperson@yid.or.tz", "gs@yid.or.tz"]),
    "yohannes": ("Yohannes Secondary School", "https://yohannes.sc.tz/", []),
    "younginvestors": ("Younginvestors KE", "https://younginvestors.co.tz/", []),
    "youngscientists": ("Youngscientists", "https://youngscientists.co.tz/", ["info@youngscientists.co.tz"]),
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
    leads_to_append = []
    
    for slug, (tender_count, doc_count, status, err) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        
        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "documents_downloaded": doc_count,
            "status": "success" if status == "no_tenders" or tender_count > 0 else ("error" if status == "error" else "success"),
            "error": err,
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
        
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": "success" if status != "error" else "error",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        }
        log_data["runs"].append(log_entry)
        with open(scrape_log_path, "w") as f:
            json.dump(log_data, f, indent=2)
        
        # If no tenders (successful scrape) and not error: create opportunity lead
        if status == "no_tenders" and not err and slug in INST_CONFIG:
            name, url, emails = INST_CONFIG[slug]
            if not emails:
                emails = []
            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": url,
                "emails": emails,
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": DRAFT_BODY.format(name=name),
                "created_at": NOW,
                "status": "pending",
            }
            leads_to_append.append(lead)
        
        # Print summary
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
    
    # Append leads
    if leads_to_append:
        leads_path = PROJECT / "opportunities" / "leads.json"
        existing = []
        if leads_path.exists():
            with open(leads_path) as f:
                existing = json.load(f)
        existing.extend(leads_to_append)
        with open(leads_path, "w") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        print(f"\nAppended {len(leads_to_append)} leads to leads.json")
        return len(leads_to_append)
    return 0


if __name__ == "__main__":
    n = main()
    if n > 0:
        import subprocess
        subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True)
        print("Ran sync_leads_csv.py")
