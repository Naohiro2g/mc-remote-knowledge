# 各clientのCIでF1のfixtureを通す依頼（F3、Python・Java）

> 多言語Client LibraryのPhase E／F（`2026-10-23-01`、`10-protocol/polyglot-phase-ef-plan_ja.md`の「F3」）。F3の合格は、
> 各clientのCIでF1のfixtureが全件PASSし、実McRemoteを相手にしたpulseが1本通ること。human owner 2026-11-10：
> 「クライアントの多言語化を最優先とする。その先のUnity版マイクラリモコンを急ぐため」。この票は、各担当の受け持ちの中で
> 先にしてください。参照するknowledge commitは、この依頼が入ったmainのcommitです。Python担当は「共通」と「Python」、
> Java担当は「共通」と「Java」を読んでください。

## 共通

- 対象：minecraft-remote-tooling `8264c3881bb4128c14cda6d122641ebcfa67d9c5`の`packages/protocol/test/fixtures/`にある、F1の6本
  （`client-bootstrap-{framing,hello,pairing,blocks,errors,close}-v23.2.1.json`、44 case）と、schemaの
  `client-bootstrap-v1.schema.json`。scripted peerのデータの形は、同じcommitの`packages/protocol/README.md`にある
- toolingが、`protocol_mismatch`のcaseを`2026-11-10-01`に合わせる（F1-HE-09のdataに欄を足し、`-32600`で届くcaseを1つ足す。
  `00-hub/polyglot-f1-mismatch-fixture-instructions_ja.md`）。そのmerge commitをcoordinatorから伝えるので、同じPR（mergeして
  いれば次のPR）で取得元を固定し直す。それまでは`8264c38`で進めてよい
- 読み方：固定したcommitで読む（F2）。copyで持つときは、同じディレクトリの`LICENSE`（1,070 bytes、SHA-256
  `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`）も一緒に置く。共通のtest runnerは作らず、自分の言語の
  test runnerでloaderを書く
- `client-bootstrap-blocks-v23.2.1.json`の12 caseは、`value_refs`で同じディレクトリの`block-value-v22.json`を参照する。
  今つないでいなくても、その参照の範囲で読む
- 合格：CIで、F1の全caseがPASSする。skipを残したら、F3は済みにしない。caseが契約と違う、または読み方が決まらないと思ったら、
  そのcaseのIDと理由を返す（coordinatorがtoolingへ回す）
- `unresolved`を持つcaseは、`expected`に書いてあることを確かめる。`unresolved`に挙げたこと（EOFの時の扱い、応答待ちの
  requestの例外の型とtimeout、自動の再送など）は、clientで新しく決めない。決める必要が出たら、決めずに返す（E2で決める）
- `protocol_mismatch`は`data.reason`で判定し、codeでは分けない（`2026-11-10-01`）。`data.server`と`data.client_requires`は、
  errorから読めるように保つ
- caseに合わせてclientの振る舞いを直してよい。直したことは返却に書く。振る舞いを直すときは、そのcaseが直す前に意図した理由で
  落ちることを見てから直す
- 実McRemoteとのpulse：hello → `world.setBlock` → `world.getBlock`を1本通す。相手は、担当の手元のPaperと、公開のMcRemote
  `2321.1.0`。認証は、今あるlive testの方法を使い、その方法を返す。Minecraftの中での承認など、人の操作が要るなら、その前で止めて
  手順を返す（human ownerが行う）。token、pair code、host、IP、player名、座標は返却に書かない
- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。tag、Release、公開のworkflowの実行はしない

## Python

- 応答の版の互換判定を入れる（`10-protocol/versioning-design_ja.md`の「8.2 互換判定（クライアント側）」）。majorの一致、
  serverのminorが同じか上、patchは見ない。F1のF1-HE-04〜08が、その期待値（04と05は不一致、06〜08は一致）
- 不一致は、`Minecraft.create()`の失敗（`2026-08-02-06`⑤の「protocol mismatch」）にする。tokenは消さない（`2026-08-30-03`）
- 申告するprotocolは今の`23.2.1`のまま

## Java

- Javaが要求する最低のprotocolは`23.0.0`で、F1のhelloのcaseは、clientの申告を`23.2.1`としている。testでは、caseの申告の値を
  使ってよい。Javaの既定の申告を変えるかは、変えずに、案と理由を返す（human ownerが決める）

## 返却

- PRの番号、merge commit、CIのrun ID
- fixtureの取得元の前と後（commit、copyならbytesとSHA-256）
- fileごとのcase数とPASS数。直したclientの振る舞い（caseのIDと、前と後）
- 違うと思ったcaseと理由、決めずに残したこと
- pulse：日付、Paperの版、McRemoteの版（`2321.1.0`）、手順、結果。認証の方法
- Protocol Inventoryの「共有fixtureの使い方」の自分の行の、前と後
- Javaだけ：既定の申告のprotocolの案

## coordinatorがすること

- 返却を、GitHubのAPI（PR、merge commit、CI、fixtureのbytes）で照合し、Protocol Inventoryへ写す
- toolingの返却のmerge commitを伝える
- 違うと思われたcaseをtoolingへ回し、決めずに残されたことをE2の案に入れる
- TypeScriptの実装を始める票を作る

## 返却と照合（2026-11-10）

PythonとJavaとも、knowledge `5e00768911feb7be1e54ae3b7e9c2d776b88927a`を読んだ。coordinatorがGitHubのAPIで、PR、merge commitと
既定のbranchの先頭、CIのrunを確かめた。fixtureのcopyは、merge commitのtreeとtooling `8264c38`のtreeで、同じ名前のfileの
blobがすべて同じ（bytesが同じ）ことを確かめた。

| 担当 | PR | merge commit | CI | F1 |
| --- | --- | --- | --- | --- |
| Python | minecraft-remote-api #13（head `da304b95d245a6c2b1fb3df0154a766255664216`） | `161cd68514a1fbb018811d3cfab64cb29d5ac98b` | PRのrun 42798588428、merge後のrun 42799253920、どちらも成功 | 44 case PASS、skip 0（`tests/test_client_bootstrap_fixture.py`） |
| Java | minecraft-remote-java #2（head `ac042792a4faefdfe04440477ad1f2b88a3b3974`） | `e35144cd44f0622a7df1164e95960f1f44636435` | PRのrun 42787996203、merge後のrun 42788299291、どちらも成功（Temurin 21と25） | 44 case PASS、skip 0（`ClientBootstrapFixtureTest`） |

- 取得元：どちらもtooling `8264c3881bb4128c14cda6d122641ebcfa67d9c5`。F1の6本、`client-bootstrap-v1.schema.json`、
  `block-value-v22.json`（3,217 bytes、SHA-256 `e8e108d59c40751d67a432543d75cb4bf9146ef9781721012085c80545b854f3`）、`LICENSE`をcopyで持つ。
  toolingの追補（`ea7838a`）への固定し直しは、coordinatorが伝えてから次のPRで行う
- 違うと思ったcase：どちらも無し。`unresolved`に挙がったこと（EOFの例外の型、応答待ちのrequestのtimeout、自動の再送、
  承認を拒む専用の応答、messageの文言とcodeの番号）は、どちらも決めていない
- 直す前にcaseが意図した理由で落ちることを、どちらも確かめた
- pulseの扱い：human owner 2026-11-10「「live-auto相当」で良い」。Minecraftの中での承認はcredentialを用意する操作で、
  確かめた往復は自動。`2026-07-06-03`のlive-autoとして、scriptとPASSのsummaryを証跡にし、`14-evidence/`にrecordを置かない
  （Pythonの置く案は採らない）。記録はこの節

### Python

- 応答の版の互換判定を入れた（F1-HE-04〜08）。不一致は`Minecraft.create()`の失敗で、tokenは消さず、`protocol_mismatch`の
  dataに`server`と`client_requires`を保つ。申告は`23.2.1`のまま
- ほかに直したこと：JSONでない行と知らないidの応答を読み飛ばす（F1-FR-06、FR-07の相関）。socketの読み込みにUTF-8を明示する
  （F1-FR-01／02）
- 公開APIは増やしていない。不正な入力を送るcaseは、raw RPCで確かめた
- pulse：2026-11-10、Paper 1.21.11（build 132）、McRemote `2321.1.0`、Java 21.0.13。`scripts/auth_smoke.py`でhuman ownerが
  Minecraftの中で承認し、pulseは`pair=False`で同じtoken storeを使った。hello → 空気の位置を選ぶ → setBlock → getBlockで一致 →
  元へ戻す → getBlockで戻ったことを確認 → close。PASS。script `scripts/f3_bootstrap_pulse.py`（SHA-256
  `272f52ba17d76330b7785fedd02f4760e8e633c50374fa72819a47a9e533c24a`）
- 担当は、pulseのsanitizedな結果を`14-evidence/`へ置く案を返した。置かない（上の「pulseの扱い」）

### Java

- 公開APIに足したこと：`MinecraftRemote.Builder.buildContext(dimension, x, y, z)`（helloの`build`）、`ProtocolMismatchException`
  （`reason()`、`serverProtocol()`、`clientRequires()`。前は`ProtocolException`）。helloの`client`は、`clientIdentity(...)`を
  明示したときだけ送る（F1-HE-02の最小のhelloのため）
- ほかに直したこと：LF（0x0A）だけで行を区切る（前はCR／CRLFでも区切っていた。F1-FR-01〜06）。LFの無い末尾はEOFでも応答に
  しない（F1-FR-05、CL-03）。idごとの応答待ちの表で応答を対応させる（F1-FR-07。公開APIは同期のまま）
- server側の`protocol_mismatch`は、code `-32600`でも`-32000`でもreasonで判定する。toolingの`ea7838a`を手元で一時的に
  差し替えると、F1-HE-09とHE-10もPASSした（担当の返却。固定はまだ）
- pulse：2026-11-10、Paper 1.21.11（build 132）、McRemote `2321.1.0`。`examples`の`livePulse`で、human ownerがMinecraftの中で
  承認した。hello（`build`で原点を要求）→ setBlock（金のブロック）→ getBlockで`minecraft:gold_block`。PASS。1回目は承認が
  間に合わず`pair_expired`で終わった。置いたブロック1個はworldに残っている。担当は正式の根拠にしない扱いとした
- 既定の申告protocol（今は`23.0.0`）：担当の案はA「`23.0.0`のまま」（Javaが呼ぶmethodはすべて23.0.0にある。ただし
  `chat.post`の成功の`null`は23.2.1で版に刻まれた）とB「`23.2.1`へ上げる」（Pythonとfixtureにそろうが、使わない機能のために
  23.0〜23.1のserverを拒む）。human owner 2026-11-10：はじめに「B：23.2.1へ上げる」、続けて「撤回、A：23.0.0のままにする。
  24.0.0で揃えば問題ない」。既定の申告は`23.0.0`のまま
- toolingへの補足：F1-ER-01〜03の`matched_ids`の範囲をREADMEに書いてほしい（tooling担当へ伝える）
- `docs/polyglot-f3_ja.md`のpulseの項は、merge時点の「未実施」のまま。固定し直しのPRでPASSへ直す
