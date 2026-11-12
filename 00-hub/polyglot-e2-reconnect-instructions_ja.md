# 待ち方とつなぎ直し（E2の③⑤）を入れる依頼（Python・Java・Scratch・C#・TypeScript）

> 多言語Client LibraryのE2で、接続の振る舞いを`2026-11-11-01`①〜⑧、`2026-11-12-01`、`2026-11-12-05`で決めた。前の票
> （`00-hub/polyglot-f1-e2-repin-instructions_ja.md`、C#は`00-hub/polyglot-csharp-start-instructions_ja.md`）で、各clientは②④⑦⑧を
> 直し、③⑤の今とAPIの形の案を返した。TypeScriptは③⑤を入れた。toolingはF1に③⑤のcase（v2）を足し、caseの補いを返した
> （minecraft-remote-tooling `335c604f859d6dfad04f0434bfa4eb6445761430`、v1は54 case、v2は12 case）。この票は、③⑤を決定のとおりに
> 入れ、F1をそのcommitへ固定し直す依頼です。TypeScriptは固定し直しだけです。human owner 2026-11-10：「クライアントの多言語化を
> 最優先とする。その先のUnity版マイクラリモコンを急ぐため」。参照するknowledge commitは、この依頼が入ったmainのcommitです。
> 各担当は「共通」と、自分の節を読んでください。

## 共通

### 決まったこと

- `2026-11-11-01`③（wire「3.4 id 規律」）：応答は、既定で長く、粘り強く待つ。普通に使っていてtimeoutを感じない長さにする。
  応答待ちがある間、その接続で最後に受信してからの時間で見て、呼び出しや接続ごとに延ばせる。超えたら②と同じ「完了不明」で、
  その接続を回収する。これとは別に、transportの生存確認で切れた接続を見つけ、Wi-Fiの一時的な切断には長めに耐える。ボットや
  攻撃への短い上限は、serverの認証前の上限が持つ（`2026-10-07-02`）。値と設定の仕方は言語ごとに、実測で決める
- `2026-11-11-01`⑤：接続が切れた後の次の呼び出しで、自動でつなぎ直す。既定で有効にし、applicationが無効にできる。保存した
  tokenで新しいhelloから始め、clientが最後に成功を確かめたdimensionとoriginをhelloの`build`で戻す。entity handleとevent cursorは
  無効にし、つなぎ直したことと、その間のeventのlossをapplicationへ知らせる。条件：
  - (A)つなぎ直せずに失敗した呼び出しは「未送信」として、②の「完了不明」と分けて知らせる
  - (B)前の接続で送ったFASTの設置を、つなぎ直した後の`connection.flush`の成功が保証するように見せない。前のflushの後に
    つなぎ直したことが分かるようにする
  - (C)helloで版の互換判定と`catalogHash`の照合をやり直し、helloの`server`や`session`が変わったら知らせる。版が合わなければ、
    黙って続けずに失敗にする（`2026-11-12-01`）
  - (D)pairingが要るとき（`auth_required`）は自動で進めず、止めて知らせる
  - (E)1つの接続を複数のスレッド（JavaScriptでは同時に走る複数の呼び出し）が共有していても、つなぎ直しは1回にする
  - (F)つなぎ直しの間隔は、ばらつかせながら延ばし、長めに粘る
  - (G)何もしていない間の切断は、③の生存確認が見つけて「切れている」状態にする
- `2026-11-11-01`④：requestを自動で再送しない。つなぎ直したときでも、再送するかはapplicationが決める
- `2026-11-12-05`（wire「6.5」）：pairingの途中で接続が切れたら、期限内なら、同じ`pairing_id`の次のpollを新しい接続で送って
  pairingを続ける。応答の前に切れたpollは完了不明として終え、次のpollはその送り直しではなく、pollの続きとして扱う（④に当たら
  ない）。続けたpollが`pair_not_found`などで失敗したら、二度目のpairingはせずapplicationへ失敗を返す（`2026-08-30-03`）
- 検討メモ`10-protocol/connection-liveness-notes_ja.md`：待ち方の3段（知らせる、生存確認、最後の上限）、欠点とつぶし方。値は
  決めていない

### F1の取得元

tooling `335c604`の`packages/protocol/test/fixtures/`の11 file。形の説明は、同じcommitの`packages/protocol/README.md`（v1）と
`packages/protocol/CLIENT_BOOTSTRAP_V2_ja.md`（v2）。copyで持つときは、fileごとのbytesとSHA-256をtestで確かめる（F2、`2026-10-22-07`）。

| file | case | bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `client-bootstrap-framing-v23.2.1.json` | 7 | 15,131 | `be063b519b5d653a4bb4ec3da6f67e5d481a28dcf5913961c848b2b909d4b26d` |
| `client-bootstrap-hello-v23.2.1.json` | 12 | 26,046 | `caf24ad5382e411ba54172b05d6020fc59fc429dc0251ff28db3908b4189784e` |
| `client-bootstrap-pairing-v23.2.1.json` | 12 | 45,943 | `19230b310c7482adc740095d5604110937ebaa7803a0fed4c294083a9e63a460` |
| `client-bootstrap-blocks-v23.2.1.json` | 12 | 45,945 | `664babdf3131a74e4aaf6d9e5dfb5e4cfc6e197df0a0d48142688820f1be813d` |
| `client-bootstrap-errors-v23.2.1.json` | 3 | 9,179 | `c458d3ffbae846cfb33c032eba14d8f0005c6a1fbe871290b53fcfec8ec41aaa` |
| `client-bootstrap-close-v23.2.1.json` | 8 | 20,879 | `2abb6f48942e1dc7bc42014ba016c3d08a6632c59445c048b008a4c411ea1e30` |
| `client-bootstrap-operations-v23.2.1.json`（v2） | 12 | 66,335 | `8309f5847ad69aa2d82fcbcb1726918c3a69ba875e04e8f38678352b06b7f7a1` |
| `client-bootstrap-v1.schema.json` | — | 11,521 | `970dd68999edc14a4dcc2b67ab2f712e830b7841b2ec4548fee66af117fd281b` |
| `client-bootstrap-v2.schema.json` | — | 19,468 | `8ae1c7313d01fa0fa24f4f2079ba453129dc16b678342df6f7ef66b9255d1381` |
| `block-value-v22.json` | — | 3,217 | `e8e108d59c40751d67a432543d75cb4bf9146ef9781721012085c80545b854f3` |
| `LICENSE` | — | 1,070 | `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb` |

- 前の取得元から変わったcase：F1-AU-11、12を追加（承認を待つ間のEOFの後のpoll、pollの応答の前のEOF）、F1-OP-08をc2で
  pairingする形へ直した。`36ebe9e`からは、F1-HE-11、12、F1-CL-07、08とv2も加わっている（`d2691cd`、`0d120e5`）
- F1-AU-07の観測の終わりと、v2の`expected`の比べ方は、READMEとv2の説明に書かれた。fixtureの中身は変わっていない
- F1は、F1-AU-12の先（応答を失ったpollの後のpoll）を、まだcaseにしていない

### 参考：TypeScriptの形

TypeScriptが入れた形（`Naohiro2g/minecraft-remote-typescript` PR #3、#4）。参考で、合わせなくてよい。値は仮。

- `ConnectOptions`の`responseTimeout`（仮の既定15分。最後の受信から数え、呼び出しごとに延ばせる）、`keepAliveDelay`（仮の既定30秒、
  TCPのkeepalive）、`reconnect`（既定で有効。仮の間隔は500msから30秒、諦めるまで5分）
- `onReconnect`（`ReconnectEvent`：前と後のhello、`server`と`session`と`catalogHash`が変わったか、eventのloss）
- 失敗の型は`CompletionUnknownError`（②③）と`NotSentError`（⑤A）。つなぎ直しで`auth_required`なら、pairingせずに`NotSentError`で止める
- つなぎ直しで戻すbuildは、成功した`build.setDimension`と`build.setOrigin`だけを追う。⑤Gは、OSのTCP keepaliveに任せる

### すること

1. 取得元を`335c604`へ固定し直し、CIでv1の54 caseをすべて通す。skipを残したら済みにしない
2. ③⑤を決定のとおりに入れる。APIの形は、前の票で返した案（自分の節）から始める
   - ③の既定の長さは、普通に使っていてtimeoutを感じない長さにする。選んだ値と、そう選んだ理由（実測したなら、その結果）を返す
   - ⑤のA〜Gと、`2026-11-12-05`を入れる
3. v2の12 caseをCIへつなぐ。libraryにまだ無い機能のcase（FASTと`connection.flush`、entity handle、event cursor、catalogの
   cacheなど）は、todoとして理由を返し、合格に数えない。無い機能のための⑤の条件は、その機能を入れるときに満たす
4. F1に無い流れは、担当のunit testで確かめる。少なくとも、F1-AU-12の先（応答を失ったpollの後に、同じ`pairing_id`の次のpollを
   新しい接続で送り、承認の後にtokenつきのhelloへ進む）と、⑤E（同時に複数の呼び出しが切断に気づいても、つなぎ直しは1回）
5. 直すときは、そのcase（F1に無ければ担当のunit test）が、直す前に意図した理由で落ちることを見てから直す
6. 次のことを返す（検討メモの「6. 確かめること」の、各Client Libraryの項）
   - ③の生存確認を設定できるか（TCPのkeepalive。browserではどうなっているか）と、既定にしたもの
   - 1つのclientのobjectを、複数のスレッド（または同時に走る複数の呼び出し）から使えるか
7. 実McRemoteとのpulse（hello → `world.setBlock` → `world.getBlock`）を1本通す。相手は担当の手元のPaperと、公開のMcRemote
   `2321.1.0`（`protocol_mismatch`はcode `-32600`で届くが、reasonで判定するので通る）。つなぎ直しも実機で見られるなら（例：
   PaperやMcRemoteを止めて戻した後の次の呼び出し）、手順と結果を返す。Minecraftの中での承認やPaperの再起動など、人の操作が
   要るなら、その前で止めて手順を返す（human ownerが行う）。「live-auto相当」で、scriptとPASSのsummaryを残す
8. 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい（権限で拒まれたら、human ownerが行う）。tag、Release、公開の
   workflowの実行はしない
- caseが契約と違う、または読み方が決まらないと思ったら、そのcaseのIDと理由を返す。決まっていないことは、clientで新しく決めない
- token、`pairing_id`、private endpoint、host、IP、player名、座標を、返却と公開のartifactへ書かない

## Python

- 前の票で返した③⑤の今：応答の待ちはsocketのtimeoutで60秒。超えると接続を回収する。呼び出しごとの設定と、最後の受信から
  数えるtimerは無い。生存確認とつなぎ直しは無い
- 案：`ConnectionOptions`、`LivenessOptions`、`ReconnectOptions(enabled)`、`on_reconnect(ReconnectInfo)`、`call_options`、
  `RequestNotSentError`と`CompletionUnknownError`（どちらも`ConnectionLostError`の子）
- 60秒は、③の「timeoutを感じない長さ」に足りるかを見直す。最後の受信から数えるtimerにする
- 正面の入口は`Minecraft.create()`（`2026-08-02-06`）。つなぎ直しで戻すdimensionとoriginは、`setBuildOrigin`などで最後に成功を
  確かめた値

## Java

- 前の票で返した③⑤の今：`readTimeout`が既定10秒。超えると、そのidだけを失敗にして接続を使い続ける。これは③の却下案「timeoutの
  後も接続を使い続ける」に当たるので、直す（超えたら、その接続の応答待ちをすべて完了不明にして接続を回収する）。生存確認と
  つなぎ直しは無い
- 案：`Builder.responseTimeout`、TCPのkeepalive、`Builder.autoReconnect`（既定true）、`reconnectListener`、`CompletionUnknownException`
  と`NotSentException`（どちらも`TransportException`の子）
- 既定の申告protocolは`23.0.0`のまま（human owner「24.0.0で揃えば問題ない」）。F1のcaseは`23.2.1`の申告を使ってよい

## Scratch

human ownerが、前の票で案として返った次のことを決めた（2026-11-12）。この票で入れる。

- ⑦：認証reasonで対象のtokenだけを捨て、tokenなしのhelloへ戻る。`auth_required`の後だけpairingへ進む。tokenなしで成功したら、
  pairingの表示もpairing完了のhatも出さない。一接続試行に一度だけ、は今のまま
  - pairing完了のhatは、tokenを保存した時ではなく、続くhelloが成功した時に発火する
- ⑧：次のpollを送る前にも、clientの期限を調べる。localな期限切れには、判断元が分かる内部の属性を持たせ、serverのcodeとreasonは
  作らない。案内はserverの`pair_expired`と同じ意味にし、どちらが判断したかは観測で見分けられるようにする
- ②：WebSocketのclose codeとreasonを、応答待ちの失敗から分ける（transportのdiagnosticは接続の観測に残す）。表示の重複の
  除き方も合わせて直し、同じ配信失敗の案内が二重に出ないようにする
- F1：前の票の案のとおり、browserの側（VMのFakeWebSocket）でつなぐ。`335c604`のどのcaseをbrowserの側で確かめ、どれをBridgeと
  toolingのTCPの側に置くかを、IDの一覧で返す。v2の12 caseについても、同じように分ける。browserの側のPASSは、直接のTCPの
  PASSとは別に数える（Protocol Inventoryの「共有fixtureの使い方」）。そのため、上の「すること」の1と3は、browserの側で
  確かめられるcaseに読み替える
- ③⑤：前の票の案（内部のconnection policyの`requestIdleTimeoutMs`と`autoReconnect`、一つの再接続Promiseを共有、最後に成功した
  dimensionとoriginのsnapshot、`McRemoteCompletionUnknownError`と`McRemoteNotSentError`、read-onlyの接続event）で入れる。この票では、
  新しいblockと表示を足さない。つなぎ直しの知らせとFASTとflushの境界を、blockや表示へどう見せるかは、案にして返す（human ownerが
  決める）
- 生存確認：browserのWebSocketのAPIからはpingを送れない（検討メモの「3」の3）。VMで見つけられること（closeとerror、③のtimer）
  を入れ、Bridgeから送るpingが要るかは、案にして返す
- `2026-11-12-05`：plugin側のTCPはBridgeが持つ。McRemoteが承認を待つ間に認証前のTCPを閉じたとき、Scratchの側でpollが続くかを
  確かめて返す
- 変えたblock、hat、表示の文言は、前と後を返す

## C#

- 前の票で返した③⑤の今：入れていない。案は`ClientOptions.ResponseIdleTimeout`と呼び出しごとの`RequestOptions.ResponseIdleTimeout`、
  `ClientOptions.AutoReconnectEnabled`（既定true）、`ConnectionRestored`の通知。つなぎ直しで認証が要れば、pairingせずにcallerへ返す
- 承認を待つ間に認証前のTCPが閉じたときの続け方は、前のPRで入れた。F1-AU-11、12と、上の「すること」の4で確かめる
- v2は初めてつなぐ。applicationの呼び出しと、仮想の時計のopsを表すrunnerが要る（`CLIENT_BOOTSTRAP_V2_ja.md`）
- `ConnectionRestored`などの通知はbackgroundのthreadから呼ばれうる。Unityでどう受けるか（main threadへ戻す例）を、docsに書く
- library projectのtargetは`netstandard2.1`のまま

## TypeScript

- ③⑤は入れてある。この票では、取得元を`335c604`へ固定し直し、F1-AU-11、12と、直したF1-OP-08を通す
- OP-06（FASTとflush）とOP-11（handle、cursor、catalogのcache）は、機能が無いので、todoのままでよい
- 上の「すること」の4（F1-AU-12の先、⑤E）を、unit testに無ければ足す
- 認証の流れを変えたら、pulseを1本通す。変えなければ、しなくてよい

## 返却

- 実際に読んだknowledge commit、PRの番号、merge commit、CIのrun ID
- fixtureの取得元の前と後（commit、copyならfileごとのbytesとSHA-256）と、fileごとのcase数とPASS数（todoにしたcaseのIDと理由）
- ③⑤の入れた形：API、既定の値とその理由、失敗の型、知らせの形、⑤のA〜Gと`2026-11-12-05`をどう満たしたか、それを確かめたtest。
  落ちるのを見てから直したなら、そのcaseと前と後
- 「すること」の6の答え
- pulse：日付、Paperの版、McRemoteの版、手順、結果、認証の方法、片付けの方法。つなぎ直しを実機で見たなら、その手順と結果
- 違うと思ったcase、決めずに残したこと
- Protocol Inventoryの「共有fixtureの使い方」の自分の行の、前と後
- Scratchだけ：browserの側とTCPの側に分けたcaseのIDの一覧。変えたblock、hat、表示の文言の前と後。blockや表示への見せ方の案。
  Bridgeのpingの案

## coordinatorがすること

- 返却を、GitHubのAPI（PR、merge commit、CI、fixtureのbytes）で照合し、Protocol Inventoryへ写す
- 各clientの既定の値と、生存確認の答えを突き合わせる。検討メモの「6」のMcRemote、Stack、WireScopeの項は、別の票にする
