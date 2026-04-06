#!/usr/bin/env python3
"""Fetch the latest SafeTravel.is point warnings and save as JSON.

Run this script periodically to update the local mirror of
safetravel.is point warnings. The data is embedded in the HTML of
https://safetravel.is/travel-conditions/ as a JavaScript array.

Usage:
    python3 fetch_safetravel_pins.py
"""
import urllib.request
import urllib.error
import re
import json
import sys
import io
from datetime import datetime, timezone

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

URL = 'https://safetravel.is/travel-conditions/'
OUTPUT = 'safetravel_pins.json'

try:
    req = urllib.request.Request(URL, headers={'User-Agent': 'IcelandTrip2026/1.0 (+mirror)'})
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode('utf-8', errors='replace')
except urllib.error.URLError as e:
    print(f'Failed to fetch {URL}: {e}', file=sys.stderr)
    sys.exit(1)

# Extract the items array
m = re.search(r'var items\s*=\s*(\[.*?\]);', html, re.DOTALL)
if not m:
    print('Could not find items array in HTML', file=sys.stderr)
    sys.exit(2)

try:
    items = json.loads(m.group(1))
except json.JSONDecodeError as e:
    print(f'Could not parse items JSON: {e}', file=sys.stderr)
    sys.exit(3)

# Clean HTML from text fields
def clean_html(s):
    if not s:
        return ''
    s = re.sub(r'<[^>]+>', ' ', str(s))
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

for item in items:
    if 'text' in item:
        item['text'] = clean_html(item['text'])

output = {
    'fetched_at': datetime.now(timezone.utc).isoformat(),
    'source': URL,
    'count': len(items),
    'pins': items
}

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Saved {len(items)} pins to {OUTPUT}')
for item in items:
    title = item.get('title', '?').strip()
    color = item.get('condition_color', '?')
    print(f'  [{color}] {title}')
