# Stack返却票の受領確認（Scratch）

> 最新状態: 受領先との再照合後、元2 directory／6 fileを処理済み。対応表はstack-received-inventory.json、実施結果とknowledgeへの追跡更新依頼はKNOWLEDGE_UPDATE_ja.md。以下はcleanup前の受領確認時点の記録。

- 作成日: 2026-10-06
- Scratch source: `agent/b9-tooling@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md` runtime、`00-hub/b9-gate-close-instructions_ja.md`
- knowledge contract commit: `5beaad2557abbc6e90ada03edf7d0a2918fa7a52`。今回remote mainが同一であることを確認し、同SHAで既読のruntime／close指示を参照
- 元搬送票: 同directoryの`STACK_ja.md`
- 返却元: Stack `handoff-materials/2026-10-06-stack-backstage-handoff/materials/RECEIPT_ja.md`
- Stackの報告source: `agent/home-luckperms@a30aa8b1b230e88ed92c515b357a088d97ddb0da`
- 返却票identity: 9,247 bytes／SHA-256 `ed5dbd56488b259e86f8040d2500bd10f8d1173da2502ac9a682d82282954483`。同directoryの`STACK_RECEIPT_ja.md`へbyte同一コピー
- 受領inventory: 同directoryの`stack-received-inventory.json`へ元をbyte同一コピー。原票内の相対リンクはStack側の元票を基点に読む

## 受領・独立照合

回答2 directoryの全6 file／13,894 bytesについて、Scratchの元、搬送時のinventory、Stackの受領inventory、Stackの収容先にある実体を照合し、全文byte一致・bytes／SHA-256一致を確認した。5 fileは新しいコピー先、WSS回答本文1 fileはStackの既存全文を再利用しており、その実体も一致した。

- 監査script: `verify-stack-receipt.py`
- 結果: `stack-receipt-verification.json`、passed=true
- 元素材を移動・削除していない。Stackの製品source・test・稼働環境を本担当が再検証したものではない

## Stackから受領した対応状況

- 設定生成: 正式Scratch schemaを使う通常ホーム経路`home-alpha-full@2`〜`@4`は対応済み。schema_version必須、release_identityを入れない生成・render／doctor検査があるとの報告。PR #61は10/2統合済み、今回対象suite60件と全体391件がPASSと報告された。旧`home-server@6`／`compose@14`自体を修正したという主張はない
- WSS検査: 10/2に回答を受領し、直接Bridge／外側WSSのofferを修正済み。401から101・one-shot選択へ変わった実環境の既存記録を保持しているとの報告。今回は再接続していない
- doctorへのWSS upgrade検査の組込みは未実装だが、元回答で求めた直接Bridge／外側WSS検査の対応完了とは区別する
- Scratchの設定異常専用UIは、元票に記した当時のScratch側の課題。今回の受領確認で現行UIを再検証していない
- StackのPR #62／#63は返却票作成時点で未マージと記載されている。これら別作業の統合は本受領確認の対象外

## Scratch側の元資料と②追跡

| 元directory | 更新した状態 | 処理条件 |
| --- | --- | --- |
| `2026-10-02-home-scratch-contract-reply` | 受領・全文照合と対応完了報告を確認。Stackへの引継ぎ待ちは完了 | 受領をScratchの追跡へ反映済み。別の正本／evidenceからの参照の更新・引継ぎを確認後、元を処理できる |
| `2026-10-02-stack-wss-reply` | 受領・全文照合と対応完了報告を確認。Stackへの引継ぎ待ちは完了 | 同上。全4 fileの収容または既存全文参照を確認済み |

この2 directoryを②の受領待ちとして追跡する必要は無くなった。以後は収容先をStack側の上記受領inventoryで参照し、元は参照整理後の③候補として扱う。今回、元の削除と他の正本／knowledgeの参照更新は行っていない。10/5のclose分類票は当時のsnapshotとして保持し、本票を更新差分とする。

## 次の追跡

- knowledge担当へ、Stack受領・対応完了、元処理条件をb9 close②追跡へ反映してもらう。knowledge正式着地は今回未実施
- 本packetにはStackとbackstage両方の返却・受領確認が揃った。引継ぎ先の受領待ちは解消し、Scratchの元参照確認・cleanupとknowledge追跡反映を残す
- backstage関連の起動・戻し先・使用中logとruntimeには、`BACKSTAGE_ACK_ja.md`の保持条件を継続適用する

- 今回の変更: Stack返却票・inventoryのコピー、実体照合script／結果、本受領確認、packet MANIFEST／inventory、ローカルNOTES
- 未実施: 元の移動・削除、稼働環境操作、製品修正、test再実行、他repo変更、knowledge正式authoring
