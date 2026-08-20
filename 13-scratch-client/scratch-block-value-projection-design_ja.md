# Scratch block value投影・Picker・ErrorText設計

## 1. この設計が決めること

protocol 22のwireは`block_id`と`state` objectを分ける。Scratchはrecordを第一級値として
持たないため、Scratch-visibleな値へMinecraft Java版のblock state記法を投影する。

```text
StateText:     axis=z,open=false
BlockInfoText: minecraft:oak_log[axis=z]
ErrorText:     ⟦mcr-error:unknown_block⟧
```

この文字列表現はScratch内の値モデルである。plugin wire、Python、WireScopeへ逆流させず、
protocol 21の文字列`block_state_ref`互換shimとしても扱わない。共通の構造化値は
[ブロック値・状態・多言語投影設計](../10-protocol/block-value-design_ja.md)を正とする
（決定`2026-08-19-04`）。

## 2. StateText

set系blockはblock IDとstateを別入力として持つ。

```text
[x] [y] [z] に
ブロックID [oak_log]
状態 [axis=z]
を置く
```

StateTextはMinecraft block stateの角括弧内だけを表し、外側の`[`／`]`を含めない。
空stateの正式表現は空文字であり、malformed入力のfallbackではない。

```text
""                                      → {}
axis=z                                  → {"axis":"z"}
facing=east,open=true                   → {"facing":"east","open":true}
```

### 2.1 文法と正準形

```text
state-text = "" | pair ("," pair)*
pair       = property "=" token
property   = [a-z0-9_]+
token      = [a-z0-9_./:-]+
```

- Scratchが生成するpropertyは名前の昇順とする。
- 空白、重複property、末尾comma、空要素、property／value欠落を許容しない。
- 入力全体の前後にあるASCII spaceだけは除去できる。tab、改行、内部空白は拒否する。
- `,`、`=`、`[`、`]`または上のtoken文法外の文字を含むcatalog valueはStateTextで表現不能とする。
- 表現不能値をescapeして独自文法へ変えず、`unsupported_state_token`として送信しない。
- property／valueにはmachine tokenだけを使い、日本語名や英語表示名を保存・送信しない。

受理した`open=true,axis=z`は`axis=z,open=true`へ正規化する。入力の字面ではなく、
正規化後のStateTextをScratch projectへ保存する。

### 2.2 JSON型の解決

StateText単独では`false`がbooleanかstringか、`3`がnumberかstringかを決めない。helloの
`catalogHash`と一致するcatalogによりpropertyのJSON型と許容値を解決する。

- 空StateTextはcatalogなしでも`{}`へ変換できる。
- 非空StateTextは適合catalogがある場合だけwire objectへ変換する。
- catalog未取得、不一致、利用不能時に字面から型を推測しない。
- JSON numberはcatalogのnumberとscale非依存で比較する。`3`と`3.0`は同じ数値だが、string`"3"`は別型である。
- catalogで型や値を解決できなければ送信せず、actionableなErrorText／表示を返す。
- client検証は入力支援であり、server registryによる最終validationを置き換えない。

## 3. BlockInfoText

`world.getBlock`の`BlockValue`は、完全なMinecraft block表記へ投影する。

```text
minecraft:gold_block
minecraft:oak_log[axis=z]
minecraft:bamboo_door[facing=east,half=lower,hinge=left,open=true,powered=false]
```

- block IDは完全修飾する。
- stateはfull stateとし、propertyを名前の昇順にする。
- stateを持たないblockには角括弧を付けない。
- sprite ID、stream ID、credential、capability、catalogHashを埋め込まない。
- 一回の`world.getBlock`から作るimmutable snapshotとし、ID／stateごとに通信しない。
- BlockInfoTextの解析でも§2.1のproperty／token文法を使う。

## 4. Scratch block surface

```text
([x] [y] [z] のブロック情報)
([ブロック情報] のブロックID)
([ブロック情報] の状態)
([ブロック情報] の状態 [property])
<([ブロック情報] に状態 [property] がある)>
<([値] はMcRemoteエラー)>
```

最初のreporterだけが通信する。成功時はBlockInfoText、JSON-RPC error時はErrorTextを返し、
失敗を空文字や前回成功値へ畳まない。monitor評価ではthrottleと同一引数のin-flight coalescingを
使い、明示script callは毎回通信する。disconnect時に通信cacheを破棄する。

残りは通信しない純粋accessor／predicateである。propertyが無いとき、存在predicateはfalse、
property accessorは`unknown_state_property` ErrorTextを返す。malformedな一般文字列は
`invalid_block_info`とし、ErrorText入力は元reasonを保ったまま伝播する。

```text
[調べたブロック v] を ([0] [0] [0] のブロック情報) にする

もし <([調べたブロック] はMcRemoteエラー)> なら
  [調べたブロック] と言う
でなければ
  [10] [0] [0] に
    ブロックID ([調べたブロック] のブロックID)
    状態 ([調べたブロック] の状態)
  を置く
end
```

## 5. ErrorText

ErrorTextのexact shapeは次とする。

```text
⟦mcr-error:<reason>⟧
```

`reason`は`[a-z][a-z0-9_]*`に一致する安定enumである。`⟦`／`⟧`はMinecraftのblock ID／
StateText文法に現れないため、`error:foo`のような正規namespaceと衝突しない。predicateは単なる
prefix一致でなく、ErrorText全体のexact grammarを検証する。

remote JSON-RPC errorはcompatibility fixtureのallowlistにある`data.reason`だけを同名ErrorTextへ
写す。未知reason、文法外reason、`data.reason`欠落は`⟦mcr-error:remote_error⟧`へ畳む。
message、入力全文、任意の`error.data`をErrorTextへ連結しない。

主なローカルreasonは次とする。

- `invalid_block_info`
- `invalid_block_state`
- `unknown_state_property`
- `catalog_unavailable_for_state`
- `unsupported_state_token`
- `remote_error`

ErrorTextは通常のScratch値として変数へ保存・比較できるが、extension共有のlast-error stateは
作らない。localized actionable messageは制御値と分離し、localeごとに表示できる。command blockの
server errorをbranch可能なresultへ変えることは本sliceに含めない。

## 6. Catalog Picker

Pickerはblock ID入力とStateText入力を一つの操作で編集する。

- 新しいblockを選んだ直後はStateTextを空にする。
- UIでは全propertyとMinecraft既定値を見せる。
- 利用者が変更したpropertyだけを明示指定へ加える。
- 「既定値に戻す」でそのpropertyをStateTextから除く。
- 既存StateTextを開いた場合は明示property集合を維持する。
- 変更せず適用した場合は意味を変えない。
- block IDを変えた場合は旧blockのstateを引き継がない。
- get由来のfull stateは全propertyを明示指定として保持できる。

IDとStateTextは一つのBlockly event groupで原子的に更新し、Undoでも同時に戻す。どちらかの
入力へvariable／reporterが接続されている場合は両方とも変更せず、接続を黙って外さない。
読取専用でPickerを開くことは許容し、適用不能理由をactionableに表示する。

## 7. 多言語表示と検索

machine tokenは翻訳しない。表示・検索metadataだけをlocalizeする。

- block名はen／jaを持ち、ja-Hiraはjaへfallbackしてcanonical IDを併記する。
- state property／valueはja-Hira、ja、enとmachine tokenを扱う。
- 1段目に現在locale、2段目に英語表示名とmachine tokenを示す。
- metadata欠落時もmachine tokenを隠さない。
- ja-Hira、ja、en、machine token、登録済みaliasを空白区切りAND検索する。
- 保存・送信するのはmachine tokenだけである。

block名全件のja-Hira翻訳はb5 gateにしない。stateのja-Hira表示と混同しない。

## 8. sprite／thread lifecycle

BlockInfoText、StateText、ErrorTextは通常のScratch値として扱う。

- 「このスプライトのみ」の変数へ保存できる。
- Stage変数へ保存した場合だけ明示共有する。
- cloneは通常のsprite-local variable複製規則に従う。
- extension共有のlast block、last state、last errorを作らない。
- accessorはtarget非依存の純粋処理とする。
- visible valueへtarget identityを埋め込まない。
- b5のmain stream 1件でもspriteごとの値処理を独立させる。
- 将来substreamへ写像してもvisible value shapeを変更しない。

### 8.1 build execution mode

Scratchの正典操作は、接続panelのhidden settingでなく保存されるcommand blockとする。

```text
建築モードを [TRACE ▼] にする（TRACEの待ち時間 (0.25) 秒）
```

blockと入力値は`.sb3`へ保存されるが、project読込だけでruntime stateを復元しない。実行すると呼出元が属する
現在streamのclient execution policyを変更する。新しいstreamの既定はDEBUG／`0.25`秒である。b5はmain stream
1件なのでStage、sprite、clone、全scriptが同じmodeを共有し、将来substreamを追加した場合はstreamごとに分離する。
module global、browser global、`localStorage`へ保存せず、modeをwire params／helloへ送らない。

mode blockはmodeとTRACE delayを検証し、connection送信sequencerへ一つのtransitionとして登録する。後続commandの
登録を止めて`connection.flush`を待ち、成功後に両値を原子的に変更してから後続を再開する。失敗時は旧modeを維持し、
actionable errorを出す。各setは登録時点のmodeとdelayを保持する。別scriptとの境界はVMの実行開始時刻でなく
connection送信列への登録順とし、flushとlocal mode更新の間へsetを割り込ませない。

TRACE delayは`0`以上の有限numberとし、不正値を`0`へ丸めない。TRACEのset成功response後に、そのset blockを
実行したScratch threadだけを待たせる。connection全体や別scriptは止めず、`setBlocks`一回につき一回だけ待つ。
error時は待たず、後のmode変更で成立済みのdelayを取り消さない。DEBUG／FASTでも入力欄と値は維持するが使用しない。
runtime固有の最大値は実装fixtureで固定する。

DEBUGはrequest responseを待ち、TRACEはresponseと成功後delayを待つ。FASTはnotificationを登録後、通常は呼出元を
継続し、transport逼迫時だけfinite bufferのbackpressureを受ける。FASTのserver-side成功／errorを捏造せず、
WireScopeではsent／unconfirmedとして扱う。StateText／catalog等のlocal validation errorはmodeにかかわらず表示する。

FASTの明示barrierとして、`connection.flush`へ対応する次のcommand blockを設ける。

```text
送ったブロック設置が終わるまで待つ
```

flush失敗はactionable errorとする。明示的な切断等、responseを待てる終了経路はflushできるが、tab close、reload、
navigationで完了を保証しない。接続panelは現在のmode／delayを表示できるが、b5では第二の変更面にしない。

## 9. protocol 21との関係

protocol 21／b4はGitHub prereleaseとして公開済みだが、stableな作品利用へ入っておらず、
一体文字列入力を保護すべき運用実績もない。このため次を作らない。

- b4一体文字列入力からb5二入力への`.sb3` migration
- protocol 21／22のunion受付または自動判定
- protocol 21 StateText shim
- b4 project load warning／作品互換fixture

b4 artifact、tag、evidenceは当時の実装事実として保持する。

## 10. fixtureと実装gate

Scratch fixtureは最低限、次を固定する。

1. 空／単一／複数property StateTextと昇順正準化
2. boolean／number／stringのcatalog型解決とscale非依存number比較
3. 重複、欠落、末尾comma、内部空白、表現不能tokenの拒否
4. catalog未取得／hash不一致とpartial state wire object
5. BlockValueからBlockInfoText、ID、StateText、propertyへの投影
6. stateless／full stateとget→setの意味的round-trip
7. property存在predicate、欠落、malformed入力
8. ErrorText exact grammar、allowlist、unknown remote reason、伝播
9. Pickerのpartial state、default復帰、block変更、原子的適用／Undo
10. variable／reporter接続時に両入力を変更せず取り外さないこと
11. sprite-local、Stage共有、clone、並行thread、共有last-value不在
12. disconnect cache回収、monitor throttle、in-flight coalescing
13. mode blockとdelayの`.sb3`保存、読込だけではruntimeへ適用しないこと
14. main stream上の並行script、transition登録順、flush追越し禁止、失敗時の旧mode維持
15. TRACE delayが呼出元threadだけに作用し、`setBlocks`一回につき一回であること
16. FAST local validation／remote unconfirmed、明示flush、tab close非保証

plugin、Python、Scratch、WireScopeのfixtureとartifactをprotocol 22 compatibility setとして検収する。

## 11. 未確定として維持すること

- localized errorを出す具体的なUIとmonitor通知抑止
- ErrorTextの説明reporter
- command errorをbranch可能なresultにするScratch全体の設計
- catalog multilingual metadataのexact field schema
- 一段／二段表示の切替条件とaccessibility読み上げ文
- 実装commit、fixture path、artifact hash、real-browser／live evidence

## 12. 採用しない形

- Scratch公開値の主要操作をJSON object文字列にする。
- Scratch StateTextをplugin wire、Python、WireScopeへ戻す。
- state valueの型を字面だけから推測する。
- catalog不一致時に古い型情報で送信する。
- malformed StateTextやproperty欠落を空文字へ畳む。
- 正規block namespaceと衝突する`error:<reason>`をErrorTextに使う。
- remote reasonやmessageを無検証でScratch値へ連結する。
- ID／stateの片方だけをPickerで変更する。
- extension共有last-value、protocol 21 migration、互換unionを作る。
