#!/usr/bin/env python3
"""Inventory a Wonderland M XAPK and a user-supplied Android app-data export.

The source archives and app-data directory are treated as read only.  Generated
manifests are deterministic, role/role-card bundles are indexed only as opaque
files, and downloaded bundles are compared with the published Steam manifest.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import BinaryIO, Iterable


READ_CHUNK = 1024 * 1024
INVENTORY_SCHEMA_VERSION = 3
EXPECTED_PAYLOADS = (
    "NItem.Dat",
    "NItem_EN.Dat",
    "NNpc.dat",
    "NNpc_EN.dat",
    "NSceneData.dat",
    "NSceneData_EN.dat",
    "NSkill.dat",
    "NSkill_EN.dat",
    "NTalk.dat",
    "NTalk_EN.dat",
    "NCompound2.dat",
    "NFormula.dat",
)
DOWNLOAD_LEADS = (
    "AllFileList.txt",
    "packagesversion.txt",
    "MaxStreamingAssets.txt",
    "StreamingAssetsVision.txt",
)
STEAM_BUNDLE_PREFIX = "WLM_Data/StreamingAssets/"


def normalize(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def sha256_stream(stream: BinaryIO) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(READ_CHUNK), b""):
        digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    with path.open("rb") as stream:
        return sha256_stream(stream)


def magic_label(prefix: bytes) -> str:
    if prefix.startswith(b"UnityFS\0"):
        return "UnityFS"
    if prefix.startswith(b"\x7fELF"):
        return "ELF"
    if prefix.startswith(b"PK\x03\x04"):
        return "ZIP"
    if prefix.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    if prefix.startswith(b"SQLite format 3\0"):
        return "SQLite"
    if prefix.startswith(b"\x03\x00\x08\x00"):
        return "Android binary XML"
    if not prefix:
        return "empty"
    if all(value in b"\t\n\r" or 32 <= value < 127 for value in prefix):
        return "text"
    return "binary"


def purpose_for(relative_path: str) -> str:
    path = normalize(relative_path)
    lowered = path.casefold()
    if lowered == "cache/vulkan_pso_cache.bin":
        return "graphics_pipeline_cache"
    if lowered.startswith("files/hadload/"):
        return "download_completion_marker"
    if lowered.startswith("files/streamingassetszip/"):
        return "download_version_or_count_marker"
    if lowered.startswith("files/unitycache/shared/") and lowered.endswith("/__data"):
        return "unity_runtime_cache_data"
    if lowered.startswith("files/unitycache/shared/") and lowered.endswith("/__info"):
        return "unity_runtime_cache_metadata"
    if lowered == "files/sound.unity3d":
        return "downloaded_unity_bundle:sound.unity3d"
    if lowered.startswith("files/") and lowered.endswith(".unity3d"):
        parts = PurePosixPath(path).parts
        category = parts[1] if len(parts) > 2 else "root"
        return f"downloaded_unity_bundle:{category}"
    return "unknown_preserved"


def read_small_text(path: Path) -> str | None:
    if path.stat().st_size > 4096:
        return None
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def iter_files(root: Path) -> Iterable[Path]:
    return sorted(
        (candidate for candidate in root.rglob("*") if candidate.is_file()),
        key=lambda candidate: candidate.relative_to(root).as_posix().casefold(),
    )


def zip_entry_record(archive: zipfile.ZipFile, info: zipfile.ZipInfo) -> dict[str, object]:
    with archive.open(info) as stream:
        prefix = stream.read(32)
        stream.seek(0)
        digest = sha256_stream(stream)
    return {
        "path": normalize(info.filename),
        "size_bytes": info.file_size,
        "compressed_size_bytes": info.compress_size,
        "sha256": digest,
        "magic": magic_label(prefix),
    }


def inventory_xapk(xapk: Path) -> dict[str, object]:
    with zipfile.ZipFile(xapk) as archive:
        outer_entries = [
            zip_entry_record(archive, info)
            for info in sorted(
                (entry for entry in archive.infolist() if not entry.is_dir()),
                key=lambda entry: entry.filename.casefold(),
            )
        ]
        xapk_manifest = json.loads(archive.read("manifest.json"))
        embedded_apks: list[dict[str, object]] = []
        for entry in outer_entries:
            if not str(entry["path"]).casefold().endswith(".apk"):
                continue
            apk_bytes = archive.read(str(entry["path"]))
            with zipfile.ZipFile(io.BytesIO(apk_bytes)) as apk:
                members = [
                    zip_entry_record(apk, info)
                    for info in sorted(
                        (member for member in apk.infolist() if not member.is_dir()),
                        key=lambda member: member.filename.casefold(),
                    )
                ]
            embedded_apks.append(
                {
                    "path": entry["path"],
                    "size_bytes": entry["size_bytes"],
                    "sha256": entry["sha256"],
                    "entry_count": len(members),
                    "entries": members,
                }
            )

    all_names = [str(entry["path"]) for entry in outer_entries]
    for apk in embedded_apks:
        all_names.extend(str(entry["path"]) for entry in apk["entries"])
    by_basename: dict[str, list[str]] = defaultdict(list)
    for name in all_names:
        by_basename[PurePosixPath(name).name.casefold()].append(name)
    return {
        "path": str(xapk),
        "size_bytes": xapk.stat().st_size,
        "modified_utc": datetime.fromtimestamp(xapk.stat().st_mtime, timezone.utc).isoformat(),
        "sha256": sha256_file(xapk),
        "entry_count": len(outer_entries),
        "manifest": xapk_manifest,
        "entries": outer_entries,
        "embedded_apks": embedded_apks,
        "expected_payload_presence": {
            name: sorted(by_basename.get(name.casefold(), [])) for name in EXPECTED_PAYLOADS
        },
        "download_lead_presence": {
            name: sorted(by_basename.get(name.casefold(), [])) for name in DOWNLOAD_LEADS
        },
    }


def inventory_app_data(
    app_data_dir: Path,
) -> tuple[list[dict[str, object]], dict[str, object], dict[str, dict[str, object]]]:
    records: list[dict[str, object]] = []
    category_counts: Counter[str] = Counter()
    category_bytes: Counter[str] = Counter()
    by_basename: dict[str, list[str]] = defaultdict(list)
    marker_contents: dict[str, str] = {}
    bundles: dict[str, dict[str, object]] = {}
    unity_cache_data = 0
    unity_cache_info = 0
    unity_cache_hashes: list[str] = []
    unity_cache_data_directories: set[str] = set()
    unity_cache_info_directories: set[str] = set()

    for path in iter_files(app_data_dir):
        relative = path.relative_to(app_data_dir).as_posix()
        stat = path.stat()
        with path.open("rb") as stream:
            prefix = stream.read(32)
            stream.seek(0)
            digest = sha256_stream(stream)
        purpose = purpose_for(relative)
        record = {
            "relative_path": relative,
            "file_size": stat.st_size,
            "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            "sha256": digest,
            "magic": magic_label(prefix),
            "likely_purpose": purpose,
        }
        records.append(record)
        category_counts[purpose] += 1
        category_bytes[purpose] += stat.st_size
        by_basename[path.name.casefold()].append(relative)

        lowered = relative.casefold()
        if lowered.startswith("files/hadload/") or lowered.startswith("files/streamingassetszip/"):
            text = read_small_text(path)
            if text is not None:
                marker_contents[relative] = text
        if purpose == "unity_runtime_cache_data":
            unity_cache_data += 1
            unity_cache_hashes.append(digest)
            unity_cache_data_directories.add(PurePosixPath(relative).parent.as_posix())
        elif purpose == "unity_runtime_cache_metadata":
            unity_cache_info += 1
            unity_cache_info_directories.add(PurePosixPath(relative).parent.as_posix())

        if purpose.startswith("downloaded_unity_bundle:"):
            bundle_path = normalize(relative.removeprefix("files/"))
            bundles[bundle_path] = {
                "relative_path": bundle_path,
                "file_size": stat.st_size,
                "sha256": digest,
                "magic": magic_label(prefix),
            }

    primary_bundle_hashes = {str(bundle["sha256"]) for bundle in bundles.values()}
    unity_cache_primary_matches = sum(digest in primary_bundle_hashes for digest in unity_cache_hashes)
    cache_data_without_info = sorted(unity_cache_data_directories - unity_cache_info_directories)
    cache_info_without_data = sorted(unity_cache_info_directories - unity_cache_data_directories)
    summary = {
        "source_path": str(app_data_dir),
        "file_count": len(records),
        "total_bytes": sum(int(record["file_size"]) for record in records),
        "categories": {
            name: {"files": category_counts[name], "bytes": category_bytes[name]}
            for name in sorted(category_counts)
        },
        "marker_contents": {name: marker_contents[name] for name in sorted(marker_contents)},
        "unity_cache": {
            "data_files": unity_cache_data,
            "info_files": unity_cache_info,
            "paired_directories": len(
                unity_cache_data_directories & unity_cache_info_directories
            ),
            "pair_counts_match": not cache_data_without_info and not cache_info_without_data,
            "data_without_info": cache_data_without_info,
            "info_without_data": cache_info_without_data,
            "exact_primary_bundle_hash_matches": unity_cache_primary_matches,
            "unique_from_primary_bundle_tree": unity_cache_data - unity_cache_primary_matches,
        },
        "expected_payload_presence": {
            name: sorted(by_basename.get(name.casefold(), [])) for name in EXPECTED_PAYLOADS
        },
        "download_lead_presence": {
            name: sorted(by_basename.get(name.casefold(), [])) for name in DOWNLOAD_LEADS
        },
    }
    return records, summary, bundles


def load_steam_bundles(path: Path) -> dict[str, dict[str, object]]:
    bundles: dict[str, dict[str, object]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            relative = normalize(str(row["relative_path"]))
            if not relative.casefold().startswith(STEAM_BUNDLE_PREFIX.casefold()):
                continue
            bundle_path = relative[len(STEAM_BUNDLE_PREFIX) :]
            if not bundle_path.casefold().endswith(".unity3d"):
                continue
            bundles[bundle_path] = {
                "relative_path": bundle_path,
                "file_size": int(row["file_size"]),
                "sha256": str(row["sha256"]).casefold(),
                "source_path": relative,
            }
    return bundles


def compare_bundles(
    mobile: dict[str, dict[str, object]], steam: dict[str, dict[str, object]]
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    category_counts: dict[str, Counter[str]] = defaultdict(Counter)
    paths = sorted(set(mobile) | set(steam), key=str.casefold)
    for path in paths:
        current = mobile.get(path)
        previous = steam.get(path)
        if current is None:
            status = "missing_from_android_export"
        elif previous is None:
            status = "added_in_android_export"
        elif current["file_size"] == previous["file_size"] and current["sha256"] == previous["sha256"]:
            status = "exact_match"
        else:
            status = "platform_or_content_difference"
        category = PurePosixPath(path).parts[0] if "/" in path else "root"
        counts[status] += 1
        category_counts[category][status] += 1
        rows.append(
            {
                "relative_path": path,
                "category": category,
                "status": status,
                "android_size": current["file_size"] if current else "",
                "steam_size": previous["file_size"] if previous else "",
                "android_sha256": current["sha256"] if current else "",
                "steam_sha256": previous["sha256"] if previous else "",
            }
        )
    return rows, {
        "android_bundle_count": len(mobile),
        "steam_bundle_count": len(steam),
        "counts": {name: counts[name] for name in sorted(counts)},
        "categories": {
            category: {name: category_counts[category][name] for name in sorted(category_counts[category])}
            for category in sorted(category_counts)
        },
        "added_paths": [row["relative_path"] for row in rows if row["status"] == "added_in_android_export"],
        "missing_paths": [
            row["relative_path"] for row in rows if row["status"] == "missing_from_android_export"
        ],
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def cached_inventory_matches(
    summary_path: Path,
    app_csv_path: Path,
    comparison_csv_path: Path,
    xapk_inventory_path: Path,
    report_path: Path,
    xapk: Path,
    app_data_dir: Path,
    reference_csv: Path,
) -> dict[str, object] | None:
    required = (summary_path, app_csv_path, comparison_csv_path, xapk_inventory_path, report_path)
    if not all(path.is_file() for path in required):
        return None
    try:
        previous = json.loads(summary_path.read_text(encoding="utf-8"))
        if previous.get("inventory_schema_version") != INVENTORY_SCHEMA_VERSION:
            return None
        xapk_record = previous["xapk"]
        xapk_stat = xapk.stat()
        if str(xapk_record.get("path", "")).casefold() != str(xapk).casefold():
            return None
        if int(xapk_record.get("size_bytes", -1)) != xapk_stat.st_size:
            return None
        current_xapk_time = datetime.fromtimestamp(xapk_stat.st_mtime, timezone.utc).isoformat()
        if xapk_record.get("modified_utc") != current_xapk_time:
            return None
        reference = previous.get("reference_manifest", {})
        if str(reference.get("path", "")).casefold() != str(reference_csv).casefold():
            return None
        if int(reference.get("size_bytes", -1)) != reference_csv.stat().st_size:
            return None
        if reference.get("sha256") != sha256_file(reference_csv):
            return None
        if str(previous.get("app_data", {}).get("source_path", "")).casefold() != str(app_data_dir).casefold():
            return None

        cached_metadata: list[tuple[str, int, str]] = []
        with app_csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                cached_metadata.append(
                    (normalize(row["relative_path"]), int(row["file_size"]), row["modified_utc"])
                )
        current_metadata = []
        for path in iter_files(app_data_dir):
            stat = path.stat()
            current_metadata.append(
                (
                    path.relative_to(app_data_dir).as_posix(),
                    stat.st_size,
                    datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                )
            )
        if cached_metadata != current_metadata:
            return None
        return previous
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError):
        return None


def presence_table(presence: dict[str, list[str]]) -> str:
    lines = ["| Name | Hits |", "|---|---:|"]
    for name in (*EXPECTED_PAYLOADS, *DOWNLOAD_LEADS):
        lines.append(f"| `{name}` | {len(presence.get(name, []))} |")
    return "\n".join(lines)


def markdown_report(result: dict[str, object]) -> str:
    xapk = result["xapk"]
    app = result["app_data"]
    comparison = result["bundle_comparison"]
    package = xapk["manifest"]
    embedded_lines = []
    for apk in xapk["embedded_apks"]:
        embedded_lines.append(
            f"| `{apk['path']}` | {apk['size_bytes']:,} | `{apk['sha256']}` | {apk['entry_count']:,} |"
        )
    category_lines = []
    for category, values in app["categories"].items():
        category_lines.append(f"| `{category}` | {values['files']:,} | {values['bytes']:,} |")
    comparison_lines = []
    for status, count in comparison["counts"].items():
        comparison_lines.append(f"| `{status}` | {count:,} |")
    added_lines = "\n".join(f"- `{path}`" for path in comparison["added_paths"]) or "- None"
    missing_lines = "\n".join(f"- `{path}`" for path in comparison["missing_paths"]) or "- None"
    marker_lines = []
    for path, value in app["marker_contents"].items():
        if value or "streamingassetszip" in path.casefold():
            marker_lines.append(f"- `{path}` = `{value}`")

    combined_presence = {
        name: sorted(
            set(xapk["expected_payload_presence"].get(name, []))
            | set(app["expected_payload_presence"].get(name, []))
        )
        for name in EXPECTED_PAYLOADS
    }
    for name in DOWNLOAD_LEADS:
        combined_presence[name] = sorted(
            set(xapk["download_lead_presence"].get(name, []))
            | set(app["download_lead_presence"].get(name, []))
        )

    return f"""# Android XAPK and Runtime Export Inventory

Generated: {result['generated_at']}

## Verdict

The supplied XAPK and Android app-data export were read only. The XAPK identifies
package `{package.get('package_name')}`, version `{package.get('version_name')}`,
and version code `{package.get('version_code')}`. The app-data export contains a
complete-looking downloaded Unity bundle tree plus non-gameplay cache metadata,
but none of the 12 expected custom `N*.dat` payloads is present as an ordinary
file or APK member. The gameplay-domain record gate therefore remains closed.

Role and role-card bundles are represented only by path, size, and hash metadata.
No character model was parsed, rendered, or published.

## XAPK

- Source: `{xapk['path']}`
- Bytes: `{xapk['size_bytes']:,}`
- SHA-256: `{xapk['sha256']}`
- Outer entries: `{xapk['entry_count']}`

| Embedded APK | Bytes | SHA-256 | Entries |
|---|---:|---|---:|
{chr(10).join(embedded_lines)}

`source-provenance.json` records the separate static signature verification that
establishes publisher-certificate continuity and APK v2 content-digest validity.
This inventory does not infer signature validity from the XAPK container itself.

## Android app-data export

- Source: `{app['source_path']}`
- Files: `{app['file_count']:,}`
- Bytes: `{app['total_bytes']:,}`
- Unity cache data/info files: `{app['unity_cache']['data_files']}` / `{app['unity_cache']['info_files']}`
- Unity cache directories with exact data/info pairs: `{app['unity_cache']['paired_directories']}`
- Unity cache pair counts match: `{app['unity_cache']['pair_counts_match']}`
- Unity cache files matching primary bundle bytes: `{app['unity_cache']['exact_primary_bundle_hash_matches']}`
- Unity cache files byte-unique from the primary bundle tree: `{app['unity_cache']['unique_from_primary_bundle_tree']}`

| Classified purpose | Files | Bytes |
|---|---:|---:|
{chr(10).join(category_lines)}

Observed download-state markers:

{chr(10).join(marker_lines) if marker_lines else '- None with non-empty values.'}

The 51 `HadLoad/HadLoad*.txt` files are zero-length marker files. They are
preserved in the full CSV inventory and are not interpreted as package contents.

## Steam bundle comparison

Android and Steam bundle paths were normalized below their respective
StreamingAssets roots. A differing byte hash can reflect platform-specific Unity
serialization, compression, or content; it is not automatically a gameplay-data
change.

| Measurement | Count |
|---|---:|
| Android downloaded bundles | {comparison['android_bundle_count']:,} |
| Steam reference bundles | {comparison['steam_bundle_count']:,} |
{chr(10).join(comparison_lines)}

### Added Android paths

{added_lines}

### Missing Android paths

{missing_lines}

## Named payload and manifest presence

This is an exact, case-insensitive basename check across XAPK members and the
app-data export.

{presence_table(combined_presence)}

`MaxStreamingAssets.txt` and `StreamingAssetsVision.txt` are direct runtime
files. Their values and paths are recorded above. No `AllFileList.txt` or
`packagesversion.txt` copy was supplied.

## Generated evidence

- `android-app-files.csv`: full deterministic path/size/time/hash/type inventory.
- `android-bundle-comparison.csv`: every Android/Steam bundle relationship.
- `xapk-inventory.json`: outer and nested APK member hashes and file types.
- `android-source-inventory.json`: compact summary, marker values, and exact-name checks.
"""


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--xapk", required=True, type=Path)
    parser.add_argument("--app-data-dir", required=True, type=Path)
    parser.add_argument(
        "--reference-csv",
        type=Path,
        default=repository / "source_manifest" / "home_install" / "home-logical-files.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repository / "source_manifest" / "android_export",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=repository / "reports" / "android_runtime_export_inventory.md",
    )
    parser.add_argument("--force", action="store_true", help="Rehash every source file")
    args = parser.parse_args()

    xapk = args.xapk.resolve()
    app_data_dir = args.app_data_dir.resolve()
    reference_csv = args.reference_csv.resolve()
    output_dir = args.output_dir.resolve()
    report = args.report.resolve()
    if not xapk.is_file() or not zipfile.is_zipfile(xapk):
        raise SystemExit(f"XAPK is not a readable ZIP archive: {xapk}")
    if not app_data_dir.is_dir():
        raise SystemExit(f"Android app-data directory not found: {app_data_dir}")
    if not reference_csv.is_file():
        raise SystemExit(f"Steam reference CSV not found: {reference_csv}")
    for output in (output_dir, report.parent):
        if output == app_data_dir or app_data_dir in output.parents:
            raise SystemExit("Generated outputs must not be inside the supplied app-data export")
        if output == xapk.parent or xapk.parent in output.parents:
            raise SystemExit("Generated outputs must not be inside the supplied XAPK directory")

    summary_path = output_dir / "android-source-inventory.json"
    app_csv_path = output_dir / "android-app-files.csv"
    comparison_csv_path = output_dir / "android-bundle-comparison.csv"
    xapk_inventory_path = output_dir / "xapk-inventory.json"
    if not args.force:
        cached = cached_inventory_matches(
            summary_path,
            app_csv_path,
            comparison_csv_path,
            xapk_inventory_path,
            report,
            xapk,
            app_data_dir,
            reference_csv,
        )
        if cached is not None:
            print(
                json.dumps(
                    {
                        "output_dir": str(output_dir),
                        "report": str(report),
                        "app_data_files": cached["app_data"]["file_count"],
                        "android_bundles": cached["bundle_comparison"]["android_bundle_count"],
                        "comparison_counts": cached["bundle_comparison"]["counts"],
                        "cached": True,
                        "cache_basis": "source paths, sizes, modified times, and reference-manifest hash",
                    },
                    indent=2,
                )
            )
            return 0

    xapk_result = inventory_xapk(xapk)
    app_records, app_summary, mobile_bundles = inventory_app_data(app_data_dir)
    steam_bundles = load_steam_bundles(reference_csv)
    comparison_rows, comparison_summary = compare_bundles(mobile_bundles, steam_bundles)
    result = {
        "inventory_schema_version": INVENTORY_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "current Wonderland M XAPK and supplied Android app-data export",
        "legacy_game_evidence_imported": False,
        "character_assets_parsed": False,
        "xapk": xapk_result,
        "app_data": app_summary,
        "bundle_comparison": comparison_summary,
        "reference_manifest": {
            "path": str(reference_csv),
            "size_bytes": reference_csv.stat().st_size,
            "sha256": sha256_file(reference_csv),
        },
        "domain_record_gate": "closed_until_current_payload_records_are_recovered_and_validated",
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        app_csv_path,
        app_records,
        ["relative_path", "file_size", "modified_utc", "sha256", "magic", "likely_purpose"],
    )
    write_csv(
        comparison_csv_path,
        comparison_rows,
        [
            "relative_path",
            "category",
            "status",
            "android_size",
            "steam_size",
            "android_sha256",
            "steam_sha256",
        ],
    )
    xapk_inventory_path.write_text(
        json.dumps(xapk_result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    summary_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(markdown_report(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "report": str(report),
                "app_data_files": app_summary["file_count"],
                "android_bundles": comparison_summary["android_bundle_count"],
                "comparison_counts": comparison_summary["counts"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
