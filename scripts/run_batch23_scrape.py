#!/usr/bin/env python3
"""Process scrape results for batch23 - 25 institutions."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch23"

INSTITUTIONS = [
    ("cmggroup", "CMG GROUP", "http://cmggroup.co.tz/", "success", 0, 0),
    ("cmsa", "Capital Market and Securities Authority", "https://cmsa.go.tz/", "error", 0, 0),  # timeout
    ("cmtl", "CMTL Logistics", "https://cmtllogistics.com/", "success", 0, 0),
    ("cmtllogistics", "CMTL Logistics", "https://cmtllogistics.com/", "success", 0, 0),
    ("cnet", "C-Net Technologies", "https://www.onet.co.tz/", "success", 0, 0),
    ("cntech", "Computer Networks & Technology", "https://cntech.co.tz/", "success", 0, 0),
    ("coastalholidays", "Coastal Holidays", "https://coastalholidays.co.tz/", "success", 0, 0),
    ("cobwebtanzania", "Cobweb Tanzania", "https://cobwebtanzania.co.tz/", "success", 0, 0),
    ("cocoda", "COCODA Tanzania", "https://cocoda.or.tz/", "success", 0, 0),
    ("codelab", "CodeLab Tanzania", "https://codelab.co.tz/", "error", 0, 0),  # timeout
    ("codenet", "Codenet Family", "https://codenet.co.tz/", "success", 0, 0),
    ("codestudios", "Code Studios", "https://codestudios.co.tz/", "success", 0, 0),
    ("coffee", "TCB Coffee Board", "https://coffee.go.tz/", "error", 0, 0),  # timeout
    ("coffeecuring", "Mbinga CCCo", "https://coffeecuring.co.tz/", "error", 0, 0),  # suspended
    ("coherent", "Coherent", "https://coherent.co.tz/", "error", 0, 0),  # suspended
    ("colbaconsulting", "COLBA Consulting", "https://colbaconsulting.co.tz/", "error", 0, 0),  # suspended
    ("colorplus", "Safintra/Colorplus", "https://www.safintra.co.za/", "success", 0, 0),
    ("colours", "Colours & Compounds", "https://www.colours.co.tz/", "success", 0, 0),
    ("colvislogistics", "Colvis Logistics", "https://colvislogistics.co.tz/", "success", 0, 0),
    ("compact-energies", "Compact Energies", "https://compactenergies.co.tz/", "success", 0, 0),
    ("computer", "Capricorn Technologies", "https://computer.co.tz/", "success", 0, 0),
    ("comsec", "ComSec", "https://comsec.co.tz/", "success", 0, 0),
    ("connectioninv", "Connection Investment", "https://connectioninv.co.tz/", "success", 0, 0),
    ("constructsyafrica", "Constructsy Africa", "https://constructsyafrica.co.tz/", "success", 0, 0),
    ("controller", "Controller.com", "https://www.controller.com/", "success", 0, 0),
]

def main():
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    summaries = []

    for slug, name, url, status, tender_count, doc_count in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        # Ensure tenders/active exists
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

        # last_scrape.json
        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "next_scrape": None,
            "active_tenders_count": tender_count,
            "status": status,
            "error": "fetch_timeout" if status == "error" and slug in ("cmsa", "codelab", "coffee") else ("site_suspended" if status == "error" else None),
            "run_id": RUN_ID,
        }
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(last_scrape, f, indent=2)

        # scrape_log.json - append
        scrape_log_path = inst_dir / "scrape_log.json"
        if scrape_log_path.exists():
            with open(scrape_log_path) as f:
                log = json.load(f)
        else:
            log = {"runs": []}

        err_msg = None
        if status == "error":
            if slug in ("cmsa", "codelab", "coffee"):
                err_msg = "fetch_timeout"
            elif slug in ("coffeecuring", "coherent", "colbaconsulting"):
                err_msg = "site_suspended"

        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": now,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": 0,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [err_msg] if err_msg else [],
        })
        with open(scrape_log_path, "w") as f:
            json.dump(log, f, indent=2)

        line = f"RESULT|{slug}|{status}|{tender_count}|{doc_count}"
        summaries.append(line)
        print(line)

    print("\n--- BATCH23 COMPLETE ---")
    for s in summaries:
        print(s)

if __name__ == "__main__":
    main()
