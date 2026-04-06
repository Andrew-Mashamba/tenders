#!/usr/bin/env python3
"""
Post-scrape tasks: regenerate active_tenders.md, send summary email, save notification.
Usage: python3 post_scrape.py [--scraped N] [--errors N] [--tenders N]
"""

from __future__ import annotations

import argparse
import json
import re
import smtplib
import ssl
import sys
from datetime import datetime, date, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

PROJECT_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS")
ACTIVE_TENDERS_MD = PROJECT_DIR / "institutions" / "active_tenders.md"
EMAIL_CONFIG = PROJECT_DIR / "config" / "email.json"
SENT_DIR = PROJECT_DIR / "notifications" / "sent"


def get_institution_category(slug: str) -> str:
    """Extract institution category from README frontmatter."""
    readme = PROJECT_DIR / "institutions" / slug / "README.md"
    if not readme.exists():
        return "Other"
    try:
        content = readme.read_text(encoding="utf-8")
        match = re.search(r"category:\s*[\"']([^\"']+)[\"']", content)
        return match.group(1).strip() if match else "Other"
    except Exception:
        return "Other"


def parse_date(s: str | None) -> date | None:
    """Parse YYYY-MM-DD or ISO datetime to date."""
    if not s:
        return None
    s = str(s).strip()
    if not s or s.lower() in ("none", "null", ""):
        return None
    try:
        if "T" in s:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def days_until(d: date | None, ref: date) -> int | None:
    """Days from ref to d. Negative if d is in the past."""
    if d is None:
        return None
    return (d - ref).days


def load_all_active_tenders() -> list[dict]:
    """Load all institutions/*/tenders/active/*.json files."""
    tenders = []
    active_dir = PROJECT_DIR / "institutions"
    if not active_dir.exists():
        return tenders
    for inst_dir in active_dir.iterdir():
        if not inst_dir.is_dir():
            continue
        slug = inst_dir.name
        tender_dir = inst_dir / "tenders" / "active"
        if not tender_dir.exists():
            continue
        for jf in tender_dir.glob("*.json"):
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                data["_institution_slug"] = slug
                data["_category"] = get_institution_category(slug)
                tenders.append(data)
            except Exception:
                continue
    return tenders


def generate_active_tenders_md(
    tenders: list[dict],
    today: date,
    run_id: str,
    scrape_stats: dict,
) -> str:
    """Generate active_tenders.md content."""
    closing_soon_days = 7
    closing_soon_cutoff = today + timedelta(days=closing_soon_days)

    closing_soon = []
    new_today = []
    for t in tenders:
        cd = parse_date(t.get("closing_date"))
        scraped = parse_date(t.get("scraped_at") or t.get("last_checked"))
        if cd and today <= cd <= closing_soon_cutoff:
            days_left = (cd - today).days
            closing_soon.append((t, days_left))
        if scraped == today:
            new_today.append(t)

    # Sort closing soon by days left
    closing_soon.sort(key=lambda x: (x[1], x[0].get("closing_date") or ""))

    # Group by category, then by institution
    by_category: dict[str, dict[str, list[dict]]] = {}
    for t in tenders:
        cat = t.get("_category", "Other")
        slug = t.get("_institution_slug", "unknown")
        if cat not in by_category:
            by_category[cat] = {}
        if slug not in by_category[cat]:
            by_category[cat][slug] = []
        by_category[cat][slug].append(t)

    # Sort tenders within each group by closing_date
    def sort_key(t):
        cd = t.get("closing_date") or ""
        return (cd == "" or cd is None, cd or "9999-99-99")

    for cat in by_category:
        for slug in by_category[cat]:
            by_category[cat][slug].sort(key=sort_key)

    # Sort categories alphabetically, "Other" last
    cat_order = sorted(by_category.keys(), key=lambda c: (c == "Other", c))

    lines = [
        "# Active Tenders Index",
        "",
        f"**Last Updated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} (Run ID: {run_id})",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total Active Tenders | {len(tenders)} |",
        f"| Institutions with Active Tenders | {len({t.get('_institution_slug') for t in tenders})} |",
        f"| New Tenders (this run) | {len(new_today)} |",
        f"| Closing Within 7 Days | {len(closing_soon)} |",
        "",
        "## Closing Soon (Within 7 Days)",
        "",
    ]

    if closing_soon:
        lines.append("| Institution | Tender | Closing Date | Days Left | Documents |")
        lines.append("|-------------|--------|--------------|-----------|-----------|")
        for t, days_left in closing_soon:
            title = (t.get("title") or "")[:55] + ("…" if len(t.get("title", "") or "") > 55 else "")
            docs = len(t.get("documents") or [])
            lines.append(
                f"| {t.get('_institution_slug', '')} | {title} | {t.get('closing_date') or 'None'} | {days_left} | {docs} |"
            )
    else:
        lines.append("*No tenders closing within 7 days.*")
    lines.append("")

    lines.append("## All Active Tenders by Institution Category")
    lines.append("")

    for cat in cat_order:
        insts = by_category[cat]
        total = sum(len(v) for v in insts.values())
        lines.append(f"### {cat} ({total} tenders)")
        lines.append("")

        for slug in sorted(insts.keys()):
            tlist = insts[slug]
            lines.append(f"#### {slug} ({len(tlist)} tender{'s' if len(tlist) != 1 else ''})")
            lines.append("")
            lines.append("| Tender ID | Title | Closing Date | Status | Docs |")
            lines.append("|-----------|-------|--------------|--------|------|")
            for t in tlist:
                tid = t.get("tender_id", "")
                title = (t.get("title") or "")[:50] + ("…" if len(t.get("title", "") or "") > 50 else "")
                closing = t.get("closing_date") or "None"
                status = t.get("status", "active")
                docs = len(t.get("documents") or [])
                lines.append(f"| {tid} | {title} | {closing} | {status} | {docs} |")
            lines.append("")

    lines.append("## Scrape Log")
    lines.append("")
    lines.append("| Run ID | Timestamp | Active | New | Closing Soon | Scraped | Errors |")
    lines.append("|--------|-----------|--------|-----|--------------|----------|--------|")
    lines.append(
        f"| {run_id} | {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} | {len(tenders)} | {len(new_today)} | {len(closing_soon)} | {scrape_stats.get('scraped', '-')} | {scrape_stats.get('errors', '-')} |"
    )

    return "\n".join(lines)


def send_summary_email(body_md: str, scrape_stats: dict) -> bool:
    """Send summary email via SMTP SSL."""
    try:
        with open(EMAIL_CONFIG) as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to read email config: {e}", file=sys.stderr)
        return False

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    subject = f"[TENDERS] Daily Summary — {len(body_md.splitlines())} active tenders — {now}"

    msg = MIMEMultipart()
    msg["From"] = config["from"]
    msg["To"] = config["to"]
    msg["Subject"] = subject

    body_plain = body_md.replace("|", " | ").replace("---", "---")
    msg.attach(MIMEText(body_plain, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"], context=context) as server:
            server.login(config["smtp_user"], config["smtp_password"])
            server.send_message(msg)
        print(f"Summary email sent to {config['to']}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}", file=sys.stderr)
        return False


def save_notification(body_md: str, scrape_stats: dict, run_id: str) -> Path:
    """Save notification JSON to notifications/sent/."""
    SENT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SENT_DIR / f"summary_{ts}.json"
    payload = {
        "type": "post_scrape_summary",
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "scrape_stats": scrape_stats,
        "body": body_md,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Notification saved to {path}")
    return path


def main():
    parser = argparse.ArgumentParser(description="Post-scrape: regenerate index, send email")
    parser.add_argument("--scraped", type=int, default=0, help="Pages/items scraped count")
    parser.add_argument("--errors", type=int, default=0, help="Error count")
    parser.add_argument("--tenders", type=int, default=0, help="Tenders found count")
    args = parser.parse_args()

    scrape_stats = {
        "scraped": args.scraped,
        "errors": args.errors,
        "tenders": args.tenders,
    }

    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    today = date.today()

    tenders = load_all_active_tenders()
    body_md = generate_active_tenders_md(tenders, today, run_id, scrape_stats)

    ACTIVE_TENDERS_MD.parent.mkdir(parents=True, exist_ok=True)
    ACTIVE_TENDERS_MD.write_text(body_md, encoding="utf-8")
    print(f"Regenerated {ACTIVE_TENDERS_MD} ({len(tenders)} tenders)")

    if send_summary_email(body_md, scrape_stats):
        save_notification(body_md, scrape_stats, run_id)
    else:
        pending = PROJECT_DIR / "notifications" / "pending"
        pending.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = pending / f"summary_{ts}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"type": "post_scrape_summary", "body": body_md, "scrape_stats": scrape_stats},
                f,
                indent=2,
            )
        print(f"Email failed; saved to pending: {path}")


if __name__ == "__main__":
    main()
