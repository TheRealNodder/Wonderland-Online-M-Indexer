# Provenance Audit

Generated: 2026-07-18T02:56:55.139890+00:00

Overall status: **PASS**

Every populated domain row was checked for required provenance fields, a
`current_client_extracted` verification status, and a source path present in
the hashed Wonderland M source manifest.

| Table | Rows | Audited | Missing fields | Non-current status | Unmapped source rows | Result |
|---|---:|:---:|---:|---:|---:|:---:|
| `animation_assets` | 2 | yes | 0 | 0 | 0 | pass |
| `audio_assets` | 890 | yes | 0 | 0 | 0 | pass |
| `client_versions` | 1 | yes | 0 | 0 | 0 | pass |
| `extraction_evidence` | 5375 | yes | 0 | 0 | 0 | pass |
| `items` | 5375 | yes | 0 | 0 | 0 | pass |
| `localization_entries` | 34161 | yes | 0 | 0 | 0 | pass |
| `maps` | 1105 | yes | 0 | 0 | 0 | pass |
| `source_files` | 28627 | manifest | 0 | 0 | 0 | reference |
| `unresolved_relationships` | 12 | yes | 0 | 0 | 0 | pass |

## Legacy-game guard

No populated domain row lacks current-client status or a source path in the
hashed modern Wonderland M manifest. This audit found no evidence of legacy
Wonderland Online contamination. It deliberately does not claim that absence
of legacy contamination is mathematically proven; semantic facts still require
field-level current-client evidence.
