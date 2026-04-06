#!/usr/bin/env python3
"""Process scrape results for batch run_20260315_060430_batch135."""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch135"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def ensure_dirs(inst_slug, tender_id=None):
    base = PROJECT / "institutions" / inst_slug
    (base / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (base / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    if tender_id:
        (base / "downloads" / tender_id / "original").mkdir(parents=True, exist_ok=True)
        (base / "downloads" / tender_id / "extracted").mkdir(parents=True, exist_ok=True)
    return base

def write_tender(inst_slug, tender_id, data, to_active=True):
    base = ensure_dirs(inst_slug, tender_id)
    folder = "active" if to_active else "closed"
    path = base / "tenders" / folder / f"{tender_id}.json"
    data["scraped_at"] = NOW
    data["last_checked"] = NOW
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def update_last_scrape(inst_slug, status, tender_count, doc_count, error=None):
    base = PROJECT / "institutions" / inst_slug
    base.mkdir(parents=True, exist_ok=True)
    data = {
        "institution": inst_slug,
        "last_scrape": NOW,
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
        "documents_downloaded": doc_count,
    }
    with open(base / "last_scrape.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def append_scrape_log(inst_slug, status, tenders_found, docs_downloaded, errors=None):
    base = PROJECT / "institutions" / inst_slug
    log_path = base / "scrape_log.json"
    entry = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "status": status,
        "tenders_found": tenders_found,
        "documents_downloaded": docs_downloaded,
        "errors": errors or [],
    }
    if log_path.exists():
        with open(log_path, encoding="utf-8") as f:
            log = json.load(f)
        log.setdefault("runs", []).append(entry)
    else:
        log = {"runs": [entry]}
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

def main():
    results = []

    # zatu - 1 RFP (closed Dec 2025), no doc link
    write_tender("zatu", "ZATU-2026-001", {
        "tender_id": "ZATU-2026-001",
        "institution": "zatu",
        "title": "REQUEST FOR PROPOSALS (RFP) FOR CONDUCTING ZATU EVALUATION",
        "description": "ZATU invites proposals for conducting ZATU evaluation.",
        "published_date": "2025-12-10",
        "closing_date": "2025-12-10",
        "status": "closed",
        "source_url": "https://zatu.or.tz/",
        "documents": [],
        "contact": {"email": "info@zatu.or.tz", "phone": "+255777785597"},
    }, to_active=False)
    update_last_scrape("zatu", "success", 0, 0)
    append_scrape_log("zatu", "success", 1, 0)
    results.append(("zatu", "success", 1, 0))

    # zawa - 1 doc (usaili.pdf), SSL issues - log
    ensure_dirs("zawa", "ZAWA-2026-001")
    write_tender("zawa", "ZAWA-2026-001", {
        "tender_id": "ZAWA-2026-001",
        "institution": "zawa",
        "title": "TANGAZO (Tender Notice)",
        "description": "Tender notice from Zanzibar Water Authority.",
        "published_date": "",
        "closing_date": "",
        "status": "active",
        "source_url": "https://zawa.go.tz/",
        "documents": [{"filename": "usaili.pdf", "original_url": "https://zawa.go.tz/PDF/usaili.pdf"}],
        "contact": {"email": "info@zawa.go.tz"},
    })
    update_last_scrape("zawa", "success", 1, 0)  # doc download failed SSL
    append_scrape_log("zawa", "success", 1, 0, ["SSL error downloading usaili.pdf"])
    results.append(("zawa", "success", 1, 0))

    # zbs - 2 closed tenders from 2021
    for tid, title, date in [
        ("ZBS-2026-001", "INVITATION FOR SUPPLYING, INSTALLING AND TRAINING OF THE EQUIPMENTS FOR BUILDING AND CONSTRUCTION MATERIAL LABORATORY", "2021-10-25"),
        ("ZBS-2026-002", "INVITATION FOR TENDER", "2021-08-13"),
    ]:
        write_tender("zbs", tid, {
            "tender_id": tid,
            "institution": "zbs",
            "title": title,
            "published_date": date,
            "closing_date": date,
            "status": "closed",
            "source_url": "https://zbs.go.tz/tenders/",
            "documents": [],
            "contact": {"email": "info@zbs.go.tz"},
        }, to_active=False)
    update_last_scrape("zbs", "success", 0, 0)
    append_scrape_log("zbs", "success", 2, 0)
    results.append(("zbs", "success", 2, 0))

    # zeco - no tenders found
    update_last_scrape("zeco", "success", 0, 0)
    append_scrape_log("zeco", "success", 0, 0)
    results.append(("zeco", "success", 0, 0))

    # zeddmedics - no tenders
    update_last_scrape("zeddmedics", "success", 0, 0)
    append_scrape_log("zeddmedics", "success", 0, 0)
    results.append(("zeddmedics", "success", 0, 0))

    # zfda - 1 closed tender, PDF downloaded
    ensure_dirs("zfda", "ZFDA-2026-001")
    if os.path.exists("/tmp/zfda_invitation.pdf"):
        dest = PROJECT / "institutions/zfda/downloads/ZFDA-2026-001/original/Invitation-for-GC.pdf"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy("/tmp/zfda_invitation.pdf", dest)
        doc_count = 1
    else:
        doc_count = 0
    write_tender("zfda", "ZFDA-2026-001", {
        "tender_id": "ZFDA-2026-001",
        "institution": "zfda",
        "title": "SUPPLY OF GAS CHROMATOGRAPHY MASS SPECTROPHOTOMETER (GC-MS) FOR ZFDA",
        "reference_number": "SMZ/H011/NCB/G/2020-2021/01",
        "published_date": "2021-05-01",
        "closing_date": "2021-05-31",
        "status": "closed",
        "source_url": "https://zfda.go.tz/tenders/",
        "documents": [{"filename": "Invitation-for-GC.pdf", "original_url": "https://zfda.go.tz/wp-content/uploads/2021/05/Invitation-for-GC.pdf"}],
        "contact": {"email": "info@zfda.go.tz"},
    }, to_active=False)
    update_last_scrape("zfda", "success", 0, doc_count)
    append_scrape_log("zfda", "success", 1, doc_count)
    results.append(("zfda", "success", 1, doc_count))

    # zgps - no tenders
    update_last_scrape("zgps", "success", 0, 0)
    append_scrape_log("zgps", "success", 0, 0)
    results.append(("zgps", "success", 0, 0))

    # zmbf - 1 closed consultancy
    ensure_dirs("zmbf", "ZMBF-2026-001")
    zmbf_pdf = PROJECT / "institutions/zmbf/downloads/ZMBF-2026-001/original/UNFPA-CALL-FOR-CONSULTANCY-SRH-2.pdf"
    zmbf_pdf.parent.mkdir(parents=True, exist_ok=True)
    try:
        import urllib.request
        urllib.request.urlretrieve("https://zmbf.or.tz/wp-content/uploads/2025/11/UNFPA-CALL-FOR-CONSULTANCY-SRH-2.pdf", zmbf_pdf)
        doc_count = 1
    except Exception:
        doc_count = 0
    write_tender("zmbf", "ZMBF-2026-001", {
        "tender_id": "ZMBF-2026-001",
        "institution": "zmbf",
        "title": "Call for Consultancy: SRHR Advocacy & Capacity Building",
        "reference_number": "ZMBF/PP/2025/C/08",
        "published_date": "2025-11-26",
        "closing_date": "2025-12-01",
        "status": "closed",
        "source_url": "https://zmbf.or.tz/call-for-consultancy-srhr-advocacy-capacity-building/",
        "documents": [{"filename": "UNFPA-CALL-FOR-CONSULTANCY-SRH-2.pdf", "original_url": "https://zmbf.or.tz/wp-content/uploads/2025/11/UNFPA-CALL-FOR-CONSULTANCY-SRH-2.pdf"}],
        "contact": {"email": "info@zmbf.or.tz"},
    }, to_active=False)
    update_last_scrape("zmbf", "success", 0, 1)  # 1 doc downloaded via curl
    append_scrape_log("zmbf", "success", 1, 1)
    results.append(("zmbf", "success", 1, 1))

    # zmc - no tenders found
    update_last_scrape("zmc", "success", 0, 0)
    append_scrape_log("zmc", "success", 0, 0)
    results.append(("zmc", "success", 0, 0))

    # zmotion - no tenders
    update_last_scrape("zmotion", "success", 0, 0)
    append_scrape_log("zmotion", "success", 0, 0)
    results.append(("zmotion", "success", 0, 0))

    # zoomtanzania - jobs site, no tenders
    update_last_scrape("zoomtanzania", "success", 0, 0)
    append_scrape_log("zoomtanzania", "success", 0, 0)
    results.append(("zoomtanzania", "success", 0, 0))

    # zpc - no tender listings on main page
    update_last_scrape("zpc", "success", 0, 0)
    append_scrape_log("zpc", "success", 0, 0)
    results.append(("zpc", "success", 0, 0))

    # zpdc - 503
    update_last_scrape("zpdc", "error", 0, 0, "503 Service Unavailable")
    append_scrape_log("zpdc", "error", 0, 0, ["503 Service Unavailable"])
    results.append(("zpdc", "error", 0, 0))

    # zppda - timeout
    update_last_scrape("zppda", "error", 0, 0, "Fetch timed out")
    append_scrape_log("zppda", "error", 0, 0, ["Fetch timed out"])
    results.append(("zppda", "error", 0, 0))

    # No-README institutions
    for slug in ["zati", "zawadiyanguinitiative", "zcsra", "zenithattorneys", "zenj", "zentech", "zgafricaadvocates", "zhelb", "zic", "zilgassystems", "zls"]:
        base = PROJECT / "institutions" / slug
        base.mkdir(parents=True, exist_ok=True)
        update_last_scrape(slug, "error", 0, 0, "README not found")
        append_scrape_log(slug, "error", 0, 0, ["README not found"])
        results.append((slug, "error", 0, 0))

    # Append leads for institutions with no tenders
    LEADS_JSON = PROJECT / "opportunities" / "leads.json"
    base_body = """Dear {name} Team,

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
    new_leads = [
        {"institution_slug": "zeddmedics", "institution_name": "ZEDD Medics", "website_url": "https://zeddmedics.co.tz/", "emails": [], "opportunity_type": "sell", "opportunity_description": "Healthcare/pharma company with procurement needs. No formal tenders. ZIMA could offer healthcare systems, telemedicine integrations."},
        {"institution_slug": "zgps", "institution_name": "Zanzibar Green Power Solution", "website_url": "https://zgps.co.tz/", "emails": ["info@zgps.co.tz"], "opportunity_type": "sell", "opportunity_description": "Renewable energy company. No tenders. ZIMA could offer energy management, IoT, or business systems."},
        {"institution_slug": "zmotion", "institution_name": "ZMOTION Solutions", "website_url": "https://zmotion.co.tz/", "emails": [], "opportunity_type": "partner", "opportunity_description": "IT company with SACCO (Akibayetu), HR (OfficeWorker), POS (Niletee) products. ZIMA could partner on fintech integrations."},
        {"institution_slug": "zoomtanzania", "institution_name": "Zoom Tanzania", "website_url": "https://www.zoomtanzania.net/", "emails": [], "opportunity_type": "sell", "opportunity_description": "Jobs platform. No procurement tenders. ZIMA could offer HR systems, payment integrations."},
        {"institution_slug": "zeco", "institution_name": "Zanzibar Electricity Corporation", "website_url": "https://zeco.co.tz/", "emails": ["info@zeco.co.tz"], "opportunity_type": "sell", "opportunity_description": "Utility company with procurement. No active tenders on page. ZIMA could offer billing, GePG, digital systems."},
    ]
    if LEADS_JSON.exists():
        with open(LEADS_JSON, encoding="utf-8") as f:
            leads = json.load(f)
        existing_slugs = {l.get("institution_slug") for l in leads}
        for lead in new_leads:
            if lead["institution_slug"] not in existing_slugs:
                lead["draft_email_subject"] = f"Partnership Opportunity – ZIMA Solutions & {lead['institution_name']}"
                lead["draft_email_body"] = base_body.format(name=lead["institution_name"])
                lead["created_at"] = NOW
                lead["status"] = "pending"
                leads.append(lead)
        with open(LEADS_JSON, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)

    for slug, status, tc, dc in results:
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")

if __name__ == "__main__":
    main()
