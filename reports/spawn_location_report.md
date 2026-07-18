# Spawn location priority report

Current result: **no Wonderland M monster-to-spawn-to-map relationship is
verified yet**. The table is intentionally empty; legacy Wonderland Online and
unverified seed-guide claims were not substituted for missing current-client
records.

| Monster ID | Monster Name | Map ID | Map Name | Floor or Zone | Encounter Type | Drop Summary | Confidence | Evidence |
|---|---|---|---|---|---|---|---:|---|

## Monsters with no resolved map

No current-client monster records are available. The `monsters` table contains
`0` rows, so there are no IDs that can honestly be listed yet.

## Maps with unresolved internal names

- `1,105` map asset IDs are extracted with direct current-client asset
  provenance.
- All `1,105` still lack a verified display name, region, floor, and portal
  relationship because `NSceneData.dat` and related runtime records are absent.

## Duplicate monster names with different IDs

Not testable until current-client monster records are obtained.

## Original Wonderland Online versus Wonderland M

No comparison rows are published. Original-PC-game names and locations remain
quarantined until a current WLM record or manual current-game observation
establishes the Wonderland M side of the comparison.

## Candidate AFK zones

No evidence-backed recommendation can be produced yet. The first usable chain
must be:

`NNpc record -> encounter/spawn record -> NSceneData map -> drop record -> NItem record`

The verified current-client IL2CPP schema now provides the expected NPC, scene,
item, skill, formula, and compound loader layouts. The named payload bytes themselves
remain the blocker. See `current_client_il2cpp_schema.md` and
`current_client_string_references.md`.
