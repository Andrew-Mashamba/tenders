#!/bin/bash
# =============================================================================
# TENDERS — Daily Tender Scraper
# Phase 1: Agent CLI reads READMEs, fetches pages, downloads docs,
#           identifies real tenders, rejects junk, organizes JSON
# Phase 2: Pure Python organizes expired tenders, updates index, sends email
#
# Usage:
#   ./scrape_all.sh                        # Full run (all institutions)
#   ./scrape_all.sh --batch 100            # First 100 institutions
#   ./scrape_all.sh --workers 3            # 3 parallel agent sessions
#   ./scrape_all.sh --resume               # Resume interrupted run
#   ./scrape_all.sh --post-only            # Just organize + send email
#   AGENT_BATCH=12 ./scrape_all.sh         # 12 institutions per agent call
# =============================================================================

set -uo pipefail

PROJECT_DIR="/Volumes/DATA/PROJECTS/TENDERS"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
LOGS_DIR="$PROJECT_DIR/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
MASTER_LOG="$LOGS_DIR/scrape_master_$(date +%Y%m%d).log"
PID_FILE="$LOGS_DIR/scraper.pid"

# Configuration (override via environment variables)
AGENT_BATCH=${AGENT_BATCH:-8}        # Institutions per agent CLI call
WORKERS=${WORKERS:-1}                 # Parallel agent CLI sessions

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$MASTER_LOG"
}

# Prevent concurrent runs
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "ERROR: Scraper already running (PID $OLD_PID). Exiting."
        exit 1
    fi
    rm -f "$PID_FILE"
fi

echo $$ > "$PID_FILE"
trap 'rm -f "$PID_FILE"' EXIT

mkdir -p "$LOGS_DIR"

# Check Agent CLI
AGENT_BIN=$(which agent 2>/dev/null || echo "/Users/andrewmashamba/.local/bin/agent")
if [ ! -x "$AGENT_BIN" ]; then
    log "ERROR: Agent CLI not found at $AGENT_BIN"
    python3 "$SCRIPTS_DIR/send_error_email.py" "Agent CLI not found" 2>/dev/null || true
    exit 1
fi

log "============================================================"
log "SMART TENDER SCRAPER Starting"
log "Run ID: run_${TIMESTAMP}"
log "Config: agent_batch=$AGENT_BATCH workers=$WORKERS"
log "============================================================"

# Build arguments — pass through any CLI args
EXTRA_ARGS=""
for arg in "$@"; do
    EXTRA_ARGS="$EXTRA_ARGS $arg"
done

# Run the smart scraper
python3 "$SCRIPTS_DIR/smart_scrape.py" \
    --agent-batch "$AGENT_BATCH" \
    --workers "$WORKERS" \
    $EXTRA_ARGS \
    2>&1 | tee -a "$MASTER_LOG"

EXIT_CODE=${PIPESTATUS[0]}

if [ "$EXIT_CODE" -ne 0 ]; then
    log "ERROR: Smart scraper exited with code $EXIT_CODE"
    # Send error email with last 50 lines of log
    python3 "$SCRIPTS_DIR/send_error_email.py" \
        "Smart scraper failed (exit=$EXIT_CODE). Check $MASTER_LOG" 2>/dev/null || true
fi

# Clean up old logs (keep last 30 days)
find "$LOGS_DIR" -name "scrape_*.log" -mtime +30 -delete 2>/dev/null || true
find "$LOGS_DIR/agent_batches" -name "batch_*.log" -mtime +7 -delete 2>/dev/null || true

log ""
log "Scrape run complete (exit=$EXIT_CODE)."
log "Master log: $MASTER_LOG"
