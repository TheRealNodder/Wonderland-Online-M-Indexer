# Engine Detection

## Result

**Unity IL2CPP, Unity 6000.0.58f2.**

## Direct client evidence

- `UnityPlayer.dll`: present
- `GameAssembly.dll`: present
- `global-metadata.dat`: present
- `resources.assets`: present
- `StreamingAssets`: present
- `global-metadata.dat` sanity: `0xFAB11BAF`, metadata version `31`.
- Sample AssetBundle headers identify Unity `6000.0.58f2`.

No evidence of Unity Mono, Unreal Engine, Cocos, or Electron was found in the installed client layout.
