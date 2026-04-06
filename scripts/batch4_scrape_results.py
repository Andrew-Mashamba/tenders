#!/usr/bin/env python3
"""Process batch4 scrape results: no tenders found, create opportunity leads and update scrape state."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch4"
ZIMA_README = PROJECT / "zima_solutions_ltd" / "README.md"

# Institution config: slug, name, website_url, emails from README
INSTITUTIONS = [
    ("afritech", "Africom Ltd", "https://africom.co.tz/", ["033 248-248"]),
    ("afritrust", "Afritrust Group Ltd", "https://afritrust.co.tz/", ["info@afritrust.com"]),
    ("afriwag", "Afriwag", "https://afriwag.or.tz/", ["info@afriwag.or.tz", "info@afriwag.co.tz"]),
    ("afriyantz", "Afriyan Tanzania", "https://afriyantz.or.tz/", []),
    ("afrogems", "The Tanzanite Dream", "https://tanzanite888.tz/", []),
    ("afroilgroup", "AFROIL", "https://afroilgroup.co.tz/", []),
    ("afroinsurance", "Afro Insurance Agency", "https://afroinsurance.co.tz/", []),
    ("afromark", "Afromark", "https://afromark.co.tz/", ["info@afromark.co.tz"]),
    ("afrosense", "Afrosense", "https://afrosense.co.tz/", ["info@afrosense.co.tz"]),
    ("afyaconnect", "AfyaConnect", "https://www.afyaconnect.co.tz/", []),
    ("afyadepot", "AfyaDepo Platform", "https://afyadepot.co.tz/", []),
    ("afyadirectory", "Tanzania Medical Directory", "https://www.afyadirectory.co.tz/", ["admin@afyadirectory.co.tz"]),
    ("afyaplus", "Afyaplus Tanzania", "https://afyaplus.co.tz/", ["info@afyaplus.co.tz"]),
    ("afyaplustz", "Afyaplus Organization", "https://afyaplustz.or.tz/", ["info@afyaplustz.or.tz"]),
    ("age-upgrade", "Age-Upgrade", "https://age-upgrade.or.tz/", ["info@age-upgrade.or.tz"]),
    ("agematours", "AGEMA Tours and Safaris", "https://www.agematours.co.tz/", ["info@agematours.co.tz"]),
    ("agenergies", "AG Energies", "https://agenergies.co.tz/", ["info@agenergies.co.tz"]),
    ("agim", "AGIM Consultants", "https://www.agim.co.tz/", []),
    ("agitf", "AGITF", "https://agitf.go.tz/", ["info@agitf.go.tz"]),
    ("aglex", "Aglex Company Limited", "https://aglex.co.tz/", ["info@aglex.co.tz", "radiocalls@aglex.co.tz"]),
    ("agricom", "Agricom Africa", "https://agricom.co.tz/", ["info@agricom.co.tz"]),
    ("agricomafrica", "Agricom Africa", "https://agricom.co.tz/", ["info@agricom.co.tz"]),
    ("agriedo", "Agriedo", "https://agriedo.co.tz/", ["agriedo@agriedo.co.tz", "info@agriedo.co.tz"]),
    ("agripromise", "Agripromise Company Limited", "https://agripromise.co.tz/", ["info@agripromise.co.tz"]),
    ("agrishine", "Agrishine Company Limited", "https://agrishine.co.tz/", ["info@agrishine.co.tz"]),
]

# Sites that timed out - scrape with error status
FETCH_ERRORS = {"age-upgrade", "agematours", "agitf"}

DRAFT_BODY = """Dear {institution_name} Team,

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


def extract_emails_from_text(text: str) -> list[str]:
    """Extract email addresses from text."""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    found = set(re.findall(pattern, text))
    # Filter out common non-email patterns
    exclude = {"example.com", "email.com", "domain.com", "cdn-cgi", "sentry.io", "wixpress.com"}
    return [e for e in sorted(found) if not any(x in e.lower() for x in exclude)]


def main():
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    leads_path = PROJECT / "opportunities" / "leads.json"

    # Load existing leads
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

    results = []
    new_leads_count = 0

    for slug, name, url, known_emails in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        status = "error" if slug in FETCH_ERRORS else "no_tenders"
        tender_count = 0
        doc_count = 0

        # Scrape emails from README (we use known from README; in full scrape would fetch page)
        emails = list(dict.fromkeys(known_emails))  # dedupe preserving order

        # Opportunity lead
        opportunity_type = "sell"
        if "afyadepot" in slug or "afyaplus" in slug:
            opportunity_type = "partner"
        opportunity_desc = (
            "No formal tenders found on {} website. ZIMA Solutions could offer digital transformation, "
            "fintech integrations, or ICT services."
        ).format(name)

        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails if emails else [],
            "opportunity_type": opportunity_type,
            "opportunity_description": opportunity_desc,
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": DRAFT_BODY.format(institution_name=name),
            "created_at": now,
            "status": "pending",
        }

        # Append lead only if not already present (avoid duplicates)
        existing_slugs = {l.get("institution_slug") for l in leads}
        if slug not in existing_slugs:
            leads.append(lead)
            new_leads_count += 1

        # Update last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "run_id": RUN_ID,
            "active_tenders_count": 0,
            "status": status,
            "error": "Fetch timed out" if slug in FETCH_ERRORS else None,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # Update scrape_log.json (format: list of run entries)
        log_path = inst_dir / "scrape_log.json"
        log_entries = []
        if log_path.exists():
            with open(log_path) as f:
                data = json.load(f)
            log_entries = data if isinstance(data, list) else data.get("runs", [])
        log_entries.append({
            "run_id": RUN_ID,
            "institution": slug,
            "timestamp": now,
            "status": status,
            "tenders_found": 0,
            "documents_downloaded": 0,
            "notes": "Fetch timed out" if slug in FETCH_ERRORS else "No active tenders found.",
        })
        with open(log_path, "w") as f:
            json.dump(log_entries, f, indent=2)

        results.append((slug, status, tender_count, doc_count))

    # Save leads only if we added any (avoid rewriting huge file unnecessarily)
    if new_leads_count > 0:
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)

    return results


if __name__ == "__main__":
    results = main()
    for slug, status, tc, dc in results:
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")
