# Windows 11 Gitなし入口検証 — human ownerの報告

- 報告受領日: 2026-10-05（JST）。実施時刻とWindowsのbuild番号は未記録。
- 実施者: human owner（プロジェクトオーナー）。
- test class: live-human（人間実施の報告。agentによるWindows実機観測はない）。
- 結果: 手順全体を「問題なく成功」と報告。
- 対象: Windows 11のクリーンインストールから、Gitを入れずにuv、B8 Release wheel、import、JupyterLabへ進む入口ルート。
- 手順: Python repo `main@7981031765cfcc43acc23f03e86e97ba74bae494` の `docs/windows-b8-entry_ja.md`。
- package: `minecraft-remote-api==2320.0.0b8`。
- uv: `0.12.23 (46b84fd0b 2026-10-03 x86_64-pc-windows-msvc)`。
- 以下はユーザーの報告からlocal pathをredactしたもの。Notebookのコードは2026-10-05の追記で実行内容を確定し、初回転記との差を末尾に記録している。出力は報告のまま。

## 実行したNotebookセル（human ownerの追記で確定）

```python
from mc_remote import Minecraft
from importlib.metadata import version
print(version("minecraft-remote-api"))
print(Minecraft.__name__)
```

報告された出力:

```text
2320.0.0b8
Minecraft
```

## PowerShellで報告されたpackage情報

```text
uv pip show minecraft-remote-api
Name: minecraft-remote-api
Version: 2320.0.0b8
Location: <local-site-packages>
Requires:
Required-by: mc-b8-entry
```

## 記録の範囲と転記の補足

- ユーザーは案内した手順全体の成功を報告している。貼り付けにはuvの版、Notebookのimport／version／クラス名出力、PowerShellのpackage metadataがある。
- 初回貼り付けは `print(Minecraft.name)`。2026-10-05にhuman ownerから「`Minecraft.__name__` はDiscord経由でコピペしたので食われた。アンダースコア入りで実行している」と追記を受領した。実行したセルは上記の `print(Minecraft.__name__)` で確定し、元手順と一致する。初回の表記差はDiscord経由の転記によるもので、解決済み。
- CLIのimport確認コマンドの個別出力、全インストールログ、screenshot、Windows側のwheel SHA-256測定は添付されていない。
- Minecraftサーバーへの接続・pairing・ゲーム内描画／サウンドは今回の入口検証の主張に含めない。
- 本番PyPI publishとmature判断は今回の報告に含めない。
