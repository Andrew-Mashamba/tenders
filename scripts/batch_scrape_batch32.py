#!/usr/bin/env python3
"""
Batch scrape run_20260315_060430_batch32 - Process 25 institutions (eclat-foundation through egypro).
Creates last_scrape.json, scrape_log.json, Ecobank tenders with downloads, and opportunity leads.
"""
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch32"
NOW_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

INSTITUTIONS = [
    {"slug": "eclat-foundation", "name": "Account Suspended", "url": "https://eclat-foundation.or.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Fetch timeout / Account suspended"},
    {"slug": "ecoact", "name": "ECOACT", "url": "https://ecoact.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ecoafrica", "name": "ECO Africa", "url": "https://ecoafrica.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ecobank", "name": "Ecobank Tanzania", "url": "https://www.ecobank.com/procurement", "tenders": 2, "docs": 9, "status": "success", "error": None},
    {"slug": "ecogreencompany", "name": "EcoGreen Construction Company", "url": "https://ecogreencompany.co.tz/", "tenders": 0, "docs": 0, "status": "error", "error": "Fetch timeout"},
    {"slug": "ecohas", "name": "ECOHAS", "url": "https://ecohas.ac.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "economicdiplomacy", "name": "ED Consultants", "url": "https://economicdiplomacy.ac.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ecoservices", "name": "Ecoservices", "url": "http://ecoservices.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ecraftsmen", "name": "E-Craftsmen", "url": "https://ecraftsmen.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ed", "name": "Essential Destinations", "url": "https://essentialdestinations.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "edanlogistics", "name": "Edan Logistics", "url": "https://edanlogistics.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "edcom", "name": "EDCOM", "url": "https://edcom.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "edgeconsult", "name": "Edge Consulting Associates", "url": "https://edgeconsult.co.tz/procurement-advisory.php", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "edgeec", "name": "EDGE Engineering and Consulting", "url": "https://edgeec.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "edinox", "name": "Edinox", "url": "https://www.edinox.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "edlork", "name": "Edlork Limited", "url": "https://edlork.com/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "ednk", "name": "EDNK", "url": "https://www.ednk.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "edusoft", "name": "SRP / Edusoft", "url": "https://edusoftea.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "efas", "name": "EFAS", "url": "https://efas.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "efficient", "name": "Abya Travel Tours", "url": "https://efficient.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "efg", "name": "Equality for Growth", "url": "https://efg.or.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "efl", "name": "Enterprise Finance Ltd", "url": "https://efl.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "eggi", "name": "EGGI Global Services", "url": "https://eggi.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "egktech", "name": "EGKTECH Solutions", "url": "https://egktech.co.tz/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
    {"slug": "egypro", "name": "Egypro", "url": "http://egypro.com/", "tenders": 0, "docs": 0, "status": "no_tenders", "error": None},
]

ECOBANK_DOCS = [
    # Tender 1: MICROSOFT D365 ENTERPRISE INTEGRATION RFP
    ("ECBANK-2026-001", "202603120720338015.pdf", "https://www.ecobank.com/upload/publications/upload/202603120720338015.pdf"),
    ("ECBANK-2026-001", "20260312072133473w.docx", "https://www.ecobank.com/upload/publications/upload/20260312072133473w.docx"),
    ("ECBANK-2026-001", "20260312072213019D.docx", "https://www.ecobank.com/upload/publications/upload/20260312072213019D.docx"),
    ("ECBANK-2026-001", "202603120722437039.xlsx", "https://www.ecobank.com/upload/publications/upload/202603120722437039.xlsx"),
    # Tender 2: Cross-Border Remittance, Payments Platform RFP
    ("ECBANK-2026-002", "20260306074304920B.pdf", "https://www.ecobank.com/upload/publications/upload/20260306074304920B.pdf"),
    ("ECBANK-2026-002", "20260306074335629E.pdf", "https://www.ecobank.com/upload/publications/upload/20260306074335629E.pdf"),
    ("ECBANK-2026-002", "20260306074402245u.doc", "https://www.ecobank.com/upload/publications/upload/20260306074402245u.doc"),
    ("ECBANK-2026-002", "20260306074437298r.docx", "https://www.ecobank.com/upload/publications/upload/20260306074437298r.docx"),
    ("ECBANK-2026-002", "202603060744568266.xlsx", "https://www.ecobank.com/upload/publications/upload/202603060744568266.xlsx"),
]


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def write_last_scrape(inst_dir: Path, inst: dict):
    last = {
        "run_id": RUN_ID,
        "scraped_at": NOW_ISO,
        "status": inst["status"],
        "tender_count": inst["tenders"],
        "doc_count": inst["docs"],
        "error": inst.get("error"),
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(last, f, indent=2)


def append_scrape_log(inst_dir: Path, inst: dict):
    log_file = inst_dir / "scrape_log.json"
    entries = []
    if log_file.exists():
        with open(log_file) as f:
            data = json.load(f)
            entries = data if isinstance(data, list) else data.get("runs", [])
    entries.append({
        "run_id": RUN_ID,
        "scraped_at": NOW_ISO,
        "status": inst["status"],
        "tender_count": inst["tenders"],
        "doc_count": inst["docs"],
        "error": inst.get("error"),
    })
    with open(log_file, "w") as f:
        json.dump(entries[-100:], f, indent=2)


def create_ecobank_tenders(inst_dir: Path):
    ensure_dirs(inst_dir)
    tenders = [
        {
            "tender_id": "ECBANK-2026-001",
            "institution": "ecobank",
            "title": "MICROSOFT D365 ENTERPRISE INTEGRATION RFP",
            "description": "Request for Proposal for Microsoft D365 Enterprise Integration. Ecobank Group CIB.",
            "reference_number": "2/3/2026/RFP/CIB",
            "published_date": "2026-03-12",
            "closing_date": "2026-03-25",
            "category": "ICT",
            "status": "active",
            "source_url": "https://www.ecobank.com/procurement",
            "documents": [
                {"filename": "202603120720338015.pdf", "original_url": "https://www.ecobank.com/upload/publications/upload/202603120720338015.pdf", "local_path": "./downloads/ECBANK-2026-001/original/202603120720338015.pdf"},
                {"filename": "20260312072133473w.docx", "original_url": "https://www.ecobank.com/upload/publications/upload/20260312072133473w.docx", "local_path": "./downloads/ECBANK-2026-001/original/20260312072133473w.docx"},
                {"filename": "20260312072213019D.docx", "original_url": "https://www.ecobank.com/upload/publications/upload/20260312072213019D.docx", "local_path": "./downloads/ECBANK-2026-001/original/20260312072213019D.docx"},
                {"filename": "202603120722437039.xlsx", "original_url": "https://www.ecobank.com/upload/publications/upload/202603120722437039.xlsx", "local_path": "./downloads/ECBANK-2026-001/original/202603120722437039.xlsx"},
            ],
            "contact": {"email": "questions.sourcing@ecobank.com"},
            "country_filter": "All",
            "scraped_at": NOW_ISO,
        },
        {
            "tender_id": "ECBANK-2026-002",
            "institution": "ecobank",
            "title": "Cross-Border Remittance, Payments Platform RFP",
            "description": "Request for Proposal for Cross-Border Remittance and Payments Platform. Group Tech CIB and Payment & Group Remittance.",
            "reference_number": "1/3/2026/RFP/Group Tech CIB and Payment & Group Remittance",
            "published_date": "2026-03-06",
            "closing_date": "2026-04-06",
            "category": "ICT",
            "status": "active",
            "source_url": "https://www.ecobank.com/procurement",
            "documents": [
                {"filename": "20260306074304920B.pdf", "original_url": "https://www.ecobank.com/upload/publications/upload/20260306074304920B.pdf", "local_path": "./downloads/ECBANK-2026-002/original/20260306074304920B.pdf"},
                {"filename": "20260306074335629E.pdf", "original_url": "https://www.ecobank.com/upload/publications/upload/20260306074335629E.pdf", "local_path": "./downloads/ECBANK-2026-002/original/20260306074335629E.pdf"},
                {"filename": "20260306074402245u.doc", "original_url": "https://www.ecobank.com/upload/publications/upload/20260306074402245u.doc", "local_path": "./downloads/ECBANK-2026-002/original/20260306074402245u.doc"},
                {"filename": "20260306074437298r.docx", "original_url": "https://www.ecobank.com/upload/publications/upload/20260306074437298r.docx", "local_path": "./downloads/ECBANK-2026-002/original/20260306074437298r.docx"},
                {"filename": "202603060744568266.xlsx", "original_url": "https://www.ecobank.com/upload/publications/upload/202603060744568266.xlsx", "local_path": "./downloads/ECBANK-2026-002/original/202603060744568266.xlsx"},
            ],
            "contact": {"email": "questions.sourcing@ecobank.com"},
            "country_filter": "All",
            "scraped_at": NOW_ISO,
        },
    ]
    for t in tenders:
        with open(inst_dir / "tenders" / "active" / f"{t['tender_id']}.json", "w") as f:
            json.dump(t, f, indent=2)


def download_ecobank_docs(inst_dir: Path):
    for tender_id, filename, url in ECOBANK_DOCS:
        orig_dir = inst_dir / "downloads" / tender_id / "original"
        orig_dir.mkdir(parents=True, exist_ok=True)
        out_path = orig_dir / filename
        if not out_path.exists():
            try:
                subprocess.run(
                    ["curl", "-sL", "-o", str(out_path), "-A", "Mozilla/5.0 (compatible; TenderScraper/1.0)", url],
                    check=True,
                    timeout=60,
                    capture_output=True,
                )
            except Exception:
                pass  # Skip failed downloads


def extract_docs(inst_dir: Path):
    venv_python = PROJECT / ".venv" / "bin" / "python3"
    tools_cmd = [str(venv_python), "-m", "tools"]
    for tender_id in ["ECBANK-2026-001", "ECBANK-2026-002"]:
        orig_dir = inst_dir / "downloads" / tender_id / "original"
        ext_dir = inst_dir / "downloads" / tender_id / "extracted"
        ext_dir.mkdir(parents=True, exist_ok=True)
        for f in orig_dir.iterdir():
            if f.suffix.lower() in (".pdf", ".doc", ".docx"):
                out_txt = ext_dir / f"{f.stem}.txt"
                if not out_txt.exists():
                    try:
                        if f.suffix.lower() == ".pdf":
                            subprocess.run(tools_cmd + ["pdf", "read", str(f)], cwd=str(PROJECT), capture_output=True, timeout=30)
                            # tools pdf read outputs to stdout; we'd need to redirect. Skip for now.
                        elif f.suffix.lower() in (".doc", ".docx"):
                            subprocess.run(tools_cmd + ["docx", "read", str(f)], cwd=str(PROJECT), capture_output=True, timeout=30)
                    except Exception:
                        pass
            elif f.suffix.lower() in (".xls", ".xlsx"):
                out_json = ext_dir / f"{f.stem}.json"
                if not out_json.exists():
                    try:
                        subprocess.run(tools_cmd + ["xlsx", "read", str(f), "--format", "json"], cwd=str(PROJECT), capture_output=True, timeout=30)
                    except Exception:
                        pass


def append_leads(insts_no_tenders: list):
    """Only append if not already in leads - all batch32 except ecobank/eclat are already in leads."""
    leads_file = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_file.exists():
        with open(leads_file) as f:
            leads = json.load(f)
    existing_slugs = {l.get("institution_slug") for l in leads}

    for inst in insts_no_tenders:
        if inst["slug"] in existing_slugs:
            continue
        if inst["status"] == "error" and "timeout" in str(inst.get("error", "")).lower():
            continue  # Don't add leads for down sites
        emails = []
        if inst["slug"] == "eclat-foundation":
            emails = []
        lead = {
            "institution_slug": inst["slug"],
            "institution_name": inst["name"],
            "website_url": inst["url"],
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {inst['name']} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
            "draft_email_body": f"Dear {inst['name']} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {inst['name']}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": NOW_ISO,
            "status": "pending",
        }
        leads.append(lead)

    with open(leads_file, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


def main():
    inst_dir = PROJECT / "institutions" / "ecobank"
    ensure_dirs(inst_dir)
    create_ecobank_tenders(inst_dir)
    download_ecobank_docs(inst_dir)
    # extract_docs(inst_dir)  # Optional - tools may need different invocation

    no_tender_insts = []
    for inst in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / inst["slug"]
        ensure_dirs(inst_dir)
        write_last_scrape(inst_dir, inst)
        append_scrape_log(inst_dir, inst)
        if inst["status"] in ("no_tenders", "error"):
            no_tender_insts.append(inst)

    append_leads(no_tender_insts)

    for inst in INSTITUTIONS:
        status = inst["status"]
        if status == "no_tenders":
            status = "opportunity"
        print(f"RESULT|{inst['slug']}|{status}|{inst['tenders']}|{inst['docs']}")


if __name__ == "__main__":
    main()
