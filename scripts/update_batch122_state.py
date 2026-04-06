#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for batch 122 institutions."""
import json
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch122"
NOW = "2026-03-14T08:54:00Z"

# slug -> (status, tender_count, doc_count, error)
RESULTS = {
    "transafrica": ("no_tenders", 0, 0, None),
    "transec": ("no_tenders", 0, 0, None),
    "transpac": ("no_tenders", 0, 0, "Site under maintenance"),
    "transplant": ("no_tenders", 0, 0, None),
    "trantruck": ("no_tenders", 0, 0, None),
    "travelhype": ("no_tenders", 0, 0, None),
    "traveltrack": ("no_tenders", 0, 0, None),
    "trc": ("error", 0, 0, "Fetch timeout"),
    "trcs": ("success", 1, 0, None),
    "trendymedia": ("no_tenders", 0, 0, None),
    "triniti": ("no_tenders", 0, 0, None),
    "trinitylogistics": ("no_tenders", 0, 0, None),
    "trinityschools": ("no_tenders", 0, 0, None),
    "trinitysolar": ("no_tenders", 0, 0, None),
    "tripleafricaadventures": ("no_tenders", 0, 0, None),
    "trisoftnet": ("no_tenders", 0, 0, None),
    "trix": ("no_tenders", 0, 0, None),
    "trmega": ("no_tenders", 0, 0, None),
    "tro": ("error", 0, 0, "Fetch timeout"),
    "trueimage": ("no_tenders", 0, 0, None),
    "truemaisha": ("no_tenders", 0, 0, None),
    "tutume": ("no_tenders", 0, 0, None),
    "tuwasa": ("success", 1, 1, None),
    "tva": ("no_tenders", 0, 0, None),
    "tvla": ("error", 0, 0, "Fetch timeout"),
}


def main():
    for slug, (status, tender_count, doc_count, error) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        entry = {
            "run_id": RUN_ID,
            "scraped_at": NOW,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
            "error": error,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(entry, indent=2))
        log_path = inst_dir / "scrape_log.json"
        log = []
        if log_path.exists():
            try:
                log = json.loads(log_path.read_text())
                if not isinstance(log, list):
                    log = []
            except Exception:
                log = []
        log.append(entry)
        log_path.write_text(json.dumps(log, indent=2))
    print("Updated last_scrape.json and scrape_log.json for 25 institutions")


if __name__ == "__main__":
    main()
