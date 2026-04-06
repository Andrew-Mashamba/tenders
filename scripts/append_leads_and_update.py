#!/usr/bin/env python3
"""Append leads to leads.json and update institution scrape state. Run ID: run_20260315_060430_batch112"""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch112"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

LEADS_TO_APPEND = [
    {
        "institution_slug": "swissport",
        "institution_name": "Swissport International AG - Tanzania",
        "website_url": "https://www.swissport.com/en/sustainability/policy/sustainable-procurement",
        "emails": ["tenders@swissport.co.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders on Swissport sustainable procurement page. ZIMA could offer digital transformation, GePG/TIPS integrations, or ICT services for aviation ground handling operations.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Swissport Tanzania",
        "draft_email_body": "Dear Swissport Tanzania Team,\n\nZIMA Solutions Limited specialises in digital transformation for enterprises in Tanzania. We noticed your sustainable procurement commitment and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support Swissport. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "synaptic",
        "institution_name": "Synaptic Solutions tz",
        "website_url": "https://synaptic.co.tz/",
        "emails": ["info@synaptic.co.tz", "info@synaptic.co.ke"],
        "opportunity_type": "partner",
        "opportunity_description": "No formal tenders on Synaptic IT solutions site. ZIMA could partner on ERP/CRM implementations, digital transformation, or Microsoft solutions for East African clients.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Synaptic Solutions",
        "draft_email_body": "Dear Synaptic Solutions Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your ERP and Microsoft solutions expertise and believe we could explore partnership opportunities.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about potential collaboration. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "taas-online",
        "institution_name": "Tanzania Academy of Sciences (TAAS)",
        "website_url": "https://taas-online.or.tz/",
        "emails": ["info@taas-online.or.tz", "yunusmgaya@gmail.com", "asifananyaro@gmail.com"],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders on TAAS site. ZIMA could offer digital systems for scientific institutions, research management, or data platforms.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Tanzania Academy of Sciences",
        "draft_email_body": "Dear TAAS Team,\n\nZIMA Solutions Limited specialises in digital transformation for institutions in Tanzania. We noticed the Academy's work in science and technology and believe we could support your digital infrastructure needs.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• Data analytics and management systems\n• AI-powered solutions\n• HR and project management systems\n\nWe would welcome a conversation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "taborapolytechnic",
        "institution_name": "Tabora Polytechnic College",
        "website_url": "https://taborapolytechnic.ac.tz/",
        "emails": ["taborapolytechnic@yahoo.com"],
        "opportunity_type": "sell",
        "opportunity_description": "No procurement tenders on Tabora Polytechnic site. ZIMA could offer school management systems, e-learning platforms, or fee payment integrations.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & Tabora Polytechnic College",
        "draft_email_body": "Dear Tabora Polytechnic College Team,\n\nZIMA Solutions Limited specialises in digital transformation for educational institutions in Tanzania. We noticed your college and believe we could support your technology goals.\n\nOur offerings include:\n• School Management Systems\n• GePG and fee payment integrations\n• E-learning platforms\n• HR and student information systems\n\nWe would welcome a conversation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
    {
        "institution_slug": "tacaids",
        "institution_name": "Tanzania Commission for AIDS (TACAIDS)",
        "website_url": "https://tacaids.go.tz/pages/tender",
        "emails": ["info@tacaids.go.tz"],
        "opportunity_type": "sell",
        "opportunity_description": "TACAIDS tender page is a placeholder with no active tenders. ZIMA could offer digital systems for health sector, data management, or procurement platforms.",
        "draft_email_subject": "Partnership Opportunity – ZIMA Solutions & TACAIDS",
        "draft_email_body": "Dear TACAIDS Team,\n\nZIMA Solutions Limited specialises in digital transformation for government agencies and health sector in Tanzania. We noticed your tender page and believe we could support your procurement and ICT infrastructure needs.\n\nOur offerings include:\n• GePG and government payment integrations\n• Data management and analytics\n• Procurement and tender management systems\n• Health information systems\n\nWe would welcome a conversation. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    },
]

INST_UPDATES = [
    ("swissport", "success", 0, 0),
    ("synaptic", "success", 0, 0),
    ("taas-online", "success", 0, 0),
    ("taborapolytechnic", "success", 0, 0),
    ("tacaids", "success", 0, 0),
]

def main():
    # Append leads
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    
    # Avoid duplicates by slug
    existing_slugs = {l.get("institution_slug") for l in leads}
    for lead in LEADS_TO_APPEND:
        if lead["institution_slug"] not in existing_slugs:
            leads.append(lead)
            existing_slugs.add(lead["institution_slug"])
    
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    
    # Update last_scrape.json and scrape_log.json for each institution
    for slug, status, tender_count, doc_count in INST_UPDATES:
        inst_dir = PROJECT / "institutions" / slug
        if not inst_dir.exists():
            continue
        last = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": None,
            "active_tenders_count": tender_count,
            "status": status,
            "error": None,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last, f, indent=2)
        
        log_path = inst_dir / "scrape_log.json"
        log = {"runs": []}
        if log_path.exists():
            with open(log_path) as f:
                log = json.load(f)
        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [],
        })
        with open(log_path, "w") as f:
            json.dump(log, f, indent=2)
    
    print("Leads appended and scrape state updated.")

if __name__ == "__main__":
    main()
