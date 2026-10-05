## 確定搬送票

- 搬送元 repo: scratch-editor
- 搬送元 surface: Codex
- 搬送元 branch/commit: `agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`上の未commit差分。
- 作成日: 2026-09-30
- 種別: 局所決定
- 決定: ブロックピッカーに、ブロックID＋日英の短い名称だけの版別辞書を同梱する。1.21.11は1,154件、26.2は1,184件。日本語／ja-HiraはID＋日本語名と下段右寄せ英語名、英語はID＋英語名。候補ごとに区切り線を付け、検索結果の候補件数を表示する。検索はID・日英名称への空白区切りANDで、英字大小文字・全角半角を正規化する。
- 理由: ユーザーの実装指示と既存の表示／検索metadata方針に従い、識別・検索に必要な名称へ範囲を限定する。利用時の公式取得を追加せず、版別に明示更新できる。
- 却下案（3件まで）: ピッカー操作時の公式ファイル取得。言語ファイル全体の同梱。エンティティ名・説明文の追加。
- 影響: Scratch GUI内の表示・検索だけ。CURRENT catalogの候補、wire、catalogHash、選択時のID／stateは維持する。未収録の版／IDはIDのみを表示する。
- 根拠/検証: knowledge `fc208b8b2a8a259447f2be65ce140c1af29ddf99`の`13-scratch-client/scratch-roadmap_ja.md`、`scratch-block-value-projection-design_ja.md` §7。unit/deterministic: GUI全70 suites／512 tests PASS（1 skipped）、lint 0 errors、i18n:src、build:dev、diff check PASS。ブラウザ素材は同directoryの`browser-smoke.cjs`／`.log`／`block-picker.png`で、テスト用catalogによる表示確認。正式evidenceや実plugin live-humanではない。
  表示調整時はknowledge `16668c5e5152d593c4b184939c9a9e723529d6e9`のruntime／INDEX／projection §7に再照合。追加後の関連4 suites／29 tests、変更箇所lint、i18n:src、build:dev、diff check PASS。テスト用catalogでgold 5件、door 42件（trapdoor含む）、英語名右寄せと区切り線を確認し、`block-picker-gold.png`／`block-picker-door.png`／`block-picker-door-long.png`を追加。
- 既に変更した実装/文書: GUI picker JSX／CSS、`mcremote-block-names.js`、版別名称JSON／sources／README、更新script、GUIローカライズ、関連unit tests、`mc-remote/README.md`。公式metadata・asset index・JAR・日本語assetのSHA-1を照合して抽出。元JAR・言語ファイル全体は配布物へ含めない。個別の再配布許諾・適法性確認済みとは主張しない。
- ナレッジ着地希望: Scratch roadmapのピッカー実装現在地を捕捉。新しいwire contractやversion bumpは不要。
- 捕捉 cleanup: 捕捉またはScratch担当への移管を確認した後、この搬送directoryを整理する。元コードは未commitのため正式artifact identityは未確定。
- 着地後の確認戻り先: scratch-editor担当。`NOTES_ja.md`の「カタログピッカーの日英表示・検索」。
