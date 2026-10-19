# rc1 gate closeの素材（2026-10-19）

> rc1横断release gate（`00-hub/release-gate-notes_ja.md` rc1）のclose分類（`00-hub/rc1-gate-close-instructions_ja.md`、
> knowledge `04c56b8da8ac0aaa5c393276d1a1c73d50860663`）で、McRemote、Python、Scratchが①とした素材を収容した。3 OSの試験の結果は
> `14-evidence/records/2026-10-19-rc1-candidate-3os-live-human_ja.md`、公開の照合はgate notesにある。この記録は素材の置き場所と
> 分類を示す。

## 収容した素材

| 収容先（`14-evidence/artifacts/2026-10-19-rc1-gate-close/`） | 中身 | 搬送元 |
| --- | --- | --- |
| `mcremote/2026-10-18-rc1-candidate/` | 候補のCIとJARの観測identity、23.2.0のclientのhelloを実Paper 2版（1.21.11、26.3）で受け入れたtranscript、起動時のSQLite providerの観測、供試buildの選定と範囲の返却票 | McRemote 同名 |
| `mcremote/2026-10-19-rc1-prerelease/` | 公開時のmain／tag／Releaseの属性、5 assetのGitHubのdigestと匿名HTTPSで取った実体の照合、dry runのmanifestの一致、tagのCIと候補の一致 | McRemote 同名 |
| `python/2026-10-18-rc1-python-candidate/` | 候補のCI artifactの取得、wheel／sdistと同梱WireScopeの照合、toolingの入力の由来、入れたwheelのsmoke | minecraft-remote-api 同名 |
| `python/2026-10-19-rc1-python-release/` | 公開時のRelease本文と属性とasset、取った実体と凍結値の照合、候補とのmanifestの比較、承認前のPyPIのjobの待ち（07:38:32 UTCの時点。その後に承認して公開済み） | minecraft-remote-api 同名 |
| `scratch/2026-10-18-rc1-work-scratch/` | 凍結の前の着手の結果、exact identity、testのPASSと未検証の境界 | scratch-editor 同名 |
| `scratch/2026-10-19-rc1-release-scratch-tooling/` | toolingとScratchの公開時の照合、凍結したOCIをCLIでそのまま昇格させたこと、registryの匿名の読み取り、OCIのconfig／layer／mtimeの確認、照合のscript | scratch-editor 同名 |

McRemoteの9 file（22,870 bytes）は搬送元の一覧（McRemote `handoff-materials/2026-10-19-rc1-close/materials/classification_ja.md`）、
Pythonの10 file（13,180 bytes）は搬送元の一覧（minecraft-remote-api `handoff-materials/2026-10-19-rc1-python-release/MANIFEST_ja.md`の
close分類の節）、Scratchの15 file（45,476 bytes）は搬送元の一覧（scratch-editor
`handoff-materials/2026-10-19-rc1-close-inventory/materials/EVIDENCE_FILES.tsv`）のbytesとSHA-256で照合した（不一致0）。収容の後、
coordinatorがprivate address、ホスト名、home directoryのpath、token、ペアコード、UUIDの定型を点検した。当たったのはGHCRの公開の
locator（`ghcr.io/naohiro2g/…`）だけだった。Pythonは`2026-10-19-rc1-python-close/`と別のrecordを案にしたが、b10と同じく一つの
gate closeの置き場所にまとめた。Scratchのscriptの中の`/tmp/`のpathは当時の実行場所で、収容した先から動かす入口ではない。

## 分類

| 担当 | ① | ② | ③ |
| --- | --- | --- | --- |
| McRemote | 2 directoryから9 file | 対応版の拡張のparkの原票（2 file。hub NOTES 2026-10-17のpark）、隔離pulseのone-off runner（初回stableのcloseまで）、close返却packet | 31 file（公開assetや公開のverification recordと同じ中身であることを担当が照合） |
| Python | 2 directoryから10 file | なし | 7 file（wheel、sdist、CIの一時容器など。公開物と同じbytes） |
| Scratch | 2 directory（15 file） | `2026-10-17-scratch-reference-versions`（次の版別snapshotの検収）、`2026-10-18-rc1-scratch-confirmation`（初回stableの後のpickerのaliasと入門の導線の設計入力）、close返却packet | 0 |

- toolingのcheckoutに`handoff-materials`は無い。toolingの公開の照合はScratchの`2026-10-19-rc1-release-scratch-tooling`にある
- Scratchのブロック一覧のrc1の`blocks.json`の`sourceCommit`は`09c59cbdfab650f9e0368ff18f0656728e5d00ea`（生成のときに指定したref）で、
  tagの`ec79b3b`と違う。generatorが照合する範囲の差分は空で、ブロックの中身は変わっていない（Scratch担当の説明、
  `handoff-materials/2026-10-19-rc1-close-inventory/materials/REFERENCE_SOURCE_ja.md`）。knowledgeの`api/scratch/2321.0.0rc1/blocks.json`は
  Scratchの生成物と同じbytes
- ①の元は、この収容の照合の後に各担当が整理してよい。②は各担当の書いた用途と、捨ててよくなる条件のとおりに持つ
- Stackの返却（候補の置き場所の中身の削除と分類）は、この記録の時点でまだ
