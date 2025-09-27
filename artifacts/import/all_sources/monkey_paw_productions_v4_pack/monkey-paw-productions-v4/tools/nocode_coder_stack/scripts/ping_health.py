#!/usr/bin/env python3
import sys, urllib.request, json, ssl
url = sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:8000/api/health"
ctx = ssl.create_default_context()
with urllib.request.urlopen(url, context=ctx, timeout=5) as r:
    print("Health:", r.status, json.loads(r.read().decode("utf-8")))
