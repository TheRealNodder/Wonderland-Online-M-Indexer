#!/usr/bin/env python3
"""Split the browser runtime payload into lazy-loaded section files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECTION_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
SEARCH_FIELD = re.compile(
    r"(?:^|_)(?:id|name|title|key|text|category|type|reason|next_step|field_name|"
    r"source_asset_name|source_record_key|encounter|map|item|monster|quest|confidence)(?:$|_)",
    re.IGNORECASE,
)
SKIP_SEARCH_FIELDS = {
    "raw_value",
    "parsed_value",
    "client_version",
    "extraction_timestamp",
    "parser_version",
    "verification_status",
}


def compact_json(value: Any, *, indent: int | None = None) -> bytes:
    separators = None if indent else (",", ":")
    return json.dumps(value, ensure_ascii=False, indent=indent, separators=separators).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def compact_source(value: Any) -> str:
    if not value:
        return ""
    source = str(value).replace("\\", "/")
    marker = "/WLM/"
    folded = source.casefold()
    if marker.casefold() in folded:
        index = folded.index(marker.casefold())
        return source[index + len(marker) :]
    return Path(source).name


def identity(section: str, record: dict[str, Any]) -> str:
    if section == "localization":
        return f"{record.get('display_text') or 'Localization'} #{record.get('localization_key', '')}".strip()
    if section == "evidence":
        value = f"{record.get('entity_type') or 'Evidence'} #{record.get('entity_id', '')}"
        return f"{value} {record.get('field_name') or ''}".strip()
    if section == "unresolved":
        return f"{record.get('relationship_type') or 'Unresolved'}: {record.get('source_id') or ''}".strip()
    id_key = next((key for key in record if re.search(r"(?:^|_)id$", key)), None)
    name_key = next(
        (
            key
            for key in record
            if re.search(r"display_name|display_title|shop_name|item_name|monster_name|internal_name", key)
            and record.get(key)
        ),
        None,
    )
    label = str(record.get(name_key) if name_key else "Record")
    return f"{label} #{record.get(id_key)}" if id_key and record.get(id_key) is not None else label


def search_values(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, (str, int, float, bool)):
        return [str(value)]
    if isinstance(value, list):
        output: list[str] = []
        for item in value:
            output.extend(search_values(item))
        return output
    if isinstance(value, dict):
        output = []
        for item in value.values():
            output.extend(search_values(item))
        return output
    return []


def build_search_index(sections: dict[str, list[Any]]) -> list[list[Any]]:
    rows: list[list[Any]] = []
    for section, values in sections.items():
        for row_index, record in enumerate(values):
            if not isinstance(record, dict):
                continue
            label = identity(section, record)
            terms = [section.replace("_", " ")]
            for key, value in record.items():
                if key in SKIP_SEARCH_FIELDS or not SEARCH_FIELD.search(key):
                    continue
                terms.extend(search_values(value))
            normalized: list[str] = []
            seen: set[str] = set()
            for term in terms:
                term = " ".join(term.casefold().split())
                if term and term not in seen:
                    normalized.append(term)
                    seen.add(term)
            rows.append(
                [
                    section,
                    row_index,
                    label,
                    record.get("confidence", ""),
                    compact_source(record.get("source_file")),
                    " ".join(normalized),
                ]
            )
    return rows


def load_existing_shards(data_dir: Path) -> dict[str, Any]:
    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    runtime: dict[str, Any] = {"meta": manifest.get("meta", {})}
    for name, entry in manifest.get("sections", {}).items():
        path = data_dir.parent / str(entry["path"]).removeprefix("./")
        value = json.loads(path.read_text(encoding="utf-8"))
        runtime[name] = value.get("records", []) if isinstance(value, dict) else value
    return runtime


def write_runtime_shards(runtime: dict[str, Any], data_dir: Path) -> dict[str, Any]:
    data_dir.mkdir(parents=True, exist_ok=True)
    section_dir = data_dir / "sections"
    section_dir.mkdir(parents=True, exist_ok=True)
    sections = {key: value for key, value in runtime.items() if isinstance(value, list)}
    invalid = [key for key in sections if not SECTION_NAME.fullmatch(key)]
    if invalid:
        raise ValueError(f"Unsafe section names: {invalid}")

    search_rows = build_search_index(sections)
    section_content = {
        name: {
            "records": values,
            "record_count": len(values),
            "content_hash": sha256_bytes(compact_json(values)),
        }
        for name, values in sorted(sections.items())
    }
    search_content_hash = sha256_bytes(compact_json(search_rows))
    sqlite_path = data_dir / "wonderland_m_complete.sqlite3"
    sqlite_info: dict[str, Any] | None = None
    if sqlite_path.is_file():
        sqlite_raw_hash = hashlib.sha256()
        with sqlite_path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                sqlite_raw_hash.update(chunk)
        sqlite_info = {
            "path": "./data/wonderland_m_complete.sqlite3",
            "bytes": sqlite_path.stat().st_size,
            "sha256": sqlite_raw_hash.hexdigest(),
        }
    build_source = {
        "meta": runtime.get("meta", {}),
        "sections": {
            name: {"record_count": value["record_count"], "content_hash": value["content_hash"]}
            for name, value in section_content.items()
        },
        "search_content_hash": search_content_hash,
        "sqlite": sqlite_info,
    }
    build_id = sha256_bytes(compact_json(build_source))[:24]
    generated_at = str(runtime.get("meta", {}).get("generated_at") or datetime.now(timezone.utc).isoformat())
    schema_version = 3

    section_manifest: dict[str, dict[str, Any]] = {}
    expected_files: set[Path] = set()
    for name, content in section_content.items():
        wrapper = {
            "build_id": build_id,
            "schema_version": schema_version,
            "generated_at": generated_at,
            "record_count": content["record_count"],
            "content_hash": content["content_hash"],
            "records": content["records"],
        }
        payload = compact_json(wrapper)
        payload_hash = sha256_bytes(payload)
        target = section_dir / f"{name}.{payload_hash[:12]}.json"
        target.write_bytes(payload)
        expected_files.add(target.resolve())
        section_manifest[name] = {
            "path": f"./data/sections/{target.name}",
            "count": content["record_count"],
            "bytes": len(payload),
            "sha256": payload_hash,
            "content_hash": content["content_hash"],
        }

    for stale in section_dir.glob("*.json"):
        if stale.resolve() not in expected_files:
            stale.unlink()

    search_wrapper = {
        "build_id": build_id,
        "schema_version": schema_version,
        "generated_at": generated_at,
        "record_count": len(search_rows),
        "content_hash": search_content_hash,
        "records": search_rows,
    }
    search_payload = compact_json(search_wrapper)
    search_payload_hash = sha256_bytes(search_payload)
    search_path = data_dir / f"search-index.{search_payload_hash[:12]}.json"
    search_path.write_bytes(search_payload)
    for stale in data_dir.glob("search-index*.json"):
        if stale.resolve() != search_path.resolve():
            stale.unlink()
    manifest = {
        "format_version": schema_version,
        "build_id": build_id,
        "schema_version": schema_version,
        "generated_at": generated_at,
        "meta": runtime.get("meta", {}),
        "counts": {key: len(value) for key, value in sorted(sections.items())},
        "sections": section_manifest,
        "search": {
            "path": f"./data/{search_path.name}",
            "count": len(search_rows),
            "bytes": len(search_payload),
            "sha256": search_payload_hash,
            "content_hash": search_content_hash,
        },
        "sqlite": sqlite_info,
    }
    (data_dir / "manifest.json").write_bytes(compact_json(manifest, indent=2))
    return manifest


def markdown_report(manifest: dict[str, Any], old_bytes: int, monolith_removed: bool) -> str:
    section_total = sum(int(value["bytes"]) for value in manifest["sections"].values())
    initial_bytes = (Path(__file__).resolve().parents[1] / "data" / "manifest.json").stat().st_size
    lines = [
        "# Runtime index sharding report",
        "",
        f"- Previous eager runtime payload: `{old_bytes}` bytes",
        f"- Initial manifest payload: `{initial_bytes}` bytes",
        f"- Build ID: `{manifest['build_id']}`",
        f"- Schema version: `{manifest['schema_version']}`",
        f"- Section payload total: `{section_total}` bytes",
        f"- Search payload, loaded only when used: `{manifest['search']['bytes']}` bytes",
        f"- Search records: `{manifest['search']['count']}`",
        f"- Monolithic runtime removed: **{monolith_removed}**",
        "",
        "Opening the site now loads only the manifest. A section is fetched when selected,",
        "and the search file is fetched only after a global-search query is entered.",
        "Section and search filenames include content hashes. Every file carries the same build ID,",
        "schema version, timestamp, record count, and content hash.",
        "The complete SQLite snapshot remains available for full offline queries.",
        "",
        "## Section files",
        "",
        "| Section | Records | Bytes | SHA-256 |",
        "|---|---:|---:|---|",
    ]
    for name, value in sorted(manifest["sections"].items()):
        lines.append(f"| `{name}` | {value['count']} | {value['bytes']} | `{value['sha256']}` |")
    lines.extend(
        [
            "",
            "Sharding changes delivery only. It does not change record values, evidence,",
            "confidence, verification status, or the SQLite source snapshot.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path, default=repository / "data" / "runtime-index.json")
    parser.add_argument("--data-dir", type=Path, default=repository / "data")
    parser.add_argument("--report", type=Path, default=repository / "reports" / "runtime_index_sharding.md")
    parser.add_argument("--remove-source", action="store_true")
    args = parser.parse_args()

    if args.runtime.is_file():
        raw = args.runtime.read_bytes()
        runtime = json.loads(raw.decode("utf-8"))
        old_bytes = len(raw)
    else:
        runtime = load_existing_shards(args.data_dir.resolve())
        old_bytes = sum(len(compact_json(value)) for value in runtime.values() if isinstance(value, list))
    manifest = write_runtime_shards(runtime, args.data_dir.resolve())
    for name, info in manifest["sections"].items():
        shard_path = args.data_dir.parent / str(info["path"]).removeprefix("./")
        shard = json.loads(shard_path.read_text(encoding="utf-8"))
        if shard.get("records") != runtime[name] or shard.get("record_count") != info["count"]:
            raise RuntimeError(f"Shard validation failed: {name}")
    search_path = args.data_dir.parent / str(manifest["search"]["path"]).removeprefix("./")
    search = json.loads(search_path.read_text(encoding="utf-8"))
    if len(search.get("records", [])) != manifest["search"]["count"]:
        raise RuntimeError("Search index validation failed")

    removed = False
    if args.remove_source and args.runtime.is_file():
        args.runtime.unlink()
        removed = True
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(markdown_report(manifest, old_bytes, removed or not args.runtime.exists()), encoding="utf-8")
    print(
        json.dumps(
            {
                "manifest": str((args.data_dir / "manifest.json").resolve()),
                "sections": len(manifest["sections"]),
                "section_bytes": sum(value["bytes"] for value in manifest["sections"].values()),
                "search_bytes": manifest["search"]["bytes"],
                "source_removed": removed,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
