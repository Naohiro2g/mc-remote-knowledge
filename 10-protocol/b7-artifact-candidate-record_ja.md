# b7 artifact candidate記録

> 状態: `b7-integrated-source-set-1`固定済み。`ec7a233…`で記録したcoordinator生成の
> `b7-integrated-artifact-input-1`はowner artifactでないため正式gate入力から失効。
> Scratch owner artifact、Scratch／Bridge OCI、最終artifact set、tag、公開releaseは未完。

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
| Python | `minecraft_remote_api-2301.0.0b7-py3-none-any.whl` | 177,243 | `cc5842b79501fd103f1e7d2e3a4ea1cc72029e6969265591f60c9324338d3094` | main再生成物がcandidateとbyte一致。担当local artifact |
| Python | `minecraft_remote_api-2301.0.0b7.tar.gz` | 183,908 | `6be3db058cc1aff7cf5375b58dc11737e5d471f0f67a6cdaa28a869d0c12c236` | main再生成物がcandidateとbyte一致。担当local artifact |

この表はdefault branch統合直後の入力だった。後続のcoordinator再生成とdurable staging固定は§6を正とする。

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

source setとfixtureは固定済みで、McRemote／Python担当のartifact identityも返却済みである。一方、Scratch GUI、Bridge、
common WireScopeの正式owner artifactは未返却であるため、pre-OCI artifact入力は未成立である。次はScratch担当が
`develop@773e298…`から指示書どおり生成・検証し、四成果物のdurable identityを返す。coordinatorはその返却物を再buildせず、
remote source／fixture／manifest／digestと照合する。

owner artifact照合前にScratch／Bridge OCI、最終artifact set、tag、GitHub prereleaseへ進まない。OCI push、PyPI／npm、
Stack pin、shared deployも未実施である。Python wheel内bundled WireScopeの扱いは別のrelease判定事項として維持する。
