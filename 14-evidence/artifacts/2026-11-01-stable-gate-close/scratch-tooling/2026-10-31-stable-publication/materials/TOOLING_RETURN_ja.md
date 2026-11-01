# tooling stable公開の返却（Scratchはcoordinator照合待ち）

- knowledge contract path：`00-hub/stable-gate-release-instructions_ja.md`「共通」「minecraft-remote-tooling」「Scratch editor」
- knowledge contract commit：`9dee6881a414a2b1fd4a37fa4fe26ddbedd9d8a5`
- 最新runtime／INDEX実読commit：`71786f5cd86edd66fc860dd0c855af3a5f91bb59`。公開依頼本文に変更がないことをcompare APIで確認。
- 公開日時：2026-11-01 00:05:53 JST（2026-10-31T15:05:53Z）
- Release：https://github.com/Naohiro2g/minecraft-remote-tooling/releases/tag/v2321.0.0
- Release ID：430004222、`prerelease=false`、`draft=false`。`/releases/latest`が同じIDを返すことを確認。
- main head／tag target：`6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`。mainを動かしていない。rc1 tagも同じcommitのまま。
- annotated tag object：`3186f47f63f44d9d28eee6ed1e6e3ec6afb573a8`
- 公開run ID：なし（GitHub API／CLIとregctlによる手動公開）。元のtooling候補runは39053886890、source一致・successをAPIで確認。今回build workflowを起動していない。

## Release asset

ローカルの実ファイルを再hash後にuploadし、GitHub providerのsize／digestが全件一致することを公開前後に確認した。
公開URLからの全fileの再downloadによる独立照合は、この返却では主張しない。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| bridge.oci.tar | 114626048 | `3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c` |
| wirescope-app.manifest.json | 2339 | `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235` |
| wirescope-app.zip | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |

全件、指示票の凍結値と一致。

## Bridge OCI

- 公開tag：`ghcr.io/naohiro2g/mc-remote-bridge:v2321.0.0`
- index：`sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`
- 既存の凍結indexを同じrepo内でregctl copyし、stable tagへ追加した。再buildとprovenanceの書換えはしていない。
- stable tagをregctl HEAD（require-list）で再取得し、index一致を確認した。

## Scratchの状態と次の操作

- `develop@bee41dc9629ee3225c19ef1d6be1299b6b4bf7d1`を保持。
- Scratchのstable tag／Release／registry tagは未作成。image workflowは今回まだ変更していない。
- 凍結候補の8添付fileとScratch OCIは準備・照合済み。
- **coordinatorによるtoolingの照合完了の連絡またはknowledgeへの明示記録を受けてから、Scratch公開へ進む。**
- これはtooling公開の事実返却であり、coordinatorの照合完了や横断gate判定を代行するものではない。
