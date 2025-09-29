
import csv, os

KEYWORDS = {
    "tv_news": ["cnn", "fox", "msnbc", "nbc", "abcnews", "cbsnews", "news"],
    "social_clip": ["tiktok", "instagram", "reels", "shorts", "twitter", "x.com"],
    "movie": ["trailer", "movie", "filmclip"],
    "music_video": ["vevo", "musicvideo", "mv_"]
}

def load_mapping(csv_path: str):
    m = []
    if not csv_path or not os.path.exists(csv_path):
        return m
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            m.append(row)
    return m

def classify(name: str, path: str, mapping):
    nm = (name or "").lower()
    p = (path or "").lower()
    for row in mapping:
        key = (row.get("name_or_path") or "").lower()
        if key and (key in nm or key in p):
            src = (row.get("source") or "original").strip().lower()
            return {
                "source": src,
                "src_url": row.get("src_url") or "",
                "attrib_text": row.get("attribution_text") or ""
            }
    for kind, words in KEYWORDS.items():
        if any(w in nm or w in p for w in words):
            return {"source": kind, "src_url": "", "attrib_text": ""}
    return {"source": "original", "src_url": "", "attrib_text": ""}

def events_to_manifest(events, mapping, slug: str):
    segs = []
    for ev in events:
        name = ev.get("name") or ev.get("clip_name") or ""
        src = ev.get("src") or ev.get("file") or ""
        dur = float(ev.get("duration_secs") or 0.0)
        cls = classify(name, src, mapping)
        if cls["source"] == "original":
            segs.append({"type":"original", "label": name, "duration": dur})
        else:
            segs.append({
                "type":"third_party",
                "source": cls["source"],
                "src_url": cls["src_url"],
                "duration": dur,
                "transformations": {"voiceover": False, "overlay_text": False, "pip_or_crop": True},
                "attribution": {"onscreen": bool(cls["attrib_text"]), "text": cls["attrib_text"] or ""}
            })
    uses_tp = any(s.get("type")=="third_party" for s in segs)
    return {"slug": slug, "uses_third_party": uses_tp, "segments": segs}
