#!/usr/bin/env python3
"""Process scrape results for run_20260313_205329_batch119 - 25 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch119"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z")

# Institution slug -> (status, tender_count, doc_count, institution_name, website_url, emails[], error/notes)
RESULTS = {
    "thezhotel": ("success", 0, 0, "The Z Hotel Zanzibar", "https://www.thezhotel.com/", ["info@thezhotel.com"], None),
    "thinkmate": ("success", 0, 0, "Thinkmate", "https://thinkmate.co.tz/", ["admin@thinkmate.co.tz"], None),
    "thornflex": ("success", 0, 0, "Thornflex", "https://thornflex.co.tz/", ["info@thornflex.co.tz"], None),
    "thornlux": ("success", 0, 0, "Thornlux International Limited", "https://thornlux.co.tz/", ["md@thornlux.co.tz"], None),
    "thosma": ("success", 0, 0, "Thosma Logistics Limited", "https://thosma.co.tz/", ["info@thosma.co.tz", "zambia@thosma.co.zm"], None),
    "thrillton": ("success", 0, 0, "THRILLTON Consulting Limited", "https://thrillton.co.tz/", ["info@thrillton.co.tz", "info@thrilliton.co.tz"], None),
    "tht": ("error", 0, 0, "Tanzania House of Talents", "https://tht.co.tz/", [], "Site down (Cloudflare 521)"),
    "thtu": ("success", 0, 0, "THTU", "https://thtu.or.tz/", ["thtuhq@gmail.com", "thtuhq@thtu.or.tz"], None),
    "tia": ("success", 0, 0, "Tanzania Institute of Accountancy", "https://www.tia.ac.tz/", ["tia@tia.ac.tz"], None),
    "tiac": ("success", 0, 0, "TIAC", "https://tiac.or.tz/", ["info@tiac.or.tz", "info@tiac.co.tz"], None),
    "tib-development-bank": ("success", 0, 0, "TIB Development Bank", "https://www.tib.co.tz/", ["md@tib.co.tz"], "No tenders available"),
    "tibanova": ("success", 0, 0, "Tibanova", "https://tibanova.co.tz/", ["mawasiliano@truebitstech.com"], None),
    "ticc": ("success", 0, 0, "TALEMWA/TICC", "https://ticc.co.tz/", ["info@ticc.co.tz"], None),
    "tilenstyle": ("success", 0, 0, "Tile & Style", "https://tilenstyle.co.tz/", ["info@tilenstyle.co.tz"], None),
    "tim": ("success", 0, 0, "Tanzania Institute of Managers", "https://tim.co.tz/", ["sales@tim.co.tz"], None),
    "timbercraft": ("success", 0, 0, "Timbercraft", "https://timbercraft.co.tz/", [], None),
    "time": ("success", 0, 0, "Tanzania Institute of Monitoring and Evaluation", "https://time.ac.tz/", ["info@time.ac.tz"], None),
    "timeshorizon": ("success", 0, 0, "Times Horizon LTD", "https://timeshorizon.co.tz/", ["info@timeshorizon.co.tz"], None),
    "timesmajira": ("success", 0, 0, "Timesmajira", "https://timesmajira.co.tz/", [], None),
    "tip": ("success", 0, 0, "Tanzania Interfaith Partnership", "https://tip.or.tz/", ["info@tip.or.tz"], None),
    "tiper": ("success", 1, 1, "Tiper Tanzania Ltd", "https://tiper.co.tz/", ["info@tiper.co.tz"], None),  # 1 tender (closed), 1 doc
    "tipm": ("success", 0, 0, "Tanzania Institute of Project Management", "https://tipm.ac.tz/", ["info@tipm.ac.tz"], None),
    "tirdo": ("error", 0, 0, "TIRDO", "https://tirdo.or.tz/", ["help@tirdo.or.tz", "info@tirdo.or.tz"], "Fetch timed out"),
    "tirima": ("success", 0, 0, "Tirima Enterprises Limited", "https://tirima.co.tz/", ["info@tirima.co.tz"], None),
    "tirtec": ("error", 0, 0, "TIRtec", "https://tirtec.ac.tz/", ["webmaster@tirtec.ac.tz"], "Account suspended"),
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
    leads_added = []
    for slug, (status, tender_count, doc_count, name, url, emails, err) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last = {
            "institution": slug,
            "run_id": RUN_ID,
            "last_scrape": NOW,
            "status": status,
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2))

        # scrape_log.json - append
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            log_data = json.loads(log_path.read_text())
            if not isinstance(log_data, list):
                log_data = log_data.get("runs", [])
        else:
            log_data = []
        log_data.append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": status,
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        })
        log_path.write_text(json.dumps(log_data, indent=2))

        # Lead for no-tender institutions (exclude tiper which had 1 tender)
        if tender_count == 0 and slug not in ("tiper",):
            opp_desc = f"No formal tenders found on {name} website."
            if err:
                opp_desc += f" Note: {err}"
            else:
                opp_desc += " ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."

            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": url,
                "emails": [e for e in emails if e and "@" in e],
                "opportunity_type": "sell",
                "opportunity_description": opp_desc,
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": DRAFT_BODY.format(name=name),
                "created_at": NOW,
                "status": "pending",
            }
            leads_added.append(lead)

        # Print RESULT line
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    # Append leads to leads.json
    if leads_added:
        leads_path = PROJECT / "opportunities" / "leads.json"
        existing = []
        if leads_path.exists():
            raw = leads_path.read_text()
            if raw.strip():
                existing = json.loads(raw)
                if not isinstance(existing, list):
                    existing = existing.get("leads", [])
        existing.extend(leads_added)
        leads_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False))
        print(f"\nAppended {len(leads_added)} leads to opportunities/leads.json")


if __name__ == "__main__":
    main()
