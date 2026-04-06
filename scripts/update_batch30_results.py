#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for run_20260315_060430_batch30."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch30"
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Results: (slug, status, tender_count, doc_count, error_msg)
RESULTS = [
    ("dowelef", "success", 0, 0, None),
    ("doz-pie", "success", 0, 0, None),
    ("dpl", "success", 0, 0, None),
    ("dppznz", "success", 0, 0, None),
    ("dreamchasers", "success", 0, 0, None),
    ("dreamdestinationsafaris", "error", 0, 0, "Account suspended"),
    ("drive", "success", 0, 0, None),
    ("drivechangefoundation", "success", 0, 0, None),
    ("drrec", "success", 0, 0, None),
    ("drtc", "success", 0, 0, None),
    ("dse", "success", 0, 0, None),
    ("dsfa", "error", 0, 0, "Fetch timed out"),
    ("dsm", "error", 0, 0, "Fetch timed out"),
    ("dsmcorridor", "success", 0, 0, None),
    ("dsmglass", "success", 0, 0, None),
    ("dsouza", "success", 0, 0, None),
    ("dtcl", "success", 0, 0, None),
    ("duce", "success", 0, 0, None),
    ("duhosting", "success", 0, 0, None),
    ("duhosting.tz", "success", 0, 0, None),
    ("dukalangu", "success", 0, 0, None),
    ("dukanikwetu", "success", 0, 0, None),
    ("durbantz", "success", 0, 0, None),
    ("duthebest", "success", 0, 0, None),
    ("duwasa", "error", 0, 0, "Fetch timed out"),
]


def main():
    for slug, status, tender_count, doc_count, error_msg in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": TIMESTAMP,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "status": status,
            "error": error_msg,
        }
        (inst_dir / "last_scrape.json").write_text(
            json.dumps(last_scrape, indent=2), encoding="utf-8"
        )

        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            log_data = json.loads(scrape_log_path.read_text(encoding="utf-8"))
        else:
            log_data = {"runs": []}

        log_data["runs"].insert(
            0,
            {
                "run_id": RUN_ID,
                "timestamp": TIMESTAMP,
                "duration_seconds": 0,
                "status": status,
                "tenders_found": tender_count,
                "new_tenders": 0,
                "updated_tenders": 0,
                "documents_downloaded": doc_count,
                "errors": [error_msg] if error_msg else [],
            },
        )
        scrape_log_path.write_text(
            json.dumps(log_data, indent=2), encoding="utf-8"
        )

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")


if __name__ == "__main__":
    main()
