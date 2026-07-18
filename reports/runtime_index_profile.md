# Runtime index profile

- Runtime JSON: `22207323` bytes
- Deterministic gzip estimate: `913631` bytes
- Records loaded eagerly: `46028`
- Python JSON parse average (three local samples): `122.65` ms
- Eager monolithic fetch detected: **True**
- Per-filter full-record stringify detected: **True**

Browser timing will vary by device. The Python samples measure payload parse cost only,
not network, DOM rendering, image loading, or JavaScript garbage collection.

## Section contribution

| Section | Records | JSON bytes | Gzip bytes | Runtime share | Always-empty fields |
|---|---:|---:|---:|---:|---|
| `localization` | 34161 | 14406905 | 648841 | 64.87% | - |
| `items` | 5375 | 3683257 | 86554 | 16.59% | `aliases`, `buy_price`, `compound_use`, `crafting_use`, `description`, `display_name`, `element`, `equipment_slot`, `level_requirement`, `material_rank`, `material_type`, `quest_item_status`, `sell_price`, `stack_size`, `stats`, `subcategory`, `trade_restrictions` |
| `evidence` | 5375 | 3321255 | 139804 | 14.96% | - |
| `maps` | 1105 | 788559 | 35269 | 3.55% | `access_requirements`, `coordinate_system`, `display_name`, `dungeon`, `encounter_groups`, `entrances`, `exits`, `floor`, `gathering_nodes`, `height`, `npcs`, `parent_map`, `portals`, `quest_markers`, `region`, `scene_asset`, `subregion`, `tilemap`, `treasure_points`, `width` |
| `unresolved` | 12 | 6694 | 493 | 0.03% | `target_id` |
| `compounds` | 0 | 2 | 22 | 0.00% | - |
| `drops` | 0 | 2 | 22 | 0.00% | - |
| `dungeons` | 0 | 2 | 22 | 0.00% | - |
| `map_requirements` | 0 | 2 | 22 | 0.00% | - |
| `monsters` | 0 | 2 | 22 | 0.00% | - |
| `npcs` | 0 | 2 | 22 | 0.00% | - |
| `portals_teleports` | 0 | 2 | 22 | 0.00% | - |
| `quest_chains` | 0 | 2 | 22 | 0.00% | - |
| `quest_rewards` | 0 | 2 | 22 | 0.00% | - |
| `quests` | 0 | 2 | 22 | 0.00% | - |
| `shops` | 0 | 2 | 22 | 0.00% | - |
| `step_afk_locations` | 0 | 2 | 22 | 0.00% | - |
| `verification_issues` | 0 | 2 | 22 | 0.00% | - |
| `visible_spawns` | 0 | 2 | 22 | 0.00% | - |

## Recommended direction

- Load a small manifest first and fetch section JSON only when selected.
- Keep global search in a compact precomputed search shard instead of stringifying full records on each keystroke.
- Defer evidence and localization detail payloads until their sections or a record dialog need them.
- Keep the SQLite snapshot as the complete downloadable source while making the browser payload task-oriented.

Any sharding change must preserve IDs, provenance, confidence, client version, and
verification status. Performance work must not turn unresolved fields into facts.
