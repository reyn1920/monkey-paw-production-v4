
import os, csv
KEYWORDS={"tv_news":["cnn","fox","msnbc","nbc","abcnews","cbsnews","news"],"social_clip":["tiktok","instagram","reels","shorts","twitter","x.com"],"movie":["trailer","movie","filmclip"],"music_video":["vevo","musicvideo","mv_"]}
def load_mapping(csv_path:str):
    m=[]; 
    if not csv_path or not os.path.exists(csv_path): return m
    with open(csv_path,"r",encoding="utf-8") as f:
        for r in csv.DictReader(f): m.append(r)
    return m
def classify(name:str, path:str, mapping):
    nm=(name or '').lower(); p=(path or '').lower()
    for row in mapping:
        key=(row.get('name_or_path') or '').lower()
        if key and (key in nm or key in p):
            return {"source": (row.get('source') or 'original').lower(), "src_url": row.get('src_url') or "", "attrib_text": row.get('attribution_text') or ""}
    for kind, words in KEYWORDS.items():
        if any(w in nm or w in p for w in words): return {"source": kind, "src_url":"", "attrib_text": ""}
    return {"source":"original","src_url":"","attrib_text":""}
def overlap(a0,a1,b0,b1): 
    s=max(a0,b0); e=min(a1,b1); return max(0.0, e-s)
def events_to_manifest(events, mapping, slug, title_regions=None, vo_regions=None):
    title_regions=title_regions or []; vo_regions=vo_regions or []; segs=[]
    for ev in events:
        name=ev.get('name') or ''; src=ev.get('src') or ''; dur=float(ev.get('duration_secs') or 0.0)
        s0=float(ev.get('start_secs') or 0.0); s1=float(ev.get('end_secs') or (s0+dur))
        cls=classify(name, src, mapping)
        ov_total=sum(overlap(s0,s1,tr.get('start_secs',0.0),tr.get('end_secs',0.0)) for tr in title_regions)
        overlay_flag = (ov_total >= 0.2*dur) if dur>0 else False
        vo_total=sum(overlap(s0,s1,vr.get('start_secs',0.0),vr.get('end_secs',0.0)) for vr in vo_regions)
        voiceover_flag = (vo_total >= 0.5*dur) if dur>0 else False
        if cls['source']=='original':
            segs.append({'type':'original','label':name,'duration':dur,'start':s0,'end':s1,'transformations':{'overlay_text':overlay_flag,'voiceover':False,'pip_or_crop':False}})
        else:
            segs.append({'type':'third_party','source':cls['source'],'src_url':cls['src_url'],'duration':dur,'start':s0,'end':s1,'transformations':{'voiceover':voiceover_flag,'overlay_text':overlay_flag,'pip_or_crop':True,'vo_overlap_secs':vo_total,'overlay_overlap_secs':ov_total},'attribution':{'onscreen':bool(cls['attrib_text']),'text':cls['attrib_text']}})
    return {"slug": slug, "uses_third_party": any(s.get('type')=='third_party' for s in segs), "segments": segs}
