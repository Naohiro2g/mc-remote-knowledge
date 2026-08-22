# b5 protocol 22 exact compatibility set 横断release gate evidence

## Record

- test ID: `2026-08-22-b5-dimension-key-live`
- test class: `unit/deterministic` + `live-auto` + `live-human`
- observed date: `2026-08-22`〜`2026-08-23` JST
- result: **PASS / b5横断技術gate GREEN**
- protocol: `22.0.0`
- artifact version: `2200.0.0b5`
- decisions: `2026-08-20-03`／`2026-08-20-04`／`2026-08-21-01`／`2026-08-21-02`／`2026-08-22-02`
- knowledge execution contract: `00-hub/release-gate-notes_ja.md@7d5762dbe624096d73aac326effe4714bbe6c404`
- target runtime: Minecraft `1.21.11`／Paper `1.21.11-132`／Java `21.0.11`

本recordは、有限runtime policy、構造化block値、height／spawn、entity handle、build execution mode、
`connection.flush`、3種event、DimensionKey、Python／Scratch／WireScopeをb5の一組として判定する。
公開tag／release／registry publish、public deployment、b6 API、Scratch browser保存、capacity本較正を
GREENとはしない。

## Exact compatibility set

| Component | Source / CI | Artifact identity |
| --- | --- | --- |
| McRemote | `bbbb53602a9c375e2ead3ee4c22174d5cf424f55` | `mc-remote-1.21.11-2200.0.0b5.jar`、195,998 bytes、SHA-256 `f7ddbcb5a92acadfe1adb7a9f6a4f50a05707e2eefbd1c01ff9aeeebe0a36547` |
| Python | `64b0f8831fa33e74f1b70b9102b3f29ec99b8e14` | wheel 170,271 bytes／SHA-256 `370f0fef3d5124a1024cbea8dfb4c65f2080cb545ab342086a827287d0f3f195`、sdist 175,715 bytes／SHA-256 `4337c6502f2be58e2bbf526d657c3f41d962bab08dd5a68eeb9527d66c9896b6` |
| Scratch／Bridge | `1a11c46bac5696afd3f494caac56ae682ed00fb0`／CI `32574020556` | GUI artifact ID `9476135596`／digest `sha256:a5fef95460d2e07accd5eb82276def9eafa36692166e1db34e833447e6f6865e`、Bridge ID `9476136894`／digest `sha256:2b84bf753ac67ea4906c9beb590cdb63d03da282015e40995ec129e3697b8e7b` |
| WireScope | Scratch sourceと同じ | ZIP 59,836 bytes／SHA-256 `407031d5e64279d90572f0843c788d2e4d9daac5b1ad12ffa121fa7f9fca6964`、manifest 2,321 bytes／SHA-256 `15d0c6b9a46ee68ac93dc850c9c5014c46476f7af1a49c7e98b2397cd7f95bda` |

observer schema、observer session、Scratch handoff、station attachはversion `1`、compatibility revisionは
`v1.1`である。Python担当がScratch exact sourceからNode `24.19.0`でWireScopeを独立再生成し、Scratch生成物、
Python同梱物の両方へbyte-for-byte一致させた。

## Deterministic gate

| Surface | Verification | Result |
| --- | --- | --- |
| McRemote | Java 95 tests、runner 4 tests、clean build、runner構文、diff check | PASS |
| McRemote artifact | 独立clean checkout 2件から同一JAR | PASS |
| Python | Python 3.11／3.13で各225 tests、observer focused 109 tests、lock、compile、fixture、metadata／RECORD／license | PASS |
| Python artifacts | 独立clean checkout 2件からwheel／sdistが各byte-for-byte一致 | PASS |
| Scratch | CI run `32574020556`の全job、VM／GUI full regression・build | PASS |
| Scratch McRemote | McRemote 327 assertions、event DTO 22 assertions、protocol 12 tests、WireScope 66 tests、GUI targeted 14 tests | PASS |
| WireScope artifact | 同一Scratch commitから2回生成しZIP／manifest一致 | PASS |

candidateへ固定した暫定policyはcommand FIFO `1024`、response queue `64` frames、event ring `256` events／
`262144` bytes、poll default／server max `64`／`64`、entity handles `256`、particle count `1000`、
work request／session／player／global `4096`／`4096`／`8192`／`32768`、compact poll response最大
`61440` bytes、Python send queue `1024`、request／flush timeout `60.0`秒、TRACE `0.0`〜`2.0`秒・既定
`0.25`秒である。これらは有限性と上限時挙動を閉じるb5暫定値であり、最終capacityではない。

## Live evidence

### McRemote non-DimensionKey slice

新McRemote candidateの直系ancestor `fc84c8fd5e41c07c5d89671f193fdb7012eabd36`／JAR
`7f9bf3616accc27cac100c705aa3bfc722024978a76a5505015d80047054012f`で、structured block、
`getBlocks`、`getHeight`、座標先行particle／entity spawn、256 handlesと257件目のcapacity拒否、FIFO／flush、
1041 notification burst、`events.poll`、validationを実PaperでPASSした。GitHub compareで同sourceが新candidate
`bbbb5360…`のmerge baseかつ直系ancestor（新candidateが1 commit ahead）であることを確認した。
新commitの変更はDimensionKey sliceであり、上記非影響live観測を再実行せず、95件の新candidate testと組み合わせる。

### Python DimensionKey segment

exact wheelと新JARを使い、次をPASSした。

- authenticated helloのcanonical `dimension`／origin
- `overworld`→`minecraft:overworld`とbuild contextの一体同期
- `getPose()`／同一poseの`setPose()`
- `world`を旧aliasにせず`minecraft:world`として`unknown_dimension`
- `myworld:world`をclient allowlistで拒否せずserverの`unknown_dimension`まで搬送
- `build.setWorld`の`method_not_found`と、失敗後のclient context不変
- `block_right_click`／`chat_posted`／`projectile_hit`のcanonical dimension
- same-context guardと意図的dimension mismatch拒否
- WireScope schema version `1`、`world` field不在、real-browser frame一覧、source終了表示

初期2回の停止はrunnerのerror data過剰固定とbrowserが消費したsnapshot slotの再取得によるtest harness不具合で、
candidate／server／configは変更していない。tee後の最終runを本recordのPASSとする。

### Scratch DimensionKey segment

exact CI buildと同じ新JARを使い、次をPASSした。

- 標準menu `overworld`／`the_nether`／`the_end`と完全修飾build context result
- `myworld:world`のserver-side `unknown_dimension`と、`world`旧alias不在
- `player.getPose`／`player.setPose`
- chat、right-click、projectileの3 hat
- 全event DTOのcanonical dimension、capture済みorigin、loss `0`
- real-browser WireScopeのbuild／player／event frameと`world` field不在

250 ms間隔の`events.poll`が100-frame observer windowを押し流すため、各人間操作後にScratch tabを閉じ、
終了後の静止履歴を確認する分割runを使った。初回黒画面は旧localhost cacheが現行ZIPにない旧JS名を要求したためで、
同じexact artifactをfresh originから配信して現行assetのHTTP 200と表示を確認した。candidate変更とは扱わない。

## Sanitized artifacts

- [python-result-summary.json](../artifacts/2026-08-22-b5-dimension-key-live/python-result-summary.json)
  - SHA-256: `f221a0b60ecf0132d5049fa81b21552e65eff56a39c9f12f0b149968825885d7`
- [scratch-selected-frames.json](../artifacts/2026-08-22-b5-dimension-key-live/scratch-selected-frames.json)
  - SHA-256: `ecf2b19c9667c2e3e61bd75870b05aa641f837a84b87ef5ecf37f2f38e6a423a`
- [redactions.json](../artifacts/2026-08-22-b5-dimension-key-live/redactions.json)

選択frameはDimensionKey、origin、座標、角度、test chat文字列、error reasonを保持する。これらを秘密とは扱わない。
bearer token、pairing ID、private endpoint、player UUIDは主張に不要なため収集artifactへ入れていない。pair codeは
必須redaction対象ではないが、今回のsummaryには収録していない。

## Gate conclusion

`2026-08-21-02`のb5最小横断gateについて、有限policy、boundary fixture、Scratch full regression／build、clean
common artifact、実pluginの短いevent／block／spawn／mode wire smoke、Python／Scratch real-browser WireScope E2E、
protocol 22 DimensionKey改訂が一つのexact compatibility setへ収束した。したがって**b5横断技術gateをGREEN**とする。

GREENはhuman release ownerによるtag／GitHub prerelease／registry publish／public deployの批准を代替しない。
外部release操作は別途明示承認後に実施し、作成後identityを再確認する。

## Non-claim／後続

- Scratch browser保存、`.sb3`／`.sprite3` compatibility、IndexedDB、quota／破損／migrationはb5後・b6前の独立entry gate。
- b6のfilter／clear、nearby／entity pose／remove、sign、typed particle等を実装済みとはしない。
- full load／soak、授業相当負荷、暫定capacityの本較正を完了とはしない。
- custom namespaceのgrammarとserver到達は確認したが、実際にloadedされた非`minecraft` dimensionの成功往復は未確認。
- other Paper／Minecraft versions、public hosted deployment、release rollbackをGREENとはしない。
- 通常dev環境の恒久起動方式、Stack runbook、backstage inventoryの改訂完了を主張しない。
