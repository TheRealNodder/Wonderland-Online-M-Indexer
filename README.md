# Wonderland Online M Indexer

A static, evidence-first index for the current Wonderland M Steam client.

The site consumes generated JSON under `data/`. Raw game files are never stored
or modified by the site build. Confirmed records retain source-file provenance,
confidence, extraction method, client version, and verification status.

The validated relational snapshot is published as
`data/wonderland_m_complete.sqlite3` alongside the browser runtime index.

## Local preview

```powershell
python -m http.server 4173
```

Open `http://localhost:4173`.

## Refresh site data

```powershell
python tools/build_site_data.py `
  --extraction-dir "C:\Users\Public\Documents\WonderlandM_Atlas_Extraction" `
  --site-dir .
```

The generated site intentionally excludes player, account, save, and character
model data.
