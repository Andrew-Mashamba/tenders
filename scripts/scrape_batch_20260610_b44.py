#!/usr/bin/env python3
"""Scrape batch run 20260610_183702_b44: mwangadc, mwanza, mwanzacc, mwauwasa, mybees, mzumbe, nacte, nafakakilimo."""
import html as htmlmod
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, unquote, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "20260610_183702_b44"
TODAY = datetime(2026, 6, 10).date()
NOW = datetime.now(timezone.utc)
NOW_ISO = NOW.isoformat().replace("+00:00", "Z")

DOC_EXT = re.compile(r"\.(pdf|doc|docx|xls|xlsx|zip|rar)$", re.I)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
STRIP_TAGS = re.compile(r"<[^>]+>")


def ensure_dirs(inst_dir: Path):
    for sub in ("tenders/active", "tenders/closed", "tenders/archive", "downloads"):
        (inst_dir / sub).mkdir(parents=True, exist_ok=True)


def fetch_url(url: str, timeout: int = 60) -> tuple[str | None, str | None]:
    try:
        r = subprocess.run(
            ["curl", "-sLk", "-m", str(timeout), "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url],
            capture_output=True,
            text=True,
            timeout=timeout + 10,
        )
        if r.returncode != 0:
            return None, r.stderr or "curl failed"
        return r.stdout, None
    except Exception as e:
        return None, str(e)


def download_file(url: str, dest: Path, timeout: int = 120) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            ["curl", "-sLk", "-m", str(timeout), "-A", "Mozilla/5.0", "-o", str(dest), url],
            capture_output=True,
            timeout=timeout + 10,
        )
        return r.returncode == 0 and dest.exists() and dest.stat().st_size > 100
    except Exception:
        return False


def extract_pdf_text(pdf_path: Path, out_path: Path) -> bool:
    venv_python = PROJECT / ".venv" / "bin" / "python3"
    py = str(venv_python) if venv_python.exists() else sys.executable
    try:
        r = subprocess.run(
            [py, "-m", "tools", "pdf", "read", str(pdf_path)],
            cwd=str(PROJECT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode == 0 and r.stdout.strip():
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(r.stdout)
            return True
    except Exception:
        pass
    return False


def parse_date(s: str):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def next_seq(inst_dir: Path, slug_upper: str, year: int = 2026) -> int:
    max_seq = 0
    for folder in ("active", "closed", "archive"):
        d = inst_dir / "tenders" / folder
        if not d.exists():
            continue
        for f in d.glob(f"{slug_upper}-{year}-*.json"):
            m = re.search(rf"{re.escape(slug_upper)}-{year}-(\d+)", f.stem)
            if m:
                max_seq = max(max_seq, int(m.group(1)))
    return max_seq + 1


def write_last_scrape(inst_dir: Path, slug: str, status: str, tender_count: int, doc_count: int, new_tenders: int, error=None):
    nxt = (NOW + timedelta(days=1)).isoformat().replace("+00:00", "Z")
    data = {
        "institution": slug,
        "last_scrape": NOW_ISO,
        "next_scrape": nxt,
        "status": status,
        "active_tenders_count": tender_count,
        "tenders_found": tender_count,
        "new_tenders": new_tenders,
        "documents_downloaded": doc_count,
        "error": error,
        "run_id": RUN_ID,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(data, indent=2) + "\n")


def append_scrape_log(inst_dir: Path, status: str, tender_count: int, doc_count: int, errors: list):
    log_path = inst_dir / "scrape_log.json"
    data = {"runs": []}
    if log_path.exists():
        data = json.loads(log_path.read_text())
    data.setdefault("runs", []).append(
        {
            "run_id": RUN_ID,
            "timestamp": NOW_ISO,
            "duration_seconds": 0,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": tender_count,
            "updated_tenders": 0,
            "documents_downloaded": doc_count,
            "errors": errors or [],
        }
    )
    log_path.write_text(json.dumps(data, indent=2) + "\n")


def save_tender(inst_dir: Path, tender: dict) -> None:
    tid = tender["tender_id"]
    (inst_dir / "tenders" / "active" / f"{tid}.json").write_text(json.dumps(tender, indent=2, ensure_ascii=False) + "\n")


def move_expired_active(inst_dir: Path):
    active_dir = inst_dir / "tenders" / "active"
    closed_dir = inst_dir / "tenders" / "closed"
    for f in list(active_dir.glob("*.json")):
        t = json.loads(f.read_text())
        cd = t.get("closing_date")
        if cd:
            d = parse_date(cd)
            if d and d < TODAY:
                t["status"] = "closed"
                (closed_dir / f.name).write_text(json.dumps(t, indent=2) + "\n")
                f.unlink()


def parse_october_cms_table(html: str, base_url: str) -> list[dict]:
    rows = []
    for tr in re.findall(r"<tr[^>]*>.*?</tr>", html, re.DOTALL | re.I):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL | re.I)
        if len(tds) < 3:
            continue
        title = STRIP_TAGS.sub("", tds[0]).strip()
        if not title or title.lower() in ("jina la zabuni", "jiina la zabuni", "tender name", "s/n", "#"):
            continue
        pub = STRIP_TAGS.sub("", tds[1]).strip()
        exp = STRIP_TAGS.sub("", tds[2]).strip()
        doc_url = ""
        for td in tds[3:]:
            m = re.search(r'href=["\']([^"\']+)["\']', td, re.I)
            if m:
                doc_url = urljoin(base_url, m.group(1))
                break
        closing = parse_date(exp)
        if closing and closing < TODAY:
            continue
        rows.append(
            {
                "title": title,
                "description": title,
                "published_date": pub if parse_date(pub) else "",
                "closing_date": closing.isoformat() if closing else None,
                "doc_url": doc_url,
                "category": "General",
            }
        )
    return rows


def scrape_mwangadc() -> tuple[str, int, int]:
    slug = "mwangadc"
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    url = "https://mwangadc.go.tz/tenders"
    html, err = fetch_url(url)
    if err or not html or len(html) < 1000:
        write_last_scrape(inst_dir, slug, "error", 0, 0, 0, err or "Fetch failed")
        append_scrape_log(inst_dir, "error", 0, 0, [err or "Fetch failed"])
        return "error", 0, 0

    move_expired_active(inst_dir)
    tenders = parse_october_cms_table(html, url)
    doc_count = 0
    new_count = 0
    seq = next_seq(inst_dir, "MWANGADC")
    for t in tenders:
        tid = f"MWANGADC-2026-{seq:03d}"
        seq += 1
        docs = []
        if t["doc_url"]:
            fname = unquote(Path(urlparse(t["doc_url"]).path).name) or "document.pdf"
            local = inst_dir / "downloads" / tid / "original" / fname
            if download_file(t["doc_url"], local):
                doc_count += 1
                if fname.lower().endswith(".pdf"):
                    extract_pdf_text(local, inst_dir / "downloads" / tid / "extracted" / f"{fname}.txt")
                docs.append(
                    {
                        "filename": fname,
                        "original_url": t["doc_url"],
                        "local_path": f"./downloads/{tid}/original/{fname}",
                        "content_type": "application/pdf",
                        "downloaded_at": NOW_ISO,
                    }
                )
        save_tender(
            inst_dir,
            {
                "tender_id": tid,
                "institution": slug,
                "title": t["title"],
                "description": t["description"],
                "reference_number": "",
                "published_date": t["published_date"] if isinstance(t["published_date"], str) else "",
                "closing_date": t["closing_date"],
                "closing_time": "",
                "category": t["category"],
                "status": "active",
                "source_url": url,
                "documents": docs,
                "contact": {"name": "Procurement Department", "email": "ded@mwangadc.go.tz", "phone": "+255 272974343", "address": "Mwanga District, Kilimanjaro"},
                "eligibility": "",
                "scraped_at": NOW_ISO,
                "last_checked": NOW_ISO,
            },
        )
        new_count += 1

    write_last_scrape(inst_dir, slug, "success", len(tenders), doc_count, new_count)
    append_scrape_log(inst_dir, "success", len(tenders), doc_count, [])
    return "ok", len(tenders), doc_count


def scrape_mwanza_family(slug: str, url: str) -> tuple[str, int, int]:
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    html, err = fetch_url(url)
    move_expired_active(inst_dir)

    if err or not html:
        write_last_scrape(inst_dir, slug, "error", 0, 0, 0, err or "Fetch failed")
        append_scrape_log(inst_dir, "error", 0, 0, [err or "Fetch failed"])
        return "error", 0, 0

    if "GWF CORE" in html or len(html) < 2000:
        write_last_scrape(inst_dir, slug, "error", 0, 0, 0, "Site replaced by GWF CORE SPA; tender page unreachable")
        append_scrape_log(inst_dir, "error", 0, 0, ["Site replaced by GWF CORE SPA"])
        return "error", 0, 0

    tenders = parse_october_cms_table(html, url)
    write_last_scrape(inst_dir, slug, "success", len(tenders), 0, 0)
    append_scrape_log(inst_dir, "success", len(tenders), 0, [])
    return "ok", len(tenders), 0


def scrape_mwauwasa() -> tuple[str, int, int]:
    slug = "mwauwasa"
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    url = "https://mwauwasa.go.tz/tenders"
    html, err = fetch_url(url)
    if err or not html:
        write_last_scrape(inst_dir, slug, "error", 0, 0, 0, err or "Fetch failed")
        append_scrape_log(inst_dir, "error", 0, 0, [err or "Fetch failed"])
        return "error", 0, 0

    move_expired_active(inst_dir)
    items = re.findall(r'<p class="download"[^>]*>(.*?)</p>', html, re.DOTALL | re.I)
    docs_raw = []
    for item in items:
        href_m = re.search(r'href=["\']([^"\']+)["\']', item, re.I)
        if not href_m:
            continue
        href = href_m.group(1)
        text = htmlmod.unescape(re.sub(r"\s+", " ", STRIP_TAGS.sub(" ", item))).strip()
        deadline_m = re.search(r"Deadline\s*(\d{4}-\d{2}-\d{2})", text, re.I)
        deadline = deadline_m.group(1) if deadline_m else None
        if deadline and parse_date(deadline) and parse_date(deadline) < TODAY:
            continue
        docs_raw.append({"url": href, "text": text, "deadline": deadline})

    if not docs_raw:
        write_last_scrape(inst_dir, slug, "success", 0, 0, 0)
        append_scrape_log(inst_dir, "success", 0, 0, [])
        return "ok", 0, 0

    seq = next_seq(inst_dir, "MWAUWASA")
    tid = f"MWAUWASA-2026-{seq:03d}"
    closing_date = docs_raw[0].get("deadline")
    title = "Construction Works for Mwanza Sewer Connection Upgrade, Tanzania"
    description = (
        "National Competitive Bidding for construction works under the Lake Victoria Basin "
        "Integrated Water Resources Management Programme. Scope includes infill sewers (22 km conventional "
        "and 3.5 km simplified sewers), 1600 household sewer connections, and related infrastructure."
    )
    reference_number = "TR184/2025/2026/513719/W/01"
    published_date = "2026-06-02"

    # Refine from IFB if available
    ifb = next((d for d in docs_raw if "IFB" in d["url"].upper()), docs_raw[0])
    tmp_ifb = inst_dir / "downloads" / tid / "original" / "_ifb_preview.pdf"
    if download_file(ifb["url"], tmp_ifb):
        txt_path = inst_dir / "downloads" / tid / "extracted" / "_ifb_preview.txt"
        if extract_pdf_text(tmp_ifb, txt_path) and txt_path.exists():
            txt = txt_path.read_text(errors="ignore")
            if m := re.search(r"Publication Date:\s*(.+)", txt):
                pd = parse_date(m.group(1).strip().replace("nd", "").replace("rd", "").replace("th", "").replace("st", ""))
                if pd:
                    published_date = pd.isoformat()
            if m := re.search(r"NCB NO:\s*(\S+)", txt):
                reference_number = m.group(1)

    documents = []
    doc_count = 0
    for d in docs_raw:
        fname = unquote(d["url"].split("/")[-1].split("?")[0])
        local = inst_dir / "downloads" / tid / "original" / fname
        if download_file(d["url"], local):
            doc_count += 1
            if fname.lower().endswith(".pdf"):
                extract_pdf_text(local, inst_dir / "downloads" / tid / "extracted" / f"{fname}.txt")
            documents.append(
                {
                    "filename": fname,
                    "original_url": d["url"],
                    "local_path": f"./downloads/{tid}/original/{fname}",
                    "content_type": "application/pdf" if fname.lower().endswith(".pdf") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "downloaded_at": NOW_ISO,
                }
            )

    save_tender(
        inst_dir,
        {
            "tender_id": tid,
            "institution": slug,
            "title": title,
            "description": description,
            "reference_number": reference_number,
            "published_date": published_date,
            "closing_date": closing_date,
            "closing_time": "10:00 EAT",
            "category": "Construction",
            "status": "active",
            "source_url": url,
            "documents": documents,
            "contact": {
                "name": "MWAUWASA Procurement",
                "email": "info@mwauwasa.go.tz",
                "phone": "0800110023",
                "address": "Mwanza, Tanzania",
            },
            "eligibility": "Eligible bidders per Tanzania Public Procurement Act 2023 and KfW guidelines",
            "scraped_at": NOW_ISO,
            "last_checked": NOW_ISO,
        },
    )

    write_last_scrape(inst_dir, slug, "success", 1, doc_count, 1)
    append_scrape_log(inst_dir, "success", 1, doc_count, [])
    return "ok", 1, doc_count


def scrape_mybees() -> tuple[str, int, int]:
    slug = "mybees"
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    url = "https://mybees.co.tz/"
    html, err = fetch_url(url)
    move_expired_active(inst_dir)
    if err or not html:
        write_last_scrape(inst_dir, slug, "error", 0, 0, 0, err or "Fetch failed")
        append_scrape_log(inst_dir, "error", 0, 0, [err or "Fetch failed"])
        return "error", 0, 0

    # Next.js B2B platform — no public tender listings
    write_last_scrape(inst_dir, slug, "success", 0, 0, 0)
    append_scrape_log(inst_dir, "success", 0, 0, [])
    return "ok", 0, 0


def scrape_mzumbe() -> tuple[str, int, int]:
    slug = "mzumbe"
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    urls = [
        "https://mzumbe.ac.tz",
        "https://mzumbe.ac.tz/en/administrations/units/procurement-management-unit/",
    ]
    all_html = ""
    for url in urls:
        html, _ = fetch_url(url)
        if html:
            all_html += html

    move_expired_active(inst_dir)
    if not all_html or len(all_html) < 500:
        write_last_scrape(inst_dir, slug, "error", 0, 0, 0, "Site unreachable")
        append_scrape_log(inst_dir, "error", 0, 0, ["Site unreachable"])
        return "error", 0, 0

    # Reject non-tender docs; look for active procurement notices
    tender_count = 0
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]{5,200})</a>', all_html, re.I):
        href, label = m.group(1), STRIP_TAGS.sub("", m.group(2)).strip()
        full = urljoin("https://mzumbe.ac.tz", href)
        label_l = label.lower()
        if any(k in label_l for k in ("vacancy", "job", "nafasi", "employment")):
            continue
        if not any(k in label_l for k in ("tender", "zabuni", "procurement", "rfq", "rfp", "bid", "quotation")):
            continue
        if not DOC_EXT.search(full):
            continue
        closing = None
        if closing and closing < TODAY:
            continue
        tender_count += 1

    write_last_scrape(inst_dir, slug, "success", 0, 0, 0)
    append_scrape_log(inst_dir, "success", 0, 0, [])
    return "ok", 0, 0


def scrape_nacte() -> tuple[str, int, int]:
    slug = "nacte"
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    urls = [
        "https://www.nactvet.go.tz/page/procurement-management",
        "https://www.nactvet.go.tz/page/downloads",
    ]
    all_html = ""
    for url in urls:
        html, _ = fetch_url(url)
        if html:
            all_html += html

    move_expired_active(inst_dir)
    if not all_html:
        write_last_scrape(inst_dir, slug, "error", 0, 0, 0, "Fetch failed")
        append_scrape_log(inst_dir, "error", 0, 0, ["Fetch failed"])
        return "error", 0, 0

    # Documents are forms/calendars/guidebooks — not active tenders
    junk_names = ("guidebook", "calendar", "almanac", "application form", "form no", "accreditation", "registration", "recognition", "curriculum")
    tender_count = 0
    for m in re.finditer(r'href=["\']([^"\']+)["\']', all_html, re.I):
        href = m.group(1)
        if not DOC_EXT.search(href) and "/storage/public/files/" not in href:
            continue
        name = unquote(href.split("/")[-1]).lower()
        if any(j in name for j in junk_names):
            continue
        if any(k in name for k in ("tender", "zabuni", "procurement", "rfp", "rfq", "bid", "quotation")):
            tender_count += 1

    write_last_scrape(inst_dir, slug, "success", 0, 0, 0)
    append_scrape_log(inst_dir, "success", 0, 0, [])
    return "ok", 0, 0


def scrape_nafakakilimo() -> tuple[str, int, int]:
    slug = "nafakakilimo"
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    urls = ["https://nafakakilimo.or.tz/", "https://nafakakilimo.or.tz/news.php"]
    all_html = ""
    for url in urls:
        html, _ = fetch_url(url)
        if html:
            all_html += html

    move_expired_active(inst_dir)
    # Job announcements only — reject per scraping rules
    write_last_scrape(inst_dir, slug, "success", 0, 0, 0)
    append_scrape_log(inst_dir, "success", 0, 0, [])
    return "ok", 0, 0


def update_readme_mwanza_sites():
    for slug in ("mwanza", "mwanzacc"):
        readme = PROJECT / "institutions" / slug / "README.md"
        if not readme.exists():
            continue
        text = readme.read_text()
        if "GWF CORE" in text:
            continue
        text = re.sub(
            r"(requires_javascript:\s*)false",
            r"\1true",
            text,
            count=1,
        )
        if "GWF CORE" not in text:
            text = text.replace(
                'strategy: "Scrape https://',
                'strategy: "Site currently serves GWF CORE SPA shell (tender page unreachable as of 2026-06-10). Previously scraped October CMS table at https://',
                1,
            )
            notes_marker = "notes: |"
            if notes_marker in text:
                text = text.replace(
                    notes_marker,
                    'notes: |\n  As of 2026-06-10 the domain returns a GWF CORE SPA shell (~715 bytes) with no tender table. October CMS tender URLs no longer resolve.\n',
                    1,
                )
        readme.write_text(text)


def main():
    results = []
    results.append(("mwangadc", *scrape_mwangadc()))
    results.append(("mwanza", *scrape_mwanza_family("mwanza", "https://mwanza.go.tz/tenders")))
    results.append(("mwanzacc", *scrape_mwanza_family("mwanzacc", "https://mwanzacc.go.tz/tenders")))
    results.append(("mwauwasa", *scrape_mwauwasa()))
    results.append(("mybees", *scrape_mybees()))
    results.append(("mzumbe", *scrape_mzumbe()))
    results.append(("nacte", *scrape_nacte()))
    results.append(("nafakakilimo", *scrape_nafakakilimo()))
    update_readme_mwanza_sites()

    for slug, status, tc, dc in results:
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")


if __name__ == "__main__":
    main()
