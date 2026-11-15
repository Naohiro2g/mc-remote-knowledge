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
