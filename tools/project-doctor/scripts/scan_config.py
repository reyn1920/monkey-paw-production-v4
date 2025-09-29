import os, json, sys
root = sys.argv[1] if len(sys.argv)>1 else "."
cfg = []
for base, _, files in os.walk(root):
    for f in files:
        if f.endswith((".yaml",".yml",".json",".toml",".env",".ini",".cfg")):
            cfg.append(os.path.join(base,f))
print(json.dumps({"config_files": sorted(cfg)}, indent=2))
