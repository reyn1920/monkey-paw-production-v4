#!/usr/bin/env python3
# Read and rewrite the file to fix any encoding issues
file_path = "backend/app.py"
with open(file_path, encoding="utf-8") as f:
    content = f.read()

# Create backup
with open("backend/app.py.backup", "w", encoding="utf-8") as f:
    f.write(content)

# Rewrite the original file
with open("backend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

# DEBUG_REMOVED: print("File rewritten successfully")
