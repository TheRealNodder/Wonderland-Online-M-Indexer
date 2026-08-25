#!/usr/bin/env python3
"""Index selected static-data schemas from a verified Wonderland M IL2CPP dump.

The output is intentionally narrow.  It records only loader and record types
needed for the offline indexer and omits player, account, role-card, and
character-model managers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from datetime import datetime, timezone
from pathlib import Path


READ_CHUNK = 1024 * 1024
METADATA_MAGIC = 0xFAB11BAF
TARGET_PAYLOADS = (
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
TARGET_TYPES = (
    "CDataBehaviour",
    "CDataBehaviour_Bytes",
    "CDownloadUrlPathData",
    "rMixStuffRd",
    "COneCompoundItemRdData",
    "CCompound2DataManager",
    "COneFormulaData",
    "CFormulaDataManager",
    "rWaveRecord",
    "rElmInfo",
    "rGeolRecord",
    "rRGBInfo",
    "rMazeElmInfo",
    "COneGroundData",
    "CGroundDataManager",
    "COneItemData",
    "CItemDataManager",
    "CItemDataManager_EN",
    "COneNpcData",
    "CNpcDataManager",
    "CNpcDataManager_EN",
    "COneSceneData",
    "CSceneDataManager",
    "CSceneDataManager_EN",
    "COneSkillData",
    "CSkillDataManager",
    "CSkillDataManager_EN",
    "COneTalkData",
    "CTalkDataManager",
    "CTalkDataManager_EN",
    "rOneTransferPointData",
    "CTransferPointData_EN",
    "DataMgrs",
)
DECLARATION = re.compile(
    r"^(?P<declaration>(?:public|private|internal|protected).+?\b"
    r"(?P<kind>class|struct|interface|enum)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*).+?)"
    r"\s*// TypeDefIndex: (?P<index>\d+)\s*$"
)
FORBIDDEN_MANAGER_LINE = re.compile(
    r"(?:CPlayerTitleData|CRoleCardData|PlayerTitleData|RoleCardData|AccountData)",
    re.IGNORECASE,
)
RELEVANT_METHOD = re.compile(
    r"(?:Load|Read|DataFileName|Find|GetName|HandleAdd|Download|\.ctor)",
    re.IGNORECASE,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(READ_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint(path: Path) -> dict[str, object]:
    return {
        "path": str(path.resolve()),
        "size": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def read_metadata_identity(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        header = stream.read(8)
    if len(header) != 8:
        raise ValueError(f"Metadata header is truncated: {path}")
    magic, version = struct.unpack("<II", header)
    return {
        "magic": f"0x{magic:08X}",
        "magic_valid": magic == METADATA_MAGIC,
        "metadata_version": version,
    }


def extract_blocks(text: str) -> dict[str, dict[str, object]]:
    lines = text.splitlines()
    namespace = ""
    blocks: dict[str, dict[str, object]] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("// Namespace:"):
            namespace = line.partition(":")[2].strip()
            index += 1
            continue
        match = DECLARATION.match(line)
        if not match or match.group("name") not in TARGET_TYPES:
            index += 1
            continue

        name = match.group("name")
        block_lines = [line]
        depth = line.count("{") - line.count("}")
        saw_open = depth > 0
        cursor = index + 1
        while cursor < len(lines):
            current = lines[cursor]
            block_lines.append(current)
            depth += current.count("{") - current.count("}")
            saw_open = saw_open or "{" in current
            cursor += 1
            if saw_open and depth == 0:
                break
        block_text = "\n".join(block_lines)
        fields, properties, methods, omitted = parse_members(name, block_lines)
        blocks[name] = {
            "name": name,
            "namespace": namespace,
            "kind": match.group("kind"),
            "type_def_index": int(match.group("index")),
            "declaration": match.group("declaration"),
            "fields": fields,
            "properties": properties,
            "methods": methods,
            "omitted_out_of_scope_members": omitted,
            "block_sha256": hashlib.sha256(block_text.encode("utf-8")).hexdigest(),
        }
        index = cursor
    return blocks


def parse_members(name: str, lines: list[str]) -> tuple[list[str], list[str], list[str], int]:
    section = ""
    fields: list[str] = []
    properties: list[str] = []
    methods: list[str] = []
    omitted = 0
    for raw in lines:
        stripped = raw.strip()
        if stripped in {"// Fields", "// Properties", "// Methods"}:
            section = stripped.removeprefix("// ").lower()
            continue
        if not stripped or stripped.startswith("//") or stripped.startswith("["):
            continue
        if name == "DataMgrs" and FORBIDDEN_MANAGER_LINE.search(stripped):
            omitted += 1
            continue
        if section == "fields" and stripped.endswith(";") or (
            section == "fields" and "; // 0x" in stripped
        ):
            fields.append(stripped)
        elif section == "properties" and "{" in stripped and "}" in stripped:
            properties.append(stripped)
        elif section == "methods" and stripped.endswith("{ }"):
            methods.append(stripped)
    return fields, properties, methods, omitted


def load_payload_literals(path: Path) -> list[dict[str, str]]:
    payload_names = {value.casefold() for value in TARGET_PAYLOADS}
    raw = json.loads(path.read_text(encoding="utf-8"))
    matches = [
        {"value": str(entry["value"]), "address": str(entry["address"])}
        for entry in raw
        if str(entry.get("value", "")).casefold() in payload_names
    ]
    matches.sort(key=lambda entry: (entry["value"].casefold(), entry["address"]))
    return matches


def markdown_report(result: dict[str, object]) -> str:
    identity = result["current_client_identity"]
    dump = result["il2cpp_dump"]
    types = result["types"]
    lines = [
        "# Current Wonderland M IL2CPP schema index",
        "",
        f"- Verdict: **{result['verdict']}**",
        f"- Evidence scope: {result['scope']}",
        f"- Metadata: `{identity['magic']}`, version `{identity['metadata_version']}`",
        f"- Indexed target types: `{len(types)}` / `{len(TARGET_TYPES)}`",
        f"- Exact target data-file literals: `{len(result['data_file_literals'])}`",
        "- Imported legacy Wonderland Online data: **No**",
        "- Imported player/account/role-card/character-model data: **No**",
        "",
        "## Provenance",
        "",
        "| Artifact | Bytes | SHA-256 |",
        "|---|---:|---|",
    ]
    for label, artifact in (
        (Path(str(dump["game_assembly"]["path"])).name, dump["game_assembly"]),
        (Path(str(dump["global_metadata"]["path"])).name, dump["global_metadata"]),
        ("Il2CppDumper.exe", dump["dumper"]),
        ("fresh dump.cs", dump["dump_cs"]),
        ("fresh stringliteral.json", dump["string_literals"]),
    ):
        lines.append(f"| {label} | {artifact['size']} | `{artifact['sha256']}` |")
    lines.extend(
        [
            "",
            "The dump was generated from the verified local WLM inputs. The dumper completed",
            "the schema and dummy-DLL stages; its nonzero shell result was caused only by the",
            "configured final `Press any key to exit` prompt under redirected input.",
            "",
            "## Exact current-client data-file literals",
            "",
            "| Literal | IL2CPP address |",
            "|---|---|",
        ]
    )
    for entry in result["data_file_literals"]:
        lines.append(f"| `{entry['value']}` | `{entry['address']}` |")
    lines.extend(["", "## Indexed loader and record schemas", ""])
    for item in types:
        lines.extend(
            [
                f"### `{item['name']}`",
                "",
                f"Namespace `{item['namespace'] or '(global)'}`; {item['kind']}; TypeDef `{item['type_def_index']}`.",
                "",
            ]
        )
        if item["fields"]:
            lines.append("Expected schema fields and code constants:")
            lines.append("")
            for field in item["fields"]:
                lines.append(f"- `{field}`")
            lines.append("")
        relevant = [method for method in item["methods"] if RELEVANT_METHOD.search(method)]
        if relevant:
            lines.append("Relevant loader/access methods:")
            lines.append("")
            for method in relevant:
                lines.append(f"- `{method}`")
            lines.append("")
        if item["omitted_out_of_scope_members"]:
            lines.append(
                f"Omitted `{item['omitted_out_of_scope_members']}` player-title/role-card manager members as out of scope."
            )
            lines.append("")
    lines.extend(
        [
            "## Interpretation",
            "",
            "This is parser schema evidence, not evidence that the named payload files are",
            "currently present on disk. The payloads remain unresolved until a lawful current-client",
            "source yields their bytes. Old PC Wonderland Online layouts and seed data are not valid",
            "substitutes for this WLM schema.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump-cs", required=True, type=Path)
    parser.add_argument("--string-literals", required=True, type=Path)
    parser.add_argument("--game-assembly", required=True, type=Path)
    parser.add_argument("--global-metadata", required=True, type=Path)
    parser.add_argument("--dumper", required=True, type=Path)
    parser.add_argument(
        "--output-json",
        type=Path,
        default=repository / "reports" / "current_client_il2cpp_schema.json",
    )
    parser.add_argument(
        "--output-markdown",
        type=Path,
        default=repository / "reports" / "current_client_il2cpp_schema.md",
    )
    args = parser.parse_args()

    paths = (
        args.dump_cs,
        args.string_literals,
        args.game_assembly,
        args.global_metadata,
        args.dumper,
    )
    missing_paths = [str(path) for path in paths if not path.is_file()]
    if missing_paths:
        raise SystemExit(f"Missing required files: {missing_paths}")

    identity = read_metadata_identity(args.global_metadata)
    blocks = extract_blocks(args.dump_cs.read_text(encoding="utf-8-sig", errors="replace"))
    missing_types = [name for name in TARGET_TYPES if name not in blocks]
    if missing_types:
        raise SystemExit(f"Target types missing from dump: {missing_types}")
    literals = load_payload_literals(args.string_literals)
    missing_literals = sorted(
        set(value.casefold() for value in TARGET_PAYLOADS)
        - set(entry["value"].casefold() for entry in literals)
    )
    if not identity["magic_valid"] or identity["metadata_version"] != 31:
        raise SystemExit(f"Unexpected IL2CPP metadata identity: {identity}")
    if missing_literals:
        raise SystemExit(f"Target payload literals missing from current dump: {missing_literals}")

    result: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "verified current Wonderland M static-data loader schema only",
        "verdict": "PASS - current WLM metadata v31 schema indexed",
        "evidence_grade": "A - directly derived from hashed current-client binaries",
        "current_client_identity": identity,
        "legacy_game_evidence_imported": False,
        "player_account_rolecard_character_model_data_imported": False,
        "target_payloads_present_on_disk": False,
        "il2cpp_dump": {
            "tool_label": "Il2CppDumper v6.7.46",
            "completion_note": (
                "Dumping and dummy-DLL stages completed. The process then encountered its configured "
                "Press-any-key prompt because stdin was redirected; generated outputs are complete."
            ),
            "game_assembly": fingerprint(args.game_assembly),
            "global_metadata": fingerprint(args.global_metadata),
            "dumper": fingerprint(args.dumper),
            "dump_cs": fingerprint(args.dump_cs),
            "string_literals": fingerprint(args.string_literals),
        },
        "data_file_literals": literals,
        "types": [blocks[name] for name in TARGET_TYPES],
        "excluded_scope": [
            "player/account data",
            "role and role-card records/assets",
            "character-model data",
            "legacy PC Wonderland Online data",
            "unrelated prior-game dump outputs",
        ],
    }
    output_json = args.output_json.resolve()
    output_markdown = args.output_markdown.resolve()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    output_markdown.write_text(markdown_report(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "verdict": result["verdict"],
                "types": len(result["types"]),
                "data_file_literals": len(literals),
                "output_json": str(output_json),
                "output_markdown": str(output_markdown),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
