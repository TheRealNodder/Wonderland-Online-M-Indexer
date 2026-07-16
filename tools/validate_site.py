#!/usr/bin/env python3
"""Validate the generated static Wonderland M Indexer payload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_SECTIONS = {
    "items", "monsters", "drops", "maps", "step_afk_locations", "visible_spawns",
    "dungeons", "npcs", "shops", "quests", "quest_chains", "quest_rewards",
    "map_requirements", "portals_teleports", "compounds", "localization", "evidence",
    "unresolved", "verification_issues",
}
CONFIDENCE = {
    "direct_client_record", "direct_localization_match", "direct_asset_relationship",
    "strong_relationship", "inferred_relationship", "name_match_only", "unresolved",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, default=Path.cwd())
    args = parser.parse_args()
    site = args.site_dir.resolve()
    runtime_path = site / "data" / "runtime-index.json"
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    failures: list[str] = []

    missing = sorted(REQUIRED_SECTIONS - runtime.keys())
    if missing:
        failures.append(f"Missing sections: {', '.join(missing)}")
    if runtime.get("meta", {}).get("character_data_included") is not False:
        failures.append("character_data_included must be false")
    for section in REQUIRED_SECTIONS:
        value = runtime.get(section)
        if not isinstance(value, list):
            failures.append(f"Section {section} is not an array")

    item_ids = [row.get("item_id") for row in runtime.get("items", [])]
    if len(item_ids) != len(set(item_ids)):
        failures.append("Duplicate item IDs in site payload")
    map_ids = [row.get("map_id") for row in runtime.get("maps", [])]
    if len(map_ids) != len(set(map_ids)):
        failures.append("Duplicate map IDs in site payload")

    asset_fields = ("icon_asset", "minimap_asset", "full_map_asset")
    missing_assets = []
    for section in ("items", "maps"):
        for row in runtime.get(section, []):
            for field in asset_fields:
                value = row.get(field)
                if not value:
                    continue
                relative = value.removeprefix("./")
                if not (site / relative).is_file():
                    missing_assets.append({"section": section, "id": row.get("item_id") or row.get("map_id"), "field": field, "path": value})
    if missing_assets:
        failures.append(f"Missing asset references: {len(missing_assets)}")

    invalid_confidence = []
    for section, values in runtime.items():
        if not isinstance(values, list):
            continue
        for row in values:
            value = row.get("confidence") if isinstance(row, dict) else None
            if value and value not in CONFIDENCE:
                invalid_confidence.append({"section": section, "value": value})
    if invalid_confidence:
        failures.append(f"Invalid confidence values: {len(invalid_confidence)}")

    too_large = [path for path in site.rglob("*") if path.is_file() and ".git" not in path.parts and path.stat().st_size >= 100_000_000]
    if too_large:
        failures.append("Files exceed GitHub's 100 MB limit: " + ", ".join(str(path.relative_to(site)) for path in too_large))

    result = {
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "counts": {key: len(value) for key, value in runtime.items() if isinstance(value, list)},
        "missing_assets": missing_assets[:100],
        "runtime_bytes": runtime_path.stat().st_size,
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
