# 接続先ごとにID、ラベル、host、portを持つ形を実装する依頼（Scratch／tooling）

> `2026-10-24-06`を実装する。human owner「「接続先ごとに独立したID・ラベル・host・portを持つ」方式の実装を次に。」
> （2026-11-15）。きっかけは、Unity箱庭のserverのportの既定を`25585`にしたこと（`2026-11-15-01`）。同じPCや同じhostの
> McRemote（`25575`）とUnity箱庭のserverを、別の接続先として選べるようにする。方針は、担当が前に返したもの（scratch-editor
> `handoff-materials/2026-10-24-bridge-multiple-targets-confirmation/materials/TARGET_CONFIG_HANDOFF_ja.md`）と同じ。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 決まっていること（守るもの）

`2026-10-24-06`と`00-hub/deployment-interface-design_ja.md` §6：

- 人が編集する接続先の一覧は一か所。そこからScratchの選択肢と、Bridgeの対応表と許可を作る。ScratchとBridgeを別々に
  手で直させない
- 接続先ごとに`id`、`label`、`host`、`port`を持つ。`id`は`host`、`port`、`label`から独立させ、hostなどを変えても変えない
- `label`はScratchの表示、`host`と`port`はBridgeがつなぐ先。Bridgeは`id`から`{host, port}`を引く。同じhostの別port、
  別のhost、内外の混在、3件以上を、同じ仕組みで扱う
- 作った設定は実行時に読む。接続先を変えても、ScratchとBridgeを作り直さない。反映は、Scratchはbrowserの再読み込み、
  Bridgeは設定の反映と再起動（今あるTCP接続への無停止の反映は含めない）
- 公開のScratchから、一覧に無いhostやportへつなぐ入口は作らない
- 初回stableのBridge `v2321.0.0`は変えない。対応表を足す最初の1回は、新しいbuildになる
- 入力、生成、配備はStackが担う。この票では作らない
- tokenは、今と同じく接続先ごとに分けて置く

## すること

1. **Bridge**（minecraft-remote-tooling）：`id`から`{host, port}`を引く対応表を足す。一覧に無い`id`は拒む
2. **Scratch**（scratch-editor）：接続先を`{id, label, host, port}`の一覧から作り、選んだ接続先の`id`でBridgeへつなぐ
3. **Scratch LANパッケージ**：今の設定は接続先が1つ（「このPC」か「LAN内の別のPC」と、McRemoteのport）。同じPCの
   Minecraft（`127.0.0.1:25575`）とUnity箱庭のserver（`127.0.0.1:25585`）を両方入れて、Scratchで選べるようにする。
   今の`settings.json`からの移り方も
4. unit testで、直す前に落ち、直した後に通ることを確かめる。同じhostの別port、別のhost、3件以上、一覧に無い`id`
5. 1台のPCで、LANパッケージからMcRemoteとUnity箱庭のserverを選び分けて、ペアリングと建築ができることを、human ownerが確かめる
6. PRにする（scratch-editorとtooling）。mergeはhuman ownerが判断する。版の番号は、番号を取る時に`2026-11-05-02`で決める

## 決めていないこと（案を返す）

- 一覧の入力のsyntax、file名、schema（Stackとの契約になる）
- `sandbox`という名前と、wireの`?sandbox=`の扱い（名前を変えるか、今の名前のまま`id`を入れるか）と、前の版のScratchや
  Bridgeからの移り方
- LANパッケージの設定画面の形と、接続先の`label`の既定の文

## 返却

- 実際に読んだknowledge commit
- PRの番号、head、CIのrun
- 上の「決めていないこと」の案と、一覧の例
- testが直す前に落ちたことの確かめ方
- 確かめられなかったことと、その理由

## coordinatorがすること

- PRとCIを、GitHubのAPIで照合する。決めていないことの案をhuman ownerに見せ、決まったら、Stackへ入力、生成、配備の票を出す
  （公開VPSで、McRemoteとUnity箱庭のserverを別の接続先にする）

## 返却と照合（2026-11-16）

Scratch／tooling担当は、knowledge `3309389`を読んだ。返却はscratch-editorの`handoff-materials/2026-11-15-bridge-connection-targets/`
（`materials/RETURN_ja.md` 7,247 bytes、`86300f6a8c7b8ab97fee3a472712b878daa1fc007ce1083c32366310604355e7`。案は
`materials/CONNECTION_TARGETS_PROPOSAL_ja.md` 5,025 bytes、`f7113a7984cc6fab18cd01f91f07bb0b4614df6d2bc8be4f3f37b78865f35e81`）。

- tooling PR #11：`agent/connection-targets-2026-11-15` → `main`（`335c604`）、head `df2491d64836215945c32f097456bf7d799c5c98`。
  CIのPR `43664108289`と、候補の生成`43666540083`（`workflow_dispatch`）は成功。artifact `14142605179`
  （`sha256:44f3268f0010d132678f3997eb35363d0ae94d4c05c44eb2574349ba9dde7f3f`）。Bridge OCIのindexは
  `sha256:4fc95bcad2bd35d33d32228e8953da0e88b4197bce6253fea657590b102eef8c`、archiveは114,626,048 bytes
  `cc9dea93adcbe3890dfd08c0bc78f0fc0b67c7fc5864df9c96331420a1e53d18`（担当の申告）。WireScopeのZIPは変わらない
- Scratch PR #35：`agent/connection-targets-2026-11-15` → `develop`（`d0b4bb7`）、head
  `3d1ae0b05b8ec4e098c81ec7e02ca4258fa1fa51`。CIのpush `43687769563`とPR `43687775460`は成功
- coordinatorがGitHubのAPIで、2つのPRのhead、CIの結論とhead_sha、artifactのdigestとheadを確かめた
- test：Bridge 42件（実際のTCPで2つのportへ振り分け、別のhost、3件以上、一覧に無いものを拒む、今の形の起動、認証の中継）、GUI 39件、
  VMの拡張563 assertions、Runtime 280、`id`ごとのtokenと切り替え17、LANの設定画面6件、launcher 12件など。新しいtestを直す前の
  sourceに当てて落ちることを確かめた（logは返却の場所）
- 3つの案は`2026-11-16-01`で決めた（human owner 2026-11-16「Bridgeの案、採用。」）
- 確かめていないこと：5（完成したLANパッケージからMcRemoteとUnity箱庭を選び分けて、ペアリングと建築）。Linuxの試作ZIP
  （source `3d1ae0b`、287,241,299 bytes、`32a1b5938f9527c5403b8be2c0673d7762d745ffc9d26a11a09f74f023c957ae`。表示は`2321.1.0`の
  ままの技術の確認用）の起動は通った。Windows、macOS、tablet、外のhostへの接続、Stackの生成と配備も確かめていない
- 次：human ownerが試作ZIPで5を試し、2つのPRのmergeを判断する。出すのは`2321.3`で、toolingのBridgeも新しい版になる。Stackへの
  入力、生成、配備の票は、mergeの後に、Unity箱庭のimageの返却と合わせて作る
