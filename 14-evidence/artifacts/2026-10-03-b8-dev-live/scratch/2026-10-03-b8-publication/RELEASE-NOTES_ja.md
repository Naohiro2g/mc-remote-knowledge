マイクラリモコン版Scratchのb8ベータ版です。Minecraft Java版1.21.11、McRemote protocol 23.2.0に対応します。

- entityの近傍取得、情報・姿勢の取得、移動と削除を行うブロックを追加しました。
- パーティクルの再生先、dustの色と大きさ、ブロックのパーティクルを設定できるようになりました。
- 音IDやブロックの音を指定して鳴らすブロックを追加しました。音量、高さ（pitchまたはN0〜N24）、再生先を設定できます。
- カタログのID一覧をScratchリストへ取り込めます。ブロックピッカーに日本語・英語名を表示し、IDと名前で検索できます。
- ブロックの状態選択とデフォルト値の扱い、名前空間を省略したブロック情報の入力、スクリプト領域の拡大縮小を改善しました。
- WireScopeのB8 method対応と、空のevents.pollによる履歴の押し出し、数値入力のコピー・貼り付け、backpressureの案内を修正しました。
- 拡張機能カードの画像とmc-remoteの表示名を更新しました。

Geyser経由のiPadで確認したところ、dustの色は反映されますが、大きさは変化しませんでした。Java版では大きさの変化を確認しています。

Scratch／BridgeのOCI image、WireScope ZIPとmanifest、Scratchの設定契約は固定workflowで生成します。生成後、このReleaseの`manifest.json`から各成果物の取得先とidentityを確認できます。

[使い方・開発案内](https://github.com/Naohiro2g/scratch-editor/blob/v2320.0.0b8/README_mc-remote.md)
