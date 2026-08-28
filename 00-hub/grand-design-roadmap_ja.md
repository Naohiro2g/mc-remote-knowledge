# マイクラリモコン グランドデザイン / 実行ロードマップ

> public 正本世代の粗い相マーカー。日々の task list は焼かず、各 dev session が INDEX・DECISIONS・NOTES から生成する。

## 現在地

**現在はR1／R2を基線として維持し、R3進行中**（2026-08-26更新）。R1／R2／R3は利用者価値と
成熟段階、b6／b7／b8／rc／stableはproduct release列、ケータリング／教材／広報はreleaseをまたぐ
並走trackであり、別の軸です（`2026-08-26-09`）。

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
| R1 — 作れる | 完了・回帰基線 | Python／API／建築機能を各releaseで維持する |
| R2 — 安全につながる | 完了・回帰基線 | pair／token／permission／Bridge／復旧境界を各releaseで維持する |
| R3 — 学べる・教えられる | 進行中 | Python／Scratch、WireScope、保存・再利用、ケータリング運用、教材、第三者setup／復旧を一つの体験へ閉じる |

R3は旧R3-A／B／Cを計画単位にせず、API learning surface、保存・再利用、観察・debug、release／運用package、
curriculum／teacher handoffの能力trackで管理する。これは旧記録を削除する意味ではなく、作業順、価値gate、
component sliceを同じ文字suffixへ重ねないための現行整理である。R4はpost-Aprilの価値目標が定まるまで新設しない。

初回stableまでのrelease列、Paper 26.x対応、method状態は
[betaから初回stableまでのreleaseロードマップ](../10-protocol/beta-to-stable-release-roadmap_ja.md)、
Scratch固有の現状は[Scratch roadmap](../13-scratch-client/scratch-roadmap_ja.md)、保存境界は
[作品の保存・移送設計](../13-scratch-client/scratch-project-storage-transfer-design_ja.md)を正とする。

## 3. 2027年4月までの粗い時間軸

| 時期 | product | 並走track |
| --- | --- | --- |
| 2026-08末 | b6／protocol 23.0.0公開済み | sign、poke、browser保存を横断統合 |
| 2026-09前半 | b7／23.1.0のconcept sliceを再固定 | README／sample Pass A、homepage骨格、Paper 26.2 pulse |
| 2026-09中旬〜後半 | b8／条件付きb9、月末API freeze | README／sample Pass B、ケータリングPC／kitで更新・rollback検証開始 |
| 2026-10 | rc、新API追加停止 | 外部testerへ準備済み環境、手順、検証票、feedback導線を提供 |
| 2026-11 | 初回stable | stable導入／更新情報と採用Paper 26.x supportを公開 |
| 2026-12〜2027-01 | stable保守 | 運用手順化、機能実現位置とsampleを使った教材・学習path作成 |
| 2027-02 | fixes中心 | 別支援者によるcold setup、開始、障害復旧rehearsal |
| 2027-03 | classroom artifact freeze | 教材固定、本番相当dry run、修正だけを許可 |
| 2027-04 | 3月に選定したstableで新学年開始 | 学習者観察を後続releaseへ還流、独自Mob／agent型建築curriculumを段階開始 |

## 4. 現在の横断優先

1. 各public repoのREADMEとsample codeを人間向けに整理するPass Aを、b7設計と並行して直ちに始める。
2. direction／navigation、entity lifecycle、空間query、player別preview、world effectの候補を、学習pathと実装単位からb7〜b9の縦sliceへ再編する。
3. b6直後のPaper 26.2 compatibility pulseを行い、wire不変なら影響外client PASSを再利用する。
4. 9月中旬からケータリングPC／kitでb7→b8→rc→stableの更新、rollback、再pairing、file退避を経験する。
5. 10月rcから外部testerが会話履歴なしで開始・更新・復旧・feedbackできる入口を用意し、homepage／release情報／技術記事を並走させる。
6. long-lived credentialの公開gateは閉じたまま、ケータリングで実需要を観察してから再開する。

個別 repo の「次の一手」は保存せず、その repo の NOTES と contract から都度生成します。

README／sample trackの説明正本は
[README・sample近代化ロードマップ](readme-sample-modernization-roadmap_ja.md)です。本格的な独自Mob、
独自AI、教育版agent式建築の再構成、Scratch extension分割は初回stableへ押し込まず、2027年春からの
curriculum／product trackとして段階化します。

## 5. 不変の gate

- protocol / plugin / clients の互換主張は test evidence を伴う。
- `live-human` は sanitized evidence record を残す。
- vanilla Java / Bedrock の基線を壊さず、追加観察面は任意導入にする。
- public contributor が archive / backstage を読まなくても判断できる。
