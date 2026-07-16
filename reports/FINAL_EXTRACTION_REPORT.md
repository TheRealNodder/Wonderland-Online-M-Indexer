# Final Extraction Report

## Client

- Game engine: Unity IL2CPP
- Unity version: 6000.0.58f2
- IL2CPP metadata version: 31
- Total files scanned and SHA-256 hashed: 28627
- Total files with content parsed: 14422
- Non-character Unity bundles parsed: 14411
- `role`/`rolecard` bundles excluded from derived content: 14128

## Extracted totals

- Localization records: 34161
- Items with direct atlas IDs: 5375
- Maps with direct asset IDs: 1105
- Monsters: 0
- Drop entries: 0
- Encounter groups: 0
- NPCs: 0
- Shops: 0
- Quests: 0
- Quest rewards: 0
- Quest conditions: 0
- Recipes: 0
- Audio metadata records: 890
- Animation metadata records: 2

## Drop rates

- Exact drop rates recovered: 0
- Drop weights unresolved: all; local drop tables were not found.
- No unproven raw value has been labeled as a percentage.

## Missing client payloads

The IL2CPP metadata directly references `NItem.dat`, `NItem_EN.dat`, `NNpc.dat`, `NSceneData.dat`, `NSkill.dat`, `NTalk.dat`, `NCompound2.dat`, and `NFormula.dat`, but those files are absent from the Steam installation. These appear to be downloaded or server-supplied data and are not inferred from the older PC game.

## Unsupported or protected files

- Unreadable files: 0
- Encrypted/protected files bypassed: 0
- Bundle parse errors: 0
- Five item sprite records have no local Texture2D object; their IDs remain indexed with null icon assets.

## Vine Grass and Harl Grass

Five whole-word `Vine` localization contexts were found, including `3017245=Vine`; no exact `Vine Grass`, `Harl Grass`, or whole-word `Harl` record was found. No current-client item ID, drop source, drop rate, encounter group, or step-based AFK location is confirmed from the installation files examined so far.

## Validation

- Automated validation: PASS
- Unresolved relationships: 12

## Recommended next steps

- Obtain the non-account-specific downloaded data payloads through a lawful client-cache export, without network interception or account/character data.
- Re-run the same parsers and promote relationships only when direct records become available.
- Use the generated JSON indexes and SQLite database as the immutable source for the Wonderland Online M Indexer website.
