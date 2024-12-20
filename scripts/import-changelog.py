import re
from datetime import datetime
import os


def parse_version_block(text):
    """Parse a version block from the changelog text."""
    # Regular expression to match version and date
    version_pattern = r"Version (\d+\.\d+\.\d+) \((.*?)\)"
    version_match = re.match(version_pattern, text.split("\n")[0])

    if not version_match:
        return None

    version = version_match.group(1)
    date_str = version_match.group(2)

    # Parse the date
    try:
        release_date = datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        print(f"Warning: Could not parse date for version {version}")
        release_date = "unknown"

    # Extract changes
    changes = []
    for line in text.split("\n")[2:]:  # Skip version line and dashes
        line = line.strip()
        if line and line.startswith("*"):
            changes.append(line)

    return {"version": version, "date": release_date, "changes": changes}


def generate_markdown_file(version_info):
    """Generate a markdown file for a version."""
    content = [
        "---",
        "title: Kanboard " + version_info["version"],
        "release_date: " + version_info["date"],
        "release_version: v" + version_info["version"],
        "release_type: kanboard",
        "---\n",
    ]

    # Add changes
    content.extend(version_info["changes"])

    return "\n".join(content)


def split_changelog(changelog_text):
    """Split the changelog into individual version blocks."""
    # Split on version headers
    version_blocks = re.split(r"\nVersion \d+\.\d+\.\d+", changelog_text)
    version_blocks = [block for block in version_blocks if block.strip()]

    # Reconstruct the version headers with the content
    versions = []
    version_headers = re.findall(r"Version \d+\.\d+\.\d+.*?\n", changelog_text)

    for i, block in enumerate(version_blocks):
        if i < len(version_headers):
            versions.append(version_headers[i] + block)

    return versions


def main():
    # Create output directory if it doesn't exist
    output_dir = "releases/kanboard"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open("../kanboard/ChangeLog") as f:
        changelog_text = f.read()

    # Split the changelog into version blocks
    version_blocks = split_changelog(changelog_text)

    # Process each version block
    for block in version_blocks:
        version_info = parse_version_block(block)
        if version_info:
            # Generate filename
            filename = f"v{version_info['version']}.md"
            filepath = os.path.join(output_dir, filename)

            # Generate and write the markdown content
            content = generate_markdown_file(version_info)
            with open(filepath, "w") as f:
                f.write(content)

            print(f"Generated {filename}")


if __name__ == "__main__":
    main()
