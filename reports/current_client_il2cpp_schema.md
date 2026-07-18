# Current Wonderland M IL2CPP schema index

- Verdict: **PASS - current WLM metadata v31 schema indexed**
- Evidence scope: verified current Wonderland M static-data loader schema only
- Metadata: `0xFAB11BAF`, version `31`
- Indexed target types: `33` / `33`
- Exact target data-file literals: `12`
- Imported legacy Wonderland Online data: **No**
- Imported player/account/role-card/character-model data: **No**

## Provenance

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| GameAssembly.dll | 46948864 | `429da8cb9a4ba29a07fd7104d5055c1842bb007830e46085cdc6ed0b3239a9c6` |
| global-metadata.dat | 10514580 | `bb4011d548961d50345e36574b7213411fc4b8fb28d6a85e6093edfcd14f3aa6` |
| Il2CppDumper.exe | 13374349 | `071e36d396ae93cb2cfec032513b46a6bfd67e9b93157830711ab6d79db55045` |
| fresh dump.cs | 21633756 | `9390c516292474e5bcc4c1b2b40f0615cdadb85e4dd51c386b1b8eb0aa07bf05` |
| fresh stringliteral.json | 1581566 | `bf1d4aea599220054d508a9d7b6c84b584f3f205b30ce6cf1e7bbe090319027e` |

The dump was generated from the verified local WLM inputs. The dumper completed
the schema and dummy-DLL stages; its nonzero shell result was caused only by the
configured final `Press any key to exit` prompt under redirected input.

## Exact current-client data-file literals

| Literal | IL2CPP address |
|---|---|
| `NCompound2.dat` | `0x29238F0` |
| `NFormula.dat` | `0x2923A00` |
| `NItem.Dat` | `0x2923C20` |
| `NItem_EN.Dat` | `0x2923CA8` |
| `NNpc.dat` | `0x2924060` |
| `NNpc_EN.dat` | `0x2924170` |
| `NSceneData.dat` | `0x2924638` |
| `NSceneData_EN.dat` | `0x2924740` |
| `NSkill.dat` | `0x29247C8` |
| `NSkill_EN.dat` | `0x2924850` |
| `NTalk.dat` | `0x2924A70` |
| `NTalk_EN.dat` | `0x2924B80` |

## Indexed loader and record schemas

### `CDataBehaviour`

Namespace `(global)`; class; TypeDef `309`.

Expected schema fields and code constants:

- `protected static TextAsset sc_CurrDataText; // 0x0`
- `protected static byte[] sbAry_FCurrDataByte; // 0x8`
- `protected byte[] FDataBytes; // 0x20`
- `public E_GameLanguage DataLanguage; // 0x28`
- `private DataDictionary<ushort, IGameDataStruct> m_dictCurrData; // 0x30`
- `private int m_iDataSize; // 0x38`
- `private bool m_bLogAll; // 0x3C`
- `public bool IsLoadOk; // 0x3D`

Relevant loader/access methods:

- `public FuncYieldAfterDownloadDo get_DoLoadBundleAsset() { }`
- `protected bool get_LogAllLoad() { }`
- `protected bool HandleLoadText(string strDataName, E_ReadFrom eFrom) { }`
- `protected virtual void LoadLocalData(bool bEditorRead = False) { }`
- `public IEnumerator LoadBundleData(string strDataName, AssetBundle cBundle) { }`
- `public void CallOnFinishRead(string strDataName, E_ReadFrom eFrom, bool bSuccess) { }`
- `protected void .ctor() { }`

### `CDataBehaviour_Bytes`

Namespace `(global)`; class; TypeDef `310`.

Relevant loader/access methods:

- `public override bool LoadDataFromTextAsset(TextAsset cText) { }`
- `protected void .ctor() { }`

### `CDownloadUrlPathData`

Namespace `Game.Data`; class; TypeDef `1197`.

Expected schema fields and code constants:

- `private const string C_DEFAULT_LOAD_PATH = "Data/DownloadUrlPath";`
- `private const byte C_LoadStep_None = 0;`
- `private const byte C_LoadStep_Resource = 1;`
- `private const byte C_LoadStep_Download = 2;`
- `private byte m_bCompleteDownload; // 0x28`
- `private Dictionary<E_UrlPathAreaType, string> mAreaDownloadPathMap; // 0x30`
- `private Dictionary<E_UrlPathAreaType, string> m_tLocalAreaDownloadMap; // 0x38`

Relevant loader/access methods:

- `public byte get_LoadStep() { }`
- `private void set_LoadStep(byte value) { }`
- `public override string get_MyDownloadFileName() { }`
- `private bool LoadLocalFile() { }`
- `public override bool DoLoadFromDownload(COneDownloadRec cDnl) { }`
- `private string GetLocalDownloadUrlPath(E_UrlPathAreaType _eType) { }`
- `public string GetDownloadUrlPath(E_UrlPathAreaType _eType) { }`
- `public void .ctor() { }`

### `rMixStuffRd`

Namespace `Game.Data`; struct; TypeDef `1194`.

Expected schema fields and code constants:

- `public ushort StuffId; // 0x0`
- `public byte Num; // 0x2`

Relevant loader/access methods:

- `public void ReadData(byte[] aryBytes, ref int iPos) { }`

### `COneCompoundItemRdData`

Namespace `Game.Data`; struct; TypeDef `1195`.

Expected schema fields and code constants:

- `public ushort ItemId; // 0x0`
- `public ushort BluePrint; // 0x2`
- `public byte Skill; // 0x4`
- `public ushort MachineId; // 0x6`
- `public byte MakeNum; // 0x8`
- `public rMixStuffRd[] StuffAry; // 0x10`
- `public byte StuffNum; // 0x18`
- `public ushort Timez; // 0x1A`
- `public byte SkillLv; // 0x1C`
- `public byte SuggestNumber; // 0x1D`
- `public byte SpareByte2; // 0x1E`
- `public byte SpareByte3; // 0x1F`
- `public byte SpareByte4; // 0x20`
- `public byte SpareByte5; // 0x21`
- `public ushort SpareWord1; // 0x22`
- `public ushort SpareWord2; // 0x24`
- `public ushort SpareWord3; // 0x26`
- `public ushort SpareWord4; // 0x28`
- `public ushort SpareWord5; // 0x2A`
- `public int SpareInt1; // 0x2C`
- `public int SpareInt2; // 0x30`
- `public int SpareInt3; // 0x34`
- `public int SpareInt4; // 0x38`
- `public int SpareInt5; // 0x3C`

Relevant loader/access methods:

- `public void .ctor(byte[] aryBytes, ref int iPos) { }`

### `CCompound2DataManager`

Namespace `Game.Data`; class; TypeDef `1196`.

Expected schema fields and code constants:

- `private const byte ByteCRC = 211;`
- `private const ushort WordCRC = 64444;`
- `private const int IntegerCRC = 168229221;`
- `private const byte CompoundBias = 3;`
- `private Dictionary<ushort, ushort> TrafficDesign_Drawings; // 0x40`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `private void HandleAddOne(COneCompoundItemRdData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public void FindUtensil(ushort Id, ref List<COneCompoundItemRdData> result) { }`
- `public ushort FindOneIdx(ushort Id) { }`
- `public COneCompoundItemRdData FindOne(ushort Id) { }`
- `public COneCompoundItemRdData FindOne2(ushort Id) { }`
- `public void .ctor() { }`

### `COneFormulaData`

Namespace `Game.Data`; struct; TypeDef `1203`.

Expected schema fields and code constants:

- `public byte aVer; // 0x0`
- `public double aW1; // 0x8`
- `public double aW2; // 0x10`
- `public double aW3; // 0x18`
- `public double aW4; // 0x20`
- `public double aW5; // 0x28`
- `public double aW6; // 0x30`
- `public double aW7; // 0x38`
- `public double aW8; // 0x40`
- `public double aW9; // 0x48`
- `public double aW10; // 0x50`
- `public double aW11; // 0x58`
- `public double aW12; // 0x60`
- `public double aW13; // 0x68`
- `public double aW14; // 0x70`
- `public double aW15; // 0x78`
- `public double aW16; // 0x80`
- `public double aW17; // 0x88`
- `public double aW18; // 0x90`
- `public double aW19; // 0x98`
- `public double aW20; // 0xA0`
- `public double aW21; // 0xA8`
- `public double aW22; // 0xB0`
- `public double aW23; // 0xB8`
- `public double aW24; // 0xC0`
- `public double aW25; // 0xC8`
- `public double aW26; // 0xD0`
- `public double aW27; // 0xD8`
- `public double aW28; // 0xE0`
- `public double aW29; // 0xE8`
- `public double aW30; // 0xF0`
- `public double aW31; // 0xF8`
- `public double aW32; // 0x100`
- `public double aW33; // 0x108`
- `public double aW34; // 0x110`
- `public double aW35; // 0x118`
- `public double aW36; // 0x120`
- `public double aW37; // 0x128`
- `public double aW38; // 0x130`
- `public double aW39; // 0x138`
- `public double aW40; // 0x140`
- `public double aW41; // 0x148`
- `public double aW42; // 0x150`
- `public double aW45; // 0x158`
- `public double aW50; // 0x160`
- `public double aW51; // 0x168`
- `public int aExtraExp; // 0x170`
- `public ushort aBaseHp; // 0x174`
- `public ushort aBaseSp; // 0x176`
- `public ushort aAttAgiScope; // 0x178`
- `public byte aRan; // 0x17A`
- `public byte SpareByte1; // 0x17B`
- `public byte SpareByte2; // 0x17C`
- `public byte SpareByte3; // 0x17D`
- `public byte SpareByte4; // 0x17E`
- `public byte SpareByte5; // 0x17F`
- `public ushort SpareWord1; // 0x180`
- `public ushort SpareWord2; // 0x182`
- `public ushort SpareWord3; // 0x184`
- `public ushort SpareWord4; // 0x186`
- `public ushort SpareWord5; // 0x188`
- `public int SpareInt1; // 0x18C`
- `public int SpareInt2; // 0x190`
- `public int SpareInt3; // 0x194`
- `public int SpareInt4; // 0x198`
- `public int SpareInt5; // 0x19C`

Relevant loader/access methods:

- `public void .ctor(byte[] aryBytes, ref int iPos) { }`

### `CFormulaDataManager`

Namespace `Game.Data`; class; TypeDef `1204`.

Expected schema fields and code constants:

- `private const byte ByteCRC = 0;`
- `private const ushort WordCRC = 0;`
- `private const int IntegerCRC = 0;`
- `private const byte FormulaDataBias = 0;`
- `public COneFormulaData Current; // 0x40`

Relevant loader/access methods:

- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `public override string get_DataFileName() { }`
- `public override bool LoadDataFromBytes() { }`
- `public void .ctor() { }`

### `rWaveRecord`

Namespace `Game.Data`; struct; TypeDef `1205`.

Expected schema fields and code constants:

- `public ushort WaveBlockX; // 0x0`
- `public ushort WaveBlockY; // 0x2`
- `public byte WaveNo; // 0x4`
- `public byte WaveDist; // 0x5`

Relevant loader/access methods:

- `public void ReadData(byte[] aryData, ref int iReadPos) { }`

### `rElmInfo`

Namespace `Game.Data`; struct; TypeDef `1206`.

Expected schema fields and code constants:

- `public uint uiName; // 0x0`
- `public short shLeft; // 0x4`
- `public short shTop; // 0x6`

Relevant loader/access methods:

- `public void ReadData(byte[] aryData, ref int iReadPos) { }`

### `rGeolRecord`

Namespace `Game.Data`; struct; TypeDef `1207`.

Expected schema fields and code constants:

- `public byte Attr; // 0x0`
- `public ushort Left; // 0x2`
- `public ushort Top; // 0x4`
- `public ushort Right; // 0x6`
- `public ushort Bottom; // 0x8`

Relevant loader/access methods:

- `public void ReadData(byte[] aryData, ref int iReadPos) { }`

### `rRGBInfo`

Namespace `Game.Data`; struct; TypeDef `1208`.

Expected schema fields and code constants:

- `public byte Red; // 0x0`
- `public byte Green; // 0x1`
- `public byte Blue; // 0x2`

Relevant loader/access methods:

- `public void ReadData(byte[] aryData, ref int iReadPos) { }`

### `rMazeElmInfo`

Namespace `Game.Data`; struct; TypeDef `1209`.

Expected schema fields and code constants:

- `public ushort GroundID; // 0x0`
- `public ushort BlockID; // 0x2`
- `public byte GroundKind; // 0x4`
- `public byte BlockIndex; // 0x5`
- `public byte BlockKind; // 0x6`
- `public int BaseY; // 0x8`

Relevant loader/access methods:

- `public void ReadData(byte[] aryData, ref int iReadPos) { }`

### `COneGroundData`

Namespace `Game.Data`; class; TypeDef `1210`.

Expected schema fields and code constants:

- `private bool m_bCompleteLoad; // 0x20`
- `private CMap m_cMasterMap; // 0x28`
- `private int mMapWidth; // 0x30`
- `private int mMapHeight; // 0x34`
- `private byte mbySum; // 0x38`
- `private ushort mNewID; // 0x3A`
- `private ushort mNewX; // 0x3C`
- `private ushort mNewY; // 0x3E`
- `private ushort mBlockWidth; // 0x40`
- `private ushort mBlockHeight; // 0x42`
- `private ushort mWavCnt; // 0x44`
- `private ushort m_wElmCount; // 0x46`
- `private byte mGarNpcCnt; // 0x48`
- `private byte mGeolBaseAtt; // 0x49`
- `private byte mGeolCnt; // 0x4A`
- `private byte mMazeKind; // 0x4B`
- `private byte mMazeCol; // 0x4C`
- `private byte mMazeRow; // 0x4D`
- `public byte[,] arybyTempBlock; // 0x50`
- `public rWaveRecord[] aryWaveRecord; // 0x58`
- `public rElmInfo[] aryElmInfo; // 0x60`
- `public rGeolRecord[] aryGeolRecord; // 0x68`
- `private string PlaceName; // 0x70`
- `private int iGM_MapX; // 0x78`
- `private int iGM_MapY; // 0x7C`
- `private rRGBInfo RGB; // 0x80`
- `public rMazeElmInfo[,] aryMazeElmInfo; // 0x88`
- `private CElmDataCtrl[] m_aryElmData; // 0x90`

Relevant loader/access methods:

- `public bool get_IsCompleteLoaded() { }`
- `public bool LoadGround(byte[] aryBytes, int iSize) { }`
- `public void .ctor() { }`

### `CGroundDataManager`

Namespace `Game.Data`; class; TypeDef `1212`.

Expected schema fields and code constants:

- `private const int C_ClearToGCCount = 5;`
- `private int m_iNextGroundNum; // 0x20`
- `private int m_iDataSize; // 0x24`
- `private byte[] m_aryNextGroundData; // 0x28`
- `private CMap m_cMapDataHandler; // 0x30`
- `private int m_iLoadCount; // 0x38`
- `private UnityWebRequest www; // 0x40`

Relevant loader/access methods:

- `public void OnFailedDownloadDo() { }`
- `public void OnCompleteDownloadDo(COneDownloadRec cDnl) { }`
- `public bool LoadPreparedToGround(COneGroundData cGnd) { }`
- `private IEnumerator LoadLocalData(int iID) { }`
- `public void .ctor() { }`

### `COneItemData`

Namespace `Game.Data`; struct; TypeDef `1220`.

Expected schema fields and code constants:

- `private string m_Name; // 0x0`
- `public byte Kind; // 0x8`
- `public ushort ID; // 0xA`
- `public ushort BoySGID; // 0xC`
- `public ushort GirlSGID; // 0xE`
- `public ushort BoyGID; // 0x10`
- `public ushort GirlGID; // 0x12`
- `public ushort BoyGID2; // 0x14`
- `public ushort GirlGID2; // 0x16`
- `public ushort[] Attribute; // 0x18`
- `public byte[] AttrItem; // 0x20`
- `public int[] Value; // 0x28`
- `public byte byMaterial; // 0x30`
- `public byte Level; // 0x31`
- `public byte FitType; // 0x32`
- `public byte SpecialAbility; // 0x33`
- `public int[] TopColorNo; // 0x38`
- `public int[] MiddleColorNo; // 0x40`
- `public int[] BottomColorNo; // 0x48`
- `public int[] WeaponColorNo; // 0x50`
- `public byte OpenUsed; // 0x58`
- `public byte NeedLV; // 0x59`
- `public int Price; // 0x5C`
- `public int SellPrice; // 0x60`
- `public byte Gender; // 0x64`
- `public ushort Restrict; // 0x66`
- `public int Threshold; // 0x68`
- `public byte Element; // 0x6C`
- `public int ElementValue; // 0x70`
- `public ushort SkillLink; // 0x74`
- `public ushort Spare1; // 0x76`
- `public ushort Spare2; // 0x78`
- `public ushort Spare3; // 0x7A`
- `public ushort Spare4; // 0x7C`
- `public ushort Spare5; // 0x7E`
- `private string Desc; // 0x80`
- `public byte SizeH; // 0x88`
- `public byte SizeW; // 0x89`
- `public byte SizeL; // 0x8A`
- `public ushort Evolution; // 0x8C`
- `public byte ItemW; // 0x8E`
- `public byte ItemH; // 0x8F`
- `public byte ShowOrder; // 0x90`
- `public ushort PicLeftId; // 0x92`
- `public ushort PicRightId; // 0x94`
- `public ushort AssignId; // 0x96`
- `public byte FurPutKind; // 0x98`
- `public byte Apanage; // 0x99`
- `public byte Apanage2; // 0x9A`
- `public byte SpareByte3; // 0x9B`
- `public byte SpareByte4; // 0x9C`
- `public byte SpareByte5; // 0x9D`
- `public ushort ItemAvailTime; // 0x9E`
- `public ushort UseCount; // 0xA0`
- `public ushort PresentID; // 0xA2`
- `public ushort PurplePoint; // 0xA4`
- `public ushort SpareWord5; // 0xA6`
- `public int SpareInt1; // 0xA8`
- `public int SpareInt2; // 0xAC`
- `public int SpareInt3; // 0xB0`
- `public int SpareInt4; // 0xB4`
- `public int SpareInt5; // 0xB8`

Relevant loader/access methods:

- `public void .ctor(byte[] aryBytes, ref int iPos) { }`
- `public string PleaseNotUseThis_GetName() { }`

### `CItemDataManager`

Namespace `Game.Data`; class; TypeDef `1221`.

Expected schema fields and code constants:

- `private const byte ByteCRC = 154;`
- `private const ushort WordCRC = 61379;`
- `private const int IntegerCRC = 193000628;`
- `private const byte ItemDataBias = 9;`
- `private Dictionary<int, byte> m_ShopWeaponBeatLvList; // 0x40`
- `private Dictionary<int, int> m_ShopWwaponNextLvID; // 0x48`
- `private COneItemData LastUsedItem1; // 0x50`
- `private COneItemData LastUsedItem2; // 0x110`
- `public const byte C_PlayerUseForgetItem = 1;`
- `public const byte C_FNpcUseForgetItem = 101;`
- `private int aLoginSend; // 0x1D0`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `public void LoadInEditor() { }`
- `private void HandleAddOne(COneItemData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public string GetName(int iID) { }`
- `public void .ctor() { }`

### `CItemDataManager_EN`

Namespace `Game.Data`; class; TypeDef `1222`.

Expected schema fields and code constants:

- `private const byte ByteCRC = 154;`
- `private const ushort WordCRC = 61379;`
- `private const int IntegerCRC = 193000628;`
- `private const byte ItemDataBias = 9;`
- `private COneItemData LastUsedItem1; // 0x40`
- `private COneItemData LastUsedItem2; // 0x100`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `private void HandleAddOne(COneItemData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public void .ctor() { }`

### `COneNpcData`

Namespace `Game.Data`; struct; TypeDef `1245`.

Expected schema fields and code constants:

- `private string Name; // 0x0`
- `public byte Kind; // 0x8`
- `public ushort ID; // 0xA`
- `public ushort GRole; // 0xC`
- `public ushort GMask; // 0xE`
- `public int TopColorNo; // 0x10`
- `public int MiddleColorNo; // 0x14`
- `public int BottomColorNo; // 0x18`
- `public int WeaponColorNo; // 0x1C`
- `public byte CatchKind; // 0x20`
- `public byte BodyKind; // 0x21`
- `public byte Weapon; // 0x22`
- `public byte Level; // 0x23`
- `public int MaxHP; // 0x24`
- `public int MaxSP; // 0x28`
- `public ushort Stg; // 0x2C`
- `public ushort Con; // 0x2E`
- `public ushort Int; // 0x30`
- `public ushort Wis; // 0x32`
- `public ushort Agi; // 0x34`
- `public byte VisibleKind; // 0x36`
- `public byte Element; // 0x37`
- `public ushort[] Skill; // 0x38`
- `public ushort[] Goods; // 0x40`
- `public byte ShadowSize; // 0x48`
- `public ushort NewWis; // 0x4A`
- `public ushort Spare3; // 0x4C`
- `public ushort Spare4; // 0x4E`
- `public ushort Spare5; // 0x50`
- `public byte NpcKind; // 0x52`
- `public ushort WeaponPic; // 0x54`
- `public byte HangKind; // 0x56`
- `public byte SizeKind; // 0x57`
- `public ushort HeadPic; // 0x58`
- `public ushort Key; // 0x5A`
- `public ushort StepSound; // 0x5C`
- `public ushort AppearAgi; // 0x5E`
- `public ushort NormalSkill; // 0x60`
- `public byte ShowWeapon; // 0x62`
- `public byte GrowKey; // 0x63`
- `public byte CanPk; // 0x64`
- `public ushort EquipId; // 0x66`
- `public byte DefendShoot; // 0x68`
- `public byte NpcSoundKey; // 0x69`
- `public byte GenusKind; // 0x6A`
- `public byte PowerAttackRate; // 0x6B`
- `public byte HPTub; // 0x6C`
- `public ushort MapWeapon; // 0x6E`
- `public ushort MercenaryTime; // 0x70`
- `public ushort SpareWord3; // 0x72`
- `public ushort SpareWord4; // 0x74`
- `public ushort SpareWord5; // 0x76`
- `public int SpareInt1; // 0x78`
- `public int SpareInt2; // 0x7C`
- `public int SpareInt3; // 0x80`
- `public int SpareInt4; // 0x84`
- `public int SpareInt5; // 0x88`

Relevant loader/access methods:

- `public void .ctor(byte[] aryBytes, ref int iPos) { }`
- `public string PleaseNotUseThis_GetName() { }`

### `CNpcDataManager`

Namespace `Game.Data`; class; TypeDef `1246`.

Expected schema fields and code constants:

- `private const byte NpcDataBias = 1;`
- `private const byte ByteCRC = 200;`
- `private const ushort WordCRC = 21001;`
- `private const int IntegerCRC = 195999510;`
- `private Dictionary<ushort, ushort> NewIdToOldId; // 0x40`
- `private Dictionary<byte, ushort> GrowKey_To_Id; // 0x48`
- `private int iLastGetNpcID; // 0x50`
- `private COneNpcData rLast; // 0x58`
- `private static readonly ArrayList FForceStepKind; // 0x0`
- `private static readonly ArrayList FNoShowNameKind; // 0x8`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `public void LoadInEditor() { }`
- `private void HandleAddOne(COneNpcData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public COneNpcData FindOne(int iNpcID) { }`
- `public string GetName(int iNpcID) { }`
- `public byte FindNpcSkill(int iNpcID, int iSkillID) { }`
- `public void .ctor() { }`

### `CNpcDataManager_EN`

Namespace `Game.Data`; class; TypeDef `1247`.

Expected schema fields and code constants:

- `private const byte NpcDataBias = 1;`
- `private const byte ByteCRC = 200;`
- `private const ushort WordCRC = 21001;`
- `private const int IntegerCRC = 195999510;`
- `private int iLastGetNpcID; // 0x40`
- `private COneNpcData rLast; // 0x48`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `private void HandleAddOne(COneNpcData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public COneNpcData FindOne(int iNpcID) { }`
- `public string GetName(int iNpcID) { }`
- `public void .ctor() { }`

### `COneSceneData`

Namespace `Game.Data`; struct; TypeDef `1252`.

Expected schema fields and code constants:

- `public ushort ID; // 0x0`
- `private string Name; // 0x8`
- `public byte LandType; // 0x10`
- `public byte BusinessType; // 0x11`
- `public string MusicName; // 0x18`
- `public byte LimitType; // 0x20`
- `public byte IsOpen; // 0x21`
- `public byte SpecialType; // 0x22`
- `public ushort[] MarkAry; // 0x28`
- `public ushort[] ToSceneAry; // 0x30`
- `public ushort[] LayerId; // 0x38`
- `public ushort Layer1OffSet; // 0x40`
- `public ushort Layer2OffSet1; // 0x42`
- `public ushort Layer2OffSet2; // 0x44`
- `public ushort SceneLightId; // 0x46`
- `public byte IsDupMis; // 0x48`
- `public byte IsOrg; // 0x49`
- `public byte SpareByte3; // 0x4A`
- `public byte SpareByte4; // 0x4B`
- `public byte SpareByte5; // 0x4C`
- `public ushort DupMark; // 0x4E`
- `public ushort DupLimitLv; // 0x50`
- `public ushort DupLimitTime; // 0x52`
- `public ushort DupEnterX; // 0x54`
- `public ushort DupEnterY; // 0x56`
- `public int SpareInt1; // 0x58`
- `public int SpareInt2; // 0x5C`
- `public int SpareInt3; // 0x60`
- `public int SpareInt4; // 0x64`
- `public int SpareInt5; // 0x68`

Relevant loader/access methods:

- `public void .ctor(byte[] aryBytes, ref int iPos) { }`
- `public string PleaseNotUseThis_GetName() { }`

### `CSceneDataManager`

Namespace `Game.Data`; class; TypeDef `1253`.

Expected schema fields and code constants:

- `private const byte ByteCRC = 44;`
- `private const ushort WordCRC = 60012;`
- `private const int IntegerCRC = 103512999;`
- `private const byte SceneDataBias = 9;`
- `public static CSceneDataManager Instance; // 0x0`
- `private List<ushort> AllDup; // 0x40`
- `public bool loadDup; // 0x48`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `private void HandleAddOne(COneSceneData cNew, bool bRecordDupInfo = False) { }`
- `public override bool LoadDataFromBytes() { }`
- `public void LoadAllDupScence() { }`
- `public bool FindOne(ushort wID, out COneSceneData rScene) { }`
- `public COneSceneData FindOne(ushort wID) { }`
- `public byte FindLimitType(int iSceneID) { }`
- `public string GetName(int iSceneID) { }`
- `public void .ctor() { }`

### `CSceneDataManager_EN`

Namespace `Game.Data`; class; TypeDef `1254`.

Expected schema fields and code constants:

- `private const byte ByteCRC = 44;`
- `private const ushort WordCRC = 60012;`
- `private const int IntegerCRC = 103512999;`
- `private const byte SceneDataBias = 9;`
- `public static CSceneDataManager_EN Instance; // 0x0`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `private void HandleAddOne(COneSceneData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public bool FindOne(ushort wID, out COneSceneData rScene) { }`
- `public COneSceneData FindOne(ushort wID) { }`
- `public void .ctor() { }`

### `COneSkillData`

Namespace `Game.Data`; struct; TypeDef `1260`.

Expected schema fields and code constants:

- `private string Name; // 0x0`
- `public byte Kind; // 0x8`
- `public ushort ID; // 0xA`
- `public ushort ReduceSP; // 0xC`
- `public byte Element; // 0xE`
- `public ushort AtkKind; // 0x10`
- `public byte FightWay; // 0x12`
- `public byte Grade; // 0x13`
- `public byte FightArea; // 0x14`
- `public double VariableA; // 0x18`
- `public double VariableB; // 0x20`
- `public byte VariableC; // 0x28`
- `public ushort VariableD; // 0x2A`
- `public byte Round; // 0x2C`
- `public byte HitStatus; // 0x2D`
- `public byte InitSkillPot; // 0x2E`
- `public ushort PreSkillId; // 0x30`
- `public ushort Spare1; // 0x32`
- `public ushort Spare2; // 0x34`
- `public ushort Spare3; // 0x36`
- `public ushort Spare4; // 0x38`
- `public ushort Spare5; // 0x3A`
- `private string Desc; // 0x40`
- `public ushort Key; // 0x48`
- `public byte TargetKind; // 0x4A`
- `public ushort GId; // 0x4C`
- `public ushort StatusId; // 0x4E`
- `public byte Duration; // 0x50`
- `public byte LvLimit; // 0x51`
- `public byte Discolor; // 0x52`
- `public ushort HitBackId; // 0x54`
- `public byte RangeKind1; // 0x56`
- `public byte RangeKind2; // 0x57`
- `public byte RangeKind3; // 0x58`
- `public byte RangeKind4; // 0x59`
- `public byte SpareByte1; // 0x5A`
- `public byte SpareByte2; // 0x5B`
- `public byte SpareByte3; // 0x5C`
- `public byte SpareByte4; // 0x5D`
- `public byte SpareByte5; // 0x5E`
- `public ushort SoundKey; // 0x60`
- `public ushort SpareWord2; // 0x62`
- `public ushort SpareWord3; // 0x64`
- `public ushort SpareWord4; // 0x66`
- `public ushort SpareWord5; // 0x68`
- `public int SpareInt1; // 0x6C`
- `public int SpareInt2; // 0x70`
- `public int SpareInt3; // 0x74`
- `public int SpareInt4; // 0x78`
- `public int SpareInt5; // 0x7C`

Relevant loader/access methods:

- `public void .ctor(byte[] aryBytes, ref int iPos) { }`
- `public string PleaseNotUseThis_GetName() { }`

### `CSkillDataManager`

Namespace `Game.Data`; class; TypeDef `1261`.

Expected schema fields and code constants:

- `private const byte ByteCRC = 253;`
- `private const ushort WordCRC = 28320;`
- `private const int IntegerCRC = 199155391;`
- `private const byte SkillBias = 4;`
- `private ushort[] Key_To_Id; // 0x40`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `public void ForceLoad() { }`
- `private void HandleAddOne(COneSkillData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public string GetName(ushort wID) { }`
- `public ushort FindIdByKey(int aKey) { }`
- `public COneSkillData FindOne(ushort ID) { }`
- `public int FindRoleFirstSkill(byte sexx, byte Headsty) { }`
- `public void .ctor() { }`

### `CSkillDataManager_EN`

Namespace `Game.Data`; class; TypeDef `1262`.

Expected schema fields and code constants:

- `private const byte ByteCRC = 253;`
- `private const ushort WordCRC = 28320;`
- `private const int IntegerCRC = 199155391;`
- `private const byte SkillBias = 4;`
- `private ushort[] Key_To_Id; // 0x40`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `private void HandleAddOne(COneSkillData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public COneSkillData FindOne(ushort ID) { }`
- `public string GetName(ushort wID) { }`
- `public void .ctor() { }`

### `COneTalkData`

Namespace `Game.Data`; struct; TypeDef `1263`.

Expected schema fields and code constants:

- `public ushort ID; // 0x0`
- `private string TalkMemo; // 0x8`
- `public byte SpareByte1; // 0x10`
- `public byte SpareByte2; // 0x11`
- `public byte SpareByte3; // 0x12`
- `public byte SpareByte4; // 0x13`
- `public byte SpareByte5; // 0x14`
- `public ushort SpareWord1; // 0x16`
- `public ushort SpareWord2; // 0x18`
- `public ushort SpareWord3; // 0x1A`
- `public ushort SpareWord4; // 0x1C`
- `public ushort SpareWord5; // 0x1E`
- `public int SpareInt1; // 0x20`
- `public int SpareInt2; // 0x24`
- `public int SpareInt3; // 0x28`
- `public int SpareInt4; // 0x2C`
- `public int SpareInt5; // 0x30`

Relevant loader/access methods:

- `public void .ctor(byte[] aryBytes, ref int iPos) { }`

### `CTalkDataManager`

Namespace `Game.Data`; class; TypeDef `1264`.

Expected schema fields and code constants:

- `private const byte TalkDataBias = 5;`
- `private const byte ByteCRC = 99;`
- `private const ushort WordCRC = 60650;`
- `private const int IntegerCRC = 132123440;`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `private void HandleAddOne(COneTalkData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public void .ctor() { }`

### `CTalkDataManager_EN`

Namespace `Game.Data`; class; TypeDef `1265`.

Expected schema fields and code constants:

- `private const byte TalkDataBias = 5;`
- `private const byte ByteCRC = 99;`
- `private const ushort WordCRC = 60650;`
- `private const int IntegerCRC = 132123440;`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `protected override FuncYieldAfterDownloadDo get_FKeepDnlRecMethod() { }`
- `private void HandleAddOne(COneTalkData cNew) { }`
- `public override bool LoadDataFromBytes() { }`
- `public void .ctor() { }`

### `rOneTransferPointData`

Namespace `(global)`; struct; TypeDef `304`.

Expected schema fields and code constants:

- `public byte OrderNum; // 0x0`
- `public byte OpenToWho; // 0x1`
- `public byte Region; // 0x2`
- `public ushort ShowMapX; // 0x4`
- `public ushort ShowMapY; // 0x6`
- `public ushort MarkID; // 0x8`
- `public ushort SceneID; // 0xA`
- `public ushort MapX; // 0xC`
- `public ushort MapY; // 0xE`
- `private string MapName; // 0x10`
- `public ushort TargetObjLv; // 0x18`

### `CTransferPointData_EN`

Namespace `Game.Data`; class; TypeDef `1266`.

Expected schema fields and code constants:

- `private Dictionary<byte, rOneTransferPointData> m_TransferPointDataList; // 0x40`
- `private Dictionary<ushort, ushort> m_tSceneIdToMarkID; // 0x48`

Relevant loader/access methods:

- `public override string get_DataFileName() { }`
- `public override bool LoadDataFromTextAsset(TextAsset cText) { }`
- `public void .ctor() { }`

### `DataMgrs`

Namespace `Game.Data`; class; TypeDef `1273`.

Expected schema fields and code constants:

- `public static DataMgrs Handler; // 0x0`
- `private Dictionary<Type, CDataBehaviour> FStartLoadMgrsMap; // 0x28`
- `private Dictionary<CDataBehaviour, int> FMgrIdxMap; // 0x30`
- `private Dictionary<Type, MonoBehaviour> FFreeLoadMgrsMap; // 0x38`
- `private List<CDataBehaviour> FOrderDownloadList; // 0x40`
- `private DataMgrs.E_AllDataLoadStatus FLoadState; // 0x48`
- `private uint FMgrsCompleteLoad; // 0x4C`
- `private uint FMgrsLoadStatus; // 0x50`
- `private List<CDataBehaviour> FNeedRedownList; // 0x58`
- `private bool FShowingMsg; // 0x60`
- `private static CServerIPData m_cSerIpData; // 0x8`
- `private static CSceneDataManager m_cSceneData; // 0x10`
- `private static CSceneDataManager_EN m_cSceneData_EN; // 0x18`
- `private static CItemDataManager_EN m_cItemData_EN; // 0x20`
- `private static CTransferPointData_EN m_TransferPointData_EN; // 0x28`
- `private static CTalkDataManager_EN m_cTalkData_EN; // 0x30`
- `private static CMarkDataManager_EN m_cMarkData_EN; // 0x38`
- `private static CNpcDataManager_EN m_cNpcData_EN; // 0x40`
- `private static CSkillDataManager_EN m_cSkillData_EN; // 0x48`
- `private static CMissionGuideData_EN m_cMissionGuideData_EN; // 0x50`
- `private static CCompound2DataManager m_cCompound2Data; // 0x58`
- `private static CItemDataManager m_cItemData; // 0x60`
- `private static CBuildingDataManager m_cBuildingData; // 0x68`
- `private static CEveDataManager m_cEveData; // 0x70`
- `private static CTransferPointData m_TransferPointData; // 0x78`
- `private static CTrafficSettingDataMgr m_TrafficSettingDataMgr; // 0x80`
- `private static CFurnitureSettingDataMgr m_FurnitureSettingDataMgr; // 0x88`
- `private static CRidePetSettingDataMgr m_RidePetSettingDataMgr; // 0x90`
- `private static COrgOccupiedBattleData m_OrgOccupiedBattleData; // 0x98`
- `private static CTalkDataManager m_cTalkData; // 0xA0`
- `private static CMarkDataManager m_cMarkData; // 0xA8`
- `private static CNpcDataManager m_cNpcData; // 0xB0`
- `private static CSkillDataManager m_cSkillData; // 0xB8`
- `private static CFormulaDataManager m_cFormulaData; // 0xC0`
- `private static CMotionDataManager m_cMotionData; // 0xC8`
- `private static CGroundDataManager m_cGroundData; // 0xD0`
- `private static CWemDataManager m_cWemData; // 0xD8`
- `private static CElmSizeData m_cElmSizeData; // 0xE0`
- `private static CFightLightData m_cFightLightData; // 0xE8`
- `private static CLightTable m_cLightTable; // 0xF0`
- `private static CMissionGuideData m_cMissionGuideData; // 0xF8`
- `private static CEveDoorLinkData m_cEveDoorLinkData; // 0x100`
- `private static CChangeItemColorData m_cChangeItemColorData; // 0x108`
- `private static CItemAniData m_cItemAniData; // 0x110`
- `private static CExtraStringData m_cExtraStringData; // 0x120`
- `private List<string> tPathList; // 0x68`
- `private string strWritePath; // 0x70`
- `private StreamWriter tSW; // 0x78`

Relevant loader/access methods:

- `public override string get_MyDownloadFileName() { }`
- `public static bool get_FLogDataLoad() { }`
- `private void OnOneDataCompleteLoadDo(CDataBehaviour cOneDataMgr) { }`
- `private void HandleOrderDownloadData() { }`
- `private T RegisterStartLoadManager<T>() { }`
- `private T RegisterFreeLoadManager<T>() { }`
- `private CDataBehaviour IdxFindDataMgr(int iIndex) { }`
- `private bool DoCallDownload(CDataBehaviour cMono) { }`
- `public bool CallAllDataDownload() { }`
- `public override bool DoLoadFromDownload(COneDownloadRec cDnl) { }`
- `private IEnumerator MultiThreadProcessDownload(COneDownloadRec cDnl) { }`
- `public void OnFailedOneDownload(COneDownloadRec cDn) { }`
- `private void UpdateDoFailDataRedownload() { }`
- `public void .ctor() { }`

Omitted `8` player-title/role-card manager members as out of scope.

## Interpretation

This is parser schema evidence, not evidence that the named payload files are
currently present on disk. The payloads remain unresolved until a lawful current-client
source yields their bytes. Old PC Wonderland Online layouts and seed data are not valid
substitutes for this WLM schema.
