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
