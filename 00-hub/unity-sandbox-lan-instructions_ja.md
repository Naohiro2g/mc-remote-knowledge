# Unity箱庭LANのセットを、human ownerと相談して進めること（mc-remote-unity-sandbox）

> human owner 2026-11-16：Scratch LANパッケージの発展形として、Unity箱庭のserverのセットを作る。LANで配るものは、使う側
> （Scratch LANパッケージ）とサーバー役に分けた（`2026-11-16-04`）。Unity箱庭のLANのセットは、サーバー役の1つ。形は、
> human ownerと相談し、仮実装しながら決める。`2321.3`の準備（`00-hub/unity-sandbox-release-instructions_ja.md`の「次にすること
> （2026-11-16）」と「human ownerと相談して進めること（2026-11-16）」）を先にする。参照するknowledge commitは、この票が入った
> mainのcommitです。

## 決まったこと（2026-11-16）

- 使う側とサーバー役を分ける（`2026-11-16-04`）。Unity箱庭のLANのセットは、Unity箱庭のcomponentの配布物で、Scratch LAN
  パッケージには入れない
- 時期：`2321.3`に間に合えば入れ、間に合わなければ`2321.4`（human owner「Unity箱庭LANは、間に合えば2321.3、間に合わなければ
  2321.4に」）
- ver2（サーバー1台＋ブラウザ、証明書を配る）の証明書の検証は、Unity箱庭で先に試す（human owner 2026-11-16）。証明書の
  検証は、human ownerがStackとScratchに相談する（hub NOTESの「LANパッケージver2」の行）
- buildは手元で行う（`2026-11-15-05`）
- Scratch LANパッケージの接続先の一覧には、Unity箱庭（`127.0.0.1:25585`）が最初から入る（`2026-11-16-01`、Scratch PR #35）

## human ownerと相談して進めること

1. OSごとの配る形（Scratch LANパッケージと同じWindows、macOS、Linux）：serverとUnity Webの入れ方、起動ファイル、置き場所
   （Scratchは`HOME/mc-remote/mc-remote-scratch-LAN/<version>/`、`2026-10-13-03`）、版の見え方
2. 使う人の流れ：Unity箱庭のセットを起動し、Scratch LANパッケージで接続先「Unity箱庭」を選び、Unity Webを開く。迷わず
   再現できるか、終わり方、失敗の見つけ方（Scratch LANの考え方は`13-scratch-client/scratch-lan-package-design_ja.md`の§1、§5、§6）
3. LANの中の別の端末のブラウザからUnity Webを開く形（ver2の前段）と、証明書の検証で何を試すか
4. gateで照合できるもの：ZIPのbytesとSHA-256、ZIPの中に書くsourceのcommit（Scratch LANの`data/identity.json`のように）

## 返却

- 実際に読んだknowledge commit
- branch、head、PR
- 1〜4で、相談して決めた形と、採らなかった案（相談した日とhuman ownerの言葉）
- 試作のZIP（OSごとのbytes、SHA-256、sourceのcommit）と、確かめた端末とOS
- 確かめられなかったことと、その理由

## coordinatorがすること

- PRを、GitHubのAPIで照合する。決めた形を、返却を見てDECISIONSとLANの設計に書き、ホームページの`/lan/`の案内を直す
