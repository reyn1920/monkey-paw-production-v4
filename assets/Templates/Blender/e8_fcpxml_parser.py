
import xml.etree.ElementTree as ET
def parse_rational_sec(s:str)->float:
    s=(s or '').strip(); 
    if not s: return 0.0
    if s.endswith('s'): s=s[:-1]
    if '/' in s:
        try: a,b=s.split('/',1); return float(a)/float(b)
        except: return 0.0
    try: return float(s)
    except: return 0.0
def parse_fcpxml(xml_path: str):
    tree=ET.parse(xml_path); root=tree.getroot(); ns={'fcpx': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
    def fa(expr): return root.findall(expr, ns) if ns else root.findall(expr)
    assets={}; 
    for a in fa('.//fcpx:asset' if ns else './/asset'):
        assets[a.get('id')]={'name':a.get('name') or '', 'src': a.get('src') or ''}
    events=[]; titles=[]; vo_regions=[]
    for ac in fa('.//fcpx:asset-clip' if ns else './/asset-clip'):
        ref=ac.get('ref'); name=ac.get('name') or assets.get(ref,{}).get('name') or ''
        dur=parse_rational_sec(ac.get('duration') or '0s'); off=parse_rational_sec(ac.get('offset') or ac.get('start') or '0s')
        events.append({'name':name,'ref':ref,'src':assets.get(ref,{}).get('src',''),'duration_secs':dur,'start_secs':off,'end_secs':off+dur})
    for t in fa('.//fcpx:title' if ns else './/title'):
        dur=parse_rational_sec(t.get('duration') or '0s'); off=parse_rational_sec(t.get('offset') or t.get('start') or '0s')
        titles.append({'start_secs':off,'end_secs':off+dur})
    # naive VO detection: any asset-clip with role/name hint
    for ac in fa('.//fcpx:asset-clip' if ns else './/asset-clip'):
        role=(ac.get('audioRole') or ac.get('role') or '').lower(); nm=(ac.get('name') or '').lower()
        if any(k in role or k in nm for k in ['vo','narration','dialogue','voiceover']):
            dur=parse_rational_sec(ac.get('duration') or '0s'); off=parse_rational_sec(ac.get('offset') or ac.get('start') or '0s')
            vo_regions.append({'start_secs':off,'end_secs':off+dur})
    return {'assets':assets,'events':events,'titles':titles,'vo_regions':vo_regions}
