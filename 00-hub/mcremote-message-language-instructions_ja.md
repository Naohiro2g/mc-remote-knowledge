# McRemoteのゲーム内の文をclientの言語に合わせる依頼（McRemote）

> `2321.1`の人間の試験で、HUDの方位はclientの言語で切り替わった（jaなら北〜北西、それ以外はN〜NW。
> `11-plugin/platform-design_ja.md`の11.1）。一方、ペアリングと`/mcr hud`の文は日本語で出た。ペアリング成功は「日本語 / English」の
> 併記で、`/mcr hud status`の対象の名前は日本語だけだった。human owner 2026-11-08：「これも英語化しよう」（hub NOTES 2026-11-08の
> 行）。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 欲しいもの

- McRemoteがplayerに見せる文を、方位と同じく、clientの言語がjaなら日本語、それ以外は英語で出す
- 対象：chat、commandの返事、title、actionbar、BossBarなど、playerの画面に出るものすべて。serverのconsoleとlogは対象にしない

## すること

1. playerに見せる文を洗い出す。それぞれ、出る契機、出る場所、今の言語（日本語だけ、英語だけ、併記）を書く
2. 英語の文を起こす。日本語の文は今のまま使う
3. 先にtestを書き、ja以外のclientで日本語が出ることで落ちるのを確かめる（落ちたlogを返却に残す）
4. 直す。clientの言語がまだ分からないとき（参加の直後など）にどちらで出すかは、McRemoteが案を決めて返却に理由を書く
5. 同じtestがjaとja以外の両方で通ることを確かめる。CIを通す
6. 既定のbranchへのPRにする。mergeはhuman ownerが判断する。tag、Release、公開のworkflowの実行はしない

## 返却

- 1の一覧（文の識別、契機、場所、直す前の言語、日本語と英語の文）
- 3で落ちたtestと、そのlogの抜粋
- 4の、言語がまだ分からないときの案と理由
- 統合版（Geyser）のclientで、言語が取れるか（分かる範囲。実機で確かめていなければ、そう書く）
- PRの番号とhead、CIのrun ID
- 人間の試験で見てほしいこと（次の横断gateで使う）

## coordinatorがすること

- PRの差分、test、CIをGitHubのAPIで照合する
- mergeの後に、`11-plugin/platform-design_ja.md`へゲーム内の文の言語の規則を書き、hub NOTESの行を閉じる

## 返却と照合（2026-11-12）

McRemote担当はknowledge `a409c9695e1a117d88abc36084b9c582b54d7c50`を読んだ（この票の本文は今と同じ）。McRemote PR #17（head
`e6b59f18c786b887515bfb5bad7be2ca5fb09019`、base `bc18243c6275387953f24b59b70a2dbd499b9b20`）を、human ownerが2026-11-12にmerge
commit `cdafcfd804614def19a35b099bedc93697ca4899`でmergeした（`main`の先頭。treeはheadと同じ）。coordinatorはGitHubのAPIで、PR、
merge commitの親とtree、変わった10 file、CIのrun `43054912660`（同じhead、7 jobすべて成功、`workflow_dispatch`）を確かめた。
返却の素材7件のSHA-256は、MANIFESTの表と一致した。

- 一覧：playerに見せる文16件を`PlayerMessage`に集めた（ルートとHUDのusage、HUDの無効、足元と照準の名前、pairの4結果、
  credentialの管理の6件、アクセス禁止のkick）。ほかに、HUDの状態の行、方位、数値、静的なmetadata、playerが書いたchatと看板の
  扱いを書いた（返却の「文の棚卸し」）。アクセス禁止のkickは、今のproductionでは通らない経路で、有効にしていない
- 落ちたtest：`PlayerMessageLanguageTest`の17件のうち11件が、直す前に落ちた（英語、fr、知らないlocaleで日本語や併記が出る、
  日本語のclientに英語だけが出る）。直した後は言語のtestが22件
- 言語がまだ分からないとき：英語。応答のたびにlocaleを読み、保存しない。方位と同じで、取れないときに日本語を仮定しないため
- 結果：localのTemurin 21.0.13+9で`./gradlew build`、438 test、failure、error、skipは0。testはmockのplayerのlocaleによるunit
  testで、実機のlocaleの到着、`1.21.11`と`26.3`での実機の試験、release gateの合格は主張しない
- 統合版（Geyser）：GeyserMC/Geyser `c8758b846837bf384591334e1715614160ae49b5`の`GeyserSession.java`で、統合版の言語をJava版の
  localeとして送っている。稼働中のGeyserとの照合と、統合版の端末での確かめはしていない
- 規則は`2026-11-12-02`と、`11-plugin/platform-design_ja.md`の「12. playerに見せる文の言語」へ書いた
- 人間の試験で見てほしいこと（返却の「次の横断gate向け・人間の確認案」）：(1) Java版を日本語とEnglish (US)で1回ずつつなぎ、
  pairの成功と`/mcr hud status`の対象の名前が画面と同じ言語になり、英語に日本語や併記が残らない (2) つないだまま言語を
  切り替え、次のHUD statusとBossBarの方位がそろう (3) 統合版をGeyser経由で日本語と英語にして、同じ2画面を見る (4) 標準の
  `/help mcr`と`/version McRemote`で、製品名と構文が読める。hub NOTES 2026-11-12の行に置き、次の横断gateの人間の試験の票へ入れる
