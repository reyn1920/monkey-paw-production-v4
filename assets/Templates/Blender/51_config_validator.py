#!/usr/bin/env python3
"""
Configuration File Validator
Validates JSON, YAML, TOML, .env, and docker-compose files for syntax errors.
"""

import json
import yaml
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import toml
except ImportError:
    toml = None


def validate_json_file(file_path: str) -> Tuple[bool, str]:
    """Validate JSON file syntax."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json.load(f)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"JSON Error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_yaml_file(file_path: str) -> Tuple[bool, str]:
    """Validate YAML file syntax."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        return True, "Valid YAML"
    except yaml.YAMLError as e:
        return False, f"YAML Error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_toml_file(file_path: str) -> Tuple[bool, str]:
    """Validate TOML file syntax."""
    if toml is None:
        return False, "TOML library not available"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            toml.load(f)
        return True, "Valid TOML"
    except toml.TomlDecodeError as e:
        return False, f"TOML Error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_env_file(file_path: str) -> Tuple[bool, str]:
    """Validate .env file syntax."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        issues = []
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                issues.append(f"Line {i}: Missing '=' in environment variable")
            else:
                key, value = line.split("=", 1)
                if not key.strip():
                    issues.append(f"Line {i}: Empty variable name")

        if issues:
            return False, "; ".join(issues)
        return True, "Valid .env file"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_docker_compose_file(file_path: str) -> Tuple[bool, str]:
    """Validate docker-compose file syntax."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            return False, "Docker-compose file must be a YAML object"

        if "version" not in data and "services" not in data:
            return False, "Missing 'version' or 'services' key"

        return True, "Valid docker-compose file"
    except yaml.YAMLError as e:
        return False, f"YAML Error in docker-compose: {e}"
    except Exception as e:
        return False, f"Error reading docker-compose file: {e}"


def find_config_files() -> Dict[str, List[str]]:
    """Find all configuration files in the project."""
    config_files = {"json": [], "yaml": [], "toml": [], "env": [], "docker-compose": []}

    exclude_dirs = {
        ".venv",
        "__pycache__",
        "node_modules",
        ".git",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }

    for file_path in Path(".").rglob("*"):
        if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
            continue

        if file_path.is_file():
            if file_path.suffix == ".json":
                config_files["json"].append(str(file_path))
            elif file_path.suffix in [".yaml", ".yml"]:
                if "docker-compose" in file_path.name or "compose" in file_path.name:
                    config_files["docker-compose"].append(str(file_path))
                else:
                    config_files["yaml"].append(str(file_path))
            elif file_path.suffix == ".toml":
                config_files["toml"].append(str(file_path))
            elif file_path.name.startswith(".env"):
                config_files["env"].append(str(file_path))

    return config_files


def main():
    """Main validation function."""
    print("🔍 Configuration File Validator")
    print("=" * 50)

    config_files = find_config_files()

    total_files = sum(len(files) for files in config_files.values())
    print(f"Found {total_files} configuration files:")
    for file_type, files in config_files.items():
        print(f"  {file_type.upper()}: {len(files)} files")

    print("\n" + "=" * 50)

    all_valid = True
    validation_results = {}

    # Validate JSON files
    if config_files["json"]:
        print("\n📄 Validating JSON files...")
        for file_path in config_files["json"]:
            is_valid, message = validate_json_file(file_path)
            validation_results[file_path] = (is_valid, message)
            status = "✅" if is_valid else "❌"
            print(f"  {status} {file_path}: {message}")
            if not is_valid:
                all_valid = False

    # Validate YAML files
    if config_files["yaml"]:
        print("\n📄 Validating YAML files...")
        for file_path in config_files["yaml"]:
            is_valid, message = validate_yaml_file(file_path)
            validation_results[file_path] = (is_valid, message)
            status = "✅" if is_valid else "❌"
            print(f"  {status} {file_path}: {message}")
            if not is_valid:
                all_valid = False

    # Validate TOML files
    if config_files["toml"]:
        print("\n📄 Validating TOML files...")
        for file_path in config_files["toml"]:
            is_valid, message = validate_toml_file(file_path)
            validation_results[file_path] = (is_valid, message)
            status = "✅" if is_valid else "❌"
            print(f"  {status} {file_path}: {message}")
            if not is_valid:
                all_valid = False

    # Validate .env files
    if config_files["env"]:
        print("\n📄 Validating .env files...")
        for file_path in config_files["env"]:
            is_valid, message = validate_env_file(file_path)
            validation_results[file_path] = (is_valid, message)
            status = "✅" if is_valid else "❌"
            print(f"  {status} {file_path}: {message}")
            if not is_valid:
                all_valid = False

    # Validate docker-compose files
    if config_files["docker-compose"]:
        print("\n🐳 Validating docker-compose files...")
        for file_path in config_files["docker-compose"]:
            is_valid, message = validate_docker_compose_file(file_path)
            validation_results[file_path] = (is_valid, message)
            status = "✅" if is_valid else "❌"
            print(f"  {status} {file_path}: {message}")
            if not is_valid:
                all_valid = False

    # Summary
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All configuration files are valid!")
        return 0
    else:
        print("⚠️  Some configuration files have issues!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
