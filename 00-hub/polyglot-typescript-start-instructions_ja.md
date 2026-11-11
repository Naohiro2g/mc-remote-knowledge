# TypeScriptの実装を始める依頼（Phase G、最初の縦slice）

> 一般用途のTypeScript Client Library（`Naohiro2g/minecraft-remote-typescript`、`17-typescript-client/README_ja.md`）の実装を
> 始める。`2026-10-22-07`は、実装を多言語の比較とconformanceの一般化（Phase E／F）の具体化の後にするとした。E1の5列が
> そろい、F1のfixture（45 case）ができ、PythonとJavaがF3を通した（`00-hub/polyglot-f3-instructions_ja.md`）。human owner
> 2026-11-10：「クライアントの多言語化を最優先とする。その先のUnity版マイクラリモコンを急ぐため」。C#の実装は、このsliceが
> 通ってから始める（`2026-10-23-01`④）。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 目標

TypeScriptのコードを書いて実行すると、McRemoteへつながってMinecraftの世界が変わり、それを読み戻せる
（`10-protocol/polyglot-client-roadmap_ja.md`の「8. Phase B」と同じ縦slice。「21. Phase G」）。

- connect → `hello` → protocolの互換判定 → 認証（初回のpairingを1回） → `world.setBlock` → `world.getBlock` → close
- 対象はNode.jsのTCPだけ。browserとWebSocket、Bridgeの経路は後（Phase H）

## 入力

- 主な入力は、knowledgeのProtocol contractと共有fixture。PythonとJavaは調べる材料に使ってよいが、正本にせず、コードを翻訳しない
- contract：`10-protocol/wire-format-design_ja.md`の「2. トランスポートとフレーミング」「3. エンベロープ（JSON-RPC 2.0）」「6. helloペイロード」
  「6.5 認証：ペアリングフロー」「4. コマンド表（確定）」「7.1 構造化block value」「7.3 エラー設計」、`10-protocol/versioning-design_ja.md`の
  「8. hello による protocol ネゴシエーション」、`10-protocol/block-value-design_ja.md`
- 共有fixture：minecraft-remote-tooling `131f3153d7ab0b01b6e00a62a8249a55c8fc2ad0`の`packages/protocol/test/fixtures/`にある、F1の6本
  （`client-bootstrap-{framing,hello,pairing,blocks,errors,close}-v23.2.1.json`、45 case）、`client-bootstrap-v1.schema.json`、
  blocksの`value_refs`が参照する`block-value-v22.json`。fixtureのbytesは、PythonとJavaが固定する`ea7838a`と同じ。scripted peerの
  データの形は、同じcommitの`packages/protocol/README.md`（`matched_ids`の範囲の説明を含む）
- fixtureは固定したcommitで読む（F2、`2026-10-22-07`）。copyで持つときは、同じディレクトリの`LICENSE`（1,070 bytes、SHA-256
  `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`）も一緒に置く。`@mc-remote/protocol`のコードには依存しない

## 決まっていること（守るもの）

- 申告するprotocolは、fixtureと同じ`23.2.1`（human owner 2026-11-11：「TSはまだ何も準備していないので、23.2.1で。」）
- 応答の版の互換判定：majorの一致、serverのminorが同じか上、patchは見ない（versioningの「8.2」）
- `protocol_mismatch`は`data.reason`で判定し、codeでは分けない。`data.server`と`data.client_requires`をerrorから読めるようにする
  （`2026-11-10-01`）
- 認証：まずhelloを試し、`auth_required`のときだけpairingに入る（`2026-07-04-06`）。credentialは、注入できるstoreと、`none`と
  in-memoryの実装を持つ。OSの資格情報storeはこのsliceに入れない。`token_expired`／`token_revoked`／`token_not_found`／
  `token_invalid`では該当のtokenを消し、`auth_required`と合わせて一接続試行につき一度だけpairingする。
  `permission_denied`、`protocol_mismatch`、networkの障害ではtokenを消さない（`2026-08-30-03`）
- errorは、code、message、`data`を保ち、知らないreasonも保つ（F1のerrorsのcase）
- token、`pairing_id`、private endpointを、source、test、通常のlog、公開のartifactへ出さない。pair codeと表示用のpairing commandは
  表示してよい（`2026-08-30-03`）

## 進め方

- 振る舞いを足すときは、F1のcaseが、足す前に意図した理由で落ちることを見てから足す
- 合格：CIで、F1の45 caseがすべてPASSする。skipを残したら済みにしない。caseが契約と違う、または読み方が決まらないと思ったら、
  そのcaseのIDと理由を返す
- `unresolved`に挙がったこと（EOFの時の扱い、応答待ちのrequestの例外の型とtimeout、自動の再送など）は、clientで新しく決めない。
  決める必要が出たら、決めずに返す。coordinatorがE2の案（`10-protocol/polyglot-e2-plan_ja.md`）で決めにいく。決まったら伝える
- 実McRemoteとのpulse：hello → `world.setBlock` → `world.getBlock`を1本通す。相手は担当の手元のPaperと、公開のMcRemote
  `2321.1.0`。Minecraftの中での承認など、人の操作が要るなら、その前で止めて手順を返す（human ownerが行う）。PythonとJavaと同じく
  「live-auto相当」で、scriptとPASSのsummaryを残す（`2026-07-06-03`）。置いたブロックを戻す手順も書く
- Client APIの形（名前、async、errorの型、credential storeの差し込み方）は、TypeScriptに自然な形を担当が案にして返す。
  Python、Javaと同じ形にそろえることは求めない（ロードマップ「33. このロードマップが作らないもの」）
- 作例を1つ置く（つないで、ブロックを1つ置き、読み戻す）。pulseと同じものでよい
- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。npmへのpublish、tag、Release、release workflowは足さない

## 返却

- 実際に読んだknowledge commit、PRの番号、merge commit、CIのrun ID
- fixtureの取得元（commit、copyならfileごとのbytesとSHA-256）と、fileごとのcase数とPASS数
- Client APIの案（公開する型と関数の一覧、errorの型、credential storeの差し込み方）と、そう決めた理由
- pulse：日付、Paperの版、McRemoteの版、手順、結果、認証の方法、片付けの方法。token、pair code、host、IP、player名、座標は書かない
- 違うと思ったcase、決めずに残したこと
- PythonとJavaを調べて分かった違いのうち、Protocolで決めるべきだと思ったもの
- C#（Unity）が次に作るときに、F1と契約だけでは足りないと思ったもの
- E1の列の案：Protocol Inventoryの、このsliceで投影したmethodと能力の行

## coordinatorがすること

- 返却を、GitHubのAPI（PR、merge commit、CI、fixtureのbytes）で照合し、Protocol InventoryにTypeScriptの列を足す
- `17-typescript-client/README_ja.md`の「現在地」を直す
- E2で決まったことを伝える
- C#の実装を始める票を作る（human ownerが時期を決める）
