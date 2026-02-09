#!/usr/bin/env python3
"""
scrape_simple.py
Lightweight, polite web scraper.

Usage:
    python scrape_simple.py --url https://example.com --selector h1 --output results.json
"""
import argparse
import json
import logging
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(message)s")
LOG = logging.getLogger(__name__)

DEFAULT_UA = "Mozilla/5.0 (compatible; SimpleScraper/1.0)"


def fetch_texts(url: str, selector: str, headers: dict, timeout: int) -> List[str]:
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        LOG.error("Failed to fetch URL: %s", exc)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    elements = soup.select(selector)
    return [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]


def main(argv=None):
    p = argparse.ArgumentParser(description="Extract text from a webpage by CSS selector.")
    p.add_argument("--url", "-u", required=True, help="URL to fetch")
    p.add_argument("--selector", "-s", default="h1", help="CSS selector (default: h1)")
    p.add_argument("--user-agent", default=DEFAULT_UA, help="User-Agent header")
    p.add_argument("--timeout", type=int, default=10, help="Request timeout")
    p.add_argument("--output", "-o", help="Optional output file (.json or .csv)")
    args = p.parse_args(argv)

    headers = {"User-Agent": args.user_agent}
    LOG.info("Fetching %s (selector: %s)", args.url, args.selector)

    items = fetch_texts(args.url, args.selector, headers, args.timeout)
    if not items:
        LOG.info("No items found.")
        return

    for i, text in enumerate(items, start=1):
        LOG.info("%d. %s", i, text)

    if args.output:
        out = Path(args.output)
        try:
            if out.suffix.lower() == ".csv":
                out.write_text("\n".join(items), encoding="utf-8")
            else:
                out.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
            LOG.info("Saved %d items to %s", len(items), out)
        except Exception as exc:
            LOG.error("Failed to save output: %s", exc)


if __name__ == "__main__":
    main()

