#!/usr/bin/env python3
"""Process scrape results for run_20260315_060430_batch2 - 25 institutions."""
import json
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch2"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# Tenders found
TENDERS = [
    {
        "slug": "acbbank",
        "tenders": [
            {
                "tender_id": "ACBBANK-2026-001",
                "title": "Supplier Prequalification Notice 2026-2027",
                "description": "Akiba Commercial Bank supplier prequalification for 2026-2027.",
                "published_date": "2025-11-12",
                "closing_date": None,
                "source_url": "https://www.acbbank.co.tz/tenders",
                "document_urls": ["https://www.acbbank.co.tz/pdfviewer/supplier-prequalification-notice-2026-2027/"],
                "contact": {"email": "info@acbbank.co.tz", "phone": "0800 750 336"},
            }
        ],
    },
    {
        "slug": "actanzania",
        "tenders": [
            {
                "tender_id": "ACTANZANIA-2026-001",
                "title": "CALL FOR PROPOSALS: Independent audit of the Council's 2024 financial report",
                "description": "ACT invites proposals from qualified audit firms to conduct independent audit of Council's 2024 financial report. Submission window: 7 days from 28 Nov 2025.",
                "published_date": "2025-11-28",
                "closing_date": "2025-12-05",
                "source_url": "https://actanzania.or.tz/index.php/act-news-media/74-independent-audit-of-the-council's-2024-financial-report",
                "document_urls": [
                    "https://actanzania.or.tz/index.php/files/49/New-category/89/CALL-FOR-PROPOSAL-ACT.pdf",
                    "https://actanzania.or.tz/index.php/files/49/New-category/90/Audit-ToR-ACT.pdf",
                ],
                "contact": {"email": "act@actanzania.or.tz", "phone": "+255 719 260 726"},
            }
        ],
    },
]

# Institutions with no tenders - create leads
NO_TENDER_INSTITUTIONS = [
    {"slug": "abyatravel", "name": "Abya Travel Tours & Safaris", "url": "https://abyatravel.co.tz/", "emails": ["info@abyatravel.co.tz"]},
    {"slug": "aceleatherafrica", "name": "Ace Leather Tanzania", "url": "https://aceleatherafrica.co.tz/", "emails": ["info@aceleatherafrica.co.tz"]},
    {"slug": "aces", "name": "ACES", "url": "https://aces.co.tz/", "emails": ["info@abyatravel.co.tz"]},
    {"slug": "acet", "name": "Association of Consulting Engineers Tanzania", "url": "https://www.acet.or.tz/", "emails": []},
    {"slug": "achelis", "name": "Achelis (Tanganyika) Limited", "url": "https://achelis.co.tz/", "emails": []},
    {"slug": "acmlining", "name": "ACM Lining", "url": "https://acmlining.co.tz/", "emails": ["webmaster@acmlining.co.tz"], "error": "Account suspended"},
    {"slug": "adctanzania", "name": "ADC Tanzania Ltd", "url": "https://www.adctanzania.co.tz/", "emails": ["Info@adctanzania.co.tz", "info@adctanzania.co.tz"]},
    {"slug": "addranafoods", "name": "Addrana Foods", "url": "https://addranafoods.co.tz/", "emails": []},
    {"slug": "adelante", "name": "Adelante", "url": "https://adelante.co.tz/", "emails": ["info@adelante.co.tz"], "error": "Fetch timeout"},
    {"slug": "adelphos", "name": "Adelphos", "url": "https://adelphos.co.tz/", "emails": ["info@adelphos.co.tz", "help@consultiocleaning.com"]},
    {"slug": "adem", "name": "ADEM", "url": "https://adem.ac.tz/", "emails": ["adem@adem.ac.tz"], "error": "Fetch timeout"},
    {"slug": "ademarkltd", "name": "Ademark Company Limited", "url": "http://ademarkltd.co.tz/", "emails": ["ademark.co.ltd@gmail.com", "info@ademarkltd.co.tz", "info@ademarkltd.com"]},
    {"slug": "adifit", "name": "Adifit", "url": "https://adifit.co.tz/", "emails": ["info@adifit.co.tz"]},
    {"slug": "adlg", "name": "Actions for Democracy and Local Governance", "url": "https://adlg.or.tz/", "emails": ["ceo@adlg.or.tz", "info@adlg.or.tz"]},
    {"slug": "admark", "name": "Admark", "url": "https://admark.co.tz/", "emails": [], "error": "Site under construction"},
    {"slug": "admireoil", "name": "Admire Oil Limited", "url": "http://admireoil.co.tz/", "emails": [], "error": "Fetch timeout"},
    {"slug": "adonailogistics", "name": "Adonai Logistics Limited", "url": "https://adonailogistics.co.tz/", "emails": ["sales@adonailogistics.co.tz"]},
    {"slug": "adroittech", "name": "Adroit Tech", "url": "https://adroittech.co.tz/", "emails": [], "error": "Tenders directory empty"},
    {"slug": "advaitinc", "name": "Advait INC", "url": "https://advaitinc.co.tz/", "emails": []},
    {"slug": "advancedlogistics", "name": "Advanced Courier & Logistics Ltd", "url": "https://advancedlogistics.co.tz/", "emails": ["sales@advancedlogistics.co.tz", "baraka.mlewa@advancedlogistics.co.tz"]},
    {"slug": "advansmart", "name": "Advansmart Business Consultants", "url": "https://www.advansmart.co.tz/", "emails": ["info@advansmart.co.tz"]},
    {"slug": "adventuremakers", "name": "Adventure Makers", "url": "https://www.adventuremakers.co.tz/", "emails": ["info@adventuremakers.co.tz"]},
    {"slug": "adventurepark", "name": "Mikumi Adventure Lodge", "url": "https://adventurepark.co.tz/", "emails": ["info@adventurepark.co.tz"]},
]

DRAFT_EMAIL = """Dear {name} Team,

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


def download_file(url, dest):
    """Download file from URL to dest path."""
    try:
        r = requests.get(url, timeout=60, allow_redirects=True, headers={"User-Agent": "TENDERS-Scraper/1.0"})
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"  Download failed {url}: {e}")
        return False


def main():
    results = []
    new_leads = []

    # Process tenders
    for inst in TENDERS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        tenders_dir = inst_dir / "tenders" / "active"
        downloads_dir = inst_dir / "downloads"
        tenders_dir.mkdir(parents=True, exist_ok=True)

        doc_count = 0
        for t in inst["tenders"]:
            tender_id = t["tender_id"]
            tender_json = {
                "tender_id": tender_id,
                "institution": slug,
                "title": t["title"],
                "description": t["description"],
                "published_date": t.get("published_date"),
                "closing_date": t.get("closing_date"),
                "status": "active",
                "source_url": t["source_url"],
                "documents": [],
                "contact": t.get("contact", {}),
                "scraped_at": NOW,
                "last_checked": NOW,
            }

            # Download documents
            for i, doc_url in enumerate(t.get("document_urls", [])):
                if doc_url.endswith(".pdf"):
                    ext = ".pdf"
                    fname = f"{tender_id}_{i+1}{ext}"
                else:
                    ext = ".html" if "pdfviewer" in doc_url else ".pdf"
                    fname = f"{tender_id}_notice{ext}"
                orig_dir = downloads_dir / tender_id / "original"
                orig_dir.mkdir(parents=True, exist_ok=True)
                dest = orig_dir / fname
                if download_file(doc_url, dest):
                    doc_count += 1
                    tender_json["documents"].append({
                        "filename": fname,
                        "original_url": doc_url,
                        "local_path": str(dest.relative_to(inst_dir)),
                        "downloaded_at": NOW,
                    })

            (inst_dir / "tenders" / "active" / f"{tender_id}.json").write_text(
                json.dumps(tender_json, indent=2), encoding="utf-8"
            )

        # Update last_scrape and scrape_log
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": "2026-03-16T06:00:00Z",
            "active_tenders_count": len(inst["tenders"]),
            "status": "success",
            "error": None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")

        scrape_log = []
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            data = json.loads(log_path.read_text(encoding="utf-8"))
            scrape_log = data if isinstance(data, list) else data.get("runs", [])
        scrape_log.append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": "success",
            "tenders_found": len(inst["tenders"]),
            "new_tenders": len(inst["tenders"]),
            "documents_downloaded": doc_count,
            "errors": [],
        })
        log_path.write_text(json.dumps(scrape_log, indent=2), encoding="utf-8")

        results.append((slug, "success", len(inst["tenders"]), doc_count))
        print(f"RESULT|{slug}|success|{len(inst['tenders'])}|{doc_count}")

    # Process no-tender institutions
    for inst in NO_TENDER_INSTITUTIONS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        # Create lead
        lead = {
            "institution_slug": slug,
            "institution_name": inst["name"],
            "website_url": inst["url"],
            "emails": [e for e in inst.get("emails", []) if e and "@" in str(e)],
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services. {inst.get('error', '')}".strip(),
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
            "draft_email_body": DRAFT_EMAIL.format(name=inst["name"]),
            "created_at": NOW,
            "status": "pending",
        }
        new_leads.append(lead)

        # Update last_scrape
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": "2026-03-16T06:00:00Z",
            "active_tenders_count": 0,
            "status": "error" if inst.get("error") else "success",
            "error": inst.get("error"),
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")

        scrape_log = []
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            data = json.loads(log_path.read_text(encoding="utf-8"))
            scrape_log = data if isinstance(data, list) else data.get("runs", [])
        scrape_log.append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": "success",
            "tenders_found": 0,
            "errors": [inst["error"]] if inst.get("error") else [],
        })
        log_path.write_text(json.dumps(scrape_log, indent=2), encoding="utf-8")

        results.append((slug, "no_tenders" if not inst.get("error") else "error", 0, 0))
        print(f"RESULT|{slug}|no_tenders|0|0")

    # Append leads to leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        leads = json.loads(leads_path.read_text(encoding="utf-8"))
        if not isinstance(leads, list):
            leads = leads.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}
    for lead in new_leads:
        if lead["institution_slug"] not in existing_slugs:
            leads.append(lead)
            existing_slugs.add(lead["institution_slug"])
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

    # Run sync_leads_csv
    os.chdir(PROJECT)
    os.system("python3 scripts/sync_leads_csv.py")

    return results


if __name__ == "__main__":
    main()
