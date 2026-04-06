#!/usr/bin/env python3
"""Process scrape results for batch98 (25 institutions: rgsgroup through roscavengersafaris)."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch98"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Scrape results: (slug, status, tender_count, doc_count, error_msg?)
RESULTS = [
    ("rgsgroup", "success", 0, 0, None),
    ("rhotiahealthcentre", "error", 0, 0, "Account suspended"),
    ("ricattorneys", "success", 0, 0, None),
    ("richiedady", "success", 0, 0, None),
    ("rickmedia", "success", 0, 0, None),
    ("ricobed", "success", 0, 0, None),
    ("riftvalleylodge", "success", 0, 0, None),
    ("rightclicksolutions", "success", 0, 0, None),
    ("rightwayschools", "success", 0, 0, None),
    ("rimzone", "success", 0, 0, None),
    ("risoncompany", "success", 0, 0, None),
    ("rita", "success", 0, 0, None),  # Procurement notices from 2021 are closed
    ("riverstonesafaris", "success", 0, 0, None),
    ("riverton", "success", 0, 0, None),
    ("rjitsolutions", "success", 0, 0, None),
    ("rkgroup", "success", 0, 0, None),
    ("rmb", "error", 0, 0, "Fetch timeout/connection failed"),
    ("rmholdings", "success", 0, 0, None),
    ("roadsfund", "error", 0, 0, "Fetch timeout/connection failed"),
    ("rocksolutionlimited", "error", 0, 0, "URL returns webmail login, not company site"),
    ("rockson", "success", 0, 0, None),
    ("rolinternational", "error", 0, 0, "Account suspended"),
    ("rookconsultants", "success", 0, 0, None),
    ("rorica", "success", 0, 0, None),
    ("roscavengersafaris", "success", 0, 0, None),
]


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)


def update_last_scrape(inst_dir: Path, slug: str, status: str, tender_count: int, err: str | None):
    data = {
        "institution": slug,
        "last_scrape": NOW,
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "status": status,
        "error": err,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(data, f, indent=2)


def update_scrape_log(inst_dir: Path, status: str, tender_count: int, doc_count: int, err: str | None):
    log_path = inst_dir / "scrape_log.json"
    runs = []
    if log_path.exists():
        with open(log_path) as f:
            data = json.load(f)
            runs = data.get("runs", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
    entry = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [err] if err else [],
    }
    runs.append(entry)
    with open(log_path, "w") as f:
        json.dump({"runs": runs}, f, indent=2)


def main():
    summaries = []
    for slug, status, tender_count, doc_count, err in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        if not inst_dir.exists():
            summaries.append(f"RESULT|{slug}|error|0|0")
            continue
        ensure_dirs(inst_dir)
        update_last_scrape(inst_dir, slug, status, tender_count, err)
        update_scrape_log(inst_dir, status, tender_count, doc_count, err)
        summaries.append(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
    for s in summaries:
        print(s)


if __name__ == "__main__":
    main()
