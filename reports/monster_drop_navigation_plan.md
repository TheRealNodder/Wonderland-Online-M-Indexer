# Monster and drop navigation plan

The main path is:

`Monster -> Spawn membership -> Spawn -> Map -> Drop source -> Drop table -> Drop entry -> Item`

Do not attach every drop table directly to a monster. A drop source may be a
monster, encounter group, map object, chest, NPC, quest, script, or gathering
point. Store `source_type` and `source_id` so the schema does not assume the
answer before current-client records are parsed.

## Required records

| Record | Required links |
|---|---|
| Monster | spawn memberships, drop sources, skills, evidence |
| Spawn membership | monster, spawn, position/weight, evidence |
| Spawn or encounter | map, members, conditions, drop source, evidence |
| Map | spawns, incoming/outgoing transfers, parent/floor, evidence |
| Drop source | source type/ID, drop tables, evidence |
| Drop table | source records, entries, roll rule, evidence |
| Drop entry | drop table, item, quantity/rate fields, conditions, evidence |
| Item | drop entries, drop sources, maps reached through sources, evidence |

## Reverse indexes

Generate these from normalized relationships during each site build:

- `monster_id -> spawn_ids`
- `spawn_id -> monster_ids`
- `map_id -> spawn_ids`
- `item_id -> drop_entry_ids`
- `drop_table_id -> source references`
- `source_type + source_id -> drop_table_ids`
- `map_id -> incoming transfer_ids`
- `map_id -> outgoing transfer_ids`

Each reverse row must point back to the same evidence-bearing relationship, not
repeat a claim without provenance.

## Page behavior

- A monster page shows spawn locations, maps, drop sources/tables, items, and
  evidence.
- A spawn page shows its map, members, conditions, attached drop source, and
  evidence.
- A map page shows spawns, monsters reached through those spawns, transfers,
  floors/zones, and evidence.
- A drop-table page shows its source, roll rule, entries, quantities/rates, and
  evidence.
- An item page shows every verified source and the maps reached through those
  source relationships.
- ID fields in record details link to their target section. The current site
  already provides this behavior for known ID fields.

## Current limit

No current-client monster, spawn, drop, or confirmed item table records have
been parsed. The existing rows are item and map **asset IDs**. This plan becomes
active when the missing current-client payloads or equivalent lawful static
records are supplied and fingerprinted.
