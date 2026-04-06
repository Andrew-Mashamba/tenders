# Opportunity Leads

When the scraper finds **no tenders or procurements** on an institution's website, it identifies business opportunities (sell, partner, or build) and creates draft outreach emails.

## Files

| File | Description |
|------|--------------|
| `leads.json` | JSON array of leads (source of truth) |
| `leads.csv` | Emails table — CSV for spreadsheet import, sending later |

Regenerate the CSV from JSON: `python3 /Volumes/DATA/PROJECTS/TENDERS/scripts/sync_leads_csv.py`

## Schema

Each lead in `leads.json` has:

| Field | Type | Description |
|-------|------|-------------|
| `institution_slug` | string | Institution folder name (e.g. `acbbank`) |
| `institution_name` | string | Display name |
| `website_url` | string | Main website or tender page URL |
| `emails` | string[] | All emails found on the site |
| `opportunity_type` | string | `sell` \| `partner` \| `build` |
| `opportunity_description` | string | Why Zima fits this institution |
| `draft_email_subject` | string | Subject line for outreach |
| `draft_email_body` | string | Full email body (plain text) |
| `created_at` | string | ISO 8601 timestamp |
| `status` | string | `pending` (default) |

## Usage

- The scraper appends new leads to `leads.json` when it finds no tenders.
- Use this table for later outreach: filter by `status: pending`, pick leads, send via your email client.
- Mark `status: sent` or `status: skipped` after you act.
