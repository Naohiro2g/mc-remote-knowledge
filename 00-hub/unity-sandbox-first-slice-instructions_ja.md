# 公開Unity箱庭の最初の区切りを作る依頼（mc-remote-unity-sandbox）

> 公開Unity箱庭を最優先にした（`2026-11-13-04`、スポークは`19-unity/README_ja.md`の「公開Unity箱庭」）。最初の区切りは、
> 1台のPCで、今のScratchからBridgeを通して、Unity箱庭のserverへブロックを置き、Unity Webの画面に出ること。この票は、
> そのうち、hubの決定とScratchの返却を待たない部分（作る順番の1〜3）の依頼です。4（TCPの受付、pairing、Scratchを通す）は、
> hubで決めた後に、新しい票で頼む。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 入力

- 実装担当のレビュー返答（`handoff-materials/2026-11-13-unity-sandbox-ideas-review/`）と、それへのcoordinatorの突き合わせ
  （human ownerが渡す）。採ったものは、下の「決まっていること」と「作るもの」に書いた
- このrepoの設計メモ（`docs/unity-shared-sandbox-draft_ja.md`、`docs/unity-internal-preparation_ja.md`）とローカルデモ
- 4つの操作の意味、結果、error：`10-protocol/wire-format-design_ja.md`と、minecraft-remote-toolingの共有fixture

## 決まっていること（守るもの）

- `2026-11-13-04`：世界のモデルはMinecraft 1.21.11に準拠する（高さは-64〜319、地面も置き換えられ、リセットで戻す。blockは
  IDとstateで持つ）。pairingは、Unity Webのchatで`/mcremote pair NNN-NNN`と打って承認する。名前は「Unity箱庭」と
  「Unity箱庭のserver」
- 経路はBridge → TCP → Unity箱庭のserverの1本にする。serverに、Bridgeと同じ役のWebSocketの入口を持たせない
- 世界のモデルは、`UnityEngine`に頼らないC#にする。serverの中は、1行を読み書きするTransportと、JSON-RPC、認証、世界の層を
  分ける（実装担当の案）
- 表示同期（Unity箱庭のserverとUnity Webの間）は、このrepoの中の取り決めにする。knowledgeのprotocolにしない
- Minecraft（Mojang）の素材を入れない（`2026-11-11-02`⑤）。日本語のfontは、再配布できるlicenseのものにし、出どころを記録する
- 一般用途のC# Client Libraryの`src/`を参照しない。配布、公開の配信、release workflowは足さない（このrepoの`AGENTS.md`）

## 作るもの（この順に）

1. **世界のモデルと単体test**
   - 1.21.11の地上の世界の高さ（-64〜319）。水平の広さと9区画の原点は、設計メモのとおり
   - 地形：地面の最上段はy=62、足はy=63。その下の層は担当の案
   - 学習用のblock：設計メモの6材質、空気、TNT。値はIDとstate（`minecraft:gold_block`など）。あとでblockを足せる形にする
   - 4つの操作（`chat.post`、`world.setBlock`、`world.getBlock`、`world.setBlocks`）の、世界の側の意味
   - リセット（`worldEpoch`）と、変更の通知（`seq`と、置いた`streamId`）
   - 結果とerrorは、wireと共有fixtureに合わせる。合わせ方が決まっていないもの（範囲の外、まだ無いblockなど）は、仮の形を
     このrepoの取り決めにせず、案として返す。`setBlocks`で一度に変えられる量の上限も、案として返す
2. **ローカルデモのUnity Web build**
   - 想定のbrowserで、6材質、歩く、照準、日本語の表示を確かめる
   - 画面に足すもの：区画のラベル、区画へのワープ、置いた所を光らせる演出、chatの表示と入力（入力中はマウスのロックを外す）
   - Scratchと左右に並べたときの表示と、フォーカスが外れたときの動きを確かめる
3. **Unity箱庭のserverと表示同期**
   - 描画しない.NETのserverから、Unity Webのfileを配り、表示同期でUnity Webへ`snapshot`と変更を渡す
   - 表示同期の形は、実装担当の案（WebSocketの上で1つのmessageに1つのJSON。`snapshot`、`blockDelta`、`chat`、`streamUpdated`、
     `approvePair`、`resync`）に、次を入れる
     - 画面とstreamの結び付きを、接続より長く持つ（browserに残る画面のID）。tokenを何に結ぶかはhubで決めるので、結ぶ先を
       差し替えられる形にする
     - `setBlocks`の変更は、範囲と置いたblockで送り、セルに広げない。`snapshot`の大きさの上限の案を返す
     - `approvePair`は、chatの`/mcremote pair NNN-NNN`から送る。codeを試せる回数に上限を置く。`auth.pairBegin`、
       `auth.pairPoll`との結び付きは4で作る
     - WireScopeのIDは入れない（扱いが決まっていない）
     - 切れている間も歩けて、つなぎ直したら状態を取り直す
   - `dotnet test`で、模擬のUnity Webを使って表示同期を通すtestを作る。TCPとpairingの部分は4で足す

Unity Editorの版は`19-unity/README_ja.md`の「現在地」に従い、使った版を記録する。

## 返却

- 実際に読んだknowledge commit
- PRの番号、head、CIのrun（あれば）。mergeはhuman ownerが判断する
- 1〜3でできたことと、確かめ方（test、Unityの版、browserと端末）
- 1で、wireと共有fixtureに合わせられなかった結果とerrorと、その案。`setBlocks`の上限の案。地形の下の層
- 表示同期の形（messageとfieldの一覧）と、このrepoで書いた文書の場所
- fontの名前、license、出どころ、大きさ
- 4に向けて、hubに決めてほしいこと（Minecraftでないserverのhello、tokenと画面の結び付き、blockの一覧とcatalog、serverが
  応える最小の組）への案があれば
- 確かめられなかったことと、その理由

## coordinatorがすること

- PRとmerge commitを、GitHubのAPIで照合する
- Scratchの返却（`00-hub/unity-sandbox-scratch-instructions_ja.md`）と合わせて、hubで決めることの案を作り、human ownerに見せる。
  決まったら、4の票を新しいfileで出す

## 返却と照合（2026-11-15）

Unity担当は、knowledge `b4b23631fc6f053fe4e228bb0447c9b4b9502901`を読んだ。返却は、返却サマリと確定搬送票（既定のport）で、
human ownerが会話で渡した。coordinatorはGitHubのAPIで、mainが`958b676e293427165e872d9abd7b5bfc4173efd6`（PR #1のmerge
commit）のままで、PRが#1だけであることを確かめた。1〜4の実装はcommitされていないので、PR、head、CIは無く、GitHubでは照合
できていない。

1. **できたこと**：Unity `6000.6.8f1`（Linux、Built-in Render Pipeline、Input Manager、WebGL）
   - 1：`UnityEngine`に頼らない世界のモデル（`Code2Create.UnitySandbox.World`）。基本の10種類のblockとcatalogHash、12のmethodと
     FASTのnotification、`out_of_bounds`（`2026-11-14-04`の形）。`setBlocks`の上限は32,768で、越えると`work_limit_exceeded`
     （McRemoteの1要求のwork上限と同じ意味）。`snapshot`に総セルの上限は置かず、まとめて小さく送る
   - 2〜3：Unity Webと表示同期のserver（`Code2Create.UnitySandbox.Server`）。表示同期は`/ws/sync`で、serverからは
     `snapshot`、`blockDelta`、`chat`、`streamUpdated`、`pairResult`、Unity Webからは`resync`、`approvePair`、`chat`。文書は
     このrepoの`docs/unity-sandbox-display-sync_ja.md`。画面のIDはほかの画面へ流さない
   - 4（票を出す前に作った）：TCPの受付（portの既定は`25585`、`2026-11-15-01`）、helloより前の拒否、`pairing_id`で相関し
     別のTCPをまたぐペアリング、helloの`server`（`{ "name": "mc-remote-unity-sandbox", "version": "0.1.0" }`）
   - 地形：区画の原点のまわりだけが草で、区画の間は土が見える。human ownerが決めた形（「最初から整地してある状態」）で、
     `19-unity/README_ja.md`の「公開Unity箱庭」に書いた
   - font：`NotoSansJP-Subset.ttf`（4,947,692 bytes）。SIL Open Font License 1.1（licenseの文を同梱）。`fonts-noto-cjk`の
     `NotoSansCJK-Medium.ttc`から、`pyftsubset`で文字を絞った
2. **確かめ方**：`dotnet test`で18 testが通る（`2026-11-14-03`〜`05`を入れた後）。Unity Editorで検証とplayのsmoke。Headless
   ChromeでWebGLまで通した。human ownerが、wireの確定形を入れた後のserverへ、ScratchのLANパッケージとPythonのclient
   （`minecraft-remote-api`）からつなぎ、ペアリングして建てた（human owner 2026-11-15「さっきのスクショは、wire確定形を入れた
   あとのもの。」「Scratch LANパッケージ、Pythonクライアントからつながる。」）
3. **確かめられなかったこと**：tabletの実機、Webでの公開の配信、URPとの比べ。公開の前の上限（送り元ごとと全体のcodeの試行、
   世界のリセットの間隔）は、hub NOTESの「公開Unity箱庭へ進む」の行にある

human owner「Unity箱庭は、色々と試行錯誤してかなり完成度が上がっているが、もう少し、残っている。」。次の依頼（残りを
仕上げてPRにする）は`00-hub/unity-sandbox-first-slice-pr-instructions_ja.md`。
