#!/usr/bin/env python3
"""Scrape vedur.is for Iceland Met Office data and write a local JSON mirror.

Fetches:
- Text forecast (human-written by IMO meteorologist on duty, the most authoritative source)
- Active weather alerts
- Wind / temperature / precipitation forecast map URLs (HARMONIE model)
- Cloud cover forecast maps
- Aurora cloud overlay maps

Output: vedur_forecast.json
"""
import json, os, re, sys, io, urllib.request
from datetime import datetime, timezone

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'vedur_forecast.json')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 IcelandTripLoop/1.0'

import ssl
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30, context=_SSL_CTX) as r:
        return r.read().decode('utf-8', errors='replace')

def parse_text_forecast(html):
    """Pull the text forecast block + valid timestamps."""
    out = {'outlook': '', 'multi_day': [], 'made_at': '', 'valid_until': ''}

    # The page has these key markers:
    # "Weather outlook" ... "Forecast made: dd.mm.yyyy hh:mm" ... "Valid until: ..."
    # "Weather forecast for the next several days" ... days...
    body = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    body = re.sub(r'<style.*?</style>', ' ', body, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Outlook section (today + tomorrow)
    m = re.search(r'Weather outlook\s+(.*?)Forecast made:\s*([\d.]+\s+[\d:]+)\s*\.\s*Valid until:\s*([\d.]+\s+[\d:]+)', text)
    if m:
        out['outlook'] = m.group(1).strip()
        out['made_at'] = m.group(2).strip()
        out['valid_until'] = m.group(3).strip()

    # Multi-day forecast
    m = re.search(r'Weather forecast for the next several days\s+(.*?)Forecast made:\s*([\d.]+\s+[\d:]+)\s*\.\s*Valid until:\s*([\d.]+\s+[\d:]+)', text)
    if m:
        multi = m.group(1).strip()
        # Split on "On <Dayname>: " markers
        # Use re.split to break the multi-string at each "On X:" boundary, then label.
        parts = re.split(r'\s*On (\w+(?:\s+and\s+\w+)?)\s*:\s*', multi)
        # parts[0] is preamble (if any), then alternating: day, content, day, content, ...
        days_out = []
        for i in range(1, len(parts), 2):
            day = parts[i].strip()
            content = parts[i+1].strip() if i+1 < len(parts) else ''
            if day and content:
                days_out.append({'day': day, 'forecast': content})
        out['multi_day'] = days_out
        out['multi_made_at'] = m.group(2).strip()
        out['multi_valid_until'] = m.group(3).strip()

    return out

def fetch_map_urls(html, type_pattern):
    """Find latest map image URLs of a given type from page HTML.

    Returns (urls, latest_run). Only the page-visible frames are returned;
    the actual published range is wider — extend_frame_range() handles that
    by probing additional hours.
    """
    pattern = re.compile(r'/photos/' + re.escape(type_pattern) + r'/([0-9]{6}_[0-9]{4})_(\d+)\.(gif|png)')
    matches = pattern.findall(html)
    if not matches:
        return [], None, None
    latest_run = max(set(m[0] for m in matches))
    ext = matches[0][2]
    visible_frames = sorted({int(m[1]) for m in matches if m[0] == latest_run})
    return visible_frames, latest_run, ext

def build_frame_urls(type_pattern, run, ext, frame_numbers):
    """Build map image URLs for the given frame numbers."""
    if 'thattaspa' in type_pattern:
        return [f'https://en.vedur.is/photos/{type_pattern}/{run}_{f:03d}.{ext}' for f in frame_numbers]
    else:
        return [f'https://en.vedur.is/photos/{type_pattern}/{run}_{f}.{ext}' for f in frame_numbers]

# Vedur publishes maps out to +72h. Frame intervals per type:
#  thattaspa wind/temp:  every 1h (003 to 072)
#  thattaspa precip:     every 3h (003 to 072)
#  harmonie cloud:       every 1h (1 to 72)
#  aurora isl_skyjahula: every 1h (1 to 72)
ECM_FRAMES = list(range(3, 145, 3)) + list(range(150, 241, 6))  # 3h to +144h, then 6h to +240h
FULL_RANGES = {
    'thattaspa_ig_island_10uv':         list(range(1, 73)),       # HARMONIE wind every 1h
    'thattaspa_ig_island_2t':           list(range(1, 73)),       # HARMONIE temp every 1h
    'thattaspa_ig_island_urk-msl-10uv': list(range(3, 73, 3)),    # HARMONIE precip every 3h
    'harmonie_island_tcc_lcc_mcc_hcc':  list(range(1, 73)),       # HARMONIE cloud every 1h
    'isl_skyjahula2':                   list(range(1, 73)),       # aurora cloud every 1h
    'thattaspa_ecm-is_island_10uv':         ECM_FRAMES,           # ECMWF IFS wind (medium-range, +240h)
    'thattaspa_ecm-is_island_2t':           ECM_FRAMES,           # ECMWF IFS temp (medium-range, +240h)
    'thattaspa_ecm-is_island_urk-msl-10uv': ECM_FRAMES,           # ECMWF IFS precip+MSL (medium-range, +240h)
}

def fetch_alerts(html):
    """Extract alert JSON embedded in the page."""
    m = re.search(r"'alert':\s*\{[^}]*'data':\s*(\{.*?\})\s*\}\s*\}", html, re.S)
    if not m:
        # Try simpler pattern
        m = re.search(r"\"alerts\":\s*(\[[^\]]*\])", html, re.S)
        if not m:
            return {'count': 0, 'alerts': []}
        try:
            alerts_arr = json.loads(m.group(1))
            return {'count': len(alerts_arr), 'alerts': []}
        except:
            return {'count': 0, 'alerts': []}
    try:
        # Replace single quotes with double for JSON
        raw = m.group(1).replace("'", '"')
        data = json.loads(raw)
        alerts = data.get('alerts', [])
        # Extract English versions
        out = []
        for a in alerts:
            for info in a.get('info', []):
                if info.get('language', '').startswith('en'):
                    out.append({
                        'event': info.get('event', ''),
                        'headline': info.get('headline', ''),
                        'description': info.get('description', ''),
                        'severity': info.get('severity', ''),
                        'area': info.get('area', [{}])[0].get('areaDesc', '') if info.get('area') else '',
                        'onset': info.get('onset', ''),
                        'expires': info.get('expires', ''),
                    })
        return {'count': len(out), 'alerts': out}
    except Exception as e:
        return {'count': 0, 'alerts': [], 'error': str(e)}

def main():
    result = {
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'source': 'https://en.vedur.is/',
    }

    # 1. Text forecast (most authoritative)
    try:
        html = fetch('https://en.vedur.is/weather/forecasts/text/')
        result['text_forecast'] = parse_text_forecast(html)
        result['alerts'] = fetch_alerts(html)
    except Exception as e:
        result['text_forecast_error'] = str(e)

    # 2. Wind / temp maps from elements page
    latest_run = None
    try:
        html2 = fetch('https://en.vedur.is/weather/forecasts/elements/')
        for label, type_id in [('wind', 'thattaspa_ig_island_10uv'),
                                ('temperature', 'thattaspa_ig_island_2t'),
                                ('wind_ecmwf', 'thattaspa_ecm-is_island_10uv'),
                                ('temperature_ecmwf', 'thattaspa_ecm-is_island_2t'),
                                ('precipitation_ecmwf', 'thattaspa_ecm-is_island_urk-msl-10uv')]:
            try:
                visible, run, ext = fetch_map_urls(html2, type_id)
                if run:
                    if 'ig_island' in type_id:  # only HARMONIE runs drive precip
                        latest_run = run
                    full_frames = FULL_RANGES.get(type_id, visible)
                    urls = build_frame_urls(type_id, run, ext, full_frames)
                    result[f'{label}_maps'] = {'run': run, 'urls': urls, 'frame_hours': full_frames}
            except Exception as e:
                result[f'{label}_maps_error'] = str(e)
    except Exception as e:
        result['element_maps_error'] = str(e)

    # Precipitation maps — page uses JS, construct URLs directly using the wind run.
    try:
        if latest_run:
            type_id = 'thattaspa_ig_island_urk-msl-10uv'
            frames = FULL_RANGES[type_id]
            urls = build_frame_urls(type_id, latest_run, 'gif', frames)
            result['precipitation_maps'] = {'run': latest_run, 'urls': urls, 'frame_hours': frames}
    except Exception as e:
        result['precipitation_maps_error'] = str(e)

    # 3. Cloud cover + aurora maps
    try:
        html3 = fetch('https://en.vedur.is/weather/forecasts/aurora/')
        for label, type_id in [('cloud_total', 'harmonie_island_tcc_lcc_mcc_hcc'),
                                ('aurora_clouds', 'isl_skyjahula2')]:
            try:
                visible, run, ext = fetch_map_urls(html3, type_id)
                if run:
                    full_frames = FULL_RANGES.get(type_id, visible)
                    urls = build_frame_urls(type_id, run, ext, full_frames)
                    result[f'{label}_maps'] = {'run': run, 'urls': urls, 'frame_hours': full_frames}
            except Exception as e:
                result[f'{label}_maps_error'] = str(e)
    except Exception as e:
        result['aurora_page_error'] = str(e)

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Print summary
    tf = result.get('text_forecast', {})
    print(f'Outlook: {tf.get("outlook", "")[:120]}...')
    print(f'Multi-day: {len(tf.get("multi_day", []))} days')
    print(f'Alerts: {result.get("alerts", {}).get("count", 0)}')
    for k in ['wind_maps', 'temperature_maps', 'precipitation_maps', 'cloud_total_maps', 'aurora_clouds_maps', 'wind_ecmwf_maps', 'temperature_ecmwf_maps', 'precipitation_ecmwf_maps']:
        v = result.get(k, {})
        print(f'{k}: run {v.get("run", "?")} ({len(v.get("urls", []))} frames)')

if __name__ == '__main__':
    main()
