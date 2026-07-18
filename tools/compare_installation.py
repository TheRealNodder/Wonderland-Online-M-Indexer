#!/usr/bin/env python3
"""Compare a read-only Wonderland M installation with the published manifest.

The reference manifest lives in the ``source_files`` table of the published
SQLite snapshot.  Steam can package some StreamingAssets as ZIP members on one
machine and as loose files on another, so this tool compares both the physical
layout and a normalized logical layout.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import struct
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Iterable


READ_CHUNK = 1024 * 1024
CORE_PATHS = (
    "GameAssembly.dll",
    "UnityPlayer.dll",
    "WLM_Data/globalgamemanagers",
    "WLM_Data/il2cpp_data/Metadata/global-metadata.dat",
)
IDENTITY_PATHS = CORE_PATHS + (
    "WLM.exe",
    "WLM_Data/app.info",
    "WLM_Data/boot.config",
    "WLM_Data/RuntimeInitializeOnLoads.json",
    "WLM_Data/ScriptingAssemblies.json",
    "WLM_Data/StreamingAssets/UnityServicesProjectConfiguration.json",
)
EXPECTED_PAYLOADS = (
    "NItem.dat",
    "NItem_EN.dat",
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


@dataclass(frozen=True)
class ReferenceEntry:
    relative_path: str
    file_size: int
    sha256: str


@dataclass(frozen=True)
class LogicalEntry:
    relative_path: str
    file_size: int
    sha256: str
    source_kind: str
    physical_path: str
    container_path: str = ""
    member_path: str = ""


def normalize_path(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def sha256_stream(stream: BinaryIO) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(READ_CHUNK), b""):
        digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    with path.open("rb") as stream:
        return sha256_stream(stream)


def load_reference(database: Path) -> dict[str, ReferenceEntry]:
    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    try:
        rows = connection.execute(
            "SELECT relative_path, file_size, sha256 FROM source_files ORDER BY relative_path"
        )
        result: dict[str, ReferenceEntry] = {}
        for relative_path, file_size, sha256 in rows:
            path = normalize_path(relative_path)
            if path in result:
                raise ValueError(f"Duplicate reference path: {path}")
            result[path] = ReferenceEntry(path, int(file_size), str(sha256).lower())
        return result
    finally:
        connection.close()


def iter_physical_files(game_dir: Path) -> Iterable[Path]:
    return sorted((path for path in game_dir.rglob("*") if path.is_file()), key=lambda p: p.as_posix().lower())


def physical_metadata_inventory(game_dir: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in iter_physical_files(game_dir):
        stat = path.stat()
        records.append(
            {
                "relative_path": path.relative_to(game_dir).as_posix(),
                "file_size": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "is_archive_container": path.suffix.lower() == ".zip" and zipfile.is_zipfile(path),
            }
        )
    return records


def archive_logical_path(container_relative: str, member_name: str) -> str:
    parent = Path(container_relative).parent.as_posix()
    member = normalize_path(member_name)
    return normalize_path(f"{parent}/{member}")


def build_logical_inventory(
    game_dir: Path,
) -> tuple[dict[str, LogicalEntry], list[dict[str, object]], list[dict[str, object]]]:
    logical: dict[str, LogicalEntry] = {}
    physical: list[dict[str, object]] = []
    archives: list[dict[str, object]] = []

    for path in iter_physical_files(game_dir):
        relative = path.relative_to(game_dir).as_posix()
        stat = path.stat()
        physical_record: dict[str, object] = {
            "relative_path": relative,
            "file_size": stat.st_size,
            "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            "is_archive_container": False,
        }

        if path.suffix.lower() == ".zip" and zipfile.is_zipfile(path):
            physical_record["is_archive_container"] = True
            archive_record: dict[str, object] = {
                "relative_path": relative,
                "file_size": stat.st_size,
                "sha256": sha256_file(path),
                "members": 0,
            }
            with zipfile.ZipFile(path) as archive:
                members = sorted((info for info in archive.infolist() if not info.is_dir()), key=lambda i: i.filename.lower())
                archive_record["members"] = len(members)
                for info in members:
                    logical_path = archive_logical_path(relative, info.filename)
                    if logical_path in logical:
                        raise ValueError(f"Logical path collision at ZIP member: {logical_path}")
                    with archive.open(info) as stream:
                        digest = sha256_stream(stream)
                    logical[logical_path] = LogicalEntry(
                        relative_path=logical_path,
                        file_size=info.file_size,
                        sha256=digest,
                        source_kind="zip_member",
                        physical_path=str(path),
                        container_path=relative,
                        member_path=normalize_path(info.filename),
                    )
            archives.append(archive_record)
        else:
            if relative in logical:
                raise ValueError(f"Logical path collision at physical file: {relative}")
            logical[relative] = LogicalEntry(
                relative_path=relative,
                file_size=stat.st_size,
                sha256=sha256_file(path),
                source_kind="physical_file",
                physical_path=str(path),
            )
        physical.append(physical_record)

    return logical, physical, archives


def compare_entries(
    reference: dict[str, ReferenceEntry], logical: dict[str, LogicalEntry]
) -> dict[str, list[dict[str, object]]]:
    reference_paths = set(reference)
    logical_paths = set(logical)
    result: dict[str, list[dict[str, object]]] = {
        "added": [],
        "missing": [],
        "changed": [],
        "matched": [],
    }

    for path in sorted(logical_paths - reference_paths):
        result["added"].append(asdict(logical[path]))
    for path in sorted(reference_paths - logical_paths):
        result["missing"].append(asdict(reference[path]))
    for path in sorted(reference_paths & logical_paths):
        previous = reference[path]
        current = logical[path]
        record = {
            "relative_path": path,
            "reference_size": previous.file_size,
            "current_size": current.file_size,
            "reference_sha256": previous.sha256,
            "current_sha256": current.sha256,
            "source_kind": current.source_kind,
            "container_path": current.container_path,
            "member_path": current.member_path,
        }
        if previous.file_size == current.file_size and previous.sha256 == current.sha256:
            result["matched"].append(record)
        else:
            result["changed"].append(record)
    return result


def metadata_header(game_dir: Path) -> dict[str, object]:
    path = game_dir / "WLM_Data" / "il2cpp_data" / "Metadata" / "global-metadata.dat"
    with path.open("rb") as stream:
        header = stream.read(8)
    if len(header) != 8:
        return {"path": path.relative_to(game_dir).as_posix(), "error": "header shorter than 8 bytes"}
    sanity, version = struct.unpack("<II", header)
    return {
        "path": path.relative_to(game_dir).as_posix(),
        "sanity_hex": f"0x{sanity:08X}",
        "metadata_version": version,
    }


def unity_bundle_identity(game_dir: Path) -> dict[str, object]:
    for path in iter_physical_files(game_dir):
        if path.suffix.lower() != ".unity3d":
            continue
        with path.open("rb") as stream:
            header = stream.read(256)
        if not header.startswith(b"UnityFS\0") or len(header) < 16:
            continue
        position = 8
        bundle_format = struct.unpack(">I", header[position : position + 4])[0]
        position += 4
        try:
            version_end = header.index(b"\0", position)
            unity_version = header[position:version_end].decode("ascii", "replace")
            position = version_end + 1
            revision_end = header.index(b"\0", position)
            unity_revision = header[position:revision_end].decode("ascii", "replace")
        except ValueError:
            continue
        return {
            "source_file": path.relative_to(game_dir).as_posix(),
            "bundle_format": bundle_format,
            "unity_version_field": unity_version,
            "unity_revision": unity_revision,
        }
    return {"error": "No readable UnityFS bundle header found"}


def application_identity(game_dir: Path) -> dict[str, object]:
    path = game_dir / "WLM_Data" / "app.info"
    values = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return {
        "source_file": path.relative_to(game_dir).as_posix(),
        "company": values[0] if values else "",
        "product": values[1] if len(values) > 1 else "",
    }


def find_payloads(logical: dict[str, LogicalEntry]) -> dict[str, list[dict[str, object]]]:
    by_name: dict[str, list[LogicalEntry]] = {}
    for entry in logical.values():
        by_name.setdefault(Path(entry.relative_path).name.casefold(), []).append(entry)
    return {
        name: [asdict(entry) for entry in sorted(by_name.get(name.casefold(), []), key=lambda e: e.relative_path)]
        for name in EXPECTED_PAYLOADS
    }


def write_csv(path: Path, entries: Iterable[LogicalEntry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "relative_path",
        "file_size",
        "sha256",
        "source_kind",
        "physical_path",
        "container_path",
        "member_path",
    ]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(asdict(entry))


def markdown_list(values: list[str]) -> str:
    return "\n".join(f"- `{value}`" for value in values) if values else "- None"


def write_reports(
    output_dir: Path,
    result: dict[str, object],
    logical: dict[str, LogicalEntry],
    physical: list[dict[str, object]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "home-logical-files.csv", (logical[path] for path in sorted(logical)))
    (output_dir / "home-physical-files.json").write_text(
        json.dumps(physical, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )
    (output_dir / "install-comparison.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )

    counts = result["comparison_counts"]
    core = result["core_fingerprints"]
    payloads = result["payload_presence"]
    comparison = result["comparison"]
    archive_lines = []
    for archive in result["archive_containers"]:
        archive_lines.append(
            f"- `{archive['relative_path']}`: {archive['members']} logical members, "
            f"SHA-256 `{archive['sha256']}`"
        )
    core_lines = []
    for path in IDENTITY_PATHS:
        record = core[path]
        core_lines.append(
            f"| `{path}` | {record['current_size']} | `{record['current_sha256']}` | "
            f"{'yes' if record['matches_reference'] else 'no'} |"
        )
    payload_lines = []
    for name in EXPECTED_PAYLOADS:
        hits = payloads[name]
        payload_lines.append(f"| `{name}` | {len(hits)} |")

    report = f"""# Home Installation Comparison

Generated: {result['generated_at']}

## Result

**{result['decision']}**

The game directory was read only. ZIP members were hashed in memory and mapped to
their logical `WLM_Data/StreamingAssets/...` paths; nothing was extracted into the
Steam installation.

## Logical comparison

| Measurement | Count |
|---|---:|
| Reference files | {counts['reference_files']} |
| Current physical files | {counts['physical_files']} |
| Current logical files | {counts['logical_files']} |
| Matching logical files | {counts['matched']} |
| Changed logical files | {counts['changed']} |
| Missing logical files | {counts['missing']} |
| Added logical files | {counts['added']} |

## Core fingerprints

| Path | Bytes | Current SHA-256 | Matches reference |
|---|---:|---|:---:|
{chr(10).join(core_lines)}

IL2CPP metadata header: `{result['metadata_header']['sanity_hex']}`, version
`{result['metadata_header']['metadata_version']}`. Current UnityFS revision:
`{result['unity_bundle_identity'].get('unity_revision', 'unresolved')}`. Current
application identity: company `{result['application_identity']['company']}`,
product `{result['application_identity']['product']}`.

## Archive normalization

{chr(10).join(archive_lines) if archive_lines else '- No ZIP containers were normalized.'}

## Expected downloaded payload names

This is a filename-level presence check, not a claim about compressed Unity object
contents or server behavior.

| Payload | Logical filename hits |
|---|---:|
{chr(10).join(payload_lines)}

## Differences

### Changed

{markdown_list([row['relative_path'] for row in comparison['changed']])}

### Missing

{markdown_list([row['relative_path'] for row in comparison['missing']])}

### Added

{markdown_list([row['relative_path'] for row in comparison['added']])}

## Provenance guard

- The reference database describes the current Steam/mobile **Wonderland M**
  client, not the original early-2000s Wonderland Online release.
- Exact agreement of the Unity 6/IL2CPP core plus every logical source-file hash
  supports using the existing current-client extraction as the baseline.
- Original-PC-game information remains excluded unless a separate current-client
  record independently corroborates it.
"""
    (output_dir / "install-comparison.md").write_text(report, encoding="utf-8")


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-dir", required=True, type=Path)
    parser.add_argument(
        "--database",
        type=Path,
        default=repository / "data" / "wonderland_m_complete.sqlite3",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repository / "source_manifest" / "home_install",
    )
    parser.add_argument("--force", action="store_true", help="Hash every file even when path, size, and timestamp metadata are unchanged")
    args = parser.parse_args()

    game_dir = args.game_dir.resolve()
    database = args.database.resolve()
    output_dir = args.output_dir.resolve()
    if not game_dir.is_dir():
        raise SystemExit(f"Game directory not found: {game_dir}")
    if not database.is_file():
        raise SystemExit(f"Reference database not found: {database}")
    if output_dir == game_dir or game_dir in output_dir.parents:
        raise SystemExit("Output directory must not be inside the game installation")

    cached_physical_path = output_dir / "home-physical-files.json"
    cached_result_path = output_dir / "install-comparison.json"
    if not args.force and cached_physical_path.is_file() and cached_result_path.is_file():
        previous_physical = json.loads(cached_physical_path.read_text(encoding="utf-8"))
        current_physical = physical_metadata_inventory(game_dir)
        if previous_physical == current_physical:
            previous_result = json.loads(cached_result_path.read_text(encoding="utf-8"))
            passed = bool(
                previous_result.get("logical_identical")
                and previous_result.get("core_identical")
                and previous_result.get("metadata_header", {}).get("sanity_hex") == "0xFAB11BAF"
                and previous_result.get("metadata_header", {}).get("metadata_version") == 31
                and previous_result.get("unity_bundle_identity", {}).get("unity_revision") == "6000.0.58f2"
            )
            print(
                json.dumps(
                    {
                        "decision": previous_result.get("decision"),
                        "counts": previous_result.get("comparison_counts"),
                        "output_dir": str(output_dir),
                        "cached": True,
                        "cache_basis": "physical paths, sizes, archive flags, and modified timestamps are unchanged",
                    },
                    indent=2,
                )
            )
            return 0 if passed else 1

    reference = load_reference(database)
    logical, physical, archives = build_logical_inventory(game_dir)
    comparison = compare_entries(reference, logical)
    payload_presence = find_payloads(logical)
    header = metadata_header(game_dir)
    bundle_identity = unity_bundle_identity(game_dir)
    app_identity = application_identity(game_dir)

    core_fingerprints: dict[str, dict[str, object]] = {}
    for path in IDENTITY_PATHS:
        current = logical.get(path)
        previous = reference.get(path)
        core_fingerprints[path] = {
            "current_size": current.file_size if current else None,
            "current_sha256": current.sha256 if current else None,
            "reference_size": previous.file_size if previous else None,
            "reference_sha256": previous.sha256 if previous else None,
            "matches_reference": bool(
                current
                and previous
                and current.file_size == previous.file_size
                and current.sha256 == previous.sha256
            ),
        }

    logical_identical = not comparison["added"] and not comparison["missing"] and not comparison["changed"]
    core_identical = all(record["matches_reference"] for record in core_fingerprints.values())
    metadata_current = header.get("sanity_hex") == "0xFAB11BAF" and header.get("metadata_version") == 31
    unity_current = bundle_identity.get("unity_revision") == "6000.0.58f2"
    if logical_identical and core_identical and metadata_current and unity_current:
        decision = (
            "PASS: the home installation is logically byte-identical to the published "
            "Wonderland M source snapshot after normalizing ZIP packaging"
        )
    else:
        decision = (
            "REVIEW REQUIRED: the home installation differs from the published source "
            "snapshot; inspect the reported paths before extraction"
        )

    result: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "game_dir": str(game_dir),
        "reference_database": str(database),
        "decision": decision,
        "logical_identical": logical_identical,
        "core_identical": core_identical,
        "metadata_header": header,
        "unity_bundle_identity": bundle_identity,
        "application_identity": app_identity,
        "comparison_counts": {
            "reference_files": len(reference),
            "physical_files": len(physical),
            "logical_files": len(logical),
            "matched": len(comparison["matched"]),
            "changed": len(comparison["changed"]),
            "missing": len(comparison["missing"]),
            "added": len(comparison["added"]),
        },
        "core_fingerprints": core_fingerprints,
        "archive_containers": archives,
        "payload_presence": payload_presence,
        "comparison": {
            "added": comparison["added"],
            "missing": comparison["missing"],
            "changed": comparison["changed"],
        },
        "legacy_guard": {
            "reference_scope": "current Wonderland M Steam/mobile client",
            "original_pc_game_evidence_imported": False,
            "modern_client_identity_supported": logical_identical and core_identical and metadata_current and unity_current,
        },
    }
    existing_result_path = output_dir / "install-comparison.json"
    if existing_result_path.is_file():
        try:
            existing_result = json.loads(existing_result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing_result = None
        if isinstance(existing_result, dict):
            previous_without_time = {key: value for key, value in existing_result.items() if key != "generated_at"}
            current_without_time = {key: value for key, value in result.items() if key != "generated_at"}
            if previous_without_time == current_without_time and existing_result.get("generated_at"):
                result["generated_at"] = existing_result["generated_at"]
    write_reports(output_dir, result, logical, physical)
    print(json.dumps({"decision": decision, "counts": result["comparison_counts"], "output_dir": str(output_dir)}, indent=2))
    return 0 if logical_identical and core_identical and metadata_current and unity_current else 1


if __name__ == "__main__":
    raise SystemExit(main())
