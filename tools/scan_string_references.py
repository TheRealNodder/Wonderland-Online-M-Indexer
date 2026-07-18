#!/usr/bin/env python3
"""Find exact current-client filename references with byte-offset evidence."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Iterable


DEFAULT_PATTERNS = (
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
    "StreamingAssets_1.zip",
)
DEFAULT_EXTENSIONS = {
    "",
    ".assets",
    ".config",
    ".dat",
    ".dll",
    ".exe",
    ".info",
    ".json",
    ".resource",
    ".ress",
    ".txt",
}
READ_CHUNK = 4 * 1024 * 1024


def normalize(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def excluded(relative_path: str) -> bool:
    lowered = f"/{normalize(relative_path).casefold()}/"
    return any(token in lowered for token in ("/role/", "/rolecard/", "/jrole/", "atlas_role", "atlas_jrole"))


def printable_context(data: bytes, offset: int, length: int) -> str:
    start = max(0, offset - 36)
    end = min(len(data), offset + length + 36)
    return "".join(chr(value) if 32 <= value < 127 else "." for value in data[start:end])


def scan_stream(stream: BinaryIO, patterns: tuple[str, ...]) -> list[dict[str, object]]:
    needles: list[tuple[str, str, bytes]] = []
    for pattern in patterns:
        needles.append((pattern, "ascii", pattern.encode("ascii")))
        needles.append((pattern, "utf-16le", pattern.encode("utf-16le")))
    overlap = max(len(needle) for _, _, needle in needles) - 1
    hits: list[dict[str, object]] = []
    tail = b""
    absolute = 0
    while True:
        chunk = stream.read(READ_CHUNK)
        if not chunk:
            break
        data = tail + chunk
        base = absolute - len(tail)
        searchable = data.lower()
        for pattern, encoding, needle in needles:
            lowered_needle = needle.lower()
            start = 0
            while True:
                found = searchable.find(lowered_needle, start)
                if found < 0:
                    break
                absolute_offset = base + found
                if absolute_offset >= 0 and (not tail or found + len(needle) > len(tail)):
                    hits.append(
                        {
                            "pattern": pattern,
                            "encoding": encoding,
                            "matched_text": data[found : found + len(needle)].decode(encoding, "replace"),
                            "byte_offset": absolute_offset,
                            "byte_offset_hex": f"0x{absolute_offset:X}",
                            "context": printable_context(data, found, len(needle)),
                        }
                    )
                start = found + 1
        absolute += len(chunk)
        tail = data[-overlap:] if overlap else b""
    return hits


def iter_files(game_dir: Path, include_unity_bundles: bool) -> Iterable[Path]:
    for path in sorted((candidate for candidate in game_dir.rglob("*") if candidate.is_file()), key=lambda p: p.as_posix().lower()):
        relative = path.relative_to(game_dir).as_posix()
        if excluded(relative):
            continue
        if include_unity_bundles or path.suffix.casefold() in DEFAULT_EXTENSIONS or path.suffix.casefold() == ".zip":
            yield path


def markdown_report(result: dict[str, object]) -> str:
    hits = result["hits"]
    counts = Counter(str(hit["pattern"]) for hit in hits)
    lines = [
        "# Current Wonderland M string-reference scan",
        "",
        f"- Scope: {result['scope']}",
        f"- Files scanned: `{result['files_scanned']}`",
        f"- Bytes scanned: `{result['bytes_scanned']}`",
        f"- Exact case-insensitive hits: `{len(hits)}`",
        "- Imported legacy Wonderland Online evidence: **No**",
        "- Role, role-card, and jrole paths: **Excluded**",
        "",
        "## Target summary",
        "",
        "| Target | Hits |",
        "|---|---:|",
    ]
    for pattern in result["patterns"]:
        lines.append(f"| `{pattern}` | {counts.get(str(pattern), 0)} |")
    lines.extend(
        [
            "",
            "## Exact evidence",
            "",
            "| Target | Matched text | Source | Encoding | Byte offset |",
            "|---|---|---|---|---:|",
        ]
    )
    for hit in hits:
        source = str(hit["logical_file"]).replace("|", "\\|")
        lines.append(
            f"| `{hit['pattern']}` | `{hit['matched_text']}` | `{source}` | "
            f"`{hit['encoding']}` | `{hit['byte_offset_hex']}` |"
        )
    lines.extend(
        [
            "",
            "The filename references prove that the verified current client knows these data",
            "payload names. They do not prove that the payload bytes are present in the installed",
            "tree; the full logical manifest comparison found no such files.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-dir", required=True, type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=repository / "reports" / "current_client_string_references.json",
    )
    parser.add_argument(
        "--output-markdown",
        type=Path,
        default=repository / "reports" / "current_client_string_references.md",
    )
    parser.add_argument("--pattern", action="append", dest="patterns")
    parser.add_argument("--include-unity-bundles", action="store_true")
    args = parser.parse_args()

    game_dir = args.game_dir.resolve()
    output = args.output.resolve()
    output_markdown = args.output_markdown.resolve()
    patterns = tuple(args.patterns) if args.patterns else DEFAULT_PATTERNS
    if not game_dir.is_dir():
        raise SystemExit(f"Game directory not found: {game_dir}")
    if any(candidate == game_dir or game_dir in candidate.parents for candidate in (output, output_markdown)):
        raise SystemExit("Outputs must not be written inside the game installation")

    evidence: list[dict[str, object]] = []
    files_scanned = 0
    bytes_scanned = 0
    archives_scanned = 0
    for path in iter_files(game_dir, args.include_unity_bundles):
        relative = path.relative_to(game_dir).as_posix()
        if path.suffix.casefold() == ".zip" and zipfile.is_zipfile(path):
            archives_scanned += 1
            with zipfile.ZipFile(path) as archive:
                for info in sorted((member for member in archive.infolist() if not member.is_dir()), key=lambda i: i.filename.lower()):
                    logical = normalize(f"{Path(relative).parent.as_posix()}/{info.filename}")
                    if excluded(logical):
                        continue
                    if not args.include_unity_bundles and Path(info.filename).suffix.casefold() not in DEFAULT_EXTENSIONS:
                        continue
                    with archive.open(info) as stream:
                        hits = scan_stream(stream, patterns)
                    files_scanned += 1
                    bytes_scanned += info.file_size
                    for hit in hits:
                        hit.update(
                            {
                                "source_file": relative,
                                "logical_file": logical,
                                "source_kind": "zip_member",
                                "member_path": normalize(info.filename),
                            }
                        )
                        evidence.append(hit)
            continue

        with path.open("rb") as stream:
            hits = scan_stream(stream, patterns)
        files_scanned += 1
        bytes_scanned += path.stat().st_size
        for hit in hits:
            hit.update(
                {
                    "source_file": relative,
                    "logical_file": relative,
                    "source_kind": "physical_file",
                    "member_path": "",
                }
            )
            evidence.append(hit)

    evidence.sort(key=lambda hit: (str(hit["logical_file"]), int(hit["byte_offset"]), str(hit["pattern"]), str(hit["encoding"])))
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "game_dir": str(game_dir),
        "scope": "current Wonderland M client only",
        "legacy_game_evidence_imported": False,
        "patterns": list(patterns),
        "include_unity_bundles": args.include_unity_bundles,
        "files_scanned": files_scanned,
        "bytes_scanned": bytes_scanned,
        "archives_scanned": archives_scanned,
        "hits": evidence,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    output_markdown.write_text(markdown_report(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "output_markdown": str(output_markdown),
                "files_scanned": files_scanned,
                "hits": len(evidence),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
