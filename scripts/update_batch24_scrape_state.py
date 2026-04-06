#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for batch24 institutions."""
import json
from pathlib import Path
from datetime import datetime

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch24"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

# Results: slug -> (tender_count, doc_count, status, error?)
RESULTS = {
    "conveyance": (0, 0, "no_tenders", None),
    "coop-bank": (1, 4, "success", None),  # 1 active (CRM), 3 closed, 4 docs
    "cordex": (0, 0, "no_tenders", None),
    "coreit": (0, 0, "no_tenders", None),  # domain welcome page
    "coresecurities": (0, 0, "error", "Fetch timed out"),
    "cornerstone": (0, 0, "no_tenders", None),
    "cosota": (0, 0, "error", "Fetch timed out"),
    "costbenchmark": (0, 0, "no_tenders", None),
    "cotech": (0, 0, "no_tenders", None),
    "cottonclub": (0, 0, "no_tenders", None),
    "counsenuth": (4, 4, "success", None),
    "coyesa": (0, 0, "no_tenders", None),
    "coyeta": (0, 0, "no_tenders", None),
    "cpat": (0, 0, "error", "Fetch timed out"),
    "cpb": (0, 0, "error", "Fetch timed out"),
    "cpctanzania": (0, 0, "no_tenders", None),
    "cpi": (0, 0, "no_tenders", None),
    "cps": (0, 0, "no_tenders", None),
    "cqs": (0, 0, "no_tenders", None),
    "craftmasterbuilders": (0, 0, "no_tenders", None),
    "cranetrader": (0, 0, "no_tenders", None),
    "cravason": (0, 0, "no_tenders", None),
    "crb": (0, 0, "no_tenders", None),
    "crbafricalegal": (0, 0, "no_tenders", None),
    "crdb": (2, 2, "success", None),  # 2 active tenders (Trade Finance, AI/ML)
}

def main():
    for slug, (tender_count, doc_count, status, error) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        if not inst_dir.exists():
            continue
        
        active_count = tender_count if status == "success" else 0
        if slug == "coop-bank":
            active_count = 1  # 1 active, 3 closed
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": "2026-03-14T06:00:00Z",
            "active_tenders_count": active_count,
            "status": "success" if error is None else "error",
            "error": error,
            "run_id": RUN_ID
        }
        
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)
        
        scrape_log = inst_dir / "scrape_log.json"
        if scrape_log.exists():
            with open(scrape_log) as f:
                log = json.load(f)
        else:
            log = {"runs": []}
        
        run_entry = {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": tender_count if status == "success" and tender_count > 0 else 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [error] if error else []
        }
        log["runs"].append(run_entry)
        
        with open(scrape_log, "w") as f:
            json.dump(log, f, indent=2)
        
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

if __name__ == "__main__":
    main()
