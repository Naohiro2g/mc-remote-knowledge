# b8 McRemote live-auto 返却票

McRemote segmentは **PASS行60、FAIL行0、exit code 0** で完走した。認証ONのまま試験用に一度pairingし、3つの認証済みconnection epochでprotocol `23.2.0`／Minecraft `1.21.11`を照合した。横断gateの最終判定はcoordinatorへ返す。

## Release gate 確認票（McRemote live-auto追記）

- 対象 repo: `Naohiro2g/McRemote`
- 対象 branch/commit: `feat/b8-entity-lifecycle-particle@17309919f6340b07abbbe16476ad1d4f762518c0`
- release / channel: `2320.0.0b8` candidate / prerelease準備
- gate coordinator: knowledge担当session
- human release owner: プロジェクトowner（本会話のユーザー）
- current phase: McRemote live-auto完了、segment結果の返却
- contract maturity / required test tier: 凍結contract、Tier 3の変更範囲内live-auto
- knowledge contract path: `00-hub/b8-gate-live-test-sheet_ja.md`「共通」「1. McRemote — live-auto」／`00-hub/release-gate-notes_ja.md`のb8凍結節
- knowledge contract commit: `749ba60dc8c18938e50ce66b8e820aac4401c69e`
- gate manifest identity: 未成立（上記SSOTの記載）。凍結setのidentityを使用
- change cone: 指定live-autoの範囲。b8 entity lifecycle、Particle Stage 2、sound、無印resource IDと既存build／FIFO／event／capacity検査
- reused PASS / rationale: 既存unit 273件PASS、fresh install認証ON、旧b7での無印ID拒否は前担当の記録。今回これらを再実行せず、凍結source／JARに対する指定live-autoを新規実施
- exact compatibility set / freeze status: `b8-integrated-artifact-set-1`／凍結。McRemote JAR `mc-remote-1.21.11-2320.0.0b8.jar`、261,025 bytes、SHA-256 `7ab24fa1ff6c20513e46cbf3629f1f4860365acbf3a7e191e48a4e75af1677fb`
- target deployment / profile / lock: human owner指定のdev通常環境、ホームサーバーのhost-native Paper。private接続先は票に記載しない。ロック変更なし
- authorized next action: 本票・素材をcoordinatorへ返却。後続segmentと公開操作はcoordinatorの進行による
- test class: `live-auto`（試験token取得のpairingのみhuman ownerがMinecraft内で承認）
- 実行した command / 手順: 下記の秘匿化済みcommand。JAR差し替え完了連絡、dev接続先、pairing承認を受領した後、SSHの読み取りでJAR／起動identityを照合して実行。実施時刻は2026-10-03 04:22:13〜04:23:09 JST
- 結果: **PASS行60、FAIL行0、exit code 0**。最初の認証済みhelloでprotocol／MC版一致。全3認証済みhelloは同じ値。helloのpermission snapshotは`online=true, offline=true, buildRange=1000`
- evidence record / artifact: 以下の搬送素材。knowledgeの正式record／artifactへの着地は未実施。提案先は`14-evidence/records/2026-10-03-b8-mcremote-live-auto_ja.md`、`14-evidence/artifacts/2026-10-03-b8-mcremote-live-auto/`
- 未検証の境界: b7→b8で保存済み実tokenが続くこと（本試験は新規試験token）。2-player receiver、dust／blockの目視、音の聴取・定位、Python／Scratch／WireScope segment。capacity試験entityの現在の生存数と試験blockの原状復元は未確認・未実施
- security / compatibility / rollback の確認: `Auth enforcement: true`、`Credential domain health: HEALTHY (healthy)`を起動logで確認。token無しhelloは`auth_required`、protocol 21 helloは`protocol_mismatch`。設定・credential backend・JAR・公開sourceを変更せず、tokenをメモリ内だけで使用。要求／応答とlogのtoken／pairing_id／player UUID／private host秘匿化を検査済み。rollbackは本segmentで実施しない
- 判定を求める事項: McRemote segment結果の受理と正式evidenceへの収容。横断GREEN／公開可否は主張しない

```bash
python3 -u handoff-materials/2026-10-03-b8-mcremote-live-auto/materials/run_with_transcript.py \
  --host <human-owner指定dev-host> --port <human-owner指定dev-port> \
  --expect-mc 1.21.11 --protocol 23.2.0 \
  --handle-capacity 256 --particle-limit 1000 --interactive-pair
```

## 観測

- dev JARは凍結identityとbyte数／SHA-256が一致。
- Minecraft `1.21.11`、Paper `1.21.11-132-ver/1.21.11@c5eb079`、Java `21.0.12.1+1-1-24.04.4-Ubuntu`。
- strict BlockSpec／BlockValue、旧method拒否、DimensionRef／DimensionKey、FIFO／flushと1041 notification burst、events.poll、particle validation／work／chunk、entity capacity／epoch independence、b8 lifecycle、typed particle、sound、無印ID、認証済みparticle self receiverがPASS。全PASS行は`live-auto.log`に保存。
- 前担当の無認証live-autoはPASS行61。本試験は認証済みなので、selfの無認証拒否2行に代わってparticle self受理1行を通る。現runnerの分岐による行数差である。
- SSHで以前のサーバーdirectoryを参照した最初の読み取りはdirectory欠落で終了。Java process cwdから現directoryを確認して再読した。製品試験開始前の場所確認であり、live-autoの再試験や製品修正ではない。

## 試験で生成したentity／blockの扱い

- `world.spawnEntity`成功258回。容量試験のcow257体（primary256＋secondary1）は自動削除されない。生成時はoverworldの`y=72, z=0.5`、primaryの`x=0.5〜255.5`、secondaryの`x=30.5`。現在の生存数・位置は未再観測。connectionを閉じてもentityは削除されない。
- lifecycle試験用cow1体は`entity.remove`成功を確認。直後の`entity.getPose`は`entity_not_found`。
- 変更した試験blockは原状復元しない。origin `[0,0,0]`／overworld／`y=72`。以下は成功要求と読み取りに基づく試験時の最終値であり、試験後の再観測ではない。

| 座標 | 試験時の最終block |
| --- | --- |
| `[0,72,0]` | `gold_block` |
| `[1,72,0]` | `oak_log`（axis=z） |
| `[2,72,0]` | `oak_stairs`（facing=east、half=top、waterlogged=true） |
| `[3,72,0]`、`[4,72,0]` | `oak_stairs`（facing=north） |
| `[3,72,1]` | `oak_log`（axis=x） |
| `[4,72,1]` | `gold_block` |
| `[7,72,0]` | `lapis_block`（notification burst最終値） |
| `[8,72,0]` | `emerald_block`（work-limit notification後も保持） |

既存entityや元のblock状態を識別できないため、一括killや推測による復元は実施していない。

## 搬送素材identity

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `environment.log` | 644 | `df68ce7c48b2021082498275b24352baa1cb6616081070b33c4ed21c28b9562d` |
| `live-auto.log` | 3,149 | `030dd9775c6ddd6f9134e107ebf431591e1ad1dd093174527144f7a70ff449cf` |
| `rpc-transcript.jsonl` | 345,510 | `afb4900620eb9bbd1ae9de921d7c48a47dce4935e699513871c55073040b814a` |
| `run_with_transcript.py` | 5,692 | `c264aa11c590aad47f072d0742485d874781b2679437ddc715db50fcdf6a0823` |

凍結runner `scripts/live_auto.py`のSHA-256は`7a093d27ac349023e7be90c48597ead1a1207772a4fee084933ee2f8c794352f`。ラッパーはそのdigestを開始前に検査し、runnerのRPC送受信を記録する。candidateのscriptは変更していない。
