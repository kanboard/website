import json
import sys
import re
from typing import Any


def check_alphabetical_order(data: dict, path: str = "") -> list[str]:
    """
    Check if a dictionary is ordered alphabetically by key and report any violations.

    Args:
        data: Dict or any other type to check
        path: String representing the current path in the dictionary (for nested dicts)

    Returns:
        List of strings with the violations found
    """
    violations = []

    if isinstance(data, dict):
        keys = list(data.keys())

        for i in range(len(keys) - 1):
            if keys[i].lower() > keys[i + 1].lower():
                current_path = f"{path}/" if path else ""
                violation = f"Violation at {current_path}: '{keys[i]}' should come after '{keys[i + 1]}'"
                violations.append(violation)

        for key, value in data.items():
            current_path = f"{path}/{key}" if path else key
            violations.extend(check_alphabetical_order(value, current_path))

    return violations


def is_valid_plugin_structure(plugin: dict[str, Any]) -> tuple[bool, str]:
    """
    Validate the structure of a plugin configuration.
    Returns a tuple of (is_valid: bool, error_message: str)
    """
    fields = {
        "author": {"type": str},
        "compatible_version": {"type": str, "regex": r"^(>=|<=|>|<)\d+\.\d+\.\d+$"},
        "description": {"type": str},
        "download": {"type": str, "regex": r"^https?://.+$"},
        "has_hooks": {"type": bool},
        "has_overrides": {"type": bool},
        "has_schema": {"type": bool},
        "homepage": {"type": str, "regex": r"^https?://.+$"},
        "is_type": {
            "type": str,
            "values": ["plugin", "action", "theme", "connector", "multi"],
        },
        "last_updated": {"type": str, "regex": r"^\d{4}-\d{2}-\d{2}$"},
        "license": {"type": str},
        "readme": {"type": str, "regex": r"^https?://.+$"},
        "remote_install": {"type": bool},
        "title": {"type": str},
        "version": {"type": str},
    }

    for field, rules in fields.items():
        # Check if field exists
        if field not in plugin:
            return False, f'Field "{field}" is missing.'

        # Check type
        expected_type = rules["type"]
        if not isinstance(plugin[field], expected_type):
            return (
                False,
                f'Field "{field}" should be of type "{expected_type.__name__}".',
            )

        # Check regex pattern if specified
        if "regex" in rules and not re.match(rules["regex"], plugin[field]):
            return (
                False,
                f'Field "{field}" with value "{plugin[field]}" does not match the required pattern {rules["regex"]}',
            )

        # Check allowed values if specified
        if "values" in rules and plugin[field] not in rules["values"]:
            return False, f'Field "{field}" has an invalid value.'

    return True, ""


def main():
    input_file = "plugins.json"
    try:
        with open(input_file) as f:
            plugins = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing {input_file}: {str(e)}", file=sys.stderr)
        sys.exit(1)

    violations = check_alphabetical_order(plugins)
    is_ordered = len(violations) == 0

    if not is_ordered:
        print("Dictionary is not alphabetically ordered:")
        for violation in violations:
            print(f"- {violation}")
        sys.exit(1)

    for plugin_name, plugin_data in plugins.items():
        is_valid, error_msg = is_valid_plugin_structure(plugin_data)
        if not is_valid:
            print(
                f'Plugin "{plugin_name}" has an invalid schema: {error_msg}',
                file=sys.stderr,
            )
            sys.exit(1)

    print("All plugins are in alphabetical order and have a valid schema.")


if __name__ == "__main__":
    main()
