protocol 23.2.1 の rc1 です。23.2.0 の server／client とも接続できることを試験で確認しています。

human owner が合格と判断した `rc1-integrated-artifact-set-1` の生成物を、再ビルドせず公開しています。
source: `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`。
候補生成: Actions run [39053886890](https://github.com/Naohiro2g/minecraft-remote-tooling/actions/runs/39053886890)、artifact ID `12109060950`。

| ファイル | bytes | SHA-256 |
| --- | ---: | --- |
| wirescope-app.zip | 83854 | da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad |
| wirescope-app.manifest.json | 2339 | 3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235 |
| bridge.oci.tar | 114626048 | 3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c |

WireScope ZIP と detached manifest は対で使用してください。

Bridge: `ghcr.io/naohiro2g/mc-remote-bridge:v2321.0.0rc1`。
OCI index digest: `sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`（linux/amd64、linux/arm64）。凍結 archive を digest を維持して転送し、registry から取得した index の SHA-256 を照合しています。

共有fixtureは、この tag の `packages/protocol/test/fixtures/` にあります。旧版は履歴として保持しています。

| ファイル | bytes | SHA-256 |
| --- | ---: | --- |
| chat-event-compat-v23.2.1.json | 32384 | eead244a7340c315cb63e1e77ede0fe9cf48162c06fedbeef36d941950d5000d |
| entity-particle-v23.2.1.json | 36483 | 0319ff8373a96798cf5e9e421a804729fd33a0fa53e96adc12c93ed7994777ae |

使ってみた結果や困ったことは、[feedback](https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml)へお寄せください。
