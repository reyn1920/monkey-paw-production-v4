#!/usr/bin/env python3
import sys
import os
import json
import re


def extract(content):
    content = re.sub(r"<script.*?</script>", "", content, flags=re.S | re.I)
    content = re.sub(r"<style.*?</style>", "", content, flags=re.S | re.I)
    items = []
    for m in re.findall(r"<li[^>]*>(.*?)</li>", content, flags=re.S | re.I):
        t = re.sub(r"<[^>]+>", "", m).strip()
        if t:
            items.append(t)
    for m in re.findall(r"<option[^>]*>(.*?)</option>", content, flags=re.S | re.I):
        t = re.sub(r"<[^>]+>", "", m).strip()
        if t:
            items.append(t)
    for m in re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", content, flags=re.S | re.I):
        t = re.sub(r"<[^>]+>", "", m).strip()
        if t:
            items.append(t)
    return items


def main(indir, outjson):
    out = {"voices": [], "items": []}
    for root, _, files in os.walk(indir):
        for f in files:
            if not f.lower().endswith((".html", ".htm", ".txt")):
                continue
            p = os.path.join(root, f)
            try:
                c = open(p, encoding="utf-8", errors="ignore").read()
            except:
                continue
            for t in extract(c):
                if re.search(r"voice|preview|pro|male|female|tone|characters", t, re.I):
                    out["voices"].append(
                        {
                            "source": "local_html",
                            "voice_id": None,
                            "name": t,
                            "gender": None,
                            "lang": None,
                            "meta": {},
                        }
                    )
                else:
                    out["items"].append(
                        {
                            "category": "scraped_text",
                            "title": t[:80],
                            "content": t[:1000],
                            "path": p,
                            "meta": {},
                        }
                    )
    json.dump(out, open(outjson, "w", encoding="utf-8"), indent=2)
    print("wrote", outjson, "voices", len(out["voices"]), "items", len(out["items"]))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python utils/rescrape_local.py indir out.json")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
