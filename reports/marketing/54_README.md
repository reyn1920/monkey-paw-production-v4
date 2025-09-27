# Base44 Combined Bundle — TRAE.AI + App + React Dashboard (Add‑Only, Zero‑Cost)

Includes:
- FastAPI backend (SQLite) with health, state toggles, streams, static serving
- Ethical headful Puppeteer scaffold
- Rule‑1 vocabulary guard + Python syntax audit
- Seeds and utilities
- React dashboard (Vite + Tailwind) for friendly control: big toggles, visuals
- Avatars pack: Linly Talker (default) + Talking Heads (optional), voice routes, proofs
- TRAE.AI directives to self‑install and integrate without removals

Quick start (macOS):
```bash
unzip base44_combined_bundle.zip -d ~/base44_combined && cd ~/base44_combined
./setup/setup_mac.sh
./setup/setup_node.sh
# build dashboard
cd frontend && npm install && npm run build && cd ..
# launch API (serves /dashboard)
./scripts/launch_all.sh
python -m webbrowser http://127.0.0.1:8099/dashboard
```

Remote access options (free):
- **Local network:** use your Mac IP: `http://<your_lan_ip>:8099/dashboard`
- **Static dashboard:** you can deploy `frontend/dist` on a free static host (e.g., GitHub Pages) and point it to your API URL.
- **Router port‑forwarding:** forward 8099 to your machine (security caution).
