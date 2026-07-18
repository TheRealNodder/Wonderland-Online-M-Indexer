# Official Client Candidate Inspection

Generated: 2026-07-17 (America/Los_Angeles)

## Verdict

The approved Android APK and standalone Windows download are current
Wonderland M 1.1060.1 artifacts. They strengthen package provenance, loader
schema, and download-architecture evidence. Neither package contains the 12
custom data payloads needed to create confirmed item, monster, spawn, drop,
recipe, NPC, quest, or map records.

No downloaded candidate executable was run. The Steam installation was not
modified.

## Artifact identities

| Artifact | Bytes | SHA-256 | Identity result |
|---|---:|---|---|
| `WL.apk` | 98,257,251 | `8f5df0fb1764a02dc174b67f992d977569e514091cc740a182ffa2f50ab5c3e2` | `com.x980.wlmobile`, version `1.1060.1`, Unity `6000.0.58f2` |
| `WL.exe` | 84,038,263 | `aa5fe53f27d79029b0d6a859c2c4c1c21f9bd0e6c39d59f307024c4abdf81f52` | Unsigned self-extracting archive containing a current `1.1060.1` Unity base client |

The APK v2 RSA/SHA-256 signature and APK content digest both verify. Its
signing-certificate SHA-256 fingerprint is
`a1402d411ca1fd484cedbaa2affcd62e2a8b7ce52fe57be1d9593a6a702e9882`.
The Windows wrapper has no Authenticode signature; it was inspected as an
archive and never executed.

## Steam comparison

The standalone archive expands to 33 files. Compared with the verified Steam
logical manifest:

- Reference logical files: 28,627
- Candidate files: 33
- Exact matches: 15
- Changed: 18
- Missing: 28,594
- Added: 0

The matching launcher, Unity player, base scene/configuration files, current
version string, and schema establish current-product continuity. The missing
content establishes that the standalone artifact is a bootstrap/base client,
not a replacement for the verified Steam snapshot.

## Current-client schema

The Steam, standalone, and Android builds expose the same 33 targeted WLM
loader/data types and all 12 expected payload filenames. The standalone schema
is an exact match to Steam. The APK is a semantic match with one expected
platform-specific offset difference.

The named payloads remain:

`NItem.Dat`, `NItem_EN.Dat`, `NNpc.dat`, `NNpc_EN.dat`, `NSceneData.dat`,
`NSceneData_EN.dat`, `NSkill.dat`, `NSkill_EN.dat`, `NTalk.dat`,
`NTalk_EN.dat`, `NCompound2.dat`, and `NFormula.dat`.

None is present in either candidate package.

## Download-architecture lead

Static AssetRipper inspection of the APK Unity bundle recovered a
`DownloadUrlPath` TextAsset with the active public base
`https://wlmhkftp.chinesegamer.net/WLF_U3ds/`. Current code appends one of
`PC_U6/`, `Android_U6/`, or `iPhone_U6/` and names these manifest/package
components:

- `AllFileList.txt`
- `packagesversion.txt`
- `MaxStreamingAssets.txt`
- `StreamingAssetsVision.txt`
- `StreamingAssetsZip/`
- `StreamingAssets_*.zip`

Plausible direct manifest, package, and table probes under the public base
returned HTTP 404. The base is therefore classified only as
`endpoint_candidate`. The 404s neither prove that it is unused nor authorize
guessing paths, headers, signed values, or request parameters.

## Aleta checkpoint 4

Aleta returned **Pass for package provenance and runtime-capture planning**.
The independent review agreed that:

- No gameplay-domain records are justified from these packages.
- Package hashes, signatures, version, schema results, filename literals,
  endpoint candidates, platform rules, and probe results may be recorded as
  source metadata.
- The next evidence step should be a filesystem-first observation of files
  written by the already verified Steam client during normal startup/patching,
  preferably before account login.
- The initial observation must not use Reload Data, replay tokens, reuse signed
  links, alter requests, bypass controls, inspect protected traffic, or import
  legacy wiki rows as substitutes.

The current-domain record gate remains closed until actual current WLM payload
bytes are recovered, hashed, schema-validated, and parsed with exact provenance.
