#!/usr/bin/env python3
import os, sys, ast, json, re, argparse
try:
    import yaml  # type: ignore
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False

DEFAULT_BAN = [
    "production","Production","PRODUCTION",
    "simulation","placeholder","theoretical","demo","mock","fake","sample","test"
]
DEFAULT_SKIPS = [".venv","node_modules","__pycache__","dist","build",".git",".idea",".vscode"]
ALLOW_LINE_SUBSTR = ["APP_DIR","ONLINE_APP_DIR","TRAE_DB_PATH","online production"]

CTRL_CHARS = "".join(chr(c) for c in range(0x00, 0x20) if c not in (0x09,0x0A,0x0D))
CTRL_RE = re.compile(f"[{re.escape(CTRL_CHARS)}]")
BRACKET_SURGEON_RE = re.compile(r"^\s*#\s*(BRACKET_SURGEON:.*|FIXIT:.*)$")

def read_text(p):
    with open(p,"rb") as f:
        b=f.read()
    if b.count(b"\0")>0:
        raise ValueError("binary file")
    return b.decode("utf-8","replace")

def write_text(p,t):
    with open(p,"w",encoding="utf-8") as f:
        f.write(t)

def normalize_newlines(s):
    s=s.replace("\r\n","\n").replace("\r","\n")
    if not s.endswith("\n"): s+="\n"
    return s

def safe_fixes(path,text):
    t=normalize_newlines(text)
    t=CTRL_RE.sub("",t)
    lines=[ln for ln in t.splitlines() if not BRACKET_SURGEON_RE.match(ln)]
    return "\n".join(lines)+"\n"

def scan_py(path,ban,fix):
    issues=[]
    try:
        src=read_text(path)
        for i,line in enumerate(src.splitlines(),1):
            if any(w in line for w in ALLOW_LINE_SUBSTR): pass
            else:
                for tok in ban:
                    if tok and tok in line:
                        issues.append(f"{path}:{i}: banned token '{tok}'")
        try:
            ast.parse(src,filename=path)
        except SyntaxError as e:
            if fix:
                fixed=safe_fixes(path,src)
                if fixed!=src:
                    write_text(path,fixed)
                    try:
                        ast.parse(fixed,filename=path)
                        issues.append(f"{path}:{e.lineno}: fixed artifacts; re-parse ok")
                        return issues
                    except SyntaxError as e2:
                        issues.append(f"{path}:{e2.lineno}: syntax still broken after fix")
                else:
                    issues.append(f"{path}:{e.lineno}: syntax error")
            else:
                issues.append(f"{path}:{e.lineno}: syntax error")
    except Exception as e:
        issues.append(f"{path}:0: read error: {e}")
    return issues

def scan_json(path,fix):
    issues=[]
    try:
        src=read_text(path)
        try:
            json.loads(src)
        except Exception as e:
            if fix:
                fixed=safe_fixes(path,src)
                try:
                    json.loads(fixed)
                    write_text(path,fixed); issues.append(f"{path}: fixed artifacts; parse ok")
                except Exception as e2:
                    issues.append(f"{path}: json parse still broken: {e2}")
            else:
                issues.append(f"{path}: json parse error: {e}")
    except Exception as e:
        issues.append(f"{path}:0: read error: {e}")
    return issues

def scan_yaml(path,fix):
    if not HAVE_YAML:
        return []
    issues=[]
    try:
        src=read_text(path)
        try:
            yaml.safe_load(src)
        except Exception as e:
            if fix:
                fixed=safe_fixes(path,src)
                try:
                    yaml.safe_load(fixed)
                    write_text(path,fixed); issues.append(f"{path}: fixed artifacts; parse ok")
                except Exception as e2:
                    issues.append(f"{path}: yaml parse still broken: {e2}")
            else:
                issues.append(f"{path}: yaml parse error: {e}")
    except Exception as e:
        issues.append(f"{path}:0: read error: {e}")
    return issues

BRACE_PAIRS={"(":")","[":"]","{":"}"}
def brace_ok(text):
    st=[]
    for ch in text:
        if ch in BRACE_PAIRS: st.append(BRACE_PAIRS[ch])
        elif ch in BRACE_PAIRS.values():
            if not st or st.pop()!=ch: return False
    return not st

def scan_js_like(path,fix):
    issues=[]
    try:
        src=read_text(path)
        if not brace_ok(src):
            if fix:
                fixed=safe_fixes(path,src)
                if brace_ok(fixed):
                    write_text(path,fixed); issues.append(f"{path}: fixed artifacts; braces ok")
                else:
                    issues.append(f"{path}: unbalanced braces")
            else:
                issues.append(f"{path}: unbalanced braces")
    except Exception as e:
        issues.append(f"{path}:0: read error: {e}")
    return issues

def should_skip(d,inc_venv,inc_node,extra):
    skips=list([".venv","node_modules","__pycache__","dist","build",".git",".idea",".vscode"])+list(extra or [])
    if inc_venv: skips=[s for s in skips if s!=".venv"]
    if inc_node: skips=[s for s in skips if s!="node_modules"]
    return any(s in d for s in skips)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--include-venv", action="store_true")
    ap.add_argument("--include-node", action="store_true")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--ban", default=",".join(DEFAULT_BAN))
    ap.add_argument("--skip", default="")
    ap.add_argument("--ext", default=".py,.json,.yaml,.yml,.js,.jsx,.ts,.tsx")
    args=ap.parse_args()

    root=os.path.abspath(args.root)
    ban=[b.strip() for b in args.ban.split(",") if b.strip()]
    extra=[s.strip() for s in args.skip.split(",") if s.strip()]
    exts=tuple(x.strip() for x in args.ext.split(",") if x.strip())

    issues=[]; total=0
    for dirpath, dirnames, filenames in os.walk(root):
        if should_skip(dirpath,args.include_venv,args.include_node,extra): continue
        for name in filenames:
            if not name.endswith(exts): continue
            p=os.path.join(dirpath,name); total+=1
            if name.endswith(".py"): issues.extend(scan_py(p,ban,args.fix))
            elif name.endswith(".json"): issues.extend(scan_json(p,args.fix))
            elif name.endswith(".yaml") or name.endswith(".yml"): issues.extend(scan_yaml(p,args.fix))
            else: issues.extend(scan_js_like(p,args.fix))

    if issues:
        for i in issues: print(i)
        print(f"SUMMARY: {len(issues)} issues across {total} files")
        sys.exit(1)
    print(f"SUMMARY: 0 issues across {total} files")

if __name__=="__main__":
    main()
