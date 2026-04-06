#!/usr/bin/env python3
"""
Smart Tender Scraper
====================
Phase 1 (Agent CLI — intelligent fetch + analyze):
  - Agent reads each institution's README.md for config
  - Fetches tender pages, adapts to HTML changes intelligently
  - Downloads all documents (PDF, DOC, etc.)
  - Extracts text, identifies REAL tenders, rejects junk
  - Creates structured JSON in tenders/active/
  - Captures opportunity leads when no tenders found
  - Updates last_scrape.json per institution

Phase 2 (Pure Python — organize + notify):
  - Move expired tenders to closed/archive
  - Update global active_tenders.md
  - Send email notification

Usage:
  python3 smart_scrape.py                       # Full run (all institutions)
  python3 smart_scrape.py --slug crdb-bank      # Single institution
  python3 smart_scrape.py --start 0 --batch 50  # Range of institutions
  python3 smart_scrape.py --workers 3           # 3 parallel agent sessions
  python3 smart_scrape.py --agent-batch 8       # 8 institutions per agent call
  python3 smart_scrape.py --post-only           # Phase 2 only (organize + notify)
  python3 smart_scrape.py --resume              # Resume from last state
"""

import os
import re
import json
import sys
import time
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── Config ───────────────────────────────────────────────────────────────────

BASE_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS")
INSTITUTIONS_DIR = BASE_DIR / "institutions"
LOGS_DIR = BASE_DIR / "logs"
STATE_FILE = BASE_DIR / "scripts" / ".smart_scrape_state.json"
AGENT_BIN = "/Users/andrewmashamba/.local/bin/agent"
AGENT_LOG_DIR = BASE_DIR / "logs" / "agent_batches"


# ─── README Parser ────────────────────────────────────────────────────────────

def parse_readme(slug: str) -> dict | None:
    """Parse institution README.md — check if scraping is enabled."""
    readme = INSTITUTIONS_DIR / slug / "README.md"
    if not readme.exists():
        return None

    try:
        content = readme.read_text(errors='ignore')[:4096]
    except Exception:
        return None

    # Check enabled
    m = re.search(r'scraping:\s*\n\s*enabled:\s*(true|false)', content)
    if m and m.group(1).lower() == 'false':
        return None

    # Extract basic info for progress tracking
    name_m = re.search(r'name:\s*["\']([^"\']+)', content)
    cat_m = re.search(r'category:\s*["\']([^"\']+)', content)
    url_m = re.search(r'tender_url:\s*["\']([^"\']+)', content)

    return {
        'slug': slug,
        'name': name_m.group(1) if name_m else slug,
        'category': cat_m.group(1) if cat_m else 'Unknown',
        'tender_url': url_m.group(1) if url_m else '',
        'readme': str(readme),
        'folder': str(INSTITUTIONS_DIR / slug),
    }


def get_enabled_institutions() -> list[dict]:
    """Get all institutions with scraping enabled, sorted by category."""
    configs = []
    for d in sorted(os.listdir(INSTITUTIONS_DIR)):
        if not (INSTITUTIONS_DIR / d).is_dir():
            continue
        config = parse_readme(d)
        if config:
            configs.append(config)
    return configs


# ─── Phase 1: Agent CLI Scrape ───────────────────────────────────────────────

def build_scrape_prompt(batch_configs: list[dict], run_id: str) -> str:
    """Build comprehensive Agent CLI prompt for fetching + analyzing."""
    today = date.today().isoformat()

    inst_list = '\n'.join(
        f"  - {c['slug']} (README: {c['readme']})"
        for c in batch_configs
    )

    prompt = f"""You are an intelligent tender scraping agent. Your job is to scrape real tenders
from institution websites, download documents, and organize everything properly.

TODAY'S DATE: {today}

For EACH institution listed below, follow these steps IN ORDER:

## Step 1: Read the README
Read the institution's README.md to understand:
- The tender_url to scrape
- CSS selectors for parsing (use as hints, adapt if HTML differs)
- Document download paths and patterns
- Strategy notes and special handling instructions

## Step 2: Fetch the Tender Page
- Use curl or WebFetch to get the page HTML
- If the page requires JavaScript, note it and try anyway
- Respect rate limits from the README
- If the tender_url fails, try the homepage and look for tender/procurement links

## Step 3: Analyze the Page Content
Read the HTML content intelligently. Look for:
- Tender titles, reference numbers, descriptions
- Closing dates, published dates
- Document download links (PDF, DOC, DOCX, XLS, XLSX, ZIP)
- Contact information (email, phone, address)
- Category of tender (ICT, Construction, Supply, Consultancy, etc.)

## Step 4: REJECT JUNK — This is critical
DO NOT create tender records for:
- ❌ Job postings / employment vacancies (nafasi za kazi, vacancies, careers)
- ❌ News articles / press releases / blog posts
- ❌ General website content / About Us / FAQ
- ❌ EXPIRED tenders (closing date before {today})
- ❌ Auction/liquidation notices (unless procurement-related)
- ❌ Scraped CSS/JavaScript code
- ❌ Social media content
- ❌ Generic placeholder text

ONLY create records for REAL, CURRENT tenders:
- ✅ Procurement notices, RFPs, RFQs
- ✅ Expressions of Interest (EOI)
- ✅ Prequalification / supplier registration (if currently open)
- ✅ Zabuni, manunuzi, tangazo la zabuni (Swahili tender terms)
- ✅ Supply/delivery/construction/consultancy contracts
- ✅ Tenders with no closing date (assume active)

## Step 5: Download Documents
For each real tender found:
1. Create directory: {{inst_dir}}/downloads/{{tender_id}}/original/
2. Download ALL linked PDF/DOC/DOCX/XLS/XLSX/ZIP files
3. Follow download links, resolve redirects
4. Save with readable filenames (decode percent-encoding)
5. Extract text from PDFs → save to downloads/{{tender_id}}/extracted/{{filename}}.txt

## Step 6: Create Tender JSON
Save to {{inst_dir}}/tenders/active/{{tender_id}}.json:
```json
{{{{
  "tender_id": "{{SLUG_UPPER}}-{{YEAR}}-{{SEQ}}",
  "institution": "{{slug}}",
  "title": "Full tender title (translate Swahili to English if needed)",
  "description": "Scope of work / what is being procured",
  "reference_number": "Official reference number if found",
  "published_date": "YYYY-MM-DD or empty",
  "closing_date": "YYYY-MM-DD or null if unknown",
  "closing_time": "HH:MM EAT or empty",
  "category": "ICT/Construction/Supply/Consultancy/General",
  "status": "active",
  "source_url": "URL where this was found",
  "documents": [
    {{{{
      "filename": "document.pdf",
      "original_url": "https://...",
      "local_path": "./downloads/TENDER-ID/original/document.pdf",
      "content_type": "application/pdf",
      "downloaded_at": "{datetime.now().isoformat()}Z"
    }}}}
  ],
  "contact": {{{{
    "name": "Procurement Department",
    "email": "email from page",
    "phone": "phone from page",
    "address": "address from page"
  }}}},
  "eligibility": "Requirements if stated",
  "scraped_at": "{datetime.now().isoformat()}Z",
  "last_checked": "{datetime.now().isoformat()}Z"
}}}}
```

IMPORTANT for tender_id:
- Format: {{SLUG_UPPER}}-{{YEAR}}-{{SEQUENCE}} (e.g., CRDB-2026-003)
- Check existing files in tenders/active/ to get the right sequence number
- Don't duplicate existing tenders (compare by title + source_url)

## Step 7: Update Scrape State
Write {{inst_dir}}/last_scrape.json:
```json
{{{{
  "institution": "{{slug}}",
  "last_scrape": "{datetime.now().isoformat()}Z",
  "next_scrape": "{(datetime.now() + timedelta(days=1)).isoformat()}Z",
  "status": "success|error",
  "active_tenders_count": N,
  "tenders_found": N,
  "new_tenders": N,
  "documents_downloaded": N,
  "error": null
}}}}
```

## Step 8: Opportunity Leads (when NO tenders found)
If an institution has no real tenders:
1. Read {BASE_DIR}/zima_solutions_ltd/README.md to understand Zima Solutions
2. Study the institution — what they do, their sector
3. Scrape ALL emails from the page
4. Identify opportunities: sell (Zima product), partner, or build (custom solution)
5. Append a lead to {BASE_DIR}/opportunities/leads.json:
   ```json
   {{{{
     "institution_slug": "...",
     "institution_name": "...",
     "website_url": "...",
     "emails": ["..."],
     "opportunity_type": "sell|partner|build",
     "opportunity_description": "Why Zima fits...",
     "draft_email_subject": "...",
     "draft_email_body": "...",
     "created_at": "{datetime.now().isoformat()}Z",
     "status": "pending"
   }}}}
   ```
   Read existing leads.json first, parse as JSON array, append, write back.

## Step 9: Update README if needed
After scraping, compare what you found with the README config. If ANY of these differ, UPDATE the README.md:
- **tender_url changed** — site restructured, new tender page URL
- **CSS selectors wrong** — the actual HTML uses different selectors than listed
- **known_document_paths changed** — documents are stored at a different path
- **institution.name wrong** — the README has a placeholder or incorrect name
- **requires_javascript** — site is now an SPA or vice versa
- **scraping.enabled should be false** — site is permanently down, parked, or has no procurement section at all
- **strategy needs update** — the approach described no longer matches reality
- **New document URL patterns** discovered

Keep the full README structure intact. Only update the fields that need changing.

## Step 10: Print Result
For EACH institution, print exactly:
RESULT|{{slug}}|{{ok_or_error}}|{{tender_count}}|{{doc_count}}

CRITICAL RULES:
- Process ALL {len(batch_configs)} institutions. Do NOT stop early.
- If a site is down, log the error and move to the next one.
- Only create records for REAL, CURRENT tenders.
- If tender text is in Swahili, translate key fields to English.
- Download EVERY document — metadata-only scraping is useless.
- One institution failure must NOT stop the entire batch.
- Clean up any INVALID existing tender JSONs (junk, expired, duplicates) — move to closed/ or delete.

Project directory: {BASE_DIR}
Run ID: {run_id}

=================================================================
INSTITUTIONS TO SCRAPE ({len(batch_configs)}):
=================================================================
{inst_list}
"""
    return prompt


def run_scrape_batch(batch_configs: list[dict], batch_num: int,
                     total_batches: int, run_id: str) -> dict:
    """Run Agent CLI on a batch of institutions."""
    slugs = [c['slug'] for c in batch_configs]
    batch_label = f"Batch {batch_num}/{total_batches}"

    print(f"\n  [{batch_label}] {', '.join(slugs[:4])}"
          f"{'...' if len(slugs) > 4 else ''} ({len(slugs)} institutions)")

    prompt = build_scrape_prompt(batch_configs, f"{run_id}_b{batch_num}")

    AGENT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = AGENT_LOG_DIR / f"batch_{batch_num}_{run_id}.log"

    cmd = [
        AGENT_BIN, '-p', '--force', '--trust',
        '--model', 'composer-1.5',
        '--workspace', str(BASE_DIR),
        prompt
    ]

    t0 = time.time()
    result_data = {
        'batch_num': batch_num,
        'slugs': slugs,
        'status': 'pending',
        'results': {},
        'elapsed': 0,
        'tenders_found': 0,
        'docs_downloaded': 0,
    }

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=180 * len(batch_configs)  # ~3 min per institution
        )

        # Save agent log
        with open(log_file, 'w') as f:
            f.write(result.stdout or '')
            if result.stderr:
                f.write(f"\n\n=== STDERR ===\n{result.stderr[-2000:]}")

        # Parse RESULT lines
        if result.stdout:
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line.startswith('RESULT|'):
                    parts = line.split('|')
                    if len(parts) >= 4:
                        slug = parts[1]
                        status = parts[2]
                        tenders = int(parts[3]) if parts[3].isdigit() else 0
                        docs = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0
                        result_data['results'][slug] = {
                            'status': status,
                            'tenders': tenders,
                            'docs': docs,
                        }
                        result_data['tenders_found'] += tenders
                        result_data['docs_downloaded'] += docs

        result_data['status'] = 'ok' if result.returncode == 0 else 'error'

    except subprocess.TimeoutExpired:
        result_data['status'] = 'timeout'
        with open(log_file, 'w') as f:
            f.write(f"TIMEOUT after {180 * len(batch_configs)}s\n")

    except Exception as e:
        result_data['status'] = 'error'
        with open(log_file, 'w') as f:
            f.write(f"ERROR: {e}\n")

    elapsed = time.time() - t0
    result_data['elapsed'] = round(elapsed, 1)

    # Report
    ok = sum(1 for r in result_data['results'].values() if r['status'] in ('ok', 'success'))
    tenders = result_data['tenders_found']
    docs = result_data['docs_downloaded']
    status_icon = '✓' if result_data['status'] == 'ok' else '✗'

    print(f"  [{batch_label}] {status_icon} {ok}/{len(slugs)} processed | "
          f"{tenders} tenders | {docs} docs | {elapsed:.0f}s")

    return result_data


def phase1_scrape(configs: list[dict], agent_batch_size: int = 8,
                  workers: int = 1) -> dict:
    """Phase 1: Agent CLI scrapes all institutions."""
    run_id = datetime.now().strftime('%Y%m%d_%H%M%S')

    print(f"\n{'='*70}")
    print(f"PHASE 1: AI Scrape — {len(configs)} institutions")
    print(f"  Agent batch size: {agent_batch_size}")
    print(f"  Parallel workers: {workers}")
    print(f"  Run ID: {run_id}")
    print(f"{'='*70}")

    # Split into batches
    batches = []
    for i in range(0, len(configs), agent_batch_size):
        batches.append(configs[i:i + agent_batch_size])

    total_batches = len(batches)
    stats = {
        'run_id': run_id,
        'total_institutions': len(configs),
        'total_batches': total_batches,
        'completed_batches': 0,
        'failed_batches': 0,
        'tenders_found': 0,
        'docs_downloaded': 0,
        'institutions_processed': 0,
        'institution_results': {},
        'elapsed': 0,
    }

    t0 = time.time()

    if workers <= 1:
        # Sequential processing
        for i, batch in enumerate(batches):
            batch_num = i + 1
            result = run_scrape_batch(batch, batch_num, total_batches, run_id)

            stats['completed_batches'] += 1
            if result['status'] == 'ok':
                stats['tenders_found'] += result['tenders_found']
                stats['docs_downloaded'] += result['docs_downloaded']
                stats['institutions_processed'] += len(result['results'])
                stats['institution_results'].update(result['results'])
            else:
                stats['failed_batches'] += 1

            # Save progress state
            stats['elapsed'] = round(time.time() - t0, 1)
            save_state({
                'date': date.today().isoformat(),
                'run_id': run_id,
                'completed_slugs': list(stats['institution_results'].keys()),
                'stats': stats,
            })
    else:
        # Parallel agent sessions
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {}
            for i, batch in enumerate(batches):
                batch_num = i + 1
                future = executor.submit(
                    run_scrape_batch, batch, batch_num, total_batches, run_id
                )
                futures[future] = batch_num

            for future in as_completed(futures):
                batch_num = futures[future]
                try:
                    result = future.result()
                    stats['completed_batches'] += 1
                    if result['status'] == 'ok':
                        stats['tenders_found'] += result['tenders_found']
                        stats['docs_downloaded'] += result['docs_downloaded']
                        stats['institutions_processed'] += len(result['results'])
                        stats['institution_results'].update(result['results'])
                    else:
                        stats['failed_batches'] += 1
                except Exception as e:
                    print(f"  [Batch {batch_num}] ✗ Exception: {e}")
                    stats['failed_batches'] += 1

                # Save progress
                stats['elapsed'] = round(time.time() - t0, 1)
                save_state({
                    'date': date.today().isoformat(),
                    'run_id': run_id,
                    'completed_slugs': list(stats['institution_results'].keys()),
                    'stats': stats,
                })

    stats['elapsed'] = round(time.time() - t0, 1)

    print(f"\n  Phase 1 complete in {stats['elapsed']:.0f}s")
    print(f"  Institutions processed: {stats['institutions_processed']}/{len(configs)}")
    print(f"  Tenders found: {stats['tenders_found']}")
    print(f"  Documents downloaded: {stats['docs_downloaded']}")
    print(f"  Failed batches: {stats['failed_batches']}")

    return stats


# ─── Phase 2: Post-scrape Organization ──────────────────────────────────────

def phase2_post_scrape():
    """Phase 2: Organize tenders, update index, send email."""
    print(f"\n{'='*70}")
    print("PHASE 2: Post-scrape organization")
    print(f"{'='*70}")

    today = date.today()
    moved_closed = 0
    moved_archive = 0
    active_count = 0

    # Move expired tenders
    for inst_dir in INSTITUTIONS_DIR.iterdir():
        if not inst_dir.is_dir():
            continue

        active_dir = inst_dir / "tenders" / "active"
        closed_dir = inst_dir / "tenders" / "closed"
        archive_dir = inst_dir / "tenders" / "archive"

        if not active_dir.exists():
            continue

        for jf in active_dir.glob("*.json"):
            try:
                data = json.loads(jf.read_text())
                closing = data.get('closing_date')
                if not closing:
                    active_count += 1
                    continue

                try:
                    close_date = datetime.strptime(str(closing)[:10], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    active_count += 1
                    continue

                if close_date < today:
                    if (today - close_date).days > 90:
                        archive_dir.mkdir(parents=True, exist_ok=True)
                        data['status'] = 'archived'
                        jf.write_text(json.dumps(data, indent=2))
                        shutil.move(str(jf), str(archive_dir / jf.name))
                        moved_archive += 1
                    else:
                        closed_dir.mkdir(parents=True, exist_ok=True)
                        data['status'] = 'closed'
                        jf.write_text(json.dumps(data, indent=2))
                        shutil.move(str(jf), str(closed_dir / jf.name))
                        moved_closed += 1
                else:
                    active_count += 1
            except Exception:
                active_count += 1
                continue

    print(f"  Active tenders: {active_count}")
    print(f"  Moved to closed: {moved_closed}")
    print(f"  Moved to archive: {moved_archive}")

    # Run post_scrape.py for global index + email
    print("  Updating global index + sending email...")
    try:
        result = subprocess.run([
            sys.executable, str(BASE_DIR / "scripts" / "post_scrape.py"),
            '--scraped', str(active_count + moved_closed),
            '--errors', '0',
            '--tenders', str(active_count),
        ], timeout=60, capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✓ Global index updated + email sent")
        else:
            print(f"  ✗ post_scrape.py failed: {result.stderr[:200]}")
    except Exception as e:
        print(f"  ✗ post_scrape.py error: {e}")

    # Sync leads CSV
    try:
        subprocess.run([
            sys.executable, str(BASE_DIR / "scripts" / "sync_leads_csv.py")
        ], timeout=30, capture_output=True)
        print("  ✓ Leads CSV synced")
    except Exception:
        pass

    return {
        'active': active_count,
        'closed': moved_closed,
        'archived': moved_archive,
    }


# ─── State Management ────────────────────────────────────────────────────────

def load_state() -> dict:
    """Load scrape state for resume support."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {'date': '', 'completed_slugs': [], 'stats': {}}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, default=str))


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Smart Tender Scraper — Agent CLI + Post-processing')
    parser.add_argument('--slug', type=str, help='Scrape single institution')
    parser.add_argument('--start', type=int, default=0, help='Start offset')
    parser.add_argument('--batch', type=int, default=0, help='Total institutions (0=all)')
    parser.add_argument('--agent-batch', type=int, default=8,
                        help='Institutions per agent CLI call (default 8)')
    parser.add_argument('--workers', type=int, default=1,
                        help='Parallel agent CLI sessions (default 1)')
    parser.add_argument('--post-only', action='store_true',
                        help='Phase 2 only: organize + notify')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from last state (skip completed institutions)')
    parser.add_argument('--skip-scraped', action='store_true',
                        help='Skip institutions that already have active tenders or are in the tracker')
    args = parser.parse_args()

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    AGENT_LOG_DIR.mkdir(parents=True, exist_ok=True)

    t_start = time.time()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    print(f"\n{'#'*70}")
    print(f"  SMART TENDER SCRAPER — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Run ID: run_{timestamp}")
    print(f"{'#'*70}")

    # Phase 2 only shortcut
    if args.post_only:
        phase2_post_scrape()
        return

    # Check Agent CLI
    if not os.path.isfile(AGENT_BIN):
        print(f"  ERROR: Agent CLI not found at {AGENT_BIN}")
        sys.exit(1)

    # Load institution configs
    if args.slug:
        configs = [c for c in [parse_readme(args.slug)] if c]
        if not configs:
            print(f"  ERROR: Institution '{args.slug}' not found or disabled")
            sys.exit(1)
    else:
        configs = get_enabled_institutions()

    total = len(configs)

    # Apply offset/limit
    configs = configs[args.start:]
    if args.batch:
        configs = configs[:args.batch]

    # Skip institutions that already have tenders pulled
    if args.skip_scraped:
        already_done = set()

        # Institutions with active tenders in folders
        for d in os.listdir(INSTITUTIONS_DIR):
            active_dir = INSTITUTIONS_DIR / d / "tenders" / "active"
            if active_dir.is_dir() and any(active_dir.glob("*.json")):
                already_done.add(d)

        # Institutions in requirements database
        req_db = BASE_DIR / "applications" / "requirements_database.json"
        if req_db.exists():
            try:
                for r in json.loads(req_db.read_text()):
                    s = r.get('institution_slug', '')
                    if s:
                        already_done.add(s)
            except Exception:
                pass

        # Institutions scraped today
        today_str = date.today().isoformat()
        for d in os.listdir(INSTITUTIONS_DIR):
            ls = INSTITUTIONS_DIR / d / "last_scrape.json"
            if ls.exists():
                try:
                    data = json.loads(ls.read_text())
                    if data.get('last_scrape', '')[:10] == today_str:
                        already_done.add(d)
                except Exception:
                    pass

        before = len(configs)
        configs = [c for c in configs if c['slug'] not in already_done]
        skipped = before - len(configs)
        if skipped:
            print(f"  Skipping {skipped} already-scraped institutions ({len(configs)} remaining)")

    # Resume support — skip already-completed institutions
    if args.resume:
        state = load_state()
        if state.get('date') == date.today().isoformat():
            completed = set(state.get('completed_slugs', []))
            before = len(configs)
            configs = [c for c in configs if c['slug'] not in completed]
            skipped = before - len(configs)
            if skipped:
                print(f"  Resuming: skipping {skipped} already-completed institutions")
        else:
            print("  No same-day state to resume from. Starting fresh.")

    print(f"\n  Enabled institutions: {len(configs)} (of {total} total)")

    if not configs:
        print("  No institutions to scrape.")
        phase2_post_scrape()
        return

    # Show plan
    categories = {}
    for c in configs:
        cat = c.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
    top_cats = sorted(categories.items(), key=lambda x: -x[1])[:5]
    print(f"  Categories: {', '.join(f'{cat}={n}' for cat, n in top_cats)}")
    print(f"  Agent batch size: {args.agent_batch}")
    print(f"  Workers: {args.workers}")
    print(f"  Estimated batches: {(len(configs) + args.agent_batch - 1) // args.agent_batch}")

    # Phase 1: Agent CLI scrape
    scrape_stats = phase1_scrape(configs, args.agent_batch, args.workers)

    # Phase 2: Post-scrape organization
    post_stats = phase2_post_scrape()

    # Final report
    elapsed = time.time() - t_start
    print(f"\n{'#'*70}")
    print(f"  SCRAPE COMPLETE — {elapsed:.0f}s total ({elapsed/60:.1f} min)")
    print(f"  Institutions scraped: {scrape_stats.get('institutions_processed', 0)}/{len(configs)}")
    print(f"  Tenders found: {scrape_stats.get('tenders_found', 0)}")
    print(f"  Documents downloaded: {scrape_stats.get('docs_downloaded', 0)}")
    print(f"  Active tenders: {post_stats.get('active', 0)}")
    print(f"  Moved to closed: {post_stats.get('closed', 0)}")
    print(f"  Failed batches: {scrape_stats.get('failed_batches', 0)}")
    print(f"{'#'*70}")

    # Save final state
    save_state({
        'date': date.today().isoformat(),
        'run_id': f"run_{timestamp}",
        'completed_slugs': list(scrape_stats.get('institution_results', {}).keys()),
        'stats': {
            'scrape': scrape_stats,
            'post': post_stats,
            'total_elapsed': round(elapsed, 1),
        },
    })


if __name__ == '__main__':
    main()
