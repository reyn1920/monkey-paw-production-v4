#!/bin/bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This helper is for macOS only." >&2; exit 1
fi

# === Customize (optional) ===
# Add extra app paths with AI_CODER_APPS, colon-separated:
#   AI_CODER_APPS="/Applications/BBEdit.app:/Applications/Obsidian.app" bash this.sh
EXTRA_APPS="${AI_CODER_APPS:-}"

OUT="/tmp/ai-coders-pppc.mobileconfig"

python3 - <<'PY' "$OUT" "$EXTRA_APPS"
import os, sys, plistlib, subprocess, uuid, shlex, pathlib

out = sys.argv[1]
extra = sys.argv[2]

# Common AI/dev editors & terminals (add more as desired)
CANDIDATES = [
    "/Applications/Windsurf.app",
    "/Applications/Cursor.app",
    "/Applications/Visual Studio Code.app",
    "/Applications/IntelliJ IDEA.app",
    "/Applications/PyCharm.app",
    "/Applications/WebStorm.app",
    "/Applications/CLion.app",
    "/Applications/Rider.app",
    "/Applications/GoLand.app",
    "/Applications/iTerm.app",
    "/Applications/iTerm2.app",
    "/System/Applications/Utilities/Terminal.app",
]
if extra:
    CANDIDATES.extend([p for p in extra.split(":") if p])

def exists(p): return os.path.exists(p)
def bundle_id(app):
    info = os.path.join(app, "Contents", "Info.plist")
    try:
        with open(info, "rb") as f:
            d = plistlib.load(f)
        return d.get("CFBundleIdentifier")
    except Exception:
        return None

def code_req(app):
    try:
        out = subprocess.check_output(["codesign", "-dr", "-", app], stderr=subprocess.STDOUT)
        txt = out.decode("utf-8","ignore")
        if "designated => " in txt:
            return txt.split("designated => ",1)[1].strip()
    except Exception:
        pass
    return None

apps = []
for p in CANDIDATES:
    if exists(p):
        bid = bundle_id(p)
        cr  = code_req(p)
        if bid and cr:
            apps.append({"path": p, "bid": bid, "cr": cr})

if not apps:
    print("No known editors found. Set AI_CODER_APPS to add paths.", file=sys.stderr)
    sys.exit(1)

def allow_entry(app):
    return {
        "Identifier": app["bid"],
        "IdentifierType": "bundleID",
        "CodeRequirement": app["cr"],
        "Authorization": "Allow",
    }

# TCC services we can pre-approve via PPPC
services = {
    "SystemPolicyAllFiles": [],           # Full Disk Access
    "SystemPolicyDesktopFolder": [],
    "SystemPolicyDownloadsFolder": [],
    "SystemPolicyDocumentsFolder": [],
    "SystemPolicyNetworkVolumes": [],
    "SystemPolicyRemovableVolumes": [],
    "Accessibility": [],                  # Assistive access / UI scripting
    "AppleEvents": [],                    # Automation
}

# Common AppleEvents receivers these tools may drive
AE_RECEIVERS = [
    ("com.apple.finder", "bundleID"),
    ("com.apple.systemevents", "bundleID"),
    ("com.apple.Terminal", "bundleID"),
    ("com.googlecode.iterm2", "bundleID"),  # iTerm2
]

for a in apps:
    e = allow_entry(a)
    for key in ("SystemPolicyAllFiles","SystemPolicyDesktopFolder","SystemPolicyDownloadsFolder",
                "SystemPolicyDocumentsFolder","SystemPolicyNetworkVolumes","SystemPolicyRemovableVolumes",
                "Accessibility"):
        services[key].append(e.copy())
    # AppleEvents needs receiver per target
    for recv, rtype in AE_RECEIVERS:
        ae = e.copy()
        ae["AEReceiverIdentifier"] = recv
        ae["AEReceiverIdentifierType"] = rtype
        services["AppleEvents"].append(ae)

# Inner TCC payload
tcc_uuid = str(uuid.uuid4()).upper()
tcc_payload = {
    "PayloadType": "com.apple.TCC.configuration-profile-policy",
    "PayloadUUID": tcc_uuid,
    "PayloadIdentifier": "local.pppc.ai-coders."+tcc_uuid.lower(),
    "PayloadVersion": 1,
    "PayloadDisplayName": "AI Coders – Privacy Permissions (PPPC)",
    "PayloadDescription": "Pre-approve FDA/Accessibility/Automation + folders for AI/dev editors.",
    "PayloadOrganization": "Local Admin",
    "Services": services,
}

# Outer configuration profile
cfg_uuid = str(uuid.uuid4()).upper()
profile = {
    "PayloadType": "Configuration",
    "PayloadVersion": 1,
    "PayloadIdentifier": "local.profile.ai-coders."+cfg_uuid.lower(),
    "PayloadUUID": cfg_uuid,
    "PayloadDisplayName": "AI Coders – Privacy Bundle",
    "PayloadDescription": "Installs PPPC for AI/dev editors. Some items still require user approval.",
    "PayloadOrganization": "Local Admin",
    "PayloadContent": [ tcc_payload ],
}

with open(out, "wb") as f:
    plistlib.dump(profile, f, sort_keys=False)
print(f"Wrote {out}")
PY

echo "Attempting to install the profile (you may be prompted)…"
if command -v profiles >/dev/null 2>&1; then
  if profiles install -type configuration -path "$OUT" >/dev/null 2>&1; then
    echo "Installed via: profiles install -type configuration -path $OUT"
  elif profiles -I -F "$OUT" >/dev/null 2>&1; then
    echo "Installed via: profiles -I -F $OUT"
  else
    echo "Could not auto-install. Opening the profile so you can confirm it in System Settings…"
    open "$OUT"
  fi
else
  echo "'profiles' tool not found. Opening the profile for manual install…"
  open "$OUT"
fi

# Enable Developer Tools access (lets non-admins use lldb/instruments; optional)
if command -v /usr/sbin/DevToolsSecurity >/dev/null 2>&1; then
  sudo /usr/sbin/DevToolsSecurity -enable || true
fi

# Open remaining Privacy panes that still require manual approval on user Macs
open_pane() { open "$1" >/dev/null 2>&1 || true; sleep 0.5; }
PREFS=(
  "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"  # Screen Recording
  "x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone"
  "x-apple.systempreferences:com.apple.preference.security?Privacy_Camera"
  "x-apple.systempreferences:com.apple.preference.security?Privacy_Bluetooth"
  "x-apple.systempreferences:com.apple.preference.security?Privacy_AppManagement"  # 'access data from other apps'
)
for u in "${PREFS[@]}"; do open_pane "$u"; done

# Friendly checklist
osascript <<'OSA' >/dev/null 2>&1 || true
display dialog "Finishing steps (macOS requires manual approval here):\n\n• Screen Recording – enable for your editors (Windsurf, Cursor, VS Code, JetBrains, Terminal/iTerm2)\n• Microphone/Camera – enable if you use voice/video features\n• App Management – allow apps to access data from other apps if prompted\n\nTip: If you manage Macs via MDM, push the generated /tmp/ai-coders-pppc.mobileconfig from the server for zero-click deployment on supervised devices." buttons {"OK"} default button 1 with icon note
OSA

echo "All set. For MDM fleets, upload/push: $OUT"
