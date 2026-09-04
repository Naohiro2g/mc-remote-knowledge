# Scratch–Stack deployment interface 設計

> Scratch担当、Stack担当、OSS管理者が、相手componentの内部や過去のdeployment経緯を調べずに
> 作業できるための横断contract。
>
> 拘束は `2026-08-31-01`／`2026-09-04-04`／`2026-09-04-05`、Scratchが公開する機械可読schema／fixtureはscratch-editor、
> operator向けcommand／runbookはmc-remote-stackを正本とする。

## 1. 管理者から見える通常経路

通常経路の入口は、「b6セットをVPSへ」「b7セットをdevへケータリング型で」のような人間の依頼である。
Stack担当は、それまでのsessionと追加対話を使ってrelease、target、構築方式を確定し、次の順で完了まで進める。

```text
1. Backstage inventoryを確認する
2. 対象hostをread-only preflightする
3. preset／order／lockを確定する
4. applyする
5. doctorで確認する
```

物理host写像はBackstage、exact artifactはpreset／lock、構築方式はprofileやhostと独立して管理する。
分離した入力を完全自動resolverで推測することは要求しない。Stack担当が会話とinventoryの既知情報を
一つの論理desired stateであるorderへ具体化する。利用者が最初から`mc-remote.toml`を用意する必要はない。

Stack内部のvalidate、preset解決、artifact lock、render、起動は通常経路が引き受ける。新規deploymentか
既存deploymentの更新かもStackが判定し、通常経路へbootstrap専用手順とupdate専用手順を露出しない。

`doctor`は実際に配信・接続されている結果を確認する。render済みJSON、Compose、Bridge allowlistは
生成物であり、管理者が個別編集する入力ではない。

## 2. 責務境界

```text
Scratch image
  ├─ Scratch browser application
  ├─ McRemote extension / GUI
  ├─ image-owned product config
  ├─ deployment runtime configの読込contract
  └─ 接続fail-close

Stack
  ├─ operator order
  ├─ immutable presetの解決
  ├─ exact artifact lock
  ├─ Scratch runtime configの生成
  ├─ Bridge設定の生成
  ├─ apply
  └─ doctor
```

Scratch担当はStackのorder、preset、renderer、profileを調査しない。Stack担当はScratchのReact、VM、
extension、webpack実装を調査しない。両者の接続点は、Scratch担当が公開するcontract directoryだけである。

## 3. 設定は所有者ごとに二つへ分ける

### 3.1 Product config

Scratch imageが所有する完成済みfileである。

```text
/usr/share/nginx/html/mc-remote-product-config.json
```

```json
{
  "schema_version": 1,
  "homepage_url": "https://example.org/",
  "notices": [
    {
      "heading": "開発元からのお知らせ",
      "body": "..."
    }
  ]
}
```

ここには製品homepage、開発元Notice、showcase等のbuild固有Noticeを置く。client versionとsource identityは
compile-time identityおよびOCI metadataで管理し、このfileやruntime configへ重複させない。

Stackはproduct configを生成、mount、上書きしない。

### 3.2 Runtime config

deploymentが所有する完成済みfileである。Stackはorderから生成し、Scratch imageの次のpathへread-onlyで
mountする。

```text
/usr/share/nginx/html/mc-remote-runtime-config.json
```

```json
{
  "schema_version": 1,
  "connection_enabled": true,
  "bridge_url": "wss://bridge.example.org/",
  "default_sandbox": "minecraft.example.org",
  "connection_targets": [
    {
      "id": "classroom",
      "label": "Classroom",
      "sandbox": "minecraft.example.org"
    }
  ],
  "wirescope_url": "https://wirescope.example.org/",
  "notices": [
    {
      "heading": "授業のお知らせ",
      "body": "本日の利用時間は16時までです。"
    }
  ]
}
```

`wirescope_url`と`notices`は省略できる。Noticeの一項目は`heading`と`body`、任意の構造化
`link: {href, label}`を持てる。本文はplain textとし、任意HTMLを入力にしない。

`connection_enabled`は通常operatorが選ぶ項目ではなく、Stackの通常出力は`true`とする。ただし意図的に
接続を持たないshowcaseと、missing／invalid configを区別する内部guardとしてcontractには残す。

```text
connection_enabled=false
  → bridge_url、default_sandbox、connection_targetsを省略できる正常なdisabled状態

connection_enabled=true
  → bridge_url、default_sandbox、1件以上のconnection_targetsが必須
```

imageには特定deploymentへ接続しないdisabled runtime configを同梱できる。Stackによるmountはこのfile全体を
置換してよい。product情報は別fileなので失われない。

### 3.3 Browserでの扱い

browserは二fileを別々に読み、第三のeffective config fileを生成しない。Notice UIは次の固定順で並べる。

```text
1. deployment / operator Notice
2. product Notice
```

runtime configがmissing、HTTP error、schema不正なら、Scratch Editorは起動したままMcRemote接続だけを
fail-closeし、設定異常を表示する。product configが読めない場合もEditorと正常なruntime接続は止めず、
product情報の異常を表示する。

二つのconfigと`index.html`は`no-store`相当、hash付きbundle assetは長期cache可とする。

## 4. Scratchが公開するcontract directory

scratch-editorは次を一組で所有する。

```text
packages/scratch-gui/contracts/runtime-config/
├── schema.json
└── fixtures/
    ├── valid.json
    ├── disabled.json
    └── invalid/
```

schemaはnested objectを含め未知fieldを拒否する。fixture、loader test、container mount path、cache header testを
同じ変更で維持する。deployment runtime configはMinecraft Remote Protocolではないため、
`@mc-remote/protocol`へ入れない。

product configのschema／fixtureはScratch内部contractとして、隣接する次のdirectoryへ置く。

```text
packages/scratch-gui/contracts/product-config/
```

Stack担当へ渡す正式な入力は次だけである。

```text
scratch contract commit
runtime-config contract directory path
container mount path
Scratch image digest
実行したtestと結果
```

Stack担当はこのdirectory以外のScratch sourceからfieldを発掘しない。

## 5. Stackのorder

通常orderの外形は次とする。

```toml
schema_version = 1
deployment = "school-a"
preset = "classroom@1"

[surfaces]
scratch_url = "https://scratch.example.org/"
bridge_url = "wss://bridge.example.org/"
wirescope_url = "https://wirescope.example.org/"

[[targets]]
id = "classroom"
label = "Classroom"
sandbox = "minecraft.example.org"
default = true

[[notices]]
heading = "授業のお知らせ"
body = "本日の利用時間は16時までです。"
```

`surfaces.wirescope_url`と`notices`は省略できる。surfaceはhostnameでなく完全URLを受け取るため、公開DNS、
LAN、private network、同一hostnameのport分離を別schemaへ分けない。

operatorに通常指定させない値はpresetが所有する。

- component versionとimage digest
- renderer revision
- container topologyと内部port
- volumeとcomponent固有の配置
- channel、exposure、purpose等の内部分類

presetは名前付きのimmutable revisionであり、movingな`latest`や未固定branchを含めない。component単位overrideは
具体的な運用要求が現れるまで通常surfaceへ追加しない。

依頼に合うpresetが無い場合、Stack担当は会話で確認されたcomponent／artifact setと構築方式から新しいimmutable
presetを作成して進める。これはStack担当がcomponent候補を独自選定するという意味ではない。実際に使うartifactの
identityをpreset／lockへ固定する。

## 6. 一つのtargetから導出する

targetはorderへ一度だけ書く。`default=true`は正確に一件とし、0件または複数件はorder errorにする。

Stackは同じtarget集合から次を生成する。

```text
Scratch runtime config
  connection_targets = [{id, label, sandbox}, ...]
  default_sandbox = default=trueのtargetのsandbox

Bridge config
  sandbox allowlist = targets[].sandbox
  upstream target = presetとtargetから導出
```

`sandbox`はtarget集合内で一意とする。Scratch用targetとBridge allowlistを別々に入力させない。

当面は`{id, label, sandbox}`を維持する。browser selector、gameplay address、Bridge upstreamを別modelへ
分解するのは、現行modelで表現できない実deploymentが現れた場合の別判断とする。

### 6.1 配置topologyとbrowser TLS

同じrelease setでも、Scratch／BridgeとMinecraft／McRemoteを置く場所により、証明書の要否と運用負担が変わる。
次の三形を既知のtopologyとして扱い、毎回ゼロから選択肢を調査しない。

| topology | Scratch／Bridge | Minecraft／McRemote | browser transport |
| --- | --- | --- | --- |
| 通常dev | 開発者workstationのloopback | LAN内server host | server hostの証明書は不要。HTTP loopback pageからWS loopback Bridgeへ接続する開発用例外を使う |
| 一体型 | deployment host | 同じdeployment host | 明示profile内のHTTP＋same-origin WS簡易mode、または信頼済みHTTPS／WSSを選ぶ |
| Web edge／Sandbox分離型 | Internet到達可能なedge host | 外部のMinecraft host | edgeでHTTPS／WSSを終端し、BridgeからMcRemoteへTCP接続する |

ケータリング型はpreset、order、lock、artifactを用いる構築方式であり、上表のtopology名ではない。通常dev、一体型、
Web edge／Sandbox分離型のいずれも、対応profileとartifactがあればケータリング型で構築できる。

一体型をprivate networkだけで使う場合は、次の三つからbrowser transportを選ぶ。

- `classroom-all-in-one`等の明示profileに限り、HTTP＋same-origin WS簡易modeを使える。このmodeではMcRemoteを
  利用できるが、camera、microphone、Web Crypto等のsecure-context機能が制限され得ることを利用者へ表示する。
  b7 Scratch runtime contractは平文WSをHTTP loopback page／loopback Bridgeの組だけに制限しており、非loopbackの
  LAN簡易modeは未実装である。このためb7一体型では、Scratchを変更して同modeを実装・検証するまではHTTPS／WSSを使う。
- Caddy等のinternal CAでLAN内証明書を発行し、利用するPC／tabletへroot CAを信頼させる。Internetからの到達は
  不要だが、利用端末ごとのtrust配布を運用対象にする。
- 公開DNS名とpublic CAを使う。ACME HTTP-01のvalidationにはInternetからTCP/80への到達が必要であり、
  公開HTTPS surfaceの提供には別にTCP/443への到達が必要である。DNS-01等を使う場合は、DNS provider、credential、
  Caddy buildを別途確定する。

通常devはこの問題をserver側で解いているのではない。Scratch browserとBridgeをworkstationのloopbackへ置き、
Minecraft／McRemoteだけをLAN serverへ置くため、server hostにWeb証明書を配備しない。

Web edge／Sandbox分離型では、Bridge allowlistをorderのtarget集合と完全一致させ、外部McRemote portへの到達性、
認証強制を必須とする。初期presetがtarget一件だけを扱う場合は、そのpresetの制約として明示する。backendが対応する
場合はMcRemote portの接続元をedge hostへ制限する。現行contractでは
browser→edgeだけをTLSで保護し、edge→McRemoteの平文TCPは採用時に明示して受容するresidual riskである。
source制限を提供しないmanaged game hostをbackendに使う場合も、この制約と認証強制を確認した条件付きtopologyとして
扱える。

channelとexposureは`2026-07-23-01`どおり独立であり、`alpha`／`dev`というchannel名から公開／非公開を導出しない。
非公開規定を持つenvironmentを公開するには、orderへ`exposure=public`を明示し、human ownerの公開承認をapply入力として
記録し、profile／purpose／security policyとのcross-field validationを通す。compact deployment interface v1は
exposureと公開承認をまだorder／lockへ表現しないため、この組合せを許可せず、対応schemaとvalidationの実装まで
public `alpha`／`dev` applyをfail closedとする。

最初の`classroom@1`縦sliceは同一Compose network内へMinecraftを置く一体型である。Web edge／Sandbox分離型は
利用可能な設計選択肢だが、Stackが対応profile／presetと外部到達を検査するdoctorを実装するまでは、既存presetへ
hostnameだけを差し替えて適用しない。

## 7. Stackのrender、apply、doctor

Stackの意味は次の一文で表す。

> immutableなpresetと一つのoperator orderから、exact artifact setとcomponent設定を生成し、環境を起動して
> 実際の到達性を確認するdeployment tool。

rendererはpresetごとに全体を複製せず、共通pipelineをpreset dataとorderで駆動する。解決したartifactとimageは
identity／digestでlockする。

通常commandは次の二つである。

```text
apply <mc-remote.toml>
doctor <deployment>
```

`apply`はdeploymentの有無からcreate／updateを判定し、通常利用者へ別のbootstrap／update手順を要求しない。
同じorder、preset revision、artifact setは意味的に同じcomponent設定を生成する。timestampや絶対pathまでの
byte一致は要求しない。

`apply`前のread-only preflightは、同名Compose projectだけでなく、host-native process、別Compose project、
対象topologyが使用する全TCP／UDP portのlistenerと所有者を確認する。対象deploymentと衝突しない無関係なserviceを
停止することは通常経路の前提にしない。

Minecraft releaseの後退拒否は、既存worldを引き継ぐupdateで旧versionへ戻そうとする場合に適用する。独立した
新規deploymentや新規worldは、同じhost上に新しいidentityと非衝突資源で作る限り、この拒否の対象にしない。

`doctor`は最低限、次を実環境から確認する。

- Scratch URLが応答する
- 配信runtime configがScratch schemaを満たす
- Scratch target集合とBridge allowlistが一致する
- default targetが一件存在する
- BridgeからMcRemoteへ到達できる
- McRemote認証が通常既定のenforcement ONで動作する

## 8. 担当別実装境界

### Scratch担当

この文書、repo固有指示、Scratch側contractだけを読む。Stack repoは調査しない。

実装するもの:

1. product configとruntime configの分離
2. 二fileの独立読込と固定Notice順
3. schema／fixture／loader test
4. missing／invalid時のEditor継続と接続fail-close
5. mount pathとcache header
6. showcaseのdisabled runtime configとproduct Noticeへの移行
7. merge用entrypoint、`jq`、environment matrixを持たないScratch image
8. CIでのimage build
9. Stackへのcontract handoff

完了条件:

- runtime configを全面置換してもproduct Noticeとhomepageが残る
- operator Noticeがproduct Noticeより先に表示される
- 片方または両方のconfig異常でもEditor自体は起動する
- invalid runtime configではtoken読出しとWebSocket生成へ進まない
- valid runtime configでは指定targetへ接続できる
- nested unknown fieldをtestで拒否する
- deployment hostnameやsecretをimageへ焼かない
- container内merge機構がない
- unit／deterministic testとimage buildがPASSする

### Stack担当

この文書、repo固有指示、Scratchから返されたcontract handoffだけを読む。contract directory以外のScratch sourceは
調査しない。

実装するもの:

1. 一つの`mc-remote.toml`
2. 最小preset一件
3. 一つのtarget集合からScratch configとBridge allowlistを生成
4. Scratch schemaによるrender validation
5. runtime configだけのread-only mount
6. preset dataで駆動する共通renderer
7. create／updateを隠蔽する通常`apply`
8. 最小`doctor`
9. exact image lock
10. operator向けREADMEを「一file・apply・doctor」から始める

完了条件:

- target入力がorder内の一箇所だけにある
- runtime configがScratch schemaを通る
- Stackがproduct config、product Notice、release identityを生成しない
- 一つのorderと`apply`で最小環境を起動できる
- 管理者がrender済みfileを編集しない
- preset追加のためrenderer全体を複製しない
- unit／deterministic testがPASSする

## 9. 最初の縦slice

最初に次だけを通す。

- preset一件
- target一件
- operator Notice 0件または1件
- Scratch image
- Bridge image
- 現在利用可能なMinecraft／Paper＋McRemote配置
- optionalな既存WireScope URL

横断確認は、exact artifact setで`apply`し、Scratch表示、Notice順、pairing／認証、block write／read、doctorを
確認する。

## 10. 今回作らないもの

- product defaults＋overlay＋effective configの三層merge
- environment入力とfile入力の二経路
- Noticeのinherit／prepend／append／replace
- WireScope OCI image
- McRemote専用server image
- managed／external／host-native mode taxonomy
- target modelの先行再設計
- backup、restore、credential lifecycleの再設計
- component単位overrideの一般公開
- 多地点doctor分類
- 新しいSBOM／provenance体系

これらを将来禁止するのではない。最初のdeployment interfaceを成立させる条件にしない。
