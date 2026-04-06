#!/usr/bin/env python3
"""Fast batch scrape - 15s timeout, no doc downloads."""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch48"
INSTITUTIONS = [
    "hsh", "hssrf", "hubnet", "huca", "hudhud", "huga", "huheso",
    "humanrights", "humanrightsinstitute", "humor", "hunkydory",
    "hurumahospital", "husseini", "hyperionconsultants", "hypermed",
    "iaa", "iae", "iamorganic", "ibes", "ibmtelecenter", "ibn-tv",
    "ibunjazar", "icare", "ice", "icealion",
]

TENDER_KEYWORDS = re.compile(r"\b(tender|tenders|procurement|rfi|rfp|rfq|eoi|bid|bids|manunuzi)\b", re.I)
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

def load_config(slug):
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return {}
    text = readme.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    try:
        import yaml
        parts = text.split("---", 2)
        return yaml.safe_load(parts[1]) or {}
    except Exception:
        return {}

def get_url(config):
    w = config.get("website") or {}
    return w.get("tender_url") or w.get("homepage") or ""

def fetch(url, timeout=15):
    try:
        r = requests.get(url, headers={"User-Agent": "TendersBot/1.0"}, timeout=timeout)
        return r.text, None
    except Exception as e:
        return None, str(e)

def has_tenders(html):
    if not html:
        return False
    return bool(TENDER_KEYWORDS.search(html))

def update_inst(slug, status, tenders, docs, err=None):
    inst = PROJECT / "institutions" / slug
    inst.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    (inst / "last_scrape.json").write_text(json.dumps({
        "institution": slug, "last_scrape": now, "next_scrape": now,
        "active_tenders_count": tenders, "status": status, "error": err,
    }, indent=2))
    log = inst / "scrape_log.json"
    data = {"runs": []}
    if log.exists():
        try:
            data = json.loads(log.read_text())
        except Exception:
            pass
    data["runs"].insert(0, {
        "run_id": RUN_ID, "timestamp": now, "duration_seconds": 0,
        "status": status, "tenders_found": tenders, "new_tenders": tenders,
        "updated_tenders": 0, "documents_downloaded": docs, "errors": [err] if err else [],
    })
    log.write_text(json.dumps(data, indent=2))

def main():
    for slug in INSTITUTIONS:
        cfg = load_config(slug)
        url = get_url(cfg)
        if not url:
            update_inst(slug, "error", 0, 0, "No URL")
            print(f"RESULT|{slug}|error|0|0")
            continue
        if "facebook" in url:
            update_inst(slug, "skipped", 0, 0, "Facebook")
            print(f"RESULT|{slug}|skipped|0|0")
            continue
        html, err = fetch(url)
        if err:
            update_inst(slug, "error", 0, 0, err[:80])
            print(f"RESULT|{slug}|error|0|0")
            continue
        if has_tenders(html):
            update_inst(slug, "success", 1, 0)
            print(f"RESULT|{slug}|success|1|0")
        else:
            update_inst(slug, "success", 0, 0)
            print(f"RESULT|{slug}|success|0|0")

if __name__ == "__main__":
    main()
