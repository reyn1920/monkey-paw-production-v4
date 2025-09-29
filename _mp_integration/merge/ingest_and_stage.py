# Placeholder for ingestion script
# This script will copy matched folders from import_paths into a timestamped staging area.
# No deletions are performed.

import os
import shutil
import json
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'merge_config.json')

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

stage_dir = os.path.join(os.path.dirname(__file__), '..', 'staging', datetime.now().strftime('%Y%m%d_%H%M%S'))
os.makedirs(stage_dir, exist_ok=True)

for import_path in config['import_paths']:
    if os.path.exists(import_path):
        for root, dirs, files in os.walk(import_path):
            for name in dirs:
                if any(f in name for f in config['name_filters']):
                    src = os.path.join(root, name)
                    dst = os.path.join(stage_dir, name)
                    if not os.path.exists(dst):
                        shutil.copytree(src, dst)
                        print(f'Copied {src} to {dst}')
