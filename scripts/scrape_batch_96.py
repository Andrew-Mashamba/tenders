#!/usr/bin/env python3
"""
Scrape batch 96: 25 institutions (reeftours through reynatours).
Run ID: run_20260313_205329_batch96
"""
import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch96"

INSTITUTIONS = [
    {"slug": "reeftours", "name": "Reef Tours and Travel", "url": "https://reeftours.co.tz/", "emails": ["info@reeftours.co.tz"]},
    {"slug": "refined", "name": "Refined Advisory", "url": "https://www.refined.co.tz/", "emails": []},
    {"slug": "refixit", "name": "Refixit", "url": "https://www.refixit.co.tz/", "emails": ["hello@refixit.co.tz"]},
    {"slug": "registry", "name": "registry.co.tz", "url": "https://registry.co.tz/", "emails": ["accreditation@registry.co.tz"]},
    {"slug": "rehoboth", "name": "Rehoboth", "url": "https://rehoboth.co.tz/", "emails": ["info@rehoboth.co.tz"]},
    {"slug": "reign", "name": "Reign", "url": "https://reign.co.tz/", "emails": ["info@reign.co.tz"]},
    {"slug": "reigroup", "name": "REI GROUP", "url": "https://reigroup.co.tz/", "emails": ["reilogistics@yahoo.com"]},
    {"slug": "relevance", "name": "Relevance Consultancy", "url": "https://relevance.co.tz/", "emails": ["info@relevance.co.tz"]},
    {"slug": "reliance", "name": "Reliance", "url": "https://reliancetz.com/", "emails": ["insure@reliance.co.tz"]},
    {"slug": "reliancegroup", "name": "Reliance Group Tanzania", "url": "https://reliancegroup.co.tz/", "emails": ["info@reliancegroup.co.tz"]},
    {"slug": "relish", "name": "Relish Enthusiast Adventures", "url": "https://relish.co.tz/", "emails": []},
    {"slug": "remodel", "name": "Remodel", "url": "https://www.remodel.or.tz/", "emails": ["frg8kt@virginia.edu"]},
    {"slug": "reni", "name": "reni.co.tz", "url": "https://reni.co.tz/", "emails": ["help@reni.co.tz"]},
    {"slug": "repoa", "name": "REPOA", "url": "https://repoa.or.tz/category/tenders/", "emails": ["repoa@repoa.or.tz"], "has_tenders": True},
    {"slug": "reputable", "name": "Reputable Holdings", "url": "https://reputable.co.tz/", "emails": ["reputabletz@gmail.com", "info@reputable.co.tz"]},
    {"slug": "resa", "name": "Resa Medical Group", "url": "https://resa.co.tz/", "emails": ["info@resa.co.tz"]},
    {"slug": "resco", "name": "RESCO", "url": "https://www.resco.co.tz/", "emails": ["info@resco.co.tz"]},
    {"slug": "resilienceacademy", "name": "Resilience Academy", "url": "https://resilienceacademy.ac.tz/", "emails": ["resilienceacademytz@gmail.com"]},
    {"slug": "ressourcen", "name": "Ressourcen", "url": "https://www.ressourcen.co.tz/", "emails": ["hello@ressourcen.co.tz"]},
    {"slug": "restlessdevelopment", "name": "Restless Development", "url": "https://restlessdevelopment.org/", "emails": ["infotanzania@restlessdevelopment.org"]},
    {"slug": "restova", "name": "Restova", "url": "https://restova.co.tz/", "emails": []},
    {"slug": "reveurse", "name": "Reveurse", "url": "https://reveurse.co.tz/", "emails": ["info@reveurse.co.tz", "reveurse@reveurse.co.tz"]},
    {"slug": "revivetherapy", "name": "Revive Physiotherapy", "url": "https://www.revivetherapy.co.tz/", "emails": ["info@revivetherapy.co.tz", "revivephysiotherapy24@gmail.com"]},
    {"slug": "rexattorneys", "name": "Rex Attorneys", "url": "https://rexattorneys.co.tz/", "emails": ["info@rexattorneys.co.tz"]},
    {"slug": "reynatours", "name": "Reyna Tour", "url": "https://www.reynatours.co.tz/", "emails": ["info@reynatours.co.tz", "info@kwetuadventures.co.tz"]},
]

# REPOA tenders (from scrape)
REPOA_TENDERS = [
    {"id": "REPOA-2026-001", "title": "Invitation for Pre-qualification at REPOA – Supply of Goods and Provision of Non-Consultancy Services for FY 2025-2027",
     "url": "https://repoa.or.tz/by-repoa/invitation-for-pre-qualification-at-repoa-the-supply-of-goods-and-provision-of-non-consultancy-services-for-fy-2025-2027/",
     "doc_url": "https://www.repoa.or.tz/wp-content/uploads/2025/07/Advert-Invitation-for-Pre-qualification-at-REPOA-FY-2025-2027.pdf"},
    {"id": "REPOA-2026-002", "title": "Expression of Interest (EoI) for Property Development at REPOA",
     "url": "https://repoa.or.tz/by-repoa/expression-of-interest-eoi-for-property-development-at-repoa/",
     "doc_url": "https://www.repoa.or.tz/wp-content/uploads/2025/02/Expression-of-Interest-EoI-for-Property-Development.pdf"},
    {"id": "REPOA-2026-003", "title": "Terms of Reference for Mid Term Review of REPOA's Strategic Plan 2020-2024",
     "url": "https://repoa.or.tz/by-repoa/terms-of-reference-for-mid-term-review-of-repoas-strategic-plan-2020-2024/",
     "doc_url": "https://www.repoa.or.tz/wp-content/uploads/2023/04/ToRs-for-REPOA-mid-term-review-of-the-SP-2020-2024_April-2023.pdf"},
    {"id": "REPOA-2026-004", "title": "Call For Proposals: A Value Chain Analysis of Competitiveness and Trade Diversification in the Rice Sub Sector in Tanzania",
     "url": "https://repoa.or.tz/tenders/call-for-proposals-a-value-chain-analysis-of-competitiveness-and-trade-diversification-in-the-rice-sub-sector-in-tanzania/",
     "doc_url": "http://www.repoa.or.tz/wp-content/uploads/2021/05/Rice-Value-Chain-Study-Terms-of-Reference-for-the-Key-Expert-2.pdf"},
]


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TENDERS-Scraper/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.read())
            return True
    except Exception as e:
        print(f"  Download failed {url}: {e}")
        return False


def extract_text_pdf(pdf_path: Path) -> Path:
    txt_path = pdf_path.parent.parent / "extracted" / (pdf_path.stem + ".txt")
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            ["python3", "-m", "tools", "pdf", "read", str(pdf_path)],
            cwd=PROJECT, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout:
            txt_path.write_text(result.stdout, encoding="utf-8")
    except Exception:
        pass
    return txt_path


def process_repoa_tenders():
    inst_dir = PROJECT / "institutions" / "repoa"
    ensure_dirs(inst_dir)
    doc_count = 0
    for t in REPOA_TENDERS:
        tender_json = {
            "tender_id": t["id"],
            "title": t["title"],
            "description": "",
            "published_date": None,
            "closing_date": None,
            "category": "procurement",
            "document_links": [t["doc_url"]],
            "contact_info": {"email": "repoa@repoa.or.tz", "phone": "+255 (22) 270 0083"},
            "source_url": t["url"],
        }
        (inst_dir / "tenders" / "active" / f"{t['id']}.json").write_text(
            json.dumps(tender_json, indent=2), encoding="utf-8"
        )
        if t.get("doc_url"):
            dest = inst_dir / "downloads" / t["id"] / "original" / Path(t["doc_url"]).name
            if download_file(t["doc_url"], dest):
                doc_count += 1
                extract_text_pdf(dest)
    return len(REPOA_TENDERS), doc_count


def create_lead(inst: dict) -> dict:
    emails = [e for e in inst.get("emails", []) if "@" in e and "." in e.split("@")[-1]]
    return {
        "institution_slug": inst["slug"],
        "institution_name": inst["name"],
        "website_url": inst["url"],
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
        "draft_email_body": f"""Dear {inst['name']} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {inst['name']}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
""",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }


def append_leads(new_leads: list):
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        leads = json.loads(leads_path.read_text(encoding="utf-8"))
    leads.extend(new_leads)
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")


def update_scrape_state(inst_dir: Path, slug: str, status: str, tender_count: int, doc_count: int, error: str = None):
    now = datetime.now(timezone.utc).isoformat()
    last = {
        "run_id": RUN_ID,
        "timestamp": now,
        "status": status,
        "tender_count": tender_count,
        "doc_count": doc_count,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
    log_path = inst_dir / "scrape_log.json"
    log_entries = []
    if log_path.exists():
        log_entries = json.loads(log_path.read_text(encoding="utf-8"))
    log_entries.append({"run_id": RUN_ID, "timestamp": now, "status": status, "tender_count": tender_count, "doc_count": doc_count})
    log_path.write_text(json.dumps(log_entries[-100:], indent=2), encoding="utf-8")


def main():
    results = []
    leads_to_add = []

    for inst in INSTITUTIONS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        ensure_dirs(inst_dir)

        if inst.get("has_tenders") and slug == "repoa":
            tender_count, doc_count = process_repoa_tenders()
            update_scrape_state(inst_dir, slug, "success", tender_count, doc_count)
            results.append(f"RESULT|{slug}|success|{tender_count}|{doc_count}")
            print(results[-1])
            continue

        # No tenders - create lead
        lead = create_lead(inst)
        leads_to_add.append(lead)
        update_scrape_state(inst_dir, slug, "no_tenders", 0, 0)
        results.append(f"RESULT|{slug}|no_tenders|0|0")
        print(results[-1])

    if leads_to_add:
        # Dedupe: only append leads not already in leads.json
        leads_path = PROJECT / "opportunities" / "leads.json"
        existing_slugs = set()
        if leads_path.exists():
            existing = json.loads(leads_path.read_text(encoding="utf-8"))
            existing_slugs = {l.get("institution_slug") for l in existing if l.get("institution_slug")}
        new_leads = [l for l in leads_to_add if l.get("institution_slug") not in existing_slugs]
        if new_leads:
            append_leads(new_leads)
            subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=PROJECT, check=True)

    print("\n--- BATCH 96 COMPLETE ---")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
