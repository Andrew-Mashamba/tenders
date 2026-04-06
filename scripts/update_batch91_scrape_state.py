#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for batch91 institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch91"
NOW = datetime.now(timezone.utc).isoformat()

# (slug, status, tender_count, doc_count, error?)
RESULTS = [
    ("pimak", "no_tenders", 0, 0, None),
    ("pinnacle", "no_tenders", 0, 0, None),
    ("pioneerbuilders", "no_tenders", 0, 0, None),
    ("pis", "no_tenders", 0, 0, None),
    ("piussec", "no_tenders", 0, 0, None),
    ("pivotech", "no_tenders", 0, 0, None),
    ("pivotechgroup", "no_tenders", 0, 0, None),
    ("pkadventure", "no_tenders", 0, 0, None),
    ("planetfitness", "no_tenders", 0, 0, None),
    ("planex", "no_tenders", 0, 0, None),
    ("planningznz", "no_tenders", 0, 0, "eprocurement requires login"),
    ("plasco", "no_tenders", 0, 0, None),
    ("plpdf", "no_tenders", 0, 0, "fetch timeout"),
    ("pluglab", "no_tenders", 0, 0, None),
    ("plustronics", "no_tenders", 0, 0, None),
    ("plvdigital", "no_tenders", 0, 0, None),
    ("pmcgl", "no_tenders", 0, 0, None),
    ("pmgroup", "no_tenders", 0, 0, None),
    ("pmmicd", "no_tenders", 0, 0, None),
    ("pmo", "no_tenders", 0, 0, None),
    ("pmstec", "no_tenders", 0, 0, None),
    ("pnelectrics", "no_tenders", 0, 0, None),
    ("poaenergies", "no_tenders", 0, 0, None),
    ("policyforum", "success", 1, 1, None),
    ("poppins", "no_tenders", 0, 0, None),
]

def main():
    for slug, status, tender_count, doc_count, err in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "next_scrape": "2026-03-15T06:00:00Z",
            "active_tenders_count": tender_count,
            "status": "success" if status == "success" else "no_tenders",
            "error": err,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2))

        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            log = json.loads(scrape_log_path.read_text())
        else:
            log = {"runs": []}
        log["runs"].insert(0, {
            "run_id": RUN_ID,
            "timestamp": NOW,
            "status": "success" if status == "success" else "no_tenders",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [err] if err else [],
        })
        scrape_log_path.write_text(json.dumps(log, indent=2))

    print(f"Updated scrape state for {len(RESULTS)} institutions")

if __name__ == "__main__":
    main()
