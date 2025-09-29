#!/usr/bin/env python3
#!/usr/bin/env python3
import sys

sys.path.append(".")

import traceback

from app.dashboard import DashboardApp

try:
    app = DashboardApp()
    print("App created successfully")
    print('Routes with "action" in them=')
    action_routes = [
        rule for rule in app.app.url_map.iter_rules() if "action" in rule.rule
    ]
    if action_routes:
        for rule in action_routes:
            print(f"{rule.rule} -> {rule.endpoint}")
    else:
        print('No routes with "action" found')

    print("\\nAll routes=")
    for rule in app.app.url_map.iter_rules():
        print(f"{rule.rule} -> {rule.endpoint}")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
