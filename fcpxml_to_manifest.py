#!/usr/bin/env python3
import sys, json, os
from backend.fcpxml_parser import parse_fcpxml
from backend.manifest_builder import load_mapping, events_to_manifest

def main():
    if len(sys.argv)<3:
        print("Usage: fcpxml_to_manifest.py input.fcpxml output.json [mapping.csv]"); sys.exit(1)
    xml = sys.argv[1]; out = sys.argv[2]; mapping = sys.argv[3] if len(sys.argv)>3 else ""
    parsed = parse_fcpxml(xml)
    slug = os.path.splitext(os.path.basename(out))[0]
    mani = events_to_manifest(parsed["events"], load_mapping(mapping), slug)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out,"w",encoding="utf-8").write(json.dumps(mani, indent=2))
    print("Wrote", out)

if __name__ == "__main__":
    main()
