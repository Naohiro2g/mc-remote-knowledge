# b8 Scratch統一実施票：開始前の準備

- 作成日: 2026-10-03
- exact set: `b8-integrated-artifact-set-1`
- Scratch source: `691576f60b7f0824e1753bd6823901d01fbe2422`
- knowledge contract path: `00-hub/b8-gate-live-test-sheet_ja.md`の「共通」「3. Scratch」、`00-hub/release-gate-notes_ja.md`のb8凍結節、Scratch projection §3・6、roadmap、Protocol移管計画
- knowledge contract commit: `749ba60dc8c18938e50ce66b8e820aac4401c69e`。remote mainの実SHAと一致を確認して指定refから参照。
- 状態: **segment 3のagent試験終了、human目視4点もPASS、確認票あり**。human ownerがpairingを承認し、helloの版一致を確認して実行した。ブロック9件、sound2 command、catalog、picker、WireScope対象frame、空poll、数値欄コピーはPASS。server backpressure実機再現は未確認。返却は`RESULT_ja.md`。

## 実施前に完了したこと

- HEADが凍結sourceと一致、追跡済みsourceに差分なし。
- `2026-10-02-b8-candidate-local-fixes/materials/`の5成果物を実ファイルからbytes／SHA-256で再照合。GUI tar 138,375,344 bytes／`c7318efdfb22076c2d40501a526d7ca16a121510f7685d875fff34cdc4404843`、WireScope ZIP 83,746 bytes／`4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07`、Scratch用manifest 2,321 bytes／`6ea468f50d50b52722b8f34145743df86cebc60865fe0e827be5632c26b024d0`。
- GUI／Bridge／WireScopeを凍結アーカイブから `runtime/` へ展開し、入力と全fileのbytes一致を確認。配布ファイルを変更せず、ローカルdeployment設定をHTTPで重ねた。GUI 8611／Bridge 8612／WireScope 4183をloopbackで起動。接続先実値と運用logは`private/`へ保存。
- B8共有fixtureは36,481 bytes／111 case／`ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`で凍結値と一致。
- fixture移管の凍結後棚卸しを実施。Protocol 7、WireScope 4、Bridge 1の合計12ファイルを凍結Git sourceから採取。owner・依存・配布を変える移管は行っていない。詳細は `FIXTURE-PREFLIGHT_ja.md`。
- pickerの既定値省略とBlockInfoText手入力のnamespace補完が、指定knowledge SHAのprojection §3・6とroadmapに実装どおり着地していることを確認。局所決定2件の着地確認OK。

## 再開時の入口

1. human ownerのJAR差し替え完了連絡と、devの接続先を受け取る。物理hostの値を過去のlocalhost試運転から推測しない。
2. 統一実施票の順序に従い、Scratch segmentを進める。接続用deployment設定を凍結source／artifactと分けて用意する。
3. 認証済みhelloでprotocol `23.2.0`とMC `1.21.11`を確認してから本体を実行する。pairingが必要ならhuman ownerが承認する。auth.enforcementは変更しない。
4. `CHECKLIST_ja.md`のブロック別項目とreal-browser WireScopeを確認する。失敗時はsegmentを止め、要求・応答・reason・identityを返す。その場でcandidateを修正して続けない。
5. token／pairing_id／private address／player UUIDを含まない結果とscreenshot観測を一枚の確認票へまとめる。画像はGit外に保存し、正式evidenceへの配置はknowledgeが行う。

Pythonの同梱WireScopeはcoordinatorの判断で`df34849`由来のまま凍結している。Scratch用manifestへ置き換えたり、Pythonへ再生成を求めたりしない。

## 素材と境界

- `materials/prepare.py`: 接続なしのidentity照合・fixture棚卸し・アーカイブ展開。
- `materials/frozen-identities.json`: 実ファイルから採取した凍結identity照合結果。`live_started: false`。
- `materials/fixture-inventory.json`、`fixture-consumers.txt`: 凍結sourceの棚卸し。
- `materials/preparation.log`: 準備のPASS。これはlive試験のPASSではない。
- 本directoryはローカル準備素材であり、正式knowledge evidenceではない。実施後に結果素材をknowledgeへ搬送し、gate整理で参照先を確定する。
- 本体の実施値と画像は`materials/live-results.json`／`image-identities.json`とRESULTを参照。`frozen-identities.json`の`live_started:false`は開始前の照合時点の記録。
- devへのScratch接続はcode1000で終了、今回のentityは削除済み。live-human segment 4は未実施。候補再build・更新、他repo変更、tag／release公開は行っていない。`private/`を正式搬送へ含めない。
