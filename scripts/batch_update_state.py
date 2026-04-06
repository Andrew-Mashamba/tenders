#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for a batch of institutions."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch6"
INSTITUTIONS = [
    "akiplaw", "akros", "alamaarchitecture", "alat", "albitech", "alc", "aleka",
    "alexiamedical", "alfahidistationery", "alfapharma", "algebraschools", "alharamein",
    "alinlawcare", "alitrah", "aljigardening", "allchemicoltd", "alliancelife", "alliedgroup",
    "allstar", "almaha", "almc", "alphaagrovets", "alphaassociates", "alphafabricators",
    "altavistaengineering",
]

def main():
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    for slug in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "run_id": RUN_ID,
            "active_tenders_count": 0,
            "status": "success",
            "error": None,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log_path = inst_dir / "scrape_log.json"
        runs = []
        if scrape_log_path.exists():
            try:
                with open(scrape_log_path) as f:
                    data = json.load(f)
                runs = data if isinstance(data, list) else data.get("runs", [])
            except (json.JSONDecodeError, TypeError):
                runs = []

        runs.append({
            "run_id": RUN_ID,
            "timestamp": now,
            "status": "ok",
            "tenders_found": 0,
            "new_tenders": 0,
            "documents_downloaded": 0,
            "tender_ids": [],
            "errors": [],
        })
        with open(scrape_log_path, "w") as f:
            json.dump(runs, f, indent=2)

        print(f"RESULT|{slug}|no_tenders|0|0")

if __name__ == "__main__":
    main()
