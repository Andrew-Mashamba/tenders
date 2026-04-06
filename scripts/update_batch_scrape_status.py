#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for batch78 institutions."""
import json
from pathlib import Path
from datetime import datetime

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch78"
NOW = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:23] + "Z"

# slug -> (status, tender_count, doc_count, error?)
RESULTS = {
    "mpwapwadc": ("error", 0, 0, "Fetch timed out"),
    "mpwapwatc": ("error", 0, 0, "Account suspended"),
    "mrhp": ("error", 0, 0, "Page not found (404)"),
    "mri": ("success", 1, 1, None),
    "mrimbapalmhotel": ("success", 0, 0, None),
    "mrishoconsult": ("success", 0, 0, None),
    "mrutuagrosolutions": ("success", 0, 0, None),
    "msafiriexpress": ("error", 0, 0, "Account suspended"),
    "msameja": ("success", 0, 0, None),
    "mscl": ("success", 0, 0, None),
    "msekeni": ("success", 0, 0, None),
    "mservices": ("success", 0, 0, None),
    "msichana": ("success", 0, 0, None),
    "msminvestment": ("success", 0, 0, None),
    "msoft": ("success", 0, 0, None),
    "msomeni": ("success", 0, 0, None),
    "msongolainstitute": ("success", 0, 0, None),
    "msosiexpress": ("success", 0, 0, None),
    "mstcdc": ("success", 1, 0, None),
    "mstj": ("success", 0, 0, None),
    "msumbanews": ("success", 0, 0, None),
    "mtaakwamtaa": ("success", 0, 0, None),
    "mtaji": ("success", 0, 0, None),
    "mtendelehotel": ("success", 0, 0, None),
    "mtmerugamelodge": ("success", 0, 0, None),
}

def main():
    for slug, (status, tender_count, doc_count, err) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW[:10] + "T06:00:00Z",
            "active_tenders_count": tender_count,
            "status": status,
            "error": err,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log_path = inst_dir / "scrape_log.json"
        log_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": tender_count,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        }
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                data = json.load(f)
            runs = data.get("runs", [])
        else:
            runs = []
        runs.append(log_entry)
        with open(scrape_log_path, "w") as f:
            json.dump({"runs": runs}, f, indent=2)

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

if __name__ == "__main__":
    main()
