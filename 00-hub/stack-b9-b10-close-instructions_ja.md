# Stackのb9／b10の期間のclose分類と、Backstageの返却からの確認

> Stackとbackstageは、rc1からgate coordinatorの管轄に戻った（`2026-10-18-01`）。b9とb10のgateを閉じたときは、human ownerの直轄の
> 間で、Stackとbackstageにcloseの分類を頼んでいなかった。Backstageは自分の分を後から分類して返した（2026-10-19、Backstage
> `handoff-receipts/2026-10-18-b9-b10-close-return_ja.md`、main `e3838bc`）。この依頼は、Stackの分の分類と、その返却票にあった
> Stackへの確認4件です。参照するknowledge commitは、この依頼が入ったmainのcommitです。rc1の分は返却済み（rc1の期間の
> directoryは無い、2026-10-19）なので含めない。

## 1. handoff-materialsの分類

- 対象：Stackの`handoff-materials`のうち、まだcloseの分類をしていないdirectory。b9とb10の期間（2026-10-04〜10-17）に限らず、
  それより前でも未分類のものは含める
- 分け方は他のcomponentと同じ（`00-hub/rc1-gate-close-instructions_ja.md`の「共通」）
  - ① knowledgeのevidenceへ移す：後から同じ観測を再現しにくいもの
  - ② 自repoで持ち続ける：後続で使うもの。何に使うかと、捨ててよくなる条件を書く
  - ③ 捨てる：knowledgeか公開物に同じ内容があるもの、一時的なもの
- privateな運用の記録（host、IP、account、backupの中身など）は①に入れない。backstageへ移すべきものがあれば、そう書く
  （`2026-07-21-03`）
- ①の元は、knowledgeへ全文が移ったことをcoordinatorが確かめるまで消さない
- 返却：directoryごとに①②③と理由、①はfile一覧（bytes、SHA-256）と収容先の案、②は使い道と捨ててよくなる条件。実際に
  読んだknowledgeのcommitを書く

## 2. Backstageの返却票にあった確認4件

それぞれ、今の状態と、rc1の公開VPSの別セットへの切り替え（`2026-10-18-02`）に入れるかの案を返す。

1. JSTのlogのtimestampの修正：未適用と聞いている。rc1の別セットで入れるか
2. 第2セット用の予約port：rc1の別セットに使うか
3. 公式backstageをStackの立ち上げの仕組みへ移すこと（`2026-09-29-01`）：rc1に入れるか、後にするか
4. 旧projectの更新snapshotの蓄積：旧セットで`.mcrctl`が50 GBに育っていた。今の実装で同じことが起きるか。起きるなら、
   別セットへの切り替えの前に手当てが要るか

Backstageの返却票の残り2件（公開VPSのrollbackの実試験、手元の配信の終了）は、閉じる案でhuman ownerの判断に回した。
