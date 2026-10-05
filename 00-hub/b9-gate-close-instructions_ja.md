# b9横断release gate closeの依頼（handoff-materialsの分類）

> b9横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-04の節）は、4 repoの公開とPyPI.orgへの公開を照合し終えた。
> gateを閉じる前に、b9の間に作った`handoff-materials`を分類してもらう依頼です。参照するknowledge commitは、この依頼が入った
> mainのcommitです。default branchへの統合はcoordinatorが照合済み（McRemote main `5cb33eb`、Python mainは`b901c88`の1つ先の
> `39f2ec9`、Scratch develop `7fbbf03`、minecraft-remote-tooling main `dc1ab83`）なので、この依頼には含めない。

## 共通

- 分類: 自repoのb9の`handoff-materials`（2026-10-04〜10-05のdirectory）を、次の3つに分ける
  - ① knowledgeのevidenceへ移す: 後から同じ観測を再現しにくいもの（実機試験の素材、公開時の照合、人間の確認など）
  - ② 自repoで持ち続ける: 後続（rc1など）で使うもの。何に使うかと、捨ててよくなる条件を書く
  - ③ 捨てる: knowledgeか公開物に同じ内容があるもの、一時的なもの
- 既に収容したもの: 下の表のdirectoryは、knowledgeへ収容済み。全文とSHA-256が収容先と一致するかを確かめ、一致すれば元を
  ③として扱ってよい。knowledgeで変えたfileは表に書いた
- 守ること: knowledgeへ全文が移ったことをcoordinatorが確かめるまで、①の元を消さない（b8のときの規則）。token、private address、
  player UUID、private設定は①に入れない
- 返却: directoryごとに①②③と理由、①はfile一覧（bytes、SHA-256）と収容先の案、②は使い道と捨ててよくなる条件。knowledgeの
  commitは実際に読んだSHAを書く

| repo | directory | 収容先 | knowledgeで変えたfile |
| --- | --- | --- | --- |
| McRemote | `2026-10-05-b9-dev-restart` | `14-evidence/artifacts/2026-10-05-b9-dev-live/mcremote/segment-0/` | `restart-result_ja.md`、`deployment-result.json`（home directoryのpathを`~`へ） |
| McRemote | `2026-10-05-b9-mcremote-live-auto` | `14-evidence/artifacts/2026-10-05-b9-dev-live/mcremote/segment-1/` | なし（`__pycache__`は収容していない） |
| Python | `2026-10-05-b9-python-live` | `14-evidence/artifacts/2026-10-05-b9-dev-live/python/segment-2/` | なし |
| Python | `2026-10-05-b9-dev-hello` | `14-evidence/artifacts/2026-10-05-b9-dev-live/python/saved-token-check/` | なし |
| Python | `2026-10-05-python-windows-entry` | `14-evidence/artifacts/2026-10-05-python-windows-entry/`（materialsの2 file） | なし |
| Scratch | `2026-10-05-b9-scratch-dev` | `14-evidence/artifacts/2026-10-05-b9-dev-live/scratch/segment-3/` | なし（`private/`、`runtime/`、`artifacts/`、PNG 4枚は収容していない） |

## McRemote

分類するもの: `2026-10-04-b9-mcremote-confirmation`、`2026-10-05-b9-mcremote-candidate`（JARの再現性の比較）、
`2026-10-05-b9-mcremote-release`、`2026-10-05-tooling-repo-name`（`2026-10-05-02`として着地済み、knowledge `945807b`）、
上の表の2件。b8の②として残している`2026-10-03-b8-mcremote-release`（JARの権限bitの比較）は、b9で権限bitを固定し、手元とCIの
JARが一致したので、捨ててよいかを返す

## Python client

分類するもの: `2026-10-04-b9-python-confirmation`、`2026-10-05-b9-python-work`、`2026-10-05-b9-python-tooling`、
`2026-10-05-b9-python-release`（PyPI.orgへの初公開の照合）、上の表の3件

## Scratch editor（WireScope）

分類するもの: `2026-10-04-b9-scratch-confirmation`（移管評価の別紙を含む）、`2026-10-05-b9-tooling-migration`、
`2026-10-05-b9-release`（OCIの比較。公開したOCIと凍結したOCIのmtimeの照合を含む）、上の表の1件。b8の②として残している
directoryのうち、b9で用が済んだもの（`2026-10-03-wirescope-column-width`など）も返す。`private/`と`runtime/`は①に入れない
