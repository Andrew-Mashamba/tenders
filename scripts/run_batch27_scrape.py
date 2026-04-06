#!/usr/bin/env python3
"""Process batch27 scrape: DCC tenders + opportunities for 24 no-tender institutions."""
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch27"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# DCC tenders parsed from HTML
DCC_TENDERS = [
    {"title": "Collection of Waste from Peripheral Wards to Pugu Kinyamwezi Dumpsite", "published": "2025-09-28", "closing": "2025-10-02", "pdf": "/storage/app/uploads/public/68d/999/64d/68d99964d62ee506429960.pdf"},
    {"title": "PROPOSED WORKS FOR IMPROVEMENT OF GENERAL ENVIRONMENTAL CONDITIONS OF BOTANICAL GARDEN AT DAR ES SALAAM CITY COUNCIL", "published": "2025-09-22", "closing": "2025-09-26", "pdf": "/storage/app/uploads/public/68d/0e0/1f5/68d0e01f5afe6903308379.pdf"},
    {"title": "Procurement of Hydrauric Excavator Machine 35 Tons for Damp site Operations at Dar es Salaam City Council", "published": "2025-03-12", "closing": "2025-03-19", "pdf": "/storage/app/uploads/public/67d/1eb/f2a/67d1ebf2a584f960168386.pdf"},
    {"title": "PROCURING OF LABORATORY SUPPLIES AND REAGENT AT CHANIKA HC", "published": "2025-01-18", "closing": "2025-01-21", "pdf": "/storage/app/uploads/public/678/bd5/8b3/678bd58b30480888155567.pdf"},
    {"title": "Supply of Building Material for the Construction of 2 Stairway of Mzinga Health Centre", "published": "2024-12-16", "closing": "2024-12-23", "pdf": "/storage/app/uploads/public/676/03f/8f7/67603f8f78843823667057.pdf"},
    {"title": "Installation of CCTV Cameras phase one at Kariakoo Area", "published": "2024-12-06", "closing": "2024-12-10", "pdf": "/storage/app/uploads/public/675/31d/319/67531d3193543714977232.pdf"},
    {"title": "Solar Street Lights Installation for Pemba Street, Mafia Street, Pugu Mnadani, Baraka Obama, Magogoni, Kichanga Chui, Lumumba, Pangani- Kasulu, Stesheni bus Stand, Kivule Hospital and Tandamti Street", "published": "2024-10-24", "closing": "2024-10-28", "pdf": "/storage/app/uploads/public/671/a82/b09/671a82b090442843005648.pdf"},
    {"title": "CONSTRUCTION OF FENCE AT KIVULE DISTRICT HOSPITAL BY JUNE 2025", "published": "2024-10-16", "closing": "2024-10-16", "pdf": "/storage/app/uploads/public/670/fcf/b13/670fcfb130a41281993236.pdf"},
]

# Institutions with no tenders - add to leads
NO_TENDER_INSTITUTIONS = [
    {"slug": "dcl", "name": "Diligent Consulting Ltd", "url": "https://dcl.co.tz/", "emails": ["info@dcl.co.tz"]},
    {"slug": "dctmvumi", "name": "DCT Mvumi Secondary School", "url": "https://dctmvumi.sc.tz/", "emails": ["headmaster@dctmvumi.sc.tz"]},
    {"slug": "dea", "name": "DARWIN EDUCATION AGENCY (DEA)", "url": "https://dea.co.tz/", "emails": ["info@dea.co.tz"]},
    {"slug": "decomputersolutions", "name": "De Computer Solutions & Supply", "url": "https://decomputersolutions.co.tz/", "emails": ["info@decomputersolutions.co.tz"]},
    {"slug": "decostone", "name": "Decostone", "url": "https://decostone.co.tz/", "emails": ["webmaster@decostone.co.tz"]},
    {"slug": "deepmedia", "name": "Deep Media Digital Agency", "url": "https://www.deepmedia.co.tz/", "emails": ["info@deepmedia.co.tz"]},
    {"slug": "dees", "name": "Crafty Dees", "url": "https://www.dees.co.tz/", "emails": []},
    {"slug": "dekamologistics", "name": "Dekamo Logistics co.ltd", "url": "https://dekamologistics.co.tz/", "emails": ["dekamologistics@gmail.com"]},
    {"slug": "delcatechnologies", "name": "Delca Technologies", "url": "https://delcatechnologies.co.tz/", "emails": ["delcatechnologies@gmail.com"]},
    {"slug": "delightgroup", "name": "Delight Group", "url": "https://delightgroup.co.tz/", "emails": ["info@delightgroup.co.tz", "delightgrouptz@gmail.com"]},
    {"slug": "delinagroup", "name": "Delina Group", "url": "https://delinagroup.co.tz/", "emails": ["info@delinagroup.co.tz"]},
    {"slug": "deltanet", "name": "DeltaNet Tanzania", "url": "https://deltanet.co.tz/", "emails": ["info@deltanet.co.tz"]},
    {"slug": "deltavets", "name": "Delta Veterinary Services", "url": "https://deltavets.co.tz/", "emails": ["info@deltavets.co.tz"]},
    {"slug": "demusassociates", "name": "Demus Associates", "url": "https://demusassociates.co.tz/", "emails": ["contact@demusassociates.co.tz"]},
    {"slug": "denels", "name": "Denels", "url": "https://denels.co.tz/", "emails": ["info@denels.co.tz"]},
    {"slug": "denikoconstruction", "name": "DENIKO Construction Ltd", "url": "https://denikoconstruction.co.tz/", "emails": ["info@denikocontruction.co.tz"]},
    {"slug": "dentist", "name": "Dental Studio", "url": "https://dentist.co.tz/", "emails": ["info@dentist.co.tz"]},
    {"slug": "dentistindar", "name": "SD Dental Tanzania", "url": "https://dentistindar.co.tz/", "emails": ["sddental_clinic@hotmail.com", "drshabbir786@yahoo.com"]},
    {"slug": "deoadventure", "name": "Deoadventure", "url": "https://www.deoadventure.co.tz/", "emails": ["adventure@deoadventure.co.tz"]},
    {"slug": "desire", "name": "Desire Park", "url": "https://desire.co.tz/", "emails": []},
    {"slug": "detaramo", "name": "Detaramo Company Limited", "url": "https://detaramo.co.tz/", "emails": ["info@detaramo.co.tz"]},
    {"slug": "dewdreamy", "name": "dewdreamy", "url": "https://www.dewdreamy.co.tz/", "emails": ["info@dewdreamy.co.tz"]},
]

# Error institutions (site down/timeout)
ERROR_INSTITUTIONS = [
    {"slug": "dda", "error": "Fetch timeout"},
    {"slug": "ddca", "error": "SSL/fetch error"},
]

DRAFT_EMAIL_BODY = """Dear {name} Team,

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


def download_file(url: str, dest: Path) -> bool:
    """Download file via curl (handles SSL with -k for .go.tz)."""
    try:
        subprocess.run(
            ["curl", "-skL", "-m", "60", "-o", str(dest), "-A", "Mozilla/5.0", url],
            check=True,
            capture_output=True,
        )
        return dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def extract_text_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using tools."""
    try:
        result = subprocess.run(
            ["python3", "-m", "tools", "pdf", "read", str(pdf_path)],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout or "" if result.returncode == 0 else ""
    except Exception:
        return ""


def process_dcc():
    """Process DCC tenders: download PDFs, save JSON, extract text."""
    inst_dir = PROJECT / "institutions" / "dcc"
    tenders_dir = inst_dir / "tenders"
    active_dir = tenders_dir / "active"
    closed_dir = tenders_dir / "closed"
    active_dir.mkdir(parents=True, exist_ok=True)
    closed_dir.mkdir(parents=True, exist_ok=True)

    doc_count = 0
    active_count = 0
    base_url = "https://dcc.go.tz"

    for i, t in enumerate(DCC_TENDERS, 1):
        tender_id = f"DCC-2026-{i:03d}"
        closing = t["closing"]
        is_active = closing >= "2026-03-13"  # today
        out_dir = active_dir if is_active else closed_dir

        pdf_url = urljoin(base_url, t["pdf"])
        filename = pdf_url.split("/")[-1]
        download_dir = inst_dir / "downloads" / tender_id / "original"
        extracted_dir = inst_dir / "downloads" / tender_id / "extracted"
        download_dir.mkdir(parents=True, exist_ok=True)
        extracted_dir.mkdir(parents=True, exist_ok=True)

        dest = download_dir / filename
        if download_file(pdf_url, dest):
            doc_count += 1
            txt_path = extracted_dir / (Path(filename).stem + ".txt")
            text = extract_text_pdf(dest)
            if text:
                txt_path.write_text(text, encoding="utf-8")
        else:
            dest = None

        doc_entry = None
        if dest and dest.exists():
            doc_entry = {
                "filename": filename,
                "original_url": pdf_url,
                "local_path": f"./downloads/{tender_id}/original/{filename}",
                "downloaded_at": NOW,
            }

        tender_json = {
            "tender_id": tender_id,
            "institution": "dcc",
            "title": t["title"],
            "description": "",
            "published_date": t["published"],
            "closing_date": closing,
            "category": "General",
            "status": "active" if is_active else "closed",
            "source_url": "https://dcc.go.tz/tenders",
            "documents": [doc_entry] if doc_entry else [],
            "contact": {"email": "info@dcc.go.tz", "phone": "0738 378 386"},
            "scraped_at": NOW,
            "last_checked": NOW,
        }

        (out_dir / f"{tender_id}.json").write_text(json.dumps(tender_json, indent=2), encoding="utf-8")
        if is_active:
            active_count += 1

    return len(DCC_TENDERS), doc_count, active_count


def update_dcc_logs(tender_count: int, doc_count: int, active_count: int):
    """Update last_scrape.json and scrape_log.json for DCC."""
    inst_dir = PROJECT / "institutions" / "dcc"
    last = {
        "institution": "dcc",
        "last_scrape": NOW,
        "next_scrape": "2026-03-14T06:00:00Z",
        "active_tenders_count": active_count,
        "status": "success",
        "error": None,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

    log_path = inst_dir / "scrape_log.json"
    log = {"runs": []}
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
    log["runs"].append({
        "run_id": RUN_ID,
        "timestamp": NOW,
        "status": "success",
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [],
    })
    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")


def append_leads():
    """Append no-tender institutions to leads.json."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        leads = json.loads(leads_path.read_text(encoding="utf-8"))
    if not isinstance(leads, list):
        leads = leads.get("leads", []) or []

    existing_slugs = {l.get("institution_slug") for l in leads}
    added = 0
    for inst in NO_TENDER_INSTITUTIONS:
        if inst["slug"] in existing_slugs:
            continue
        lead = {
            "institution_slug": inst["slug"],
            "institution_name": inst["name"],
            "website_url": inst["url"],
            "emails": inst["emails"],
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
            "draft_email_body": DRAFT_EMAIL_BODY.format(name=inst["name"]),
            "created_at": NOW,
            "status": "pending",
        }
        leads.append(lead)
        existing_slugs.add(inst["slug"])
        added += 1
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
    return added


def update_institution_log(slug: str, status: str, tender_count: int, doc_count: int, error: str = None):
    """Update last_scrape.json and scrape_log.json for an institution."""
    inst_dir = PROJECT / "institutions" / slug
    inst_dir.mkdir(parents=True, exist_ok=True)
    last = {
        "institution": slug,
        "last_scrape": NOW,
        "status": status,
        "active_tenders_count": tender_count,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
    log_path = inst_dir / "scrape_log.json"
    log = {"runs": []}
    if log_path.exists():
        try:
            log = json.loads(log_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    log["runs"].append({
        "run_id": RUN_ID,
        "timestamp": NOW,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    })
    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")


def main():
    results = []
    # DCC - has tenders
    t_count, d_count, a_count = process_dcc()
    update_dcc_logs(t_count, d_count, a_count)
    results.append(f"RESULT|dcc|success|{t_count}|{d_count}")

    # No-tender institutions
    for inst in NO_TENDER_INSTITUTIONS:
        update_institution_log(inst["slug"], "no_tenders", 0, 0)
        results.append(f"RESULT|{inst['slug']}|no_tenders|0|0")

    # Error institutions
    for inst in ERROR_INSTITUTIONS:
        update_institution_log(inst["slug"], "error", 0, 0, inst["error"])
        results.append(f"RESULT|{inst['slug']}|error|0|0")

    # Append leads
    added = append_leads()
    if added > 0:
        subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=PROJECT, check=True)

    for r in results:
        print(r)
    print(f"\nLeads appended: {added}")


if __name__ == "__main__":
    main()
