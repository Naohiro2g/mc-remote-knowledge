# b8横断release gate 統一実施票

> 状態: **完了・履歴**。b8横断release gateは2026-10-03にCLOSEDとなった（`00-hub/release-gate-notes_ja.md`の2026-09-30の節）。
> 現在の指示ではなく、b8で出した票の記録として残す。

> 凍結したexact set `b8-integrated-artifact-set-1`（`00-hub/release-gate-notes_ja.md`の2026-09-30の節）を、devの通常環境で
> 確かめる実施票です。上から順に進めます。各segmentの担当は、自分のsegmentと「共通」を読んでください。

## 共通

- 使うもの: 凍結したidentityだけを使う。McRemote JAR `7ab24fa1…77fb`、Python `52d35f5`のwheel `dcedff01…0180`、Scratch `691576f`、
  fixture `054a3af`。未pushのworktreeや一時buildを差し込まない
- 場所: devの通常環境（Paper／McRemoteはホームサーバーでhost-native、Scratch／Bridgeは手元の開発端末）
- 開始時の照合: どのsegmentも、最初の認証済み`hello`で`protocol`が`23.2.0`、`mc_version`が`1.21.11`であることを確かめる。
  違えば本体を実行せずFAILとして返す（`2026-09-28-03`）
- 認証: devの`auth.enforcement`は変えない（ONのまま）。pairingが要るときはhuman ownerが承認する
- 止め方: 失敗したらそのsegmentで止め、要求・応答・reason・使ったidentityをcoordinatorへ返す。その場で直して続けない。
  直すときはcomponent側で修正し、凍結し直す
- 返却: segmentごとに、使ったidentity、PASS／FAILの一覧、観測、未実施の範囲を一枚で返す。token、pairing_id、private address、
  player UUIDは書かない（pair codeは書いてよい）

## 0. 環境の準備（human owner）

1. devの通常環境で、今のMcRemote JAR（b7）を退避し、`mc-remote-1.21.11-2320.0.0b8.jar`（`7ab24fa1…77fb`）へ一件だけ差し替えて
   再起動する。Paper、world、config、credentialはそのまま
2. 差し替えた後のidentityを記録する: MC版、Paperのbuild、Java版、JARのSHA-256。server logの`Auth enforcement: true`と
   `Credential domain health: HEALTHY`。旧`b5:`／`b7:`キーの移行のログ
3. **実tokenの継続**: b7のときにpairingしたclient（Pythonかscratchの保存済みtoken）で、pairingし直さずに`hello`する。
   成功すればPASS（b7→b8のupgradeでsession tokenが続く）。`token_not_found`ならFAILとして記録し、そのtokenがdevで発行された
   ものかもあわせて書く

## 1. McRemote — live-auto

- `scripts/live_auto.py --expect-mc 1.21.11 --protocol 23.2.0 --handle-capacity 256 --particle-limit 1000`をdevに対して流す
- 認証はONのまま。pairingが要るならhuman ownerに承認してもらう（ローカルで使った`auth.enforcement=false`の一時bypassはdevでは
  使わない）
- 返却: PASS行の数、FAILの内容、試験で作ったentity／blockの扱い

## 2. Python — 代表往復

- `52d35f5`のwheelで、devへ接続する
- entity lifecycle（spawn→nearby→pose get／set→remove）、ParticleSpec（dust、block、`receiver`の`world`／`self`）、サウンド2 method
  （`pitch`と`note`、`playBlockSound`の既定）、無印のID（`flame`、`cow`、`block.bell.use`）、短いimport
- WireScope（Python source）を開き、上の操作のframeが表示されることをhuman ownerが目で確かめる（Python担当はbrowserを操作できない）
- 3D graphのsample（`examples/particle_graph.py`）を流す
- 返却: 操作ごとのPASS／FAIL、WireScopeの表示の観測

## 3. Scratch — 学習面とreal-browser WireScope

- 手元の開発端末で`691576f`のScratch／Bridgeを動かし、devへ接続する
- entity／particleの9ブロック、サウンド2 command、カタログID一覧ブロック、pickerの日本語名と検索、既定値の省略
- WireScope（Scratch source）を、Scratch担当が独立のChromiumで開き、上の操作のframe（B8 entityの4 method、typed particle、
  particleのFAST通知、サウンド）が落ちずに表示されることを確かめる。human ownerも目で確かめる
- b7 release後の是正3件（空pollで履歴を押し出さない、数値欄のCtrl+C／Ctrl+V、backpressureの案内）
- 返却: ブロックごとのPASS／FAIL、WireScopeのscreenshotの観測（画像はGit外）

## 4. live-human（human owner。2人目のplayerが要る）

1. receiver: particleとサウンドそれぞれで、`self`は送った本人にだけ、`world`は周りの全員に届く
2. dust（色と大きさ）とblockのparticleが描画される
3. 音が聞こえる。左右の定位と、離れたときの減衰がある。`note`で音階が変わる。`playBlockSound`の5つの`kind`が鳴る
4. 3D graphのsampleの描画

## 5. その後

- coordinatorが各segmentの返却を`14-evidence/`のsanitized recordにまとめ、横断の`GREEN`／`HOLD`／`RED`を判定する
- human ownerの公開承認の後、coordinatorが各repoへ公開の指示票を出す
