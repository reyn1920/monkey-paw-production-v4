
import re
TC_RE=re.compile(r"(\d{2}):(\d{2}):(\d{2}):(\d{2})")
def tc_to_frames(tc, fps=30):
    m=TC_RE.match(tc.strip()); 
    if not m: return 0
    hh,mm,ss,ff=map(int,m.groups()); return ((hh*3600+mm*60+ss)*fps)+ff
def frames_to_seconds(frames, fps=30): return frames/float(fps)
def parse_edl(edl_path, fps=30):
    ev=[]; lines=open(edl_path,"r",encoding="utf-8",errors="ignore").read().splitlines(); cur=None
    for ln in lines:
        m=re.match(r"^(\d{3})\s+\S+\s+(V|A|VA)\s+\S+\s+(\d{2}:\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2}:\d{2})", ln)
        if m:
            rec={"event":int(m.group(1)),"track":m.group(2),"src_in":m.group(3),"src_out":m.group(4),"rec_in":m.group(5),"rec_out":m.group(6),"duration_secs":frames_to_seconds(tc_to_frames(m.group(6),fps)-tc_to_frames(m.group(5),fps),fps),"clip_name":None,"file":None}
            ev.append(rec); cur=rec; continue
        m=re.match(r"^\* FROM CLIP NAME:\s*(.+)", ln); 
        if m and cur: cur["clip_name"]=m.group(1).strip()
        m=re.match(r"^\* SOURCE FILE:\s*(.+)", ln); 
        if m and cur: cur["file"]=m.group(1).strip()
    return ev
