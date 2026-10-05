# b9 Python公開 — 移管素材

- 分類: **① knowledgeの正式evidenceへ移す**
- 移す先の提案: `14-evidence/records/2026-10-05-b9-python-release_ja.md` と `14-evidence/artifacts/2026-10-05-b9-python-release/`
- 理由: 公開許可、tag CI照合、公開assetと両indexの照合、sdist誤記の訂正、PyPI exact-pin取得をrelease identityへ紐づけるため
- knowledge contract commit: `6df2d14033a4646ce958737c06849725fcaee51e`
- release source／tag: `b901c88fe41b67530ff353271683ece9fd453076`／`v2320.0.0b9`
- 公開後文書commit: `39f2ec951b7cf0deb07bbfb7156faa26832372f4`（main、push済み、CI success）
- GitHub／TestPyPI／PyPI.org公開と本体bytes・SHA照合、Linuxのfresh uv exact-pin取得・importはPASS
- 正式evidence配置はknowledge側。収容・照合確認まで削除しない
- private設定、token、artifact binaryは素材に収容しない
- verify_publication.pyのrelease/main一致検査は文書更新前のb901時点で実行済み。mainは文書専用commitへ進んだため、scriptを再実行する場合のmain一致条件は当時の検査条件として扱う

| File | bytes | SHA-256 |
| --- | ---: | --- |
| `materials/authorization-preflight_ja.md` | 1,699 | `95bdcb1154a249e195c8cf83c6a6fbde1589156f786df45714acf6ab5e8282c9` |
| `materials/preflight.json` | 2,071 | `866b3fc6e6cffff15e79e7b4fb396c056dc047f54e377b3f3e286c5995a8e0ad` |
| `materials/pypi-entry-check.json` | 680 | `e6967a42d29ae14d6e59b9398d50c48ca4aa3b2155c0ceedd540de2d43feff21` |
| `materials/pypi-entry-check.pyproject.toml` | 530 | `a68bf648b1cea7900bfeb8a73f7e49ff43e18502fa105c167416cedb45f241b4` |
| `materials/pypi-entry-check.uv.lock` | 1,048 | `f3a4f158c0c0e600a9e7df91ac368dd19cdde199cc75c8d943d6c46af3df6145` |
| `materials/pypi-verification.json` | 1,176 | `b9b6e3ae276c4759b69c0583af51df84caf408b7d3367c0a06403a7987b3719a` |
| `materials/release-manifest.json` | 681 | `da9887d12e57d929a93531bbcffc7795895aa0bbc7eef1792e2d03cb4979e838` |
| `materials/release-notes_ja.md` | 1,674 | `33e3795ecf661a64e9f287f8009a9b644d0efed0d1976b8f049b1ecc96288ed7` |
| `materials/release-return_ja.md` | 7,810 | `863af82f8b6d3487f9956f1ad693dfe11988cfccacc2f5595f5d7548209028b1` |
| `materials/release-verification.json` | 1,469 | `9c39a550838f91e5fce424c2e8d582f1a8c2e0e6776b5825297460345f08485e` |
| `materials/tag-ci-manifest.json` | 672 | `10b8e5cc102df5f53b0726a41df8b3f110656b1760cc0918e902684661645121` |
| `materials/tag-ci-verification.json` | 631 | `fffe0292e8485484d4edf120cfbd3e7d6558fdb4edc0b121bfeabdf22416ad83` |
| `materials/testpypi-verification.json` | 1,200 | `3c563a57ce61d1e0c456d89ca8235b8fdc9aa427f9842bca730b85b13eaaa05f` |
| `materials/verify_publication.py` | 4,684 | `9ede7a96d9a7525106987916e6f83977878a72f26ff418e0474772f672decfe3` |
