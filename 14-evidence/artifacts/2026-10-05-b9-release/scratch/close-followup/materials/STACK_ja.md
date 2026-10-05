# 搬送票：Scratch → Stack（設定契約・WSS検査の回答受領と対応状況確認）

この票の対象資料を読み、既存の対応状況を確認してください。必要な回答・再現素材をStack側へ収容し、受領結果とScratch側の元資料の処理可否を返してください。

- 搬送元 repo: `Naohiro2g/scratch-editor`
- 搬送元 surface: Scratch担当／Codex
- 搬送元 branch/commit: `agent/b9-tooling@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`（公開b9 source）。本票と元のhandoff資料はGit管理外
- 作成日: 2026-10-06
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md` runtime、`00-hub/b9-gate-close-instructions_ja.md`
- knowledge contract commit: `5beaad2557abbc6e90ada03edf7d0a2918fa7a52`（remote mainと一致を確認して実読）
- b9 close分類の起点: `handoff-materials/2026-10-05-b9-close/materials/CLOSE_ja.md`（実読knowledge `099c40b0c312694712653885200f3114ea4bed33`）
- 宛先: Stack担当（ホーム用設定生成／WSS接続検査）
- 種別: その他（既存問い合わせへの回答の受領確認と素材の引継ぎ）
- 決定／依頼: b8から②として保持している回答2件について、Stack側で対応済みかを確認し、結論と必要な素材の保管先を確定する
- 理由: Scratch側に回答・再現素材はあるが、受領と対応完了の戻りを確認できていない。今回の票で未対応と断定しない
- 却下案: なし
- 影響: 回答2 directoryの保持・終了条件を確定する。実装変更が必要と分かった場合は残作業として返す

## 対象資料

以下はScratch repoルートからの相対path。別repoのagentは、利用中の作業環境にある`scratch-editor`を起点に読む。

| 対象 | 入口 | 付属資料 |
| --- | --- | --- |
| ホーム用設定の契約差異 | `handoff-materials/2026-10-02-home-scratch-contract-reply/materials/reply_ja.md` | 親directoryの`MANIFEST_ja.md` |
| WSS 401の検査要求 | `handoff-materials/2026-10-02-stack-wss-reply/materials/reply_ja.md` | 同directoryの`probe-subprotocol.mjs`、`probe-result.json`、親directoryの`MANIFEST_ja.md` |

元6 fileのbytes／SHA-256は本票と同directoryの`stack-source-inventory.json`。引取り時にこの一覧と照合する。対象を読めない場合は参照不能として返し、受領済みとはしない。

## 確認してほしいこと

1. 設定生成: 元回答の契約は`schema_version: 1`必須、`release_identity`は設定JSONの未知fieldとして拒否。Stackの設定生成が正式schemaへ追従済みかを、現在のStack側のsource・検査結果で確認する。元問い合わせはStack `main@68832e0a95c0462462e9a10115bfae272ec1a6d7`起点
2. WSS検査: 元回答では、正しいOriginに加えて`mcremote.bridge.one-shot.v1`をWebSocket subprotocolとしてofferする必要がある。Scratchと同じofferは`mcremote.bridge.probe.v1, mcremote.bridge.one-shot.v1`。成功確認はHTTP 101とresponseのone-shot選択。Stackの直接Bridge／WSS検査がこの条件へ追従済みかを確認する。元問い合わせはStack `agent/home-runtime-permissions@19c8afa68a3133addf82f308ab642d8ca4e51e15`起点
3. 対応済みなら、commit／test／既存の記録を返す。実環境の101まで確認したか、検査sourceだけ対応したかを区別する。新たな稼働環境の接続・設定変更・deployはこの受領確認には含めない
4. 回答と再現素材の必要分をStack側のhandoff／記録へコピーして保管先を示す。恒久的に残す結論はStack側の記録へ、横断事項はknowledgeへ搬送する。既に同じ全文がある場合は重複収容せず、一致した参照先を返す

元回答のScratch側未対応事項: 不正runtime設定と意図的な接続無効を、当時のUIが同じ案内として扱っていた。これは当時のScratch側の観測であり、Stackに修正を割り当てるものではない。今回、現行Scratchの挙動を再検証していない。

## 返却物

- 受領した資料の一覧と、収容先path・参照commit（未commitならその旨）・bytes／SHA-256
- 設定生成とWSS検査それぞれの状態: 対応済み／残作業あり／確認できない。根拠となるsource・test・記録
- Scratch側の元2 directoryごとに、削除可／保持が必要、その理由と終了条件
- 回答をknowledgeへ着地させた場合は正式pathとpush済みknowledge SHA

## 根拠・処理条件

- 根拠/検証: 元回答とprobe結果を読んだ。元回答には設定23 testとschema拒否確認、Bridgeの選択testと4 caseのローカルprobe PASSが記載されている。今回の作業は搬送票作成と元6 fileのhash採取のみで、既存testを再実行していない
- 既に変更した実装/文書: 本搬送票と元資料inventory、ローカルNOTES。製品source、Stack repo、稼働環境の変更なし
- ナレッジ着地希望: 受領と処理可否をb9 closeの②追跡へ反映。新しい仕様決定が必要になった場合は別の搬送として扱う
- 捕捉 cleanup: Scratchの元2 directoryは、必要な全文の受領・照合と終了条件の確認後にScratch担当が処理する。Stack担当は元を移動・削除しない
- 着地後の確認戻り先: human owner経由でこのScratch担当sessionへ返す。本票作成時点では外部送信・Stack側の受領は未実施
