#!/usr/bin/env python3
"""Update last_scrape.json and scrape_log.json for a batch of institutions."""
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch126"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Results: slug -> (status, tender_count, doc_count)
RESULTS = {
    "veercom": ("no_tenders", 0, 0),
    "vega": ("no_tenders", 0, 0),
    "vegastar": ("no_tenders", 0, 0),
    "vegrab": ("ok", 1, 1),
    "velmalaw": ("no_tenders", 0, 0),
    "vemisafaris": ("no_tenders", 0, 0),
    "vemmaattorneys": ("no_tenders", 0, 0),
    "vendorconsult": ("error", 0, 0),  # timed out
    "vercoe": ("no_tenders", 0, 0),
    "veridocglobal": ("no_tenders", 0, 0),
    "veta": ("error", 0, 0),  # timed out
    "vetah": ("no_tenders", 0, 0),
    "vevinainternational": ("no_tenders", 0, 0),
    "vfsl": ("error", 0, 0),  # timed out
    "vgk": ("no_tenders", 0, 0),
    "vicapoc": ("no_tenders", 0, 0),
    "vicatel": ("no_tenders", 0, 0),
    "victoriafinance": ("no_tenders", 0, 0),
    "victorstephen": ("no_tenders", 0, 0),
    "victoryauditors": ("no_tenders", 0, 0),
    "vidomedia": ("error", 0, 0),  # timed out
    "vihasco": ("no_tenders", 0, 0),
    "vijijitanzania": ("no_tenders", 0, 0),
    "vil": ("no_tenders", 0, 0),
    "vipuri": ("no_tenders", 0, 0),
}

def main():
    for slug, (status, tender_count, doc_count) in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        last_scrape = {
            "run_id": RUN_ID,
            "scraped_at": NOW,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
            "error": "Site timed out or blocked" if status == "error" else None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2))
        log_entry = {
            "run_id": RUN_ID,
            "scraped_at": NOW,
            "status": status,
            "tender_count": tender_count,
            "doc_count": doc_count,
        }
        scrape_log_path = inst_dir / "scrape_log.json"
        log_entries = []
        if scrape_log_path.exists():
            try:
                log_entries = json.loads(scrape_log_path.read_text())
                if not isinstance(log_entries, list):
                    log_entries = []
            except Exception:
                log_entries = []
        log_entries.append(log_entry)
        scrape_log_path.write_text(json.dumps(log_entries[-50:], indent=2))
    print(f"Updated scrape state for {len(RESULTS)} institutions")

if __name__ == "__main__":
    main()
