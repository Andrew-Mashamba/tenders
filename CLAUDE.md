# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TENDERS is an automated tender scraping system for Tanzanian financial institutions (banks, SACCOs, microfinance). It uses Cursor Agent CLI as the scraping agent, scheduled via macOS LaunchAgent to run daily at 06:00 AM EAT.

The system scrapes ~73 institution tender pages, downloads documents (PDF, DOC, XLSX, etc.), extracts text, generates structured JSON, and sends email notifications via SMTP (info@zima.co.tz → andrew.s.mashamba@gmail.com).

It includes a **web frontend** (`frontend/` — React 19 + Vite 6) and a **FastAPI backend** (`backend/`) for browsing tenders, tracking applications, managing institutions, viewing opportunities, and controlling the scraper.

## Commands

```bash
# Install/manage the daily scheduled scraper
scripts/install.sh install      # Install LaunchAgent (daily 06:00 AM EAT)
scripts/install.sh uninstall    # Remove LaunchAgent
scripts/install.sh status       # Check if scraper is running
scripts/install.sh run          # Run full scrape immediately
scripts/install.sh test-email   # Verify SMTP configuration

# Scrape all institutions
scripts/scrape_all.sh

# Scrape a single institution
scripts/scrape_single.sh <institution-slug>   # e.g., scripts/scrape_single.sh crdb-bank

# Frontend
cd frontend
./start.sh                      # Start both API (port 8010) and Vite dev server (port 3000)
npm run dev                     # Vite dev server only
npm run build                   # Production build to dist/
npm run api                     # FastAPI backend only
```

## Architecture

**Scraping engine:** There is no traditional code — the scraper is Cursor Agent CLI itself, invoked with `-p --force --trust`. The scraping logic is defined in `scripts/scrape_prompt.md` (the master prompt) and each institution's `README.md` (per-institution config + selectors).

**Key flow:** `LaunchAgent plist → scrape_all.sh → agent CLI → reads each institution README → scrapes/downloads/emails`

### Directory Structure

- **`frontend/`** — React SPA only
  - `src/` — React 19 SPA (Vite 6, Tailwind CSS 4, React Router v7.1, Recharts)
  - `src/pages/` — Dashboard, Tenders, TenderDetail, Applications, Opportunities, Institutions, InstitutionDetail, ScraperControl
  - `src/components/` — Layout, DataTable, StatsCard, StatusBadge
  - `src/lib/api.js` — Centralized API client for all backend calls
  - `start.sh` — Launches backend + Vite dev server
  - Production build output: `frontend/dist/`
- **`backend/`** — FastAPI (`main.py`); reads from `institutions/`, serves REST API + static `frontend/dist/` when present
  - In production, API often on port 8001; dev (`start.sh`) uses 8010 with Vite proxying `/api` to it
- **`institutions/`** — One subdirectory per institution (e.g., `crdb-bank/`, `nmb-bank/`). Each contains:
  - `README.md` — YAML frontmatter config (scraping selectors, URLs, schedule, anti-bot settings, document rules) followed by markdown instructions. This is the primary configuration file for each institution.
  - `tenders/active/`, `tenders/closed/`, `tenders/archive/` — Tender JSON files by lifecycle stage
  - `downloads/{tender_id}/original/` and `downloads/{tender_id}/extracted/` — Raw and text-extracted documents
  - `last_scrape.json`, `scrape_log.json` — Scrape state (gitignored)
- **`institutions/websites.md`** — Master directory of all institution URLs and tender page links
- **`institutions/active_tenders.md`** — Auto-generated global index of all active tenders (do not edit manually)
- **`opportunities/`** — When no tenders are found, the scraper identifies business opportunities (sell/partner/build), collects emails, creates draft outreach emails, and appends leads to `opportunities/leads.json`
- **`config/email.json`** — SMTP credentials (gitignored)
- **`scripts/`** — Shell scripts and the LaunchAgent plist
- **`notifications/pending/` and `sent/`** — Email notification queue (gitignored)
- **`logs/`** — Scrape run logs (auto-cleaned after 30 days)

### Institution README Format

Each institution's `README.md` has YAML frontmatter with:
- `scraping.enabled: true/false` — Whether to scrape this institution
- `website.tender_url` — The URL to scrape
- `scraping.selectors` — CSS selectors for parsing (container, tender_item, title, date, document_link, pagination)
- `scraping.anti_bot` — Rate limiting, JS requirements, captcha info
- `scraping.documents` — File types, download rules, URL patterns, known document paths
- `scraping.schedule` — "daily" or other frequency

### Tender ID Format

`{SLUG}-{YEAR}-{SEQUENCE}` (e.g., `CRDB-2026-003`)

### Error Handling

- `scripts/send_error_email.py` — Fallback email sender if Claude CLI fails (sends last 50 log lines)
- Failed emails are saved to `notifications/pending/` as JSON
- The scraper has a PID file lock (`logs/scraper.pid`) to prevent concurrent runs
- LaunchAgent has a 2-hour timeout and auto-retries on failure

## Document Tools

Python package in `tools/` for PDF, DOCX, and XLSX manipulation. Uses venv at `.venv/`.

```bash
# Activate venv first
source .venv/bin/activate

# PDF
python3 -m tools pdf read <file.pdf>                          # Extract text
python3 -m tools pdf read <file.pdf> --pages 1-3              # Specific pages
python3 -m tools pdf read <file.pdf> --tables                 # Extract tables as JSON
python3 -m tools pdf read <file.pdf> --metadata               # File metadata
python3 -m tools pdf merge f1.pdf f2.pdf -o merged.pdf        # Merge PDFs
python3 -m tools pdf split f.pdf --pages 1,3,5 -o out.pdf     # Extract pages
python3 -m tools pdf forms-read <file.pdf>                    # List form fields
python3 -m tools pdf forms-fill <file.pdf> --data d.json -o filled.pdf
python3 -m tools pdf create --type proposal --data d.json -o proposal.pdf
python3 -m tools pdf create --type letter --data d.json -o letter.pdf

# DOCX
python3 -m tools docx read <file.docx>                        # Extract text
python3 -m tools docx read <file.docx> --format json          # Structured output
python3 -m tools docx create --type proposal --data d.json -o proposal.docx
python3 -m tools docx create --type letter --data d.json -o letter.docx
python3 -m tools docx create --template tpl.docx --data d.json -o out.docx
python3 -m tools docx edit <file.docx> --replace '{"old":"new"}' -o out.docx
python3 -m tools docx to-pdf <file.docx> -o out.pdf

# XLSX
python3 -m tools xlsx read <file.xlsx>                         # Plain text dump
python3 -m tools xlsx read <file.xlsx> --format json           # JSON output
python3 -m tools xlsx create --data d.json -o out.xlsx
python3 -m tools xlsx edit <file.xlsx> --cell A1 --value "X" -o out.xlsx
```

### Python API (for use in scripts)

```python
from tools.pdf.reader import extract_text, extract_tables
from tools.pdf.merger import merge, split
from tools.pdf.forms import read_fields, fill_form
from tools.pdf.creator import create_proposal, create_cover_letter
from tools.docx.reader import extract_text as docx_text
from tools.docx.creator import create_proposal as docx_proposal, create_from_template
from tools.xlsx.reader import extract_data
from tools.xlsx.creator import create_from_data
```

## Frontend

React 19 SPA with a FastAPI backend. Key routes:

| Route | Page | Purpose |
|-------|------|---------|
| `/` | Dashboard | Stats, charts, closing-soon tenders |
| `/tenders` | Tenders | Search, filter, batch prepare/apply |
| `/tenders/:id` | TenderDetail | Documents, contacts, details |
| `/applications` | Applications | Track status with urgency levels |
| `/opportunities` | Opportunities | Business leads & draft emails |
| `/institutions` | Institutions | Institution list & scrape status |
| `/scraper` | ScraperControl | Start/stop scraper, live logs |

**API endpoints** (`/api/*`): stats, tenders, applications (prepare/apply/PDF generation), opportunities, institutions, scraper control, document download/text extraction, notifications.

**Dev setup:** Vite proxies `/api/*` → `http://localhost:8010` during development (`frontend/start.sh`). Dependencies: `npm install` in `frontend/`, `pip install -r backend/requirements.txt` for the API.

## Important Notes

- The project path is referenced as `/Volumes/DATA/PROJECTS/TENDERS` in all scripts and prompts
- Rate limits must be respected per institution (`anti_bot.rate_limit_seconds`)
- Always download documents — metadata-only scraping defeats the purpose
- If a tender page URL changes, update that institution's `README.md` with the new URL
- One institution failure should never stop the entire scrape run

## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update tasks/lessons.md with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests → then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First:** Write plan to tasks/todo.md with checkable items
2. **Verify Plan:** Check in before starting implementation
3. **Track Progress:** Mark items complete as you go
4. **Explain Changes:** High-level summary at each step
5. **Document Results:** Add review section to tasks/todo.md
6. **Capture Lessons:** Update tasks/lessons.md after corrections

## Core Principles

- **Simplicity First:** Make every change as simple as possible. Impact minimal code.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Only touch what's necessary. No side effects with new bugs.
