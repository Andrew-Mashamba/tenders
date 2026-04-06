#!/bin/bash
# =============================================================================
# TENDERS — Scrape a single institution
# Usage: ./scrape_single.sh <institution-slug>
# Example: ./scrape_single.sh crdb-bank
# =============================================================================

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <institution-slug>"
    echo "Example: $0 crdb-bank"
    echo ""
    echo "Available institutions:"
    ls -1d /Volumes/DATA/PROJECTS/TENDERS/institutions/*/ | xargs -I{} basename {}
    exit 1
fi

SLUG="$1"
PROJECT_DIR="/Volumes/DATA/PROJECTS/TENDERS"
INST_DIR="$PROJECT_DIR/institutions/$SLUG"
LOGS_DIR="$PROJECT_DIR/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOGS_DIR/scrape_${SLUG}_${TIMESTAMP}.log"

if [ ! -d "$INST_DIR" ]; then
    echo "ERROR: Institution '$SLUG' not found at $INST_DIR"
    exit 1
fi

if [ ! -f "$INST_DIR/README.md" ]; then
    echo "ERROR: No README.md found for '$SLUG'"
    exit 1
fi

mkdir -p "$LOGS_DIR"

echo "[$(date)] Scraping single institution: $SLUG" | tee -a "$LOG_FILE"

"$(which agent 2>/dev/null || echo /Users/andrewmashamba/.local/bin/agent)" -p --force --trust --model composer-1.5 --workspace "$PROJECT_DIR" \
    "You are a tender scraping agent. Read the README.md at $INST_DIR/README.md and follow ALL instructions in it to:

1. Scrape the tender page for this institution
2. If tenders found: download all linked documents (PDF, DOC, DOCX, XLS, XLSX, ZIP), save tender JSON in $INST_DIR/tenders/active/, save downloads in $INST_DIR/downloads/{tender_id}/original/, extract text to extracted/, generate summary.json
3. If NO tenders or procurements found: read $PROJECT_DIR/zima_solutions_ltd/README.md, study the institution, identify opportunities (sell/partner/build), scrape ALL emails from the site, create a draft outreach email, APPEND a lead to $PROJECT_DIR/opportunities/leads.json, then run: python3 $PROJECT_DIR/scripts/sync_leads_csv.py to update the emails table (opportunities/leads.csv). Lead schema: institution_slug, institution_name, website_url, emails[], opportunity_type, opportunity_description, draft_email_subject, draft_email_body, created_at (ISO), status: pending
4. Update $INST_DIR/last_scrape.json and $INST_DIR/scrape_log.json
5. Update the global index at $PROJECT_DIR/institutions/active_tenders.md (if tenders found)
6. Send email notification using config from $PROJECT_DIR/config/email.json (if tenders found)

Read the README first, then execute. Be thorough — download every document you find, or capture opportunity leads when none exist.
Run ID: run_${SLUG}_${TIMESTAMP}
Project directory: $PROJECT_DIR" \
    2>&1 | tee -a "$LOG_FILE"

echo "[$(date)] Done scraping: $SLUG" | tee -a "$LOG_FILE"
