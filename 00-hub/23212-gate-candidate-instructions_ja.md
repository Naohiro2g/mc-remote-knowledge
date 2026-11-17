# `2321.2`の候補を作る依頼（McRemote、Scratch）

> `2321.2`のgateを開いた（`00-hub/release-gate-notes_ja.md`の「2026-11-15 `2321.2`横断release gate」）。McRemoteとScratchに、
> 版を`2321.2.0`にした候補を頼む。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## McRemote

### 決まったこと

- 入れるもの：main `082df43145b4a5bfe5854a3985a82c936ed0ce76`（PR #16〜#20）
- helloの`protocol`を`23.3.0`にする（`2026-11-15-03`）。配布物の版は`2321.2.0`で、先頭は`2321`のまま
- BANで拒む経路の直しとkeepaliveは、この候補に入れない（`00-hub/mcremote-liveness-instructions_ja.md`の「進め方の変更
  （2026-11-15）」）

### すること

1. helloの`protocol`が`23.3.0`であることを見るtestを足すか、今のtestの期待を変え、今の`23.2.1`で落ちるのを見る。PR #18で
   足したcaseのうち、clientの申告`23.3.0`を断るものは、serverが`23.3.0`になると通るので、申告の版を変える
2. `23.3.0`にする。互換判定（`10-protocol/versioning-design_ja.md` §8.2）は変えない
3. 版を`2321.2.0`にする。版とprotocolを書く所（build、`manifest.json`など）をそろえる
4. PRにして、localとCIの検査を通す。CIでJARを作る。mergeはhuman ownerが判断する。tag、Release、公開のworkflowはしない
5. Paperの自動の確認を、1.21.11と26.3で行う

### 返却

- 実際に読んだknowledge commit
- 1で落ちたtestと落ち方、直した後のtestの数
- PRの番号、候補のhead、CIのrun ID、artifactのID、JARの名前とbytesとSHA-256（全桁）
- Paperの自動の確認の結果（Paperの版とbuild番号）
- `2321.1.0`から変わったものの一覧（Release本文の材料。本文はhuman ownerが書く）

## Scratch

### 決まったこと

- 入れるもの：カタログのpickerの改善、パレットの折りたたみ（human owner 2026-11-15「実装済み。単独リリース可能。」）
- 版は`v2321.2.0`。McRemoteの拡張のwireとAPI、Bridge、WireScope、共有fixtureが変わるなら、止めて返す
- 新しいreasonの表示は、この候補に入れない（`2321.3`）

### すること

1. 2つの変更が入った候補を作り、版を`2321.2.0`にする。CIで配布物（Web editor、LANの3 OSのZIP、Scratch OCI）を作る
2. Paper 26.3とMcRemoteにつないで、pickerとパレットを確かめる人間の試験の手順を書く

### 返却

- 実際に読んだknowledge commit
- 候補のbranchとhead、PR（あれば）、CIのrun ID、配布物の名前とbytesとSHA-256（全桁）、Scratch OCIのdigest
- 2つの変更の中身と、確かめたこと（test、browser）
- `v2321.1.0`からの差（commitとfileの数、本家への追従が入るか、推奨browserの下限が変わるか）
- LANのランチャーと「はじめに.html」で変わるもの
- 2の手順

## coordinatorがすること

- 候補のhead、CI、artifactを、GitHubのAPIで照合する。そろったらexact setを凍結し、人間の試験の票を作る

## Scratchの作り直し（2026-11-16）

> 返却（PR #36、head `12bef132e83901ade2a482836c611aec99d8b104`）を照合した（`00-hub/release-gate-notes_ja.md`の2321.2の節の
> 「返却の照合（2026-11-15〜16）」）。候補の`mc-remote/block-reference/site/`は`2321.1.0`のままで、`site/2321.2.0/`が無い。
> 上の依頼にブロック一覧を入れていなかった（coordinatorの漏れ）。参照するknowledge commitは、この節が入ったmainのcommitです。

### 決まったこと

- ブロック一覧を作り直す（human owner 2026-11-16「Scratchのブロック一覧　作り直し。」）。一覧はScratchの版ごとに残す
  （`2026-10-17-04`）
- `2321.2.0`の一覧では、`setDimension`と`setBuildOrigin`のmethodを、VMが送る`build.setDimension`と`build.setOrigin`と書く
  （hub NOTESの2026-11-10の行）。前の版の一覧は直さない
- tagを付けるcommitと、配布物とブロック一覧の生成元をそろえる（`2321.1`の`set-2`と同じ形）。Stackの取り込みの条件
  （一覧の`sourceCommit`がtagの指すcommitの祖先で、その間に変わったのは`site/`の生成物だけ）を満たす
- 人間の試験はPaper 26.3 #244（human owner 2026-11-16）

### すること

1. 候補（`12bef13`）の上で、一覧の生成を直し、`2321.2.0`の一覧を新しいcommitで作る。commitの分け方は担当が決める
2. その先頭で、CIで配布物（Web editor、LANの3 OSのZIP、Scratch OCI）を作り直す
3. PR #36を更新する。mergeはhuman ownerが判断する。developには候補に無いcommitがあるので、tagの指すcommitはdevelopの先頭に
   ならない。merge commitで入れればtagのcommitはdevelopに含まれる。公開のworkflowが、それで通るかを確かめる

### 返却

- 実際に読んだknowledge commit
- 新しいhead、CIのrun ID、artifactのIDとdigest、配布物の名前とbytesとSHA-256（全桁）、Scratch OCIのdigest
- 一覧の`release`、`sourceRef`、`sourceCommit`、変わったfileの数。`2321.1.0`の一覧との違い（blockの数、ID、表示、methodの名前）
- `12bef13`の配布物から変わるもの（どのfileが変わるか）
- 公開のworkflowが、tagの指すcommitとdevelopの関係に何を求めるか

## 範囲を広げた後の候補（2026-11-17）

> `2026-11-17-01`で、`2321.2`にUnity箱庭の最初の公開と、ScratchとtoolingのUnity箱庭に向けた変更を入れた。human ownerに
> よると、ScratchとUnity箱庭の候補はできていて、human ownerが最終の確認をする。この節は、その返却に要るものをまとめる。
> McRemoteの候補（`2ccf0b1`）は変えない。参照するknowledge commitは、この節が入ったmainのcommitです。

### Scratch

- 入れるもの：`develop`にmergeしたもの（PR #35〜#37、`b9c791d3fe7db8644421b4cbdbb4599b0476239c`まで）。版は`v2321.2.0`
- Bridge、runtime config（`schema_version: 2`）、Scratchは組で入れる（`2026-11-16-01`③）。LANのZIPに入れるBridgeは、toolingの
  候補のcommitから作る
- ブロック一覧は、候補のcommitから`2321.2.0`で作り直す。Stackの取り込みの条件は、上の「Scratchの作り直し（2026-11-16）」と同じ
- PR #36の`d72a033`の候補（artifact `14173277606`）は使わない

返却：

- 実際に読んだknowledge commit
- 候補のbranchとhead、CIのrun ID、artifactのIDとdigest、配布物の名前とbytesとSHA-256（全桁）、Scratch OCIのdigest、
  `candidate-manifest.json`（toolingのcommit、Bridge OCIのdigest）
- ブロック一覧の`release`と`sourceCommit`。「Unity」の絞り込みに入れたmethodと、何を元にしたか
- `v2321.1.0`から変わったもの（Release本文の材料。本文はhuman ownerが書く）
- 人間の試験の手順の案（McRemote `2321.2.0`のPaperと、Unity箱庭の候補の両方につなぐ）

### minecraft-remote-tooling

- 入れるもの：PR #11（Bridgeの接続先ID）とPR #12（WireScopeの`server`の表示とerrorの`data`）。human ownerが2026-11-17に
  `main`へmergeした（`62f95f4a72db90cdfb2e759150f8488b6a264a49`まで）
- 版は`v2321.2.0`

返却：

- 実際に読んだknowledge commit
- mergeしたcommit、候補のhead、CIのrun ID、artifactのIDとdigest、Bridge OCIのdigest、WireScopeのZIPとmanifestのbytesと
  SHA-256（全桁）
- `v2321.0.0`から変わったもの
- 接続先の一覧を与えずに環境変数だけで起動したBridgeが、前と同じに動くこと（`2026-11-16-01`②）を何で確かめたか

### Unity箱庭

- 最初の版は`2321.2.0`（`2026-11-17-01`①）。`VERSION`を`2321.2.0`にしたcommitをGitHubに置き、そのcommitからimageを作る
  （labelの`revision`を照合するため）
- GHCRへのpushは、human ownerが判断してから行う（`00-hub/unity-sandbox-release-instructions_ja.md`の「すること」の6のまま）
- LANのセットを入れるかは、human ownerと相談する（版は決めていない）

返却：

- 実際に読んだknowledge commit
- 候補のcommit（GitHubにあるもの）とPR
- imageのIDとbytes、labelの全部、base imageの名前とdigest
- `/healthz`の応答と、helloの`server.version`と`protocol`
- 答えるmethodの一覧（Scratchの「Unity」の絞り込みと`19-unity/README_ja.md`のため）
- `player.setPos`と`player.setPose`で世界の外を指したときの、errorの`data`の例（playerは高さ320まで受け付けるので、
  `bounds`の`y_max`に何を入れたか）
- `zero_direction`のcode。wireとMcRemoteは`-32602`で、返却（2026-11-17）の確定搬送票は`-32000`と書いている
- 人が確かめたことと、確かめられなかったこと

### coordinatorがすること（2026-11-17）

- 返却をGitHubのAPIで照合し、配布物を外からダウンロードして計り直す。Unity箱庭のimageは、GHCRへpushする前なので、IDと
  labelで照合する
- そろったらexact setを凍結し、Stackへの票（候補を置く、`unity-sb`と`unity-sb-lts`、接続先の一覧）と、人間の試験の票を作る
