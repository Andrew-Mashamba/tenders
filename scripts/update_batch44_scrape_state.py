#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for batch44 institutions."""
import json
from pathlib import Path
from datetime import datetime

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch44"
TS = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# slug -> (status, tender_count, doc_count, error?)
RESULTS = [
    ("gusa", "success", 0, 0, None),
    ("guta", "success", 0, 0, None),
    ("habarileo", "success", 0, 0, None),
    ("habarismz", "error", 0, 0, "Fetch timed out"),
    ("habibafricanbank", "success", 0, 0, None),
    ("hacoca", "success", 1, 0, None),
    ("hakiardhi", "success", 0, 0, None),
    ("hakirasilimali", "success", 1, 0, None),
    ("haleluyatours", "success", 0, 0, None),
    ("hallmarkattorneys", "error", 0, 0, "Fetch timed out"),
    ("halogame", "error", 0, 0, "Fetch timed out"),
    ("halotel", "success", 0, 0, None),
    ("hampshire", "success", 0, 0, None),
    ("hamtours", "success", 0, 0, None),
    ("hanangdc", "error", 0, 0, "Fetch timed out"),
    ("handenitc", "error", 0, 0, "Fetch timed out"),
    ("handman", "success", 0, 0, None),
    ("hanspaul", "error", 0, 0, "Fetch timed out"),
    ("happychildren", "success", 0, 0, None),
    ("harmonyhotel", "success", 0, 0, None),
    ("harusi", "success", 0, 0, None),
    ("hasa", "success", 0, 0, None),
    ("hasafa", "success", 0, 0, None),
    ("hashtech", "success", 0, 0, None),
    ("hasnet", "success", 0, 0, None),
]

def main():
    for slug, status, tender_count, doc_count, err in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        last = {
            "institution": slug,
            "last_scrape": TS,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "documents_downloaded": doc_count,
            "status": status,
            "error": err,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2))
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            log = json.loads(log_path.read_text())
        else:
            log = {"runs": []}
        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": TS,
            "status": status,
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        })
        log_path.write_text(json.dumps(log, indent=2))
    print(f"Updated {len(RESULTS)} institutions")

if __name__ == "__main__":
    main()
