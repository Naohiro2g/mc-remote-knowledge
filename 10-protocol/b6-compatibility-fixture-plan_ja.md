# b6 compatibility fixture 計画

> 状態: 2026-08-27、Tier 2入口のsource監査結果。正本contractは
> [wire format設計](wire-format-design_ja.md) §5.4／§5.8.1、
> [versioning設計](versioning-design_ja.md) §10.11.4、DECISIONS
> `2026-08-26-05`／`2026-08-26-06`／`2026-08-26-08`を正とし、fixture ownerは
> `2026-08-27-02`で固定した。本書はcontractを増やさず、
> `b6-source-candidate-set-1`の既存testとの対応、gap、次のfixture化範囲を示す。

## 1. 目的と境界

b6の共有contractを、plugin／Python／Scratchの三実装が同じcaseとして読める単位へ分ける。
現在のcomponent testを捨てて一つの巨大suiteへ置き換えるのではなく、次を区別する。

- **共有fixture対象**: protocol `23.0.0`、現行／旧entity handle、sign三操作、`pickaxe_poke` DTO、
  protocol 23から除いたlegacy method。
- **代表live対象**: 一つの物理pokeを一eventへ畳むdedup、capture成立時だけの腕振り、signのworld mutation。
  これらをJSON decodeだけのfixtureで実証済みとしない。
- **Scratch client-only対象**: project／sprite browser保存、WireScope表示filter、`dropped_frames`、mini配置。
  server wire fixtureへ混ぜず、既存component testと実browser確認を使う。
- **観測範囲外**: 現行Scratch observer allowlistはsign三操作を投影しない。`2026-08-27-01`が
  observer allowlistを変更しないと明記しているため、b6ではsign API互換性の欠落でなく
  **WireScope v1の非必須観測範囲**と扱う。signはScratch APIと実worldで確認し、WireScope E2Eは
  hello／`pickaxe_poke`／現行allowlist method／`dropped_frames`で行う。

## 2. 監査したsource入力

| component | exact source | 監査した主なtest／fixture |
| --- | --- | --- |
| McRemote | `codex/b6-protocol23-cleanup@9b8b130808d8e1d1288f038dd04f738a86177e35` | `ProtocolInfoTest`、`SignCommandsTest`、`B5EventDtoTest`、`RightClickDeduplicatorTest`、`EntityHandleRegistryTest`、`RemoteCommandRegistrarTest` |
| Python | `codex/b6-protocol23-python@69a160aecfc6cd346b3341cdf10007e2903b5207` | `tests/test_b6.py`、`tests/test_b5.py`、`python-main-lifecycle.json`、`b5_values.py`、`observer.py` |
| Scratch | `agent/b6-integration@040f06617c80e54cdba9421b6c69445efdf099ba` | `@mc-remote/protocol`の`contract.test.ts`／`events-v23.json`、VMの`mcremote_event.js`／`mcremote_sign.js`／`extension_mcremote.js`、GUIの`mcremote-wirescope-source.test.js` |

これはGitHub上の固定SHAをread-onlyで照合した結果である。搬送元が報告したPASS件数を
横断PASSへ読み替えず、各testが何をassertするかだけを対応づけた。

## 3. canonical case 一覧

### 3.1 protocol／artifact identity

| case | canonical assertion | fixture／test class |
| --- | --- | --- |
| `B6-I01` | hello request／responseのprotocolは`23.0.0`。`22.0.0`と未対応`23.1.0`は互換扱いしない | 決定論的test＋代表hello pulse |
| `B6-I02` | b6の配布core／診断用client build labelは`2300.0.0b6`。この値をhelloの`protocol`へ載せない | source／artifact metadata test |
| `B6-I03` | protocol 23のmethod集合にsign三操作があり、除去対象10 methodは無い。serverへ届けば通常の`method_not_found`／`-32601` | registry／surface test。method不在の実server代表caseはTier 2 pulseで1件に絞れる |

除去対象10 methodは、`world.getNearbyEntities`、`entity.getPos`／`setPos`、
`entity.getRotation`／`setRotation`、`entity.getPitch`／`setPitch`、`entity.getYaw`／`setYaw`、
`entity.remove`である。

### 3.2 entity handle

| case | canonical assertion | fixture／test class |
| --- | --- | --- |
| `B6-H01` | protocol 23で発行・投影するhandleは`mcr_eh_` prefixを持つ | current positive fixture＋各validator |
| `B6-H02` | `mceh_`はprotocol 22の履歴であり、protocol 23のaliasとして受理しない | negative fixture＋plugin lookup／client validator |
| `B6-H03` | handleはconnection epoch scopedのopaque値で、clientはUUIDやentity属性をsuffixから復元しない | component semantic test。suffix長のclient共通固定は本fixtureのassertionにしない |

pluginの現実装は22文字のbase64url suffixを発行する。一方、現行contractがclientへ要求するのは
opaqueな`mcr_eh_`値の保持と旧prefix非受理であり、発行実装のsuffix長をclient validationの新しい横断contractへ
昇格しない。

### 3.3 sign三操作

| case | canonical assertion | fixture／test class |
| --- | --- | --- |
| `B6-S01` | `LineSpec`はstring shorthandまたは`{text,color?,decorations?}`。named 16色と`#RRGGBB`、5装飾だけを受ける | shared input cases＋各encoder／validator |
| `B6-S02` | `LineValue`は`text`／`color`／`decorations`を常に持ち、無色は`black`、装飾は名前昇順 | shared canonical result＋各decoder |
| `B6-S03` | `world.getSign([x,y,z])`はfront／back各4行と`waxed`を返し、waxedでも読める | shared request／result＋代表live |
| `B6-S04` | `world.setSign([x,y,z,{front?:[4],back?:[4]}])`は指定面を面内no-mergeで置換し、成功`null` | shared request／result＋代表live |
| `B6-S05` | `world.updateSignLine([x,y,z,face,line_index,LineSpec])`は0始まり`0..3`の一行だけを更新し、成功`null` | shared request／result＋代表live |
| `B6-S06` | shape／face／index違反は`invalid_params`＋可能なら`data.path`、未知style tokenは`invalid_property_value`＋property／value／allowed | shared negative cases＋各validator |
| `B6-S07` | `not_a_sign`、writeの`sign_waxed`／`sign_update_failed`を安定reasonとして扱う。stale時は部分更新を残さない | error fixture＋plugin mutation test／live。stale競合のlive済みとはしない |

Scratch v1のwrite blockはstring shorthandだけを公開するため、Scratch UIにobject形式writerが無いことを
`B6-S01`不適合としない。ただし`@mc-remote/protocol`のTypeScript contract mirrorは、wireが受理する
完全な`LineSpec`／`LineValue`を表現しなければならない。

### 3.4 `pickaxe_poke`

| case | canonical assertion | fixture／test class |
| --- | --- | --- |
| `B6-P01` | event typeは`pickaxe_poke`、payloadは`dimension`／`origin`／`pos`／`face`／`block`／`hand`／`item`。`item`は完全修飾key | shared `events.poll` result＋plugin DTO／client decoder |
| `B6-P02` | protocol 23 clientは旧`block_right_click`を現行eventとして受けない | negative decode case＋旧event producer不在のstatic確認 |
| `B6-P03` | capture gateはpickaxe、配送先は操作playerのsession、vanilla interactionをcancelしない | plugin test／code inspection＋代表live |
| `B6-P04` | 同一player／dimension／座標／tickの二回目callbackをhand非依存で畳み、一物理pokeを一eventにする。active sessionがあるcapture時だけ腕を振る | plugin deterministic＋live-human。共有JSON fixtureの主張外 |

positive fixtureの`hand`は現行plugin出力とScratch型に合わせ`main`／`off`を使う。現行wire説明が
invalidなhandの拒否まで独立に固定していないため、このTier 2では未知handのnegative caseを追加しない。

## 4. 現行testとの対応

| case群 | McRemote | Python | Scratch | 判定 |
| --- | --- | --- | --- | --- |
| `B6-I01` | `ProtocolInfoTest` | `test_protocol_pins_23_0_0` | protocol `contract.test.ts`、VM hello test | 対応あり |
| `B6-I02` | `gradle.properties=2300.0.0b6` | package `2300.0.0b6` | VMの`CLIENT_VERSION`とtestが`2200.0.0b5` | **要修正** |
| `B6-I03` | registrarでsign登録、除去10 methodの`method_not_found` test | sign surfaceあり、legacy surfaceなし | VM sign surfaceはあるが`@mc-remote/protocol`のMethod／type／reasonにsignが無い | **要修正** |
| `B6-H01`／`H02` | issue／lookupと旧prefix NOT_FOUND | current handle decode／observer | VM event、spawn result、WireScope adapterでcurrent／legacyを検査 | 局所対応あり。共通negative fixture未接続 |
| `B6-S01`〜`S07` | parse／encode／availability 30件相当と既存live報告 | `test_b6.py`でobject writer、canonical read、null、主要negative | VM sign pure test＋surface4件。TypeScript protocol mirrorと共有JSONが無い | **要修正／共有fixture未作成** |
| `B6-P01`／`P02` | DTO shape、producer置換 | decode、missing item、旧type拒否 | `events-v23.json`をprotocol／VMが消費、旧prefix拒否 | positive shapeは揃う。三repo共通fixtureとしては未接続 |
| `B6-P04` | dedup test、過去のlive-human報告 | wire decodeのみ | event thread／hat投影 | plugin意味論として再利用。fixtureで代替しない |

## 5. source監査で見つかったrelease進行gap

### 5.1 Scratch `@mc-remote/protocol`のsign contract mirror欠落

Scratch VMはsign三操作を直接文字列methodで送受信するが、同repoのprotocol正本mirrorには次が無い。

- `Method.worldGetSign`／`worldSetSign`／`worldUpdateSignLine`
- `LineSpec`／`LineValue`、三methodのparams／result型
- `not_a_sign`／`sign_waxed`／`sign_update_failed`とcode family写像
- signのmachine-readable fixtureとprotocol package test

VM surfaceだけのPASSから「Scratch repo全体がsign wire contractをmirror済み」とは主張できない。

### 5.2 Scratch診断用build labelがb5のまま

VM helloはprotocol `23.0.0`を送る一方、`CLIENT_VERSION`と対応testは`2200.0.0b5`である。
compatibility negotiationはprotocolだけで行うため接続破壊ではないが、b6 artifactの診断identityとして不正確である。
candidate artifact生成前に`2300.0.0b6`へ揃える。

### 5.3 protocol 23 testがprotocol 22 handleを現行resultとしてassertしている

`spawn-v22.json`を歴史fixtureとして残すこと自体は既存判断と整合する。しかし現行
`@mc-remote/protocol/test/contract.test.ts`は、その`mceh_` resultを`SpawnEntityResult`へ代入し、
`/^mceh_/`をassertする。これは歴史fixtureの保存でなく、protocol 23 contract test内で旧handleを
現行resultとして正当化する形である。

`spawn-v22.json`は履歴のまま変更せず、現行handle assertionだけを`mcr_eh_`のprotocol 23 caseへ分ける。
protocol 23 testから旧prefixをpositive assertionしない。

### 5.4 共有fixture未成立

Scratchの`events-v23.json`はprotocol packageとVMで共有されるが、McRemote／Pythonは同じbytesまたは
同じcase IDをまだ消費していない。signにはJSON fixture自体が無い。したがって現在は三repoに類似testがある状態で、
「共有fixture PASS」ではない。

## 6. 最小change coneと次の順序

1. Scratchだけを更新する。`@mc-remote/protocol`へsign contract mirrorとtestを追加し、VMの
   `CLIENT_VERSION`を`2300.0.0b6`へ上げ、protocol 23 testから旧`mceh_` positive assertionを外す。
2. Scratch担当は新しいpush済みSHA、targeted protocol／VM test、build／lint、non-claimを返す。
   browser保存、WireScope filter、mini配置の実装は変更しない。
3. coordinatorは旧Scratch SHAを含む`b6-source-candidate-set-1`をrelease入力としてsupersedeし、
   McRemote／Pythonの同一SHAと新Scratch SHAでsource set 2を固定する。McRemote／Pythonの既存局所PASSは、
   Scratch内のcontract mirror／診断label変更に影響しないため再利用候補とする。
4. 共有fixtureのownerは、人間レビュー（2026-08-27）によりScratch repoの
   `@mc-remote/protocol/test/fixtures/`へ固定した。`pickaxe_poke`／handleのpositive caseは既存
   `events-v23.json`を育て、signは新規`sign-v23.json`へ`B6-S01`〜`S07`のinput／canonical result／
   negative caseを収める。protocol／artifact identityとlegacy method不在はfixtureへ無理に重複させず、
   `contract.test.ts`のsource／registry assertionで扱う。McRemote／Pythonは同じcase内容を読み、
   coordinatorが固定SHAのfixture bytes／digestと各component assertionの対応を照合する。
5. 三repoのfixture対応後にだけTier 2の通常dev横断pulseへ進む。artifact生成、shared環境deploy、
   formal live-human evidence、default branch統合、b6 GREENはまだ主張しない。

この順序を採る理由は、現在見つかった差分がScratch repo内のcontract mirrorとartifact identityに閉じ、
plugin／Pythonのwire実装やsign contractの再設計を必要としないためである。
