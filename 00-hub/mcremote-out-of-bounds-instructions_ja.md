# 世界の外への操作を`out_of_bounds`で拒み、helloの`server`を返す依頼（McRemote）

> 公開Unity箱庭を最優先にした（`2026-11-13-04`）。Unity箱庭のserverは、McRemoteと同じprotocolに応え、Unityであることを
> helloの`server`で名乗る（`2026-11-14-01`）。その形をMcRemoteに合わせるために、今`server`に入れているものを返してほしい。
> また、世界の外への`world.setBlock`、`world.setBlocks`、`world.getBlock`は、reason `out_of_bounds`で拒むと決めた
> （`2026-11-14-02`、wire「7.3 エラー設計」の表の下の`out_of_bounds`の箇条）。世界の外とは、ブロックを置ける高さ（`y_min`〜
> `y_max`。地上の世界は-64〜319、両端を含む）の外と、水平方向の世界の端（Minecraftではworld border）の外。権限やbuild policyの
> 範囲の外は、今のとおり`build_denied`。世界の制限と権限の制限を、errorで分けるため。
> human ownerは、`build_denied`もさらに分けたい（2026-11-14「なんでもbuild_deniedになって、よくわからない、になっている。」）。
> その案を作るために、今`build_denied`を返す場面をすべて返してほしい。参照するknowledge commitは、この依頼が入ったmainの
> commitです。

## すること

1. **helloの`server`**：今入れているものを返す（形、意味、いつ変わるか、どこで作っているか）。変えない
2. **世界の外での今の動き**：次のとき、id付きのrequestとnotificationで何が起きるかを返す
   - `world.setBlock`、`world.setBlocks`で、yが`Y_MIN`より下か`Y_MAX`より上。`setBlocks`の箱の一部だけが外れたときも
   - 同じく、x、zがworld borderの外
   - `world.getBlock`で、上の2つ
3. **`out_of_bounds`を入れる**：2の3つの操作を、`2026-11-14-02`のとおりにする
   - code は`-32000`番台で、番号はMcRemoteが選ぶ（`expected_hello`と同じ扱い、`2026-11-12-03`）
   - `data.bounds`に世界の範囲、`data.violating`に外れた座標を入れる。形は、今の`build_denied`の`data`に合わせて案を返す。
     world borderは中心と大きさが変えられるので、その時点の値を返す
   - `setBlocks`は、箱の一部でも外れたら何も置かない
   - 世界の外かどうかは、`buildRange`などの権限の範囲より先に判定する
   - unit testで、直す前に落ち、直した後に通ることを確かめる
4. **`build_denied`を返す場面**：methodと原因ごとに、すべて返す。それぞれ、判定する位置や量、`data`に入れているもの、根拠の
   codeの場所。変えない。knowledgeに書かれているのは、建築範囲（`buildRange`）の外（`world.setBlock`、`world.setBlocks`、
   `world.getBlock`、看板を書く操作、`world.strikeLightning`、`world.spawnParticle`、`world.getNearbyEntities`、
   `entity.setPose`、`world.playSound`、`world.playBlockSound`）と、playerごとの1回に置ける数の上限（`mcr.build.blocks`。
   `world.setBlock`、`world.setBlocks`）。これと違うもの、書かれていないもの（たとえば`world.getBlocks`、`world.spawnEntity`）が
   あれば、それも分かるようにする
5. 3はPRにする。mergeはhuman ownerが判断する。McRemoteの次のreleaseに入れる（hub NOTESの「McRemoteの次のrelease」の行）

## 返却

- 実際に読んだknowledge commit
- 1、2、4の答えと、根拠のcodeの場所
- 3のPRの番号、head、CIのrun。codeの番号と`data`の形。testが直す前に落ちたことの確かめ方
- 確かめられなかったことと、その理由

## coordinatorがすること

- PRとCIを、GitHubのAPIで照合する
- 1を見て`server`の形の案を作り、wire §6.2に書く。human ownerに見せる
- 4をknowledgeの記述と突き合わせ、`build_denied`の分け方（reasonの名前、`data`の形）の案を作る。human ownerに見せる
- 3がreleaseに入ったら、wire §7.3の表へ`out_of_bounds`を移し、F1のcase（tooling）と各clientの表示を頼む

## 返却と照合（2026-11-14）

McRemoteは、knowledge `451988d9cf55cfa0f13f4a1b00dc1983274b719d`（この依頼が入ったcommit）を読み、McRemoteのmain
`cdafcfd804614def19a35b099bedc93697ca4899`を調べた。返却票はMcRemoteの搬送素材
`handoff-materials/2026-11-14-world-out-of-bounds/materials/RETURN_ja.md`（17,193 bytes、SHA-256
`496834f867b908a4055082157f7d5c14b15824adecd842596c8f0332d6ed032f`）。coordinatorはGitHubのAPIで、PR #19のheadが
`924ca925d3631af846c4ae82d4820867b8bdf2f8`、baseが`cdafcfd`であること、CI run `43589581111`がこのheadで7 jobとも成功した
ことを確かめた。human ownerが2026-11-14にmergeした（merge commit `3ccb3fd345faa228b195a15c3c45152f5dff7d04`）。

1. **helloの`server`**：成功したhelloの応答には、`server`のkeyが無い。`protocol_mismatch`の`data.server`は、serverの
   protocolの版（今は`23.2.1`）で、別のもの。形は`2026-11-14-03`で決めた
2. **世界の外での前の動き**：高さもworld borderも確かめず、Paperへそのまま渡していた。`buildRange`の外と重なれば
   `build_denied`、内なら`result: null`や読んだblock。置くときだけ、原点からの相対で`x`、`z`が±1,000,000、`y`が±1,000の外を
   `invalid_params`にしていた。Paperで実際にどうなるかは確かめていない
3. **`out_of_bounds`（PR #19）**：codeは`-32000`。`data`は`bounds`（`y_min`、`y_max`、`world_border`の中心と大きさ）と
   `violating`（最初に外と判定した点の絶対座標）。BlockSpecの検査の後、建てる権限、`buildRange`、block数の上限、work、
   Paperへの読み書きより前に判定する。`setBlocks`は対角の2点を受付のときに確かめ、外なら何も置かない。前の相対座標の上限は、
   世界の実際の範囲の判定に置き換えた。WorldBoundsTestの24 caseが、直す前にすべて「`out_of_bounds`を期待したが、違う引数で
   呼ばれた」で落ち、直した後は48 caseが通る。実際のPaperでは試していない。`data`の形は`2026-11-14-04`で決めた
4. **`build_denied`を返す場面**：14のmethod、16の組。原因は、建築範囲（`buildRange`。原点からのx、zの差）の外と、playerごとの
   1回に置けるblock数の上限（`mcr.build.blocks`。`world.setBlock`と`world.setBlocks`）の2つ。`data`はどれもreasonだけ。
   knowledgeの列挙に無かったmethodは、`world.getBlocks`、`world.getHeight`、`world.spawnEntity`。分け方は`2026-11-14-05`で
   決めた

次の依頼（`build_denied`を分け、世界の外の判定をほかのmethodへ広げる）は`00-hub/mcremote-build-denied-split-instructions_ja.md`。
