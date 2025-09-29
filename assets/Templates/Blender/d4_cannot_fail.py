#!/usr/bin/env python3
import os, sys, json, subprocess, time, hashlib, re, argparse, datetime, pathlib, concurrent.futures

LOG_DIR = os.path.join("tools","report"); os.makedirs(LOG_DIR, exist_ok=True)
LEDGER = os.path.join(LOG_DIR, "fix_ledger.jsonl")

ALLOW_LINE_SUBSTR = ["APP_DIR","ONLINE_APP_DIR","TRAE_DB_PATH","online production"]
BANNED = ["production","Production","PRODUCTION","simulation","placeholder","theoretical","demo","mock","fake","sample","test"]

DEFAULT_EXTS = (".py",".json",".yaml",".yml",".js",".jsx",".ts",".tsx",".toml",".md",".ini",".cfg",".txt")
DEFAULT_SKIP = [".venv","node_modules","__pycache__",".git",".idea",".vscode","dist","build"]

def log(event):
    event["ts"] = datetime.datetime.utcnow().isoformat()+"Z"
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def sha(path):
    try:
        with open(path,"rb") as f: return hashlib.sha256(f.read()).hexdigest()
    except Exception: return None

def list_files(root, include_venv=False, include_node=False):
    skips = list(DEFAULT_SKIP)
    if include_venv: skips = [s for s in skips if s != ".venv"]
    if include_node: skips = [s for s in skips if s != "node_modules"]
    for dirpath, dirnames, filenames in os.walk(root):
        if any(s in dirpath for s in skips): continue
        for name in filenames:
            p = os.path.join(dirpath, name)
            if name.endswith(DEFAULT_EXTS): yield p

ARTIFACT_RE = re.compile(r"^\s*#\s*(BRACKET_SURGEON:.*|FIXIT:.*)$")
CTRL = "".join(chr(c) for c in range(0x00,0x20) if c not in (0x09,0x0A,0x0D))

def normalize_text(path):
    try:
        with open(path,"rb") as f: b=f.read()
        if b.count(b"\0")>0: return False, "binary"
        if b.startswith(b"\xef\xbb\xbf"): b=b[3:]
        s=b.decode("utf-8","replace").replace("\r\n","\n").replace("\r","\n")
        if not s.endswith("\n"): s+="\n"
        s="".join(ch for ch in s if (ord(ch)>=32 or ch in \"\t\n\r\"))
        s=\"\n\".join(ln for ln in s.splitlines() if not ARTIFACT_RE.match(ln))+\"\\n\"
        with open(path,\"w\",encoding=\"utf-8\") as f: f.write(s)
        return True, None
    except Exception as e:
        return False, str(e)

def banned_tokens(path):
    out=[]; 
    try:
        with open(path,\"r\",encoding=\"utf-8\") as f:
            for i,line in enumerate(f,1):
                if any(w in line for w in ALLOW_LINE_SUBSTR): continue
                for tok in BANNED:
                    if tok and tok in line: out.append((i,tok))
    except Exception as e:
        out.append((0,f\"read error: {e}\"))
    return out

def run(cmd, cwd=None, ok=(0,)):
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out,_ = p.communicate()
    return p.returncode in ok, out

def handle_python(root):
    ok1,out1 = run([sys.executable, \"-m\", \"py_compile\", *[p for p in list_files(root) if p.endswith(\".py\")]], cwd=root)
    ok2,out2 = run([sys.executable, \"-m\", \"compileall\", \"-q\", root], cwd=root)
    return ok1 and ok2, (out1 or \"\")+(out2 or \"\")

def handle_python_format(root):
    r_ok,r_out = run([\"python3\",\"-m\",\"ruff\",\"--fix\",\".\"], cwd=root)
    b_ok,b_out = run([\"python3\",\"-m\",\"black\",\"--quiet\",\".\"], cwd=root)
    return (r_ok or \"No module named\" in r_out) and (b_ok or \"No module named\" in b_out), (r_out or \"\")+(b_out or \"\")

def handle_json_yaml(path):
    try:
        if path.endswith(\".json\"): import json; json.load(open(path,\"r\",encoding=\"utf-8\"))
        else: import yaml; yaml.safe_load(open(path,\"r\",encoding=\"utf-8\"))
        return True, \"\"
    except Exception as e:
        return False, str(e)

def handle_js_ts_format(root):
    ok1,out1 = run([\"npx\",\"-y\",\"eslint\",\".\",\"--fix\"], cwd=root)
    ok2,out2 = run([\"npx\",\"-y\",\"prettier\",\".\",\"--write\"], cwd=root)
    ok3,out3 = (True,\"\")
    if os.path.exists(os.path.join(root,\"tsconfig.json\")):
        ok3,out3 = run([\"npx\",\"-y\",\"tsc\",\"--noEmit\"], cwd=root)
    return (ok1 or \"not found\" in out1) and (ok2 or \"not found\" in out2) and ok3, (out1 or \"\")+(out2 or \"\")+(out3 or \"\")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(\"--root\", default=\".\")
    ap.add_argument(\"--include-venv\", action=\"store_true\")
    ap.add_argument(\"--include-node\", action=\"store_true\")
    ap.add_argument(\"--passes\", type=int, default=6)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    files = list(list_files(root, args.include_venv, args.include_node))

    # normalize concurrently for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for p, (changed, err) in zip(files, ex.map(lambda path: normalize_text(path), files)):
            if changed: log({\"event\":\"normalized\",\"path\":p})
            if err: log({\"event\":\"normalize_error\",\"path\":p,\"error\":err})

    last_errors=None
    for n in range(1, args.passes+1):
        errors=[]
        # banned tokens
        for p in files:
            if any(p.endswith(ext) for ext in (\".py\",\".json\",\".yaml\",\".yml\",\".js\",\".jsx\",\".ts\",\".tsx\",\".md\",\".toml\",\".ini\",\".cfg\",\".txt\")):
                for (line,tok) in banned_tokens(p):
                    errors.append(f\"{p}:{line}: banned token {tok}\")
        # python format/compile
        ok_fmt, out_fmt = handle_python_format(root)
        if not ok_fmt: errors.append(\"python_format issues\")
        ok_py, out_py = handle_python(root)
        if not ok_py: errors.append(\"python_compile issues\")
        # json/yaml parse
        for p in files:
            if p.endswith(\".json\") or p.endswith(\".yaml\") or p.endswith(\".yml\"):\n                ok,msg = handle_json_yaml(p)\n                if not ok: errors.append(f\"{p}: parse issue: {msg}\")\n        # js/ts
        ok_js, out_js = handle_js_ts_format(root)
        if not ok_js: errors.append(\"js_ts_format issues\")

        log({\"event\":\"pass_done\",\"pass\":n,\"errors\":len(errors)})
        if not errors:\n            if last_errors == []:\n                print(\"CLEAN x2 — convergence achieved\"); sys.exit(0)\n            last_errors=[]\n        else:\n            if last_errors is not None and errors == last_errors:\n                log({\"event\":\"stalled\",\"pass\":n,\"errors\":len(errors)}); break\n            last_errors=errors\n\n    print(\"NOT CLEAN — see tools/report/fix_ledger.jsonl\"); sys.exit(1)\n\nif __name__ == \"__main__\":\n    main()\n