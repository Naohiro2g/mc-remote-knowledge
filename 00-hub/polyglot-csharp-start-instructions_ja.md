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
- 共有fixture：minecraft-remote-tooling `131f3153d7ab0b01b6e00a62a8249a55c8fc2ad0`の`packages/protocol/test/fixtures/`にある、F1の6本
  （`client-bootstrap-{framing,hello,pairing,blocks,errors,close}-v23.2.1.json`、45 case）、`client-bootstrap-v1.schema.json`、
  blocksの`value_refs`が参照する`block-value-v22.json`。scripted peerのデータの形は、同じcommitの`packages/protocol/README.md`
- fixtureは固定したcommitで読む（F2、`2026-10-22-07`）。copyで持つときは、同じディレクトリの`LICENSE`（1,070 bytes、SHA-256
  `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`）も一緒に置く。`@mc-remote/protocol`のコードには依存しない
- toolingは今、F1をE2の決定に合わせて直している（`00-hub/polyglot-f1-e2-fixture-instructions_ja.md`）。直したF1のmerge commitは
  coordinatorから伝えるので、届いたら取得元を固定し直す。それまでは`131f315`で進める

## 決まっていること（守るもの）

- 申告するprotocolは、fixtureと同じ`23.2.1`
- 応答の版の互換判定：majorの一致、serverのminorが同じか上、patchは見ない（versioningの「8.2」）
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
- 合格：CIで、F1の45 caseがすべてPASSする。skipを残したら済みにしない。caseが契約と違う、または読み方が決まらないと思ったら、
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
- F1に無い流れ（認証reasonの後のhello、pairingの後のhelloがまた拒まれる流れ、clientの側の互換判定で不一致になった後のclose）：
  toolingへcaseを頼んでいる。それまでは、上の「決まっていること」に合わせ、testは担当のunit testで持つ

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
