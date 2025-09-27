#!/usr/bin/env python3
#!/usr/bin/env python3
# Read and rewrite the file to fix any encoding issues
with open("backend/app.py", encoding="utf-8") as f:
    content = f.read()

# Create backup
with open("backend/app.py.backup", "w", encoding="utf-8") as f:
    f.write(content)

# Rewrite the original file
with open("backend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("File rewritten successfully")
