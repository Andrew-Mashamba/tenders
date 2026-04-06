#!/usr/bin/env python3
"""Download documents for tenders in active/ and extract text."""
import json
import ssl
import urllib.request
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")

def fetch_file(url, dest, timeout=30):
    try:
        ctx = ssl.create_default_context()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                dest.write_bytes(r.read())
                return True, None
        except:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                dest.write_bytes(r.read())
                return True, None
    except Exception as e:
        return False, str(e)

def main():
    inst_dir = PROJECT / "institutions"
    for slug in ["untamedsafaris", "urusecondary", "uttamis", "vaniagroup"]:
        active = inst_dir / slug / "tenders" / "active"
        if not active.exists():
            continue
        for jf in active.glob("*.json"):
            data = json.loads(jf.read_text(encoding="utf-8"))
            tid = data.get("tender_id", jf.stem)
            docs = data.get("documents", [])
            if not docs:
                continue
            download_dir = inst_dir / slug / "downloads" / tid / "original"
            extract_dir = inst_dir / slug / "downloads" / tid / "extracted"
            download_dir.mkdir(parents=True, exist_ok=True)
            extract_dir.mkdir(parents=True, exist_ok=True)
            for i, doc in enumerate(docs):
                url = doc.get("url")
                if not url:
                    continue
                fname = url.split("/")[-1].split("?")[0] or f"doc_{i}.pdf"
                dest = download_dir / fname
                if dest.exists():
                    print(f"Skip (exists): {slug}/{tid}/{fname}")
                    continue
                ok, err = fetch_file(url, dest)
                if ok:
                    print(f"Downloaded: {slug}/{tid}/{fname}")
                    # Extract text if PDF
                    if fname.lower().endswith(".pdf") and (PROJECT / ".venv").exists():
                        try:
                            import subprocess
                            out_txt = extract_dir / (fname.rsplit(".", 1)[0] + ".txt")
                            subprocess.run(
                                ["python3", "-m", "tools", "pdf", "read", str(dest)],
                                cwd=PROJECT, capture_output=True, text=True, timeout=60
                            )
                            # tools pdf read outputs to stdout; redirect to file
                            r = subprocess.run(
                                ["python3", "-m", "tools", "pdf", "read", str(dest)],
                                cwd=PROJECT, capture_output=True, text=True, timeout=60
                            )
                            if r.stdout:
                                out_txt.write_text(r.stdout, encoding="utf-8")
                                print(f"  Extracted: {out_txt.name}")
                        except Exception as e:
                            print(f"  Extract failed: {e}")
                else:
                    print(f"Failed: {slug}/{tid}/{fname}: {err}")

if __name__ == "__main__":
    main()
