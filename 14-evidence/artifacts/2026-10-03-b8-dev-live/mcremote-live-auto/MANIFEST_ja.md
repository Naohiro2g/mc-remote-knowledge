# b8 McRemote live-auto 搬送素材

- 搬送元: McRemote / Codex
- 作成日: 2026-10-03
- knowledge contract path: `00-hub/b8-gate-live-test-sheet_ja.md` 共通・1. McRemote
- knowledge contract commit: `749ba60dc8c18938e50ce66b8e820aac4401c69e`
- exact set: `b8-integrated-artifact-set-1`
- source: `feat/b8-entity-lifecycle-particle@17309919f6340b07abbbe16476ad1d4f762518c0`
- JAR: `mc-remote-1.21.11-2320.0.0b8.jar` / 261,025 bytes
- JAR SHA-256: `7ab24fa1ff6c20513e46cbf3629f1f4860365acbf3a7e191e48a4e75af1677fb`
- runner: `scripts/live_auto.py`
- runner SHA-256: `7a093d27ac349023e7be90c48597ead1a1207772a4fee084933ee2f8c794352f`
- 状態: JAR差し替え完了・接続先・試験用pairing承認を受領。devのJAR／起動identityを読み取り照合後、認証ONのlive-autoを実施。**PASS行60／FAIL行0／exit code 0で完走**。coordinatorへの返却素材まで作成し、正式evidenceへの収容を待つ。
- dev identity: Minecraft 1.21.11、Paper `1.21.11-132-ver/1.21.11@c5eb079`、Java `21.0.12.1+1-1-24.04.4-Ubuntu`。
- dev JAR照合: 261,025 bytes／SHA-256 `7ab24fa1ff6c20513e46cbf3629f1f4860365acbf3a7e191e48a4e75af1677fb`、凍結identityと一致。
- 認証状態: 起動logで`Auth enforcement: true`／`Credential domain health: HEALTHY (healthy)`を確認。試験担当は設定を変更しない。
- 実行ラッパーSHA-256: `c264aa11c590aad47f072d0742485d874781b2679437ddc715db50fcdf6a0823`。

## 素材

- `materials/run_with_transcript.py`: frozen runnerをそのまま呼び出し、RPC要求／応答と出力を秘匿化して保存する実行ラッパー。
- `materials/rpc-transcript.jsonl`: 実行時に作成。token、pairing_id、player UUID、接続先hostを省いた要求／応答記録。
- `materials/live-auto.log`: 実行時に作成。秘匿化したPASS／FAIL出力。pair codeは保持する。
- `materials/environment.log`: private hostを含めない、dev JAR digestと起動時のMC／Paper／Java／認証healthの観測。
- `materials/RESULT_ja.md`: 確認票、PASS集計、生成entity／blockの扱い、未検証の境界、素材digest。

公開candidateのscriptは変更しない。ラッパーのdigestは実施時の返却に含める。
このdirectoryは正式evidenceではない。knowledge側へ搬送した後、正式record／artifactへの昇格先を照合する。

## b8 gate closeでの分類（2026-10-03）

**① knowledgeの正式evidenceへ移す**。knowledge `2a8c3eae4e489e67f044111b0d1e6cdd22ead86a`でb8 gate CLOSEDと既存record `14-evidence/records/2026-10-03-b8-dev-live_ja.md`を確認した。recordにはsegment 1の60 PASSが要約されているが、同commitのtreeにはb8のartifact directoryがなく、全文transcriptの移管は未完了。

- 移管先案: `14-evidence/artifacts/2026-10-03-b8-dev-live/mcremote-live-auto/`。このdirectoryのMANIFESTと`materials/`の全ファイルを対応付け、既存recordから参照する。
- 移管担当: knowledge coordinator。正式record／artifact／INDEX／redactionsのauthoring・収容はknowledge側が行う。
- 理由: release gateで実機PASSの根拠にした認証済みRPC transcript、PASS log、環境観測、生成entity／blockの扱いを全文保全する。要約だけからは同じ観測を再構成できない。
- 参照identity: 試験source `17309919f6340b07abbbe16476ad1d4f762518c0`／試験JAR `7ab24fa1…`／公開JAR `fdffaf0c…`、exact set `b8-integrated-artifact-set-1`。PASS再利用はknowledgeのrelease authorizationで受理済み。
- 保持: coordinatorがknowledgeへの全文移管を確認するまでローカル素材を消さない。現時点では未削除。
