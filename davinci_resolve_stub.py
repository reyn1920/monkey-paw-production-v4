# Example structure for DaVinci Resolve scripting (Python). Run inside Resolve's Scripts folder.
try:
    import DaVinciResolveScript as dvr
except Exception as e:
    print("Resolve scripting not available in this environment:", e)
    raise SystemExit(0)

resolve = dvr.scriptapp("Resolve")
pm = resolve.GetProjectManager()
proj = pm.GetCurrentProject()
if not proj:
    print("Open a project first"); raise SystemExit(0)
tl = proj.GetCurrentTimeline()
print("Timeline:", tl.GetName() if tl else "None")
