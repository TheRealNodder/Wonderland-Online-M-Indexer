#!/usr/bin/env python3
"""Validate the generated static Wonderland M site data."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


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


def record_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def site_path(site: Path, value: str) -> Path:
    relative = value.removeprefix("./")
    resolved = (site / relative).resolve()
    if resolved != site and site not in resolved.parents:
        raise ValueError(f"Path leaves site root: {value}")
    return resolved


def read_index_file(site: Path, entry: dict[str, Any], label: str, failures: list[str]) -> Any:
    try:
        path = site_path(site, str(entry["path"]))
    except (KeyError, ValueError) as error:
        failures.append(f"Invalid {label} path: {error}")
        return []
    if not path.is_file():
        failures.append(f"Missing {label} file: {path.relative_to(site)}")
        return []
    raw = path.read_bytes()
    if int(entry.get("bytes", -1)) != len(raw):
        failures.append(f"{label} byte count does not match manifest")
    if str(entry.get("sha256", "")) != hashlib.sha256(raw).hexdigest():
        failures.append(f"{label} SHA-256 does not match manifest")
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        failures.append(f"Invalid {label} JSON: {error}")
        return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, default=Path.cwd())
    args = parser.parse_args()
    site = args.site_dir.resolve()
    failures: list[str] = []
    manifest_path = site / "data" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("format_version") != 3 or manifest.get("schema_version") != 3:
        failures.append("Manifest format and schema versions must be 3")
    build_id = manifest.get("build_id")
    if not isinstance(build_id, str) or not build_id:
        failures.append("Manifest build_id is missing")
    if manifest.get("meta", {}).get("character_data_included") is not False:
        failures.append("character_data_included must be false")
    section_entries = manifest.get("sections", {})
    missing = sorted(REQUIRED_SECTIONS - section_entries.keys())
    if missing:
        failures.append(f"Missing sections: {', '.join(missing)}")

    runtime: dict[str, list[dict[str, Any]]] = {}
    section_bytes = 0
    for section in sorted(REQUIRED_SECTIONS):
        entry = section_entries.get(section, {})
        payload = read_index_file(site, entry, f"section {section}", failures)
        if not isinstance(payload, dict):
            failures.append(f"Section {section} has no wrapper")
            payload = {}
        if payload.get("build_id") != build_id or payload.get("schema_version") != manifest.get("schema_version"):
            failures.append(f"Section {section} build does not match manifest")
        values = payload.get("records", [])
        if not isinstance(values, list):
            failures.append(f"Section {section} is not an array")
            values = []
        runtime[section] = values
        section_bytes += max(0, int(entry.get("bytes", 0)))
        if int(entry.get("count", -1)) != len(values):
            failures.append(f"Section {section} count does not match manifest")
        if int(manifest.get("counts", {}).get(section, -1)) != len(values):
            failures.append(f"Section {section} count does not match counts map")
        if int(payload.get("record_count", -1)) != len(values):
            failures.append(f"Section {section} wrapper count does not match records")
        content_hash = record_hash(values)
        if payload.get("content_hash") != content_hash or entry.get("content_hash") != content_hash:
            failures.append(f"Section {section} content hash does not match records")

    search_entry = manifest.get("search", {})
    search_payload = read_index_file(site, search_entry, "search index", failures)
    if not isinstance(search_payload, dict):
        failures.append("Search index has no wrapper")
        search_payload = {}
    if search_payload.get("build_id") != build_id or search_payload.get("schema_version") != manifest.get("schema_version"):
        failures.append("Search index build does not match manifest")
    search_rows = search_payload.get("records", [])
    if not isinstance(search_rows, list):
        failures.append("Search index is not an array")
        search_rows = []
    if len(search_rows) != int(search_entry.get("count", -1)):
        failures.append("Search index count does not match manifest")
    if int(search_payload.get("record_count", -1)) != len(search_rows):
        failures.append("Search wrapper count does not match records")
    search_content_hash = record_hash(search_rows)
    if search_payload.get("content_hash") != search_content_hash or search_entry.get("content_hash") != search_content_hash:
        failures.append("Search content hash does not match records")
    expected_search_count = sum(len(values) for values in runtime.values())
    if len(search_rows) != expected_search_count:
        failures.append("Search index does not contain one row per section record")
    for index, record in enumerate(search_rows):
        if not isinstance(record, list) or len(record) != 6:
            failures.append(f"Search row {index} does not have six fields")
            continue
        section = record[0]
        row_index = record[1]
        if section not in runtime or not isinstance(row_index, int) or not (0 <= row_index < len(runtime[section])):
            failures.append(f"Search row {index} has an invalid section reference")
        if not isinstance(record[2], str) or not record[2]:
            failures.append(f"Search row {index} has no identity")
        if len(failures) >= 100:
            break

    item_ids = [row.get("item_id") for row in runtime["items"]]
    if len(item_ids) != len(set(item_ids)):
        failures.append("Duplicate item IDs in site data")
    map_ids = [row.get("map_id") for row in runtime["maps"]]
    if len(map_ids) != len(set(map_ids)):
        failures.append("Duplicate map IDs in site data")

    asset_fields = ("icon_asset", "minimap_asset", "full_map_asset")
    missing_assets = []
    for section in ("items", "maps"):
        for row in runtime[section]:
            for field in asset_fields:
                value = row.get(field)
                if not value:
                    continue
                try:
                    path = site_path(site, str(value))
                except ValueError:
                    path = Path("__outside_site__")
                if not path.is_file():
                    missing_assets.append(
                        {"section": section, "id": row.get("item_id") or row.get("map_id"), "field": field, "path": value}
                    )
    if missing_assets:
        failures.append(f"Missing asset references: {len(missing_assets)}")

    invalid_confidence = []
    for section, values in runtime.items():
        for row in values:
            value = row.get("confidence") if isinstance(row, dict) else None
            if value and value not in CONFIDENCE:
                invalid_confidence.append({"section": section, "value": value})
    if invalid_confidence:
        failures.append(f"Invalid confidence values: {len(invalid_confidence)}")

    if (site / "data" / "runtime-index.json").exists():
        failures.append("Monolithic runtime-index.json should be removed after sharding")
    sqlite_entry = manifest.get("sqlite")
    if not isinstance(sqlite_entry, dict):
        failures.append("SQLite fingerprint is missing from manifest")
    else:
        sqlite_path = site_path(site, str(sqlite_entry.get("path", "")))
        if not sqlite_path.is_file():
            failures.append("SQLite file is missing")
        else:
            sqlite_raw = sqlite_path.read_bytes()
            if len(sqlite_raw) != int(sqlite_entry.get("bytes", -1)):
                failures.append("SQLite byte count does not match manifest")
            if hashlib.sha256(sqlite_raw).hexdigest() != sqlite_entry.get("sha256"):
                failures.append("SQLite SHA-256 does not match manifest")
    too_large = [
        path for path in site.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.stat().st_size >= 100_000_000
    ]
    if too_large:
        failures.append("Files exceed GitHub's 100 MB limit: " + ", ".join(str(path.relative_to(site)) for path in too_large))

    result = {
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "counts": {key: len(value) for key, value in runtime.items()},
        "missing_assets": missing_assets[:100],
        "manifest_bytes": manifest_path.stat().st_size,
        "section_bytes": section_bytes,
        "search_bytes": int(search_entry.get("bytes", 0)),
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
