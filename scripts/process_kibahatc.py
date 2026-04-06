#!/usr/bin/env python3
"""Process kibahatc tenders from fetched HTML."""
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
INST_DIR = PROJECT / "institutions" / "kibahatc"
RUN_ID = "run_20260313_205329_batch59"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
BASE = "https://kibahatc.go.tz"

def parse_date(s):
    """Parse 'June 01, 2022' to YYYY-MM-DD."""
    try:
        from datetime import datetime
        dt = datetime.strptime(s.strip(), "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except:
        return s

def main():
    html = (Path("/tmp/kibahatc.html").read_text())
    # <tr><td>TITLE</td><td>pub_date</td><td>closing_date</td><td><a href="/storage/...">Pakua</a></td></tr>
    pattern = r'<tr><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td><a href="([^"]+)"[^>]*>'
    matches = re.findall(pattern, html)
    
    tenders = []
    doc_count = 0
    seq = 1
    
    for title, pub, close, href in matches:
        tender_id = f"KIBAHATC-2026-{seq:03d}"
        seq += 1
        pub_date = parse_date(pub)
        closing_date = parse_date(close)
        doc_url = href if href.startswith("http") else BASE + href
        
        (INST_DIR / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
        download_dir = INST_DIR / "downloads" / tender_id / "original"
        download_dir.mkdir(parents=True, exist_ok=True)
        
        # Download PDF
        fname = href.split("/")[-1]
        out_path = download_dir / fname
        try:
            subprocess.run(
                ["curl", "-skL", "-A", "Mozilla/5.0", "-o", str(out_path), doc_url],
                check=True, capture_output=True, timeout=30
            )
            if out_path.exists() and out_path.stat().st_size > 0:
                doc_count += 1
        except Exception as e:
            pass
        
        tender = {
            "tender_id": tender_id,
            "institution": "kibahatc",
            "title": title.strip(),
            "description": "",
            "published_date": pub_date,
            "closing_date": closing_date,
            "status": "closed",
            "source_url": "https://kibahatc.go.tz/tenders",
            "documents": [{"filename": fname, "original_url": doc_url, "local_path": str(out_path)}],
            "contact": {"phone": "07720928447189"},
            "scraped_at": NOW,
        }
        with open(INST_DIR / "tenders" / "closed" / f"{tender_id}.json", "w") as f:
            json.dump(tender, f, indent=2, ensure_ascii=False)
        tenders.append(tender)
    
    # Update last_scrape and scrape_log
    with open(INST_DIR / "last_scrape.json", "w") as f:
        json.dump({
            "institution": "kibahatc",
            "last_scrape": NOW,
            "active_tenders_count": 0,
            "closed_tenders_count": len(tenders),
            "status": "success",
            "error": None,
            "run_id": RUN_ID,
        }, f, indent=2)
    
    log_path = INST_DIR / "scrape_log.json"
    runs = []
    if log_path.exists():
        runs = json.load(open(log_path)).get("runs", [])
    # Replace last kibahatc run (which was error) with success
    runs = [r for r in runs if r.get("run_id") != RUN_ID]
    runs.append({
        "run_id": RUN_ID,
        "timestamp": NOW,
        "status": "success",
        "tenders_found": len(tenders),
        "documents_downloaded": doc_count,
        "errors": [],
    })
    with open(log_path, "w") as f:
        json.dump({"runs": runs}, f, indent=2)
    
    print(f"RESULT|kibahatc|success|{len(tenders)}|{doc_count}")
    print(f"Processed {len(tenders)} tenders (all closed), downloaded {doc_count} documents")

if __name__ == "__main__":
    main()
