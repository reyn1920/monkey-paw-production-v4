#!/bin/zsh
set -e
mkdir -p reports
zsh tools/doctor/inventory_tree.zsh .
echo "# Missing Info (quick pass)" > reports/MISSING.md
echo "- Inventory captured in reports/INVENTORY.txt" >> reports/MISSING.md
