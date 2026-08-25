# XAPK and Android runtime evidence pass

Generated: 2026-08-25 (America/Los_Angeles)

## 1. Completed work

- Read the existing project state, handoff, full repository tree, and prior
  official-client evidence before extracting anything.
- Preserved the supplied XAPK and Android app-data export unchanged.
- Fully unpacked `Wonderland+M_1.1060.1_APKPure.xapk` into an isolated `work/`
  directory and inventoried every outer and embedded APK member.
- Cryptographically verified APK Signature Scheme v2 signatures and content
  digests for both embedded APKs. Both use the same publisher certificate as the
  previously verified official APK.
- Hashed and classified all 28,838 files in the supplied Android app-data export.
- Compared all 28,590 downloaded Android Unity bundles with the 28,539-bundle
  Steam reference by normalized path, size, and SHA-256.
- Generated a fresh IL2CPP dump and indexed the 33 targeted static-data types and
  all 12 expected payload filename literals from the XAPK's exact ARM64 binaries.
- Parsed the 12 Android-only item bundles, extracted their icons, visually
  checked a contact sheet, and recorded direct asset relationships.
- Did not parse or publish the 37 Android-only role bundles.
- Added deterministic tools with a metadata cache; an unchanged full-source
  inventory now rechecks in about two seconds rather than rehashing 1.5 GB.

## 2. Generated files

- `tools/inventory_android_source.py`
- `tools/index_android_item_assets.py`
- `source_manifest/android_export/android-app-files.csv`
- `source_manifest/android_export/android-bundle-comparison.csv`
- `source_manifest/android_export/android-source-inventory.json`
- `source_manifest/android_export/xapk-inventory.json`
- `source_manifest/android_export/source-provenance.json`
- `source_manifest/android_export/item-assets.json`
- `source_manifest/android_export/item_icons/*.png`
- `reports/android_runtime_export_inventory.md`
- `reports/android_new_item_assets.md`
- `reports/xapk_il2cpp_schema.json`
- `reports/xapk_il2cpp_schema.md`

Large raw XAPK, APK, IL2CPP-dump, AssetRipper, and contact-sheet intermediates
remain outside the repository under the current Codex `work/` directory or an
isolated temporary directory.

## 3. Strongest findings

### Publisher-signed XAPK identity

- XAPK SHA-256:
  `eff3324b28fe324dc3457895d4bb746647dbbfa7c01281c23a20fc4d7ab18f26`
- Package: `com.x980.wlmobile`
- Version: `1.1060.1`; version code `122`
- Base APK SHA-256:
  `1bfe35004d541fc93666ca5ac33eed8cb5d36bf359d56177ef215eb99810a065`
- ARM64 split SHA-256:
  `90201c31013e79b7aa1c78b6cc0548dd74a264bfd4476c8db9edb8e5425f9dca`
- Publisher certificate SHA-256:
  `a1402d411ca1fd484cedbaa2affcd62e2a8b7ce52fe57be1d9593a6a702e9882`
- Both embedded APK v2 signatures and content digests: **valid**

The APKPure XAPK wrapper is recorded as a user-supplied third-party distribution
container. Publisher continuity applies to the embedded APKs, not to the wrapper.

### Supplied runtime bundle tree

The supplied package-data directory contains:

- 28,838 files; 1,453,213,358 bytes
- 28,590 primary downloaded UnityFS bundles
- 51 zero-length `HadLoad/HadLoad*.txt` marker files
- `files/streamingassetszip/MaxStreamingAssets.txt` with direct value `26`
- `files/streamingassetszip/StreamingAssetsVision.txt` with direct value `3`
- 97 Unity cache `__data`/`__info` pairs

All 97 Unity cache data files are byte-unique from the 28,590 primary bundle
files. Their paths identify map-preload, footprint, fight UI, and talk-message
assets, but the exact caching policy remains unresolved.

The Android bundle tree contains every normalized Steam bundle path plus 51
additional paths:

- 12 item bundles
- 37 role bundles
- 1 sound bundle
- 1 WEM element bundle

All 28,539 shared paths differ bytewise. Because these are Windows and Android
Unity bundles, the difference is recorded as `platform_or_content_difference`;
it is not treated as proof that every asset changed semantically.

### XAPK IL2CPP schema

- `libil2cpp.so` SHA-256:
  `2286adf1320cd7710eb3f3e9d7d6b1822d6d5740b4a33879a630b79c6d64abc2`
- `global-metadata.dat` SHA-256:
  `1b0183c154c8a172fdd1cdc3ff41ea8c8136a48d79aeedbbf3b672e9d89aec63`
- Metadata: `0xFAB11BAF`, version 31
- Target types indexed: 33/33
- Expected filename literals recovered: 12/12

The XAPK binaries differ from the previously inspected direct-download APK, but
their targeted type fields, properties, methods, and filename-literal values are
an exact semantic match. Compared with the Steam schema, only the already-known
platform-specific offsets in three `CDownloadUrlPathData` fields differ.

### Android-only item assets

Direct asset IDs `3941`, `4890`, `4891`, `4892`, `4893`, `4894`, `4898`, `4899`,
`6275`, `6276`, `6277`, and `6280` each resolve through:

`downloaded UnityFS bundle -> AssetBundle prefab container -> Atlas_Item_ID -> 32x32 RGBA icon`

These relationships are `direct_asset_relationship` evidence. Names, item
types, stats, recipes, sources, and other gameplay meanings remain unresolved.

## 4. Relationships resolved

- XAPK -> base APK and ARM64 split -> publisher certificate
- XAPK -> ARM64 `libil2cpp.so` + `global-metadata.dat` -> targeted loader schema
- Android package directory -> primary downloaded bundle categories
- Android primary bundle path -> corresponding Steam logical bundle path
- Android-only item bundle -> item asset ID -> prefab reference -> extracted icon
- Unity cache directory name -> cached UnityFS bytes and cache metadata pair

No monster -> spawn -> map -> drop -> item chain was resolved because none of
the required current gameplay records is present.

## 5. Unresolved IDs and references

The following expected payloads have zero ordinary-file or APK-member hits in
both the XAPK and supplied app-data export:

- `NItem.Dat`, `NItem_EN.Dat`
- `NNpc.dat`, `NNpc_EN.dat`
- `NSceneData.dat`, `NSceneData_EN.dat`
- `NSkill.dat`, `NSkill_EN.dat`
- `NTalk.dat`, `NTalk_EN.dat`
- `NCompound2.dat`
- `NFormula.dat`

`AllFileList.txt` and `packagesversion.txt` are also absent. The 12 Android-only
item IDs have asset evidence only. The 97 Unity cache bundles have not yet been
object-indexed. The meanings of `MaxStreamingAssets=26`,
`StreamingAssetsVision=3`, and the 51 historical/current `HadLoad` markers are
not fully proven by this filesystem snapshot alone.

## 6. Failed or qualified methods

- Il2CppDumper could not read copied inputs while they remained under the
  protected Documents/Codex directory. Copying the same verified bytes to an
  isolated local temporary directory succeeded.
- Il2CppDumper emitted `This file may be protected`, then completed its dump,
  struct, and dummy-DLL stages. Its final nonzero process result came from the
  configured `Press any key to exit` call under redirected input.
- AssetRipper emitted failures for unrelated built-in Unity editor/default
  resources during primary-content export. All 12 targeted item AssetBundles,
  prefab references, and Texture2D PNGs exported and validated successfully.
- Exact filename scans, XAPK member inventory, and runtime-export inventory did
  not recover any of the 12 custom payloads. No speculative decompression or URL
  guessing was repeated.

## 7. Systems still requiring investigation

- Any lawful non-account-specific app-private storage not included in this
  `cache` + `files` export
- Code paths that create/consume `HadLoad`, `MaxStreamingAssets`, and
  `StreamingAssetsVision`
- Object-level contents of the 97 Unity cache bundles
- Semantic contents of the 12 item assets once current item-record bytes exist
- Delivery and local storage of `N*.dat` payloads, if the current client still
  receives them at all

The published SQLite database and website remain unchanged in this pass. The 12
new icons are evidence artifacts, not promoted gameplay records.

## 8. Exact next actions

1. Statistically index the 97 supplied Unity cache bundles, prioritizing
   `atlas_footprint_*` and `atlas_preload_mappreload_*`, and link any recovered
   textures/prefabs to existing map assets without inventing map names.
2. Trace the `HadLoad` and streaming-version marker read/write methods in the
   XAPK IL2CPP dump to establish their update semantics and directory selection.
3. If the user can lawfully provide additional non-account-specific app-private
   files without rooting, bypassing access controls, or including account data,
   inventory them against the 12 expected payload names before any parser work.
4. If payload bytes are recovered, hash and preserve them first, then implement
   deterministic parsers from `reports/xapk_il2cpp_schema.json`, starting with
   `NNpc` + encounter/event data + `NSceneData` and then drops/items.
5. Keep the gameplay-domain gate closed until those records exist; do not import
   legacy Wonderland Online tables or infer gameplay meaning from the 12 icons.
