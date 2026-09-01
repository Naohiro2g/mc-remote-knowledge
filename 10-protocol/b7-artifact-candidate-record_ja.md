# b7 artifact candidate記録

> 状態: `b7-integrated-source-set-1`固定済み。統合artifact set、tag、公開releaseは未完。

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

McRemote JARは既存durable stagingにある。Python二artifactはdigest報告であり、coordinator用durable stagingへの収容を
まだ主張しない。Scratch GUI、WireScope、Bridge／Scratch OCIは統合developから未生成である。

## 5. 次gate

coordinatorは三default SHAから新しい`b7-integrated-artifact-set-1`を生成する。McRemote JARとPython wheel／sdistは
統合sourceから再現して上表とのbyte一致を確認する。Scratch系はb7で変更したprotocol mirrorが実際に入るconsumerだけを
source graphから確定し、GUI、WireScope、Bridge／OCIの再生成／b6 artifact再利用を区別する。再利用は「source差分がない」
だけで決めず、artifact inputとsource stampを照合する。

artifact set、manifest、最小統合smokeが固定されるまで、tag、GitHub prerelease、PyPI、npm、OCI push、Stack pin、
shared deploymentを行わない。Java Clientはprotocol 23.0／b6 baselineのまま今回のartifact setへ含めない。
