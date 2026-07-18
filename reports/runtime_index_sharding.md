# Runtime index sharding report

- Previous eager runtime payload: `22206698` bytes
- Initial manifest payload: `7215` bytes
- Build ID: `9de5924f8e23f6ae927285a2`
- Schema version: `3`
- Section payload total: `22210854` bytes
- Search payload, loaded only when used: `9940654` bytes
- Search records: `46028`
- Monolithic runtime removed: **True**

Opening the site now loads only the manifest. A section is fetched when selected,
and the search file is fetched only after a global-search query is entered.
Section and search filenames include content hashes. Every file carries the same build ID,
schema version, timestamp, record count, and content hash.
The complete SQLite snapshot remains available for full offline queries.

## Section files

| Section | Records | Bytes | SHA-256 |
|---|---:|---:|---|
| `compounds` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `drops` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `dungeons` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `evidence` | 5375 | 3321476 | `242732f075d373046ba86dbd5dfce3adac4dcd8e1d6e9ef064e82e0ca5beac58` |
| `items` | 5375 | 3683478 | `a4e7075639817ba86c7db96580b7af6fec3d9fadcdb0e40676ec719ef761a4ff` |
| `localization` | 34161 | 14407127 | `1774bcf62e6fc3315286004450847e6b6c8673b8cf87f7e2927f152275aa373c` |
| `map_requirements` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `maps` | 1105 | 788780 | `c2242cb07bfda7c264399b549959d33bc6a035c9165454700f04688adffe1f66` |
| `monsters` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `npcs` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `portals_teleports` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `quest_chains` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `quest_rewards` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `quests` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `shops` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `step_afk_locations` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `unresolved` | 12 | 6913 | `786076fdafc5e08301625fd6c1fad1dcb7a9f9dcf744d76e26fd8fbf9f83d8d5` |
| `verification_issues` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |
| `visible_spawns` | 0 | 220 | `1d6c0c603391fe4dcbc0648ef820bdbc5351d2a64b73c13f9c32f21134341ab2` |

Sharding changes delivery only. It does not change record values, evidence,
confidence, verification status, or the SQLite source snapshot.
