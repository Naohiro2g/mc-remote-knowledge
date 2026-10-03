# b8 devの通常環境での横断試験（2026-10-03）

> test class: `live-auto` + `live-human`。b8横断release gate（`00-hub/release-gate-notes_ja.md`の2026-09-30の節）の統一実施票
> （`00-hub/b8-gate-live-test-sheet_ja.md`）による。各担当の返却票（Git外の搬送素材）をcoordinatorが要約した。token、pairing_id、
> private address、player UUIDは収録しない。

## 使ったidentity

- exact set: `b8-integrated-artifact-set-1`（protocol `23.2.0`／artifact `2320.0.0b8`）
- McRemote `17309919f6340b07abbbe16476ad1d4f762518c0`、JAR 261,025 bytes／`7ab24fa1ff6c20513e46cbf3629f1f4860365acbf3a7e191e48a4e75af1677fb`
- Python `52d35f5304e62f465c1f47ab47c00fe9bcf62470`、wheel `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`、
  同梱WireScopeのsource `df34849`（ZIP `4cb34989…0a07`）
- Scratch `691576f60b7f0824e1753bd6823901d01fbe2422`（GUI tar `c7318efd…4843`、WireScope ZIP `4cb34989…0a07`）
- 共有fixture `scratch-editor@054a3af`の`entity-particle-v23.2.json`、36,481 bytes／`ca636b4a…39f2`／111 case
- devの通常環境: host-native、Minecraft `1.21.11`、Paper `1.21.11-132`、Java `21.0.12.1+1`、認証ON、credential `HEALTHY`

## 結果

| segment | 結果 | 要点 |
| --- | --- | --- |
| 0 環境の準備と実tokenの継続 | PASS | JARを一件だけ差し替え。b7で新しくpairingしたPythonのtokenが、b8へ差し替えた後も再pairingなしで`hello`に通った |
| 1 McRemote live-auto | PASS | PASS行60、FAIL行0。認証ONのまま、3つの認証済みepochで`23.2.0`／`1.21.11`を照合 |
| 2 Python 代表往復 | PASS | entity lifecycle、ParticleSpec、`playSound`、`getBlock`と復元、`playBlockSound`の5 kind、3D graph 81往復、無印のID、短いimport。WireScopeの表示をhuman ownerが確認。途中の停止はGit外のrunnerの誤りで、製品は不変 |
| 3 Scratch 学習面とreal-browser WireScope | PASS（1項目NOTRUN） | 各ブロック、カタログID一覧、pickerの日英名と既定値の省略、BlockInfoText。WireScopeの表示をScratch担当のChromiumとhuman ownerの目視で確認。b7是正のbackpressure案内はNOTRUN |
| 4 live-human（2 player） | PASS（既知の制限1件） | receiverの`self`／`world`（particle、サウンド）、dustの色、block particle、音の定位・減衰・`note`の音階・`playBlockSound`の5 kind、3D graphの描画。Java版とiPad（Bedrock、Geyser経由）で確認。iPadではdustの大きさが変わらない |

## non-claim

- server backpressureの案内の実機表示（通常の操作でbackpressureが起きなかった）
- Bedrock（Geyser経由）でのdustの大きさ（Java版では変わる）。導入済みGeyserの版との照合と原因の確定はしていない
- 正確な可聴距離、減衰曲線、音の高さの測定、全resource IDの描画と聴取
- capacity、soak、rollback（rc1）、Windows（公開後にhuman ownerが行う）、Paper 26.x
- 試験で作ったcow 257体と試験blockは、devのworldのoriginの近く（y=72）に残した

## 観測（後続へ）

- 3D graphは動くが、効果的なデモにするには工夫が要る（human owner）
- 連続した`playSound`では和音が揃わない。シーケンス演奏（初回stable後）への関心
- `self`の表示を「自分だけ」と分かる形にする案、座標指定とblock指定で音源位置が違うことを比べる教材案
