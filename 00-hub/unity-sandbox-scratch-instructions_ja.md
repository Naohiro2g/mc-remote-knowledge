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

## 返却と照合（2026-11-14）

Scratchは、knowledge `ef4c32def9a02253b693b80d4386cdb64be029ac`（この依頼が入ったcommit）と、scratch-editor
`0e4aea4bca42988122feb46e36b952c2e8e9a733`を読んだ。Bridgeは、Scratchのlockが固定するminecraft-remote-tooling
`6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`のsourceを読んだ。coordinatorはGitHubのAPIで、scratch-editorのcommitのtreeが
developの先頭`d0b4bb7e541872c25b58d7fc7a22ee5f8a88e951`と同じであること、toolingのcommitがあることを確かめた。返却票は
Scratchの搬送素材`handoff-materials/2026-11-13-unity-sandbox-scratch/materials/RETURN_ja.md`（20,552 bytes、SHA-256
`e84487af95d8e1f2d97d8b9105f32b2f56fc990c3ce2a1c53b0efcb43611ce1b`）。コードを読んで返したもので、コードは変えておらず、
Unityへは実際につないでいない。

1. **hello**：Scratchは`protocol: "23.2.1"`、`client`、保存したtokenを送り、つなぎ直しでは`build`も送る。応答で必ず確かめる
   のは、`protocol`（majorが23、minorが2以上）、`dimension`（namespaceつき）、`origin`（3つの有限の数）。`mc_version`は
   blockの名前の辞書を選ぶのに使い、無くてもつながる（1.21.11なら今の辞書が使える）。`supported_mc_versions`、
   `world_constants`、`permissions`、`server`、`session`、`player`は、無くてもつながる。返却は、これはScratchの今の検査で、
   wireで要るfieldを省いてよいという意味ではない、としている
2. **呼ぶmethod**：`hello`、`auth.pairBegin`、`auth.pairPoll`、`catalog.get`、`events.poll`（helloの後にいつも呼ぶ）、4つの
   操作、`build.setDimension`、`build.setOrigin`、`connection.flush`。FASTでは`setBlock`と`setBlocks`をidなしのnotificationで
   送り、`connection.flush`で区切る。TRACEは、DEBUGと同じrequestの後にclientの側で待つだけ。`events.poll`が無いと、Scratch
   は案内を出してpollを止める（建築の接続は閉じない）
3. **catalog**：blockを選ぶmenuは、`catalog.get`のblockのkeyから作る（8種類なら8件）。`catalogHash`は、本文（block、
   entity、particle）をcanonical JSONにしたSHA-256と一致する必要がある。entityとparticleは空でよい。Scratchの既定の入力は
   `stone`
4. **pairingとtoken**：codeは`NNN-NNN`で、`/mcremote pair ...`の全体を出す（Unity Webのchatで打つ形と合う）。playerの名前は
   出さない。tokenはbrowserのlocalStorageに、接続先のrouteごとに置く。Bridgeは`auth.pairBegin`と`auth.pairPoll`を別のTCP
   で送ることがあり、約10秒で切る。serverはpairingをTCPの接続に結ばず、pendingのpollを長く待たせない。Minecraftという
   語を含む案内（blockのmenu、LANの設定画面）が残る
5. **Bridgeと接続先**：Scratchのruntime configの`connection_targets`に足し、BridgeのallowlistにUnity箱庭のserverの
   hostnameを足す。今のBridgeは、どの宛先にも同じTCPのportを使い、hostnameへそのままつなぐ。同じhostnameの別のportは
   選べない。1台のPCでは、LANパッケージのlauncherで接続先のhostとportを変えれば、Unity箱庭のserverへ向けられる
6. **案**：最小の組に`events.poll`の空の応答とFASTを入れる。Unityのblockだけをcatalogで返す。Minecraftという語の案内を
   接続先に合わせて変える。tokenをUnityとMinecraftで別のrouteに分ける。同じhostの別のportは、`2026-10-24-06`の接続先の
   一覧へつなぐ

hubで決めることは、hub NOTESの「公開Unity箱庭へ進む」の行にある。
