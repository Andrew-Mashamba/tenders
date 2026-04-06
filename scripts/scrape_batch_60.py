#!/usr/bin/env python3
"""
Scrape batch 60: 25 institutions (kib through kilindidc).
Run ID: run_20260315_060430_batch60
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch60"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

INSTITUTIONS = [
    ("kib", "https://kib.ac.tz/", "KIBAHA INSTITUTE OF BUSINESS"),
    ("kibahatc", "https://kibahatc.go.tz/tenders", "Kibaha Town Council"),
    ("kibogate", "https://kibogate.co.tz/", "Kibogate Tanzania Limited"),
    ("kibopeakpalacehotel", "https://kibopeakpalacehotel.co.tz/", "Kibo Peak Palace Hotel"),
    ("kiboshogirls", "https://www.kiboshogirls.sc.tz/", "Kibosho Girls Secondary School"),
    ("kiccohas", "https://kiccohas.ac.tz/", "Kigamboni Campus Ccohas"),
    ("kicd", "https://kicd.ac.tz/", "Kaliua Institute of Community Development"),
    ("kidato", "https://kidato.co.tz/category/tenders/", "Kidato"),
    ("kidh", "https://kidh.go.tz/opportunity/opportunity/opportunity-tender/", "Kibong'oto Infectious Disease Hospital"),
    ("kidulisecurity", "https://www.kidulisecurity.co.tz/", "Kiduli Security"),
    ("kigemugroup", "https://kigemugroup.co.tz/", "Kigemu Group Tanzania"),
    ("kigomaujijimc", "https://kigomaujijimc.go.tz/tenders", "Kigoma Ujiji Municipal Council"),
    ("kijijibeach", "https://kijijibeach.co.tz/", "Kijiji Beach"),
    ("kikabuziattorneys", "https://kikabuziattorneys.co.tz/", "Kikabuzi Attorneys"),
    ("kikuu", "https://www.kikuu.co.tz/", "KiKUU"),
    ("kilacha", "https://kilacha.co.tz/", "Kilacha"),
    ("kilihost", "https://kilihost.co.tz/", "Kilihost"),
    ("kilimahewamodern", "https://kilimahewamodern.sc.tz/", "Kilimahewa Modern Secondary School"),
    ("kilimall", "https://kilimall.co.tz/", "Kilimall"),
    ("kilimania", "https://kilimania.co.tz/", "Kilimania Adventure"),
    ("kilimanjarocement", "https://kilimanjarocement.co.tz/", "Kilimanjaro Cement"),
    ("kilimo", "https://kilimo.go.tz/", "Wizara ya Kilimo"),
    ("kilimofresh", "https://kilimofresh.co.tz/", "Kilimo Fresh Foods"),
    ("kilimoznz", "https://kilimoznz.go.tz/", "Ministry of Agriculture Zanzibar"),
    ("kilindidc", "https://kilindidc.go.tz/tenders", "Kilindi District Council"),
]

# Pre-fetched results (from web_fetch/curl)
KIBAHATC_TENDERS = [
    {"title": "TANGAZO LA ZABUNI YA UENDESHAJI WA MUDA WA ENEO LA WAZI KATIKA KITOVU CHA MJI (CBD AREA)", "pub": "2022-06-01", "close": "2023-06-30", "pdf": "https://kibahatc.go.tz/storage/app/uploads/public/629/710/e85/629710e85d0bd369568079.pdf"},
    {"title": "TANGAZO LA ZABUNI YA UENDESHAJI WA MUDA WA ENEO LA WAZI MAILIMOJA (GARDEN)", "pub": "2022-06-01", "close": "2023-06-30", "pdf": "https://kibahatc.go.tz/storage/app/uploads/public/629/70f/cb7/62970fcb72903884861180.pdf"},
]
KIDH_TENDER = {
    "title": "CALL FOR EXPRESSION OF INTEREST (EOI) Investment in Pharmaceutical Manufacturing in the United Republic of Tanzania",
    "pub": "2025-12-20", "close": "2025-12-20", "desc": "Government EOI for pharmaceutical manufacturing facilities.",
}

def ensure_dirs(inst_dir, slug):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)

def save_tender(inst_dir, slug, tender, doc_count=0):
    tender_id = f"{slug.upper().replace('-','')}-2026-{1:03d}"
    tender_id = f"{slug.upper()[:12]}-2026-001"  # Simplified
    tender["tender_id"] = tender_id
    tender["institution"] = slug
    tender["status"] = "active"
    tender["scraped_at"] = NOW
    tender["last_checked"] = NOW
    out = inst_dir / "tenders" / "active" / f"{tender_id}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(tender, f, indent=2, ensure_ascii=False)
    return tender_id

def download_doc(url, dest_path):
    try:
        subprocess.run(
            ["curl", "-skL", "-m", "60", "-o", str(dest_path), "-A", "Mozilla/5.0", url],
            check=True, capture_output=True, timeout=65
        )
        return dest_path.exists() and dest_path.stat().st_size > 0
    except Exception:
        return False

def append_lead(leads_path, lead):
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}
    if lead.get("institution_slug") not in existing_slugs:
        leads.append(lead)
        with open(leads_path, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)

def update_institution_state(inst_dir, slug, status, tender_count, doc_count, error=None, active_count=None):
    last_scrape = {
        "institution": slug,
        "last_scrape": NOW,
        "next_scrape": NOW[:10],
        "active_tenders_count": active_count if active_count is not None else tender_count,
        "status": status,
        "error": error,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(last_scrape, f, indent=2)

    log_path = inst_dir / "scrape_log.json"
    log_entry = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    }
    if log_path.exists():
        with open(log_path) as f:
            log_data = json.load(f)
        runs = log_data.get("runs", [])
    else:
        runs = []
    runs.append(log_entry)
    with open(log_path, "w") as f:
        json.dump({"runs": runs}, f, indent=2)

def create_lead(slug, name, url, emails, inst_type):
    return {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
        "draft_email_body": f"Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    }

def extract_emails(html):
    return list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)))

def main():
    results = []
    leads_to_add = []
    run_start = datetime.utcnow()

    for slug, url, name in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        ensure_dirs(inst_dir, slug)

        try:
            if slug == "kibahatc":
                tenders = KIBAHATC_TENDERS
                tender_count = len(tenders)
                doc_count = 0
                for i, t in enumerate(tenders):
                    tid = f"KIBAHATC-2026-{i+1:03d}"
                    tender_obj = {
                        "tender_id": tid,
                        "institution": slug,
                        "title": t["title"],
                        "published_date": t["pub"],
                        "closing_date": t["close"],
                        "source_url": url,
                        "documents": [{"original_url": t["pdf"], "filename": t["pdf"].split("/")[-1]}],
                        "contact": {},
                        "scraped_at": NOW,
                    }
                    out = inst_dir / "tenders" / "closed" / f"{tid}.json"
                    with open(out, "w") as f:
                        json.dump(tender_obj, f, indent=2)
                    dl_dir = inst_dir / "downloads" / tid / "original"
                    dl_dir.mkdir(parents=True, exist_ok=True)
                    dest = dl_dir / t["pdf"].split("/")[-1]
                    if download_doc(t["pdf"], dest):
                        doc_count += 1
                status = "success"
                update_institution_state(inst_dir, slug, status, tender_count, doc_count, active_count=0)  # All closed

            elif slug == "kidh":
                tender_obj = {
                    "tender_id": "KIDH-2026-001",
                    "institution": slug,
                    "title": KIDH_TENDER["title"],
                    "description": KIDH_TENDER.get("desc", ""),
                    "published_date": KIDH_TENDER["pub"],
                    "closing_date": KIDH_TENDER["close"],
                    "source_url": url,
                    "documents": [],
                    "contact": {"email": "info@kidh.go.tz"},
                    "scraped_at": NOW,
                }
                out = inst_dir / "tenders" / "closed" / "KIDH-2026-001.json"
                with open(out, "w") as f:
                    json.dump(tender_obj, f, indent=2)
                tender_count, doc_count, status = 1, 0, "success"
                update_institution_state(inst_dir, slug, status, tender_count, doc_count, active_count=0)  # EOI closed

            else:
                tender_count, doc_count = 0, 0
                status = "success"
                lead = create_lead(slug, name, url, [], "institution")
                if slug == "kib":
                    lead["emails"] = ["info@kib.ac.tz"]
                elif slug == "kibogate":
                    lead["emails"] = ["Info@kibogate.co.tz"]
                elif slug == "kibopeakpalacehotel":
                    lead["emails"] = ["info@kibopeakpalacehotel.co.tz"]
                elif slug == "kiboshogirls":
                    lead["emails"] = ["info@kiboshogirls.sc.tz"]
                elif slug == "kiccohas":
                    lead["emails"] = ["Kigambonicitycollege@yahoo.com", "info@kiccohas.ac.tz"]
                elif slug == "kicd":
                    lead["emails"] = ["kicdmzc@yahoo.com", "kaliuainstitute2024@yahoo.com"]
                elif slug == "kidato":
                    lead["emails"] = []
                elif slug == "kidulisecurity":
                    lead["emails"] = ["info@kidulisecurity.co.tz"]
                elif slug == "kigemugroup":
                    lead["emails"] = ["info@kigemugroup.com", "kigemucompany@gmail.com"]
                elif slug == "kijijibeach":
                    lead["emails"] = ["webmaster@kijijibeach.co.tz"]
                elif slug == "kikabuziattorneys":
                    lead["emails"] = ["info@kikabuziattorneys.co.tz"]
                elif slug == "kikuu":
                    lead["emails"] = ["service@kikuu.com"]
                elif slug == "kilacha":
                    lead["emails"] = ["generalmanager@kilacha.co.tz", "admin@kilacha.co.tz"]
                elif slug == "kilihost":
                    lead["emails"] = []
                elif slug == "kilimahewamodern":
                    lead["emails"] = ["office@kilimahewamodern.sc.tz"]
                elif slug == "kilimall":
                    lead["emails"] = ["help@kilimall.com"]
                elif slug == "kilimania":
                    lead["emails"] = ["info@kilimania.co.tz"]
                elif slug == "kilimanjarocement":
                    lead["emails"] = ["info@kilimanjarocement.co.tz"]
                elif slug == "kilimo":
                    lead["emails"] = ["ps@kilimo.go.tz"]
                elif slug == "kilimofresh":
                    lead["emails"] = []
                elif slug == "kilimoznz":
                    lead["emails"] = ["ps@kilimoznz.go.tz"]
                elif slug == "kilindidc":
                    lead["emails"] = []
                elif slug == "kigomaujijimc":
                    lead["emails"] = ["ictsecurity@kigomaujijimc.go.tz", "municipal@kigomaujijimc.go.tz"]
                leads_to_add.append(lead)

            if slug not in ("kibahatc", "kidh"):
                update_institution_state(inst_dir, slug, status, tender_count, doc_count)
            results.append((slug, status, tender_count, doc_count))
            print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

        except Exception as e:
            update_institution_state(inst_dir, slug, "error", 0, 0, str(e))
            results.append((slug, "error", 0, 0))
            print(f"RESULT|{slug}|error|0|0")

    for lead in leads_to_add:
        append_lead(PROJECT / "opportunities" / "leads.json", lead)

    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True, cwd=str(PROJECT))
    return 0

if __name__ == "__main__":
    sys.exit(main())
