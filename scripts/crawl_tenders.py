#!/usr/bin/env python3
"""Crawl Tanzanian domains for tender/procurement pages."""

import asyncio
import aiohttp
import ssl
import re
import json
import time
import logging
import warnings
from pathlib import Path
from urllib.parse import urljoin

# Suppress all the noise
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")

PRIORITY_FILE = "/tmp/tz_priority.txt"
OUTPUT_FILE = "/Volumes/DATA/PROJECTS/TENDERS/institutions/websites.md"
RESULTS_JSON = "/tmp/tender_crawl_results.json"

# Keywords that indicate a tender/procurement page
TENDER_KEYWORDS = [
    'tender', 'tenders', 'procurement', 'rfp', 'rfq', 'rfi',
    'expression of interest', 'eoi', 'bidding', 'bid',
    'zabuni', 'manunuzi',  # Swahili for tenders/procurement
    'quotation', 'invitation to bid', 'request for proposal',
    'supply', 'prequalification',
]

# URL paths commonly used for tender pages
TENDER_PATHS = [
    '/tenders', '/tender', '/procurement', '/procurement/',
    '/tenders/', '/tender/', '/bids', '/bids/',
    '/rfp', '/rfp/', '/opportunities', '/opportunities/',
    '/zabuni', '/manunuzi',
    '/en/tenders', '/en/procurement',
    '/pages/tenders', '/pages/procurement',
]

TIMEOUT = aiohttp.ClientTimeout(total=10, connect=5)
CONCURRENT = 50  # concurrent connections
SEMAPHORE = asyncio.Semaphore(CONCURRENT)


async def check_domain(session, domain, results):
    """Check if a domain has tender-related content."""
    async with SEMAPHORE:
        url = f"https://{domain}"
        found = []

        # Try homepage first
        try:
            async with session.get(url, allow_redirects=True, timeout=TIMEOUT) as resp:
                if resp.status == 200:
                    text = await resp.text(errors='replace')
                    text_lower = text.lower()

                    # Check for tender keywords in homepage
                    matched_keywords = []
                    for kw in TENDER_KEYWORDS:
                        if kw in text_lower:
                            matched_keywords.append(kw)

                    if matched_keywords:
                        # Extract tender-related links
                        tender_links = []
                        link_pattern = re.compile(r'href=["\']([^"\']*(?:tender|procurement|rfp|bid|zabuni|manunuzi)[^"\']*)["\']', re.I)
                        for match in link_pattern.finditer(text):
                            link = match.group(1)
                            if not link.startswith(('javascript:', 'mailto:', '#')):
                                full_url = urljoin(str(resp.url), link)
                                tender_links.append(full_url)

                        # Extract title
                        title_match = re.search(r'<title[^>]*>([^<]+)</title>', text, re.I)
                        title = title_match.group(1).strip() if title_match else domain

                        found.append({
                            'url': str(resp.url),
                            'title': title,
                            'keywords': matched_keywords,
                            'tender_links': list(set(tender_links))[:10],
                        })
        except Exception:
            # Try HTTP if HTTPS fails
            try:
                url_http = f"http://{domain}"
                async with session.get(url_http, allow_redirects=True, timeout=TIMEOUT) as resp:
                    if resp.status == 200:
                        text = await resp.text(errors='replace')
                        text_lower = text.lower()

                        matched_keywords = []
                        for kw in TENDER_KEYWORDS:
                            if kw in text_lower:
                                matched_keywords.append(kw)

                        if matched_keywords:
                            tender_links = []
                            link_pattern = re.compile(r'href=["\']([^"\']*(?:tender|procurement|rfp|bid|zabuni|manunuzi)[^"\']*)["\']', re.I)
                            for match in link_pattern.finditer(text):
                                link = match.group(1)
                                if not link.startswith(('javascript:', 'mailto:', '#')):
                                    full_url = urljoin(str(resp.url), link)
                                    tender_links.append(full_url)

                            title_match = re.search(r'<title[^>]*>([^<]+)</title>', text, re.I)
                            title = title_match.group(1).strip() if title_match else domain

                            found.append({
                                'url': str(resp.url),
                                'title': title,
                                'keywords': matched_keywords,
                                'tender_links': list(set(tender_links))[:10],
                            })
            except Exception:
                pass

        # Also try common tender paths directly
        if not found:
            for path in TENDER_PATHS[:4]:  # Only try top paths to save time
                for scheme in ['https', 'http']:
                    try:
                        test_url = f"{scheme}://{domain}{path}"
                        async with session.get(test_url, allow_redirects=True, timeout=TIMEOUT) as resp:
                            if resp.status == 200:
                                text = await resp.text(errors='replace')
                                if len(text) > 500:  # Not just an error page
                                    text_lower = text.lower()
                                    matched_keywords = []
                                    for kw in TENDER_KEYWORDS:
                                        if kw in text_lower:
                                            matched_keywords.append(kw)

                                    if matched_keywords:
                                        title_match = re.search(r'<title[^>]*>([^<]+)</title>', text, re.I)
                                        title = title_match.group(1).strip() if title_match else domain

                                        found.append({
                                            'url': str(resp.url),
                                            'title': title,
                                            'keywords': matched_keywords,
                                            'tender_links': [],
                                        })
                                        break
                    except Exception:
                        continue
                if found:
                    break

        if found:
            results[domain] = found
            fprint(f"  FOUND: {domain} — {found[0]['keywords']}")


async def main():
    with open(PRIORITY_FILE) as f:
        domains = [line.strip() for line in f if line.strip()]

    fprint(f"Crawling {len(domains)} priority domains for tenders...")
    fprint(f"Concurrency: {CONCURRENT}")
    print()

    results = {}

    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(ssl=ssl_ctx, limit=CONCURRENT, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Process in batches
        batch_size = 100
        for i in range(0, len(domains), batch_size):
            batch = domains[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(domains) + batch_size - 1) // batch_size
            fprint(f"Batch {batch_num}/{total_batches} ({i+1}-{i+len(batch)} of {len(domains)})...")

            tasks = [check_domain(session, domain, results) for domain in batch]
            await asyncio.gather(*tasks, return_exceptions=True)

            fprint(f"  Found so far: {len(results)}")

    # Save results
    with open(RESULTS_JSON, 'w') as f:
        json.dump(results, f, indent=2)

    fprint(f"\nDone! Found {len(results)} domains with tender content.")
    fprint(f"Results saved to {RESULTS_JSON}")


def fprint(*args, **kwargs):
    """Print with flush."""
    print(*args, **kwargs, flush=True)


if __name__ == "__main__":
    asyncio.run(main())
