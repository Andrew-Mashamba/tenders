#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for batch53 institutions."""
import json
from pathlib import Path
from datetime import datetime, timedelta

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch53"

INSTITUTIONS = [
    ("itrack", "https://itrack.co.tz/", 0, 0, None),
    ("itransport", "https://itransport.co.tz/", 0, 0, "Account suspended"),
    ("itss", "https://itss.co.tz/", 0, 0, None),
    ("itstars", "https://itstars.co.tz/", 0, 0, None),
    ("itsupport", "https://itsupport.co.tz/", 0, 0, "Account suspended"),
    ("itv", "https://www.itv.co.tz/", 0, 0, None),
    ("iyangroup", "https://iyangroup.co.tz/", 0, 0, None),
    ("jadon", "https://jadon.co.tz/", 0, 0, None),
    ("jafferyacademy", "https://jafferyacademy.co.tz/", 0, 0, None),
    ("jafrexsystems", "https://jafrexsystems.co.tz/", 0, 0, None),
    ("jaire", "http://jaire.co.tz/", 0, 0, None),
    ("jamaap", "https://jamaap.co.tz/", 0, 0, None),
    ("jambo", "https://jambo.co.tz/", 0, 0, None),
    ("jambotelematics", "https://jambotelematics.co.tz/", 0, 0, None),
    ("jamhurimedia", "https://www.jamhurimedia.co.tz/", 0, 0, None),
    ("jamhuristationers", "https://jamhuristationers.co.tz/", 0, 0, None),
    ("jamii", "https://jamii.go.tz/publications/tenders", 0, 0, "Fetch timed out"),
    ("jamiimedia", "https://jamiimedia.co.tz/", 0, 0, None),
    ("jamsolutions", "https://jamsolutions.co.tz/", 0, 0, None),
    ("janstevensinternational", "https://janstevensinternational.co.tz/", 0, 0, None),
    ("jaomaffl", "https://jaomaffl.co.tz/", 0, 0, None),
    ("jasecinvestment", "https://jasecinvestment.co.tz/", 0, 0, None),
    ("jasmai", "https://jasmai.co.tz/", 0, 0, None),
    ("jassociates", "https://jassociates.co.tz/", 0, 0, None),
    ("jaynir", "https://jaynir.co.tz/", 0, 0, None),
]

def main():
    now = datetime.utcnow()
    now_str = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    next_str = (now + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    for slug, url, tenders, docs, err in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": now_str,
            "next_scrape": next_str,
            "active_tenders_count": tenders,
            "status": "success" if not err else "error",
            "error": err,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log = {"runs": []}
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            with open(log_path) as f:
                scrape_log = json.load(f)
        scrape_log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": now_str,
            "duration_seconds": 0,
            "status": "success" if not err else "error",
            "tenders_found": tenders,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": docs,
            "errors": [err] if err else [],
        })
        with open(log_path, "w") as f:
            json.dump(scrape_log, f, indent=2)

    print(f"Updated {len(INSTITUTIONS)} institutions")

if __name__ == "__main__":
    main()
