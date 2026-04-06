#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for batch73 run."""
import json
from pathlib import Path
from datetime import datetime

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch73"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# slug -> (status, error_msg)
RESULTS = {
    "meatudc": ("error", "Site unreachable or SSL error"),
    "mecco": ("no_tenders", None),
    "mecompany": ("no_tenders", None),
    "mediaworksglobal": ("no_tenders", None),
    "medox": ("no_tenders", None),
    "meerkatz": ("error", "Account suspended"),
    "megalink": ("no_tenders", None),
    "megnacio": ("no_tenders", None),
    "mehtaassociates": ("no_tenders", None),
    "melegreen": ("no_tenders", None),
    "melsat": ("no_tenders", None),
    "membiinvestment": ("no_tenders", None),
    "menu": ("no_tenders", None),
    "mepro": ("error", "Fetch timeout"),
    "merakiconsult": ("no_tenders", None),
    "merca": ("no_tenders", None),
    "mercibel": ("no_tenders", None),
    "meridianbet": ("error", "Blocked by Cloudflare"),
    "meridianbetsport": ("error", "Fetch timeout"),
    "meritech": ("no_tenders", None),
    "meritengineering": ("no_tenders", None),
    "messaging-service": ("no_tenders", None),
    "meteo": ("error", "Fetch timeout"),
    "metro": ("error", "Fetch timeout"),
    "mewata": ("no_tenders", None),
}


def main():
    for slug, (status, err) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW,
            "active_tenders_count": 0,
            "status": status,
            "error": err,
            "run_id": RUN_ID,
        }
        (inst_dir / "last_scrape.json").write_text(
            json.dumps(last_scrape, indent=2), encoding="utf-8"
        )

        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log = json.load(f)
        else:
            log = {"runs": []}

        run_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": 0,
            "documents_downloaded": 0,
            "errors": [err] if err else [],
        }
        log["runs"].append(run_entry)
        scrape_log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")

        print(f"RESULT|{slug}|{status}|0|0")


if __name__ == "__main__":
    main()
