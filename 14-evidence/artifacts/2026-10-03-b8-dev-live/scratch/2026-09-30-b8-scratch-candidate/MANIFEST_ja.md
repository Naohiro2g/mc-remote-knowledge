# B8 Scratch candidate 素材

> 更新候補: `agent/b8-compatibility@df34849d2502a498a06c5fe07a91d03e925124eb`。B7是正3件を含む新しい素材は`../2026-10-01-b8-candidate-b7-fixes/`。このdirectoryは旧candidateの報告照合用で、新しい試験入力には使わない。

- 作成日: 2026-10-01
- source branch: `agent/b8-compatibility`
- source commit: `dfcb03cf97fed998268b4714feb32d03a209f549`（push済み）
- knowledge contract: `0318332a2b3395a5d74b46d7da6946030a2fc172`
- fixture successor commit: `054a3af017f1abb8cc01cf85b3bc83181e648e19`
- fixture: `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`、111 case（従来59＋sound37＋resource ID15）、36,481 bytes、SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`

`materials/` のファイルは、push済みsource commitからのworkspace build後に作成した。GUIとBridgeはDocker imageの**入力アーカイブ**であり、OCI imageではない。Docker daemonが起動していないため、OCI digestとregistry identityは未取得。

| ファイル | bytes | SHA-256 | 内容 |
| --- | ---: | --- | --- |
| `materials/scratch-image-inputs.tar.gz` | 152,986,359 | `e637c7e21ba6589e2d81742bed0b8af32c6598f5337b917b701dd8fcd51d69e2` | `Dockerfile.mc-remote`と`build/` |
| `materials/bridge-image-inputs.tar.gz` | 38,138 | `fd43f714c77d2bc184bf882460dfc05a1ce345dc6d4f5b52505a6a9d2850908f` | `Dockerfile`、`package.json`、`dist/`、`node_modules/ws/` |
| `materials/wirescope-app.zip` | 83,746 | `4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07` | WireScope browser app |
| `materials/wirescope-app.manifest.json` | 2,321 | `65c020832125c7947427d83392dccf478bcc92a1e53f2316c8bfe21b06a8748f` | WireScopeのdetached manifest（source commitを内包） |
| `materials/contracts.tar.gz` | 1,908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` | Scratch契約ディレクトリ |

実施した検証: Protocol 37件、Bridge 30件、WireScope 142件、Scratch観測20件、VM 121 subtests／514 assertions、GUIのlearner／picker 42件と日本語表示5件。全workspaceの本番buildは前commitでPASSし、サウンド追加後にVM／GUI／WireScopeの本番buildを再実行してPASS。時刻列・カード変更後にもWireScope／GUIの本番buildと対象test・lintをPASS。独立Chromiumのlocalhostプレビューで時刻列、詳細時刻、handshake開閉を確認した。VM／GUI lintはエラー0件（既存警告あり）。Bridgeのlocalhost待受テストはsandboxで`EPERM`だったため、同じtestをsandbox外で再実行して全30件PASS。

未実施: OCI image build・push、shared環境への配置、Scratchと接続したWireScope E2E、実機・人間参加試験、横断gateの判定。このdirectoryはhandoff素材であり正式evidenceではない。

## B8に追加したサウンド入力

`world.playSound`と`world.playBlockSound`の命令ブロック、および音量・高さ・再生先を作る音の設定ブロックを`acc913887f`で実装した。高さは数値なら`pitch`、`N0`〜`N24`なら`note`として送る。空欄はoptionsの該当項目を省略する。音名から`N0`〜`N24`への換算はScratchのプログラム側で行う。Python等の`pitch=`／`note=`はScratch repoの範囲外である。Scratchの動作を元にknowledgeのスポークへ記録する必要がある。
