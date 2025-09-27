from pathlib import Path
import json, sys

def main(src_path: str):
    p = Path(src_path)
    text = p.read_text() if p.exists() else "No content"
    meta = {
        "title": p.stem.replace("_"," ").title(),
        "description": text[:200],
        "tags": ["monkey paw","auto"],
        "thumbnail": str(p.with_suffix(".png").name)
    }
    out = p.with_suffix(".meta.json")
    out.write_text(json.dumps(meta, indent=2))
    print(out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "artifacts/staging/draft_youtube.txt")
