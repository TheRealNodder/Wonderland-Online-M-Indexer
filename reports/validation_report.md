# Validation Report

Generated: 2026-07-16T19:11:20.137745+00:00

Overall status: **PASS**

## Automated checks

- `sqlite_integrity`: pass (0)
- `foreign_key_integrity`: pass (0)
- `invalid_probabilities`: pass (0)
- `invalid_coordinates`: pass (0)
- `missing_source_provenance`: pass (0)
- `missing_npc_functions`: pass (0)
- `unresolved_drop_groups`: pass (0)
- `consistent_client_versions`: pass (1)
- `circular_quest_dependencies`: pass (0)

## Scope notes

- Empty domain tables pass referential checks but remain unresolved, not confirmed absent from the game.
- System-string localization keys are general UI records; they are not treated as orphaned domain names until a domain linkage is asserted.
- No percentage is displayed unless `calculated_percentage` and `calculation_formula` are both populated.
