#!/bin/zsh
set -e
INS=${1:-'artifacts/staging/*.txt'}
OUT=${2:-'artifacts/published/book.epub'}
python3 tools/exporters/book_epub/build_epub.py "$INS" "$OUT"
