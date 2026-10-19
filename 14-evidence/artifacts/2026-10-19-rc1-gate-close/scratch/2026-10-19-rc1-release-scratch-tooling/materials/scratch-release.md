protocol 23.2.1 の rc1 です。23.2.0 の server／client とも接続できることを試験で確認しています。

human owner が合格と判断した `rc1-integrated-artifact-set-1` の ZIP と OCI を、再ビルドせず公開しています。
Scratch source: `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`。develop には README 追補の `f20e55eb53f192eab6cdc4f0d5aae4f52b2dc8db` まで含まれますが、この tag は試験した source に固定しています。
候補生成: Actions run [39072595749](https://github.com/Naohiro2g/scratch-editor/actions/runs/39072595749)、artifact ID `12116296168`。
共通 tooling: [v2321.0.0rc1](https://github.com/Naohiro2g/minecraft-remote-tooling/releases/tag/v2321.0.0rc1)、source `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`。

Scratch LANパッケージは、お使いのOSのZIPを選んでください。使い始める手順は [Scratch LANパッケージの案内](https://mc-remote.com/lan/scratch/) にあります。展開した `mc-remote-scratch-LAN/` を `HOME/mc-remote/`（ホームフォルダー内の `mc-remote`）へ置き、版のフォルダー内の `はじめに.html` を開いてください。新しい `2321.0.0rc1` フォルダーは、前の版のフォルダーの隣に置けます。

Windows では、ZIPを展開する前にファイルのプロパティの「許可する」にチェックしてから展開してください。

| ファイル | bytes | SHA-256 |
| --- | ---: | --- |
| wirescope-app.zip | 83854 | da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad |
| wirescope-app.manifest.json | 2339 | 3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235 |
| mc-remote-scratch-LAN-2321.0.0rc1-windows-x64.zip | 261848009 | 86bbaf9a278683315ffe2ebd4f19d56ba53f5501289e4cddfc22f284d8d4e209 |
| mc-remote-scratch-LAN-2321.0.0rc1-macos-arm64.zip | 266199673 | bdfff47b8c1210a359ed65a8be6fca26624546e3c04add125063968acc091412 |
| mc-remote-scratch-LAN-2321.0.0rc1-linux-x64.zip | 271455727 | b76b574803c58403e38438d2569917bd72ca95f039026f12ed3a294edfcfba54 |
| scratch-gui.tar.gz | 138835708 | 2dafb257c511989946da021591191cc1501e0d1a9211cc559373ed7de30f19c2 |
| contracts.tar.gz | 1908 | 48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390 |
| manifest.json | 2320 | 776e0d51a8d8db14cb5ace23f2a41f9d6a56e7eacb0a51e88463bd6bf076c68c |

OCI は、凍結した archive を digest を維持して registry へ転送しています（linux/amd64、linux/arm64）。provenance と SBOM も含め、凍結 index と同じです。

- Scratch: `ghcr.io/naohiro2g/mc-remote-scratch:v2321.0.0rc1`、index `sha256:75e76edb6b8a1de4fb896184b5c26bed7cb1791296f82903e6b1ec4a1a5ab840`。
- Bridge: `ghcr.io/naohiro2g/mc-remote-bridge:v2321.0.0rc1`、index `sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`。

Scratch OCI の version label は両architectureとも `v2321.0.0rc1`。今回の公開は凍結OCIの直接転送のため、作成時刻・履歴・COPY layerのmtimeも凍結物と同一です。COPY入力のmtimeを一定値に正規化する変更は加えていません。

使ってみた結果や困ったことは、[feedback](https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml)へお寄せください。
