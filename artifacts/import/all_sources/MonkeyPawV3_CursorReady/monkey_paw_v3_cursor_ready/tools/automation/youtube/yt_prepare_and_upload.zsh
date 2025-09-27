#!/bin/zsh
set -e
SRC=${1:-artifacts/staging/draft_youtube.txt}
python3 tools/automation/youtube/prepare_youtube_assets.py "$SRC"
python3 tools/automation/youtube/make_thumbnail.py "$SRC" || true
python3 tools/automation/youtube/upload_youtube.py "${SRC%.txt}.meta.json"
