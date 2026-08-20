# WireScope

WireScope は、Scratch、Python、将来のほかの client が同じ画面で McRemote の通信を観察するための
read-only observer です。この README は人間向けの入口です。配置、capability、security boundary の正本は
[WireScope deployment 設計](wirescope-deployment-design_ja.md)、共通appのattach／session／artifactは
[station attach設計](wirescope-station-attach-design_ja.md)と決定`2026-08-10-02`／`2026-08-11-02`／
`2026-08-11-03`を参照してください。公式public browser surfaceのhostnameと、将来のbrowser source
handoff familyは決定`2026-08-20-01`／`2026-08-20-02`およびdeployment設計§4.1／§6を正とします。

## WireScope の三役モデル：source／station／browser

WireScope が動くとき、登場する role はいつも三つです。

**source（流す人）** — 観察される frame を生み出して差し出す側。Scratch editor、Python program など。
自分と Minecraft の間の通信を写し取り、秘密情報を落とした generation-side allowlist 済みのコピーを
station へ送ります。

**station（配る人）** — source から観察データを受け取り、閲覧者へ届ける中継役です。あわせて固定identityの
WireScope HTML／JavaScriptを配り、どのobserverがどのtargetを見てよいかを整理します。有限の一時bufferも
station構成のroleに含みますが、どのprocessが所有するか、件数、byte上限はまだ決めていません。

**browser（見る人）** — station から画面を受け取って開き、許可されたstreamを購読して表示するtab／windowです。
observerとしては読むだけで、Minecraft本体の接続やcommand能力を受け取りません。

観察データの流れは一方向です。

```text
source ──（allowlist済みの写し）──> station ──（観察データ）──> browser
```

逆向きにMinecraft操作能力が伝わらないことが重要です。browserからstationへの購読要求やgrant redeem等の
制御通信はあり得ますが、それをsource commandやMinecraft commandへ昇格させません。stationもsourceを
探しに行くpullを標準にせず、source側から観察データを差し出します。これにより「見るだけ」を通信方向だけでなく
capability境界として維持します。

### なぜ「station」という別の名前が要るのか

Scratch版の現在の実装では、Scratch editorがWireScope tabを開いて`MessageChannel`で直接データを渡し、
別originの配信元が共通appを届けます。source handoff、broker、app配信のroleが複数の実体へ融合しているため、
独立したrelay processは見えません。それでもdeployment全体として「画面を配り、targetとobserverを結ぶ」役は
存在します。

Pythonでもbrowserを起動すること自体はできますが、Python runtimeの状態を別processのbrowserへ直接共有は
できません。同一PCならloopbackの小さなstation、教室ならdeployment内のstation、VPSなら公開HTTPS stationが
候補になります。**roleは同じで、誰が演じ、どのprocessへ分かれるかだけがdeploymentごとに変わる**——この
「配役は変わるが台本は不変」の台本側に付けた名前がstationです。

### 配役の早見表

以下はprofile候補を理解するための例であり、transportの確定表ではありません。

| profile例 | source | station roleの配役 | browser |
| --- | --- | --- | --- |
| Scratch個人利用 | Scratch editor | Scratch handoff＋別originの`@mc-remote/live`配信へ融合 | 別originのtab／window |
| Python同一PC | Python program | loopback station候補 | loopback top-level tab |
| 教室deployment | 各学習者のScratch／Python | 教室deployment内のstation候補 | 各学習者のLAN tab |
| VPS公開beta | 各利用者のclient | 公開HTTPS station候補 | 公開HTTPS URLのtab |

「個人」「教室」だけではprofileを決めません。WSL、Docker、SSH、Jupyter等では同じ利用者でもsource、station、
browserのnetwork namespaceが異なります。正しい分類軸は三者のaddress-space関係です。

### 覚え方

一行で言うなら——**sourceは写して流す、stationは配る、browserは読む**。stationは特定PCやserverの名前ではなく、
「配るroleがdeploymentのどこかにある」という役職名です。

## WireScopeの育ち方

現在のread-only WireScopeは暫定版だから読むだけなのではなく、正当な出発点です。長期には
**見る→選んで見る・比べる→つつく→組む**と育てます。ただしbrowserへMinecraft操作権限を足すのではありません。
将来consoleを置く場合も、独立してpairingする新しいsourceを同じ画面へ加え、browser observerは読む役のままにします。
正本は決定`2026-08-10-03`と[deployment設計 §12](wirescope-deployment-design_ja.md#12-長期ビジョン見る道具から創作を支える道具へ)です。

## このスポークの役割

- 共通observer UIとschemaの意味論
- source／station／browserの責務
- deployment profileとaddress-space境界
- attach、publish、operatorのcapability分離
- 有限・非永続な観察経路とfailure semantics
- 将来のWireScopeが三役を壊さず育つための長期ビジョン

実装ownerは分かれます。共通appは`Naohiro2g/scratch-editor`の`@mc-remote/live`、source adapterは各client、
deployment実装は`mc-remote-stack`が所有します。本スポークへ実装や秘密の実値を複製しません。
