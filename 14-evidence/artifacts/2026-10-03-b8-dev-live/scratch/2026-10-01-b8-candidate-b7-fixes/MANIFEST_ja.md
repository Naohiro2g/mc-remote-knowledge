# B8更新candidate素材（B7是正3件を採用）

> 後継candidate: `691576f60b7f0824e1753bd6823901d01fbe2422`。
> 更新素材と確認票は `../2026-10-02-b8-candidate-local-fixes/`。この票はknowledgeのgate記録から参照される旧identityの照合用。

- 作成日: 2026-10-01
- source: `agent/b8-compatibility@df34849d2502a498a06c5fe07a91d03e925124eb`（push済み、git ls-remoteで一致確認）
- knowledge contract: `893cbfdbc5a480531d1a1ad7ae6f0fad8d36ef9f`
- 旧candidate: `dfcb03cf97fed998268b4714feb32d03a209f549`
- B8 fixture: `054a3af017f1abb8cc01cf85b3bc83181e648e19`版からbytes不変。36,481 bytes／111 case／SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`

- 空pollの履歴保持: `76f9e7d6384064faeef294843d702afde3017f64`
- server backpressureの案内分離: `b407ca9cfb4c5d77701d3b379f0b1dd23e4cf6cf`
- 入力欄の編集ショートカット: `df34849d2502a498a06c5fe07a91d03e925124eb`

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `scratch-image-inputs.tar.gz` | 152,885,920 | `2b3eda9a42c09f326b2139848322aa955fe19099a139cd6935c18c2d9e6be458` |
| `bridge-image-inputs.tar.gz` | 38,138 | `fd43f714c77d2bc184bf882460dfc05a1ce345dc6d4f5b52505a6a9d2850908f` |
| `wirescope-app.zip` | 83,746 | `4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07` |
| `wirescope-app.manifest.json` | 2,321 | `45d56d5012c2c0b21631597e160363d93bcf3e736b74cc0b8a1041afc8101413` |
| `contracts.tar.gz` | 1,908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |

GUI／Bridge tarはDocker imageの入力でありOCIではない。通常devの試験は開発端末で動かすため、今回registry／Release assetへの掲載は不要とのcoordinator指示。素材はローカル保存、正式evidenceではない。

## 再生成と検証

Node v24.19.0、既存のlock-installed workspaceを使用。npm ciは今回再実行していない。以下を新sourceで実行しPASS:

- node test/unit/extension_mcremote.js（scratch-vm）: 123 subtests／524 assertions
- npx jest test/unit/util/blockly-input-editing-shortcuts.test.js test/unit/util/vm-listener-hoc.test.jsx test/unit/util/mcremote-l10n.test.js test/unit/util/mcremote-wirescope-source.test.js --runInBand（scratch-gui）: 4 suites／41 tests
- npm test --workspace=@mc-remote/live: lint、13 files／142 tests
- npm run build --workspace=packages/scratch-vm
- npm run build --workspace=packages/scratch-gui（dev／dist／dist-standalone）
- npm run build --workspace=@mc-remote/bridge
- npm run build:artifact --workspace=@mc-remote/live -- --source-commit df34849d2502a498a06c5fe07a91d03e925124eb
- git diff --check

WireScope artifactはsandboxのgit spawnSync EPERM後、同じbuildコマンドをsandbox外で再実行して成功。VM／GUI lintとGUI i18n:srcは同じsource内容で採用前に実行済み（lint error 0）。今回追加のsource編集はしていない。

WireScope ZIPの全6 assetをmanifestのbytes／hashへ照合。ZIPは旧candidateと同一で、detached manifestは新しいsource commitを含むためhashが変わった。GUIのconfig schema versionは1、既定connection_enabledはfalse。

入力tarはtar --sort=name --mtime='UTC 1980-01-01' --owner=0 --group=0 --numeric-owner --mode='a+rX,u+w,go-w' と gzip -n で正規化。GUIはDockerfile.mc-remote＋build、BridgeはDockerfile＋package.json＋dist＋node_modules/ws、contractsはGUI contractsディレクトリを収録。

未実施: 実plugin接続、shared変更、人間参加試験、横断gate判定、tag／release公開、OCI生成。統一実施票は凍結後に受け取る。B8 source凍結後にfixture移管の棚卸しを再採取する。
