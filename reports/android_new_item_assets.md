# Android-only item asset evidence

Generated: 2026-08-25T17:52:57.101867+00:00

## Verdict

AssetRipper `1.3.14.0` parsed all `12` Android-only
item bundles selected by exact path comparison with the Steam snapshot. Each
bundle yielded one 32 x 32 RGBA Texture2D PNG and one direct item-prefab container
relationship. The internal numeric IDs are confirmed as asset IDs only.

No item names, descriptions, categories, stats, prices, crafting relationships,
drops, or spawn locations were inferred. Those fields remain unresolved until a
current gameplay record or other Grade A/B evidence links them.

| Item asset ID | Source bundle | Prefab object ID | Evidence icon | Confidence |
|---:|---|---|---|---|
| `3941` | `item/atlas_item_3941.unity3d` | `8304186654073558837` | `source_manifest/android_export/item_icons/3941.png` | `direct_asset_relationship` |
| `4890` | `item/atlas_item_4890.unity3d` | `7460282743278765402` | `source_manifest/android_export/item_icons/4890.png` | `direct_asset_relationship` |
| `4891` | `item/atlas_item_4891.unity3d` | `2306486399014747213` | `source_manifest/android_export/item_icons/4891.png` | `direct_asset_relationship` |
| `4892` | `item/atlas_item_4892.unity3d` | `-3474809626449252331` | `source_manifest/android_export/item_icons/4892.png` | `direct_asset_relationship` |
| `4893` | `item/atlas_item_4893.unity3d` | `-5553752961362322529` | `source_manifest/android_export/item_icons/4893.png` | `direct_asset_relationship` |
| `4894` | `item/atlas_item_4894.unity3d` | `5373571166882913818` | `source_manifest/android_export/item_icons/4894.png` | `direct_asset_relationship` |
| `4898` | `item/atlas_item_4898.unity3d` | `-3893196997390686084` | `source_manifest/android_export/item_icons/4898.png` | `direct_asset_relationship` |
| `4899` | `item/atlas_item_4899.unity3d` | `-5501909913817250804` | `source_manifest/android_export/item_icons/4899.png` | `direct_asset_relationship` |
| `6275` | `item/atlas_item_6275.unity3d` | `6386661052171849058` | `source_manifest/android_export/item_icons/6275.png` | `direct_asset_relationship` |
| `6276` | `item/atlas_item_6276.unity3d` | `6702394746122635189` | `source_manifest/android_export/item_icons/6276.png` | `direct_asset_relationship` |
| `6277` | `item/atlas_item_6277.unity3d` | `-8304402949396995759` | `source_manifest/android_export/item_icons/6277.png` | `direct_asset_relationship` |
| `6280` | `item/atlas_item_6280.unity3d` | `8637471393068352063` | `source_manifest/android_export/item_icons/6280.png` | `direct_asset_relationship` |

## Method

- Selected only `added_in_android_export` item paths from
  `source_manifest/android_export/android-bundle-comparison.csv`.
- Ran AssetRipper against isolated copies, never the supplied source directory.
- Validated each AssetBundle name and `assets/fordownloads/item/...prefab`
  container reference.
- Preserved original bundle and PNG SHA-256 hashes in `item-assets.json`.
- Visually inspected a contact sheet of all 12 icons before indexing.
- Did not parse or publish role/role-card assets.
