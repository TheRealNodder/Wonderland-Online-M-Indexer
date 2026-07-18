#!/usr/bin/env python3
"""Build static site data from the external Wonderland M extraction workspace."""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from shard_runtime_index import write_runtime_shards


def load_json(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    return value if isinstance(value, list) else []


def copy_asset(value: str | None, source_root: Path, site_root: Path, category: str) -> str | None:
    if not value:
        return None
    source = Path(value)
    if not source.is_file() or source_root not in source.parents:
        return None
    target_dir = site_root / "assets" / category
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    if not target.exists() or target.stat().st_size != source.stat().st_size:
        shutil.copy2(source, target)
    return f"./assets/{category}/{target.name}"


def query(db: sqlite3.Connection, sql: str) -> list[dict[str, Any]]:
    return [dict(row) for row in db.execute(sql)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extraction-dir", required=True, type=Path)
    parser.add_argument("--site-dir", required=True, type=Path)
    args = parser.parse_args()
    extraction = args.extraction_dir.resolve()
    site = args.site_dir.resolve()
    data_dir = site / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    items = load_json(extraction / "extracted" / "items" / "items.json")
    for item in items:
        item["icon_asset"] = copy_asset(item.get("icon_asset"), extraction, site, "items")
    maps = load_json(extraction / "extracted" / "maps" / "maps.json")
    for record in maps:
        record["minimap_asset"] = copy_asset(record.get("minimap_asset"), extraction, site, "maps")
        record["full_map_asset"] = copy_asset(record.get("full_map_asset"), extraction, site, "maps")

    db_path = extraction / "database" / "wonderland_m_complete.sqlite3"
    shutil.copy2(db_path, data_dir / "wonderland_m_complete.sqlite3")
    db = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    try:
        evidence = query(db, "SELECT entity_type,entity_id,field_name,source_file,source_asset_name,source_object_id,source_record_key,extraction_method,confidence,client_version,extraction_timestamp,parser_version,verification_status FROM extraction_evidence ORDER BY entity_type,entity_id")
        localization = query(db, "SELECT localization_key,language,display_text,category,source_file,source_asset_name,source_record_key,extraction_method,confidence,verification_status FROM localization_entries ORDER BY localization_key,language")
        unresolved = query(db, "SELECT relationship_type,source_id,target_id,reason,next_step,confidence,source_file,verification_status FROM unresolved_relationships ORDER BY id")
        issues = query(db, "SELECT severity,issue_type,entity_type,entity_id,details,status,confidence,source_file FROM verification_issues ORDER BY id")
        localization_count = db.execute("SELECT COUNT(*) FROM localization_entries").fetchone()[0]
        source_count = db.execute("SELECT COUNT(*) FROM source_files").fetchone()[0]
    finally:
        db.close()

    portals = load_json(extraction / "extracted" / "maps" / "portals.json")
    teleports = load_json(extraction / "extracted" / "maps" / "teleports.json")
    runtime = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "game": "Wonderland M",
            "engine": "Unity IL2CPP",
            "unity_version": "Unity 6000.0.58f2",
            "il2cpp_metadata_version": 31,
            "verification_status": "current_client_extracted",
            "files_scanned": source_count,
            "localization_count": localization_count,
            "character_data_included": False,
            "database_path": "./data/wonderland_m_complete.sqlite3",
        },
        "items": items,
        "monsters": load_json(extraction / "extracted" / "monsters" / "monsters.json"),
        "drops": load_json(extraction / "extracted" / "items" / "monster_drops.json"),
        "maps": maps,
        "step_afk_locations": load_json(extraction / "extracted" / "encounters" / "step_encounters.json"),
        "visible_spawns": load_json(extraction / "extracted" / "encounters" / "visible_spawns.json"),
        "dungeons": [record for record in maps if record.get("dungeon")],
        "npcs": load_json(extraction / "extracted" / "npcs" / "npcs.json"),
        "shops": load_json(extraction / "extracted" / "shops" / "shops.json"),
        "quests": load_json(extraction / "extracted" / "quests" / "quests.json"),
        "quest_chains": load_json(extraction / "extracted" / "quests" / "quest_chains.json"),
        "quest_rewards": load_json(extraction / "extracted" / "quests" / "quest_rewards.json"),
        "map_requirements": load_json(extraction / "extracted" / "maps" / "map_requirements.json"),
        "portals_teleports": portals + teleports,
        "compounds": load_json(extraction / "extracted" / "items" / "compound_recipes.json"),
        "localization": localization,
        "evidence": evidence,
        "unresolved": unresolved,
        "verification_issues": issues,
    }
    manifest = write_runtime_shards(runtime, data_dir)
    old_runtime = data_dir / "runtime-index.json"
    if old_runtime.is_file():
        old_runtime.unlink()

    report_dir = site / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    for name in ("FINAL_EXTRACTION_REPORT.md", "validation_report.md", "engine_detection.md", "vine_harl_grass_findings.md"):
        source = extraction / "reports" / name
        if source.is_file():
            shutil.copy2(source, report_dir / name)
    print(
        json.dumps(
            {
                "status": "ok",
                "manifest": str(data_dir / "manifest.json"),
                "sections": len(manifest["sections"]),
                "items": len(items),
                "maps": len(maps),
                "evidence": len(evidence),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
