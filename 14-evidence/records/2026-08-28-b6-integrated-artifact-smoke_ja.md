# b6 integrated artifact smoke evidence

## Record

- test ID: `2026-08-28-b6-integrated-artifact-smoke`
- test class: `unit/deterministic` + `live-human`
- result: **PASS — 統合後JARの起動、認証、新規session、通常再起動後session再利用**
- observed date: `2026-08-28`
- target: host-native `dev-integration`／Minecraft `1.21.11`／Paper `1.21.11-132`
- decision: `2026-08-26-08`／`2026-08-28-01`
- knowledge baseline: `0d4038888f11ef34f2157cc766b4975647b03d01`

本recordは、三repoのdefault branchへ統合した`b6-integrated-source-set-1`からScratch／Bridge OCIを除く六artifactを
clean環境で再生成し、McRemote統合JARを通常devへ配置して最小runtime smokeを実施した結果を固定する。
sign／`pickaxe_poke`／Scratch browser保存／WireScope UXのTier 2結果は先行recordを再利用し、本試験では
default branch統合後に追加されたMcRemote session token永続化fixとの結合点へ範囲を絞った。

## Exact compatibility set

| Component | Source identity | Artifact |
| --- | --- | --- |
| McRemote | `main@4e8f1ff1bd48bfa28c465f2dc24060fbb419317f` | JAR 204,463 bytes／SHA-256 `0ec8d4c0b105f3034361b260fc39fcb78013e932e684d34d5ca95c9a6c6a87a6` |
| Python | `main@a30a37b15658da655fe1e3535a73fb0e80c06f56` | wheel `0887807f…1877b`／sdist `0507a10c…e2da3b` |
| Scratch／Bridge／WireScope | `develop@df9264ec355dd722a848df46e96d4b0fc9340ca2` | GUI `1757f665…7ef5`／WireScope ZIP `b3d62702…ca315`／manifest `8570d3ee…296f` |
| protocol | — | `23.0.0` |
| artifact version | — | `2300.0.0b6` |

六artifactと入力manifestは`b6-integrated-artifact-input-1`としてcoordinatorのdurable stagingへ固定した。
入力manifestは2,127 bytes、SHA-256
`1a3b40fc3747359bd2a206f37aa4b8508989b97aedc6b6d584d8cfd49b3c4a4b`である。Scratch／Bridge OCIをまだ
含まないため、これを最終artifact setとは呼ばない。既存manual image workflowは同じsource SHAからScratchと
Bridgeの両multi-arch OCIを一回の実行でpublishする。

## Deterministic result

| Scope | Observation | Result |
| --- | --- | --- |
| McRemote clean export | `./gradlew clean test jar`、149/149件 | PASS |
| Python clean export | 242/242件、wheel／sdist生成 | PASS |
| Python artifact | 旧candidateとwheel／sdistがbyte-for-byte同一 | PASS |
| Scratch clean checkout | Node `24.19.0`／npm `11.12.1`、`npm ci`、全workspace production build | PASS |
| Scratch GUI artifact | 旧candidateとbyte-for-byte同一 | PASS |
| WireScope artifact | owner script二回のZIP／manifestが同一 | PASS |
| durable staging | 六fileをcopy後にsize／SHA-256再照合 | PASS |

追加で実行したscratch-vm full TAPはassertion-levelのowner集計を返さず、file-level
`132 total／11 fail／121 skip`となった。失敗には並列renderer初期化、SIGKILL、timeoutが含まれる。
これはowner報告の4003件集計へ換算せず、ownerからexact passed／failed／skipped内訳が返るまで確認事項を維持する。

## Runtime result

| Checkpoint | Observation | Result |
| --- | --- | --- |
| pre-stop | online player 0、旧candidate JARのrollback入力あり | PASS |
| deployment | Paper、world、config、credential backendを維持してJAR一件だけ交換 | PASS |
| first startup | McRemote `1.21.11-2300.0.0b6`、標準listener、credential `HEALTHY` | PASS |
| auth negative paths | tokenなし、未知token、旧prefix token、不正形式をそれぞれ契約どおり拒否 | PASS |
| new session | 人間が一度pairingし、認証済みhello `23.0.0`＋`catalog.get` | PASS |
| normal restart | online player 0を再確認し、同じ統合JARを正常停止・再起動 | PASS |
| persisted session | pairingなしで同じ期限内tokenを再利用し、認証済み`catalog.get` | PASS |

catalogの代表結果はblock 1,166、entity 157、particle 115だった。session再利用試験はauth成功だけでなく、
再起動後の認証済みmethod callまで到達して判定した。

## Operation observation

既存`run.sh`は自身で名前付きScreen sessionを作る。coordinatorが最初に`run.sh`を別のScreenで包んだ起動は、
server開始前に終了してdead outer sessionだけを残し、listenerを作らなかった。dead sessionを除去し、JAR、world、
config、credential backendを変えず`run.sh`を直接実行すると起動した。本番手順では`run.sh`をさらにScreenで
包まない。この観測を製品artifactのFAILへ読み替えず、運用手順の実測入力として残す。

## Sanitized artifacts

- [result-summary.json](../artifacts/2026-08-28-b6-integrated-artifact-smoke/result-summary.json)
  - 3,422 bytes
  - SHA-256: `990de3984efc9d1c3c9658f57f5614761ff46b58c99d034d2cc4ccc44bdb2b6c`
- [redactions.json](../artifacts/2026-08-28-b6-integrated-artifact-smoke/redactions.json)
  - 579 bytes
  - SHA-256: `1c9960525f8a49d0b8f4ca361c75ab4cabad8703904f23f793f35b53f38e52c0`

pairing code、session token、token hash、player UUID／name、credential UUID、private endpoint、raw logは
収録しない。Redaction境界は`redactions.json`を正とする。

## Claim boundary

本recordが証明するのは、上記exact integrated source／artifact入力でのclean build、通常devへの統合JAR配置、
起動、credential health、auth否定パス、新規session、同じJARの通常再起動後の期限内session再利用、認証済み
代表callである。次は証明しない。

- Scratch／Bridge multi-arch OCIのbuild／push、digest固定、container smoke
- Scratch testのowner exact passed／failed／skipped集計
- 最終`b6-artifact-candidate-set-4`
- public artifact upload、tag、release、b6 `GREEN`
- sign／poke／browser保存／WireScope Tier 2の再実行
- npm audit noticeの評価またはsecurity clean
