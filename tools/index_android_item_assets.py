#!/usr/bin/env python3
"""Index item icons from Android-only Wonderland M Unity bundles.

AssetRipper is run separately against copies of the selected bundles. This tool
validates that export, copies only the item Texture2D PNGs, and records direct
bundle -> prefab -> item-icon evidence without assigning gameplay names or stats.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import struct
from datetime import datetime, timezone
from pathlib import Path


ITEM_PATH = re.compile(r"^item/atlas_item_(\d+)\.unity3d$", re.IGNORECASE)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_identity(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        header = stream.read(26)
    if len(header) != 26 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        raise ValueError(f"Not a readable PNG with an IHDR header: {path}")
    width, height = struct.unpack(">II", header[16:24])
    return {
        "width": width,
        "height": height,
        "bit_depth": header[24],
        "color_type": header[25],
    }


def load_added_items(comparison_csv: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with comparison_csv.open("r", encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["status"] != "added_in_android_export" or row["category"] != "item":
                continue
            match = ITEM_PATH.fullmatch(row["relative_path"])
            if not match:
                raise ValueError(f"Unexpected added item-bundle path: {row['relative_path']}")
            records.append(
                {
                    "item_id": int(match.group(1)),
                    "bundle_relative_path": row["relative_path"],
                    "bundle_size_bytes": int(row["android_size"]),
                    "bundle_sha256": row["android_sha256"],
                }
            )
    records.sort(key=lambda record: int(record["item_id"]))
    return records


def asset_bundle_evidence(export_dir: Path, item_id: int) -> dict[str, object]:
    path = export_dir / "Assets" / "AssetBundle" / f"item_atlas_item_{item_id}.unity3d.json"
    if not path.is_file():
        raise FileNotFoundError(f"Missing AssetRipper bundle export: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    expected_bundle = f"item/atlas_item_{item_id}.unity3d"
    if data.get("m_AssetBundleName", "").casefold() != expected_bundle.casefold():
        raise ValueError(f"AssetBundle name mismatch for item {item_id}: {data.get('m_AssetBundleName')}")
    container = data.get("m_Container", {})
    expected_prefab = f"assets/fordownloads/item/atlas_item_{item_id}.prefab"
    if list(container) != [expected_prefab]:
        raise ValueError(f"Unexpected prefab container for item {item_id}: {list(container)}")
    prefab = container[expected_prefab]
    return {
        "asset_bundle_export": path.as_posix(),
        "asset_bundle_name": data["m_AssetBundleName"],
        "prefab_path": expected_prefab,
        "prefab_object_id": str(prefab["m_Asset"]["m_PathID"]),
        "preload_index": int(prefab["m_PreloadIndex"]),
        "preload_size": int(prefab["m_PreloadSize"]),
    }


def copy_verified(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file():
        if sha256_file(source) != sha256_file(destination):
            raise ValueError(f"Refusing to overwrite a different icon: {destination}")
        return
    shutil.copy2(source, destination)


def report(result: dict[str, object]) -> str:
    rows = []
    for record in result["items"]:
        rows.append(
            f"| `{record['item_id']}` | `{record['bundle_relative_path']}` | "
            f"`{record['prefab_object_id']}` | `{record['icon_relative_path']}` | "
            f"`{record['confidence']}` |"
        )
    return f"""# Android-only item asset evidence

Generated: {result['generated_at']}

## Verdict

AssetRipper `{result['assetripper_version']}` parsed all `{len(result['items'])}` Android-only
item bundles selected by exact path comparison with the Steam snapshot. Each
bundle yielded one 32 x 32 RGBA Texture2D PNG and one direct item-prefab container
relationship. The internal numeric IDs are confirmed as asset IDs only.

No item names, descriptions, categories, stats, prices, crafting relationships,
drops, or spawn locations were inferred. Those fields remain unresolved until a
current gameplay record or other Grade A/B evidence links them.

| Item asset ID | Source bundle | Prefab object ID | Evidence icon | Confidence |
|---:|---|---|---|---|
{chr(10).join(rows)}

## Method

- Selected only `added_in_android_export` item paths from
  `source_manifest/android_export/android-bundle-comparison.csv`.
- Ran AssetRipper against isolated copies, never the supplied source directory.
- Validated each AssetBundle name and `assets/fordownloads/item/...prefab`
  container reference.
- Preserved original bundle and PNG SHA-256 hashes in `item-assets.json`.
- Visually inspected a contact sheet of all 12 icons before indexing.
- Did not parse or publish role/role-card assets.
"""


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-data-dir", required=True, type=Path)
    parser.add_argument("--assetripper-export", required=True, type=Path)
    parser.add_argument("--assetripper-version", default="1.3.14.0")
    parser.add_argument(
        "--comparison-csv",
        type=Path,
        default=repository / "source_manifest" / "android_export" / "android-bundle-comparison.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repository / "source_manifest" / "android_export",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=repository / "reports" / "android_new_item_assets.md",
    )
    args = parser.parse_args()

    app_data_dir = args.app_data_dir.resolve()
    export_dir = args.assetripper_export.resolve()
    comparison_csv = args.comparison_csv.resolve()
    output_dir = args.output_dir.resolve()
    report_path = args.report.resolve()
    if not app_data_dir.is_dir():
        raise SystemExit(f"App-data directory not found: {app_data_dir}")
    if not export_dir.is_dir():
        raise SystemExit(f"AssetRipper export not found: {export_dir}")
    if not comparison_csv.is_file():
        raise SystemExit(f"Comparison CSV not found: {comparison_csv}")
    for output in (output_dir, report_path.parent):
        if output == app_data_dir or app_data_dir in output.parents:
            raise SystemExit("Generated outputs must not be inside the supplied app-data export")

    items = load_added_items(comparison_csv)
    records: list[dict[str, object]] = []
    for item in items:
        item_id = int(item["item_id"])
        source_bundle = app_data_dir / "files" / Path(str(item["bundle_relative_path"]))
        if not source_bundle.is_file():
            raise FileNotFoundError(f"Source bundle missing: {source_bundle}")
        if source_bundle.stat().st_size != item["bundle_size_bytes"]:
            raise ValueError(f"Source bundle size changed: {source_bundle}")
        if sha256_file(source_bundle) != item["bundle_sha256"]:
            raise ValueError(f"Source bundle hash changed: {source_bundle}")

        icon_source = export_dir / "Assets" / "Texture2D" / f"Atlas_Item_{item_id}.png"
        if not icon_source.is_file():
            raise FileNotFoundError(f"Missing AssetRipper Texture2D PNG: {icon_source}")
        png = png_identity(icon_source)
        if png != {"width": 32, "height": 32, "bit_depth": 8, "color_type": 6}:
            raise ValueError(f"Unexpected icon PNG identity for item {item_id}: {png}")
        icon_destination = output_dir / "item_icons" / f"{item_id}.png"
        copy_verified(icon_source, icon_destination)
        bundle_evidence = asset_bundle_evidence(export_dir, item_id)
        records.append(
            {
                **item,
                "source_bundle": str(source_bundle),
                **bundle_evidence,
                "texture_asset_name": f"Atlas_Item_{item_id}",
                "icon_relative_path": icon_destination.relative_to(repository).as_posix(),
                "icon_size_bytes": icon_destination.stat().st_size,
                "icon_sha256": sha256_file(icon_destination),
                "png": png,
                "extraction_method": (
                    f"AssetRipper {args.assetripper_version} primary-content Texture2D PNG export"
                ),
                "confidence": "direct_asset_relationship",
                "gameplay_record_status": "unresolved",
            }
        )

    result = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_scope": "current Wonderland M Android runtime export",
        "assetripper_version": args.assetripper_version,
        "legacy_gameplay_data_imported": False,
        "character_assets_parsed": False,
        "items": records,
    }
    output_json = output_dir / "item-assets.json"
    if output_json.is_file():
        previous = json.loads(output_json.read_text(encoding="utf-8"))
        previous_without_time = {key: value for key, value in previous.items() if key != "generated_at"}
        current_without_time = {key: value for key, value in result.items() if key != "generated_at"}
        if previous_without_time == current_without_time and previous.get("generated_at"):
            result["generated_at"] = previous["generated_at"]
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "items_indexed": len(records),
                "output": str(output_json),
                "report": str(report_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
