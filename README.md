# python-cli-automation-tools
Safe Python CLI tools for Excel cleaning, file renaming, scraping, and APIs.


# Python CLI Automation Tools

Small, safe, production-minded Python scripts for common automation tasks.

---

## Tools Included

### 1) Excel Cleaner (CLI)
Safely clean Excel files.
- Drops fully empty rows
- Optional missing-value handling: `ffill` (default), `bfill`, or `none`

**Usage**
```bash
python excel_cleaner.py -i input.xlsx -o output.xlsx --fill-method ffill
2) File Renamer (Safe & Idempotent)
Rename files in bulk without overwriting.

Dry-run mode

Collision-safe (finds next free index)

Safe to run multiple times

Usage

python rename_files.py --folder files --prefix invoice_ --start 1 --dry-run
3) Simple Web Scraper
Lightweight and polite scraper.

Configurable CSS selector

Optional JSON or CSV output

Uses User-Agent and timeout

Usage

python scrape_simple.py --url https://example.com --selector h1 --output results.json
4) Minimal Flask API
Simple JSON API.

No debug mode

Ready to run behind Gunicorn

Run locally

python app.py
Production

gunicorn -w 4 -b 0.0.0.0:8000 app:app
Requirements
pip install pandas openpyxl requests beautifulsoup4 flask
Notes
Use --dry-run before renaming files.

Files are never overwritten by design.

Check a website’s robots.txt before scraping.

Do not use Flask’s built-in server in production.

