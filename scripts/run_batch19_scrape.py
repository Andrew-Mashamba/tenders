#!/usr/bin/env python3
"""Process 25 institutions for run_20260315_060430_batch19 - update scrape state."""
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch19"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

INSTITUTIONS = [
    ("buy4me", "Buy For Me", "https://buy4me.co.tz/", "success", 0, 0),
    ("buyforme", "Buy For Me", "https://buy4me.co.tz/", "success", 0, 0),
    ("bvk", "BVK Logistics", "https://bvk.co.tz/", "success", 0, 0),
    ("bytrade", "ByTrade Tanzania", "https://bytrade.or.tz/", "success", 0, 0),
    ("c-labs", "C-Labs", "https://c-labs.co.tz/", "success", 0, 0),
    ("cacla", "Cacla Engineering", "https://www.cacla.co.tz/", "success", 0, 0),
    ("calfoniahills", "Calfonia Hills", "https://calfoniahills.ac.tz/", "success", 0, 0),
    ("camara", "Camara Education", "https://camara.or.tz/", "success", 0, 0),
    ("camartec", "CAMARTEC", "https://www.camartec.go.tz/", "success", 0, 0),
    ("candorventure", "Candor Venture", "https://candorventure.co.tz/", "error", 0, 0),  # timeout
    ("canocity", "Canocity", "https://canocity.co.tz/", "error", 0, 0),  # timeout
    ("canossa", "Canossa High School", "https://canossa.ac.tz/", "success", 0, 0),
    ("capitalcitymarathon", "Capital City Marathon", "https://capitalcitymarathon.co.tz/", "error", 0, 0),  # suspended
    ("capitaltechnologies", "Capital Technologies", "https://www.capitaltechnologies.co.tz/", "success", 0, 0),
    ("caps", "Caps Limited", "http://caps.co.tz/quotation", "error", 0, 0),  # timeout
    ("capuchin", "Capuchin Franciscans", "https://capuchin.or.tz/", "success", 0, 0),
    ("cardiocare", "Cardiocare Tanzania", "https://cardiocare.co.tz/", "success", 0, 0),
    ("caretech", "Caretech IT", "https://caretech.co.tz/", "success", 0, 0),
    ("careworth", "Careworth Limited", "https://careworth.co.tz/", "success", 0, 0),
    ("cargopoint", "Cargo Point", "https://cargopoint.co.tz/", "success", 0, 0),
    ("carhouse", "Carhouse", "https://carhouse.co.tz/", "error", 0, 0),  # timeout
    ("carjunction", "Car Junction", "https://carjunction.co.tz/", "success", 0, 0),
    ("carnivoressafaris", "Carnivores Safaris", "https://carnivoressafaris.co.tz/", "success", 0, 0),
    ("cartrack", "Cartrack Tanzania", "https://cartrack.co.tz/", "success", 0, 0),
    ("casco", "CASCO Construction", "https://casco.co.tz/", "success", 0, 0),
]

def main():
    for slug, name, url, status, tender_count, doc_count in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)

        err_msg = None
        if status == "error":
            err_msg = "Account suspended" if slug == "capitalcitymarathon" else "Site timeout or unreachable"
        last_scrape = {
            "institution": slug,
            "last_scrape": NOW,
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "status": status,
            "error": err_msg,
            "tenders_found": tender_count,
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
            "timestamp": NOW,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": [last_scrape.get("error")] if last_scrape.get("error") else [],
        })
        with open(log_path, "w") as f:
            json.dump(scrape_log, f, indent=2)

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

if __name__ == "__main__":
    main()
