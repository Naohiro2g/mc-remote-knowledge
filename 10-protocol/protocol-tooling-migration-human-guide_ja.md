# Protocol／WireScope／Bridge移管計画 — 人間向け固定文

> 状態: 2026-09-01人間批准済み。`2026-09-01-03`のpark判断を、人間が再開時に読み返す固定文。
>
> この文書は、2026-09-01時点で人間が何を問題と見て、どの案を有力と感じ、何をまだ決めていないかを残すverbatim版で
> ある。将来のagentは、現時点の評価を一般的な移管手順や検証checklistへ置き換えない。

## 今、決まっていること

公開repository `Naohiro2g/minecraft-remote-protocol`は既に作成されている。しかし、Protocol ownerの移管は行わない。
このrepositoryは将来案を検討するためのpark済みbootstrapであり、現行ownerでもb7の入力でもない。

b7のshared fixture ownerはscratch-editor内の`@mc-remote/protocol`を維持する。permission successor fixtureもScratchから
発行し、McRemote、Python、Java、Scratchの参照先をpark済みrepositoryへ切り替えない。Protocol移管の検討をb7 releaseの
完了条件へ追加しない。

## なぜ今は進めないか

b6 releaseが早めに完了したため、多言語展開の下地を作ることができた。Protocol共通基盤をScratchから独立させる種も、
その過程ですでに仕込まれていた。

b7も実装とlive確認が進み、近いうちにreleaseできる見込みである。だからこそ、Protocol、WireScope、Bridge、TCP接続を含む
大きなownership／topology変更をb7実装中へ差し込まない。b7を先に閉じ、その後にb8前へ入れるかb8後へ送るかを判断する。

公開bootstrapが既に存在することや、そこへ工数を使ったことは、今すぐ移管を完了させる理由にしない。

## 現在の配置についての評価

`@mc-remote/protocol`、Bridge、WireScopeがscratch-editor内で一緒に育ったこと自体には価値があった。Protocol変更、fixture、
browser接続、observer、artifactを同じmonorepoで横断して作り、検証できた。

一方、現在はPythonもWireScopeを利用し、Java、一般TypeScript、C#等の多言語展開を予定している。共通Protocol projection、
shared fixture、WireScope common app、場合によってはBridgeまでScratch product repositoryが所有し続ける形は不自然になった。

問題は「同居していること」そのものではなく、共通基盤がScratch製品のbranch、release、担当境界の内側に置かれていることで
ある。Scratch monorepoで得た一体開発の価値まで捨てる必要はない。

## 現時点の有力案

### 共通TypeScript tooling monorepo

Protocol、conformance、WireScope、必要ならBridgeを、Scratchから独立した中立repositoryへ一体で移す案である。

直観的には、この案が最も筋が良い。Protocol projectionを独立させながら、Scratch monorepoで得た共通基盤としての一体性、
同一branchでの横断変更、共通fixture／artifactの検証を維持できる。少なくとも、共通基盤の全てをScratchへ同居させ続ける
現状よりかなり良い。

同じrepositoryへ置いても、package境界と依存方向は分けられる。`@mc-remote/protocol`はdependency-free leafを維持し、
WireScopeやBridgeはそのconsumerとして置ける。repositoryが同じことと、versionやreleaseを一体化することは同義ではない。

公開済みの`minecraft-remote-protocol`をそのmonorepoとして育てるか、名前またはrepository構成を変えるかは未決である。

### ProtocolとWireScopeを分離する案

Protocol projection／fixtureとWireScope common appを別repositoryへ置く案も残す。WireScopeは独自のobserver schema、session、
browser app、artifact、security境界を持つため、将来的に専用repoへ分離する合理性はある。

ただし、分離を最初から正解とはしない。ProtocolとWireScopeを共通基盤として一体管理する価値も高い。最終的に分離するか、
monorepo内の独立packageとして維持するかは、移管再開時に改めて比較する。

### Hybrid

完全移行までScratch側にcopyやworkspace packageを一時的に残す案である。移行順序、build、distribution上必要なら候補になる。
ただし恒久的な二重ownerにはせず、外部ownerからの一方向consumerであることを明確にする。

## 移管する場合の基本方向

移管するなら、Scratchを共通基盤のownerからconsumerへ変える完全移行が自然な目標である。

ScratchにはScratch Client、Scratch VM／GUI、Scratch固有のframe生成、handoff、起動UI等を残す。Protocol projection、shared
fixture、WireScope common app等の共通部分は中立ownerから消費する。実際のbuildやdistributionの都合でhybrid期間が必要かは、
移管時点で調べて判断する。

これはProtocolだけを先に移して完了とする話ではない。WireScopeの位置を同時に評価し、Bridgeについても維持、一般化、置換、
廃止を候補にする。Bridge評価では、Python／Java等のdirect TCP、Scratch／browserのWebSocket経路、将来のbrowser Clientを
どう接続するかを一緒に見る。

現時点では、Bridgeを残すことも廃止することも、TCPを維持することも変更することも決めていない。

## まだ決めていないこと

- monorepoを最終形とするか、WireScopeを専用repoへ分離するか
- 公開bootstrap `minecraft-remote-protocol`をそのまま使うか、役割または名前を見直すか
- Bridgeをどこへ置き、維持／一般化／置換／廃止のどれを選ぶか
- direct TCPとbrowser接続の将来形
- package／fixture／WireScope artifactの取得・配布方法
- hybrid期間の要否
- b8前に実施するかb8後へ送るか

これらは曖昧なままagentへ委ねる項目ではなく、再開時に実装と利用状況を調べ、人間が比較して決める項目である。

## 再開時の扱い

「b7 release後」は、自動的な移管開始条件ではない。b7 release後に、まずこの文書へ戻り、候補と現時点の評価が今も妥当かを
確認する。

その時点で、実際の依存、通信経路、security、移動範囲、工数、rollbackを調べ、各候補を具体化する。coordinatorは調査結果、
候補、推奨案、利点と失うもの、予定する外部操作、knowledgeへ追加する決定文を先に提示する。

人間がtopology、実施時期、最初の作業範囲を判断した後に、指示書、repository操作、source移動へ進む。
