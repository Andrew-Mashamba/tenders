#!/usr/bin/env python3
"""Process 25 institutions for run_20260315_060430_batch65 - update scrape state and print summaries."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch65"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

INSTITUTIONS = [
    ("lands", "success", 4, 4),  # Already has 4 tenders from prior scrape
    ("landtribunalsmz", "no_tenders", 0, 0),
    ("lapwings", "no_tenders", 0, 0),
    ("las", "no_tenders", 0, 0),
    ("lastanarhotel", "no_tenders", 0, 0),
    ("latra", "error", 0, 0),  # nest.go.tz SPA - requires JS
    ("laureate", "no_tenders", 0, 0),
    ("lavano", "no_tenders", 0, 0),
    ("lavazza", "no_tenders", 0, 0),
    ("lavenderdaycare", "no_tenders", 0, 0),
    ("lavicato", "no_tenders", 0, 0),
    ("lawage", "no_tenders", 0, 0),
    ("lawficattorneys", "no_tenders", 0, 0),
    ("lawhill", "no_tenders", 0, 0),
    ("lawhut", "no_tenders", 0, 0),
    ("lcg", "no_tenders", 0, 0),
    ("lds", "no_tenders", 0, 0),
    ("leadingedgeresources", "no_tenders", 0, 0),
    ("learningheights", "no_tenders", 0, 0),
    ("lecriconsult", "no_tenders", 0, 0),
    ("leeraschool", "no_tenders", 0, 0),
    ("legacymall", "error", 0, 0),  # Account suspended
    ("legendaryexpeditions", "no_tenders", 0, 0),
    ("lel", "no_tenders", 0, 0),
    ("lembainvestments", "no_tenders", 0, 0),
]

# Institutions that need NEW leads (not already in leads.json)
NEW_LEAD_SLUGS = {"landtribunalsmz", "latra"}

INST_NAMES = {
    "lands": "MLHHSD | Mwanzo",
    "landtribunalsmz": "The Land Tribunal Zanzibar",
    "lapwings": "Lapwings – Africa Safaris Expert",
    "las": "LAS – Clearing & Forwarding",
    "lastanarhotel": "La Stanar Hotel",
    "latra": "LATRA",
    "laureate": "Laureate International School",
    "lavano": "Lavano Holidays",
    "lavazza": "Capsule Machines | Suvacor Ltd",
    "lavenderdaycare": "LAVENDER DAY CARE CENTER",
    "lavicato": "LAVICATO – Venue, Events & Catering",
    "lawage": "Law Age Advocate",
    "lawficattorneys": "Lawfic Attorneys",
    "lawhill": "Lawhill",
    "lawhut": "Law Hut",
    "lcg": "LOREME CONSULTING GROUP",
    "lds": "Lock and Door System",
    "leadingedgeresources": "Leading Edge Resources",
    "learningheights": "Learning Heights",
    "lecriconsult": "Lecri Consult",
    "leeraschool": "Leera Schools",
    "legacymall": "Legacy Mall",
    "legendaryexpeditions": "Legendary Expeditions",
    "lel": "LAB EQUIP LTD",
    "lembainvestments": "Lemba Investment Company",
}

INST_URLS = {
    "lands": "https://lands.go.tz/",
    "landtribunalsmz": "https://landtribunalsmz.go.tz/Tender",
    "lapwings": "https://lapwings.co.tz/",
    "las": "https://las.co.tz/",
    "lastanarhotel": "https://lastanarhotel.co.tz/",
    "latra": "https://nest.go.tz/tenders/published-tenders?search=land%20transport%20regulatory%20authority",
    "laureate": "https://laureate.or.tz/",
    "lavano": "https://lavano.co.tz/",
    "lavazza": "https://www.suvacor.com/",
    "lavenderdaycare": "https://lavenderdaycare.co.tz/",
    "lavicato": "https://lavicato.co.tz/",
    "lawage": "https://lawage.co.tz/",
    "lawficattorneys": "https://www.lawficattorneys.co.tz/",
    "lawhill": "https://lawhill.co.tz/",
    "lawhut": "https://lawhut.co.tz/",
    "lcg": "https://lcg.co.tz/",
    "lds": "https://www.lds.co.tz/",
    "leadingedgeresources": "https://www.leadingedgeresources.co.tz/",
    "learningheights": "https://learningheights.co.tz/",
    "lecriconsult": "https://lecriconsult.co.tz/",
    "leeraschool": "https://leeraschool.ac.tz/",
    "legacymall": "https://legacymall.co.tz/",
    "legendaryexpeditions": "https://www.legendaryexpeditions.co.tz/",
    "lel": "https://lel.co.tz/",
    "lembainvestments": "https://lembainvestments.co.tz/",
}

INST_EMAILS = {
    "landtribunalsmz": ["info@landtribunalsmz.go.tz"],
    "latra": ["info@latra.go.tz"],
}


def draft_email_body(inst_name: str) -> str:
    return f"""Dear {inst_name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {inst_name}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
"""


def main():
    results = []
    leads_to_append = []

    for slug, status, tender_count, doc_count in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        # Update last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW[:10] + "T06:00:00Z",
            "active_tenders_count": tender_count,
            "status": "success" if status == "success" else ("error" if status == "error" else "no_tenders"),
            "error": "Site requires JavaScript (NeST SPA)" if slug == "latra" else ("Account suspended" if slug == "legacymall" else None),
            "run_id": RUN_ID,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")

        # Update scrape_log.json
        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            log_data = json.loads(scrape_log_path.read_text(encoding="utf-8"))
        else:
            log_data = {"runs": []}
        log_data["runs"].append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": "success" if status in ("success", "no_tenders") else "error",
            "tenders_found": tender_count,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [last_scrape["error"]] if last_scrape["error"] else [],
        })
        scrape_log_path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

        # Create lead for new institutions (landtribunalsmz, latra)
        if slug in NEW_LEAD_SLUGS:
            opp_desc = "No formal tenders found. LATRA uses NeST (SPA); Land Tribunal Zanzibar has no tender listings. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."
            if slug == "latra":
                opp_desc = "LATRA tenders are on nest.go.tz (National e-Procurement System) which requires JavaScript. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."
            elif slug == "landtribunalsmz":
                opp_desc = "No formal tenders found on Land Tribunal Zanzibar website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."
            leads_to_append.append({
                "institution_slug": slug,
                "institution_name": INST_NAMES.get(slug, slug),
                "website_url": INST_URLS.get(slug, ""),
                "emails": INST_EMAILS.get(slug, []),
                "opportunity_type": "sell",
                "opportunity_description": opp_desc,
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {INST_NAMES.get(slug, slug)}",
                "draft_email_body": draft_email_body(INST_NAMES.get(slug, slug)),
                "created_at": NOW,
                "status": "pending",
            })

        results.append((slug, status, tender_count, doc_count))

    # Append new leads to leads.json
    if leads_to_append:
        leads_path = PROJECT / "opportunities" / "leads.json"
        leads = json.loads(leads_path.read_text(encoding="utf-8")) if leads_path.exists() else []
        if not isinstance(leads, list):
            leads = leads.get("leads", [])
        existing_slugs = {l.get("institution_slug") for l in leads}
        for lead in leads_to_append:
            if lead["institution_slug"] not in existing_slugs:
                leads.append(lead)
                existing_slugs.add(lead["institution_slug"])
        leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print summary lines
    for slug, status, tender_count, doc_count in results:
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    return len(leads_to_append)


if __name__ == "__main__":
    n = main()
    if n > 0:
        import subprocess
        subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True, cwd=str(PROJECT))
