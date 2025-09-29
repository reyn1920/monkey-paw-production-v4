
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path
import json
from .edl_parser import parse_edl
from .fcpxml_parser import parse_fcpxml
from .manifest_builder import load_mapping, events_to_manifest
from .clip_compliance import analyze_timeline, DEFAULT_RULES
router = APIRouter()
def write_and_check(manifest, out_folder: Path):
    out_folder.mkdir(parents=True, exist_ok=True)
    mani_path = out_folder / "timeline.json"
    mani_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    res = analyze_timeline(str(mani_path), DEFAULT_RULES)
    (out_folder / "compliance.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    return str(mani_path), res
@router.post("/compliance/ingest_fcpxml")
def ingest_fcpxml(body: dict):
    slug=(body.get("slug") or "").strip(); xml_path=(body.get("xml_path") or "").strip(); mapping_csv=(body.get("mapping_csv") or "").strip()
    if not slug or not Path(xml_path).exists(): return JSONResponse({"ok":False,"error":"slug or xml_path missing"}, status_code=400)
    parsed=parse_fcpxml(xml_path); events=parsed["events"]; titles=parsed.get("titles") or []; vo=parsed.get("vo_regions") or []; mapping=load_mapping(mapping_csv)
    mani=events_to_manifest(events, mapping, slug, title_regions=titles, vo_regions=vo)
    mani_path, comp=write_and_check(mani, Path(f"assets/out/{slug}"))
    return {"ok":True, "manifest": mani_path, "compliance": comp, "detected":{"titles":len(titles),"vo_regions":len(vo)}}
@router.post("/compliance/ingest_edl")
def ingest_edl(body: dict):
    slug=(body.get("slug") or "").strip(); edl_path=(body.get("edl_path") or "").strip(); fps=int(body.get("fps",30)); mapping_csv=(body.get("mapping_csv") or "").strip()
    if not slug or not Path(edl_path).exists(): return JSONResponse({"ok":False,"error":"slug or edl_path missing"}, status_code=400)
    events=parse_edl(edl_path, fps=fps); mapping=load_mapping(mapping_csv); mani=events_to_manifest(events, mapping, slug); mani_path, comp=write_and_check(mani, Path(f"assets/out/{slug}"))
    return {"ok":True, "manifest": mani_path, "compliance": comp}
@router.post("/compliance/ingest_auto")
def ingest_auto(body: dict):
    slug=(body.get("slug") or "").strip(); folder=Path(body.get("folder") or "assets/inbox")
    if not slug or not folder.exists(): return JSONResponse({"ok":False,"error":"slug or folder missing"}, status_code=400)
    cand=sorted(list(folder.glob("*.fcpxml"))+list(folder.glob("*.edl")), key=lambda p:p.stat().st_mtime, reverse=True)
    if not cand: return JSONResponse({"ok":False,"error":"no .fcpxml or .edl found"}, status_code=404)
    p=cand[0]
    if p.suffix.lower()==".fcpxml": return ingest_fcpxml({"slug":slug,"xml_path":str(p),"mapping_csv":"assets/mappings/clip_sources.csv"})
    else: return ingest_edl({"slug":slug,"edl_path":str(p),"mapping_csv":"assets/mappings/clip_sources.csv","fps":30})
