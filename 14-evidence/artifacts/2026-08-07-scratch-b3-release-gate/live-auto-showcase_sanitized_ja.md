# b3 candidate showcase — sanitized live-auto summary

- test class: `live-auto`
- Scratch candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- local test surface: loopback HTTP temporary fixture

## Artifact生成

1. `MCREMOTE_SHOWCASE=true`でscratch-gui dev buildを生成した。
2. `node scripts/prune-pages-artifact.mjs build`を実行した。
3. `node scripts/write-showcase-runtime-config.mjs build 3f1a10a366bfbe76e32b5a31c54da19eddd56e56`を実行した。
4. 公開entryは`index.html`のみ。`blocks-only.html`、`compatibility-testing.html`、`player.html`、`standalone.html`と各bundleをartifactから除外した。
5. runtime configは`connection_enabled=false`、release identityはcandidate SHAと一致し、showcase noticeを先頭に持った。

## HTTP matrix

- 200: `/`、`/index.html`、`/mc-remote-runtime-config.json`
- 404: `/blocks-only.html`、`/blocksonly.js`
- 404: `/compatibility-testing.html`、`/compatibilitytesting.js`
- 404: `/player.html`、`/player.js`
- 404: `/standalone.html`、`/guistandalone.js`

## Browser smoke

`live-auto-showcase-smoke.cjs`をheadless Chromiumで実行した。in-app Browserは環境の信頼境界で利用不能だったため、このfallbackを使用した。

- showcase notice heading／body: PASS
- McRemote connect blockの存在: PASS
- built page内の登録済み`mcremote_connect` primitive実行: reason `connection_disabled`
- built VM runtime config: `connectionEnabled=false`
- release identity: candidate SHA一致
- WebSocket生成数: 0

## 判定

showcase artifactは公開される全entryで二重fail-closeを維持した。通常版のruntime config／Bridge／Sandbox接続をshowcase artifactへ持ち込んでいない。

## Redaction

token、pair code、pairing ID、private host、player UUIDは使用・記録していない。
