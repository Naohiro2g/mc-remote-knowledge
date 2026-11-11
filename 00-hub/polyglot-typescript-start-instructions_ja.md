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

## 返却と照合（2026-11-11）

TypeScript担当はknowledge `bb34378b3368b68464a3a996bad9df0aaa6ac41b`を読んだ（この票の本文は今と同じ）。minecraft-remote-typescript
PR #2（head `b10c6585617551d0c5ff4de29ce20bac2e36d120`）を、human ownerが2026-11-11にmerge commit
`9984d1a71b554aa62fa176661c15b2671f306353`でmergeした（`main`の先頭。agentのmergeはClaude Codeの権限で拒否された）。
coordinatorはGitHubのAPIで、PR、merge commit、CIの3 run、fixtureのcopy、作例を確かめた。

- CI：PRのrun 42952319110、pushのrun 42952292065（どちらもhead）、merge後のrun 42953541965が成功。どれも53件PASS（F1の45件、
  fixtureの検査3件、単体5件）で、fail 0、skip 0（件数は担当の返却による）。tag、Release、release workflowは無い。`package.json`は
  `private: true`のまま。`@mc-remote/protocol`には依存しない
- fixture：tooling `131f315`の9 file（F1の6本、schema、`block-value-v22.json`、LICENSE）を`test/fixtures/protocol/`にcopyした。
  coordinatorは9 fileが`131f315`の同じfileとGit blobで一致することを確かめた。testが毎回bytesとSHA-256を確かめる。F1は45 case、
  45 PASS
- 落ちることの確認：空のstubから層を1つずつ足し、各caseが、まだ入れていない振る舞いを理由に落ちることを見てから足した
  （FR-01〜06、HE-04／05、AU-01／02、AU-07、CL-03／05）。公開APIでは送れない入力のF1-FR-07、AU-03、AU-04は、内部のRPC層で送った
- Client APIの案：`connect(options): Promise<MinecraftRemote>`。`MinecraftRemote`は`hello`、`setBlock`、`getBlock`、`call(method,
  params)`、`close()`。errorの基底は`McRemoteError`で、`RemoteError`（code、message、dataを保つ）、`ProtocolMismatchError`
  （`server`、`clientRequires`、`source: 'server' | 'client'`）、`ConnectionError`（reasonを持たない）、`PairingExpiredError`。
  credentialは`CredentialStore { load, save, delete }`を差し込み、実装は`noCredentialStore()`（既定）と`memoryCredentialStore()`。
  keyはapplication、session、tcp、接続先の組。pairingは`onPairing(challenge)`を渡したときだけで、`pairing_id`は渡さない。理由：
  async／awaitとerrorのclass階層がTypeScriptで自然。結果の型をwireの名前のままにして、WireScopeで見る値とそろえる。core libraryに
  暗黙の保存や表示を持たせない（`2026-08-30-03`）
- 決めた振る舞い：申告は`23.2.1`。応答の版の互換判定は「8.2」のとおりで、不一致は`ProtocolMismatchError`（`source: 'client'`）にして
  閉じる。`protocol_mismatch`は`data.reason`で判定する（HE-09、HE-10）。認証reasonではtokenを消してtokenなしのhelloへ戻り、
  `auth_required`のときだけ、一回の`connect()`につき一度pairingする。pairingは専用の接続で行い、その後のhelloは新しい接続
  （F1-AU-01の形）。pollの間隔は1.5秒。切断では応答待ちを`ConnectionError`で失敗させ、LFの無い末尾は応答にしない。timeout、
  自動の再送、自動の再接続は入れていない
- pulse（live-auto相当）：2026-11-11、担当の手元のPaper 1.21.11（build 132）とMcRemote `2321.1.0`。`examples/set-and-get-block.mjs`
  （作例を兼ねる。SHA-256 `fe926080355e766a9edf52a0ca959e5293f2abcdbdbde2d8b1316ec87ccedd07`、coordinatorがmergeの後の`main`で一致を
  確かめた）で、pairing（human ownerがMinecraftの中で承認）、hello（protocol `23.2.1`、Minecraft 1.21.11）、置く位置が空気である
  ことの確認、金のブロックを置いて読み戻し、元へ戻して読み戻し。結果はPASS（`minecraft:gold_block`、`minecraft:air`）。1回目は
  既定の位置が空気ではなく、何も置かずにFAILで止まった。tokenは`memoryCredentialStore()`でprocessの中だけ持ったので、実行の
  たびに承認が要る。worldに残したものは無い。証跡はscriptとPASSのsummaryで、`14-evidence/`にrecordを置かない
- 違うと思ったcase：無し

### 返却の後に決まったこと

- 認証reasonの後にtokenなしのhelloへ戻ること（`2026-11-11-01`⑦）と、clientが判断したpairingの期限切れをserverのerrorと分けること
  （⑧）は、TypeScriptの今の形で決まった。Javaは違うので、Javaへの票で直してもらう
- 切断の時の応答待ち（②）は、TypeScriptの今の形と合う。timeout（③）と自動のつなぎ直し（⑤、次の呼び出しで、既定で有効）は
  これから入れる。toolingがF1を同じ決定に合わせて返したら、取得元の固定し直しと一緒に、TypeScriptへの次の票で頼む
- 作例でtokenを使い回すstore：human owner 2026-11-11「このスライスでは不要にしてもよいが。」 このsliceでは入れない
  （hub NOTES 2026-11-11の行）
- C#のために足りないと返されたもの（`auth.pairBegin`の`client`を省けるか、期限の後にpollを1回送るか、行末のCR、credentialの
  keyの組、F1に無い流れ）は、C#の票とtoolingへの票で扱う。F1に無い流れと、期限の後のpollは、toolingへの票
  （`00-hub/polyglot-f1-e2-fixture-instructions_ja.md`）に入れた
