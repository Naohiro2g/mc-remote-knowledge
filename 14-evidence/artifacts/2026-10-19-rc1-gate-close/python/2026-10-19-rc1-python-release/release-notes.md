# minecraft-remote-api 2321.0.0rc1

マイクラリモコンのPythonクライアントのリリース候補です。Protocol **23.2.1** に対応します。
Protocol 23.2.0のサーバー／クライアントとの混在接続は、rc1の試験で確認済みです。

このReleaseは、合格したrc1 candidateのwheel／sdistを再ビルドせず、そのまま公開します。
PyPI.orgへの公開は、coordinatorによるRelease assetの照合後、human ownerが承認してから行います。

## WireScopeを使うときの注意（`wirescope=True`）

WireScopeの配信はPythonプロセスの中で動くため、Pythonプロセスが終了すると配信も止まります。
短いスクリプトではブラウザがページを読み込む前に終了し、白いページになることがあります。
また、ブラウザがWireScopeへ接続する前に送った操作の命令は表示されません。

観測するときは、`Minecraft.create(...)`の直後に`input()`などで待ち、ブラウザでWireScopeの接続コードを入力します。
処理の最後も、観察が終わるまで`input()`などで待ってください。

```python
from mc_remote import Minecraft

with Minecraft.create(wirescope=True) as mc:
    input("WireScopeで接続コードを入力し、接続できたらEnter: ")

    mc.postToChat("Hello, WireScope!")
    # 観測したい処理をここに書く

    input("観察を終えたらEnterで終了: ")
```

観測の開始と終了、接続状態の詳細表示・公開APIの改善は、Python／Scratch／toolingの共通課題として記録済みです。
初回stable（latest）の公開後に優先して検討します。

## フィードバック

利用環境、再現手順、期待した結果と実際の結果を、[フィードバックフォーム](https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml)へお寄せください。

## 配布物の照合

| ファイル | bytes | SHA-256 |
| --- | ---: | --- |
| `minecraft_remote_api-2321.0.0rc1-py3-none-any.whl` | 196,098 | `5f12dfcf4953bfaf5dcbe649d4a1ca2d3f5f4b5307b9896e79284478216944ca` |
| `minecraft_remote_api-2321.0.0rc1.tar.gz` | 190,285 | `dc8d9f30f538c14cfa04260c92f32e8f451748b99a8e596aeb3e59b1968e5611` |

同梱WireScopeのsourceは `Naohiro2g/minecraft-remote-tooling@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666` です。
