#!/usr/bin/env python3
import sys, json, os
from backend.edl_parser import parse_edl
from backend.manifest_builder import load_mapping, events_to_manifest

def main():
    if len(sys.argv)<3:
        print("Usage: edl_to_manifest.py input.edl output.json [fps=30] [mapping.csv]"); sys.exit(1)
    edl = sys.argv[1]; out = sys.argv[2]
    fps = int(sys.argv[3]) if len(sys.argv)>3 and sys.argv[3].isdigit() else 30
    mapping = sys.argv[4] if len(sys.argv)>4 else ""
    events = parse_edl(edl, fps=fps)
    slug = os.path.splitext(os.path.basename(out))[0]
    mani = events_to_manifest(events, load_mapping(mapping), slug)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out,"w",encoding="utf-8").write(json.dumps(mani, indent=2))
    print("Wrote", out)

if __name__ == "__main__":
    main()
