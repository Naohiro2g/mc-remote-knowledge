# 用語集（terms-glossary）

このプロジェクトの**正典語（canonical terms）の唯一の置き場**。サーフェス（claude.ai / Claude Code）やセッションを跨いで用語が発散する（同じ概念に別の語を当てる）ドリフトを、語を1箇所に pin して抑える。`protocol.json` をクライアントへ投影するのと同じ構図＝正本に置き、各所はここを読む。

- **薄く保つ**：実際に再発し、サーフェス跨ぎで誤解を生む語だけ載せる。網羅は目的でない（陳腐化する）。判定は @import 規律と同じリトマス（`CLAUDE.md`）。
- **発散を見つけたら直す**：別の語が使われていたらここの正典語に寄せる。新概念を鋳造したらここに足す。
- 種まき出典＝セッション・ループ再設計（`2026-06-23-01`）。SSOT 機構としての本格運用は NOTES の起案（用語集 SSOT 化）で継続検討。

## Deployment 構成 / 食事語彙

食事語は認知入口に限らず、判断履歴・比較・言語化に用いる系術語である。各語を技術的実体へ明示的に写像し、いつでも実体を確認できるようにする。`apply` / `restore` / `stop` / `delete` / `resolve` / `render` 等の状態変更操作は、意味の曖昧化を避けるため技術語を正準とする（`2026-07-23-01` / `2026-07-23-03`）。

| 正典表記 | 技術的な意味 | ドリフト注意 |
| --- | --- | --- |
| 献立（preset） | 名前と immutable な revision を持つ、検証済み component 構成の宣言。revision は moving selector を含まない | お品書き（一覧）や、exact deployment 全体を固定する lock と混同しない |
| お品書き（catalog） | registry から作る現在提供中の投影。deprecation / EOL、supported profile、deployment requirements / constraints 等を含む | immutable な全識別空間ではない |
| registry（献立帳） | immutable な base preset revision 群の identity 源 | 現在提供中だけを示す catalog、artifact を置く冷凍庫と混同しない |
| 注文票（order） | 一つの environment に対する human-owned な論理的 desired state | 物理ファイル粒度を含意しない |
| lock（固定結果） | profile / preset / override / resolver・rendering tool / source order を解決した、特定 deployment の secret 値と runtime-owned state を除く exact artifact resolution および non-secret render plan の rerun 源。secret 依存生成物は参照 identity までを固定し、実値注入後の bytes は lock 単独の再現保証に含めない | order、secret store、runtime backup の代わりにしない |
| おまかせ（recommendation） | 目的から preset を推薦する開始方法。説明・判断履歴では日本語系術語を使い、機械 token は英語とする | 具体的な CLI / API surface を用語定義へ焼き込まない |
| 冷凍庫（artifact store） | content-addressed な artifact 保管 | 過去 preset の identity 空間は registry（献立帳）であり、冷凍庫へ二重写像しない |
| venue | 外部管轄の作業現地。Scratch upstream contribution 等で、こちらが正本や運用を所有しない場所 | deployment instance の schema 名へ流用しない |

- `course` は curriculum / カリキュラム側の予約語とし、component 構成には使わない。
- `menu` は日本語と英語で指す対象が反転し得るため、schema / DECISIONS の正典語にしない。日常語としては使ってよい。
- `サーバー` は computing / server-system 文脈（VPS、家サーバー、Games サーバー、Minecraft サーバー等）に予約し、飲食隠喩の役割に無修飾で使わない。給仕・ホール等の具体語と技術的実体の写像は、判断履歴で実際に使う段で確定する。

## セッション・ループ（`claude-ai-guide_ja.md` §7）

| 正典語 | 意味 | 避けたい揺れ |
| --- | --- | --- |
| 経路（path） | 入口から判断に至る道筋。どのサーフェス・どのハブ/スポークを渡り歩くか。**自由**（規制しない） | フロー／パイプライン（線形を含意するので不可） |
| 着地（landing） | 判断・芽が既知の置き場に収まること。**規制対象はここ** | 記録／保存（場所と条件を混ぜがち） |
| sink（着地場所） | 判断・芽が落ちる**場所**。確約＝確定の home（DECISIONS／スポーク §）、捕捉＝NOTES。工房は sink ではない（着地せず湧く） | gate と混同しない（場所 vs 条件）。旧称 Sink 1 / Sink 2 は廃止（`2026-07-16-07`） |
| gate（着地条件） | sink への**着地が有効かを判定する条件**。Gate (b)＝着地妥当性（検証可能なサーフェスでのみ確定を確約へ）＝確約 ↔ 捕捉 の振り分け器 | sink と混同しない |
| park | 未確定・今やらない芽を捕捉（NOTES）へ退避すること | 保留（DECISIONS の状態語 `保留` と紛れる）／放置 |
| escalation-sweep | dev NOTES に park した横断の芽を、セッション終いに hub NOTES へ拾い上げる掃き出し | escalate 単発（sweep＝終い儀式の一括である点が要） |
| 確定搬送票 | dev repo や非リポ側サーフェスで固まった判断を、人間が knowledge リポへそのまま渡す固定 Markdown ブロック。中身だけを運び、DECISIONS の ID 採番・staging・commit 手順は含めない | 要約／申し送り（自由形で揺れやすい） |
| 着地確認依頼 | knowledge リポでの ID 採番・配置・commit/push 後に、元リポへ戻って「正しく着地したか」を確認させる固定 Markdown ブロック | 完了報告（戻り確認が抜ける） |
| セッションクローズ票 | セッション終了時または長時間作業の節目に出す、次回再開用の短い作業状態ブロック。決定の正本ではなく、必要なら NOTES / DECISIONS / 確定搬送票への入口を示す | 長文要約／会話ログ（再開に不要な情報が混ざる） |
| evidence record | 人間参加・横断型実機テストなど再現コストが高い検証を、後から監査できるように `14-evidence/records/<test_id>_ja.md` へまとめた構造化サマリ。搬送票の根拠/検証欄から record path と commit/SHA で参照する | ローカル未追跡ファイル名／会話内の PASS 要約 |
| sanitized artifact | token / pair code / private host / UUID 等の秘密実値・個人識別値を redaction した、`14-evidence/artifacts/<test_id>/` または private evidence 保存先へ置ける証跡 | raw log の公開 commit |
| handoff materials | dev repo 側でセッションを跨いで knowledge へ渡す素材を保持する一時置き場。公式パスは `handoff-materials/<handoff_id>/`、構成は `MANIFEST_ja.md`＋`materials/`、既定 gitignore。正式証跡ではなく、knowledge 着地と着地確認OK後に削除。private ops として保持が必要なら `mc-remote-backstage` へ移す | `14-evidence-handoff/`／root 直下 tarball／dev 側 `records/`・`artifacts/`／frozen archive への追記 |

### 裁き状態（確約 / 捕捉 / 工房）

内容が「どの裁き状態にあるか」の三語（`2026-07-16-06` / `2026-07-16-07`）。サーフェス（＝どこで働くか）と直交する軸。**「面」の字はこの体系の用語として使わない**——英語に潰すと surface になり、サーフェス軸と同一カテゴリ語として混線するため（機械読解・翻訳・LLM コモンズ焼き込み）。三語に共通接尾辞も与えない（共通軸の再発明＝Sink 番号と同じ誤りの反復になる）。

| 正典語 | 意味 | ドリフト注意 |
| --- | --- | --- |
| 確約 | 判断した。確定の home（横断＝DECISIONS 1行／局所＝スポーク §）への有効着地 | 旧称 Sink 1／「確約面」（面は使わない）。英語投影は decided（surface にしない。committed も不可＝Git の commit と衝突し、Git では push まで行って着地＝commit は未着地なので意味論もズレる） |
| 捕捉 | いつか判断する。未確定・今やらない芽の park 先（hub / per-repo NOTES） | 旧称 Sink 2／「捕捉面」（面は使わない）。英語投影は captured（surface にしない） |
| 工房 | 判断しない。独立公開リポ `mc-remote-tinker`。ID 無し・「なぜ」無し・Gate 無し・履歴保証無し・捨ててよい。sink ではない（着地せず湧く）。義務は発見の hub NOTES への1行 sweep のみ（一方向弁） | 砂場/Sandbox（箱庭サーバー sb.mc-remote.com と衝突）。environment channel `dev`（tinkering状態。exposureは別軸・`2026-07-23-01`）と混同しない。英語投影は tinker |
| サーフェス | 「作業する場所」（LLM が動く面＝claude.ai / Claude Code 等）**専用に予約** | 確約・捕捉・工房を「〜面」と呼ばない（英訳で surface に潰れ軸衝突）。詳細は §サーフェス |

### セッションループ状態名

人間が「セッションループの現在地は？」「今どの step/status？」と聞けるように、**step（どの工程か）** と **status（その工程がどういう状態か）** を分ける。step は経路を縛るための手順ではなく、経路自由な作業を現在地として投影するための語。実際の作業は前後・往復してよいが、問い合わせへの返答では次の正典語を使う。

#### step（工程）

| 正典語 | machine key | 意味 | 完了条件 |
| --- | --- | --- | --- |
| 入口整理 | `intake` | repo、surface、作業範囲、読むべき SSOT、既知の制約を確認する | 何をどこで扱うか、最初に読むものが言える |
| 読み込み | `context_read` | AGENTS / CLAUDE / knowledge / 関連スポーク / 既存差分を必要分だけ読む | 根拠ファイル・既存状態・未読リスクが言える |
| 検討 | `deliberation` | 選択肢、理由、却下案、影響範囲を整理する | 判断候補と未確定点が分かれている |
| 検証 | `verification` | 実行サーフェスでテスト・ビルド・差分確認・実機確認を行う | 検証結果、または検証不能な理由が言える |
| 振り分け | `routing` | Gate に従い、確約に確定させるか、捕捉に park するか、追加検証へ戻すかを決める | 行き先（確約 / 捕捉 / 追加検証）が明示されている |
| 搬送 | `handoff` | `確定搬送票` で dev repo / 非リポ側から knowledge リポへ中身だけを渡す | ID 未採番・commit 手順なしの搬送票が出ている |
| ナレッジ着地 | `knowledge_landing` | knowledge リポ側でレビュー、ID 採番、配置、stage、commit、push を行う | commit SHA、着地先、DECISION ID、調整点が言える |
| 着地確認 | `landing_verification` | 元リポ側で knowledge 着地先を読み、元の実装・検証・搬送票と照合する | `着地確認OK` または `着地差分メモ` が出ている |
| 掃除 | `cleanup` | 解決済みの NOTES / park / 未着地メモを `[→DEC <ID>]` / `[done]` 化または削除する | 再開時に古い未決が入口に残らない |
| 終了 | `close` | `セッションクローズ票` を出し、次回再開に必要な状態だけを残す | 次に読むもの、次の一手、未着地物が短く言える |

#### status（状態）

| 正典語 | machine key | 意味 | 避けたい揺れ |
| --- | --- | --- | --- |
| 未開始 | `not_started` | まだその step に入っていない | 未着手／未処理の混在 |
| 進行中 | `in_progress` | agent が今その step を進めている | 作業中（広すぎる） |
| 人間待ち | `waiting_human` | 命名・確定・権限・外部操作など、人間判断なしに進めると危険 | 保留（park と紛れる） |
| 検証待ち | `waiting_verification` | 実行サーフェス、実機、CI、外部事実確認が必要 | できない（権限不足と混ざる） |
| 着地待ち | `waiting_landing` | 中身は固まり、knowledge リポ側の ID 採番・配置・commit/push を待つ | 完了待ち（どの完了か不明） |
| 確認待ち | `waiting_confirmation` | 着地後に元リポ側の照合、または人間の確認を待つ | レビュー待ち（PR review と紛れる） |
| park済み | `parked` | 捕捉に退避済み。捨てていないが今は進めない | 保留／放置 |
| 完了 | `done` | その step の完了条件を満たした | 済み（何が済んだか曖昧） |
| ブロック | `blocked` | 同じ阻害条件が続き、外部入力や状態変化なしに前進できない | 難しい／未確定（まだ進められるものと混ざる） |

### 言語間投影の既定

全文翻訳の正本は作らない。ズレると困る語だけ、推奨投影語と machine key を pin する。

| 正典語 | 推奨英語投影 | machine key |
| --- | --- | --- |
| セッションループ現在地 | Session Loop Current Position | `session_loop_current_position` |
| 入口整理 | Intake | `intake` |
| 読み込み | Context Read | `context_read` |
| 検討 | Deliberation | `deliberation` |
| 検証 | Verification | `verification` |
| 振り分け | Routing | `routing` |
| 搬送 | Handoff | `handoff` |
| ナレッジ着地 | Knowledge Landing | `knowledge_landing` |
| 着地確認 | Landing Verification | `landing_verification` |
| 掃除 | Cleanup | `cleanup` |
| 終了 | Close | `close` |
| 未開始 | Not Started | `not_started` |
| 進行中 | In Progress | `in_progress` |
| 人間待ち | Waiting for Human | `waiting_human` |
| 検証待ち | Waiting for Verification | `waiting_verification` |
| 着地待ち | Waiting for Landing | `waiting_landing` |
| 確認待ち | Waiting for Confirmation | `waiting_confirmation` |
| park済み | Parked | `parked` |
| 完了 | Done | `done` |
| ブロック | Blocked | `blocked` |
| 確定搬送票 | Decision Handoff Ticket | `decision_handoff_ticket` |
| 着地確認依頼 | Landing Verification Request | `landing_verification_request` |
| セッションクローズ票 | Session Close Ticket | `session_close_ticket` |
| 投影 | projection | `projection` |
| context-local 投影 | context-local projection | `context_local_projection` |
| 確約 | Decided | `decided` |
| 捕捉 | Captured | `captured` |
| 工房 | Tinker | `tinker` |
| サーフェス | Surface | `surface` |

## 判断スコープ

| 正典語 | 意味 | ドリフト注意 |
| --- | --- | --- |
| マイクロワールド | 問いに必要な因果関係が閉じた、境界づけられた空間／コンテクスト。問題原因・境界契約・必要な相互作用を含む範囲で、条件に応じて大きさを変えられる | 単に小さい範囲、局所だけを見ること。問題を成立させる因果関係まで切り落とさない |
| mind-size | 選んだマイクロワールドを、人間の認知容量・LLMのコンテクスト容量に収まる単位へ調整する尺度。Scratchがマイクロワールドなら、ブロック／スタックはmind-sizeの単位になり得る | マイクロワールドの別名、常に固定サイズの最小単位 |

両語はPapertの語法を、学習支援とLLM支援開発の検証スコープへ適用したもの（DECISIONS `2026-07-19-05`）。

## サーフェス

| 正典語 | 意味 |
| --- | --- |
| サーフェス（surface） | LLM が動く面（claude.ai / Claude Code 等）。各々独立サンドボックス（`knowledge-repo-design_ja.md` §2） |
| 合成サーフェス | 共有ベース instructions ＋ ツール固有 overlay で構成する運用面（NOTES `2026-06-22` / DEC `2026-06-22-05`） |
| 実行サーフェス | 対象作業に必要なコード・実機・test を動かし、結果を検証できるサーフェス。特定の製品名や model 名に固定しない |
| head / hands | 決定の handoff 契約での役割。head＝非リポ側（claude.ai 等、中身だけ渡す）、hands＝リポ所有サーフェス（ID 採番・配置・実行）。`2026-06-22-03` |

## Stream

| 正典語 | 意味 |
| --- | --- |
| identity | player / client の継続主体。stream key そのものとは同一化しない |
| main stream | identity に対する既定の executor stream |
| substream | 同じ identity が追加で持てる独立 executor stream |
| executor stream | `1 stream = 1 connection = 1 build state`。world / origin / build state は stream ごとに独立 |

main / substream の方向は `2026-07-21-07`、土台は `2026-06-24-01`。Scratch object との写像は b4 scope freeze 前の未決。
