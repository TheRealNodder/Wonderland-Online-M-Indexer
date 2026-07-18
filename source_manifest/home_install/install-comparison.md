# Home Installation Comparison

Generated: 2026-07-18T02:55:51.244987+00:00

## Result

**PASS: the home installation is logically byte-identical to the published Wonderland M source snapshot after normalizing ZIP packaging**

The game directory was read only. ZIP members were hashed in memory and mapped to
their logical `WLM_Data/StreamingAssets/...` paths; nothing was extracted into the
Steam installation.

## Logical comparison

| Measurement | Count |
|---|---:|
| Reference files | 28627 |
| Current physical files | 28515 |
| Current logical files | 28627 |
| Matching logical files | 28627 |
| Changed logical files | 0 |
| Missing logical files | 0 |
| Added logical files | 0 |

## Core fingerprints

| Path | Bytes | Current SHA-256 | Matches reference |
|---|---:|---|:---:|
| `GameAssembly.dll` | 46948864 | `429da8cb9a4ba29a07fd7104d5055c1842bb007830e46085cdc6ed0b3239a9c6` | yes |
| `UnityPlayer.dll` | 33646504 | `78ec69dab5574f216863eec417c8dc3d7ac1916e6922b2b6658efe78fe185456` | yes |
| `WLM_Data/globalgamemanagers` | 719636 | `2831af7ef36cfa251f792187f3fca730d44005a9085d4984d874283eb1a6e76f` | yes |
| `WLM_Data/il2cpp_data/Metadata/global-metadata.dat` | 10514580 | `bb4011d548961d50345e36574b7213411fc4b8fb28d6a85e6093edfcd14f3aa6` | yes |
| `WLM.exe` | 672256 | `110f382c8d33e0233015d11baeb8a44e06e12afa8759766bad3dad80795505dc` | yes |
| `WLM_Data/app.info` | 8 | `e3ac160facf2ffd9faf894e9a3e495625fe494518d05e4ed5416c702904c029f` | yes |
| `WLM_Data/boot.config` | 156 | `a7a85aa4d9e591f1a9537a7676cecfe0fff643130c0b338423c98f823b5dfa53` | yes |
| `WLM_Data/RuntimeInitializeOnLoads.json` | 3483 | `5f989e9cddc4d7f57e48e061f15f6122b2286ef31fcdd6f106c87c0cc953aab4` | yes |
| `WLM_Data/ScriptingAssemblies.json` | 4516 | `ba7bfa95c11562dfa8e952bb9b1d650f27fcc228c11c034b5157313430894122` | yes |
| `WLM_Data/StreamingAssets/UnityServicesProjectConfiguration.json` | 1410 | `fcd38ffa37b2a448be41ee9a396a435f8be8e952b4b11b9b60e2962e76c7d352` | yes |

IL2CPP metadata header: `0xFAB11BAF`, version
`31`. Current UnityFS revision:
`6000.0.58f2`. Current
application identity: company `980x`,
product `WLM`.

## Archive normalization

- `WLM_Data/StreamingAssets/StreamingAssets_1.zip`: 113 logical members, SHA-256 `861e2b76cadf76bdcb233092e85538b59c0931a41a78c1cd200c3f9a29b99757`

## Expected downloaded payload names

This is a filename-level presence check, not a claim about compressed Unity object
contents or server behavior.

| Payload | Logical filename hits |
|---|---:|
| `NItem.dat` | 0 |
| `NItem_EN.dat` | 0 |
| `NNpc.dat` | 0 |
| `NNpc_EN.dat` | 0 |
| `NSceneData.dat` | 0 |
| `NSceneData_EN.dat` | 0 |
| `NSkill.dat` | 0 |
| `NSkill_EN.dat` | 0 |
| `NTalk.dat` | 0 |
| `NTalk_EN.dat` | 0 |
| `NCompound2.dat` | 0 |
| `NFormula.dat` | 0 |

## Differences

### Changed

- None

### Missing

- None

### Added

- None

## Provenance guard

- The reference database describes the current Steam/mobile **Wonderland M**
  client, not the original early-2000s Wonderland Online release.
- Exact agreement of the Unity 6/IL2CPP core plus every logical source-file hash
  supports using the existing current-client extraction as the baseline.
- Original-PC-game information remains excluded unless a separate current-client
  record independently corroborates it.
