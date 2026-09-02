# b7 artifact candidate記録

> 状態: `2026-09-02-01`によりScratch／WireScopeもb7 release対象と確定。Python owner artifactは
> Scratch set 2 WireScope pairへ差し替えた新identity（`codex/b7-wirescope-set2@91a25d3…`）へ更新済み、旧wheel/sdistは失効。
> McRemote／Scratch owner set 2／Python新identityの四component分identityをcoordinatorがGit／local staging照合済み。
> 次はexact set凍結。最終artifact set、tag、公開releaseは未完。

## 1. 統合source set

2026-09-02、b7の三candidateを内容変更なしで各default branchへfast-forwardし、次を
`b7-integrated-source-set-1`として固定した。

| component | default branch／統合SHA | tree | candidateとの関係 |
| --- | --- | --- | --- |
| Scratch protocol owner | `develop@773e2984132d82bb6e740d6458107fe42ef68a0a` | `e48fe82916ec82a5d05b216f50e353bcbf87a6f4` | exact candidate、旧defaultから`+2 / -0` |
| McRemote | `main@3d5f710db97f4b14613f7e0abaafd535701d1906` | `cdb96ac50055d03a3c7550cd8b6643cd9b802270` | exact candidate、旧defaultから`+5 / -0` |
| Python | `main@8f4bc4b96ae74fb5370a3d804676cd07e5352346` | `08992729964cee09583637334163a2eadd11e143` | exact candidate、旧defaultから`+3 / -0` |

coordinatorはGitHub APIから三default SHA／treeを照合した。merge commit、squash、cherry-pick、統合時の内容編集はない。
計画ではScratch→McRemote→Pythonの着地順を指定したが、実際には少なくともMcRemoteがScratchより先に着地した。
Pythonを含む厳密なpush時系列はremote commit identityから主張しない。この順序差は、三branchが独立したfixed baseから
strict fast-forwardされ、最終source／tree／fixtureが一致するため、source setの同一性を変えない。予定順を満たすための
巻戻しや再pushは行わない。

## 2. Shared fixture

三default branchに配置された`direction-lightning-v23.1.json`は全てSHA-256
`586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`で一致する。20,367 bytes、
Git blob `7371787ca6484a45dec0c7893608339961ae6fcf`、93件／93 unique IDである。ownerは引き続き
scratch-editor内`@mc-remote/protocol`であり、park済みProtocol repositoryへ移管していない。

## 3. 統合時検証

- Scratch: ESLint、Prettier、Vitest 28件、protocol build、`git diff --check` PASS。
- McRemote: candidate／統合後mainともPaper 1.21.11全203件、Paper 26.2／Java 25対象61件、fixture、method registry、
  `mcr.lightning` production／README 0件、`git diff --check` PASS。
- Python: targeted 48件、全253件、lock、対象lint／format、build／METADATA、`git diff --check` PASS。
  repository全体へ未導入のRuff全ruleを統合時に追加せず、既存検出142件をb7修正へ混ぜていない。

これらは各担当報告であり、coordinatorはremote SHA／treeとfixture exact bytesを独立照合した。candidateで完了した
deterministic／targeted live evidenceは、統合defaultがcandidateとexact commit／treeであるため同じsourceへ結び直せる。

## 4. 現在のartifact identity

| component | artifact | bytes | SHA-256 | 状態 |
| --- | --- | ---: | --- | --- |
| McRemote | `mc-remote-1.21.11-2301.0.0b7.jar` | 222,951 | `f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9` | main再生成物がlive PASS／durable candidateとbyte一致 |
| Python（旧、失効） | `minecraft_remote_api-2301.0.0b7-py3-none-any.whl` | 177,243 | `cc5842b79501fd103f1e7d2e3a4ea1cc72029e6969265591f60c9324338d3094` | b5時点bundled WireScopeを含むためb7最終候補として失効。§9参照 |
| Python（旧、失効） | `minecraft_remote_api-2301.0.0b7.tar.gz` | 183,908 | `6be3db058cc1aff7cf5375b58dc11737e5d471f0f67a6cdaa28a869d0c12c236` | 同上 |
| Scratch owner GUI | `scratch-gui-build-b7.tar.gz` | 234,651,616 | `d6a569f1f315ca06a24f9d7a987129e824f5df60eb32d226dd6d776f47d20b8c` | set 2、`0be46fcfa…`。coordinator local staging照合済み |
| Scratch owner Bridge中間 | `mc-remote-bridge-dist-b7.tar.gz` | 3,052 | `11199a8e6966e8a5160411104934498657f4befd3d27a8fc25c88f51afa31c72` | set 2。b6と一致（Bridge無変更） |
| Scratch owner WireScope | `wirescope-app.zip` | 79,418 | `98d684dc15f369f6568d249357d8fd3af11893859d3c07c2554295df19a263b8` | set 2。coordinator local staging照合済み |
| Scratch owner WireScope manifest | `wirescope-app.manifest.json` | 2,321 | `7498e32150884aec8c3d562b454d8b042032aa21893ae7fe886c06df2baf028f` | set 2。coordinator local staging照合済み |
| Python（新、現行） | `minecraft_remote_api-2301.0.0b7-py3-none-any.whl` | 196,970 | `81540d22b1ee05d7b24bd2e6c9270a37a194c6c1ddc868148a8263624826d2ba` | branch`codex/b7-wirescope-set2@91a25d317c95570fd9d92b5e63a5f585a856eda3`。同梱WireScope pairをcoordinatorがGit blobで照合、Scratch set 2と一致 |
| Python（新、現行） | `minecraft_remote_api-2301.0.0b7.tar.gz` | 203,313 | `55a9915b7607e35e2c1f335561b65fcd38deff90fe49f5b56c65122665b37a0b` | 同上 |

この表はdefault branch統合直後の入力だった。後続のcoordinator再生成とdurable staging固定は§6を正とする。
Python新wheel／sdist bytes自体はcoordinator未再build（owner報告。同梱WireScope pairのみGit blobで独立照合済み）。

## 5. 次gate

各component ownerがdefault branchからartifactを生成してidentityを返し、coordinatorはsource、fixture、artifact digest、
検証報告を横断照合して新しい`b7-integrated-artifact-set-1`を固定する。coordinator自身の再buildをowner artifactの代替にしない。
Scratch ownerの実行内容は
[`b7 Scratch owner artifact生成指示書`](../13-scratch-client/b7-owner-artifact-generation-instructions_ja.md)を正とする。

artifact set、manifest、最小統合smokeが固定されるまで、tag、GitHub prerelease、PyPI、npm、OCI push、Stack pin、
shared deploymentを行わない。Java Clientはprotocol 23.0／b6 baselineのまま今回のartifact setへ含めない。

## 6. 失効したcoordinator参考build（pre-OCI）

coordinatorは役割境界を誤り、三default branchのisolated checkoutから自ら成果物を再生成し、Scratch／Bridge OCIを除く
六artifactを`b7-integrated-artifact-input-1`としてdurable stagingへ置いた。全fileはcopy後に再hashし、mode `0444`を確認した。
入力manifestは3,206 bytes、SHA-256
`f77242b5430322f311b2ff6104c02959d374b46e9472d042bcc4d698252a1de8`である。

bytesと検証結果は参考観測として保持するが、Scratch担当が生成・返却したowner artifactではない。したがってこのdirectory、
manifest、下表を正式pre-OCI入力、artifact candidate、release provenanceとして使わない。削除や履歴改変はせず、失敗経緯と
比較材料として残す。

| component | artifact | size（bytes） | SHA-256 |
| --- | --- | ---: | --- |
| McRemote | `mc-remote-1.21.11-2301.0.0b7.jar` | 222,951 | `f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9` |
| Python | `minecraft_remote_api-2301.0.0b7-py3-none-any.whl` | 177,243 | `cc5842b79501fd103f1e7d2e3a4ea1cc72029e6969265591f60c9324338d3094` |
| Python | `minecraft_remote_api-2301.0.0b7.tar.gz` | 183,908 | `6be3db058cc1aff7cf5375b58dc11737e5d471f0f67a6cdaa28a869d0c12c236` |
| Scratch | `scratch-gui-build-b7.tar.gz` | 234,630,336 | `dd3361255b3d0a507c209e0c1e5781ed13f405ffb5c4ca7d32ebe2d63c89c52f` |
| WireScope | `wirescope-app.zip` | 79,169 | `b3d6270299195d2c3db93c9d122938be6ae20d23e0f10e19afe3b0e99e3ca315` |
| WireScope | `wirescope-app.manifest.json` | 2,321 | `4f3debeedc0dbcb1d4749b609c2693d27bf944453e14b767b0730476f48f0ca1` |

McRemoteはJava 21のclean buildと203/203件をPASSし、JARはdefault branch担当生成物、live PASS物、既存durable
candidateとbyte-for-byte一致した。Pythonは`PUBLISHING.md`記載の`uv run --with pytest`で253/253件と`uv build`を
PASSし、wheel／sdistは担当生成物とbyte-for-byte一致した。最初のplain `uv run pytest`はpytestがproject dependencyに
ないため起動前に失敗したが、文書化済みの一時tool解決手順で再実行した。これを製品test FAILへ数えない。
最小artifact smokeではJAR内`plugin.yml`のversion／API／permission宣言、wheelのMETADATAとb7五API、wheel／WireScope
ZIPのCRC、sdist／GUI／Bridge tar inventory、GUI runtime configとWireScope manifestのJSON parseをPASSした。

ScratchはNode `24.19.0`／npm `11.12.1`のisolated checkoutで`npm ci`、全workspace production buildをPASSした。
protocolはESLint／Prettier、Vitest 28/28、build、BridgeはESLint／Prettier、Vitest 30/30、build、WireScopeは
ESLint／Prettier、Vitest 130/130、artifact buildをPASSした。Bridge testの最初のsandbox内実行はloopback listenが
`EPERM`となったが、network namespace制約外の同一sourceで30/30件をPASSしたため製品FAILではない。

GUI tarがb6と異なるのはb7 fixtureの混入ではない。b6統合source `df9264ec…`から今回のb7 base `5df50144…`までに、
release labelを固定文言から現在値の表示へ直すGUI commit `5df50144…`が入っている。fixture二commitはprotocol配下だけで、
GUI／VM／Bridge／WireScopeから`@mc-remote/protocol`へのruntime importはない。したがってGUIは新bytesとして採用した。
一方、Bridgeの決定論的中間tarは3,052 bytes／SHA-256
`11199a8e6966e8a5160411104934498657f4befd3d27a8fc25c88f51afa31c72`でb6とexact一致し、WireScope ZIPもb6と
exact一致した。WireScope manifestだけがScratch source stampを`773e298…`へ更新したため新digestになった。

`npm ci`のaudit表示は既存依存に83件（low 6、moderate 30、high 38、critical 9）を報告した。自動`npm audit fix`は
lock／sourceを変更するため本gateへ混ぜず、既存dependency riskとして保持する。Python wheel内にはb5時点の独立した
bundled WireScope appが残り、今回固定したcommon WireScope ZIPとは別物である。これはcandidate時点のnon-claimどおり、
b7 real-browser E2Eを主張しない。tag前に別artifactへ無断置換せず、release判定で既存境界として明示する。

## 7. 訂正後のgate

source setとfixtureは固定済みで、McRemote／Python担当のartifact identityも返却済みである。Scratch owner set 1も返却され、
coordinatorは再buildせずsource／tree、四fileのsize／mode／digest、archive inventory、WireScope manifestを照合した。しかし
Scratch Client versionがb6のままなのでb7 artifactとして受理せず、§8のfollow-upへ戻す。

owner artifact照合前にScratch／Bridge OCI、最終artifact set、tag、GitHub prereleaseへ進まない。OCI push、PyPI／npm、
Stack pin、shared deployも未実施である。Python wheel内bundled WireScopeの扱いは別のrelease判定事項として維持する。

## 8. Scratch owner set 1と当時のversion blocker判断（§9で撤回）

Scratch ownerは`develop@773e2984132d82bb6e740d6458107fe42ef68a0a`から専用staging
`b7-scratch-owner-artifact-set-1`へ次を生成した。coordinator参考buildを入力にせず、copy前後一致とmode `0444`を確認している。

| artifact | size（bytes） | SHA-256 |
| --- | ---: | --- |
| `scratch-gui-build-b7.tar.gz` | 234,630,336 | `dd3361255b3d0a507c209e0c1e5781ed13f405ffb5c4ca7d32ebe2d63c89c52f` |
| `mc-remote-bridge-dist-b7.tar.gz` | 3,052 | `11199a8e6966e8a5160411104934498657f4befd3d27a8fc25c88f51afa31c72` |
| `wirescope-app.zip` | 79,169 | `b3d6270299195d2c3db93c9d122938be6ae20d23e0f10e19afe3b0e99e3ca315` |
| `wirescope-app.manifest.json` | 2,321 | `4f3debeedc0db1d4749b609c2693d27bf944453e14b767b0730476f48f0ca1` |

remote `develop`／tree、GUI 3,449 filesと必須entry、Bridge inventory、ZIP／gzip／tar integrity、WireScope manifestの
source／archive／toolchain／recipe、fixture 20,367 bytes／93件を照合し返却と一致した。owner検証はprotocol 28件、Bridge
30件、WireScope 130件、root production build PASSである。GUIのb6との差はrelease-label修正`5df50144…`、Bridge tar／
WireScope ZIPの一致、manifest source更新も説明と整合する。npm auditのowner観測は85件で、自動fixしていない。advisory dataの
時点差をartifact identityへ混ぜず、coordinator参考build時の83件へ一致させる操作はしない。

以下はset 1直後の当時判断であり、§9で撤回した。

一方、sourceの`packages/scratch-vm/src/extensions/scratch3_mcremote/client-version.js`は`2300.0.0b6`で、hello
`params.client.version`とGUI notice／About labelへ投影される。protocol 23.1.0のb7 artifactが自身をb6と名乗るため、set 1を
正式pre-OCI入力へ昇格しない。次は
[`b7 Scratch client version follow-up指示書`](../13-scratch-client/b7-client-version-followup-instructions_ja.md)により三file／
7箇所だけを`2301.0.0b7`へ直し、専用branchで検証・pushする。default branch統合後、ownerがset 2を再生成する。

## 9. §8判断の撤回とcoordinator引継ぎ

§8末尾の判断は誤りである。Scratch repository内の`mc-remote/protocol`は23.1 fixture mirrorだが、実Scratch Clientは
`packages/scratch-vm`のprotocol 23.0.0／b6 surfaceであり、b7 direction／lightningを実装していない。両surface間にruntime
importもない。したがって`MCREMOTE_CLIENT_VERSION=2300.0.0b6`は取り残しでなく実装範囲と整合し、versionだけをb7へ
上げる方が誤表示になる。

誤指示branch `agent/b7-client-version-followup@57e28850165feb8813529766fad882ad0463612b`はparent `773e298…`、
tree `88a68c3ef307f63bc46a5036a83e62b9e92e70c4`で、versionと対応testの3fileだけを変更する。Scratch担当は指示された
全buildを既に再実行した。追加buildを要求せず、このbranchをdefaultへ統合しない。

set 1のowner provenance／検証事実は保持するが、Scratch runtime artifactをb7 release入力とするか自体が未確定である。
fixture owner commitからGUI、Bridge、WireScope、Scratch tag／OCIを自動的に導かない。次のcoordinatorは
[`b7 release coordination — Claude Code引継ぎ`](b7-release-coordination-handoff_ja.md)に従い、McRemote／Python／Scratch／
Java／Stackのrelease参加scopeをsource graphから再監査し、人間レビュー後に本記録を精密化する。
