# Wonderland Online M Indexer

A static, evidence-based index for the current Wonderland M Steam client.

The site reads generated JSON under `data/`. Raw game files are not stored or
changed by the site build. Confirmed records keep their source file, extraction
method, confidence, client version, and status.

The published SQLite snapshot is `data/wonderland_m_complete.sqlite3`. The
browser loads `data/manifest.json` first, then fetches section files only when
opened. Global search uses a separate routing index. Every generated file uses
the same build ID and schema version.

Read `PROJECT_STATE.md` before extraction work. The current rows are item and map
asset IDs, localization records, and extraction evidence. Monster, spawn, drop,
NPC, quest, and recipe records remain unresolved. Old Wonderland Online PC data
is not used to fill them.

## Local preview

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Open `http://127.0.0.1:4173/`.

## Refresh site data

Run this only when the full extraction workspace is available:

```powershell
python tools/build_site_data.py `
  --extraction-dir "C:\Users\Public\Documents\WonderlandM_Atlas_Extraction" `
  --site-dir .
```

The generated site excludes player, account, save, role, role-card, and
character-model data.

## Validation

```powershell
python tools/validate_site.py --site-dir .
```

Current evidence and next actions are in `PROJECT_STATE.md`. The planned monster
and drop links are in `reports/monster_drop_navigation_plan.md`.
