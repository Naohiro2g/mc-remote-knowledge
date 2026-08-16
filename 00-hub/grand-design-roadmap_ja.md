# マイクラリモコン グランドデザイン / 実行ロードマップ

> public 正本世代の粗い相マーカー。日々の task list は焼かず、各 dev session が INDEX・DECISIONS・NOTES から生成する。

## 現在地

**現在は R2 完了・R3 入口**（2026-07-21 public epoch 開始時点）。R1 / R2 / R3 は利用者価値と公開段階、b1〜b6 は同期 release 列であり、別の軸です。

この行は低 drift な粗い相だけを保持します。相を越えるときは DECISIONS 流で更新します（`2026-06-24-03`）。

## 1. 戦略姿勢

- 初学者へ広く案内する前に、導入・観察・復旧の体験を揃える。
- 開発者・学習支援者・OSS contributor へは、判断理由と build-in-public を先行して開く。
- `stable` / `beta` を上下関係にせず、現状の公式提供は観察・検証・学習・貢献の主活動面である `beta` を優先する（`2026-07-22-01`）。
- 生成物の量より、利用者が観察し、自分で正しさを判断できることを gate にする。
- 公開 server package / runbook は `mc-remote-stack`、private ops は `mc-remote-backstage` に分ける。

## 2. 相

| 相 | 状態 | 残る意味 |
| --- | --- | --- |
| R1 — Python 整理 | 技術中核は完了 | 導入文書、sample、配布体験は継続改善 |
| R2 — 認証基盤 | 完了 | pair / token / permission / bridge を回帰 gate として維持 |
| R3 — Scratch 公開 | 入口 | 三層保存、観察面、初学者 UI / 教材、安定運用 package を一つの体験へ閉じる |

`2026-08-16-01`〜`2026-08-16-03`で匿名cloud、一般UGC hosting、Backpackを撤回し、保存・移送を
作品／スプライトのbrowser・file保存とOS clipboardへ再構成した。このため上表R3行の「三層保存」は現行scope
として使わない。`2026-08-16-09`で作品のブラウザ保存をb5、スプライトのブラウザ保存をb6へ配置したが、
R3〜R5の意味と4月へ向けた日程は、他の横断scopeを揃えた最後のR整理で改訂する。それまでは
[Scratch roadmap](../13-scratch-client/scratch-roadmap_ja.md)と
[作品の保存・移送設計](../13-scratch-client/scratch-project-storage-transfer-design_ja.md)を現在地の入力とする。

## 3. 不変の gate

- protocol / plugin / clients の互換主張は test evidence を伴う。
- `live-human` は sanitized evidence record を残す。
- vanilla Java / Bedrock の基線を壊さず、追加観察面は任意導入にする。
- public contributor が archive / backstage を読まなくても判断できる。

## 4. 現在の横断優先

1. public knowledge / stack / backstage の正本境界を運用で定着させる。
2. main stream 1件へ限定したb4のWireScope初期版、Catalog Picker、player poseを進める（`2026-08-16-08`）。
3. ケータリング実践から再構築時間、pairing 負荷、現場の失敗点を集める。long-lived credential の公開 gate は閉じたまま維持し、実需要の確認後に credential-lifecycle slice を再開する。
4. main／substreamとScratch objectの写像はb4を律速させず、post-b4の独立設計・実装sliceで再開する（`2026-08-16-08`）。

個別 repo の「次の一手」は保存せず、その repo の NOTES と contract から都度生成します。
