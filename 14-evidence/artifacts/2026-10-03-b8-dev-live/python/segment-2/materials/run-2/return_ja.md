## 確定搬送票 — Python segment 2 残り専用run 2の準備停止

- 搬送元 repo: `Naohiro2g/minecraft-remote-api`
- 搬送元 surface: Python担当session（Codex）
- 搬送元 branch/commit: `codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470`
- 作成日: 2026-10-03
- 種別: その他（接続準備の停止報告）
- 決定: run 2はFAILとして停止。本体の残り操作は未実施。保存tokenによる認証済みhelloはPASS、WireScope attachのhuman checkpointは未成立。human ownerが「時間切れ」と回答したため、確認待ちを中止してstation／Minecraft connectionを終了した。
- 理由: WireScope attach codeは120秒有効。今回のrunnerには待機中の再発行入力がなく、human readinessを確認できなかった。具体的なHTTP error payloadは採取していないので、serverやWireScopeの製品不具合とは判定しない。
- 却下案: checkpointを未確認のままworld操作を開始する案。
- 影響: frozen identityは不変。world操作0回、仮blockなし、pairingなし、保存token変更なし。run 1の再利用PASSには変更なし。
- 根拠/検証: test class=`live-auto with live-human WireScope observation`。knowledge contract path=`00-hub/release-gate-notes_ja.md`（2026-09-30節）、`00-hub/b8-gate-live-test-sheet_ja.md`（共通／2. Python）、`15-wirescope/wirescope-station-attach-design_ja.md`（§8）。knowledge contract commit=`396326def73d99aae91dca4de9416f4eca6d2aea`。下記sanitized素材を保存。正式evidence record／artifactはknowledge担当によるauthoring待ち。
- 既に変更した実装/文書: packageのtracked変更なし。次回用Git外runnerを`../run-3/python_remaining.py`へ準備し、凍結CI wheel環境でoffline loadをPASS。開始前のhuman readiness入力、製品既存のbounded reissue操作、実attach成立確認を追加。本体の残り試験内容はrun 2と同じ。run 3は未起動・未実施。
- ナレッジ着地希望: run 2準備停止と未実施範囲をgateへ記録。継続時も同じ凍結identityを使用し、run 1のPASS再利用範囲を維持する。横断GREENはPython側で出さない。
- 捕捉 cleanup: session73255終了、WireScope station／connectionは正常close。素材を上書きせずrun 2へ保持。token／private endpoint／player UUID／pairing_id／表示用attach codeは搬送素材へ含めない。
- 着地後の確認戻り先: Python担当session。

| 項目 | 結果 |
| --- | --- |
| exact set | `b8-integrated-artifact-set-1`（不変） |
| wheel | 195,068 bytes、SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180` |
| 同梱WireScope source | `df34849d2502a498a06c5fe07a91d03e925124eb`（不変） |
| 認証済みhello | PASS。protocol `23.2.0`／MC `1.21.11`、再pairなし |
| WireScope表示のhuman観測 | 未成立。owner回答「時間切れ」 |
| getBlock取得／復元・playBlockSound 5kind・3D graph | 未実施。world操作0回 |
| runnerの停止reason | `human checkpoint not confirmed`。hello成功後の入力中止によりrunnerが生成したreasonで、serverのRPC errorではない |

### 保存素材

| 素材 | SHA-256 |
| --- | --- |
| `python_remaining.py`（実際に使ったrunner） | `46b4b61f85eef5679114223755eea9ad4ac8f3fb5de2aca2ed0258348da90271` |
| `frames.jsonl`（hello送受信の2 frames） | `12a224e9c87fc0d5d0c0630549c2a12329a56da92dcd472011c4b531c4166794` |
| `summary.json` | `b61cb618110a9aa9e0896e5c0309f493f26e7f9dc325e5d6b4722a24d7d0c825` |
| `../run-3/python_remaining.py`（準備済み・未実施） | `c001bd5cbc8ab8b5151133c995dec4f226d82f4b9ac83f786a2e9797574a5c7c` |

SoundGroup数値の直接観測、2-player receiver差、描画、音の聴取・定位はこの票で主張しない。
