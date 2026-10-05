# ブロックピッカーの日英表示・検索

- 作成日: 2026-09-30
- repo / surface: scratch-editor / Codex
- branch / base: `agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`上の未commit差分。
- ユーザー指示: ブロックID＋日英の名称だけを保存してピッカーの表示・検索を実装する。
- knowledge参照: `fc208b8b2a8a259447f2be65ce140c1af29ddf99`のScratch roadmap、Scratch block value projection §7。
  表示調整時は`16668c5e5152d593c4b184939c9a9e723529d6e9`のruntime／INDEX／projection §7を再照合。
- 搬送票: `materials/knowledge-handoff_ja.md`。局所実装の捕捉用で、外部送信はしていない。
- ブラウザ素材: `materials/browser-smoke.cjs`、`materials/browser-smoke.log`、`materials/block-picker.png`。
  `block-picker-gold.png`（5件）、`block-picker-door.png`（42件、trapdoor含む）、`block-picker-door-long.png`も同directory。
- ブラウザ再現: repo rootでプレビューを8601へ起動後、`node handoff-materials/2026-09-30-block-picker-names/materials/browser-smoke.cjs`。
- 検証: GUI全70 unit suites／512 tests PASS（1 skipped）、lint 0 errors、i18n:src、build:dev、diff check PASS。ブラウザはテスト用catalogの表示・検索・ID適用を確認。
  右寄せ・区切り線・候補件数の追加後は関連4 suites／29 tests、変更箇所lint、i18n:src、build:dev、diff checkとブラウザ表示確認PASS。
- non-claim: 個別の再配布許諾確認、実plugin live-human、commit／push、B8への統合・release gateを主張しない。
- cleanup: knowledgeへの捕捉またはScratch担当への移管を確認して素材を整理する。現在の引継ぎ先はScratch担当、参照identityは上記baseと未commit差分。
