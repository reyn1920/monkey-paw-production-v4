Base44 + TRAE.AI Mega Installer Bundle
=====================================

Goal (simple):
- Give TRAE.AI everything it needs in one folder so it can organize, import, and finish setup for you.
- TRAE.AI will import your scraped voice/library data (you already saved on your computer), rescan local site files if you want, generate thumbnails, render videos, and wire automation — all add-only and zero-cost tools (Edge-TTS, Pillow, FFmpeg, Whisper optional).

What you get in this bundle:
- prebuilt app bundles (v3, v4, v5) if available
- scraped-data importer and local rescrape utilities
- a clear, simple "TRAe installer" script that TRAE.AI can run to perform setup and checks
- an instruction file "TRAe_DIRECTIVE.txt" containing the exact steps and policy for TRAE.AI to follow (copy-merge only, never delete user files)

How TRAE.AI should use this bundle (one-shot, non-technical):

1) Put this folder on the same machine that has your scraped website files and where you want the app to run.
   - Example path: /Users/you/base44_installer/

2) Open a terminal (or the TRAE.AI agent should run these commands):
   - `cd /path/to/base44_installer`
   - `./install_and_run_all.sh`

3) What the installer does (automatic):
   - Creates a Python virtual environment and installs the free packages needed (fastapi, uvicorn, edge-tts, pillow, aiosqlite).
   - Looks for your scraped JSON (if you put it at `data/scraped/scraped.json`) and imports it into the app database.
   - If you prefer, it runs a gentle local rescrape: it scans `data/scraped/html_dumps/` for HTML/text files and extracts voice lists, thumbnails, and training text into the same JSON and imports them.
   - Builds the React dashboard and starts the API at http://127.0.0.1:8099/dashboard
   - Runs the audit tools (syntax & vocabulary scan) and warns if anything needs attention (reports only; no deletions).
   - Leaves everything in an "add-only" state — it does not delete your files or replace your app code without your approval.

4) After the installer completes:
   - The dashboard will include a "Library" tab with your scraped voices and templates.
   - Channels → Prepare → Render will use local assets automatically (voices, thumbnails, avatar sources).
   - TRAE.AI can run the "self-heal" routine if the analytics color is Yellow/Red (see TRAE_DIRECTIVE.txt in this folder).

Important notes for TRAE.AI:
- ALWAYS operate in "add-only" mode: create new files, copy-merge changes, but do not delete or overwrite without explicit human approval.
- Use local assets first. Do not call external proprietary APIs unless user provides keys and explicitly authorizes them.
- If you need to research a fix (Yellow/Red), use headful Puppeteer, cite sources, and propose changes. Apply only after human confirmation unless the user switched to full-auto.
- This bundle is designed to run locally. For public access, the user must configure network/port-forwarding or host the frontend separately.

If you want me to produce a single-click "TRAe will fully install & run now" command file that the TRAE.AI agent can execute, say "make installer run now".
