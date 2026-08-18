# b5／b6 横断検証設計

この文書は、DECISIONS `2026-08-16-04`〜`07`で確定したplugin APIについて、何をどのtest classで
確かめるかを示します。未実施の計画をevidenceと呼ばず、実行後にだけrecord／artifactを作ります。
wire contractは[wire-format-design](../10-protocol/wire-format-design_ja.md)を正とします。

## 1. Unit／deterministic

各dev repositoryのtestと固定commitで次を閉じます。

- event DTOがBukkit Event objectを保持せず、world／originを発生時にcaptureする。
- paired playerの全active epochへ複製し、ring／sequence／cursorがepoch間で独立する。
- stale／latest／future cursor、非破壊poll、overflow／capacity／clearの累積値。
- compact responseが61,440 bytesを越えない。
- right-clickのmain／off-hand正規化fixture。
- handleのformat、同epoch同entityの同値、foreign／unknown同値化、disconnect失効、slot予約。
- `world.getHeight`のmax_y inclusive、world上端、空列、多層、origin相対、work admission。
- 連続位置の小数第3位、角度の小数第2位に対する正負の`HALF_UP` tie、負のゼロ除去。
- yawの`[-180,180)`境界（`180`／`181`／`-181`／`540`とround後の`180`再正規化）。
- pitchの`-90`／`90`受理と範囲外`invalid_params`、clamp禁止、失敗時状態不変。
- set入力を事前roundせず、適用後再取得resultだけを正準化すること。block座標等integerの小数拒否。
- `projectile_hit`連続位置がcapture時に正準化され、ring／poll／clientで再roundされないこと。
- particle／entity catalog ID、typed-data拒否、spawn前検証、fallback禁止、結果不明時retry禁止。
- nearbyのbounded scan／player除外／partial handle禁止、remove失効。
- signの4行／面／state検証とrollback、typed particleの有限schema。
- Python cursor／retry／handle投影、Scratch thread-local event context／monitor guard。
- WireScope schema v1.1 validatorとartifact compatibility set。

## 2. Live-auto

実Paper serverと複数clientを使い、sanitized transcriptをrelease gateに必要な回だけ保存します。

1. 2 playerでeventが相互混入しない。
2. 同一playerの2 active connection epochが同じeventをそれぞれpollできる。
3. response喪失後に同cursorで再取得し、副作用を再実行しない。
4. ring overflow／capacity拒否／clearのcounterとsequence gapが一致する。
5. disconnect／reconnectで旧cursorとhandleが使えない。
6. event後にbuild world／originを変更してもDTOが変わらず、clientの不一致guardが作動する。
7. entityのremove、unload、外部world移動、`entity.setPose` world移動を実Paper挙動と照合する。
8. spawn、particle、height、nearby、signをwork limit境界の内外で確認する。
9. WireScopeへScratch／Pythonの両sourceを順に接続し、b5 method／result／error／lossを同じUIで確認する。
10. player／projectile／entity poseの正準値がplugin、Python、Scratch、WireScopeで一致し、入力精度を
    副作用前に失っていないことを確認する。

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

## 4. Evidenceの着地条件

正式recordには、knowledge contract commit、plugin／Python／Scratch／WireScopeの固定SHA、artifact identity、
test class、実行範囲、PASS／FAIL、未検証範囲を記載します。token、pair code、UUID、private host等のraw値は
公開せず、主張のスコープを実行したcaseから越えません。exact capacity値は試験結果と採用理由を伴う
implementation contractとして着地し、横断決定を無根拠に書き換えません。
