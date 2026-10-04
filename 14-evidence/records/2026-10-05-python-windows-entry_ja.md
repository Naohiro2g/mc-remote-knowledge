# Python Windows入口：クリーンなWindows 11からのクイックスタート

> status: 入口ルートは成功（human ownerの報告）。PyPIの遷移ゲート④で残っていたWindowsの材料。mature判定は未実施（human ownerが行う）。

## Record

- test ID: `2026-10-05-python-windows-entry`
- test class: `live-human`（human ownerが実施し報告。agentはWindowsを操作していない）
- observed date: 2026-10-05 JST（実施時刻とWindowsのbuild番号は未記録）
- result: **PASS**（報告ベース）
- 対象: Windows 11のクリーンインストールから、Gitを入れずにuv → Python 3.13のproject → b8 Release wheelのURL →
  import → JupyterLabへ進む入口ルート
- 手順: Python repo `main@7981031765cfcc43acc23f03e86e97ba74bae494`の`docs/windows-b8-entry_ja.md`
- artifact: minecraft-remote-api `2320.0.0b8`（tag `v2320.0.0b8`→`52d35f5`）。Release wheel 195,068 bytes、SHA-256
  `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`（Python担当がGitHub APIで照合。Windows側でdigestは測っていない）
- uv: `0.12.23 (46b84fd0b 2026-10-03 x86_64-pc-windows-msvc)`
- decisions: `2026-09-26-03`、`2026-09-29-02`、versioning-design §10.9の遷移ゲート④
- 前の記録: [TestPyPI soak：遷移ゲート①〜④](2026-09-28-python-testpypi-soak-gates_ja.md)（④はWindowsを除いてPASS）
- 出典: Python担当の確定搬送票（2026-10-05、`main@7981031`）

## 観測

JupyterLabで次のセルを実行し、`2320.0.0b8`と`Minecraft`が出た。PowerShellの`uv pip show minecraft-remote-api`は
Version `2320.0.0b8`を示した。初回の転記で`Minecraft.name`となっていたのは、Discordを通したときにアンダースコアが
落ちたもので、実行したのは`Minecraft.__name__`である（human owner、2026-10-05）。

```python
from mc_remote import Minecraft
from importlib.metadata import version
print(version("minecraft-remote-api"))
print(Minecraft.__name__)
```

## 主張しない範囲

Minecraftサーバーへの接続、pairing、ゲーム内の描画とサウンド、PyPI.orgへの公開、mature判定。CLIのimport確認の個別出力、
全インストールログ、screenshotは添付されていない。

## Artifacts

報告原文と搬送票を全文のまま収録した。site-packagesのlocal pathはPython担当が`<local-site-packages>`へ置き換えている。
coordinatorが全文を読み、搬送元のMANIFESTのSHA-256と一致することを照合した（2026-10-05）。

| file | 内容 | SHA-256 |
| --- | --- | --- |
| [windows-user-report_ja.md](../artifacts/2026-10-05-python-windows-entry/windows-user-report_ja.md) | human ownerの報告（Notebookのセル、出力、package情報、転記の補足） | `21c3376f5384658fb9fcee2dbd7dfc57263fe9fcf76a996096ddbcf165a24fff` |
| [handoff_ja.md](../artifacts/2026-10-05-python-windows-entry/handoff_ja.md) | Python担当の確定搬送票 | `68379f4e962021bdfb920ec43c90cfb0df0e276599530105f6278850d4feadb8` |
