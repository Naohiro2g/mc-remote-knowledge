# NOTES — 未確定インボックス / carry-forward 欠落

低摩擦の捕捉（park）です。理由が立って横断判断になったものは `DECISIONS_ja.md` の未確定節へ昇格します。

## Inbox

- なし。

## Archive carry-forward gaps

archive は例外参照です。参照によって public SSOT の欠落を見つけたら、次の形で登録します。archive へのリンクだけで閉じず、公開可能な interface と why をこのリポへ持ち出し、archive を読まずに同じ判断ができる状態で `[done]` にします。

```text
- YYYY-MM-DD [ ] 対象 / 欠けていた判断 / 必要な公開界面 / 閉じる条件
```

- 2026-07-21 [done] DECISIONS `2026-06-15-03` / 改訂元の決定行が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / `2026-06-25-01` との改訂接続を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-18-06` / 後続決定が「転記ギャップ」と書き込み口一本化の根拠として参照する決定行が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-18-11` / 現行 `CLAUDE.md` に継承された `@import` 最小化原則の判断理由と、後続決定が参照する昇格基準が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 現行表現は `CLAUDE.md` を正とし、履歴と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-20-01` / 現行の未確定ダッシュボードが使う `起案` / `保留` / `却下` の導入理由と、後続 `2026-06-20-05` の参照先が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 状態語彙の判断理由と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-27-06` / bridge の TypeScript 採用と配置の判断理由、および後続 `2026-06-27-08` が精緻化・訂正した wire 共有モデルの改訂元が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 改訂前後の判断履歴と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-28-01` / 共有マルチプレイを公開ホストへの outbound 接続へ集約し家庭への inbound 公開を一般解にしない判断と、後続 `2026-06-27-08` の参照先が public epoch から欠落 / 人間が固有名詞を含め公開可と確認し、archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / アーキテクチャ判断と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-29-02` / Codex 受け入れ時に薄い `AGENTS.md` から `CLAUDE.md` 正典へ合流させたポインタ方式の判断理由と、後続 `2026-06-22-05` の参照先が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 現行topologyの起点と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-29-05` / `setBlock` を学習体験の中心APIとして残す理由と送信モードtaxonomy、および後続 `2026-07-01-08` が保持した改訂元が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 教材・protocolを結ぶ判断履歴と改訂接続を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-01-04` / 現存する `00-hub/release-gate-notes_ja.md` を横断リリース前の状態集約先とし、版別ファイルを増やさない構造判断と後続 `2026-07-10-05` の参照先が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 現行構造の判断理由と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-01-05` / b1確認票をdev側の事実・根拠収集とし、knowledge側が固定したpath・commitに対して最終判定する境界と後続 `2026-07-10-05` の参照先が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 現行の判定権限境界と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-01-07` / NotebookLM等の生成投影を追跡せずsource commitからオンデマンド再生成する現行原則と、後続 `2026-07-10-08` の参照先が public epoch から欠落 / 人間がオンデマンド再生成を現在も必要と確認し、archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 旧生成scriptは当時の実装参照として保持し、生成投影の原則と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-03-03` / `着地確認依頼` のpush済みknowledge SHAとリモート反映確認を必須化し、未pushを未着地とする現行規則、および後続 `2026-07-10-03` / `2026-07-10-05` の参照先が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 固定票の必須fieldとSHA真実則の判断理由を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-29-07` / agentの作業範囲を指定内に限定し、設計判断を着地前に人間へ返す現行規律の起点が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 現行 `CLAUDE.md` の作業範囲・人間レビュー境界の判断理由を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-03-04` / 確認不要な機械的着地を搬送物のverbatim適用に限定し、要約・文言調整等の逸脱を事前確認へ戻す現行規律の精緻化と、後続 `2026-07-10-04` の参照先が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / `2026-06-29-07` から現行規律までの改訂接続を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-03-05` / 既知逸脱を記録したうえでb1横断リリースを節目として閉じた決定と、後続 `2026-07-04-01` がb1を再tagせずb2へ進めた参照点が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / b1からb2へのリリース系譜と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-06-18-12` / freshness自動生成ファイルを別SSOTにせず `git log` を使う判断と、後続 `2026-07-10-06` の参照先が public epoch から欠落 / 人間が再録を確認し、archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / claude.ai同期手段の当時の前提を含む履歴と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-10-06` / claude.ai下流snapshotとrepo HEADの鮮度検証を、read-onlyと単一書き込み口を分離して検討した改訂前判断、および `2026-07-10-03` の参照先が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 改訂先 `2026-07-13-01` は次段で確認し、鮮度問題の判断履歴と参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-13-01` / snapshot生成器に状態を重複保持せず正本文書を指定commit treeからverbatim投影し、抽出異常時に停止する再現性規則と、`2026-07-10-06` の改訂先が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / オンデマンド生成の現行原則と改訂接続を public SSOT 内で解決し、追加依存は順次確認
- 2026-07-22 [done] DECISIONS `2026-07-05-01` / NotebookLM生成物の入口に現在・将来・parkを区別する時系列アンカーを置いた判断と、固定状態値が陳腐化して `2026-07-13-01` の正本verbatim投影へ改訂された失敗前史が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 現行生成方式の判断理由と改訂接続を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-01-03` / NotebookLM投影へ現行仕様・未実装・将来計画・履歴を区別する読み取りガイドを自動挿入し、投影側の問題を正本文書へ拡散しない設計起点が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / `2026-07-01-07` / `2026-07-05-01` / `2026-07-13-01` へ続く生成投影の発展を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-12-03` / R1・R2・R3のproduct相とb1・b2等のrelease列を別軸とし、現在地をR2完了・R3入口とした現行roadmapの直接根拠が public epoch から欠落 / archive の同一 ID・同一本文を `00-hub/DECISIONS_ja.md` へ verbatim で carry-in / 現行相マーカーと `2026-07-13-01` の参照依存を public SSOT 内で解決
- 2026-07-22 [done] DECISIONS `2026-07-15-01` / stable・beta・alphaのchannel設計とprivateな物理配置が一行に混在し、後続決定から参照される改訂元が public epoch から欠落 / provider・host・home machine・物理配置を含むため同一 ID の redacted 版も verbatim carry-in も行わない / 公開interfaceは `2026-07-16-01`（channel・artifact・実行環境の分離）と `2026-07-22-01`（stable / beta の非階層性・現状beta優先）で解決し、private ops は public knowledge へ戻さず閉じる
- 2026-07-22 [done] DECISIONS `2026-07-16-01` / 現在の`b1` / `b2` / `b3`同期状態を、環境とcomponent版の恒久的な固定対応に読める余地 / 人間レビューで、環境を互換性検証済みのexact component構成とし、具体値は`mc-remote-stack`のprofile / manifestへ置く`2026-07-22-02`を確定 / bootstrap期の同期状態と将来の独立cadenceを分離して解決
- 2026-07-22 [done] DECISIONS `2026-07-12-04` / 公式環境のdogfooding原則とVPS・家庭環境・固有host等のprivateな物理配置が混在し、特定profileへの限定も強いarchive行 / 同一IDではcarry-inせず、公開contractと構成機構の同一性だけを一般化した`2026-07-22-03`を人間レビューで確定 / 具体的な構成・配置・private overlayを固定せず、公開interfaceだけをpublic SSOTへ収容して解決
- 2026-07-22 [park] DECISIONS `2026-07-05-02` / `2026-07-21-07` / 技術的に可能なstream機能とScratch写像を一度に詰め込み、「できることを全部やる」設計へ進む懸念 / main streamを既定実行文脈とする方向は有力だが、substream写像は限定した試作と学習者による因果追跡の観察が必要 / 両決定の保留・起案状態を維持し、八論点を一括確定しない
- 2026-07-22 [ ] `20-教材/ai-learning-design_ja.md` / `2026-07-19-05`でLLM支援開発へ適用したPapertのマイクロワールド／mind-sizeが、既存の構築主義と理論的に接続されていない / LLM運用規律を複製せず、学習上の「因果関係が閉じた場」と「頭に収まる単位」として還流する / 教材哲学の充実を人間レビューし、正典節へ着地したら閉じる
- 2026-07-22 [ ] `20-教材` / `2026-07-22-01`のstable／beta非階層原則が教材スポークへ未投影 / 習熟度で固定せず学習目的・観察対象・支援量に応じて環境を選ぶ低drift原則だけを置き、変動する現状beta優先はroadmap／versioningを参照する / 教材側の配置と文言を人間レビューして着地したら閉じる
- 2026-07-22 [ ] `12-python-client/python-client-guide_ja.md` 現行性監査の基準固定 / knowledge内の古い設計だけで推測修正せず、`minecraft-remote-api` devリポの対象commit・release・実装済み範囲を確認票で固定する / 実装事実と`2026-06-15-02`以降の現行決定を照合できたら各項目の改訂へ進む
- 2026-07-22 [ ] Python初回セットアップ／identity / 廃止済み`PLAYER_NAME`、リポ内で未定義の`ADRS_MCR`、プレイヤー名をprivate設定へ書く説明を除去候補とし、現行`param_mc_remote`の実在key・pair開始点・接続先設定をdev実装で確認する / 初学者が存在しない設定を触らない一本の導線を実機確認したら閉じる
- 2026-07-22 [ ] Python origin／constants／実行環境 / `PLAYER_ORIGIN`、import順序依存、import時`mc_constants.py`生成、生成物のGit追跡、CWD・VS Code・Jupyter、版別fallbackの各主張をdev実装とtestで再検証する / `mc-constants-design_ja.md`を含め、確認できた現行挙動だけをガイドへ残したら閉じる
- 2026-07-22 [ ] Python認証CLI／credential / `mcremote login --channel beta`、`--host`／`--session`、`status`／`logout`／`devices`／`revoke`、非対話`Minecraft.create()`、store・token lifecycleについて、設計済み／実装済み／release済みを分離する / 未実装の将来形を現行セットアップとして教えず、利用可能な導線を対象releaseで検証したら閉じる
- 2026-07-22 [ ] Python学習ガイドの構成 / legacy手順の末尾へ「新プロトコル安定版」を継ぎ足した二重導線を解消し、セットアップ→pair／login→最小実行→観察可能な失敗→復旧を一つの現行フローへ再構成する / stable／betaを習熟度で固定せず対象環境を明記し、初学者による手順検証まで通したら閉じる
- 2026-07-22 [done] DECISIONS `2026-06-22-01` / `2026-07-03-03`の理由文が「層理論」の前例として参照するarchive決定がpublic epochに無かった / archive原文を人間レビューし、同一IDでverbatim carry-inした / public SSOT内で参照意味を解決したため閉じる
- 2026-07-22 [done] DECISIONS `2026-06-22-04` / `2026-07-03-03`の却下案がPostToolUse hookの前例として参照するarchive決定がpublic epochに無かった / archive原文を同一IDでcarry-inし、`2026-07-22-05`でagent非依存checkerへ改訂した / 歴史参照と現行機構をpublic SSOT内で接続したため閉じる
- 2026-07-22 [ ] R体系の棚卸しと`2026-07-13-01`のR3-A誤帰属 / 現行の粗い全体マーカー`R2完了・R3入口`とR1/R2/R3は維持する一方、archive `2026-07-12-04`はdogfooding原則でR3-Aを決めておらず、R3-A/B/Cは旧`scratch-plan`だけに現れた作業束だった。同文書内に「R3-A完了済み」と「R3-A残り」が併存し、順序相・価値gate・作業sliceが混線している / 今は新定義を確定せず、R3完了判定・R4新設・文字suffix再利用・NotebookLM現在地カプセル再生成のいずれかに進む前を再開triggerとして、歴史上の意味・現行gate・component別sliceを棚卸し精査する / `2026-07-13-01`の短縮参照と誤帰属をappend-onlyで訂正し、Rの意味・完了gate・作業分解・投影先をpublic SSOT内で組み直したら閉じる
- 2026-07-22 [done] DECISIONSの短縮ID参照 / 日付部分を省く`YYYY-MM-DD-NN/NN`等が欠落検出をすり抜けた / 全文書を調査して歴史DECISIONS 6行・現行設計文書1行と確認し、`2026-07-22-06`で新規短縮を廃止、歴史行だけをcheckerの互換入力として固定し、現行文書を完全IDへ展開した / 記法・歴史保存・参照検査を確定したため閉じる
