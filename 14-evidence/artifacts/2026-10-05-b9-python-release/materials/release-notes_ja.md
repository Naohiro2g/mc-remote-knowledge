PythonからMinecraftへ接続するクライアントのb9公開版です。protocolは`23.2.0`、対応Minecraftは`1.21.11`です。

- 未知のevent typeを読み飛ばし、`pollEvents`のcursorとloss counterを保持します。`latest_sequence`と累積loss counterの逆行を検査し、接続epochの変更時に状態をリセットします。
- `postToChat`の成功応答`null`をPythonの`None`へ対応させています。
- 共有fixtureと同梱WireScopeの取得元を`minecraft-remote-tooling`へ移管しました。
- 更新・復帰の手順を追加し、クライアントAPI一覧のドラフトを更新しました。

PyPIから版を指定して導入できます。

```bash
uv add "minecraft-remote-api==2320.0.0b9"
```

利用手順は[README](https://github.com/Naohiro2g/minecraft-remote-api/blob/v2320.0.0b9/README.md)、公開面の一覧は[PythonクライアントAPI一覧（ドラフト）](https://github.com/Naohiro2g/minecraft-remote-api/blob/v2320.0.0b9/docs/python-api-reference_ja.md)を参照してください。

凍結set `b9-integrated-artifact-set-1`のPython sourceは`b901c88fe41b67530ff353271683ece9fd453076`です。同梱WireScope sourceは`dc1ab834183e29f2eb03059b07e99d2b463776ee`です。通常devでの代表往復とWireScope表示を確認しました。

| 成果物 | bytes | SHA-256 |
| --- | ---: | --- |
| wheel | 196,221 | `e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6` |
| sdist | 190,627 | `bd027b8b94ff775bfb7a3c02ada9716ad8785e5499180bb0cfb26f1da4afe479` |

固定workflowが、検証済みwheel／sdistと`manifest.json`を添付し、TestPyPIとPyPI.orgへ公開します。
