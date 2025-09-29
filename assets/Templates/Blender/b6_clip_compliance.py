
import json
DEFAULT_RULES={"max_continuous_by_source":{"tv_news":8.0,"talk_show":6.0,"movie":5.0,"music_video":5.0,"social_clip":12.0,"unknown":6.0},"max_total_third_party_secs":90.0,"min_transform_ratio":0.6,"require_attribution":True,"require_overlay_pct":0.5}
def analyze_timeline(manifest_path: str, rules: dict=None):
    rules=rules or DEFAULT_RULES; js=json.loads(open(manifest_path,"r",encoding="utf-8").read())
    if not js.get("uses_third_party"): return {"compliance_ok":True,"notes":["No third-party footage used."],"summary":{}}
    segs=js.get("segments",[]); total_third=0.0; with_overlay=0; commentary_secs=0.0; viol=[]
    for i,s in enumerate(segs):
        if s.get("type")!="third_party": continue
        dur=float(s.get("duration",0.0) or 0.0); src=(s.get("source") or "unknown").lower(); total_third+=dur
        lim=rules["max_continuous_by_source"].get(src, rules["max_continuous_by_source"]["unknown"])
        if dur>lim+1e-3: viol.append(f"Clip {i} from {src} exceeds per-clip limit: {dur:.1f}s > {lim:.1f}s")
        t=s.get("transformations",{}); 
        if t.get("overlay_text") or t.get("pip_or_crop"): with_overlay+=1
        commentary_secs += float(t.get("vo_overlap_secs") or (dur if t.get("voiceover") else 0.0))
        if rules.get("require_attribution",True) and not (s.get("attribution",{}).get("onscreen")): viol.append(f"Clip {i} missing on-screen attribution text")
    if total_third>rules["max_total_third_party_secs"]: viol.append(f"Total third-party duration exceeds limit: {total_third:.1f}s > {rules['max_total_third_party_secs']:.0f}s")
    tp=sum(1 for s in segs if s.get("type")=="third_party")
    if tp:
        if with_overlay/tp < rules["require_overlay_pct"]-1e-9: viol.append("Insufficient overlays/PiP on third-party clips")
        if commentary_secs/total_third < rules["min_transform_ratio"]-1e-9: viol.append("Insufficient commentary over third-party audio")
    return {"compliance_ok": len(viol)==0, "violations": viol, "summary":{"total_third_party_secs":total_third}}
