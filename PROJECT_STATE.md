# Wonderland Online M Indexer - Project State

Last updated: 2026-08-25 (America/Los_Angeles)

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

User-supplied XAPK/runtime inspection: **complete for the APKPure 1.1060.1 XAPK,
its publisher-signed base/ARM64 split APKs, and the adjacent Android app-data
export**. All 28,838 runtime-export files were hashed once and cached. The XAPK
IL2CPP schema is indexed, 51 Android-only bundle paths are identified, and 12
new item icons are preserved as asset-only evidence. The gameplay-domain record
gate remains closed.

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
- Supplied XAPK identity/signatures: **PASS**, package `com.x980.wlmobile`,
  version `1.1060.1`, version code `122`; both embedded APK v2 signatures and
  content digests verified with the known publisher certificate.
- Supplied Android runtime export: **28,838 files**, **1,453,213,358 bytes**,
  including **28,590 primary bundles** and **97 Unity cache data/info pairs**.
- Android-to-Steam normalized bundle paths: all **28,539** Steam bundle paths
  present, **51 added**, **0 missing**. Shared hashes are platform/content
  differences, not assumed semantic changes.
- XAPK IL2CPP schema: **PASS**, metadata v31, 33/33 targeted types and 12/12
  filename literals. Exact targeted semantic match to the prior Android APK.
- Android-only item asset evidence: **12 direct asset relationships** with
  validated 32x32 RGBA icons; gameplay names/details remain unresolved.

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

Published checkpoints:

- `b58fcd8` - Verify current Wonderland M source provenance
- `fa89006` - Load index sections on demand
- `7dd04c2` - Record validated project checkpoints
- `7b9f9de` - Record official client candidate inspection

## Repository and source locations

- Repository: `C:\Users\josue\OneDrive\Documents\GitHub\Wonderland-Online-M-Indexer`
- Read-only game source: `D:\SteamLibrary\steamapps\common\WLM`
- Plan: `C:\Users\josue\Downloads\Wonderland_Online_M_Indexer_Plan.md`
- Supplied primary XAPK:
  `C:\Users\josue\Downloads\Wonderland M\Wonderland+M_1.1060.1_APKPure.xapk`
- Supplied Android app-data export:
  `C:\Users\josue\Downloads\Wonderland M\APK FILES\com.x980.wlmobile`
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

Supplied XAPK-specific identity:

- XAPK SHA-256:
  `eff3324b28fe324dc3457895d4bb746647dbbfa7c01281c23a20fc4d7ab18f26`
- ARM64 `libil2cpp.so` SHA-256:
  `2286adf1320cd7710eb3f3e9d7d6b1822d6d5740b4a33879a630b79c6d64abc2`
- XAPK `global-metadata.dat` SHA-256:
  `1b0183c154c8a172fdd1cdc3ff41ea8c8136a48d79aeedbbf3b672e9d89aec63`
- Publisher certificate SHA-256:
  `a1402d411ca1fd484cedbaa2affcd62e2a8b7ce52fe57be1d9593a6a702e9882`

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
- Supplied 1.1060.1 XAPK: fully unpacked in an isolated `work/` directory;
  every XAPK/APK member and every supplied runtime-export file inventoried and
  hashed without changing the originals.
- Supplied Android runtime tree: 28,590 primary UnityFS bundles inventoried;
  97 additional Unity cache data/info pairs preserved and classified.
- Android-only item bundles: 12 copied to an isolated AssetRipper input,
  successfully resolved to prefab containers and visually checked Texture2D
  icons. Role and role-card bundles remained unparsed.
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

The published database counts above are unchanged. Separate current-Android
evidence now records 12 additional item asset IDs (`3941`, `4890`-`4894`,
`4898`, `4899`, `6275`-`6277`, `6280`) and icons under
`source_manifest/android_export/`; they have not been promoted into gameplay
records or the website.

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
- The supplied APKPure XAPK and adjacent 1.45 GB Android app-data export also
  contain none of the 12 payloads as ordinary files or APK members.
- Il2CppDumper could not read XAPK binaries from the protected Documents/Codex
  path. Byte-identical copies under an isolated local temporary directory
  dumped successfully. Its nonzero result occurred only after dump completion
  at the configured redirected-input prompt.
- AssetRipper warned on unrelated built-in Unity/default resources, but every
  targeted Android-only item bundle, prefab relationship, and PNG exported and
  validated successfully.
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
5. The Android client directly stores the supplied primary bundle categories
   under its `files` directory and keeps streaming count/version markers plus
   `HadLoad` marker files. The exact update semantics and whether other
   app-private storage contains custom tables remain unresolved.
6. The 97 supplied Unity cache bundles are a second byte-unique asset set,
   primarily named for map preload/footprint and fight/talk UI. Their paths do
   not establish map or gameplay relationships without object-level parsing.

## Next recommended actions

1. Statistically index the 97 supplied Unity cache bundles, beginning with
   `atlas_footprint_*` and `atlas_preload_mappreload_*`, and link only direct
   asset relationships.
2. Trace the XAPK IL2CPP methods that create/read `HadLoad`,
   `MaxStreamingAssets`, and `StreamingAssetsVision` to establish their exact
   update semantics and storage paths.
3. If an additional lawful, non-account-specific app-private export becomes
   available without rooting or bypassing access controls, inventory it against
   the 12 expected payload names before parsing anything.
4. When payload bytes exist, fingerprint them first, preserve them read-only
   outside the repo, and build deterministic parsers from the indexed schema.
5. Prioritize `NNpc` + encounter/event structures + `NSceneData`, then link
   drops/items. Do not infer spawn relationships from NPC stats or names.
6. Implement the flexible `source_type + source_id -> drop_table` relationship
   when current drop records exist; do not assume all drops attach to monsters.
7. Add manual current-game observations only as Grade B evidence with build,
   screenshot/notes, coordinates, and reproducible steps.
8. Run validation after every generated-data or frontend change.

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

The supplied XAPK/runtime pass added:

```powershell
python tools\inventory_android_source.py `
  --xapk "C:\Users\josue\Downloads\Wonderland M\Wonderland+M_1.1060.1_APKPure.xapk" `
  --app-data-dir "C:\Users\josue\Downloads\Wonderland M\APK FILES\com.x980.wlmobile"

python tools\index_android_item_assets.py `
  --app-data-dir "C:\Users\josue\Downloads\Wonderland M\APK FILES\com.x980.wlmobile" `
  --assetripper-export <isolated-AssetRipper-output>
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
- `reports/android_runtime_export_inventory.md`
- `reports/android_new_item_assets.md`
- `reports/xapk_il2cpp_schema.md`
- `reports/xapk_android_runtime_pass.md`
- `source_manifest/android_export/android-source-inventory.json`
- `source_manifest/android_export/item-assets.json`
- `database/schema.sql`

## Resume checklist

1. Read this file and `CHATGPT_HANDOFF.md`.
2. Inspect `git status` and preserve unrelated user changes.
3. Re-run the installation comparison only if source hashes or Steam packaging
   changed.
4. Never promote a name, location, drop, or recipe without exact current-client
   or current-game evidence.
5. Update this file before stopping.
