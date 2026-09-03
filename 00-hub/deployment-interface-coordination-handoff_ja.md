# deployment interface（2026-08-31-01）coordination — 引継ぎ

> 状態: coordinator交代（2026-09-03、解任）。以下を読んでから再監査する。
> 本票はrelease承認ではなく、誤った進行を止めて検証可能な現在地を渡すための引継ぎである。

## 1. 何が起きたか

b7 release close直後、`00-hub/NOTES_ja.md`の`2026-08-31-01`優先項目（Scratch–Stack deployment interface）が
一cycle放置されていたことに気づき、着手指令を出した。Stack・Scratchとも急速に実装を進め、一度は
Stack担当がScratch/Bridge imageを契約違反で代理buildする事故があったが、これは検出・是正できた。

その後、coordinatorが§9横断縦slice（実environment apply）を進めようとして、**McRemote plugin（server側
artifact）のexact identityを一度も指示に含めないまま**指示を出し続けた。Stack担当は独自に「b6 plugin」で
準備を進めていたらしく、この不整合により半日以上が無駄になった。

さらにcoordinatorは、Stack側の`mc-remote-stack/docs/preset-resolution-design_ja.md`に「instance
（hostname ref・port・volume roleの割当）」という、複数presetの並行稼働を前提にした標準機能が既にある
ことを知らず、「別portで並行できるか確認が必要」という的外れな前提で指示を組み立てた。過去に実際、
公開VPSサーバーへ複数presetが同居していた実績があるとの人間指摘があった。

最後に、`00-hub/deployment-interface-design_ja.md` §10「今回作らないもの」に**「McRemote専用server
image」が明記されている**ことを見落とし、Plugin配布方式（Scratch/Bridgeと同じOCI digest-lock方式か、
既存の`mcrctl artifact import-reviewed`方式か）を確認せず指示を出そうとした。これも人間の問い直しで
発覚した。

いずれも、**手元にあるSSOT／component側の公開設計文書を読めば分かることを読まずに指示を出した**という
同じ構造の誤りである。b7の前coordinatorの失敗（他repoの内部事情を推論・断定する）とは違う型の誤りで、
「読めば分かることを読まずに進める」という手抜かりだった。

## 2. 確定している事実（identity照合済み）

| 対象 | identity | 状態 |
| --- | --- | --- |
| Stack | `agent/deployment-interface-2026-08-31-01@410b2c11a054915b5e2dd53e5fffc645c1f3ffba` | renderer／apply／doctor実装・決定論的検証済み（485 tests PASS）。remote確認済み |
| Scratch contract/image | `agent/scratch-deployment-interface@4c893bd532002d9216665c5c9b9825e09ede1e7c` | product/runtime config分離、contract、正式OCI image（GHCR、Scratch自身のCI経由）実装・検証済み。remote確認済み |
| preset | `classroom@1` | 上記2つの正式identityから再構成済み（コード面のみ、live未実施） |
| McRemote plugin | `mc-remote-1.21.11-2301.0.0b7.jar`、222,951 bytes、SHA-256 `f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9` | b7 release JAR。**deployment interfaceへの受け渡し方式は未確認のまま指示未送信** |

## 3. 未解決・要確認

1. **McRemote plugin配布方式**: `deployment-interface-design_ja.md` §10に「McRemote専用server imageは
   今回作らない」とあるため、Scratch/Bridgeと同じOCI digest-lock方式の対象外と読める。Stack側の既存
   `mcrctl artifact import-reviewed`（`preset-resolution-design_ja.md`記載）を使う想定と推測されるが、
   **Stack担当への確認は行っていない**。次のcoordinatorが最初に確認すべき事項。
2. **Stackが独自に進めていた「b6 plugin」での準備**: 内容・再利用可否ともに未確認。無駄にした可能性が
   高いが、断定していない。Stack担当へ確認要。
3. **§9横断縦slice**: 一度も実environmentでend-to-end実行されていない。実施時間は未知数（このsession中に
   繰り返し不正確な前提で指示を出したため、正確な所要時間の見積もりが一度も成立していない）。
4. **複数preset並行稼働**: Stack `preset-resolution-design_ja.md`の「instance」機構で標準対応と読めるが、
   これも実際に確認していない（読んだのは該当1行のみ）。

## 4. 禁止事項（今回の失敗から）

- component側の公開設計文書（`deployment-interface-design_ja.md`全文、Stack `docs/`配下の関連文書）を
  **通しで読まずに**指示票を書かない。1行のgrepで済ませない。
- 「〜という方式のはず」を確認せず指示へ書かない。分からなければ先にcomponent担当へ聞く。
- exact set（source、artifact、plugin、preset全部）を揃えずに実行系の指示を出さない。

## 5. 次のcoordinatorが最初に行う監査

1. `00-hub/deployment-interface-design_ja.md`全文を通読する（今回は§8・L244-245しか参照していない）。
2. Stack `docs/preset-resolution-design_ja.md`全文を通読し、instance機構とMcRemote plugin受け渡し方式を
   正確に理解する。
3. Stack担当へ「b6 pluginでの準備」の内容と再利用可否を確認する。
4. 上記が揃ってから、§9縦slice実施のexact set・instructionを組む。

## 6. セッションクローズ票

- repo: `mc-remote-knowledge`
- surface: deployment interface（`2026-08-31-01`）coordinator
- branch/commit: `main`／本票を含むcommit
- 作業範囲: b7 release close後の優先backlog着手指令〜§9縦slice準備
- 今回やったこと: Stack/Scratchへ着手指令、契約違反（image代理build）の検出・是正、CI failureの根本原因確認・是正確認、preset再構成の照合
- 変更ファイル: 本票、`00-hub/NOTES_ja.md`
- 検証: 全branch/commitのGit identity照合、GHCR image digest実在確認
- 未完了: §9横断縦slice未実施、plugin配布方式未確認、b6 plugin準備内容未確認
- 次に読むもの: 本票§5
- 次の一手: 本票§5の監査から再開
- 未着地の搬送物: なし（未送信の指示票は本票に転記済み、そのまま使わない——plugin配布方式確認が先）
- NOTES/DECISIONS: `00-hub/NOTES_ja.md`の該当行は現状のまま維持（本票を参照先として追記可）
- 注意点: b7 release自体（McRemote/Python/Scratch protocol release）は本件と独立に完了・CLOSED済み。今回の
  混乱はdeployment interface（`2026-08-31-01`）作業に限る
