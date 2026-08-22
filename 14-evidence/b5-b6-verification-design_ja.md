# b5／b6 横断検証設計

この文書は、DECISIONS `2026-08-16-04`〜`07`、`2026-08-19-01`／`02`、`2026-08-20-03`／`04`、
`2026-08-21-01`で確定したprotocol 22の
plugin APIについて、何をどのtest classで
確かめるかを示します。未実施の計画をevidenceと呼ばず、実行後にだけrecord／artifactを作ります。
wire contractは[wire-format-design](../10-protocol/wire-format-design_ja.md)を正とします。

build execution modeのplugin／Python／Scratch／WireScope検収と横断evidenceはb5 completion gateであり、
一部surfaceの合格だけからb5全体GREENを推測しません（`2026-08-20-04`）。一方、full load／soakと
capacityの最終較正、Scratch browser保存はb5 completion gateへ含めません（`2026-08-21-02`）。

### b5 GREENの最小横断gate

b5は次を一組で閉じます。

- queue／ring／poll／handle／particle／work／timeoutへ有限な暫定値を置き、値と境界挙動をcandidateへ固定する。
- 3種event、block query、height／spawn、DEBUG／TRACE／FAST、`connection.flush`をplugin fixtureへ適合させる。
- Python／Scratch／WireScope v1.1を同じfixtureへ適合させ、clean artifactを生成する。
- 実pluginの短いevent／block／spawn／mode smokeとreal-browser WireScope E2Eを通す。
- 無制限queue、無言drop、partial side effect、synthetic responseが無いことを確認する。

最適capacity、授業相当load、長時間soakはb6 API実装後の本較正で扱います。b5で採った暫定値は
protocol不変定数や最終運用値と主張しません。

## 1. Unit／deterministic

各dev repositoryのtestと固定commitで次を閉じます。

- event DTOがBukkit Event objectを保持せず、world／originを発生時にcaptureする。
- `BlockSpec`／`BlockValue`のstrict shape、stateless blockの`state:{}`、短縮ID／部分state入力、
  完全修飾ID／full state出力、set→getの意味的round-trip。
- protocol 21／22の混在がhelloで拒否され、文字列refとobjectのunion受理が無い。
- id付きset成功resultがexact `null`、notificationが正常／拒否とも無応答で、event blockは`BlockValue`を維持する。
- `getBlocks`が端点反転でもx→y→z（z最速）を維持し、各軸10／総数1000をworld access前に拒否する。
- `getBlockWithData`が`method_not_found`、JSON numberがscale非依存、`data.path`が規定形である。
- Pythonの`block_id`／`state` APIと`BlockValue`、Scratchの一回取得snapshot／accessor、
  sprite-local保存、共有last-block不在、clone／disconnect lifecycle。
- paired playerの全active epochへ複製し、ring／sequence／cursorがepoch間で独立する。
- stale／latest／future cursor、非破壊poll、overflow／capacityの累積値。b5のclear／filtered値は0、
  b6でfilter／clearを追加する。
- `events.poll`の省略／`max_events`希望上限、server上限、未知option拒否。
- compact responseが61,440 bytesを越えず、schema v1.1／session envelope投影後のsingle encoded frameが
  65,536 bytesを越えない。
- right-clickのmain／off-hand正規化fixture。
- handleのformat、同epoch同entityの同値、foreign／unknown同値化、disconnect失効、slot予約。
- `world.getHeight`のmax_y inclusive、world上端、空列、多層、origin相対、work admission。
- 連続位置の小数第3位、角度の小数第2位に対する正負の`HALF_UP` tie、負のゼロ除去。
- yawの`[-180,180)`境界（`180`／`181`／`-181`／`540`とround後の`180`再正規化）。
- pitchの`-90`／`90`受理と範囲外`invalid_params`、clamp禁止、失敗時状態不変。
- set入力を事前roundせず、適用後再取得resultだけを正準化すること。block座標等integerの小数拒否。
- `projectile_hit`連続位置がcapture時に正準化され、ring／poll／clientで再roundされないこと。
- `world.spawnParticle`の座標先行9／10 params、force省略時`true`／明示`true`／`false`、旧順序拒否、
  非有限座標、負offset／speed、小数／負count、unknown／typed-data-required、work／backpressure、
  accepted count result。
- `world.spawnEntity`の座標先行4 params、旧順序拒否、unknownでCOW等を生成しないこと、player／
  spawn不能type、capacity拒否時の副作用不在、epoch-scoped handle、結果不明時retry禁止。
- b6のnearbyに対するbounded scan／player除外／partial handle禁止、remove失効。
- b6 signの4行／面／state検証とrollback、typed particleの有限schema。
- Python cursor／retry／handle投影、Scratch thread-local event context／monitor guard。
- WireScope schema v1.1 validatorとartifact compatibility set。
- bounded thread-safe connection FIFO、notificationの無言drop禁止、backpressure中の順序維持。
- 正常／拒否notificationから`connection.flush`までのbarrier、後続command非包含、epoch非跨越、
  flushが個別成功を集約しないこと。
- PythonのDEBUG／TRACE／FAST、全modeのsetter `None`、mode transition fence、自動flush／明示flush。
- Scratchの保存されるmode block、main stream共有、並行script登録順、thread-local TRACE delay、tab close非保証。
- TRACE delayの`0`／`0.25`／`2.0`受理、範囲外拒否とclamp不在、Pythonの本体例外優先、
  WireScopeの`sent-unconfirmed` exact表示。

## 2. Live-auto

実Paper serverと複数clientを使い、sanitized transcriptをrelease gateに必要な回だけ保存します。

1. 2 playerでeventが相互混入しない。
2. 同一playerの2 active connection epochが同じeventをそれぞれpollできる。
3. response喪失後に同cursorで再取得し、副作用を再実行しない。
4. ring overflow／capacity拒否のcounterとsequence gapが一致する。filter／clearはb6試験で追加する。
5. disconnect／reconnectで旧cursorとhandleが使えない。
6. event後にbuild world／originを変更してもDTOが変わらず、clientの不一致guardが作動する。
7. b5ではentityのunload／外部world移動を確認し、b6でremove／`entity.setPose` world移動を実Paper挙動と照合する。
8. b5ではspawn、particle、heightをwork limit境界の内外で確認し、b6でnearby／signを追加する。spawn系はfractionalな
   origin相対座標を事前roundせず、座標先行paramsでplugin／Python／Scratch／WireScopeが一致すること、
   particleのforce省略時`true`と未知entityの副作用不在も確認する。
9. WireScopeへScratch／Pythonの両sourceを順に接続し、b5 method／result／error／lossを同じUIで確認する。
10. player／projectile／entity poseの正準値がplugin、Python、Scratch、WireScopeで一致し、入力精度を
    副作用前に失っていないことを確認する。
11. stateless／stateful blockをPythonとScratchからset→getし、同じ構造化値をWireScopeで確認する。
12. 同一座標への複数FAST notification→flushでFIFO順の最終値を確認し、不正notification→flushでは
    responseが捏造されずworld不変、flush自体は個別errorを集約しないことを確認する。
13. queue capacity境界でnotificationの無言drop／flush追越しがなく、保持不能時はconnectionとflushが失敗する。

## 3. Real-browser／live-human

共通appの実browser UI、Scratch hat／thread context、monitor-driven reporter、entity handle受領を人間が
操作して確認します。plugin wire fixture合格だけでこのgateを代替しません。

- mixed event batchからtype別hatがFIFOで起動し、各threadが自分のDTOを読む。
- shared last-event／last-entityへの依存がない。
- overflow／capacity lossが利用者に見え、Minecraft control pathは継続する。
- monitorの連続評価がthrottle／coalescingされ、明示script callは省略されない。
- `height_not_found`が通常の高さ値と区別でき、actionableに説明される。
- non-idempotent operationの結果不明時にclientが自動retryしない。
- 長いnative小数が座標3桁／角度2桁の同じwire値として表示され、raw frameとclient値が一致する。
- Scratchの一つの`ブロック情報` snapshotからIDと複数state propertyを取り出し、sprite間で
  暗黙共有されず、Stage変数へ入れた場合だけ明示共有される。
- StateTextのcatalog型解決、表現不能token拒否、BlockInfoText、`⟦mcr-error:<reason>⟧`の
  exact grammar／remote reason allowlist、PickerのID／state原子的Undoを確認する。
- Scratchのmode blockが`.sb3`へ保存され、読込だけでは適用されず、実行後にmain stream全体へ作用する。
- TRACEが成功後に呼出元threadだけを待たせ、FASTがmachine token `sent-unconfirmed`、
  日本語「送信済み・結果未確認」、英語`Sent · unconfirmed`として見え、明示flushがbarrierとして見える。
- Python／Scratch両sourceのnotificationと`connection.flush`をWireScopeが区別し、synthetic resultを作らない。

## 4. Evidenceの着地条件

正式recordには、knowledge contract commit、plugin／Python／Scratch／WireScopeの固定SHA、artifact identity、
test class、実行範囲、PASS／FAIL、未検証範囲を記載します。token、`pairing_id`、UUID、private host等のraw値は
公開せず、主張のスコープを実行したcaseから越えません。pair codeと表示用pair commandは通常log／公開evidenceへ
収録でき、redactionを要求しません。b5の暫定capacity値は境界fixtureと短いsmokeの
採用理由を伴うimplementation contractとして着地し、b6 API実装後の本較正では全methodを載せた実環境の
load／soak結果と更新理由を別recordへ残します。runtime policyの更新を横断version contractの変更と混同しません。
