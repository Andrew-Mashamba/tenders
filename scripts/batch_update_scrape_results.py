#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for a batch of institutions."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch70"

INSTITUTIONS = [
    ("mapambazukosaccos", 0, 0, "success", None),
    ("mapdata", 0, 0, "success", None),
    ("mapembeloesg", 0, 0, "success", None),
    ("mapendocapital", 0, 0, "success", None),
    ("maple", 0, 0, "success", None),
    ("maple-bloom", 0, 0, "success", None),
    ("maps-edge", 0, 0, "success", None),
    ("mapsedge", 0, 0, "success", None),
    ("mara", 0, 0, "success", None),
    ("maranathahospitals", 0, 0, "success", None),
    ("marango", 0, 0, "success", None),
    ("marconsolar", 0, 0, "success", None),
    ("marenga", 0, 0, "success", None),
    ("marianschools", 0, 0, "success", None),
    ("maricedrycleaners", 0, 0, "success", None),
    ("marin-maskin", 0, 0, "success", None),
    ("marinair", 0, 0, "success", None),
    ("marineparks", 0, 0, "success", None),
    ("marketaxis", 0, 0, "success", None),
    ("marketbook", 0, 0, "success", None),
    ("marklarry", 0, 0, "success", None),
    ("marmoegranito", 0, 0, "success", None),
    ("mars", 0, 0, "success", None),
    ("marscomm", 0, 0, "success", None),
    ("marscommunications", 0, 0, "success", None),
]


def main():
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    for slug, tenders, docs, status, err in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "next_scrape": now[:10],
            "active_tenders_count": tenders,
            "status": status,
            "error": err,
            "run_id": RUN_ID,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log = {"runs": []}
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            with open(log_path) as f:
                scrape_log = json.load(f)
        scrape_log["runs"].insert(
            0,
            {
                "run_id": RUN_ID,
                "timestamp": now,
                "duration_seconds": 0,
                "status": status,
                "tenders_found": tenders,
                "new_tenders": 0,
                "updated_tenders": 0,
                "documents_downloaded": docs,
                "errors": [err] if err else [],
            },
        )
        with open(log_path, "w") as f:
            json.dump(scrape_log, f, indent=2)

        print(f"RESULT|{slug}|{status}|{tenders}|{docs}")


if __name__ == "__main__":
    main()
