
import xml.etree.ElementTree as ET

def parse_rational_sec(s: str) -> float:
    s = (s or "").strip()
    if not s:
        return 0.0
    if s.endswith('s'):
        s = s[:-1]
    if '/' in s:
        try:
            num, den = s.split('/', 1)
            return float(num) / float(den)
        except Exception:
            return 0.0
    try:
        return float(s)
    except Exception:
        return 0.0

def parse_fcpxml(xml_path: str):
    tree = ET.parse(xml_path); root = tree.getroot()
    ns = {'fcpx': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
    assets = {}
    # assets
    query_assets = './/fcpx:asset' if ns else './/asset'
    for a in root.findall(query_assets, ns):
        aid = a.get('id'); name = a.get('name') or ''
        src = a.get('src') or ''
        assets[aid] = {'name': name, 'src': src}
    events = []
    # asset-clip nodes
    query_ac = './/fcpx:asset-clip' if ns else './/asset-clip'
    for ac in root.findall(query_ac, ns):
        ref = ac.get('ref'); name = ac.get('name') or ''
        dur = parse_rational_sec(ac.get('duration') or '0s')
        events.append({'name': name, 'ref': ref, 'duration_secs': dur, 'src': assets.get(ref, {}).get('src', '')})
    # clip nodes (fallback)
    query_clip = './/fcpx:clip' if ns else './/clip'
    for clip in root.findall(query_clip, ns):
        ref = clip.get('ref'); name = clip.get('name') or ''
        dur = parse_rational_sec(clip.get('duration') or '0s')
        if dur > 0:
            events.append({'name': name, 'ref': ref, 'duration_secs': dur, 'src': assets.get(ref, {}).get('src', '')})
    return {"assets": assets, "events": events}
