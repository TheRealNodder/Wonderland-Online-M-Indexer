# Wonderland Online M Indexer - Project State

Last updated: 2026-07-17 (America/Los_Angeles)

Read this file before starting another extraction session. The target is the
current Steam/mobile Wonderland M client, not the original early-2000s
Wonderland Online PC release.

## Current extraction pass

Pass 3, assemblies and code: **current-client schema indexing complete for the
static item, NPC, scene, skill, talk, formula, compound, ground, and transfer
data loaders**.

Official package inspection: **complete for the approved Android APK and
standalone Windows bootstrap artifacts**. This pass added source metadata only;
the gameplay-domain record gate remains closed.

Pass 1 inventory and the previous non-character asset extraction remain valid:
the current home installation is logically byte-identical to the repository's
28,627-file source manifest after normalizing ZIP packaging.

## Current checkpoint verdict

- Full normalized logical comparison: **PASS**
- Reference paths: `28,627`
- Current physical files: `28,515`
- Current logical paths: `28,627`
- Matched: `28,627`; changed: `0`; missing: `0`; added: `0`
- `StreamingAssets_1.zip` contains exactly the 113 bundles that were loose in
  the reference snapshot; every member matches by size and SHA-256.
- Populated-domain provenance audit: **PASS**, `46,921` rows checked, no missing
  provenance, non-current status, or source path outside the hashed manifest.
- Fresh current-client IL2CPP schema index: **PASS**, 33/33 targeted types and
  all 12 target filename literals recovered.
- Browser index validation: **PASS**, 19 versioned section files, 46,028 search
  routes, no missing assets, and matching build/count/content hashes.
- Official APK identity/signature: **PASS**, package `com.x980.wlmobile`, version
  `1.1060.1`, APK v2 signature and content digest verified.
- Standalone-to-Steam comparison: 15 exact matches, 18 changed files, 28,594
  missing files; classified as a current bootstrap/base client, not a source
  replacement.
- Cross-platform WLM schema comparison: standalone exact match; APK semantic
  match with one platform-specific offset difference; 33 target types and all
  12 expected filenames present in every build.
- Candidate payload presence: **0/12** in the APK and **0/12** in the standalone
  bootstrap.

ChatGPT/Aleta checkpoint 1 accepted the modern-client provenance with a gate to
perform the full 28,627-path comparison. That gate is now satisfied.

ChatGPT/Aleta checkpoint 2 accepted the current-client/legacy boundary and the
section-sharding design. It required narrower asset wording, build-matched
shards, flexible drop sources, explicit reverse links, and plain UI/comments.
Those requirements are reflected in the current files and reports.

ChatGPT/Aleta checkpoint 3 returned **Pass** with no commit blockers. Its only
continuing restriction is to leave monster, spawn, drop, and recipe tables empty
until current-client payload records are found and parsed.

ChatGPT/Aleta checkpoint 4 returned **Pass for package provenance and
runtime-capture planning**. It confirmed that the artifacts belong to the
current Wonderland M product line, rejected gameplay-domain imports, and
recommended a normal Steam-client filesystem-first cache capture as the next
evidence step. The public CDN string remains an `endpoint_candidate`; stop
guessing paths after the observed HTTP 404 results.

Battery-mode recovery check: **PASS**. The forced 28,627-file logical hash
comparison, site validator, Python/JavaScript checks, SQLite provenance audit,
and Git whitespace check all completed after resume. Unchanged install checks
now reuse the saved full-hash result when physical path/size/timestamp metadata
matches; `compare_installation.py --force` always rehashes every logical file.

Local checkpoints (not pushed):

- `b58fcd8` - Verify current Wonderland M source provenance
- `fa89006` - Load index sections on demand
- `7dd04c2` - Record validated project checkpoints

## Repository and source locations

- Repository: `C:\Users\josue\OneDrive\Documents\GitHub\Wonderland-Online-M-Indexer`
- Read-only game source: `D:\SteamLibrary\steamapps\common\WLM`
- Plan: `C:\Users\josue\Downloads\Wonderland_Online_M_Indexer_Plan.md`
- Published database snapshot: `data/wonderland_m_complete.sqlite3`
- The old full extraction workspace
  `C:\Users\Public\Documents\WonderlandM_Atlas_Extraction` is not present on
  this computer.

## Detected engine and build

- Product: `WLM`; company: `980x`
- Engine: Unity IL2CPP
- Unity product version: `6000.0.58f2 (92dee566b325)`
- `WLM.exe` file version: `6000.0.58.9625317`
- UnityFS revision: `6000.0.58f2`
- IL2CPP metadata magic: `0xFAB11BAF`
- IL2CPP metadata version: `31`
- `GameAssembly.dll` SHA-256:
  `429da8cb9a4ba29a07fd7104d5055c1842bb007830e46085cdc6ed0b3239a9c6`
- `global-metadata.dat` SHA-256:
  `bb4011d548961d50345e36574b7213411fc4b8fb28d6a85e6093edfcd14f3aa6`

## Important formats

- UnityFS asset bundles (`.unity3d`), including item/map/maze/minimap/audio/UI
  categories.
- One ZIP container whose 113 members normalize to ordinary StreamingAssets
  bundle paths.
- Unity IL2CPP PE binaries and metadata v31.
- Custom byte tables referenced by exact `N*.dat` filenames.
- JSON runtime/site exports and SQLite normalized snapshot.
- PNG assets generated by the previous non-character extraction.

## Completed directories and scope

- Entire installed WLM tree: physical and logical filename/size/SHA-256 index.
- All 28,627 logical reference paths: exact comparison complete.
- All current executable/config identity files: fingerprinted.
- All non-character populated database rows: provenance audited.
- Current metadata strings: exact filename scan complete; role, role-card, and
  jrole paths excluded.
- Fresh WLM IL2CPP dump: targeted static-data types indexed; huge raw dump kept
  outside the repository.
- Official Android APK and standalone Windows bootstrap: downloaded only after
  approval, hashed, kept outside the repository, and statically inspected
  without executing either candidate.
- APK Unity bundle: AssetRipper recovered the current `DownloadUrlPath` text
  asset and platform/package-name rules; no named gameplay payload was present.
- Standard Unity persistent-data path
  `C:\Users\josue\AppData\LocalLow\980x\WLM`: searched by exact filename for
  the 12 target static payloads; no matches. Unrelated cache files were not read.
- Previous published extraction: 14,411 non-character bundles parsed with zero
  recorded parse failures; 14,128 role/rolecard bundles excluded.

## Populated tables

| Table | Rows | Current status |
|---|---:|---|
| `source_files` | 28,627 | complete hashed source manifest |
| `localization_entries` | 34,161 | direct current-client localization |
| `items` | 5,375 | item asset IDs/icons; not confirmed item records; all names/details unresolved |
| `maps` | 1,105 | map asset IDs/images; not confirmed maps; all names/floors/regions unresolved |
| `extraction_evidence` | 5,375 | item asset evidence |
| `audio_assets` | 890 | metadata only |
| `animation_assets` | 2 | metadata only |
| `unresolved_relationships` | 12 | exact missing payload references |

Monster, drop, encounter, NPC, shop, quest, recipe, portal, teleport, and
spawn/location tables contain zero rows. Zero means unresolved, not absent from
the game.

## Browser index delivery

- `data/manifest.json` is the only data file required at initial load (about
  7 KB instead of the previous 22.2 MB runtime JSON).
- Section data is stored in content-hashed files under `data/sections/` and is
  loaded when selected.
- Global search loads its content-hashed routing index only after the first
  query. Search supports type, numeric ID, name/text, localization key, asset
  name, and current-client source path.
- Every section/search wrapper records `build_id`, `schema_version`,
  `generated_at`, `record_count`, and `content_hash`.
- The manifest also fingerprints the SQLite snapshot. The validator rejects
  build/count/hash mismatches and missing shards.
- A failed shard shows `Section unavailable` instead of an empty-table message.
- Known relation ID fields in the detail view link to their target section.
- `reports/monster_drop_navigation_plan.md` defines the future monster, spawn,
  map, drop source/table/entry, and item pages plus reverse indexes.

## Unresolved identifiers and payloads

The current WLM metadata and fresh string-literal dump reference all of these,
but the full logical installation contains none of their payload bytes:

- `NItem.Dat`, `NItem_EN.Dat`
- `NNpc.dat`, `NNpc_EN.dat`
- `NSceneData.dat`, `NSceneData_EN.dat`
- `NSkill.dat`, `NSkill_EN.dat`
- `NTalk.dat`, `NTalk_EN.dat`
- `NCompound2.dat`
- `NFormula.dat`

The fresh schema records the corresponding expected fields, code CRC/bias
constants, and loader methods. This makes a reusable parser feasible once a
lawful, non-account-specific current-client copy of the payloads is supplied.

## Failed or rejected methods

- Searching only the Steam install cannot yield the 12 payloads; the complete
  logical manifest proves they are absent by filename.
- The standard Unity WLM persistent-data path also contains none of the 12 exact
  payload filenames. This does not prove the data is never downloaded under a
  different name or representation.
- Direct public-CDN guesses for named manifests, streaming ZIPs, and tables
  returned HTTP 404. The embedded base may require a current manifest, hashed
  names, another path, or runtime parameters. Additional URL guessing was
  rejected.
- The APK and standalone bootstrap reproduce the current loader schema but do
  not contain any of the 12 payload bytes. Package extraction alone cannot
  populate gameplay-domain tables.
- The pre-existing 2026-05-27 Il2CppDumper outputs in Downloads are from
  Evertale (`inc.zigza.evertale...`) and are rejected as wrong-client evidence.
- `wonderland_m_atlas_starter.zip` contains useful prototype structure but its
  16 early-farming monsters, drops, locations, and compounds are unverified
  seed claims and include a documented location conflict. They were not merged.
- A copied self-contained Il2CppDumper executable could not memory-map itself
  from the temporary work directory. Running the original executable against
  the verified WLM inputs produced the complete outputs.
- The dumper's shell result was nonzero only after generation, at its configured
  `Press any key to exit` prompt under redirected input. `dump.cs`,
  `stringliteral.json`, `script.json`, `il2cpp.h`, and DummyDll outputs exist.
- Runtime memory inspection, packet capture, client modification, authentication
  bypass, gameplay automation, and player/account/role/rolecard/character-model
  extraction are prohibited and were not attempted.

## Evidence grades

- **A:** direct hashed current-client file, object, schema, or exact relationship.
- **B:** recorded current-version manual gameplay evidence.
- **C:** current official/community/user claim awaiting client/manual match.
- **Rejected:** legacy-only, wrong-client, conflicting, or untraceable evidence.

Only Grade A/B evidence may populate confirmed domain relationships. See
`reports/source_quarantine.md`.

## Current hypotheses

1. The 12 custom tables are downloaded or server-supplied rather than packaged
   in the Steam installation. This is a hypothesis; filename strings and loader
   code alone do not prove delivery behavior.
2. `COneNpcData` plus a separate encounter/ground/event structure will be needed
   for the full monster -> spawn -> map chain; NPC stats alone do not prove a
   spawn location.
3. Scene IDs/names and item details can be parsed deterministically from the
   current schema if the exact payload bytes become available.
4. The 113-file physical difference is packaging-only and has no content drift.
5. The current client likely writes or expands additional non-account-specific
   data during normal startup/patching. This remains a hypothesis until a
   before/after filesystem manifest records the exact changed files.

## Next recommended actions

1. Do not import legacy or starter seed rows. Plan a normal verified Steam
   launch with before/after filesystem manifests of likely client data
   locations. Prefer files written before login and do not use Reload Data on
   the first observation.
2. After the client closes, copy only new or changed non-account-specific files
   to an isolated evidence folder and record original path, timestamps, size,
   SHA-256, and comparison against the 12 expected payload filenames and named
   manifest/streaming package literals.
3. When payload bytes exist, fingerprint them first, preserve them read-only
   outside the repo, and build deterministic parsers from the indexed schema.
4. Prioritize `NNpc` + encounter/event structures + `NSceneData`, then link
   drops/items. Do not infer spawn relationships from NPC stats or names.
5. Implement the flexible `source_type + source_id -> drop_table` relationship
   when current drop records exist; do not assume all drops attach to monsters.
6. Add manual current-game observations only as Grade B evidence with build,
   screenshot/notes, coordinates, and reproducible steps.
7. Run validation after every generated-data or frontend change.

## Last successful commands

```powershell
python tools\validate_site.py --site-dir .

python tools\scan_string_references.py --game-dir "D:\SteamLibrary\steamapps\common\WLM"

python tools\index_il2cpp_schema.py `
  --dump-cs "C:\Users\josue\Documents\Codex\2026-07-17\c-users-josue-onedrive-documents-github\work\wlm_il2cpp_current\out\dump.cs" `
  --string-literals "C:\Users\josue\Documents\Codex\2026-07-17\c-users-josue-onedrive-documents-github\work\wlm_il2cpp_current\out\stringliteral.json" `
  --game-assembly "D:\SteamLibrary\steamapps\common\WLM\GameAssembly.dll" `
  --global-metadata "D:\SteamLibrary\steamapps\common\WLM\WLM_Data\il2cpp_data\Metadata\global-metadata.dat" `
  --dumper "C:\Users\josue\Downloads\Il2CppDumper-win-v6.7.46\Il2CppDumper.exe"
```

Official candidate inspection also reused:

```powershell
python tools\compare_installation.py `
  --game-dir <normalized-standalone-directory> `
  --database data\wonderland_m_complete.sqlite3 `
  --output-dir <isolated-comparison-directory> `
  --force

python tools\index_il2cpp_schema.py `
  --dump-cs <candidate-dump.cs> `
  --string-literals <candidate-stringliteral.json> `
  --game-assembly <candidate-code-binary> `
  --global-metadata <candidate-global-metadata.dat> `
  --dumper "C:\Users\josue\Downloads\Il2CppDumper-win-v6.7.46\Il2CppDumper.exe"
```

## Last generated reports

- `source_manifest/home_install/install-comparison.md`
- `reports/provenance_audit.md`
- `reports/current_client_string_references.md`
- `reports/current_client_il2cpp_schema.md`
- `reports/source_quarantine.md`
- `reports/spawn_location_report.md`
- `reports/runtime_index_profile.md`
- `reports/runtime_index_sharding.md`
- `reports/monster_drop_navigation_plan.md`
- `reports/official_client_candidate_inspection.md`
- `source_manifest/official_packages.json`
- `database/schema.sql`

## Resume checklist

1. Read this file and `CHATGPT_HANDOFF.md`.
2. Inspect `git status` and preserve unrelated user changes.
3. Re-run the installation comparison only if source hashes or Steam packaging
   changed.
4. Never promote a name, location, drop, or recipe without exact current-client
   or current-game evidence.
5. Update this file before stopping.
