#!/usr/bin/env python3
"""
Fallback error notification — sends email if the main Claude scraper fails.
Usage: python3 send_error_email.py <exit_code> <log_file>
"""

import sys
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS")
CONFIG_FILE = PROJECT_DIR / "config" / "email.json"

def send_error_email(exit_code: int, log_file: str):
    with open(CONFIG_FILE) as f:
        config = json.load(f)

    # Read last 50 lines of log for context
    log_tail = ""
    try:
        with open(log_file) as f:
            lines = f.readlines()
            log_tail = "".join(lines[-50:])
    except Exception:
        log_tail = "(could not read log file)"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    msg = MIMEMultipart()
    msg["From"] = config["from"]
    msg["To"] = config["to"]
    msg["Subject"] = f"[TENDERS] SCRAPER ERROR — Exit code {exit_code} — {now}"

    body = f"""
TENDERS SCRAPER ERROR ALERT
========================================
Time:      {now}
Exit Code: {exit_code}
Log File:  {log_file}

The daily tender scraper has failed. Please investigate.

LAST 50 LINES OF LOG:
----------------------------------------
{log_tail}
----------------------------------------

This is an automated alert from the TENDERS scraping system.
"""

    msg.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"], context=context) as server:
            server.login(config["smtp_user"], config["smtp_password"])
            server.send_message(msg)
        print(f"Error notification sent to {config['to']}")
    except Exception as e:
        print(f"Failed to send error email: {e}")
        # Save to pending notifications as fallback
        pending_dir = PROJECT_DIR / "notifications" / "pending"
        pending_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(pending_dir / f"error_{timestamp}.json", "w") as f:
            json.dump({
                "type": "error",
                "timestamp": now,
                "exit_code": exit_code,
                "log_file": log_file,
                "body": body
            }, f, indent=2)
        print(f"Saved to {pending_dir}/error_{timestamp}.json")


if __name__ == "__main__":
    exit_code = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    log_file = sys.argv[2] if len(sys.argv) > 2 else "unknown"
    send_error_email(exit_code, log_file)
