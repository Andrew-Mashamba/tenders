#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for batch94 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch94"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

INSTITUTIONS = [
    ("qualitywater", 0, 0, "no_tenders"),
    ("qualtrust", 0, 0, "no_tenders"),
    ("quantum", 0, 0, "no_tenders"),
    ("quantumarchitects", 0, 0, "no_tenders"),
    ("quantumresearch", 0, 0, "error"),  # 502
    ("queensgem", 0, 0, "no_tenders"),
    ("quickstepinvestment", 0, 0, "no_tenders"),
    ("quixgroup", 0, 0, "no_tenders"),
    ("raawu", 0, 0, "no_tenders"),
    ("rabikafarm", 0, 0, "no_tenders"),
    ("radarsecurity", 0, 0, "no_tenders"),
    ("radian", 0, 0, "no_tenders"),
    ("radio1", 0, 0, "no_tenders"),
    ("radio5fm", 0, 0, "no_tenders"),
    ("radiojoyfm", 0, 0, "no_tenders"),
    ("radiokicheko", 0, 0, "no_tenders"),
    ("radiokwizera", 0, 0, "no_tenders"),
    ("radiowave", 0, 0, "no_tenders"),
    ("rafikiattorneys", 0, 0, "no_tenders"),
    ("rafikisdo", 1, 3, "success"),  # 1 tender, 3 docs
    ("rahamiagri", 0, 0, "no_tenders"),
    ("rai", 0, 0, "no_tenders"),
    ("rainoenterprise", 0, 0, "no_tenders"),
    ("raissa", 0, 0, "no_tenders"),
    ("raitech", 0, 0, "no_tenders"),
]


def main():
    for slug, tender_count, doc_count, status in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "run_id": RUN_ID,
            "scraped_at": NOW,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
            "error": "502 Bad Gateway" if slug == "quantumresearch" else None,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        scrape_log = []
        log_path = inst_dir / "scrape_log.json"
        if log_path.exists():
            with open(log_path) as f:
                scrape_log = json.load(f)
        if not isinstance(scrape_log, list):
            scrape_log = []
        scrape_log.append({
            "run_id": RUN_ID,
            "scraped_at": NOW,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
        })
        with open(log_path, "w") as f:
            json.dump(scrape_log, f, indent=2)

    print(f"Updated last_scrape.json and scrape_log.json for {len(INSTITUTIONS)} institutions")


if __name__ == "__main__":
    main()
