# Source quarantine: legacy, seed, and wrong-client material

This report prevents unrelated or weakly sourced material from entering the
current Wonderland M evidence chain. Quarantined files may inform questions to
investigate, but they may not populate normalized entity or relationship tables.

## Classification rules

| Grade | Meaning | May populate confirmed tables? |
|---|---|:---:|
| A | Direct record, asset, schema, or hash from the verified current WLM client | yes |
| B | Current-version manual gameplay observation with recorded evidence | yes, marked manual |
| C | Current-version official/community/user source not yet matched to the client | no; candidate only |
| Rejected | Legacy-only, wrong-client, internally conflicting, or untraceable material | no |

The original early-2000s Wonderland Online release is not assumed compatible
with Wonderland M. A matching name is not enough to promote a legacy claim.

## Wrong-client Il2CppDumper output

Location: `C:\Users\josue\Downloads\Il2CppDumper-win-v6.7.46`

The pre-existing dump outputs in this folder were generated on 2026-05-27,
before the verified WLM installation snapshot. They are not WLM:

- `dump.cs` SHA-256: `f1fd687bd59666787b63e34927952f36eb6fcdcc3cf2f76bedf9fab01f33290c`
- `script.json` SHA-256: `be97260df63ea26b27bdc16edc1892d341d1ab57e2fd457db7468d5d35ecdd44`
- `stringliteral.json` SHA-256: `780eb2d338d6ace40989b1897a1bc2a41380a788f6897c910b20c98df9443b61`
- The dump declares `inc.zigza.evertale.core.csharp.runtime.dll`.
- It contains Evertale-specific gacha and `MonsterInstance` symbols.

Classification: **Rejected - different game (Evertale)**.

These outputs were not used by any tool or generated report in this pass. A
fresh dump was instead generated from the verified WLM `GameAssembly.dll` and
`global-metadata.dat`; its hashes are recorded in
`reports/current_client_il2cpp_schema.md`.

## Wonderland M Atlas starter archive

Location: `C:\Users\josue\Downloads\wonderland_m_atlas_starter.zip`

- Archive SHA-256: `a1dbe6ff22cad544dc3a735830c0a7ccd70bce33449a340dc816e7e99ef5ebf7`
- The archive contains a useful Streamlit prototype, schema, build notes, and
  tests. Those structural ideas are reference material only; no code or data
  was merged in this pass.
- `data/seed_early_farming.json` contains 16 seed monsters, named maps, claimed
  drops, and three compound claims.
- The seed explicitly describes itself as a user-guide seed and records an
  internal Plump Grasshopper location conflict.
- Its source registry includes current official/community candidates, but also
  marks WLO HUB as a legacy database that must not be promoted without current
  verification.
- Claims involving Woodman, Fern, Vine Grass, Harl Grass, maps, drops, and
  compound results are not supported by the currently published client tables.

Classification: **Grade C for explicitly current-version candidate material;
Rejected for any legacy-only component.** No row may become Grade A until it is
matched to a current-client ID/record or recorded current gameplay evidence.

## Promotion gate

A quarantined claim can leave quarantine only when all of the following are
recorded:

1. The exact current WLM build or gameplay version.
2. A current-client ID or a reproducible current-game observation.
3. Source path/object/offset or screenshot/manual-verification reference.
4. Extraction or observation method.
5. Confidence and verification status.
6. Reverse relationships where applicable.

Until then, the spawn-location report remains empty instead of being filled
with plausible older-game or seed answers.
