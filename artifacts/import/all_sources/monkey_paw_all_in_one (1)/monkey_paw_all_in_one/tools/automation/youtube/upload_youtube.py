# Dry-run uploader: prints what it would upload.
from pathlib import Path
import json, sys
def main(src_meta: str):
    p = Path(src_meta)
    meta = json.loads(p.read_text()) if p.exists() else {}
    print("[DRY-RUN] Would upload with:", json.dumps(meta, indent=2))
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "artifacts/staging/draft_youtube.meta.json")
