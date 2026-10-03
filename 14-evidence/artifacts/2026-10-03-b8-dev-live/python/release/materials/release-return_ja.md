## Release gate 確認票 — b8 Python公開の返却

- 対象 repo: `Naohiro2g/minecraft-remote-api`
- 対象 branch/commit: `main@52d35f5304e62f465c1f47ab47c00fe9bcf62470`。candidate branch `codex/b8-python-entity-particle` は同じcommitで保持。
- release / channel: `v2320.0.0b8`／GitHub prerelease公開、TestPyPI soak公開。
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: **Pythonの公開処理・公開後照合完了**。横断gate closeとWindows実機検証はcoordinatorへ戻す。
- contract maturity / required test tier: gate result GREENとexact set凍結をknowledge記録で確認。Tier3のPASSを再利用し、今回の公開ではsource／CI／public artifact／provider状態を照合。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`（2026-09-30のb8節、release authorization）、`00-hub/release-operations-responsibility-design_ja.md`（component実行境界／公開／close）、`12-python-client/pypi-soak-uv-readme-instructions_ja.md`。ローカルrunbookは`PUBLISHING.md`。
- knowledge contract commit: `fd7cad78564dd96ee91831d284abf1560fdf65b0`（remote mainからruntimeを取得し、実際に読んだSHA）。
- gate manifest identity: `b8-integrated-artifact-set-1`。
- change cone: 自repoのmain fast-forward、tag push、GitHub Release公開と固定trigger経由TestPyPI公開。package／protocol／frozen artifactの変更なし。他repo／shared環境の操作なし。
- reused PASS / rationale: 凍結source52d35f5とwheel／sdistが不変。b8実装・共有fixture・通常dev・human WireScopeの既存PASSをknowledgeのGREENに従って再利用。
- exact compatibility set / freeze status: `b8-integrated-artifact-set-1`（不変）。new main CIと公開Releaseのwheel／sdist bytes・SHAが凍結値に完全一致。同梱WireScope sourceは`df34849d2502a498a06c5fe07a91d03e925124eb`。
- target deployment / profile / lock: GitHub Release／TestPyPIだけを操作。MC serverの接続・配置・config変更なし。
- authorized next action: coordinatorの公開指示票とhuman ownerの承認に従い、手順1〜5をPython担当自身で実行済み。
- test class: `unit/deterministic`（artifact整合チェック）＋Git／provider APIでの公開状態照合。
- 実行した command / 手順: clean一時worktreeでmainを`70596ed5fc96d826d5107f2033354a59cccfc2e6`から`52d35f5304e62f465c1f47ab47c00fe9bcf62470`へ`git merge --ff-only`し、mainとtag `v2320.0.0b8`をpush。新main CIのartifactを取得・凍結bytes照合後、REST APIでprerelease=true／draft=false／make_latest=falseのReleaseを作成。固定`release.yml`のpromote／publish-testpypi完了を確認し、公開asset実downloadとTestPyPI公式JSONを照合。Windows用public wheel URLも匿名downloadで検証。
- 結果: **公開・照合PASS**。main commitとtag targetはともに`52d35f5304e62f465c1f47ab47c00fe9bcf62470`。CIのPython3.10〜3.13とbuild-candidate全success。Release workflowのpromoteとTrusted Publishing job全success。GitHub prerelease ON、draft OFF、title指定どおり。Latestは以前と同じ`v1214.10.11`。
- evidence record / artifact: 本repoのGit外`handoff-materials/2026-10-03-b8-python-release/`へ下記素材を保存。正式evidence authoringはknowledge担当。公開Release asset／GitHub API／TestPyPI公式JSONを一次根拠とする。
- 未検証の境界: Windows 11クリーンインストールからの導入はhuman owner側で公開直後に実施する。匿名wheel URL取得はPASSだが、Windows実機のimport／JupyterのPASSとは主張しない。PyPI.org公開とmature判定、public MC deploy、追加のlive試験はこの指示の範囲外。
- security / compatibility / rollback の確認: userが変更した`examples/param_mc_remote.py`と`examples/particle_graph.py`の内容は開始時のfingerprintと一致し、commitせず保持。clean worktreeからだけ統合・公開。一時worktreeは正常に削除。token／private endpointを公開body・asset・返却票へ出力していない。rollback操作なし。
- 判定を求める事項: coordinatorが公開tag target、Release flags、manifest／artifact identityをread-only照合して横断gateをcloseしてほしい。Windows検証には下記の凍結Release wheel URLを使用する。

### 公開identity

- main commit: `52d35f5304e62f465c1f47ab47c00fe9bcf62470`
- tag: `v2320.0.0b8`
- tag target: `52d35f5304e62f465c1f47ab47c00fe9bcf62470`
- Release title: `minecraft-remote-api 2320.0.0b8`
- Release ID: `402437492`
- Release URL: https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2320.0.0b8
- prerelease: true／draft: false／Latest: false（Latest APIは`v1214.10.11`のまま）。
- new main CI: https://github.com/Naohiro2g/minecraft-remote-api/actions/runs/37113256520 （event=push、head_sha=tag target、全jobs成功）。ci.ymlはmain pushで発火するため、このtag targetと同一commitのCIを照合した。
- CI artifact: ID `11271101046`、`minecraft-remote-api-dist`。ZIP 381,099 bytes／SHA-256 `a42db0b07080631daa201f74579c1940131df1ab9ca09e6c65a8a60efbce30d5`。
- 固定Release workflow: https://github.com/Naohiro2g/minecraft-remote-api/actions/runs/37113530599 （event=release、head_branch=v2320.0.0b8、head_sha=52d35f5）。promote／publish-testpypiともsuccess。

### Release assets — 実downloadで照合

| asset | bytes | SHA-256 |
| --- | --- | --- |
| wheel | 195,068 | `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180` |
| sdist | 188,775 | `9d56d92b10936787e1eebc1cf85a521ea19aa2e57b391f474eb695b0ba3fad32` |
| manifest | 681 | `7aa2868f1d9fc75b414cb37ac8d0886d390691d7b169f060def99248e29d9fc0` |

- wheel filename: `minecraft_remote_api-2320.0.0b8-py3-none-any.whl`
- sdist filename: `minecraft_remote_api-2320.0.0b8.tar.gz`
- manifest filename: `manifest.json`
- wheel／sdistは凍結CI成果物と完全一致。公開manifestはcandidate manifestのrelease_tag=nullをv2320.0.0b8へ置換した681 bytesのもの。
- manifestのsource_commitは52d35f5304e62f465c1f47ab47c00fe9bcf62470、bundled_wirescope_source_commitはdf34849d2502a498a06c5fe07a91d03e925124eb。wheel／sdistのrole／kind／file／sha256も照合済み。

### TestPyPI

- 結果: **PASS（Trusted Publishing）**。固定triggerのpublish-testpypi jobがsuccess。
- 公開URL: https://test.pypi.org/project/minecraft-remote-api/2320.0.0b8/
- 公式JSON: https://test.pypi.org/pypi/minecraft-remote-api/2320.0.0b8/json
- version=2320.0.0b8、wheel／sdistの2 fileがGitHub Releaseと同じbytes／SHA-256。両fileともyanked=false。
- PyPI.orgへのupload、yank／unyank、mature判定は実施していない。

### Windows検証用のRelease wheel

https://github.com/Naohiro2g/minecraft-remote-api/releases/download/v2320.0.0b8/minecraft_remote_api-2320.0.0b8-py3-none-any.whl

GitHub認証なしのURL取得で195,068 bytes／凍結SHA dcedff01…0180を確認済み。人間は次のcommandを入口手順のuv init後に実行できる。

```powershell
uv add https://github.com/Naohiro2g/minecraft-remote-api/releases/download/v2320.0.0b8/minecraft_remote_api-2320.0.0b8-py3-none-any.whl
```

手順: https://github.com/Naohiro2g/minecraft-remote-api/blob/v2320.0.0b8/docs/windows-b8-entry_ja.md

### 保存素材・引継ぎ

- `materials/github-final.json`: main／tag／Release assets／Latest／固定workflow jobのGitHub API最終snapshot。
- `materials/ci-37113256520.zip`、`materials/ci-37113256520/`: 公開前に照合したCI bytes。
- `materials/release-assets/`: 公開wheel／sdist／manifestの実download。
- `materials/testpypi-2320.0.0b8.json`: TestPyPI公式JSON取得原本。
- `materials/windows-wheel-anonymous.whl`: Windows入口URLの匿名取得bytes。
- `materials/verify_candidate.py`: 凍結candidate bytesとの公開前照合script。
- `materials/release-request.json`: title／flagsを明示した公開request（credentialなし）。
- `materials/handoff-inventory_ja.md`: 全handoff directoryの引継ぎ先、参照MANIFEST、次の一手。非参照確認なしに素材を削除していない。
- `materials/state.json`はローカルpreservation用fingerprintを含むため公開搬送対象から外す。正式evidence着地後の照合・cleanupを、knowledge担当とPython後続sessionへ移管する。
