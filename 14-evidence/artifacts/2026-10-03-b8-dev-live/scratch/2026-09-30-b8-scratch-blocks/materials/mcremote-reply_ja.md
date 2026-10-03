# 回答票（Scratch → McRemote）

- 作成日: 2026-09-30
- 対象: McRemote `feat/b8-entity-lifecycle-particle@a4d7ab0`、PR #12からの問い合わせ票
- 問い合わせのknowledge ref: `aac1167202ea5ccbf1eb41975d10fa678ddc0419`（GitHub APIで存在を確認）
- 今回読んだknowledge ref: `974ba19f396336c2c52d657ef1c14a2f0d04c793`
- contract: `10-protocol/wire-format-design_ja.md` §5.8.3、DECISIONS `2026-09-23-01`／`2026-09-30-01`

## 1. reasonとconfigキー

`receiver:"self"`の束縛playerがofflineのときの`player_offline`（-32000）は、Scratch側との互換上問題ありません。protocol mirrorに`ErrorReason.playerOffline`があり、ScratchのErrorTextも同reasonを保持します。既存のB8 fixtureにはoffline専用caseはなく、別reasonを要求していません。未認証の`auth_required`とは区別し、particle ID／dataを先に検証する確定順序を維持してください。この回答はoffline reasonの横断SSOTを新規確定するものではありません。

plugin内部キーの`entities.nearby_max_radius`／`entities.nearby_max_entities`も問題ありません。Scratch fixtureの`nearby.distribution_policy`は`max_radius:64`／`max_entities:64`／`may_lower:true`／`may_raise:false`です。これはfixture内の抽象policy名であり、plugin設定キーの要求ではありません。WireScopeはwireのprotocol上限（radius 0〜64、max_entities整数1〜64）を検証し、plugin固有の引き下げ値や設定キーは検証しません。引き下げpolicyによる拒否はサーバーの`invalid_params`として観測します。

## 2. ownerと配布済みfixture

ownerはScratchの`@mc-remote/protocol`で、現行owner境界を継続します。entity lifecycleとparticle Stage 2を一つにまとめたfixtureを2026-09-30に作成・push済みです。予定ではなく、現時点でconsumerテストに利用できます。

- repository: `Naohiro2g/scratch-editor`
- path: `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`
- schema: `mcremote.entity-particle.v23.2`
- protocol: `23.2.0`
- branch: `agent/b8-owner-fixture`
- commit: `0735a9c957d069f719bee9c91e8be0f9322f4920`
- SHA-256: `09c1565bf81d33c92d6282e6e20d926559168cb9d780c07d30ad2f9f5895640e`
- fixture内knowledge contract ref: `b853078bb0af1bc5cacb4b4ce08ffe7227190f60`
- 同bytesを含む互換実装branch: `agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`
- remote確認: 両branchのGitHub API返却SHAを上記commitと照合済み。default branch統合は未実施。

[固定commitのfixture](https://github.com/Naohiro2g/scratch-editor/blob/0735a9c957d069f719bee9c91e8be0f9322f4920/mc-remote/protocol/test/fixtures/entity-particle-v23.2.json)を取得し、bytesのhashを照合してください。

| 配列 | 件数 | case ID |
| --- | --- | --- |
| `nearby.cases` | 19 | `B8-N01`〜`B8-N19` |
| `nearby.handle_transaction_cases` | 7 | `B8-H01`〜`B8-H07` |
| `entity_lifecycle.cases` | 7 | `B8-E01`〜`B8-E07` |
| `particle_stage_2.cases` | 26 | `B8-P01`〜`B8-P26` |

計59件です。各caseは`id`／`name`を持ち、内容に応じて`params`／`result`／`reason`、候補集合・policy・状態遷移・検証順のassertionを持ちます。全caseがrequest／responseの同一shapeではありません。`methods`と各sectionの`params_order`／field一覧も参照してください。近傍検索・transaction・複合errorはconsumerのproduction pathへcaseごとに対応付ける必要があります。

## 検証範囲

fixture発行時はprotocol test 34/34、build PASS。互換実装commitではprotocol test 35/35、WireScope test 137/137、Scratch拡張対象test 112/112、対象lint／build PASS（引き継ぎノートの実行記録）。今回、fixture hashとremote branch identityを再照合しました。

McRemoteのconsumer適合、JAR build、実Paper挙動、live試験、b8 release GREENはこの回答から主張しません。offline専用caseが必要な場合は、理由のSSOT確定とfixture改訂を別途扱います。
