# b9横断release gate 統一実施票

> 凍結したexact set `b9-integrated-artifact-set-1`（`00-hub/release-gate-notes_ja.md`の2026-10-04の節）を、devの通常環境で
> 確かめる実施票です。上から順に進めます。各segmentの担当は、自分のsegmentと「共通」を読んでください。b9はAPIを変えないので、
> b8のlive PASSを再利用し、変わったところ（`chat.post`の`null`、移管したWireScopeとBridge、JARの作り方）だけを確かめます。

## 共通

- 使うもの: 凍結したidentityだけを使う。McRemote JAR `4feb90db…a58e`、Python `b901c88`のwheel `e166bc9c…38c6`、Scratch `7fbbf03`、
  `minecraft-remote-tooling` `dc1ab83`（WireScope ZIP `da3da0b6…31ad`、Bridge OCI `sha256:5828304c…b84f`）。未pushのworktreeや
  一時buildを差し込まない
- 場所: devの通常環境（Paper／McRemoteはホームサーバーでhost-native、Scratch／Bridgeは手元の開発端末）
- 開始時の照合: どのsegmentも、最初の認証済み`hello`で`protocol`が`23.2.0`、`mc_version`が`1.21.11`であることを確かめる。
  違えば本体を実行せずFAILとして返す（`2026-09-28-03`）
- 認証: devの`auth.enforcement`は変えない（ONのまま）。pairingが要るときはhuman ownerが承認する
- 止め方: 失敗したらそのsegmentで止め、要求・応答・reason・使ったidentityをcoordinatorへ返す。その場で直して続けない
- 返却: segmentごとに、使ったidentity、PASS／FAILの一覧、観測、未実施の範囲を一枚で返す。token、pairing_id、private address、
  player UUIDは書かない（pair codeは書いてよい）
- 知らないevent typeは実サーバーから出せないので、live試験では確かめない。shared fixture `chat-event-compat-v23.2.json`の
  deterministic testで確かめたことを使う

## 0. 環境の準備（human owner）

1. devの通常環境で、今のMcRemote JAR（b8）を退避し、`mc-remote-1.21.11-2320.0.0b9.jar`（`4feb90db…a58e`）へ一件だけ差し替えて
   再起動する。Paper、world、config、credentialはそのまま
2. 差し替えた後のidentityを記録する: MC版、Paperのbuild、Java版、JARのSHA-256。server logの`Auth enforcement: true`と
   `Credential domain health: HEALTHY`
3. **実tokenの継続**: b8のときにpairingしたclient（Pythonかscratchの保存済みtoken）で、pairingし直さずに`hello`する。
   成功すればPASS

## 1. McRemote — live-auto

- `scripts/live_auto.py --expect-mc 1.21.11 --protocol 23.2.0 --handle-capacity 256 --particle-limit 1000`をdevに対して流す
- id付き`chat.post`の成功resultが`null`であることを、live-autoの結果か一回の要求で確かめる
- 返却: PASS行の数、FAILの内容、試験で作ったentity／blockの扱い

## 2. Python — 代表往復

- `b901c88`のwheelで、devへ接続する
- `postToChat`が`None`を返す。`pollEvents`でeventを受け取れる（pokeかchat）。entity、particle、soundを1つずつ
- 同梱WireScope（`minecraft-remote-tooling` `dc1ab83`から作ったもの）を開き、上の操作のframeが表示されることをhuman ownerが
  目で確かめる
- 返却: 操作ごとのPASS／FAIL、WireScopeの表示の観測

## 3. Scratch — 移管したBridgeとWireScope

- 手元の開発端末で、Scratch `7fbbf03`のcandidateと、`minecraft-remote-tooling`のBridge（OCI `sha256:5828304c…b84f`）を動かし、
  devへ接続する。pairing（one-shot）が通ること
- 代表のブロック: チャット、ブロックの設置、entity、particle、sound、カタログID一覧、pickerの検索
- WireScope（`minecraft-remote-tooling`の生成物）を、Scratch担当が独立のChromiumで開き、上の操作のframeが落ちずに表示されることを
  確かめる。時刻列と方向列の幅（b9の列幅の変更）をhuman ownerが目で確かめる
- 返却: ブロックごとのPASS／FAIL、WireScopeのscreenshotの観測（画像はGit外）

## 4. その後

- coordinatorが各segmentの返却を`14-evidence/`のsanitized recordにまとめ、横断の`GREEN`／`HOLD`／`RED`を判定する
- human ownerの公開承認の後、coordinatorが各repoへ公開の指示票を出す。PythonのPyPI.orgへの公開には、その前にhuman ownerが
  GitHub environment `pypi`の保護と、変数`PYPI_PUBLISH_ENABLED`を設定する
