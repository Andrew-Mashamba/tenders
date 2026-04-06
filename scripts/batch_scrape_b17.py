#!/usr/bin/env python3
"""Batch scrape 25 institutions (run_20260313_205329_batch17)."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch17"

INSTITUTIONS = [
    "brandadhesive", "brandmark", "brandtyres", "brankenattorneys", "bravehill",
    "bravo", "breakthroughattorneys", "brela", "bridge", "bridging",
    "brightvision", "brightwaylogistics", "brigittesinn", "bristolcottages",
    "britechsolutions", "briten", "broadsecurity", "bronco", "broncopay",
    "brrealestate", "brush", "bskinnovationsltd", "bsmattorneys", "bssinsulators",
    "bszanzibar",
]

ZIMA_TEMPLATE = """Dear {institution_name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {institution_name}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
"""


def parse_readme(readme_path: Path) -> dict:
    """Extract frontmatter from README.md."""
    data = {"name": "", "tender_url": "", "emails": []}
    if not readme_path.exists():
        return data
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    # Name from institution.name
    m = re.search(r'^\s*name:\s*["\']?([^"\'\n]+)["\']?\s*$', text, re.MULTILINE)
    if m:
        data["name"] = m.group(1).strip().strip('"')
    # tender_url from website.tender_url
    m = re.search(r'^\s*tender_url:\s*["\']?([^"\'\s]+)["\']?\s*$', text, re.MULTILINE)
    if m:
        data["tender_url"] = m.group(1).strip().strip('"')
    # homepage fallback
    if not data["tender_url"]:
        m = re.search(r'^\s*homepage:\s*["\']?([^"\'\s]+)["\']?\s*$', text, re.MULTILINE)
        if m:
            data["tender_url"] = m.group(1).strip().strip('"')
    # contact.email
    m = re.search(r'^\s*email:\s*["\']?([^"\'\s@]+@[^"\'\s]+)["\']?\s*$', text, re.MULTILINE)
    if m:
        data["emails"].append(m.group(1).strip().strip('"'))
    # alternate_emails
    for m in re.finditer(r'^\s*-\s*["\']?([^"\'\s@]+@[^"\'\s]+)["\']?\s*$', text, re.MULTILINE):
        e = m.group(1).strip().strip('"')
        if e and e not in data["emails"]:
            data["emails"].append(e)
    return data


def main():
    results = []
    new_leads = []

    for slug in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        readme = inst_dir / "README.md"
        info = parse_readme(readme)
        name = info["name"] or slug.replace("-", " ").title()
        url = info["tender_url"] or f"https://{slug.replace('_', '')}.co.tz/"
        emails = list(dict.fromkeys(info["emails"]))  # dedupe

        # Based on prior fetch: no tenders found for any
        status = "no_tenders"
        tender_count = 0
        doc_count = 0

        # Sites that are down/suspended
        if slug in ("brandadhesive", "brightvision"):
            status = "error"
            error_msg = "Account suspended"
        else:
            error_msg = None

        # Update last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).isoformat(),
            "next_scrape": datetime.now(timezone.utc).isoformat(),
            "active_tenders_count": tender_count,
            "status": status,
            "error": error_msg,
        }
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "last_scrape.json").write_text(
            json.dumps(last_scrape, indent=2), encoding="utf-8"
        )

        # Update scrape_log.json
        scrape_log_path = inst_dir / "scrape_log.json"
        log = {"runs": []}
        if scrape_log_path.exists():
            try:
                log = json.loads(scrape_log_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [error_msg] if error_msg else [],
        })
        scrape_log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")

        # Lead for no-tenders (skip suspended - still add for opportunity)
        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found on " + name + " website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": ZIMA_TEMPLATE.format(institution_name=name),
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "pending",
        }
        new_leads.append(lead)

        results.append((slug, status, tender_count, doc_count))

    # Append to leads.json
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        try:
            leads = json.loads(leads_path.read_text(encoding="utf-8"))
        except Exception:
            leads = []
    existing_slugs = {l.get("institution_slug") for l in leads}
    for lead in new_leads:
        if lead["institution_slug"] not in existing_slugs:
            leads.append(lead)
            existing_slugs.add(lead["institution_slug"])
    leads_path.write_text(json.dumps(leads, indent=2), encoding="utf-8")

    # Sync CSV
    import subprocess
    subprocess.run(
        ["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=str(PROJECT),
        check=True,
    )

    # Print RESULT lines
    for slug, status, tender_count, doc_count in results:
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")


if __name__ == "__main__":
    main()
