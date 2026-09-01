# b7 release coordination — Claude Code引継ぎ

> 状態: coordinator交代。以下を読んでからb7 release scopeを再監査する。
> 本票はrelease承認ではなく、誤った進行を止めて検証可能な現在地を渡すための引継ぎである。

## 1. 最優先の訂正

前coordinatorは、Scratchがshared fixture ownerであることからScratch GUI／VM／Bridge／WireScopeもb7 release artifactだと
誤って推測した。その結果、自分でScratchをbuildし、次にScratch担当へ同じbuildを依頼し、最後に正しいb6 client versionを
b7へ上げる誤指示まで出した。

この連鎖を現行指示として使わない。

- component ownerだけが担当artifactを生成し、coordinatorはidentityを照合する。
- fixture ownerであることは、そのrepositoryの全product artifactがrelease参加することを意味しない。
- change cone外componentへversion bump、build、tag、OCIを自動要求しない。
- Scratch担当は既に全buildを複数回やり直している。**追加buildを要求しない**。必要なのは既存結果の受領・scope判定である。

## 2. 確定済みsource／contract

| 対象 | identity | 状態 |
| --- | --- | --- |
| McRemote | `main@3d5f710db97f4b14613f7e0abaafd535701d1906` | b7 product実装、JAR owner identity返却済み |
| Python | `main@8f4bc4b96ae74fb5370a3d804676cd07e5352346` | b7 Client Library実装、wheel／sdist owner identity返却済み |
| Scratch | `develop@773e2984132d82bb6e740d6458107fe42ef68a0a` | b7 shared fixture owner commit。Scratch runtime b7実装とは限らない |

- protocol contract: `23.1.0`、artifact version: `2301.0.0b7`
- wire正本: `10-protocol/wire-format-design_ja.md` §5.8.2
- permission改訂: DECISIONS `2026-09-01-02`
- fixture: 20,367 bytes、93/93 unique、SHA-256
  `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`
- source set: `b7-integrated-source-set-1`

McRemote JAR:

- `mc-remote-1.21.11-2301.0.0b7.jar`
- 222,951 bytes
- SHA-256 `f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9`

Python artifacts:

- wheel 177,243 bytes、SHA-256 `cc5842b79501fd103f1e7d2e3a4ea1cc72029e6969265591f60c9324338d3094`
- sdist 183,908 bytes、SHA-256 `6be3db058cc1aff7cf5375b58dc11737e5d471f0f67a6cdaa28a869d0c12c236`

## 3. Scratch実物から確認した事実

`scratch-editor@773e298…`では二つの別surfaceが同居する。

1. `mc-remote/protocol`はprotocol `23.1.0` mirror／fixture owner。
2. `packages/scratch-vm`の実Scratch Clientはprotocol `23.0.0`、diagnostic version `2300.0.0b6`。

実Scratch Clientはhelloへ`23.0.0`を送り、b7 direction／lightning learner surfaceを実装していない。repository検索では
Scratch VM／GUI／Bridge／WireScopeから`@mc-remote/protocol`へのruntime importはない。したがってProtocol leafの23.1化から
Scratch runtime 23.1対応、GUI b7 artifact、Scratch b7 tag／OCIを導いてはならない。

現時点の有力な読みは、Scratchはb7でfixture owner evidenceだけを担い、Scratch runtime releaseはb6のまま維持する、である。
ただしClaude Codeはこの文を盲目的に採用せず、versioning／release roadmap／実source graphを再確認してから現行gateを
確定する。

## 4. Scratchが既に完了した作業

Scratch ownerは`develop@773e298…`から全buildをやり直し、owner staging
`/home/tsuji/.local/share/mc-remote/gates/b7-scratch-owner-artifact-set-1/`へ次を置いた。

| artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `scratch-gui-build-b7.tar.gz` | 234,630,336 | `dd3361255b3d0a507c209e0c1e5781ed13f405ffb5c4ca7d32ebe2d63c89c52f` |
| `mc-remote-bridge-dist-b7.tar.gz` | 3,052 | `11199a8e6966e8a5160411104934498657f4befd3d27a8fc25c88f51afa31c72` |
| `wirescope-app.zip` | 79,169 | `b3d6270299195d2c3db93c9d122938be6ae20d23e0f10e19afe3b0e99e3ca315` |
| `wirescope-app.manifest.json` | 2,321 | `4f3debeedc0dbcb1d4749b609c2693d27bf944453e14b767b0730476f48f0ca1` |

Protocol 28件、Bridge 30件、WireScope 130件、root production buildをPASSし、fixture、archive、manifestも照合済みである。
これは無駄だったという理由で消さないが、b7 release inputへ自動昇格もしない。

さらに誤ったversion follow-up指示により、Scratch担当は全buildをもう一度実行済みである。branchは
`agent/b7-client-version-followup@57e28850165feb8813529766fad882ad0463612b`、parent=`773e298…`、tree=
`88a68c3ef307f63bc46a5036a83e62b9e92e70c4`で、変更はclient versionと対応testの3ファイルだけである。
exact post-build artifact identityは本会話へ未返却だが、**再buildを依頼しない**。必要なら既に完了した結果のidentity返却だけを
求める。

このbranchを`develop`へmerge／fast-forwardしない。削除も自動で行わず、誤指示の監査痕跡として保持する。

## 5. 失効したknowledge進行

- `ec7a233…`: coordinator自身のbuildを正式pre-OCI入力として記録した。provenance境界違反で失効。
- `07e48c4…`: owner buildへ戻したが、Scratch artifact自体が必要という前提を疑わなかったため不十分。
- `e3a8fcf…`: `2300.0.0b6`をb7 blockerと誤認しversion bumpを指示した。撤回。

履歴は書換えず、後続commitと本票でsupersedeする。

## 6. Claude Codeが最初に行う監査

1. `CLAUDE.md`、本票、`b7-artifact-candidate-record_ja.md`、release gate notes、versioning、release roadmap、
   wire §5.8.2を読む。
2. ScratchのProtocol leafとruntime Clientを別surfaceとしてsource graphから確認する。
3. b7公開単位をcomponentごとに列挙し、各componentについて「実装差分」「version」「artifact」「tag要否」を表にする。
4. 次の有力案を反証する: b7 release対象はMcRemote／Python、Scratchはfixture evidenceのみ、Javaはb6 baseline、Stack変更なし。
5. Python wheel内の旧bundled WireScopeも、b7 change cone外なら自動blockerにしない。実際の利用面と既存non-claimを確認する。
6. 誤ったScratch version branchを統合しないことをremoteで確認する。
7. SSOTの誤記を、履歴を消さずに訂正する。新しい横断判断を着地する前に人間へ、候補、利点、失うものを提示する。

## 7. 禁止事項

- Scratchへ追加build、version修正、artifact再生成を依頼しない。
- `57e288…`をmergeしない。
- coordinatorがdev repo artifactを代理buildしない。
- Scratch fixture owner identityをScratch b7 product release identityへ読み替えない。
- artifact scope監査前にOCI、tag、GitHub release、Stack pin、shared deployを行わない。
- 「指示書に書いてある」ことを実物との矛盾より優先しない。

## 8. 現在地

- step: 比較・検証 (`compare_verify`)
- status: 差分あり (`diff_found`)
- sink: 捕捉
- 根拠: Scratch Protocol leafは23.1、runtime Clientは23.0／b6で、誤ったversion branchと全build再実行が既に発生
- 次の一手: b7 release参加componentをsource graphと既存SSOTから再監査し、人間へ訂正案を提示する

## 9. セッションクローズ票

- repo: `mc-remote-knowledge`
- surface: b7横断release coordinator
- branch/commit: `main`／本票を含むcommit
- 作業範囲: 誤ったScratch artifact／version進行の停止とClaude Code引継ぎ
- 今回やったこと: remote source／artifact／bad branchをread-only照合し、実物と指示の矛盾を整理
- 変更ファイル: 本票、release gate／artifact record／roadmap、撤回対象指示書
- 検証: GitHub remote branch／parent／tree／3-file diff、Scratch sourceのprotocol／client version／import境界
- 未完了: b7 release component scopeの再批准、誤記訂正、正式artifact set、release
- 次に読むもの: 本票§6に列挙
- 次の一手: 追加実行前にcomponent参加表を人間レビューへ出す
- 未着地の搬送物: Scratch follow-up全buildのexact結果identity（再実行不要）
- NOTES/DECISIONS: 新decision採番はまだ行わない
- 注意点: Scratch担当は全buildをやり直し済み。再build要求禁止
