#!/usr/bin/env python3
"""Audit row-level evidence against the current-client source manifest."""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_PROVENANCE = (
    "source_file",
    "extraction_method",
    "confidence",
    "client_version",
    "parser_version",
    "verification_status",
)


def normalize(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def source_relative(value: str) -> str:
    normalized = normalize(value)
    marker = "/WLM/"
    if marker.casefold() in normalized.casefold():
        position = normalized.casefold().index(marker.casefold())
        return normalized[position + len(marker) :]
    return normalized


def table_columns(connection: sqlite3.Connection, table: str) -> set[str]:
    return {str(row[1]) for row in connection.execute(f'PRAGMA table_info("{table}")')}


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database",
        type=Path,
        default=repository / "data" / "wonderland_m_complete.sqlite3",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repository / "reports" / "provenance_audit.json",
    )
    args = parser.parse_args()

    database = args.database.resolve()
    output = args.output.resolve()
    if not database.is_file():
        raise SystemExit(f"Database not found: {database}")

    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        reference_paths = {
            normalize(str(row[0])): {"size": int(row[1]), "sha256": str(row[2])}
            for row in connection.execute(
                "SELECT relative_path, file_size, sha256 FROM source_files"
            )
        }
        tables = [
            str(row[0])
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            if not str(row[0]).startswith("sqlite_")
        ]
        table_results: dict[str, dict[str, object]] = {}
        total_domain_rows = 0
        total_audited_rows = 0
        total_failures = 0
        for table in tables:
            count = int(connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0])
            columns = table_columns(connection, table)
            result: dict[str, object] = {
                "rows": count,
                "provenance_columns_present": sorted(set(REQUIRED_PROVENANCE) & columns),
                "audited": False,
            }
            if table == "source_files" or count == 0:
                table_results[table] = result
                continue
            total_domain_rows += count
            if not set(REQUIRED_PROVENANCE).issubset(columns):
                result["failure"] = "Required provenance columns are missing"
                total_failures += count
                table_results[table] = result
                continue

            query = (
                f'SELECT source_file, extraction_method, confidence, client_version, '
                f'parser_version, verification_status FROM "{table}"'
            )
            missing_fields = 0
            non_current_status = 0
            unmapped_sources = 0
            source_paths: set[str] = set()
            unmapped_examples: set[str] = set()
            status_counts: dict[str, int] = {}
            confidence_counts: dict[str, int] = {}
            method_counts: dict[str, int] = {}
            for row in connection.execute(query):
                total_audited_rows += 1
                values = dict(row)
                if any(values.get(field) in (None, "") for field in REQUIRED_PROVENANCE):
                    missing_fields += 1
                status = str(values.get("verification_status") or "")
                confidence = str(values.get("confidence") or "")
                method = str(values.get("extraction_method") or "")
                status_counts[status] = status_counts.get(status, 0) + 1
                confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
                method_counts[method] = method_counts.get(method, 0) + 1
                if status != "current_client_extracted":
                    non_current_status += 1
                relative = source_relative(str(values.get("source_file") or ""))
                source_paths.add(relative)
                if relative not in reference_paths:
                    unmapped_sources += 1
                    if len(unmapped_examples) < 20:
                        unmapped_examples.add(relative)

            failures = missing_fields + non_current_status + unmapped_sources
            total_failures += failures
            result.update(
                {
                    "audited": True,
                    "missing_required_values": missing_fields,
                    "non_current_verification_status": non_current_status,
                    "unmapped_source_rows": unmapped_sources,
                    "unmapped_source_examples": sorted(unmapped_examples),
                    "distinct_source_files": len(source_paths),
                    "verification_status_counts": dict(sorted(status_counts.items())),
                    "confidence_counts": dict(sorted(confidence_counts.items())),
                    "extraction_method_counts": dict(sorted(method_counts.items())),
                    "pass": failures == 0,
                }
            )
            table_results[table] = result
    finally:
        connection.close()

    passed = total_failures == 0 and total_audited_rows == total_domain_rows
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "database": str(database),
        "scope": "published current-client relational snapshot",
        "status": "pass" if passed else "fail",
        "reference_source_files": len(reference_paths),
        "domain_rows": total_domain_rows,
        "audited_rows": total_audited_rows,
        "failures": total_failures,
        "legacy_guard": {
            "legacy_contamination_detected": False if passed else None,
            "legacy_absence_proven": False,
            "interpretation": (
                "No populated domain row lacks current-client status or a source path in the "
                "hashed Wonderland M manifest. This detects no legacy contamination, but it "
                "does not prove that external legacy facts could never have been copied into a field."
            ),
        },
        "tables": table_results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")

    populated = [(name, value) for name, value in table_results.items() if value["rows"]]
    lines = [
        "# Provenance Audit",
        "",
        f"Generated: {report['generated_at']}",
        "",
        f"Overall status: **{report['status'].upper()}**",
        "",
        "Every populated domain row was checked for required provenance fields, a",
        "`current_client_extracted` verification status, and a source path present in",
        "the hashed Wonderland M source manifest.",
        "",
        "| Table | Rows | Audited | Missing fields | Non-current status | Unmapped source rows | Result |",
        "|---|---:|:---:|---:|---:|---:|:---:|",
    ]
    for name, value in populated:
        if name == "source_files":
            lines.append(f"| `{name}` | {value['rows']} | manifest | 0 | 0 | 0 | reference |")
        else:
            lines.append(
                f"| `{name}` | {value['rows']} | {'yes' if value['audited'] else 'no'} | "
                f"{value.get('missing_required_values', value['rows'])} | "
                f"{value.get('non_current_verification_status', value['rows'])} | "
                f"{value.get('unmapped_source_rows', value['rows'])} | "
                f"{'pass' if value.get('pass') else 'fail'} |"
            )
    lines.extend(
        [
            "",
            "## Legacy-game guard",
            "",
            "No populated domain row lacks current-client status or a source path in the",
            "hashed modern Wonderland M manifest. This audit found no evidence of legacy",
            "Wonderland Online contamination. It deliberately does not claim that absence",
            "of legacy contamination is mathematically proven; semantic facts still require",
            "field-level current-client evidence.",
            "",
        ]
    )
    output.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": report["status"], "audited_rows": total_audited_rows, "failures": total_failures, "output": str(output)}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
