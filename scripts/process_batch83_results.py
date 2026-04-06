#!/usr/bin/env python3
"""Process scrape results for run_20260315_060430_batch83 - 25 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch83"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Scrape results: slug -> (status, tender_count, doc_count, error_msg)
RESULTS = {
    "nedico": ("error", 0, 0, "Fetch timed out"),
    "nefs": ("success", 0, 0, None),
    "nelcotech": ("success", 0, 0, None),
    "nelo": ("success", 0, 0, None),
    "neptune": ("success", 0, 0, None),
    "neso": ("success", 0, 0, None),
    "nest": ("error", 0, 0, "Fetch timed out"),
    "net-soft": ("error", 0, 0, "Site returned HTTP 500"),
    "netconcepts": ("success", 0, 0, None),
    "nethatrading": ("success", 0, 0, None),
    "netwas": ("error", 0, 0, "Fetch timed out"),
    "newdaysafari": ("error", 0, 0, "Fetch timed out"),
    "newrainbow": ("success", 0, 0, None),
    "newvinechurch": ("success", 0, 0, None),
    "newvisiondrivingschool": ("success", 0, 0, None),
    "nexellence": ("success", 0, 0, None),
    "nexis": ("success", 0, 0, None),
    "nexlaw": ("success", 0, 0, None),
    "nextsms": ("success", 0, 0, None),
    "nexusnet": ("success", 0, 0, None),
    "nfqclab": ("error", 0, 0, "Fetch timed out"),
    "nfra": ("error", 0, 0, "Fetch timed out"),
    "nfs": ("error", 0, 0, "Fetch timed out"),
    "ngaradc": ("error", 0, 0, "Fetch timed out"),
    "ngare-sero-lodge": ("success", 0, 0, None),
}


def main():
    for slug, (status, tender_count, doc_count, error_msg) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": NOW,
            "active_tenders_count": tender_count,
            "status": status,
            "error": error_msg,
            "run_id": RUN_ID,
        }

        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log_data = json.load(f)
            runs = log_data.get("runs", [])
        else:
            runs = []

        runs.append({
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [error_msg] if error_msg else [],
        })

        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)
        with open(scrape_log_path, "w") as f:
            json.dump({"runs": runs}, f, indent=2)

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")


if __name__ == "__main__":
    main()
