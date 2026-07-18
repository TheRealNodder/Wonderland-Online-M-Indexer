#!/usr/bin/env python3
"""Profile the static site's monolithic Wonderland M runtime JSON payload."""

from __future__ import annotations

import argparse
import gzip
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def encoded(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path, default=repository / "data" / "runtime-index.json")
    parser.add_argument("--app-js", type=Path, default=repository / "app.js")
    parser.add_argument("--output-json", type=Path, default=repository / "reports" / "runtime_index_profile.json")
    parser.add_argument("--output-markdown", type=Path, default=repository / "reports" / "runtime_index_profile.md")
    args = parser.parse_args()

    raw = args.runtime.read_bytes()
    parse_samples: list[float] = []
    runtime: dict[str, Any] | None = None
    decoded = raw.decode("utf-8")
    for _ in range(3):
        started = time.perf_counter()
        runtime = json.loads(decoded)
        parse_samples.append((time.perf_counter() - started) * 1000)
    assert runtime is not None

    sections: list[dict[str, Any]] = []
    total_records = 0
    for name, value in runtime.items():
        if not isinstance(value, list):
            continue
        payload = encoded(value)
        records = len(value)
        total_records += records
        field_counts: Counter[str] = Counter()
        null_or_empty: Counter[str] = Counter()
        for row in value:
            if not isinstance(row, dict):
                continue
            for key, field_value in row.items():
                field_counts[key] += 1
                if field_value is None or field_value == "" or field_value == [] or field_value == {}:
                    null_or_empty[key] += 1
        sections.append(
            {
                "section": name,
                "records": records,
                "bytes": len(payload),
                "gzip_bytes": len(gzip.compress(payload, compresslevel=9, mtime=0)),
                "percent_of_runtime": round(len(payload) * 100 / len(raw), 2),
                "field_count": len(field_counts),
                "fields_always_empty": sorted(
                    key for key, count in field_counts.items() if count and null_or_empty[key] == count
                ),
            }
        )
    sections.sort(key=lambda item: (-item["bytes"], item["section"]))

    app_source = args.app_js.read_text(encoding="utf-8")
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runtime": str(args.runtime.resolve()),
        "runtime_bytes": len(raw),
        "runtime_gzip_bytes": len(gzip.compress(raw, compresslevel=9, mtime=0)),
        "python_json_parse_ms": {
            "samples": [round(value, 2) for value in parse_samples],
            "average": round(sum(parse_samples) / len(parse_samples), 2),
        },
        "total_records": total_records,
        "sections": sections,
        "frontend_observations": {
            "eager_monolithic_fetch": 'fetch("./data/runtime-index.json"' in app_source,
            "global_search_stringifies_each_record_per_filter_pass": "JSON.stringify(record).toLocaleLowerCase()" in app_source,
            "page_size": 250 if "const PAGE_SIZE = 250" in app_source else None,
        },
        "recommendations": [
            "Load a small manifest first and fetch section JSON only when selected.",
            "Keep global search in a compact precomputed search shard instead of stringifying full records on each keystroke.",
            "Defer evidence and localization detail payloads until their sections or a record dialog need them.",
            "Keep the SQLite snapshot as the complete downloadable source while making the browser payload task-oriented.",
        ],
    }

    lines = [
        "# Runtime index profile",
        "",
        f"- Runtime JSON: `{result['runtime_bytes']}` bytes",
        f"- Deterministic gzip estimate: `{result['runtime_gzip_bytes']}` bytes",
        f"- Records loaded eagerly: `{result['total_records']}`",
        f"- Python JSON parse average (three local samples): `{result['python_json_parse_ms']['average']}` ms",
        f"- Eager monolithic fetch detected: **{result['frontend_observations']['eager_monolithic_fetch']}**",
        f"- Per-filter full-record stringify detected: **{result['frontend_observations']['global_search_stringifies_each_record_per_filter_pass']}**",
        "",
        "Browser timing will vary by device. The Python samples measure payload parse cost only,",
        "not network, DOM rendering, image loading, or JavaScript garbage collection.",
        "",
        "## Section contribution",
        "",
        "| Section | Records | JSON bytes | Gzip bytes | Runtime share | Always-empty fields |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for section in sections:
        empty = ", ".join(f"`{field}`" for field in section["fields_always_empty"]) or "-"
        lines.append(
            f"| `{section['section']}` | {section['records']} | {section['bytes']} | "
            f"{section['gzip_bytes']} | {section['percent_of_runtime']:.2f}% | {empty} |"
        )
    lines.extend(["", "## Recommended direction", ""])
    for recommendation in result["recommendations"]:
        lines.append(f"- {recommendation}")
    lines.extend(
        [
            "",
            "Any sharding change must preserve IDs, provenance, confidence, client version, and",
            "verification status. Performance work must not turn unresolved fields into facts.",
            "",
        ]
    )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    args.output_markdown.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"runtime_bytes": len(raw), "total_records": total_records, "largest_sections": sections[:3]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
