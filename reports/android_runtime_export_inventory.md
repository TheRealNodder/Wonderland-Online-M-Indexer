# Android XAPK and Runtime Export Inventory

Generated: 2026-08-25T18:00:56.131740+00:00

## Verdict

The supplied XAPK and Android app-data export were read only. The XAPK identifies
package `com.x980.wlmobile`, version `1.1060.1`,
and version code `122`. The app-data export contains a
complete-looking downloaded Unity bundle tree plus non-gameplay cache metadata,
but none of the 12 expected custom `N*.dat` payloads is present as an ordinary
file or APK member. The gameplay-domain record gate therefore remains closed.

Role and role-card bundles are represented only by path, size, and hash metadata.
No character model was parsed, rendered, or published.

## XAPK

- Source: `C:\Users\josue\Downloads\Wonderland M\Wonderland+M_1.1060.1_APKPure.xapk`
- Bytes: `90,831,531`
- SHA-256: `eff3324b28fe324dc3457895d4bb746647dbbfa7c01281c23a20fc4d7ab18f26`
- Outer entries: `4`

| Embedded APK | Bytes | SHA-256 | Entries |
|---|---:|---|---:|
| `com.x980.wlmobile.apk` | 64,360,336 | `1bfe35004d541fc93666ca5ac33eed8cb5d36bf359d56177ef215eb99810a065` | 4,236 |
| `config.arm64_v8a.apk` | 26,387,149 | `90201c31013e79b7aa1c78b6cc0548dd74a264bfd4476c8db9edb8e5425f9dca` | 10 |

`source-provenance.json` records the separate static signature verification that
establishes publisher-certificate continuity and APK v2 content-digest validity.
This inventory does not infer signature validity from the XAPK container itself.

## Android app-data export

- Source: `C:\Users\josue\Downloads\Wonderland M\APK FILES\com.x980.wlmobile`
- Files: `28,838`
- Bytes: `1,453,213,358`
- Unity cache data/info files: `97` / `97`
- Unity cache directories with exact data/info pairs: `97`
- Unity cache pair counts match: `True`
- Unity cache files matching primary bundle bytes: `0`
- Unity cache files byte-unique from the primary bundle tree: `97`

| Classified purpose | Files | Bytes |
|---|---:|---:|
| `download_completion_marker` | 51 | 0 |
| `download_version_or_count_marker` | 2 | 3 |
| `downloaded_unity_bundle:bgm` | 36 | 29,645,495 |
| `downloaded_unity_bundle:cg` | 81 | 26,509,893 |
| `downloaded_unity_bundle:fightbackground` | 123 | 22,246,763 |
| `downloaded_unity_bundle:fightlight3d` | 71 | 2,503,254 |
| `downloaded_unity_bundle:form` | 246 | 52,730,464 |
| `downloaded_unity_bundle:item` | 4,665 | 54,248,009 |
| `downloaded_unity_bundle:itemani` | 55 | 1,770,879 |
| `downloaded_unity_bundle:lights` | 615 | 30,751,226 |
| `downloaded_unity_bundle:map` | 1,516 | 130,539,788 |
| `downloaded_unity_bundle:maze` | 268 | 4,999,672 |
| `downloaded_unity_bundle:minimap` | 645 | 10,775,902 |
| `downloaded_unity_bundle:particle` | 16 | 433,455 |
| `downloaded_unity_bundle:role` | 14,156 | 939,484,957 |
| `downloaded_unity_bundle:rolecard` | 9 | 6,446,551 |
| `downloaded_unity_bundle:sound` | 213 | 4,467,916 |
| `downloaded_unity_bundle:sound.unity3d` | 1 | 2,188,332 |
| `downloaded_unity_bundle:wem` | 5,874 | 95,963,257 |
| `graphics_pipeline_cache` | 1 | 69,593 |
| `unity_runtime_cache_data` | 97 | 37,435,718 |
| `unity_runtime_cache_metadata` | 97 | 2,231 |

Observed download-state markers:

- `files/streamingassetszip/MaxStreamingAssets.txt` = `26`
- `files/streamingassetszip/StreamingAssetsVision.txt` = `3`

The 51 `HadLoad/HadLoad*.txt` files are zero-length marker files. They are
preserved in the full CSV inventory and are not interpreted as package contents.

## Steam bundle comparison

Android and Steam bundle paths were normalized below their respective
StreamingAssets roots. A differing byte hash can reflect platform-specific Unity
serialization, compression, or content; it is not automatically a gameplay-data
change.

| Measurement | Count |
|---|---:|
| Android downloaded bundles | 28,590 |
| Steam reference bundles | 28,539 |
| `added_in_android_export` | 51 |
| `platform_or_content_difference` | 28,539 |

### Added Android paths

- `item/atlas_item_3941.unity3d`
- `item/atlas_item_4890.unity3d`
- `item/atlas_item_4891.unity3d`
- `item/atlas_item_4892.unity3d`
- `item/atlas_item_4893.unity3d`
- `item/atlas_item_4894.unity3d`
- `item/atlas_item_4898.unity3d`
- `item/atlas_item_4899.unity3d`
- `item/atlas_item_6275.unity3d`
- `item/atlas_item_6276.unity3d`
- `item/atlas_item_6277.unity3d`
- `item/atlas_item_6280.unity3d`
- `role/atlas_role_12178_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_12179_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_12218_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_12450_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_12451_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_13178_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_13179_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_13218_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_13450_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_13451_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_14178_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_14179_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_14218_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_14450_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_14451_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_15178_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_15179_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_15180_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_15181_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_15182_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_15218_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_15450_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_15451_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_1573_344571555444444444444444444444444444.unity3d`
- `role/atlas_role_1764_444455346667632632444444444444444444.prefab.unity3d`
- `role/atlas_role_22401_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_23401_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_24401_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_25401_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_2573_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_2702_444444444444444444444444444555887444.unity3d`
- `role/atlas_role_3573_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_3702_444444444444444444444444444555887444.unity3d`
- `role/atlas_role_4573_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_4702_444444444444444444444444444555887444.unity3d`
- `role/atlas_role_5573_444444444444444444444444444444444444.unity3d`
- `role/atlas_role_5702_444444444444444444444444444555887444.unity3d`
- `sound/am_17.unity3d`
- `wem/atlas_elm_58001309.unity3d`

### Missing Android paths

- None

## Named payload and manifest presence

This is an exact, case-insensitive basename check across XAPK members and the
app-data export.

| Name | Hits |
|---|---:|
| `NItem.Dat` | 0 |
| `NItem_EN.Dat` | 0 |
| `NNpc.dat` | 0 |
| `NNpc_EN.dat` | 0 |
| `NSceneData.dat` | 0 |
| `NSceneData_EN.dat` | 0 |
| `NSkill.dat` | 0 |
| `NSkill_EN.dat` | 0 |
| `NTalk.dat` | 0 |
| `NTalk_EN.dat` | 0 |
| `NCompound2.dat` | 0 |
| `NFormula.dat` | 0 |
| `AllFileList.txt` | 0 |
| `packagesversion.txt` | 0 |
| `MaxStreamingAssets.txt` | 1 |
| `StreamingAssetsVision.txt` | 1 |

`MaxStreamingAssets.txt` and `StreamingAssetsVision.txt` are direct runtime
files. Their values and paths are recorded above. No `AllFileList.txt` or
`packagesversion.txt` copy was supplied.

## Generated evidence

- `android-app-files.csv`: full deterministic path/size/time/hash/type inventory.
- `android-bundle-comparison.csv`: every Android/Steam bundle relationship.
- `xapk-inventory.json`: outer and nested APK member hashes and file types.
- `android-source-inventory.json`: compact summary, marker values, and exact-name checks.
