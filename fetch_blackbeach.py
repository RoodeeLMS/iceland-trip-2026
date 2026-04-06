#!/usr/bin/env python3
"""Scrape the Reynisfjara black beach safety page and mirror current alert level.

Source: https://safetravel.is/travel-conditions/blackbeach-safety/

The page is editorial — level is conveyed in prose ("currently at X alert level").
We extract the sentence containing "currently" and infer level from keywords.

Output: blackbeach_status.json
    {
        "fetched_at": "...",
        "source": "...",
        "level": "green|yellow|orange|red|unknown",
        "sentence": "the full descriptive sentence",
        "raw_excerpt": "longer context chunk for verification"
    }
"""
import json
import os
import re
import sys
import io
import urllib.request
from datetime import datetime, timezone

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

URL = 'https://safetravel.is/travel-conditions/blackbeach-safety/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blackbeach_status.json')

def fetch():
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 IcelandTripLoop/1.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', errors='replace')

def extract(html):
    # Remove scripts/styles
    html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.S)
    html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Find sentence with "currently" or "today" status keywords
    sentence = None
    for pat in [r'[^.]*currently[^.]{0,400}\.', r'[^.]*today[^.]{0,300}\.', r'[^.]*at present[^.]{0,300}\.']:
        m = re.search(pat, text, re.I)
        if m:
            sentence = m.group().strip()
            break

    # Broader excerpt near keywords for verification
    kw_idx = -1
    for kw in ['currently', 'today', 'at present']:
        i = text.lower().find(kw)
        if i >= 0:
            kw_idx = i
            break
    raw_excerpt = text[max(0, kw_idx-100):kw_idx+500] if kw_idx >= 0 else text[:600]

    # Infer level from sentence/excerpt
    haystack = (sentence or '') + ' ' + raw_excerpt
    hl = haystack.lower()
    level = 'unknown'

    # Check for negations first e.g. "not at red alert level"
    # Strategy: find the strongest level mentioned, then see if it's negated
    def mentioned_but_not_negated(color):
        # look for color in haystack
        for m in re.finditer(color, hl):
            start = max(0, m.start() - 40)
            window = hl[start:m.start()]
            if re.search(r'\b(not|no|never|without)\b', window):
                continue
            return True
        return False

    # Try red → orange → yellow → green (most severe wins if actual)
    if mentioned_but_not_negated('red alert') or 'closed' in hl and 'beach is closed' in hl:
        level = 'red'
    elif mentioned_but_not_negated('orange') or 'viewpoint only' in hl or 'accessible from the viewpoint' in hl:
        level = 'orange'
    elif mentioned_but_not_negated('yellow'):
        level = 'yellow'
    elif mentioned_but_not_negated('green'):
        level = 'green'

    return level, sentence or '', raw_excerpt

def main():
    try:
        html = fetch()
    except Exception as e:
        print(f'Error fetching: {e}', file=sys.stderr)
        sys.exit(1)

    level, sentence, excerpt = extract(html)

    data = {
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'source': URL,
        'level': level,
        'sentence': sentence,
        'raw_excerpt': excerpt,
    }

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'[{level}] {sentence[:200] if sentence else "(no sentence)"}')

if __name__ == '__main__':
    main()
