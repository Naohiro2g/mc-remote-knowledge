## 確定搬送票

- 搬送元 repo: minecraft-remote-api
- 搬送元 surface: Codex
- 搬送元 branch/commit: `codex/b8-python-entity-particle` / base `70596ed5fc96d826d5107f2033354a59cccfc2e6`、未commit／未pushの実装差分
- 作成日: 2026-09-30
- 種別: 局所決定（Python投影）＋実装状況
- 決定: protocol `23.2.0`／package `2320.0.0b8`でSSOTのB8 contractを投影。`getNearbyEntities()`はserver順のimmutable `NearbyEntity` tuple、`getEntityPose()`／`setEntityPose()`はplayer poseと同形dict、`removeEntity()`はnull成功を検証する。`spawnParticle()`は既存文字列またはtyped `ParticleSpec` dictを受け、省略／null／forceを保つ。ID／data／receiverの意味検証とerror priorityはserverに委ねる。自動retry・handle registry・filter／workのclient再実装を追加しない。
- 理由: 既存のentity direction naming、snapshot projectionと薄いwire投影に揃え、serverの状態とエラーをそのまま観察できるようにする。
- 却下案: なし
- 影響: Python公開surface、Python observer source、同梱WireScope app、B8 API例と3D graph sample。wire contractの改訂はない。
- 根拠/検証: `unit/deterministic`。全Python `uv --cache-dir /tmp/mcr-b8-uv-cache run --offline --no-sync --with pytest pytest -q` 442/442 PASS（loopback socketのためsandbox外）。owner fixture投影 54/54 PASS。共通app owner sourceの `npm exec --workspace=@mc-remote/live -- vitest run test/observer.test.ts` 28/28 PASS。Python生成のB8 fixture snapshot 26 frameを同sourceのproduction `parseObserverSnapshot` が受理。`uv lock --offline --check`、PEP 517 build、wheel integrity／license／RECORD、diff check PASS。追補：同梱appのB8四method文字列確認1/1、B7 browser regression harnessの現行app load PASS。
- 既に変更した実装/文書: `mc_remote/minecraft.py`、`entity_value.py`、`particle_value.py`、`observer.py`、app ZIP／manifestとpin、pyproject／uv.lock、B8共有fixture／source metadata、対象tests、README／`docs/b8-python_ja.md`／`examples/particle_graph.py`。
- ナレッジ着地希望: `12-python-client/python-client-guide_ja.md` へPython surface候補行とcomponent検証範囲。横断gate確定はcoordinatorが別途行う。
- 捕捉 cleanup: commit／push後にidentity更新→knowledgeへの搬送→着地確認後にこのhandoffを整理。正式live evidenceは作成していない。
- 着地後の確認戻り先: このrepoのB8 Python担当

### Ownerとartifact identity

- fixture owner: `Naohiro2g/scratch-editor@0735a9c957d069f719bee9c91e8be0f9322f4920` / `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`
- fixture: SHA-256 `09c1565bf81d33c92d6282e6e20d926559168cb9d780c07d30ad2f9f5895640e`。59 case inventoryを保持。N19とH03〜H07はserver arithmetic／transaction専用でPython側の実処理PASSを主張しない。他のnearby caseもPython params／result／errorの投影だけを検証し、sphere検索の結果をclientで算出しない。
- common WireScope source: `Naohiro2g/scratch-editor@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`。read-onlyの使い捨てcloneからNode `24.19.0`とowner lockでbuild。sourceのfixture bytesとPython配置を照合済み。
- common ZIP: 81,222 bytes / SHA-256 `870c5bf33c7af5fe720fde0514a3192865dfc1057707bbbba405bbf238642a15`
- common manifest: 2,321 bytes / SHA-256 `fb4db540cedde45eb7a4ad2fa56cfe387352ce6f99203663d0db788f2b38b8aa`

### ローカル未公開build（最終PEP 517）

- `minecraft_remote_api-2320.0.0b8-py3-none-any.whl`: 190183 bytes / SHA-256 `6a881688effc5647b409ca6f48f2d3bb484b560a304218657d7ece23aab63f84`
- `minecraft_remote_api-2320.0.0b8.tar.gz`: 183486 bytes / SHA-256 `669103442a3d10d2998874afd140b03bbc41fa45362f875ed6e57538383ffdd4`

### 未主張

- 実plugin接続、2-player self配送、dust／blockの実描画、Paper 1.21.11／26.2、Windows。
- real-browser表示（browser接続機能をbootstrapできず未実施）。production validatorとのshape照合は実施済み。
- shared deploy、人間参加試験、exact compatibility set、横断GREEN、正式evidence、tag／release、registry publish。
- commit／push済みsource identity。

## セッションクローズ票

- repo: minecraft-remote-api
- surface: Codex
- branch/commit: `codex/b8-python-entity-particle` / base `70596ed5fc96d826d5107f2033354a59cccfc2e6`、未commit／未push
- 作業範囲: B8 Python entity lifecycle／particle Stage 2／observer／shared fixture／bundled app／3D graph sample
- 今回やったこと: 上記component実装と決定論的検証、SSOTに基づくversion更新
- 変更ファイル: 上記の実装／文書／fixture／tests。詳細は `git status --short`
- 検証: Python 442/442、shared fixture投影54/54、common app対象28/28、snapshot26 frame、PEP 517 build／wheel check PASS
- 未完了: commit／push、live-auto／live-human、real-browser、Windows、横断gate／release
- 次に読むもの: 固定knowledgeのwire §5.8.3とcoordinatorのB8指示票・接続先・許可済み次操作
- 次の一手: 実装差分をreview／commit／pushし、coordinatorへcomponent identityとこの検証範囲を返す
- 未着地の搬送物: 本票（source identity未commit）。横断gate判定はしていない
- NOTES/DECISIONS: local `NOTES_ja.md` の2026-09-30行へ記録。knowledgeへの直接変更なし
- 注意点: 公開済みREADMEの導入URLはB7 post3のまま、B8は開発中。public／shared runtimeは変更していない
