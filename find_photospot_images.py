#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Search Wikimedia Commons for images of 19 Iceland photo spots."""
import urllib.request, urllib.parse, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

UA = "IcelandTripPlanner/1.0 (personal trip planning; contact: nick@example.com)"

def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()

def http_head_ok(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            ok = r.status == 200
            final = r.geturl()
        return ok, final
    except Exception as e:
        print(f"  head ERR: {type(e).__name__}: {e}", file=sys.stderr)
        return False, str(e)

def commons_search(term, limit=8):
    url = ("https://commons.wikimedia.org/w/api.php?action=query&list=search"
           f"&srsearch={urllib.parse.quote(term)}&srnamespace=6&srlimit={limit}&format=json")
    try:
        _, body = http_get(url)
        data = json.loads(body)
        return [hit["title"] for hit in data.get("query", {}).get("search", [])]
    except Exception as e:
        print(f"  search ERR for {term!r}: {e}", file=sys.stderr)
        return []

def file_to_url(file_title):
    # file_title like "File:Foo.jpg"
    name = file_title.replace("File:", "").replace(" ", "_")
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(name)}?width=800"

def find_for(terms):
    """Try terms in order. Return (url, file_title) or (None, None)."""
    for t in terms:
        files = commons_search(t)
        for f in files:
            # Skip SVG, PDF, audio
            low = f.lower()
            if any(low.endswith(ext) for ext in (".svg", ".pdf", ".ogg", ".webm", ".tif", ".tiff")):
                continue
            url = file_to_url(f)
            ok, final = http_head_ok(url)
            if ok:
                return url, f, t
    return None, None, None

SPOTS = [
    ("Vogastapi Cliffs Pull-off", ["Vogastapi", "Voga­stapi Iceland", "Reykjanes Vogar cliffs"]),
    ("Kúagerði Lava Coast", ["Kúagerði", "Kuagerdi Iceland", "Hvassahraun lava"]),
    ("Straumsvík Lava Pools", ["Straumsvík", "Straumsvik Iceland", "Straumur Hafnarfjörður"]),
    ("Þingvallavatn South Shore", ["Þingvallavatn", "Thingvallavatn", "Þingvallavatn lake"]),
    ("Laugarvatn Steam Vents", ["Laugarvatn", "Laugarvatn lake", "Laugarvatn geothermal"]),
    ("Skálholt Cathedral", ["Skálholt cathedral", "Skalholt church", "Skálholt"]),
    ("Hafnarfjall Slopes", ["Hafnarfjall", "Hafnarfjall mountain Borgarnes"]),
    ("Pétursey Hill", ["Pétursey", "Petursey Iceland", "Pétursey mountain"]),
    ("Mýrdalssandur Black Desert", ["Mýrdalssandur", "Myrdalssandur", "Mýrdalssandur sand"]),
    ("Skeiðarársandur Bridge Monument", ["Skeiðarárbrú", "Skeidararbru bridge monument", "Skeiðarársandur bridge", "Skeiðarársandur"]),
    ("Fláajökull Pull-off", ["Fláajökull", "Flaajokull glacier", "Vatnajökull Fláajökull"]),
    ("Þakgil Road", ["Þakgil", "Thakgil Iceland", "Þakgil canyon"]),
    ("Borgarfjörður Bridge", ["Borgarfjarðarbrú", "Borgarfjordur bridge", "Borgarnes bridge"]),
    ("Eldborg Distant View", ["Eldborg crater", "Eldborg Snæfellsnes", "Eldborg volcano Iceland"]),
    ("Búðahraun Lava Field", ["Búðahraun", "Budahraun lava", "Búðakirkja lava field", "Búðir Snæfellsnes"]),
    ("Búlandshöfði Cliff Road", ["Búlandshöfði", "Bulandshofdi Snæfellsnes", "Búlandshöfði cliff"]),
    ("Grundarfjörður Old Boat", ["Grundarfjörður harbour", "Grundarfjordur boat", "Grundarfjörður"]),
    ("Bjarnarhöfn Shark Sheds", ["Bjarnarhöfn", "Bjarnarhofn shark", "Hákarl Bjarnarhöfn"]),
    ("Selatangar Ruins", ["Selatangar", "Selatangar fishing station", "Selatangar Reykjanes"]),
]

results = {}
for name, terms in SPOTS:
    url, ftitle, used = find_for(terms)
    results[name] = {"url": url, "file": ftitle, "term": used}
    print(f"{name}: {'OK' if url else 'NOT FOUND'}", file=sys.stderr)
    if url:
        print(f"  -> {url}", file=sys.stderr)
        print(f"  src: {ftitle} (term: {used})", file=sys.stderr)

print(json.dumps(results, indent=2, ensure_ascii=False))
