#!/usr/bin/env python3
"""Validate the profile repository structure and generated SVG assets."""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "README.md", "profile.config.json", "SETUP.md",
    "assets/hero-banner.svg", "assets/systems-blueprint.svg", "assets/automation-loop.svg", "assets/live-metrics.svg",
    ".github/scripts/generate_assets.py", ".github/scripts/profile_bot.py", ".github/scripts/validate_profile.py",
    ".github/workflows/profile-bot.yml", ".github/workflows/quality-gate.yml", ".github/workflows/snake.yml", ".github/workflows/codeql.yml",
]
MARKERS = ["LIVE_OVERVIEW", "PUBLIC_REPOS", "ACTIVITY_FEED"]
FORBIDDEN = ["YOUR_USERNAME", "example.com/linkedin"]


def main() -> int:
    failures: list[str] = []
    for relative_path in REQUIRED:
        if not (ROOT / relative_path).exists():
            failures.append(f"Missing required file: {relative_path}")
    config = json.loads((ROOT / "profile.config.json").read_text(encoding="utf-8"))
    if config.get("username") != "IT24103496":
        failures.append("profile.config.json username must remain IT24103496 for Dasun's profile repository.")
    if config.get("display_name") != "Dasun Welianga":
        failures.append("profile.config.json display_name must identify Dasun Welianga.")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "Dasun Welianga" not in readme or "IT24103496" not in readme:
        failures.append("README must identify Dasun and his GitHub username.")
    for marker in MARKERS:
        if readme.count(f"<!-- {marker}_START -->") != 1 or readme.count(f"<!-- {marker}_END -->") != 1:
            failures.append(f"Invalid README marker pair: {marker}")
    for term in FORBIDDEN:
        if term in readme:
            failures.append(f"README contains unwanted placeholder reference: {term}")
    for svg in (ROOT / "assets").glob("*.svg"):
        try:
            ET.parse(svg)
        except ET.ParseError as exc:
            failures.append(f"Invalid SVG {svg.name}: {exc}")
    if failures:
        print("Profile validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Profile validation passed: identity, files, markers, configuration and SVG assets are healthy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
