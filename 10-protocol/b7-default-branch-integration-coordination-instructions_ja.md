# b7 default branch統合 coordinator指示書

> status: 完了。三default branchを`b7-integrated-source-set-1`として固定済み。
> 訂正: 当初の「coordinatorがartifactを生成する」という記述は役割境界を誤っていた。release change coneへ入る
> componentだけを各ownerが生成し、coordinatorは返却identityを照合する。fixture ownerをproduct artifact参加者とみなさない。

## 目的

b7の照合済み三candidateを、内容を変えず各default branchへ着地する。これはsource identityを固定するgateであり、
tag、GitHub release、PyPI／npm／OCI公開、shared deploymentを同時に行わない。

入力knowledgeは`95b1011126901898c538ad6c0b7c790a26268b88`、successor fixtureは
`scratch-editor@773e2984132d82bb6e740d6458107fe42ef68a0a`、20,367 bytes、SHA-256
`586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`、93 unique casesである。

## 統合順序

1. Scratch owner fixtureを`develop`へfast-forwardする。
2. McRemote product candidateを`main`へfast-forwardする。
3. Python component candidateを`main`へfast-forwardする。
4. release change coneへ入るcomponent ownerが統合sourceからartifactを生成して返却し、coordinatorがdefault SHAとartifact
   identityを横断照合する。fixture evidenceだけを持つrepoへproduct artifact生成を自動要求しない。

順序は正本fixture、server、consumerの着地関係を読みやすくするためであり、前componentの公開releaseを次componentの
開始条件にはしない。

各担当は作業直前にremote defaultをfetchする。下記固定baseから動いていた場合、候補をrebase、merge、cherry-pickせず
停止してcoordinatorへ返す。固定baseのままなら候補はstrictly aheadであるため、merge commitを作らずfast-forwardする。

| repository | default | 作業前固定SHA | candidate | remote比較 |
| --- | --- | --- | --- | --- |
| `scratch-editor` | `develop` | `5df50144da13b1a1c8c23b01f2d0138ffd17b953` | `773e2984132d82bb6e740d6458107fe42ef68a0a` | `+2 / -0` |
| `McRemote` | `main` | `4e8f1ff1bd48bfa28c465f2dc24060fbb419317f` | `3d5f710db97f4b14613f7e0abaafd535701d1906` | `+5 / -0` |
| `minecraft-remote-api` | `main` | `ddcdc9da431aab7102867e103478469dda567e6f` | `8f4bc4b96ae74fb5370a3d804676cd07e5352346` | `+3 / -0` |

## Repository別指示

- Scratch: [`b7-default-branch-integration-instructions_ja.md`](../13-scratch-client/b7-default-branch-integration-instructions_ja.md)
- McRemote: [`b7-default-branch-integration-instructions_ja.md`](../11-plugin/b7-default-branch-integration-instructions_ja.md)
- Python: [`b7-default-branch-integration-instructions_ja.md`](../12-python-client/b7-default-branch-integration-instructions_ja.md)

## 今回動かさないrepository

- `mc-remote-stack`: source変更なし。tag前candidateや担当local artifactをpinしない。統合後artifact setと公開release identityが
  固定された後に、別指示でversion／digestを更新する。
- `minecraft-remote-java`: protocol `23.0.0`／artifact `2300.0.0b6` baselineを維持する。b7 directionを今回追従せず、
  main、version、fixture、tagを変更しない。
- park済み`minecraft-remote-protocol`: owner移管は批准していない。b7入力、tag、release、consumer参照先にしない。
- McRemote `agent/b7-live-auto-runner@51f4304da0c6bbf7185454644807729faca4b3c3`: 旧`mcr.lightning`前提と広い
  live scenarioを含むtest tool branchであり、今回のproduct mainへ統合しない。

## 統合後gate

三default branchのremote SHA、candidateとのtree／commit関係、clean checkoutでの再検証を受領してから、coordinatorが
`b7-integrated-source-set-1`を固定する。その後、release参加componentをsource graphから確定し、そのownerだけが統合SHAから
担当artifactを生成してdurable identityと検証結果を返す。coordinatorは不足artifactを自らbuildせず、fixture ownerという
理由だけでGUI／Bridge／WireScope等を追加しない。tag／GitHub prereleaseはartifact setと最小統合smokeの後に別承認で行う。

## 完了結果

- Scratch: `develop@773e2984132d82bb6e740d6458107fe42ef68a0a`
- McRemote: `main@3d5f710db97f4b14613f7e0abaafd535701d1906`
- Python: `main@8f4bc4b96ae74fb5370a3d804676cd07e5352346`

三者ともcandidate exact commit／treeへのstrict fast-forwardである。計画したScratch先行に対し、実際には少なくとも
McRemoteがScratchより先に着地したが、三fixed base、最終tree、fixture bytesに影響しないため巻き戻さない。詳細は
[`b7 artifact candidate記録`](b7-artifact-candidate-record_ja.md)を正とする。
