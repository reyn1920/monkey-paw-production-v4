#!/usr/bin/env python3
"""
Extract unique file paths from paste_content.txt to understand scope of fixes needed.
"""

import json
from collections import defaultdict


def extract_files_from_paste():
    """Extract all unique files and their error counts from paste_content.txt"""
    file_errors = defaultdict(list)
    unique_files = set()

    try:
        with open("paste_content.txt", encoding="utf-8") as f:
            content = f.read()

        # Parse JSON array
        try:
            diagnostics = json.loads(content)
            print(f"Found {len(diagnostics)} diagnostic entries")

            for diagnostic in diagnostics:
                if "resource" in diagnostic:
                    file_path = diagnostic["resource"]
                    # Extract relative path
                    if "/online production/" in file_path:
                        rel_path = file_path.split("/online production/")[-1]
                        unique_files.add(rel_path)

                        error_info = {
                            "line": diagnostic.get("startLineNumber", 0),
                            "message": diagnostic.get("message", ""),
                            "severity": diagnostic.get("severity", 0),
                        }
                        file_errors[rel_path].append(error_info)

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None, None

    except FileNotFoundError:
        print("paste_content.txt not found")
        return None, None

    return sorted(unique_files), dict(file_errors)


def categorize_files(files):
    """Categorize files by type and priority"""
    categories = {
        "python_core": [],
        "python_agents": [],
        "python_routers": [],
        "python_other": [],
        "javascript": [],
        "other": [],
    }

    for file_path in files:
        if file_path.endswith(".py"):
            if "agents/" in file_path:
                categories["python_agents"].append(file_path)
            elif "routers/" in file_path:
                categories["python_routers"].append(file_path)
            elif any(
                core in file_path
                for core in ["api_security", "autonomous_decision", "main", "app"]
            ):
                categories["python_core"].append(file_path)
            else:
                categories["python_other"].append(file_path)
        elif file_path.endswith(".js"):
            categories["javascript"].append(file_path)
        else:
            categories["other"].append(file_path)

    return categories


def main():
    # DEBUG_REMOVED: print("Extracting files from paste_content.txt...")
    files, file_errors = extract_files_from_paste()

    if files is None or file_errors is None:
        return

    print(f"\nFound {len(files)} unique files with errors:")

    categories = categorize_files(files)

    for category, file_list in categories.items():
        if file_list:
            print(f"\n{category.upper()} ({len(file_list)} files):")
            for file_path in file_list:
                error_count = len(file_errors.get(file_path, []))
                print(f"  - {file_path} ({error_count} errors)")

    # Show most problematic files
    print("\nMOST PROBLEMATIC FILES (>20 errors):")
    for file_path, errors in file_errors.items():
        if len(errors) > 20:
            print(f"  - {file_path}: {len(errors)} errors")

    # Save detailed report
    with open("file_error_report.json", "w") as f:
        json.dump(
            {
                "total_files": len(files),
                "categories": categories,
                "file_errors": file_errors,
            },
            f,
            indent=2,
        )


# DEBUG_REMOVED: print("\nDetailed report saved to file_error_report.json")


if __name__ == "__main__":
    main()
