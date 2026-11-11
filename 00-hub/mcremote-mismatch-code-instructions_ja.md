# protocol_mismatchのcodeを-32000番台へ移す依頼（McRemote）

> `2026-11-10-01`①で、helloの`protocol_mismatch`のcodeを`-32000`番台と決めた（wire「6.3 失敗」「7.3 エラー設計」）。出荷済みの
> `2321.1.0`は`-32600`（JSON-RPCのInvalid Request）を返す。human owner 2026-11-12：「codeの移しかえを次の票にして、同じreleaseに
> 入れる」。同じreleaseには、credentialのfileの権限（`2026-11-11-03`、PR #16）と、ゲーム内の文の言語（`2026-11-12-02`、PR #17）が
> 入る（hub NOTES 2026-11-12の「McRemoteの次のrelease」の行）。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 欲しいもの

- helloの`protocol_mismatch`を、`-32000`番台のcodeで返す。番号は、ほかのreasonと同じく、範囲の中でMcRemoteが選ぶ
- 変えないもの：`data`の`reason`（`protocol_mismatch`）、`server`、`client_requires`。messageの英語の短文。errorを返した後に
  閉じること。互換判定（majorの一致、serverのminorが同じか上、patchは見ない）

## すること

1. 先にtestを直し、今の`-32600`で落ちることを確かめる（落ちたlogを返却に残す）
2. 直す。選んだcodeと、その理由（ほかのreasonのcodeとの関係）を返却に書く
3. ほかにも、形の正しいrequestへ`-32600`を返すreasonがあれば、変えずに一覧を返す
4. 既定のbranchへのPRにする。localとCIの検査を通す。mergeはhuman ownerが判断する。tag、Release、公開のworkflowの実行は
   しない。releaseの版と時期は、human ownerが決める

clientは`data.reason`で判定し、codeでは分けない（`2026-11-10-01`③）。共有fixtureには、`-32000`のF1-HE-09と、出荷済みの
serverのための`-32600`のF1-HE-10がある。どちらもこのままにする。

## 返却

- 実際に読んだknowledge commit
- 1で落ちたtestと、そのlogの抜粋
- 選んだcodeと理由
- 3の一覧（あれば）
- PRの番号とhead、CIのrun ID

## coordinatorがすること

- PRの差分、test、CIをGitHubのAPIで照合する
- wire「7.3 エラー設計」の`protocol_mismatch`の行と、Protocol InventoryのMcRemoteの列を、mergeの後に直す
- human ownerにreleaseの時期を聞き、台帳`00-hub/release-train-notes_ja.md`に行を足す
