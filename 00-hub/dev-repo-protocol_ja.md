# 開発リポ用エージェント運用プロトコル（dev-repo protocol）

各開発リポ（パブリック）は、公開・commit 対象の `AGENTS.md` を薄い固定入口とし、McRemote 固有作業の
開始時だけ本ファイルの runtime block を knowledge リポのリモート `main` から取得して読む。運用規則の
全文を各リポへ複製しない。Claude Code 用 `CLAUDE.md` は `@AGENTS.md` だけのローカルポインタ、
`NOTES_ja.md` は運用者ローカル限定の捕捉として分けて使う。

## AGENTS.md（公開 dev リポに commit する薄い入口）

公開 dev リポ直下の `AGENTS.md` は **commit 対象**。Codex / Copilot / Gemini 等が最初に読む
公開の入口として、次の invariant だけを置く。

- McRemote 固有の設計判断の正本は GitHub 上の `Naohiro2g/mc-remote-knowledge`。
- McRemote 固有作業に入る前に、agent は本ファイルの最新 runtime block と関連 SSOT を読む。
- SSOT にアクセスできない場合は、推測で補完せず停止してユーザーへ返す。
- `AGENTS.md` は SSOT の思想・決定・スポーク構造を複製しない。複製はドリフト源。
- runtime block の取得全文は一時ファイルへ逃がし、block だけを文脈へ入れる。

`AGENTS.md` は公開 contributor / 各種 agent 向けの最小ゲートであり、SSOT の repository 名と安定した取得先だけを
持つ。Claude Code はローカル `CLAUDE.md` の `@AGENTS.md` から同じ入口へ合流する。

### AGENTS.md テンプレ

````markdown
# <repo-name>

<このリポが何か 1行>

## McRemote SSOT

McRemote 固有の設計判断の正本は GitHub 上の `Naohiro2g/mc-remote-knowledge` です。

McRemote 固有文脈に依存する作業に入る前に、agent はその SSOT リポジトリの関連文書を
必ず読んでください。対象には architecture / protocol / deployment / contributor workflow /
learning design、および McRemote 固有の判断理由に依存する挙動変更が含まれます。

最初に、knowledge リポのリモート `main` から最新の dev agent runtime protocol だけを取得して
指示として読んでください。取得元ファイル全体を会話へ出力してはいけません。

```bash
protocol_source="$(mktemp)"
knowledge_commit="$(gh api repos/Naohiro2g/mc-remote-knowledge/commits/main -q .sha)"
gh api "repos/Naohiro2g/mc-remote-knowledge/contents/00-hub/dev-repo-protocol_ja.md?ref=$knowledge_commit" \
  -q .content | base64 -d > "$protocol_source"
if [ "$(grep -Fxc '<!-- BEGIN: DEV-AGENT-RUNTIME -->' "$protocol_source")" -ne 1 ] || \
   [ "$(grep -Fxc '<!-- END: DEV-AGENT-RUNTIME -->' "$protocol_source")" -ne 1 ]; then
  echo "dev agent runtime marker missing or duplicated" >&2
  exit 1
fi
printf 'knowledge commit: %s\n' "$knowledge_commit"
awk '/^<!-- BEGIN: DEV-AGENT-RUNTIME -->$/{reading=1;next} \
     /^<!-- END: DEV-AGENT-RUNTIME -->$/{reading=0} \
     reading' "$protocol_source"
```

SSOT リポジトリへアクセスできない場合は、作業を止め、その旨を明示してください。この
リポジトリ単体、assistant memory、過去会話、ローカル推論から欠けた文脈を補完してはいけません。
SSOT にアクセスできるまで、McRemote 固有文脈に依存する設計判断や実装を進めないでください。

このファイルは SSOT を複製しません。複製はドリフトを生みます。

- このリポの関連スポーク: <要記入。例: 12-python-client/, 10-protocol/>

## このリポ固有の指示

<この公開リポ固有の build/test/layout/upstream 方針を書く。McRemote 固有の判断理由は複製しない。>
````

### AGENTS.md 配布・更新手順

1. 上のテンプレを元に、`<repo-name>` / `<このリポが何か 1行>` / 関連スポーク / repo 固有手順だけを埋める。
2. 既存 upstream の `AGENTS.md` がある場合は消さず、**McRemote SSOT** 節を先頭に置き、
   upstream / package 固有の指示は後段へ残す。
3. McRemote 固有の設計・protocol・デプロイ・学習支援に触れる作業では、agent が SSOT を読んだかを
   最初の作業報告で明示させる。
4. SSOT の中身を公開 `AGENTS.md` に転記しない。必要なら「どの SSOT を読め」の入口だけを更新する。
5. 一度配布した後は、runtime block の内容変更だけでは `AGENTS.md` を再配布しない。取得パス・marker・
   bootstrap command を変えたときだけ入口を更新する。

## CLAUDE.md（運用者ローカル限定）

Claude Code は `AGENTS.md` を自動では読まないため、各開発リポ直下のローカル `CLAUDE.md` は次の
1行だけを持つ。`.gitignore` 対象・commit 不要。内容は固定なので、runtime 更新時の再配布は不要。

```markdown
@AGENTS.md
```

運用者ローカル限定の文書（`CLAUDE.md`・`NOTES_ja.md`・リポ固有 runbook）は、
公開 dev リポに commit しない。

## Dev agent runtime protocol（knowledge 中央・on-demand）

以下の marker 間だけが、各 dev agent が McRemote 固有作業の開始時に読む runtime block の正本。
`AGENTS.md` の bootstrap command は本ファイル全文を一時ファイルへ取得し、この block だけを出力する。

````markdown
<!-- BEGIN: DEV-AGENT-RUNTIME -->
# McRemote dev agent runtime protocol

## 設計の根拠は別リポにある（mc-remote-knowledge）
- 正本: https://github.com/Naohiro2g/mc-remote-knowledge （public）
- 読み方: bootstrap で解決した knowledge commit をセッションの参照 ref とし、INDEX を入口に必要なファイルだけ読む。
    単発:   gh api "repos/Naohiro2g/mc-remote-knowledge/contents/<path>?ref=<knowledge_commit>" -q .content | base64 -d
    まとめ: read-only の使い捨てクローン → gh repo clone Naohiro2g/mc-remote-knowledge "$(mktemp -d)/kn" -- --depth 1 --config remote.origin.pushurl=disabled://read-only-clone
    このクローンは fetch 可・push 不可。別リポ参照用 clone を着地経路へ転用しない。
- 禁止: ユーザーのローカル作業クローンに触れない（読み書きとも）。
    pull / commit / checkout を作業クローンへ実行しない。編集途中のことがある。
- 全体地図: 00-hub/INDEX_ja.md ／ 横断決定ログ: 00-hub/DECISIONS_ja.md
- このリポの関連スポークは、呼び出し元リポの `AGENTS.md` を正とする。

## セッションプロトコル（on-demand 参照）
- 設計・決定の根拠が要るときは INDEX を入口に、関連スポークの該当ファイルだけ読む。知識リポを丸読みしない。
- 人間が「セッションループの現在地は？」「今どの step/status？」と聞いたら、knowledge リポ
  `00-hub/claude-ai-guide_ja.md` §7 と `00-hub/terms-glossary_ja.md` §セッションループ状態名に従い、次の形で短く返す。

```markdown
## セッションループ現在地

- step: <正典語> (`<machine_key>`)
- status: <正典語> (`<machine_key>`)
- sink: 確約 / 捕捉 / なし / 未判定
- 根拠: <読んだ SSOT・検証結果・搬送票などを1行>
- 次の一手: <今やるべき最小の行動を1行>
```

- リリース前確認を求められたら、knowledge リポ `00-hub/release-gate-notes_ja.md` の確認票フォーマットに従う。
  repo 側 agent は事実と根拠だけを書き、b1 適合の最終判定をしない。`knowledge repo b1定義.path` と
  `knowledge repo b1定義.commit` は必ず埋める。commit は確認票作成時に実際に読んだ knowledge repo の
  commit SHA とする。未記入の票は仮記入扱い。

- テスト証跡は再現コストで3階級に分ける（DECISIONS `2026-07-06-03`）。`unit/deterministic` はテストコード＋PASS
  コマンド＋commit を証跡とし、JSON 保存を必須にしない。`live-auto` は実サーバ相手だが人間操作なしの smoke で、
  通常は script＋PASS summary で足りるが、protocol ratify / release gate の根拠に使う回は transcript を保存する。
  `live-human`（`/mcremote pair` 等、人間操作・端末・実機状態を含む）は、正式根拠にする回では knowledge リポ
  `14-evidence/records/<test_id>_ja.md` に構造化サマリを作り、token / pair code / private host / UUID 等を redact
  した sanitized artifact を `14-evidence/artifacts/<test_id>/` へ置く。raw は `14-evidence/raw/`（gitignore・剪定可）
  または外部/private 保管＋hash 参照。搬送票・確認票の `根拠/検証` には test class、evidence record path、artifact
  path、commit/SHA を明記する。ローカル未追跡ファイル名だけを正式証跡として扱わない。開発フェーズ終端・milestone・
  公開準備では、再現コストだけでなく token cost と redaction / 移管コストも見て棚卸しする。
  dev 側が作るのは確定搬送票＋素材まで。record path / artifact path は命名提案として書けるが、`records/` /
  `artifacts/` / `INDEX` / `redactions.json` の正式 authoring・配置・commit は knowledge 側が行う。
  セッション終了で消えると困る素材は `handoff-materials/<handoff_id>/` に置く（既定 gitignore）。中身は
  `MANIFEST_ja.md`＋`materials/`。`handoff-materials/` は正式証跡ではなく、knowledge 着地と元リポ側の着地確認OK
  後に削除する。private ops として保持が必要なら `mc-remote-backstage` へ移す。frozen archive は着地先にしない。
  `14-evidence-handoff/` や root 直下 tarball は使わない。

- 横断的な決定（複数リポ／スポークに波及）をしたら、下の `確定搬送票` を出す。dev 側 agent は
  DECISIONS の ID 採番、staging、commit 手順を書かない。転記・レビュー・ID 採番・commit は knowledge リポ側で行う。

```markdown
## 確定搬送票

- 搬送元 repo:
- 搬送元 surface:
- 搬送元 branch/commit:
- 作成日:
- 種別: 横断決定 / 局所決定 / 未確定の昇格 / その他
- 決定:
- 理由:
- 却下案:
- 影響:
- 根拠/検証:
- 既に変更した実装/文書:
- ナレッジ着地希望:
- 捕捉 cleanup:
- 着地後の確認戻り先:
```

- knowledge リポで着地・commit・push された後、人間は `着地確認依頼` をこの repo の session に戻す。
  agent は knowledge 側の着地先を読み、元の実装・検証結果・搬送票と照合する。一致していれば `着地確認OK` を返し、
  per-repo `NOTES_ja.md` の該当行を `[→DEC <ID>]` / `[done]` へ更新または削除する。ずれがあれば `着地差分メモ`
  として再搬送できる形で返す。`knowledge commit（push 済み SHA）` と `リモート反映確認` は必ず埋める。
  未記入の着地確認依頼は仮記入扱いとし、正式な着地確認依頼として受理しない。

```markdown
## 着地確認依頼

- 元の確定搬送票:
- knowledge commit（push 済み SHA）:
- リモート反映確認:
- 着地先:
- DECISION ID:
- ナレッジ側で調整した要点:
- 確認してほしいこと:
- dev 側で更新/削除してほしいもの:
```

- セッションを閉じるとき、または長時間作業の節目では、下の `セッションクローズ票` を短く出す。これは決定の
  正本ではない。次回再開に必要な作業状態だけをまとめ、永続化が必要な未完了は per-repo `NOTES_ja.md` へ、
  横断するものは hub `NOTES_ja.md` / `DECISIONS_ja.md` へ移す。`/compact` は、必要な NOTES 書き戻しまたは
  セッションクローズ票を出してから行う。

```markdown
## セッションクローズ票

- repo:
- surface:
- branch/commit:
- 作業範囲:
- 今回やったこと:
- 変更ファイル:
- 検証:
- 未完了:
- 次に読むもの:
- 次の一手:
- 未着地の搬送物:
- NOTES/DECISIONS:
- 注意点:
```

## トークン衛生
冗長出力は文脈に流さない。全ログはファイルへ、文脈には失敗時の末尾だけ:
`<cmd> > build.log 2>&1 || tail -n 80 build.log`（全ログは残り grep で掘れる／tail は 0 を返す点に注意）。
利用可能なら冗長処理は subagent へ委譲し、成功報告は短くする。用件が変わったら新規/clear、
長くなったら NOTES 書き戻し→続行時のみ /compact。
理由と詳細は knowledge リポ root `token-hygiene-guide_ja.md` を参照。

## 実行境界（できないこと＋返し方）
dev リポ所有の実行サーフェスの能力境界。「できるところまでやって」で手順を渡されたときの既定。
- claude.ai 側の操作は実行不可：Project Knowledge の再同期、instructions の貼り直し、コネクタ設定 等。MCP 経由でも叩けない（会話ごとの live tool で Project Knowledge スナップショットを更新しない）。
- 手順にこれらが含まれたら：検証できるステップを実行し（commit/push 等、結果は SHA 等で報告）、claude.ai 側は正確な人間 runbook にして返す。「代わりにやる」と提案しない。
- やれると確証が持てない操作（別サーフェスの状態に依存する等）は人間に返す。迷ったら返す。
- 他サーフェスから渡される決定は「中身だけ」＝ID 未採番・commit/staging 手順なしで受け、ID 採番と配置メカニクスは knowledge リポ側で確定する。理由は knowledge リポ 00-hub/DECISIONS_ja.md 2026-06-22-03。
<!-- END: DEV-AGENT-RUNTIME -->
````


## 一度きりの bootstrap と更新確認

現在の対象は `McRemote` / `minecraft-remote-api` / `scratch-editor` / `mc-remote-stack`。新しい dev リポは
作成時に同じ bootstrap を行う。`scratch-editor-upstream-contrib` は `2026-07-18-02` の一方向弁により対象外。

1. knowledge リポ所有サーフェスが、各対象リポの既存 `AGENTS.md` を保ったまま **McRemote SSOT** 節へ
   上記 bootstrap command と関連スポークを追加し、各 dev リポで commit/push する。
2. 各ローカル作業 clone の運用者は、gitignore 済み `CLAUDE.md` を `@AGENTS.md` 1行へ置換する。
   ユーザーの作業 clone なので knowledge 側 agent は直接変更しない。
3. 各 dev セッションで、`AGENTS.md` 読み込み → runtime marker 間だけ取得 → 最初の作業報告で参照した
   knowledge commit / 関連スポークを明示、までを確認する。
4. 完了確認は、各 dev リポの `AGENTS.md` push 済み commit SHA と、運用者によるローカル
   `CLAUDE.md` ポインタ確認を knowledge 側へ戻す。全対象の確認が揃えば初回 rollout 完了。
5. 以後、runtime block の通常更新では配布しない。取得パス・marker・bootstrap command・対象リポ一覧を
   変えた場合だけ本節を再実行する。

## マシンブートストラップ（day-0 / doctor）

新しいマシンに開発環境を作る手順と、既存マシンの点検（doctor）手順。正本はこの節（`2026-07-20-02`）。
前節がリポ側の一度きりの rollout を扱うのに対し、本節はマシンごとに繰り返す側を扱う。
server 実行環境の構築は対象外（public SSOT は `mc-remote-stack`）。

### 人間の手作業（agent に委ねられないものだけ）

1. インストール: `git` / `gh` / agent CLI（`claude`・`codex`）。admin 権限が要るため人間が行う。
2. `gh auth login`（対話 OAuth）。bootstrap command が `gh api` を使うための CLI 認証であり、knowledge リポ自体は public。
3. `gh repo clone Naohiro2g/mc-remote-knowledge`（標準の親ディレクトリへ）。
4. knowledge リポで agent を起動し、次の1行を渡す:
   「新しいマシンのセットアップ: `00-hub/dev-repo-protocol_ja.md` §マシンブートストラップに従って」
   （点検だけなら「マシン点検: 同節の doctor に従って」）

### agent の手順（day-0）

1. **preflight**: `gh auth status`・public SSOT 到達（`gh api repos/Naohiro2g/mc-remote-knowledge -q .full_name`）・
   必要 CLI（`git` / `gh`、各リポ toolchain: `java`＋Gradle wrapper / `uv` / `node`）の存在を確認する。
   不足は列挙して人間へ返す。**agent はインストールしない**（admin は権限境界の外）。
2. knowledge リポの兄弟ディレクトリへ対象 dev リポを clone する
   （対象一覧は前節と同一。既存ディレクトリがあれば触らず報告する）。
3. 各 clone に gitignore 済みローカル `CLAUDE.md` を **`@AGENTS.md` の1行だけ**で作成する。
4. **検証**: 1リポで `AGENTS.md` の bootstrap command を実走し、markers OK と knowledge commit 表示を確認する。
5. **証拠つき報告**: 各 clone の HEAD SHA・`CLAUDE.md` 内容・bootstrap PASS・toolchain 確認結果を返す。
   自己申告でなく成果物で判定する（`2026-07-19-05` ⑥）。
6. Windows のみ: repo × agent の Windows Terminal profile snippet を生成して人間へ渡す
   （適用は人間＝`llm-agent-boundary-guide_ja.md` §5）。
7. `scratch-editor-upstream-contrib` は本手順の対象外。contrib 作業を始めるときだけ、
   `13-scratch-client/scratch-upstream-design_ja.md` の push 安全設定（`2026-07-18-02`）つき手順で別途 clone する。

### doctor（既存マシンの点検）

day-0 の 1・4・5 に加えて、各 clone について次を確認し、逸脱を人間へ報告する。**勝手に直さない**
（ユーザーの作業 clone なので、修正は人間の明示指示があるときだけ行う）:

- ローカル `CLAUDE.md` が `@AGENTS.md` 1行か（旧全文コピーの残存は、`2026-07-19-04` 以前の規則が
  生き続ける drift 面）。
- 追跡 `AGENTS.md` が bootstrap を含む版か。main から離れた branch 上の clone は branch 名とともに
  報告し、同期はそのセッションの閉じ方に委ねる。

## NOTES_ja.md（同リポ申し送り／未確定インボックス）

各 dev リポ直下に `NOTES_ja.md` を置く。**公開リポにコミットしない（ローカル限定）**＝CLAUDE.md と同じ扱いで `.gitignore` に追加して追跡しない。役割は hub の NOTES と同一（中身でなくフォーマットを共有）。per-repo は固有申し送りに限定し、横断する芽は hub/NOTES か DECISIONS へ escalate する（複製しない＝単一 source of truth）。

**セッション終いの escalation-sweep（必須）**：dev NOTES はセッション・ループの捕捉（sink）にあたる（`claude-ai-guide_ja.md` §7・`2026-06-23-01`。語彙は `2026-07-16-07`）。dev セッションを閉じる前に per-repo NOTES を一度見直し、**横断の芽（複数ワークストリーム／hub 方針に触れるもの）を hub `NOTES_ja.md` へ拾い上げる**。これを終い儀式として固定し、escalation の踏み忘れ（park したまま hub に上がらず宙に浮く）を防ぐ。引き継ぎ先セッションには「元リポの `NOTES_ja.md` を参照」と渡せば文脈が早い。

----（ここから NOTES_ja.md 雛形）----

```markdown
# NOTES — <repo-name> 申し送り／未確定

> 低摩擦の捕捉（sink）。ID/理由 不要。次セッションへの申し送り・未確定・思いつきを置く。
> 横断する芽は hub/NOTES_ja.md か DECISIONS（起案）へ escalate。確約はそちら。

- YYYY-MM-DD [ ] …
```

----（ここまで）----

新規作成時だけ marker 間の雛形をツールで抽出し、`<repo-name>` を置換する。既存 `NOTES_ja.md` は
セッション固有の捕捉を持つため、runtime 更新や bootstrap で上書きしない。`.gitignore` には
`CLAUDE.md` と並べて `NOTES_ja.md` を追加する。

入口配布は役割別 topology（DECISIONS `2026-07-20-03`）に従い、上記4 dev リポだけを対象とする。

## 進捗運用（現在地と次の一手）

進捗の「現在地」は二粒度に分け、**保存と生成を分離**する（protocol.json 投影 `2026-06-19-02`③ と同型／決定 `2026-06-24-03`）。揮発する細粒度を焼くと drift 源になる、が根拠。

- **粗い相マーカー（保存）**: grand-design-roadmap 冒頭に「現在 Rn」の1行のみ。全期間で数回しか変わらない＝低 drift。**相が進んだら（ゲート越え）DECISIONS 流で起案 → 人間が commit**。dev セッションは知識リポ作業クローンを直接書かない（CLAUDE.md 禁止則）＝新マーカー行を**提案して出す**までが上限。

- **次の一手（都度生成・焼かない）**: 日々の「次どうしよう」は roadmap に保存しない。各 dev セッションで AI が「§2 該当 R＋§4 最優先＋DECISIONS／per-repo NOTES」を読み起こして提案 → 実行サーフェスで実行 → 寄り道は per-repo NOTES に park（捕捉）。人間が roadmap を読み解くのでなく、この読み起こし＝投影を AI に頼る。

**問いの宛先を分ける（rathole／バランス喪失 対策）**:

- 「**このリポの**次は？」→ そのリポの dev セッション（自スライス＋per-repo NOTES）で生成。
- 「そもそも**今どのリポに**注力すべきか」（横断の優先・solo バランス）→ **hub roadmap を文脈に入れたセッション**に問う。単一リポセッションは自スライスしか見ず「このリポの次」を必ず返す＝脇道に固定されるリスク。横断の優先は §4 最優先（例: protocol v1 が全 WS の前提）に照らす。
