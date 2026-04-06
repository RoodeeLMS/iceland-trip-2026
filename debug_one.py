#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
UA = "IcelandTripPlanner/1.0 (personal)"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status, r.read(), r.geturl()

# 1) commons search
url = "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=Vogastapi&srnamespace=6&srlimit=5&format=json"
s, body, _ = get(url)
print("search status:", s)
data = json.loads(body)
hits = [h["title"] for h in data.get("query", {}).get("search", [])]
print("hits:", hits)

if hits:
    f = hits[0]
    name = f.replace("File:", "").replace(" ", "_")
    fp = f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(name)}?width=800"
    print("trying:", fp)
    try:
        s2, body2, final = get(fp)
        print("status:", s2, "final:", final, "bytes:", len(body2))
    except Exception as e:
        print("ERR:", type(e).__name__, e)
