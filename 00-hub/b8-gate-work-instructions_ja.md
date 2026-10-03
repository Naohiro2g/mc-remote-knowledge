# b8横断release gate 着手依頼

> 状態: **完了・履歴**。b8横断release gateは2026-10-03にCLOSEDとなった（`00-hub/release-gate-notes_ja.md`の2026-09-30の節）。
> 現在の指示ではなく、b8で出した票の記録として残す。

> b8横断release gate（`00-hub/release-gate-notes_ja.md`の2026-09-30の節）で、確認票の返却を受けて出す着手依頼です。
> blockerと非blockerの線引き、依存順、日程の確認点は、human ownerの了承（2026-09-30）によります。
> 各担当は、自分の節と「共通」を読んでください。

## 共通

- 依存順: Scratchのfixtureとobserver → McRemote／Pythonの取り込み → exact setの凍結 → 通常devでのJAR差し替えと実機試験 → release
- 日程: releaseの目標は10/3。**確認点は10/1の終わり**で、Scratchのblockerがそろったかを見る。そろわなければ、その時点で
  日程を相談する。10/2に取り込みと凍結、10/2〜10/3に実機試験を置く
- 非blocker（b8では待たない。b9のgateを開くときに扱う）: Scratchのサウンドのlearner block、pickerのalias、b7 release後の是正候補
  3件、post-b7のpark 2件（WireScopeの時刻表示と配置、McRemoteカードの説明）、各repoのREADMEの残り。時間が余っても、
  blockerを先に終える
- 返却: `release-gate-notes_ja.md`の確認票の形式で、変わったところだけを追記として返す（branch／commit、artifactのbytes／
  SHA-256、実行したtestと結果、未検証の境界）。`knowledge contract commit`には実際に読んだSHAを書く
- しないこと: 他repoへの着手、shared環境の変更、人間参加の試験、tag／releaseの公開。これらは凍結の後に別の票で示す

## Scratch editor（WireScope）— blocker、最優先

1. **B8共有fixtureのsuccessorを発行する。** 今の`entity-particle-v23.2.json`（`0735a9c`、59 case）に、次を足す
   - サウンド（wire §5.8.3「サウンド」）: `world.playSound`／`world.playBlockSound`のparams、`options`（未知の項目、`null`、`{}`）、
     volumeの範囲、`pitch`と`note`の排他と範囲、`kind`の語彙、receiver、`unknown_sound`、`no_block`、検証の順序と同時に
     起きたときの優先
   - resource ID（wire §5.0.2、`2026-09-30-06`）: block、dimension、particle、entity、soundのそれぞれについて、無印（`minecraft:`を
     補って受ける）、完全修飾（受ける）、非正準形（種類ごとのreasonで拒否。dimensionは`invalid_params`、他は`unknown_*`）
   - 発行したら、commit、file名、bytes、SHA-256、case数を確認票の追記で返す。McRemoteとPythonがこれを取り込む
2. **Protocol mirrorとWireScopeをサウンドとresource IDに追従させる。** `world.playSound`／`world.playBlockSound`／`unknown_sound`／
   `no_block`の認識、validator、sanitizerを足す。validatorはparticle／entityの無印を拒否しない（§5.0.2）
3. **Scratchからの観測を直す。** B8 entityの4 method、typed particle、particleのFAST通知、サウンド2 methodが、Scratch側のallowlistで
   落ちないようにする（確認票で再現した経路）
4. **learner blockとpickerの変更をcommitする。** entity／particleの9ブロック、カタログのID一覧ブロック、pickerの日本語名と検索。
   非blockerだが、実装済みなのでb8のcandidateに入れる
5. **candidateのartifactを作る。** push済みのcommitから、GUI、Bridge、WireScope ZIPとdetached manifestを作り、identityを返す。
   Pythonは、このWireScopeのsource commitから同梱物を作り直す

1〜3が10/1の終わりの確認点の対象。real-browserでのWireScope確認は、凍結の後の統一実施票で頼む（Scratch担当は独立の
Chromiumを使える）。

## McRemote

1. **今すぐ:** candidate `b3b3ba8`のJARで、ローカルのlive-auto（`--expect-mc 1.21.11`）を流す（無印IDを受ける変更の後の分）
2. **今すぐ:** fresh installで認証が既定でONになることを、ローカルの新しいserver directoryで確かめる（確認票の未検証の境界）
3. **Scratchのfixtureが出たら:** bytesをそのまま取り込み、digestをtestで固定して、consumer testを通す。無印のresource IDのcaseが、
   無印を拒否していた公開済みb7のJARでは落ちることを一度確かめる（b8 gateのacceptance）
4. candidateを更新したら、branch／commitと1.21.11向けJARのbytes／SHA-256を返す
5. できれば: 正式段階のrelease jobとrelease titleの導出（`2026-09-27-03`）。未実装であることだけを理由にb8を止めない
   （release運用と責務分担 §14）
6. 旧`b5.`／`b7.`キーの移行の件は、予告どおりb8の実装報告の搬送票で訂正を出す

## Python client

1. **Scratchのfixtureが出たら:** successor fixture（サウンドとresource IDのcase）を取り込み、consumer testを通す
2. **ScratchのWireScope artifactが出たら:** そのsource commitから同梱WireScopeを作り直し、サウンドとresource IDへの追従を確かめる
3. candidateを更新したら、branch／commitとCI成果物（wheel／sdist）のbytes／SHA-256、同梱WireScopeのsource commitを返す
4. Windows: human ownerがb8の公開直後に、Release wheelのURLを使って入口ルート（`docs/windows-b8-entry_ja.md`）を確かめる。
   b8 releaseを止める条件にはせず、結果はb9のPyPI登録の判断材料にする。手順書はこのままでよい

## Stack

1. dev-integrationの読むだけの事前確認（既に許可済み）の結果を、10/1のうちに返す
2. JARの差し替えは10/2の凍結の後に、別の指示で頼む
