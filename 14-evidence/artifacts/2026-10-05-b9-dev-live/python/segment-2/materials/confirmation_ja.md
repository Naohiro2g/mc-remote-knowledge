# b9 Python 代表往復確認票（2026-10-05）

- 対象 repo: `Naohiro2g/minecraft-remote-api`
- 対象 branch／commit: `codex/b9-python-contracts-pypi@b901c88fe41b67530ff353271683ece9fd453076`
- release／channel: 凍結candidate `2320.0.0b9`、protocol `23.2.0`
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: frozen／live。Python segment 2の実施・記録完了、coordinatorの採用待ち
- contract maturity／required test tier: b9 API freeze、Tier 3。今回の範囲はsegment 2
- knowledge contract path: `00-hub/b9-gate-live-test-sheet_ja.md`（共通、2. Python — 代表往復）、`00-hub/release-gate-notes_ja.md`（b9凍結set）
- knowledge contract commit: `561de98b5c15864ac9b86cb6dcaeef1f20ce635b`（実読。最新remote mainのruntime／INDEX、wireの認証とeventsも参照）
- gate manifest identity: `b9-integrated-artifact-set-1`。knowledgeが示す凍結identityを使用
- change cone: 新規pairing、認証済みhello、chat／event／entity／particle／soundの代表往復、同梱WireScope表示
- reused PASS／rationale: 凍結wheelのCI・fixture結果をartifact identityの根拠として使用。今回のlive結果は別記録
- exact compatibility set／freeze status: 凍結済み。未公開worktreeや一時buildを実行せず、CI wheelを独立venvに導入
- target deployment／profile／lock: 通常dev。既存private profileがユーザー指定SSH aliasと一致することを確認。実addressは収録しない
- authorized next action: human ownerの「進めて」により、新規pairingからsegment 2を再開。Minecraftでのpairing承認はhuman ownerが実施
- test class: `live-auto`＋`live-human`（WireScopeの表示観測）
- 実行したcommand／手順: 下記「実行」。humanの表示確認・チャット送信を待ってから代表往復を実行
- 結果: **segment 2の各操作PASS、同梱WireScopeのhuman表示確認PASS**。runner exit 0、接続close PASS
- evidence record／artifact: `result.json`、`observer_snapshot.json`（22 frames）、`human-wirescope-observation_ja.md`（human提示のframe 1〜22）、`run_segment2.py`、この票。正式record提案は`14-evidence/records/2026-10-05-b9-dev-live_ja.md`、artifact提案は`14-evidence/artifacts/2026-10-05-b9-dev-live/python/segment-2/`。正式配置はknowledge側
- 未検証の境界: 横断gateの最終判定、PyPI公開、JAR本体・Paper／Java版・server logの独立照合、音の聴取・定位、2-player receiver差
- security／compatibility／rollback: token・pairing_id・private address・player UUIDを出力しない。private設定は素材に含めない。debug=False、catalog同期なし。公開source／wheel／同梱app不変
- 判定を求める事項: 操作ごとの結果とhuman表示観測の採用。gate全体の判定はcoordinatorへ委ねる

## Identity

| 対象 | identity |
| --- | --- |
| Python source | `b901c88fe41b67530ff353271683ece9fd453076` |
| wheel | `minecraft_remote_api-2320.0.0b9-py3-none-any.whl` |
| wheel bytes／SHA-256 | 196,221／`e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6` |
| CI run／artifact | `37233244696`／`11314197935` |
| 同梱WireScope source | `dc1ab834183e29f2eb03059b07e99d2b463776ee` |
| WireScope zip bytes／SHA-256 | 83,854／`da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |
| WireScope manifest bytes／SHA-256 | 2,339／`c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7` |
| runner SHA-256 | `50d7c0d46186a2f534ff79ceb6e37578d876ae6e8b646a3789a58a28e9c7fd83` |

wheelと同梱appの本体bytes／SHA-256を再照合した。実行はisolated venvのinstalled packageで行い、source checkoutはimportしていない。
稼働中pluginはhuman ownerがb9へ差し替えたとの報告に基づく。Python側ではJARの本体SHA-256を読み取っていない。

## 実行

```bash
/tmp/mcr-b9-dev-hello-venv/bin/python \
  handoff-materials/2026-10-05-b9-python-live/materials/run_segment2.py
```

runnerはGit外の試験素材。LAN接続、private token保存、同梱WireScopeのブラウザー起動のため承認済みsandbox外で実行。
標準authenticateの期限切れtoken処理とpairing fallbackを使い、承認済みの新tokenを同じdev profile用entryへ保存した。
新規pairing後のhelloで`23.2.0`／`1.21.11`を照合し、本体実行前にhumanのWireScope attachとチャット送信を待つ。

前回の保存tokenによるhelloの`token_expired` FAILは、`../2026-10-05-b9-dev-hello/`の別素材として保持する。
今回は新規pairing後の代表往復であり、再pairingなしのcredential継続PASSの根拠にはしない。
Scratchで成功したとのhuman ownerの報告は受領したが、そのtoken継続の原本evidenceはこのPython票では独立照合していない。

## 操作ごとの結果

| 操作 | 結果 | 根拠／WireScope frame |
| --- | --- | --- |
| 新規pairing後のhello | PASS | protocol `23.2.0`、MC `1.21.11`。1〜2 |
| `postToChat` | PASS | wire result `null`、Python戻り値`None`。3〜4 |
| `pollEvents` | PASS | `chat_posted`で`b9-python-live`を受領。5〜6 |
| entity | PASS | cow生成、pose取得、削除。13〜18 |
| particle | PASS | dust／receiver self／count 8、result 8。19〜20 |
| sound | PASS | harp／volume 0.5／note 18／receiver self、result null。21〜22 |
| WireScope表示 | PASS | human ownerが実表示のframe 1〜22をpayload付きで提示 |
| cleanup／close | PASS | cow削除後に接続とWireScope stationを閉じた。runner exit 0 |

実行時刻: 2026-10-05 08:29:12〜08:43:01 JST。代表往復は08:42:17 JSTに実行。
hello・pairing後から代表往復までの間はhumanのattach／チャット送信を待っていた。
合計11 RPC／22送受信framesをobserver snapshotとhuman表示素材へ保存した（auth RPCは収録対象外）。
eventsの`through_sequence`／`latest_sequence`はともに1、`filtered_out`と累積loss counterはすべて0。
今回のeventは既知の`chat_posted`。unknown eventの実サーバ生成試験は行わず、既存deterministic fixture結果を維持する。

`player.getPos`を基にstream内のdimension／originを設定し、プレイヤーの近くで試した。
block変更やプレイヤー移動は行っていない。cowは削除済み、particleとsoundは一過性。
旧tokenを新tokenへ置き換えてローカル保存したが、token実値は素材へ収録していない。

## 返却・残る境界

Python segment 2の要求範囲は完了。この票と素材の正式evidence収容・採用はknowledge coordinatorへ依頼する。
Scratch側のtoken継続結果の採用、他segment、横断gate全体の判定と公開指示はcoordinatorの担当。
Python source、frozen wheel、同梱WireScopeを変更・再生成していない。main統合・tag・Release・PyPI公開は実施していない。
