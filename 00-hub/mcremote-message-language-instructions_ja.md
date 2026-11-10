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
