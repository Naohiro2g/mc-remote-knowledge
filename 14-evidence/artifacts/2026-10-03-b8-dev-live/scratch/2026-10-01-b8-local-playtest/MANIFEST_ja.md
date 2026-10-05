# B8 ローカル動作確認の接続準備

- source: agent/b8-compatibility@df34849d2502a498a06c5fe07a91d03e925124eb
- knowledge参照: 49d5a59f50d357bfe7cd9c5401811a5e9e58eb59（runtime、INDEX、deployment-interface-design、wirescope-deployment-design）
- human ownerはローカルMCサーバーを新プラグインで起動済みと報告。接続先は127.0.0.1:25575を確認。
- Scratch: http://127.0.0.1:8601/?extension=mcremote
- Bridge: ws://127.0.0.1:8602/ → 127.0.0.1:25575
- WireScope: http://127.0.0.1:4173/（Scratchで接続後、WireScope miniから開く）
- 8080は既存listenerがあるため変更せず、Bridgeには8602を使用。

## 起動中の実行session

- Scratch webpack dev server: 43600
- Bridge: 46907
- WireScope preview: 61915

GUIはstart-scratch.cjsがruntime-config.jsonをmiddlewareで返し、追跡済みstatic configとcandidate素材は変更しない。GUI sourceの変更はdev serverが反映する。VM sourceを修正した場合はnpm run build --workspace=packages/scratch-vm後にブラウザを再読み込みする。

## 再起動

リポジトリrootから、それぞれ別のterminalで実行:

```sh
node handoff-materials/2026-10-01-b8-local-playtest/start-scratch.cjs
```

```sh
BRIDGE_WS_HOST=127.0.0.1 BRIDGE_WS_PORT=8602 BRIDGE_ORIGIN_ALLOWLIST=http://127.0.0.1:8601,http://localhost:8601 BRIDGE_SANDBOX_ALLOWLIST=127.0.0.1 BRIDGE_DEFAULT_SANDBOX=127.0.0.1 BRIDGE_SANDBOX_PORT=25575 node mc-remote/bridge/dist/main.js
```

```sh
npm run preview --workspace=@mc-remote/live -- --host 127.0.0.1 --port 4173 --strictPort
```

## 確認

BridgeへScratchと同じsubprotocolでhelloを送信し、McRemoteから-32000／auth_requiredを受信。独立ChromeでScratch B8の表示と接続可能なruntime config、WireScopeの未attach画面を確認。内蔵browserはnative接続を確立できず、独立Playwright＋Chromeで確認した。

この準備ではペアリング、world操作、shared環境変更を実行していない。正式な横断gate／人間参加試験の根拠ではない。ユーザーはScratchの接続するブロックを実行し、表示される/mcremote pairコマンドをMinecraft内で入力してからWireScope miniから独立画面を開く。

## human ownerの接続確認（2026-10-01）

ユーザーが認証成功とWireScope表示成功を報告。貼付のsanitized frameでは最初のhelloがtoken_not_found、その後のhelloが成功し、protocol 23.2.0／mc_version 1.21.11／dimension minecraft:overworld／origin [200,0,200]／world_constants.y_sea 62を確認。本人の操作と観測によるローカル試運転の報告であり、正式な横断gate試験とはしない。ブロック実動作の検証はこれから。

## サウンドのローカル試運転（human owner報告）

- world.playSoundでblock.glass.breakを指定し、シーランタンが割れる音を聞けた。
- 置かれているシーランタンのbreak音もworld.playBlockSoundで再生できた。
- 先に試したblock.sea_lantern.breakはunknown_soundで拒否された。存在しないsound IDへの応答として切り分けた。
- 音量、pitch／note、receiver、定位、2-playerはこの報告から確認済みとはしない。正式横断gateとは別のローカル試運転。

## カタログID一覧のリスト取り込み（human owner報告）

- ユーザーがblock／entity／particleの3種類の取り込み成功を報告。
- 添付画面でblock 1,166件、entity 157件、particle 115件を確認。
- 表示されている項目はminecraft:付きIDで、先頭部分は辞書順。全要素の順序や集合一致は画面だけでは検証していない。
- 添付画像はmaterials/catalog-lists.pngへ保存。ローカル試運転の素材であり正式gate evidenceではない。
