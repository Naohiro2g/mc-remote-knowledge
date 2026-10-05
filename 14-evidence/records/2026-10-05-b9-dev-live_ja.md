# b9 devの通常環境での横断試験（2026-10-05）

> test class: `live-auto` + `live-human`。b9横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-04の節）の統一実施票
> （`00-hub/b9-gate-live-test-sheet_ja.md`）による。各担当の返却票（Git外の搬送素材）をcoordinatorが要約した。token、pairing_id、
> private address、player UUIDは収録しない。b9はAPIを変えないので、b8のlive PASS（`2026-10-03-b8-dev-live`）を再利用し、
> 変わったところだけを確かめた。

## 素材

`14-evidence/artifacts/2026-10-05-b9-dev-live/`（一覧と収容しなかったfileは`INVENTORY_ja.md`）。McRemoteのsegment 0（JARの差し替え）と
segment 1（live-autoの全文log、RPC transcript、清掃の集計、初回の失効した試行）、Pythonのsegment 2（結果、observerの22 frames、
human ownerのWireScope観測）と保存tokenの確認、Scratchのsegment 3（代表ブロックの結果、独立Chromiumの照合、列幅のhuman確認）を収容した。

## 使ったidentity

- exact set: `b9-integrated-artifact-set-1`（protocol `23.2.0`／artifact `2320.0.0b9`）
- McRemote `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`、JAR 261,016 bytes／`4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e`
- Python `b901c88fe41b67530ff353271683ece9fd453076`、wheel 196,221 bytes／`e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6`、
  同梱WireScopeのsource `minecraft-remote-tooling@dc1ab83`（ZIP `da3da0b6…31ad`）
- Scratch `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`（GUI tar `c0d08c26…c75d`）
- minecraft-remote-tooling `dc1ab834183e29f2eb03059b07e99d2b463776ee`（WireScope ZIP `da3da0b6…31ad`、Bridge OCI
  `sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`）
- devの通常環境: host-native、Minecraft `1.21.11`、Paper `1.21.11-132-ver/1.21.11@c5eb079`、Java `21.0.12.1`、認証ON、credential `HEALTHY`

## 結果

| segment | 結果 | 要点 |
| --- | --- | --- |
| 0 環境の準備と実tokenの継続 | PASS | b8のJAR（`7ab24fa1…77fb`）を退避し、b9のJARへ一件だけ差し替えた。config、起動script、Paper、Javaは不変。b8のScratchとb9のScratchの両方から、保存tokenのまま再pairingなしで`hello`が通った（human ownerの報告と、b9 Scratchのhelloの表示） |
| 1 McRemote live-auto | PASS | PASS行60、FAIL行0、終了コード0。認証済みの4つの`hello`で`23.2.0`／`1.21.11`を照合。id付き`chat.post`の応答が`{"result":null}`。試験で作ったentity 258体を削除し、変えたblock 9箇所を元のBlockValueへ戻して読み直しで一致 |
| 2 Python 代表往復 | PASS | 新しくpairingした後、`postToChat`がwireで`null`、Pythonで`None`。`pollEvents`で`chat_posted`を受けた。entity（cowの生成、pose、削除）、particle（dust、`self`）、sound（harp、`note` 18、`self`）。同梱WireScopeで22 framesの表示をhuman ownerが確認 |
| 3 Scratch 移管したBridgeとWireScope | PASS | 移管したBridgeでone-shotのpairingが通った。チャット（`null`）、ブロックの設置と読み直しと復元、entity、particle、sound（`N12`→`note`）、カタログID一覧（block 1166件）、pickerの検索（`gold`、`金ブロック`、`Block of Gold`、`door`）と適用。独立ChromiumのWireScopeで22 framesを全件照合。時刻列と方向列の幅をhuman ownerが画像で確認した |

## 観測と注意

- **Pythonの保存token:** Pythonがb8のときに保存したtokenは`token_expired`で、Pythonは新しくpairingしてからsegment 2を行った（素材
  `python/saved-token-check/`）。実tokenの継続は、segment 0のScratchの観測を根拠にする
- **Bridgeの実行形:** 手元の端末にDocker daemonが無いため、Scratch担当は凍結したBridge OCIの中のcode（linux/amd64の`/app`）を
  取り出し、host-nativeのNode `24.19.0`で動かした。Bridgeのcodeとtransportは確かめたが、OCIのcontainerとしての起動
  （entrypoint、image内のNode）は確かめていない
- **試験の補助の失敗:** McRemoteの初回はpairingが承認の前に失効して止まった（認証の前提が未成立で、worldは変えていない）。
  Scratchの自動試験の補助scriptで3件の失敗があり、補助だけを直した。どちらも凍結した製品のFAILではない
- **知らないevent type:** 実サーバーから出せないので、live試験では確かめていない。shared fixture `chat-event-compat-v23.2.json`の
  deterministic testに任せた

## 主張しない範囲

Bridge OCIのcontainerとしての起動、b9でのMinecraft画面上の描画と音の聴取、2-playerのreceiverの差（b8のPASSを再利用）、
PyPI.orgへの公開、公開deployment、実機でのrollback。
