#!/usr/bin/env python3
"""
Deep-search the repository for URLs and build a downloads inventory.

Features:
- Recursively scans for http/https URLs in text-like files
- Skips development stacks and generated folders by default
- Performs HEAD requests to fetch content-type and size when possible
- Outputs CSV and JSON inventories under out/audit_downloads_<timestamp>/
- Optional: --download to fetch missing items into downloads/
- Safe by default: inventory-only if --download not provided

Usage:
  python3 scripts/deepsearch_downloads.py [--download] [--timeout=10] [--max-head=200]

Notes:
- Exclusion list is designed to avoid dev stacks and generated content.
- Respects free-only policy; no paid services used.
"""
import os, re, sys, time, json, csv, hashlib, argparse
from pathlib import Path
from typing import Iterable, Iterator, Tuple, Dict, Any
import mimetypes

try:
    import requests
except Exception:
    requests = None  # We'll fallback to urllib if needed

import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'out'
DOWNLOADS_DIR = ROOT / 'downloads'

DEFAULT_EXCLUDES = [
    '.git', '.idea', '.DS_Store',
    '.venv', '.venv_monkeypawv4',
    'node_modules', 'dist', 'build',
    'downloads', 'out/audit_downloads_*',
    # Generated/large caches:
    'artifacts/staging', 'artifacts/published',
    # Tooling and editor config
    '.vscode', 'tools/project-doctor',
]

# Treat as binary and skip content parse if extension in this set
BINARY_EXTS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico', '.heic', '.heif',
    '.mp4', '.mov', '.mkv', '.avi', '.mp3', '.wav', '.aac', '.flac', '.aiff',
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.pdf', '.ppt', '.pptx', '.doc', '.docx', '.xls', '.xlsx', '.parquet'
}

URL_RE = re.compile(r'\bhttps?://[\w\-\./%#?=&:+,~]+', re.IGNORECASE)


def is_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    for pat in DEFAULT_EXCLUDES:
        if '*' in pat or '?' in pat:
            # glob-like
            if Path(rel).match(pat):
                return True
        else:
            # prefix match on directory path
            if rel == pat or rel.startswith(pat.rstrip('/') + '/'):
                return True
    return False


def iter_files(base: Path) -> Iterator[Path]:
    for dirpath, dirnames, filenames in os.walk(base):
        # Prune excluded directories early
        pruned = []
        for d in list(dirnames):
            full = Path(dirpath) / d
            if is_excluded(full):
                pruned.append(d)
        for d in pruned:
            dirnames.remove(d)
        for f in filenames:
            p = Path(dirpath) / f
            if is_excluded(p):
                continue
            yield p


def sniff_text(p: Path, max_bytes: int = 1_000_000) -> str:
    try:
        if p.suffix.lower() in BINARY_EXTS:
            return ''
        with open(p, 'rb') as fh:
            data = fh.read(max_bytes)
        # Heuristic: if null bytes present, treat as binary
        if b'\x00' in data:
            return ''
        return data.decode('utf-8', errors='ignore')
    except Exception:
        return ''


def find_urls_in_text(txt: str) -> Iterable[str]:
    for m in URL_RE.finditer(txt):
        yield m.group(0)


def head_info(url: str, timeout: int = 10) -> Tuple[str, int]:
    ctype, size = '', -1
    # Prefer requests if available
    if requests is not None:
        try:
            r = requests.head(url, timeout=timeout, allow_redirects=True)
            ctype = r.headers.get('Content-Type', '')
            clen = r.headers.get('Content-Length')
            if clen and clen.isdigit():
                size = int(clen)
            return ctype, size
        except Exception:
            pass
    # Fallback to urllib
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ctype = resp.headers.get('Content-Type', '')
            try:
                size = int(resp.headers.get('Content-Length', '-1'))
            except Exception:
                size = -1
    except Exception:
        pass
    return ctype, size


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path, timeout: int = 20) -> Tuple[bool, str]:
    try:
        if requests is not None:
            with requests.get(url, timeout=timeout, stream=True) as r:
                r.raise_for_status()
                with open(dest, 'wb') as fh:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            fh.write(chunk)
            return True, ''
        else:
            with urllib.request.urlopen(url, timeout=timeout) as resp, open(dest, 'wb') as fh:
                fh.write(resp.read())
            return True, ''
    except Exception as e:
        return False, str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--download', action='store_true', help='Also download missing items into downloads/')
    ap.add_argument('--timeout', type=int, default=10)
    ap.add_argument('--max-head', type=int, default=200, help='Max URLs to HEAD for metadata (to limit external requests)')
    args = ap.parse_args()

    ts = time.strftime('%Y%m%d-%H%M%S')
    audit_dir = OUT_DIR / f'audit_downloads_{ts}'
    ensure_dir(audit_dir)
    ensure_dir(DOWNLOADS_DIR)

    seen_urls = {}
    url_rows = []
    total_urls = 0

    print('[info] Scanning files...')
    for p in iter_files(ROOT):
        rel = p.relative_to(ROOT).as_posix()
        txt = sniff_text(p)
        if not txt:
            continue
        for url in find_urls_in_text(txt):
            total_urls += 1
            h = sha1(url)
            if h not in seen_urls:
                seen_urls[h] = {'url': url, 'count': 0, 'files': set()}
            seen_urls[h]['count'] += 1
            seen_urls[h]['files'].add(rel)

    print(f'[info] Unique URLs found: {len(seen_urls)} (from {total_urls} mentions)')

    # HEAD info for top N URLs by mention count
    print('[info] Fetching HEAD metadata...')
    top_items = sorted(seen_urls.items(), key=lambda kv: kv[1]['count'], reverse=True)
    head_checked = 0
    for h, meta in top_items:
        if head_checked >= args.max_head:
            break
        ctype, size = head_info(meta['url'], timeout=args.timeout)
        meta['content_type'] = ctype
        meta['content_length'] = size
        head_checked += 1

    # Build rows and write outputs
    for h, meta in top_items:
        files = sorted(list(meta['files']))
        row = {
            'url': meta['url'],
            'mentions': meta['count'],
            'content_type': meta.get('content_type', ''),
            'content_length': meta.get('content_length', -1),
            'files': ';'.join(files),
        }
        url_rows.append(row)

    csv_path = audit_dir / 'downloads_inventory.csv'
    json_path = audit_dir / 'downloads_inventory.json'

    with open(csv_path, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['url','mentions','content_type','content_length','files'])
        w.writeheader()
        for r in url_rows:
            w.writerow(r)

    with open(json_path, 'w') as fh:
        json.dump(url_rows, fh, indent=2)

    print(f'[ok] Wrote inventory: {csv_path} ({len(url_rows)} rows)')

    if args.download:
        print('[info] Downloading missing items to downloads/...')
        for r in url_rows:
            url = r['url']
            # Derive filename
            name = sha1(url)[:16]
            ext = mimetypes.guess_extension(r.get('content_type') or '') or ''
            dest = DOWNLOADS_DIR / f'{name}{ext}'
            if dest.exists() and dest.stat().st_size > 0:
                print(f'  [skip] exists {dest.name}')
                continue
            ok, err = download_file(url, dest)
            if ok:
                print(f'  [dl] {url} -> {dest.name}')
            else:
                print(f'  [err] {url}: {err}')

if __name__ == '__main__':
    main()
