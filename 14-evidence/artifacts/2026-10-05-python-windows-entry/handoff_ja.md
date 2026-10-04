## 確定搬送票

- 搬送元 repo: `Naohiro2g/minecraft-remote-api`
- 搬送元 surface: Windows 11のGitなし導入・Jupyter入口検証
- 搬送元 branch/commit: `main@7981031765cfcc43acc23f03e86e97ba74bae494`。手順の成功報告を受領し、利用者向け文書3件をローカル更新（未commit／未push）。
- 作成日: 2026-10-05
- 種別: その他（live-human検証結果の報告）
- 決定: human ownerからWindows入口ルートの成功報告を受領した。b9で必要なPyPI遷移ゲート④のWindows検証材料として返す。
- 理由: b7.post3のsoak記録で未検証だったWindows入口の結果を、b9のmature判断材料へ追加するため。
- 却下案（3件まで）: なし。
- 影響: Python b9確認票の「Windows④の結果未受領」を、2026-10-05の成功報告受領で更新する。b8公開物・tag・APIは変更しない。
- 根拠/検証: test class `live-human`（人間実施・報告ベース）。Windows 11、uv `0.12.23 (46b84fd0b 2026-10-03 x86_64-pc-windows-msvc)`。人間はクリーンインストールからのGitなし手順全体を「問題なく成功」と報告した。Jupyterの短いimportとpackage版表示、PowerShellのpackage metadataを添付。追記で `Minecraft.__name__` を実行したことを確認。詳細とDiscord転記の補足は同directoryの `windows-user-report_ja.md`。
- 既に変更した実装/文書: `docs/windows-b8-entry_ja.md`、`docs/b8-python_ja.md`、`docs/release-records_ja.md` へ、Windows入口の成功報告と検証範囲を反映。実装変更なし。
- ナレッジ着地希望: `14-evidence/records/2026-10-05-python-windows-entry_ja.md` と `14-evidence/artifacts/2026-10-05-python-windows-entry/`（命名提案。正式authoringはknowledge側）。b9 gateのWindows④の材料とsoak指示の残件を更新してほしい。
- 捕捉 cleanup: `handoff-materials/2026-10-05-python-windows-entry/` は分類①・knowledge正式evidenceへの移管待ち。全文／SHA照合とcoordinatorの移管確認まで保持する。
- 着地後の確認戻り先: このPython session。knowledge commitと着地pathを返してほしい。

### 参照contractと対象identity

- knowledge contract commit: `ceba53099fa001fea6b83d68deadc1eb9e0038fe`（remote main照合、runtime読取済み。以下の関連規定を同SHAで読んだ）。
- knowledge contract path: `12-python-client/pypi-soak-uv-readme-instructions_ja.md`、`10-protocol/versioning-design_ja.md` §10.9。
- 対象Release: `v2320.0.0b8`、package source `52d35f5304e62f465c1f47ab47c00fe9bcf62470`。
- 指定wheel URL: https://github.com/Naohiro2g/minecraft-remote-api/releases/download/v2320.0.0b8/minecraft_remote_api-2320.0.0b8-py3-none-any.whl
- Release assetのprovider identity: 195,068 bytes、SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`（GitHub APIで再照合）。Windows側でdigestを測ったとの報告はない。
- 既存soak record: `14-evidence/records/2026-09-28-python-testpypi-soak-gates_ja.md`。

### 転記の補足と検証範囲

初回のNotebook貼り付けは `print(Minecraft.name)` だったが、human ownerが2026-10-05の追記で、
実際には `print(Minecraft.__name__)` を実行したと確認した。アンダースコアはDiscord経由の転記で落ちたもの。
実行内容は元手順と一致し、この表記差は解決済み。
手順全体の成功はhuman ownerの報告であり、agentがWindows端末を操作した結果ではない。

本票はWindows入口の報告だけを返す。mature判定・横断gateの判定、PyPI.org公開、Windows上のMinecraft接続・ゲーム内操作のPASSは主張しない。
