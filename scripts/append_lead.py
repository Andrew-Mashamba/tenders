#!/usr/bin/env python3
"""Append a single lead to opportunities/leads.json."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
LEADS_JSON = PROJECT / "opportunities" / "leads.json"


def append_lead(lead: dict) -> None:
    lead["created_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    lead.setdefault("status", "pending")
    leads = []
    if LEADS_JSON.exists():
        with open(LEADS_JSON) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    # Check if slug already exists
    slugs = {l.get("institution_slug") for l in leads}
    if lead.get("institution_slug") in slugs:
        return  # Skip duplicate
    leads.append(lead)
    with open(LEADS_JSON, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    # Read lead from stdin as JSON
    lead = json.load(sys.stdin)
    append_lead(lead)
