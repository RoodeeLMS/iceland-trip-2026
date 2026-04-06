#!/usr/bin/env python3
"""Append a message to loop-log.json.

Usage:
    python3 loop_log.py <level> <title> [message]

Levels: info, success, warning, error, update

Examples:
    python3 loop_log.py success "SafeTravel pins refreshed" "22 pins, 1 new"
    python3 loop_log.py info "No changes detected"
    python3 loop_log.py error "Fetch failed" "HTTP 500"
"""
import json
import sys
import os
import io
from datetime import datetime, timezone

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop-log.json')
MAX_ENTRIES = 200  # Keep last 200 entries

if len(sys.argv) < 3:
    print('Usage: python3 loop_log.py <level> <title> [message]', file=sys.stderr)
    print('Levels: info, success, warning, error, update', file=sys.stderr)
    sys.exit(1)

level = sys.argv[1].lower()
title = sys.argv[2]
message = sys.argv[3] if len(sys.argv) > 3 else ''

valid_levels = {'info', 'success', 'warning', 'error', 'update', 'suggestion'}
if level not in valid_levels:
    print(f'Invalid level: {level}. Must be one of: {", ".join(sorted(valid_levels))}', file=sys.stderr)
    sys.exit(2)

# Load existing log
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        data = {'entries': []}
else:
    data = {'entries': []}

if 'entries' not in data:
    data['entries'] = []

# Add new entry
entry = {
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'level': level,
    'title': title,
    'message': message
}
data['entries'].insert(0, entry)  # Newest first
data['entries'] = data['entries'][:MAX_ENTRIES]
data['last_updated'] = entry['timestamp']

with open(LOG_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'[{level}] {title}' + (f' — {message}' if message else ''))
