# C#の実装を始める依頼（Phase I、最初の縦slice）

> 一般用途のC# Client Library（`Naohiro2g/minecraft-remote-csharp`、`18-csharp-client/README_ja.md`）の実装を始める。
> `2026-10-23-01`④は、C#の実装をTypeScriptのPhase Bが通ってから始めるとした。TypeScriptは2026-11-11に最初の縦sliceを返した
> （`00-hub/polyglot-typescript-start-instructions_ja.md`の「返却と照合（2026-11-11）」）。human owner 2026-11-10：「クライアントの
> 多言語化を最優先とする。その先のUnity版マイクラリモコンを急ぐため」。参照するknowledge commitは、この依頼が入ったmainの
> commitです。

## 目標

C#のコードを書いて実行すると、McRemoteへつながってMinecraftの世界が変わり、それを読み戻せる
（`10-protocol/polyglot-client-roadmap_ja.md`の「8. Phase B」と同じ縦slice。「25. Phase I」）。

- connect → `hello` → protocolの互換判定 → 認証（初回のpairingを1回） → `world.setBlock` → `world.getBlock` → close
- 対象は直接のTCPだけ。WebSocketとBridgeの経路は後
- library projectは`netstandard2.1`のまま（Unityから使える）。Unityのprojectは、このsliceに入れない

## 入力

- 主な入力は、knowledgeのProtocol contractと共有fixture。Python、Java、TypeScriptは調べる材料に使ってよいが、正本にせず、
  コードを翻訳しない
- contract：`10-protocol/wire-format-design_ja.md`の「2. トランスポートとフレーミング」「3. エンベロープ（JSON-RPC 2.0）」
  （「3.4 id 規律」を含む）「6. helloペイロード」「6.5 認証：ペアリングフロー」「4. コマンド表（確定）」「7.1 構造化block value」
  「7.3 エラー設計」、`10-protocol/versioning-design_ja.md`の「8. hello による protocol ネゴシエーション」、
  `10-protocol/block-value-design_ja.md`
- 共有fixture：minecraft-remote-tooling `36ebe9e63e4f0afcf949eae998832f68209b8119`の`packages/protocol/test/fixtures/`にある、F1の6本
  （`client-bootstrap-{framing,hello,pairing,blocks,errors,close}-v23.2.1.json`、48 case）、`client-bootstrap-v1.schema.json`、
  blocksの`value_refs`が参照する`block-value-v22.json`。scripted peerのデータの形は、同じcommitの`packages/protocol/README.md`
- fixtureは固定したcommitで読む（F2、`2026-10-22-07`）。copyで持つときは、同じディレクトリの`LICENSE`（1,070 bytes、SHA-256
  `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`）も一緒に置く。`@mc-remote/protocol`のコードには依存しない
- F1は、2026-11-11にE2の決定へ合わせた（`00-hub/polyglot-f1-e2-fixture-instructions_ja.md`の「返却と照合（2026-11-11）」）。
  toolingは今、互換判定の後のcloseと、②の残りのcaseを先に足している（`00-hub/polyglot-f1-e2-ops-fixture-instructions_ja.md`の1）。
  そのmerge commitはcoordinatorから伝えるので、届いたら取得元を固定し直す。それまでは`36ebe9e`で進める

## 決まっていること（守るもの）

- 申告するprotocolは、fixtureと同じ`23.2.1`
- 応答の版の互換判定：majorの一致、serverのminorが同じか上、patchは見ない（versioningの「8.2」）。互換でないと判定したら、
  次のrequestを送らずに接続を閉じ、applicationへ失敗を返す（`2026-11-12-01`）
- `protocol_mismatch`は`data.reason`で判定し、codeでは分けない。`data.server`と`data.client_requires`をerrorから読めるようにする
  （`2026-11-10-01`）
- 認証：まずhelloを試し、`auth_required`のときだけpairingに入る（`2026-07-04-06`）。`token_expired`／`token_revoked`／
  `token_not_found`／`token_invalid`では該当のtokenを消し、tokenなしのhelloへ戻る。すぐpairingへは進まない（`2026-11-11-01`⑦）。
  pairingは一接続試行につき一度だけ。`permission_denied`、`protocol_mismatch`、networkの障害ではtokenを消さない（`2026-08-30-03`）
- credentialは、注入できるstoreと、`none`とin-memoryの実装を持つ。OSの資格情報storeと、作例でtokenを使い回すstoreは、
  このsliceに入れない（TypeScriptと同じ。hub NOTES 2026-11-11の行）
- clientが`expires_in`を過ぎたと判断したpairingの期限切れは、`pair_expired`と同じ意味で扱えるようにし、serverのerrorの形
  （codeとreason）は作らない。serverが言ったのか、clientが判断したのかが分かるようにする（`2026-11-11-01`⑧）
- 接続が閉じたら、応答待ちのrequestをすべて、localな「完了不明」の失敗にする。serverのerrorとしては扱わず、reasonを作らない。
  LFの無い末尾は応答にしない（`2026-11-11-01`②）
- 自動で再送しない（`2026-11-11-01`④）
- errorは、code、message、`data`を保ち、知らないreasonも保つ（F1のerrorsのcase）
- token、`pairing_id`、private endpointを、source、test、通常のlog、公開のartifactへ出さない。pair codeと表示用のpairing commandは
  表示してよい（`2026-08-30-03`）

## 進め方

- 振る舞いを足すときは、F1のcaseが、足す前に意図した理由で落ちることを見てから足す
- 合格：CIで、F1の48 caseがすべてPASSする。skipを残したら済みにしない。caseが契約と違う、または読み方が決まらないと思ったら、
  そのcaseのIDと理由を返す
- 待ち方（`2026-11-11-01`③：既定で長く粘り強く待ち、最後に受信してからの時間で見て、超えたら「完了不明」で回収する）と、
  自動のつなぎ直し（⑤：次の呼び出しで、既定で有効）は、このsliceでは入れなくてよい。入れるなら決定のとおりにする。入れない
  なら、後で足せるAPIの形（timeoutの設定、つなぎ直しの有効と無効、つなぎ直したことの知らせ）を案にして返す。TypeScriptも
  次の票で入れる
- 決まっていないことは、clientで新しく決めない。決める必要が出たら、決めずに返す
- 実McRemoteとのpulse：hello → `world.setBlock` → `world.getBlock`を1本通す。相手は担当の手元のPaperと、公開のMcRemote
  `2321.1.0`。Minecraftの中での承認など、人の操作が要るなら、その前で止めて手順を返す（human ownerが行う）。Python、Java、
  TypeScriptと同じく「live-auto相当」で、scriptとPASSのsummaryを残す（`2026-07-06-03`）。置いたブロックを戻す手順も書く
- Client APIの形（名前、`async`／`Task`、errorの型、credential storeの差し込み方）は、C#に自然な形を担当が案にして返す。
  Python、Java、TypeScriptと同じ形にそろえることは求めない（ロードマップ「33. このロードマップが作らないもの」）
- Unityから使うことを考えて、APIの形を選ぶ。依存を足すときは、`netstandard2.1`とUnityで使えるかを確かめて返す
- 作例を1つ置く（つないで、ブロックを1つ置き、読み戻す）。pulseと同じものでよい
- Unityのfileは、2026-11-11に`mc-remote-unity-sandbox`へ移した（`00-hub/unity-sandbox-migration-instructions_ja.md`の「返却と照合
  （2026-11-11）」、`2026-11-11-02`）。このsliceでUnityのprojectを足さない
- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい（権限で拒まれたら、human ownerが行う）。NuGetへのpack、publish、
  tag、Release、release workflowは足さない

## TypeScriptの返却で、C#のために足りないとされたもの

TypeScriptの担当が、F1と契約だけでは足りないと返したもの。決まったものと、C#で見てほしいものに分ける。

- 決まった：切断、timeout、再送（`2026-11-11-01`②③④）。認証reasonの後の流れ（⑦）
- `auth.pairBegin`の`client`：wire「6.5」は`client`を省けるとは書いていない。載せて送る
- 期限とpollの順：F1-AU-02は、期限を過ぎた後もpollを1回送ることを前提にしている。このcaseは今のまま通す。⑧とぶつかると
  思ったら、そのことを返す（toolingにも、このcaseの案を頼んでいる）
- 行末のCR：wireの区切りはLF。CRをどう扱ったかを返す
- credentialのkeyに入れるfieldの組：`2026-08-30-03`の「target単位」を、どのfieldの組で表したかを返す（TypeScriptは
  application、session、tcp、接続先の組）
- F1に無い流れ：認証reasonの後のhelloと、pairingの後のhelloがまた拒まれる流れは、F1-AU-08〜10になった（`36ebe9e`）。
  clientの側の互換判定で不一致になった後のcloseは、`2026-11-12-01`で決め、toolingへcaseを頼んでいる。それまでは、上の
  「決まっていること」に合わせ、testは担当のunit testで持つ

## 返却

- 実際に読んだknowledge commit、PRの番号、merge commit、CIのrun ID
- fixtureの取得元（commit、copyならfileごとのbytesとSHA-256）と、fileごとのcase数とPASS数
- Client APIの案（公開する型とメソッドの一覧、errorの型、credential storeの差し込み方）と、そう決めた理由
- Unityから使うときに気をつけること（threadとmain thread、`async`の使い方、依存）
- 待ち方とつなぎ直し（③⑤）を入れたか。入れないなら、後で足せるAPIの形の案
- pulse：日付、Paperの版、McRemoteの版、手順、結果、認証の方法、片付けの方法。token、pair code、host、IP、player名、座標は書かない
- 違うと思ったcase、決めずに残したこと
- 上の「C#のために足りないとされたもの」の各項を、どう扱ったか
- Python、Java、TypeScriptを調べて分かった違いのうち、Protocolで決めるべきだと思ったもの
- E1の列の案：Protocol Inventoryの、このsliceで投影したmethodと能力の行

## coordinatorがすること

- 返却を、GitHubのAPI（PR、merge commit、CI、fixtureのbytes）で照合し、Protocol InventoryにC#の列を足す
- `18-csharp-client/README_ja.md`の「現在地」を直す
- toolingが直したF1のmerge commitを伝える

## 返却と照合（2026-11-12）

C#担当はknowledge `076a127a22eaf0188c1d13822bfd55bfeee9ec38`を読んだ（この票の本文は今と同じ）。2つのPRを、担当が2026-11-12に
mergeした。coordinatorはGitHubのAPIで、PR、merge commit、CI、fixtureのcopyを確かめた。CIのlogは取得が失敗したので、test数は
担当の返却による。

### 最初の縦slice（PR #3）

- minecraft-remote-csharp PR #3（head `dca92b84899805bfd234e41cae93c8842a95ce3c`、base `9b623c9b1cd0d5b344bd958586af3897f6a19b9b`、
  26 file）をmerge commit `bbca1e44dd0e6defc1092d1d47f956918904658e`でmergeした。CIはPRのrun `43094217375`、merge後のrun
  `43094376844`とも成功。71 testが通り、fail 0、skip 0、build警告0
- fixture：tooling `36ebe9e`の9 file（F1の6本、schema、`block-value-v22.json`、LICENSE）を`tests/MinecraftRemote.Client.Tests/Fixtures/`
  にcopyした。coordinatorは9 fileが`36ebe9e`の同じfileとGit blobで一致することを確かめた。F1は48 case、48 PASS。空のstubで
  落ちることを見てから足した
- Client APIの案：`MinecraftClient.ConnectAsync`、`SetBlockAsync`、`GetBlockAsync`、低水準の`RequestAsync`、`CloseAsync`と
  `DisposeAsync`（`await using`）。serverのerrorは`RemoteErrorException`（code、元のmessage、data、知らないreasonを保つ。
  `IsProtocolMismatch`はreasonで判定し、`server`と`client_requires`を読める）。localな失敗は`ProtocolCompatibilityException`、
  `PairingRequiredException`、`PairingExpiredException`、`ConnectionFailedException`、`RequestNotSentException`、
  `CompletionUnknownException`で、codeとreasonを作らない。credentialは`ICredentialStore`を接続の時に差し込み、`NoCredentialStore`
  （既定）と`InMemoryCredentialStore`。削除は、拒まれたtokenと一致するときだけ（別の接続が保存した新しいtokenを消さない）。
  全体は同じcommitの`docs/client-api_ja.md`
- Unity：依存はNewtonsoft.Json 13.0.4だけ（netstandard2.0のasset）。repoの外のUnity 6000.6.8f1に、作ったDLLを入れ、loopbackのTCPで
  hello、setBlock、getBlock、closeを確かめた。IL2CPP、mobile、Web、UPMでの配布は確かめていない。内部の`await`は
  `ConfigureAwait(false)`で、callbackはbackgroundのthreadから呼ばれうるので、UnityのUIはmain threadへ戻す
- ③⑤：入れていない。案は`ClientOptions.ResponseIdleTimeout`と呼び出しごとの`RequestOptions.ResponseIdleTimeout`、
  `ClientOptions.AutoReconnectEnabled`（既定true）、`ConnectionRestored`の通知。つなぎ直しで認証が要れば、pairingせずにcallerへ返す
- pulse（live-auto相当）：2026-11-12、Paper 1.21.11（build 132）、McRemote `2321.1.0`。`examples/FirstBlock/Program.cs`で、tokenなしの
  helloからpairing（human ownerがMinecraftの中で承認）、hello、金のブロックを置いて読み戻し、close。PASS。`NoCredentialStore`で
  tokenを保存しない。置いたブロックは、human ownerの指示で残した
- 実機で見つかったこと：承認を待つ間に、McRemoteが認証前のTCPを閉じた。C#は、同じ`pairing_id`の未送信のpollだけを新しいTCPで
  続けるように直し、回帰testを足した（wire「6.5」の「同じTCPを保たなくてよい」のとおり）。F1にこの流れのcaseは無い
- TypeScriptの返却で、C#のために足りないとされたもの：`auth.pairBegin`の`client`は、helloと同じ情報を必ず付ける。期限とpollの
  順は、F1-AU-02（期限の後のpollにserverが`pair_expired`）をそのまま通し、公開の`ConnectAsync`はpollの前に単調な時計で期限を
  見て`PairingExpiredException`にする（serverのerrorを作らない）。行末のCRは、CRLFのCRをJSONの行末の空白として受け、CRだけでは
  区切らない。credentialのkeyは、applicationId、sessionId、tcp、小文字にしたliteralのhost、portの組。F1に無かった流れは、
  F1-AU-08〜10と、HE-04、05を使う担当のunit testで確かめた
- 違うと思ったcase：無し。Protocolで決めるべき違い：Python、Java、TypeScriptを調べていないので、無し
- E1の列の案：同じcommitの`docs/polyglot-e1_ja.md`。method「あり」はhello、`world.setBlock`、`world.getBlock`、`auth.pairBegin`、
  `auth.pairPoll`。Protocol InventoryにC#の列を足した

### F1の固定し直し（PR #4）

- toolingの票（`00-hub/polyglot-f1-e2-ops-fixture-instructions_ja.md`）の1のmerge commit `d2691cd`を伝えた。PR #4（head
  `96b93665638e34b322a2c51f1ab70c908f5760d2`、base `bbca1e4`、9 file）をmerge commit `1f069dc321dbb3534447584946ec2cfd7912a289`で
  mergeした（`main`の先頭）。CIはPRのrun `43165286710`、merge後のrun `43165425294`とも成功。75 testが通り、skip 0
- copyした9 fileは、tooling `d2691cd`とGit blobで一致した。v1は52 case、52 PASS。v2は使っていない
- HE-11、12は、client自身が閉じたことによるEOF、次のrequestが無いこと、clientから来た`ProtocolCompatibilityException`を確かめる。
  CL-07はLFの無い末尾のEOFで応答にせず完了不明、CL-08は自分で閉じた時に応答待ちをすべて完了不明にする。libraryの振る舞いは
  変える必要が無かった
