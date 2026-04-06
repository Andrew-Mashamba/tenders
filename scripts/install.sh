#!/bin/bash
# =============================================================================
# Install/Uninstall the TENDERS daily scraper
# Usage:
#   ./install.sh install    — Install and start the daily job
#   ./install.sh uninstall  — Stop and remove the daily job
#   ./install.sh status     — Check if the job is loaded
#   ./install.sh run        — Run the scraper immediately (manual trigger)
#   ./install.sh test-email — Send a test email to verify SMTP config
# =============================================================================

set -euo pipefail

PLIST_NAME="com.tenders.scraper"
PLIST_SRC="/Volumes/DATA/PROJECTS/TENDERS/scripts/${PLIST_NAME}.plist"
PLIST_DST="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
SCRIPTS_DIR="/Volumes/DATA/PROJECTS/TENDERS/scripts"

case "${1:-help}" in

install)
    echo "Installing TENDERS daily scraper..."

    # Make scripts executable
    chmod +x "$SCRIPTS_DIR/scrape_all.sh"
    chmod +x "$SCRIPTS_DIR/scrape_single.sh"
    chmod +x "$SCRIPTS_DIR/send_error_email.py"

    # Copy plist to LaunchAgents
    cp "$PLIST_SRC" "$PLIST_DST"

    # Unload first if already loaded
    launchctl unload "$PLIST_DST" 2>/dev/null || true

    # Load the job
    launchctl load "$PLIST_DST"

    echo ""
    echo "Installed successfully!"
    echo "  Schedule: Daily at 06:00 AM (EAT)"
    echo "  Plist:    $PLIST_DST"
    echo "  Script:   $SCRIPTS_DIR/scrape_all.sh"
    echo "  Logs:     /Volumes/DATA/PROJECTS/TENDERS/logs/"
    echo ""
    echo "To run immediately:  $0 run"
    echo "To check status:     $0 status"
    echo "To uninstall:        $0 uninstall"
    ;;

uninstall)
    echo "Uninstalling TENDERS daily scraper..."
    launchctl unload "$PLIST_DST" 2>/dev/null || true
    rm -f "$PLIST_DST"
    echo "Uninstalled."
    ;;

status)
    echo "=== LaunchAgent Status ==="
    if launchctl list | grep -q "$PLIST_NAME"; then
        launchctl list | grep "$PLIST_NAME"
        echo "Status: LOADED (active)"
    else
        echo "Status: NOT LOADED"
    fi
    echo ""

    echo "=== Last Run ==="
    LATEST_LOG=$(ls -t /Volumes/DATA/PROJECTS/TENDERS/logs/scrape_2*.log 2>/dev/null | head -1)
    if [ -n "$LATEST_LOG" ]; then
        echo "Log: $LATEST_LOG"
        echo "Size: $(wc -c < "$LATEST_LOG") bytes"
        echo "Last lines:"
        tail -5 "$LATEST_LOG"
    else
        echo "No scrape logs found yet."
    fi
    echo ""

    echo "=== PID File ==="
    PID_FILE="/Volumes/DATA/PROJECTS/TENDERS/logs/scraper.pid"
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Scraper is RUNNING (PID $PID)"
        else
            echo "Stale PID file (process not running)"
        fi
    else
        echo "Not currently running."
    fi
    ;;

run)
    echo "Running scraper manually..."
    bash "$SCRIPTS_DIR/scrape_all.sh"
    ;;

test-email)
    echo "Sending test email..."
    python3 -c "
import json, smtplib, ssl
from email.mime.text import MIMEText
from datetime import datetime

with open('/Volumes/DATA/PROJECTS/TENDERS/config/email.json') as f:
    config = json.load(f)

msg = MIMEText('''
TENDERS — Test Email
========================================
This is a test email from the TENDERS scraper.
If you received this, the email configuration is working correctly.

Time: ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''
SMTP Host: ''' + config['smtp_host'] + '''
From: ''' + config['from'] + '''

No action needed.
''')

msg['From'] = config['from']
msg['To'] = config['to']
msg['Subject'] = '[TENDERS] Test Email - ' + datetime.now().strftime('%Y-%m-%d %H:%M')

context = ssl.create_default_context()
with smtplib.SMTP_SSL(config['smtp_host'], config['smtp_port'], context=context) as server:
    server.login(config['smtp_user'], config['smtp_password'])
    server.send_message(msg)
    print('Test email sent successfully to ' + config['to'])
"
    ;;

help|*)
    echo "TENDERS Scraper Installer"
    echo ""
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  install      Install and start the daily scraper (06:00 AM EAT)"
    echo "  uninstall    Stop and remove the daily scraper"
    echo "  status       Check if the scraper is installed and running"
    echo "  run          Run the scraper immediately"
    echo "  test-email   Send a test email to verify SMTP configuration"
    echo ""
    ;;
esac
