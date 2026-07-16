# Wonderland Online M Indexer - ChatGPT Handoff

Last verified: 2026-07-16 (America/Los_Angeles)

## Continuation prompt

Use this repository as the source of truth and continue the Wonderland Online M
Indexer project from the state documented below. Read this entire file before
changing anything. Preserve all provenance and confidence fields. Do not add
player, account, save, role, role-card, or character-model data. Do not treat
data from the original Wonderland Online PC game as valid for Wonderland M
unless it is independently verified against current-client evidence.

Work through implementation, validation, and documentation. Inspect the current
repository and `git status` before editing. Do not overwrite unrelated user
changes. Keep the game installation read-only and place all generated extraction
artifacts outside it.

## Repository

- GitHub: https://github.com/TheRealNodder/Wonderland-Online-M-Indexer
- Live site: https://therealnodder.github.io/Wonderland-Online-M-Indexer/
- Default branch: `main`
- Last verified commit: `efe95b38fa462378d615d112580eb3d6d4a66b4e`
- Last verified commit message: `Fix deployment`
- Current source-computer checkout:
  `C:\Users\josue\OneDrive\Email attachments\Documents\GitHub\Wonderland-Online-M-Indexer`

On the home computer, clone or open the GitHub repository instead of assuming
the source-computer path exists.

```powershell
git clone https://github.com/TheRealNodder/Wonderland-Online-M-Indexer.git
cd Wonderland-Online-M-Indexer
git status
```

## Current deployment status

- The public URL returned HTTP 200 on 2026-07-16.
- GitHub's branch-based `pages build and deployment` run succeeded for commit
  `efe95b3`.
- The custom workflow `.github/workflows/page-deployment.yml` is structurally
  valid, but its `Deploy static content to Pages` run failed at `Setup Pages`.
- Failure reason: the repository was not configured to build Pages using GitHub
  Actions. The currently working site is deployed from the `main` branch.

Recommended cleanup: keep the working branch deployment and remove
`.github/workflows/page-deployment.yml` so future pushes do not show an
unnecessary failed Actions run. The alternative is to change GitHub
`Settings > Pages > Source` to `GitHub Actions` and retain the workflow. Do not
use both deployment approaches.

## Non-negotiable safety rules

The game installation is strictly read-only. Never modify, rename, delete, patch,
or replace game or Steam files. Never write temporary output into the game
installation.

Do not:

- Launch unknown game-directory executables.
- Patch executables or inject code.
- Disable anti-cheat or bypass authentication.
- Defeat encryption or access controls.
- Inspect running process memory or attach a debugger.
- Capture or intercept game network traffic.
- Automate gameplay, simulate input, or create bots.
- Modify saves, account data, character data, or drop rates.
- Extract or publish player, account, save, role, role-card, or character-model
  data.

If a file needs administrator permission merely to be read, report it rather
than changing system permissions automatically.

## Version and evidence rules

This project covers the newer Steam/mobile Wonderland M iteration, not the
original Wonderland Online PC release.

- Direct installed-client evidence is marked `current_client_extracted`.
- Older external information must remain separate unless verified against the
  current client or current gameplay evidence.
- Preserve raw names, localization keys, IDs, source paths, record keys, object
  IDs, offsets, extraction methods, parser versions, timestamps, and raw values.
- Never report a drop percentage unless the calculation is mathematically proven.
- Empty tables mean unresolved local evidence, not proof that the feature does
  not exist in the game.

Allowed confidence values:

- `direct_client_record`
- `direct_localization_match`
- `direct_asset_relationship`
- `strong_relationship`
- `inferred_relationship`
- `name_match_only`
- `unresolved`

## Original extraction locations

These paths existed on the source computer and may differ or be absent at home:

- Game installation:
  `C:\Program Files (x86)\Steam\steamapps\common\WLM`
- Full extraction workspace:
  `C:\Users\Public\Documents\WonderlandM_Atlas_Extraction`
- Full SQLite database:
  `C:\Users\Public\Documents\WonderlandM_Atlas_Extraction\database\wonderland_m_complete.sqlite3`

The GitHub repository contains the website-ready data, selected reports, and a
database snapshot. It does not contain the complete extraction workspace or raw
game installation. To resume deep extraction on another computer, either rerun
the reusable extraction tools against a locally installed current WLM client or
lawfully transfer the full external extraction workspace. Never copy character
or account data.

## Confirmed client and engine

- Engine: Unity IL2CPP
- Unity version: `6000.0.58f2`
- IL2CPP metadata version: `31`
- Files recursively inventoried and SHA-256 hashed: `28,627`
- Total readable installation size: `2,592,691,652` bytes
- Unreadable files: `0`
- Unity asset bundles identified: `28,539`
- Non-character bundles parsed: `14,411`
- `role` and `rolecard` bundles excluded from derived content: `14,128`
- Bundle parse errors: `0`
- Protected/encrypted files bypassed: `0`

## Extracted data currently published

- Localization records: `34,161`
- Items with direct atlas IDs: `5,375`
- Maps with direct asset IDs: `1,105`
- Item/map asset references: `6,604`, all present at last validation
- Extraction evidence records: `5,375`
- Unresolved relationships: `12`
- Audio metadata records in the full extraction workspace: `890`
- Animation metadata records in the full extraction workspace: `2`
- Browser runtime index: approximately `22.2 MB`
- Published SQLite snapshot: approximately `50.1 MB`
- Published repository tree: `6,623` files, approximately `188 MB`

Current unresolved domain counts are zero, not confirmed absent:

- Monsters: `0`
- Drops: `0`
- Encounters: `0`
- NPCs: `0`
- Shops: `0`
- Quests: `0`
- Quest rewards/conditions: `0`
- Recipes/compounds: `0`
- Step-based AFK locations: `0`
- Visible spawns: `0`

## Missing current-client payloads

IL2CPP metadata references these data files, but they were absent from the Steam
installation examined:

- `NItem.dat`
- `NItem_EN.dat`
- `NNpc.dat`
- `NSceneData.dat`
- `NSkill.dat`
- `NTalk.dat`
- `NCompound2.dat`
- `NFormula.dat`

These files appear to be downloaded or server-supplied. Continue only from a
lawful, non-account-specific client-cache export or files explicitly supplied by
the user. Do not intercept traffic, inspect memory, bypass protection, automate
the game, or include account/character data.

## Vine and Harl Grass status

Confirmed current-client evidence:

- Five whole-word English `Vine` localization contexts were found.
- One context is localization key `3017245=Vine`.
- Exact `Vine Grass` matches: `0`.
- Whole-word `Harl` matches: `0`.
- Exact `Harl Grass` matches: `0`.

No current-client item ID, drop source, drop rate, monster, encounter group,
map, dungeon floor, quest/shop/compound source, or step-based AFK location is
confirmed for Vine Grass or Harl Grass. Do not import an answer from the older PC
game without direct current-version verification.

## Validation state

The extraction database and generated website passed the available automated
checks:

- SQLite integrity
- Foreign-key integrity
- Probability and coordinate validation
- Required provenance
- Client-version consistency
- Circular quest dependency checks
- Website runtime JSON parsing
- Website asset reference checks

The current website manifest explicitly contains:

```json
"verification_status": "current_client_extracted",
"character_data_included": false
```

Run the website validator after every data or frontend change:

```powershell
python tools\validate_site.py --site-dir .
```

Refresh the website data only when the full extraction workspace is available:

```powershell
python tools\build_site_data.py `
  --extraction-dir "C:\Users\Public\Documents\WonderlandM_Atlas_Extraction" `
  --site-dir .
```

For a temporary local preview:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Open `http://127.0.0.1:4173/` and stop the Python server after testing.

## Website implementation

The site is static HTML/CSS/JavaScript and currently includes navigation for:

- Global Search
- Monsters
- Items
- Drops
- Maps
- Step-Based AFK Locations
- Visible Spawns
- Dungeons
- NPC Directory
- Shops
- Quests and quest relationships
- Map requirements and portals
- Compounding
- Localization
- Extraction evidence
- Unresolved records
- Verification issues

Important files:

- `index.html` - application shell
- `styles.css` - responsive interface styling
- `app.js` - navigation, search, filtering, pagination, and record details
- `data/runtime-index.json` - browser data index
- `data/manifest.json` - extraction metadata and counts
- `data/wonderland_m_complete.sqlite3` - relational snapshot
- `tools/build_site_data.py` - site-data generator
- `tools/validate_site.py` - website validator
- `reports/FINAL_EXTRACTION_REPORT.md` - extraction summary
- `reports/vine_harl_grass_findings.md` - priority search report

## Recommended next work

1. Resolve the duplicate Pages deployment configuration. Prefer the currently
   working branch deployment and remove the redundant workflow.
2. Clone the repository on the home computer and rerun
   `tools/validate_site.py` before editing.
3. Improve first-load performance. The browser currently fetches and parses one
   approximately 22.2 MB JSON file. Consider generating per-section JSON files
   and loading sections on demand while preserving global search through a
   smaller search index.
4. Add richer item and map detail views without inventing missing relationships.
5. Continue extraction only if the missing non-character payloads become
   lawfully available. Add parsers under the external extraction workspace,
   retain raw evidence, then regenerate the SQLite database and website data.
6. Keep empty monster/drop/NPC/quest sections visibly unresolved until direct
   current-client records exist.
7. Revalidate the public site on desktop and mobile after every deployment.

## Completion discipline

Before committing work:

```powershell
git status --short
git diff --check
python tools\validate_site.py --site-dir .
```

Review generated data for character/account leakage, commit only intentional
files, push through GitHub Desktop or Git, and verify the GitHub Pages run and
public URL. Record all unresolved facts honestly rather than filling gaps with
speculation.
