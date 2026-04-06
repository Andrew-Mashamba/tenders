#!/usr/bin/env python3
"""Retry the 6 failed institutions from batch80 (gov sites with SSL)."""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch80"

RETRY_CONFIG = [
    ("mvomerodc", "https://mvomerodc.go.tz/manunuzi-na-ugavi", "MVOMERO DISTRICT COUNCIL"),
    ("mwangadc", "https://mwangadc.go.tz/tenders", "Mwanga District Council"),
    ("mwanza", "https://mwanza.go.tz/tenders", "Mwanza Region"),
    ("mwanzacc", "https://mwanzacc.go.tz/tenders", "Mwanza City Council"),
    ("mwauwasa", "https://mwauwasa.go.tz/tenders", "MWAUWASA"),
    ("mwekawildlife", "https://mwekawildlife.ac.tz/", "CAWM Mweka Wildlife"),
]

TENDER_KEYWORDS = re.compile(r"\b(tender|zabuni|procurement|manunuzi|rfp|rfq|rfi|bid|auction|supply)\b", re.I)
DOC_EXT = re.compile(r"\.(pdf|doc|docx|xls|xlsx|zip|rar)$", re.I)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str, timeout: int = 25) -> tuple[str | None, str | None]:
    try:
        r = subprocess.run(
            ["curl", "-sLk", "-m", str(timeout), "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if r.returncode != 0:
            return None, r.stderr or "curl failed"
        return r.stdout, None
    except Exception as e:
        return None, str(e)


def parse_tenders(html: str, base_url: str) -> tuple[list[dict], list[str]]:
    tenders, doc_urls = [], []
    if not html or len(html) < 100:
        return tenders, doc_urls
    if not TENDER_KEYWORDS.search(html):
        return tenders, doc_urls
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
        href = m.group(1).strip()
        if DOC_EXT.search(href):
            full = urljoin(base_url, href)
            if full not in doc_urls:
                doc_urls.append(full)
    if "zabuni" in html.lower() or "tender" in html.lower() or "manunuzi" in html.lower() or "procurement" in html.lower():
        rows = re.findall(r"<tr[^>]*>.*?</tr>", html, re.DOTALL | re.I)
        for row in rows:
            if TENDER_KEYWORDS.search(row):
                cells = re.findall(r"<t[dh][^>]*>([^<]*)</t[dh]>", row, re.I)
                if len(cells) >= 2:
                    title = cells[1].strip() if len(cells) > 1 else cells[0].strip()
                    if len(title) > 5 and "imefungwa" not in title.lower():
                        tenders.append({"title": title, "description": "", "doc_links": []})
        if not tenders and doc_urls:
            tenders.append({"title": "Tender Documents", "description": "", "doc_links": doc_urls})
    return tenders, doc_urls


def save_tenders_and_download(inst_dir: Path, slug: str, tenders: list, doc_urls: list, source_url: str) -> int:
    doc_count = 0
    year = datetime.now().year
    for i, t in enumerate(tenders[:20], 1):
        tid = f"{slug.upper().replace('-', '')[:8]}-{year}-{i:03d}"
        tender_json = {
            "tender_id": tid,
            "institution": slug,
            "title": t.get("title", "Untitled"),
            "description": t.get("description", ""),
            "published_date": "",
            "closing_date": "",
            "status": "active",
            "source_url": source_url,
            "documents": [],
            "contact": {},
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        with open(inst_dir / "tenders" / "active" / f"{tid}.json", "w") as f:
            json.dump(tender_json, f, indent=2)
        download_dir = inst_dir / "downloads" / tid / "original"
        download_dir.mkdir(parents=True, exist_ok=True)
        for doc_url in doc_urls[:10]:
            try:
                fname = Path(urlparse(doc_url).path).name or "document.pdf"
                out = download_dir / fname
                subprocess.run(["curl", "-sLk", "-m", "30", "-o", str(out), doc_url], capture_output=True, timeout=35)
                if out.exists() and out.stat().st_size > 0:
                    doc_count += 1
            except Exception:
                pass
    return doc_count


def main():
    for slug, url, name in RETRY_CONFIG:
        inst_dir = PROJECT / "institutions" / slug
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)

        html, err = fetch_url(url)
        if err or not html:
            print(f"RESULT|{slug}|error|0|0  # {err or 'Fetch failed'}")
            continue

        tenders, doc_urls = parse_tenders(html, url)
        tender_count = len(tenders)
        doc_count = save_tenders_and_download(inst_dir, slug, tenders, doc_urls, url) if tender_count > 0 else 0

        data = {"institution": slug, "last_scrape": datetime.now(timezone.utc).isoformat(), "active_tenders_count": tender_count, "status": "success", "error": None}
        with open(inst_dir / "last_scrape.json", "w") as f:
            json.dump(data, f, indent=2)

        log_path = inst_dir / "scrape_log.json"
        data = {"runs": []}
        if log_path.exists():
            with open(log_path) as f:
                data = json.load(f)
        data["runs"] = data.get("runs", []) + [{"run_id": RUN_ID, "timestamp": datetime.now(timezone.utc).isoformat(), "status": "success", "tenders_found": tender_count, "documents_downloaded": doc_count}]
        with open(log_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"RESULT|{slug}|success|{tender_count}|{doc_count}")


if __name__ == "__main__":
    main()
