# Unity箱庭へつなぐときに、ScratchとBridgeが求めるものを返す依頼（Scratch）

> 公開Unity箱庭を最優先にした（`2026-11-13-04`、スポークは`19-unity/README_ja.md`の「公開Unity箱庭」）。入口はScratchで、
> Scratch → Bridge → Unity箱庭のserverとつなぐ。Unity箱庭のserverは、McRemoteと同じ改行区切りのJSON-RPCをTCPで受け、
> Minecraftを使わない。世界のモデルはMinecraft 1.21.11に準拠する。pairingは、Scratchに出たcodeを、Unity Webのchatで
> `/mcremote pair NNN-NNN`と打って承認する。この票は、今のScratchとBridgeが、つなぐserverに何を求めているかを返して
> もらう依頼です。コードは変えない。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 返してほしいこと

読んだscratch-editorのcommitを書く。

1. **hello**：Scratchが送る値と、応答から読む値、確かめる値（`protocol`、`mc_version`、`supported_mc_versions`、`catalogHash`、
   `world_constants`、session、player、`dimension`、origin、permissionsなど）。どの値が無いか違うと、つながらないか、
   表示が変わるか
2. **呼ぶmethod**：つないでから、blockを置き、切れてつなぎ直すまでに呼ぶmethodの一覧（`auth.*`、`catalog.get`、`build.*`、
   `connection.flush`など）。execution mode（FAST、TRACE、DEBUG）で変わるもの
3. **catalog**：blockを選ぶmenuが、serverの`catalog.get`から作られるか。serverが返すblockが少ないとき（たとえば8つ）、menuは
   どうなるか。`catalogHash`とcacheの扱い
4. **pairingとtoken**：pairingの案内の文（`/mcremote pair ...`）と、それを出す画面。Minecraftのplayerの名前など、Minecraftに
   頼る表示。tokenの置き場所と、2回目からの接続で使うmethod
5. **Bridgeと接続先**：Bridgeの宛先（`connection_targets`など）と、Scratchのruntime configの接続先。Unity箱庭のserverを、
   McRemoteと並べて宛先に足すには、何をどこへ書くか。1台のPCで試すとき、LANパッケージのBridgeを向けられるか
6. 1〜5で、Unity箱庭のためにScratchやBridgeを変えた方がよいと思うものがあれば、案を返す（変えない）

## 返却

- 実際に読んだknowledge commitと、scratch-editorのcommit
- 1〜6の答え
- 確かめられなかったことと、その理由
- token、host、IPなど、秘密やprivateな運用の値を書かない

## coordinatorがすること

- Unityの返却（`00-hub/unity-sandbox-first-slice-instructions_ja.md`）と合わせて、hubで決めること（Minecraftでないserverの
  hello、tokenと画面の結び付き、blockの一覧とcatalog、serverが応える最小の組、範囲の外へのerror）の案を作り、human owner
  に見せる
