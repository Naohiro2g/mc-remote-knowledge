# b9 Python公開 — 返却票（2026-10-05）

- 対象 repo: `Naohiro2g/minecraft-remote-api`
- release／channel: `2320.0.0b9`、protocol `23.2.0`。GitHub prerelease／TestPyPI／PyPI.org
- knowledge contract path: `00-hub/release-gate-notes_ja.md` b9節「release authorization」
- knowledge contract commit: `6df2d14033a4646ce958737c06849725fcaee51e`（実読。最新runtimeとINDEXも参照）
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: 公開。**GitHub／TestPyPI／PyPI.orgの公開・本体照合とPyPI exact-pin取得PASS**
- exact set／freeze: `b9-integrated-artifact-set-1`。公開したwheel／sdistは凍結値とbyte単位で一致
- authorized next action: 上記公開許可とuserのsdist訂正・再開指示。GitHub Releaseはprerelease ON、draft OFF、Latest非対象
- test class／evidence: `unit/deterministic`（CI）、公開artifactのread-only照合。素材は下記ファイル。正式record提案`14-evidence/records/2026-10-05-b9-python-release_ja.md`、artifact提案`14-evidence/artifacts/2026-10-05-b9-python-release/`。正式配置はknowledge側

## source／tag／CI

| 対象 | 結果 |
| --- | --- |
| main統合前 | `7981031765cfcc43acc23f03e86e97ba74bae494` |
| main統合後 | `b901c88fe41b67530ff353271683ece9fd453076`（fast-forward、push済み、provider照合） |
| 公開後の文書更新main | `39f2ec951b7cf0deb07bbfb7156faa26832372f4`（README・公開ガイド等5文書、push済み、provider照合） |
| tag | `v2320.0.0b9` → `b901c88fe41b67530ff353271683ece9fd453076`（provider照合） |
| main CI | run `37267655222`、success |
| tag指定CI | run `37267690375`、success。CIにtag push triggerは無いためtagをrefとしてdispatch |
| tag CI artifact | `11326019788`、archive 383,490 bytes／provider digest `55a5f4d0ee407698ef83eece1cdbc60ed82e58e59ff48c6d3166e7e4af9d399b` |
| 同梱WireScope source | `dc1ab834183e29f2eb03059b07e99d2b463776ee` |
| release workflow | [run 37267882665](https://github.com/Naohiro2g/minecraft-remote-api/actions/runs/37267882665) |

tag指定CIのwheel／sdistをdownloadし、凍結したcandidate本体とbyte単位で一致することを確認してからReleaseを公開した。
公開workflowのpromoteは再buildを行わず、tagのcommitに対応するCI成果物を昇格する。

## GitHub Release／assets

- [GitHub Release](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2320.0.0b9)、Release ID `403391933`
- title: `minecraft-remote-api 2320.0.0b9`
- prerelease `true`／draft `false`
- Latestは従来の`v1214.10.11`のまま
- 公開時刻: 2026-10-05 14:27:34 JST（05:27:34 UTC）

| Release asset | bytes | SHA-256 |
| --- | ---: | --- |
| `minecraft_remote_api-2320.0.0b9-py3-none-any.whl` | 196,221 | `e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6` |
| `minecraft_remote_api-2320.0.0b9.tar.gz` | 190,627 | `bd027b8b94ff775bfb7a3c02ada9716ad8785e5499180bb0cfb26f1da4afe479` |
| `manifest.json` | 681 | `da9887d12e57d929a93531bbcffc7795895aa0bbc7eef1792e2d03cb4979e838` |

3 assetsとも匿名downloadした本体のbytes／SHA-256をprovider情報と照合しPASS。
manifestの`source_commit`、`release_tag`、`bundled_wirescope_source_commit`と2 artifactsのhashも一致。
CIから公開manifestへは`release_tag`だけが変更された。

WindowsなどGitなし導入用のRelease wheel URL:

[minecraft_remote_api-2320.0.0b9-py3-none-any.whl](https://github.com/Naohiro2g/minecraft-remote-api/releases/download/v2320.0.0b9/minecraft_remote_api-2320.0.0b9-py3-none-any.whl)

## TestPyPI／PyPI.org

- TestPyPI: 固定triggerの`publish-testpypi` success。公開JSON metadataと、実downloadしたwheel／sdistが上記凍結bytes／SHA-256と一致。両fileともnot yanked
- [TestPyPI b9](https://test.pypi.org/project/minecraft-remote-api/2320.0.0b9/)
- [PyPI.org b9](https://pypi.org/project/minecraft-remote-api/2320.0.0b9/): `publish-pypi` success。公開JSON metadataと実downloadしたwheel／sdistのbytes／SHA-256は上記凍結値と一致、両fileともnot yanked
- 設定照合: repository variable `PYPI_PUBLISH_ENABLED=true`、required reviewer `Naohiro2g`、prevent_self_review false、admin bypass false、deploymentはtag `v*`のみ
- human ownerがGitHub上で承認し、「The deployments have been approved」の画面をsessionへ提示。agentはenvironmentの承認を代行していない。release workflowは全4 jobがsuccess
- PyPIへのupload: wheelは2026-10-05 14:34:11 JST、sdistは14:34:12 JST（PyPI metadataのupload-time）
- Linux／Python 3.13.13／uv 0.12.19のfresh projectでPyPI.orgからexact-pin取得PASS。専用の空cacheを使用。registryは`https://pypi.org/simple`、lockの2 artifactsのhash／sizeは上表と一致
- `from mc_remote import Minecraft`とversion確認の出力は`2320.0.0b9`／`Minecraft`。import元もfresh venvのsite-packagesと確認。server接続は行っていない
- Windowsでb9を取得・接続した結果は含めない。先に通したWindows 11のB8 wheel入口検証とは別のLinux検証

実行した取得・import手順:

```bash
uv init --python 3.13 mc-pypi-check
cd mc-pypi-check
uv add "minecraft-remote-api==2320.0.0b9"
uv run python -c "from mc_remote import Minecraft; from importlib.metadata import version; print(version('minecraft-remote-api')); print(Minecraft.__name__)"
```

実試験では既存Python 3.13.13を指定し、取得元を明示する`--default-index https://pypi.org/simple --no-sources`も指定した。
そのprojectの`pyproject.toml`／`uv.lock`と要約を素材へ保存した。

## 公開後のREADME・文書追従

- commit: `39f2ec951b7cf0deb07bbfb7156faa26832372f4`。公開source `b901c88`の直後の文書専用commit
- README: 取得先をPyPIのb9 exact-pinへ変更、未公開・準備中の説明を更新
- PUBLISHING／PyPIガイド: 公開状態、実際のenvironment保護、human承認の手順、tag-only policyに適合するdispatch refを記述
- 更新・復帰ガイド: PyPIの版指定更新を追加
- release records: 公開CI、source／tag、artifact digest、取得確認を記録
- local確認: `git diff --check`、16 relative links／anchors、公開版の導入・tag dispatch記述PASS
- 公開後文書CI: run `37269202169`、success（Python 3.10〜3.13とbuild）。provider照合済み
- 文書更新後もtagは`b901c88`。公開wheel／sdist／manifestは差し替えていない

## 素材／残る作業

- `tag-ci-verification.json`／`tag-ci-manifest.json`: 公開前のCI本体照合
- `release-verification.json`／`release-manifest.json`: 公開Releaseの匿名download・provider照合
- `testpypi-verification.json`: TestPyPIの公開metadata／本体照合
- `pypi-verification.json`: PyPI.orgの公開metadata／本体照合
- `pypi-entry-check.json`／`pypi-entry-check.pyproject.toml`／`pypi-entry-check.uv.lock`: fresh uv projectでのexact-pin・import確認
- `verify_publication.py`: 実際に使用したread-only検証script
- `release-notes_ja.md`: 公開したRelease本文
- `authorization-preflight_ja.md`／`preflight.json`: 公開前の誤記停止と公開進行のcheckpoint
- sdist略記誤りは訂正commitで解消し、凍結artifactのidentityは不変
- userが編集中の`examples/hello.py`／`param_mc_remote.py`／`particle_graph.py`はstageせず保持
- 残る作業: knowledgeへの正式evidence収容・結果採用依頼、横断gate close。TestPyPIを後続版で手動に絞る変更は後続へ引き継ぐ（b9 tagの固定workflowは公開指示どおり自動のまま）
- server変更、他repoの実装、他repoの公開操作は行っていない。横断gate closeはcoordinatorの担当
