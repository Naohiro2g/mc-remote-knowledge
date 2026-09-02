# Release運用と責務分担

この文書は、公開runbook、物理マシン、deployment、横断release gateを、誰がどの正本で
扱うかを説明する。拘束層は`2026-08-21-03`／`2026-08-21-04`／`2026-08-23-01`／`2026-08-28-02`、個々のgateの現在地は
[release gate notes](release-gate-notes_ja.md)を正とする。

## 1. 骨格

McRemoteのrelease運用には、次の役割がある。

| 役割 | 主な正本 | 所有するもの |
| --- | --- | --- |
| component担当 | 各開発repo | 実装、局所fixture、build、candidate artifact |
| deployment担当 | `mc-remote-stack` | 公開runbook、profile、preset、order、lock、deploy、doctor |
| private operations担当 | `mc-remote-backstage` | 物理host、実環境inventory、privateな運営状態、secret参照 |
| gate coordinator | `mc-remote-knowledge`のgate状態 | 横断scope、依存順、exact set、統一試験票、横断判定 |
| human release owner | 人間の批准 | 公開release、tag、外部deploy等の最終承認 |

一人の担当が複数roleを兼ねてもよい。兼任しても、正本、証拠、判定権限は混ぜない。

## 2. 公開runbookは作業日誌ではない

公開deployment packageと運用runbookのSSOTは`mc-remote-stack`である。runbook専用repoを
新設せず、旧`server-runbook`をlive SSOTへ戻さない。

Stackのrunbookは、実際の作業者が会話履歴なしで利用する、対応済み操作への最短の正準経路である。
対象操作の前提、実行入口、成功条件、失敗時の戻り先を示す。CLIやvalidationへ固定できる処理を、長い
手作業として複製しない。

次をrunbook本文へ蓄積しない。

- 一回の実施日誌や試行錯誤の時系列
- 特定host、private address、SSH alias、provider account等の実値
- movingなcandidate commitやartifact hashの転記
- secretの実値
- そのgateだけのPASS／FAIL transcript

exact artifactと非秘密のdesired stateはorder／lock、公開可能な高再現コストの結果は`14-evidence/`、
private inventoryとprivate evidenceはbackstage、秘密実値を含むrawはGit外へ置く。

同じ失敗が繰り返された場合は注意書きを積むだけで終えず、preflight、doctor、CLI、validation、runbookの
どこで作業者の判断や手戻りを減らせるかを直す。未実装のupdate、rollback、restore等を対応済みと説明せず、
そのrelease gateでどこまでを必須にするかはgate定義へ戻す。

## 3. マシンとdeploymentを分ける

物理host、deployment、environment、profile、exact componentは別のidentityである。

| 対象 | 例 | 所有者 |
| --- | --- | --- |
| 物理host／SSH alias | `m720s2` | backstage |
| deployment／environment identity | `dev-integration` | Stackのorder／lock。実host写像はbackstage |
| topology／policy | 通常dev、home server等のprofile | Stack |
| exact component | source commit、JAR、wheel、browser artifact | preset／order／lockとgate exact set |
| 構築方式 | ケータリング型等 | profileやhostとは独立した方式 |

物理host名からchannel、exposure、purpose、profileを推測しない。clientをdeployment host上で動かすか、
別workstationから接続するかもtest topologyが決める。GUI、browser、Minecraft clientをserver hostへ
常に導入する一般則は持たない。

backstage管理下でshared／dev-integration用途に使う物理hostは、LAN内mDNS（avahi）でhostname解決できることを
標準とする。新規hostを追加した時、またはgate coordinatorが接続先解決failureを発見した時、backstageの
server-environment-inventoryへ解決可否・確認方法・確認日を記録する。実際のavahi-daemon設定・確認作業は
backstageの実行境界であり、knowledge側のcoordinatorはこの標準を定め、inventoryを読んで指示票へ接続先を
含める（§4）役割にとどまる（`2026-09-03-04`）。

一つのStack担当がStackとbackstageを一続きで扱える。ただし両repoのcommit／PRを分け、backstageの
実値をStackへ複製しない。管理者権限や対話認証が必要な操作は人間の実行境界として明示する。

backstageの管理下へ置いた物理hostでは、稼働service、listen port、所有者、用途、期待状態をprivate
inventoryで把握する。所有者または用途を説明できないservice／listenerは通常状態として受容せず、変更や
candidate deployの前に停止または正当なmanaged stateへ写像する。完全なprivate実値を公開Stackへ複製する
ことは要求せず、公開側にはpreflight可能なdesired stateと不整合の有無だけを投影する。

## 4. 横断release gateは一人が進行する

各横断release gateには、人間が一人のgate coordinatorを指定する。指定が無い場合の既定は、当該gateを
扱うknowledge担当sessionである。同時に複数のcoordinatorを置かない。交代時は現在phase、exact set、
完了証拠、未解決、許可済みの次操作を明示して引き継ぐ。

gate coordinatorは次を所有する。

- gate scopeと参照するknowledge commit
- contract maturity、必要なtest tier、change cone
- component間の依存順と着手依頼
- exact compatibility setの凍結と失効
- 既存PASSの再利用判定とnon-claim
- shared環境へのcandidate deploy許可
- 一つのlive-auto／live-human実施票
- evidenceの収集範囲とnon-claim
- 横断`GREEN`／`HOLD`／`RED`の判定
- release後identity確認とmilestone close

coordinatorはcomponent実装、物理hostの実状態、実施していないtestを推測しない。進行責任は、すべてを
自分で実行する責任ではない。

## 5. 担当別の実行境界

### Component担当

自repoの実装、決定論的test、push済みsource、immutable artifact、事実と差分を返す。割り当てられた
範囲の局所作業は独立に進められる。

他repoへの着手命令、shared環境へのdeploy、人間参加試験の開始、exact setの選択、横断GREEN判定は
行わない。componentのPASSだけから横断PASSを主張しない。

### Stack／backstage担当

Stackはhost preflight、profile／order／lock、artifact取得、render／apply／doctor、再適用とdeployment
evidenceを担当する。backstageは物理hostとprivate inventoryの写像を担当する。

Stackはoperatorが調整する設定をhost側の編集可能な宣言的入力として管理し、review可能なrender／applyでcontainerへ
投影する。container内でpluginが生成したconfigを、変更不能なdefaultを固定する不透明なdurable stateとして扱わない。
immutable artifact、operator desired config、world／credential等のruntime dataはowner、更新、backup、rollbackの
lifecycleを分ける（`2026-08-30-02`）。

一般的なhost準備はexact set凍結前にも進められる。candidate artifactの配置とshared環境でのgate試験は、
coordinatorがexact setと許可済み操作を示した後に行う。Stack担当はcomponent候補やproduct contractを
独自に変更しない。

### 人間参加者

Minecraft、Scratch、browser等で人間操作が必要な箇所だけを統一実施票に沿って行い、観測事実を返す。
試験中にscope、candidate、順序を独自変更せず、単独で横断GREENを宣言しない。

### Knowledge担当とhuman release owner

knowledge担当はcontract照合、sanitized evidenceの正式authoring、横断判定を行う。human release ownerは
公開tag、release、registry publish、public deploy等の外部状態を変える最終操作を批准する。

## 6. 仕様成熟度とtest tier

test classの`unit/deterministic`／`live-auto`／`live-human`は実行方式と証跡コストの分類である。
test tierは、開発の成熟度とその時点で必要な主張の強さを表す。両者を混同しない。

| Tier | 適用局面 | 既定の検証 | まだ要求しないもの |
| --- | --- | --- | --- |
| 0 | 探索・実装中 | 変更箇所のtargeted static／unit、fixture生成 | 全repo回帰、artifact固定、formal evidence |
| 1 | component contract候補 | 影響内の決定論的test、build、source／artifact再現性 | shared環境deploy、live-human |
| 2 | 横断contract形成中 | 共有fixtureと常設dev harnessの軽量横断pulse | exact set凍結、全受入試験 |
| 3 | release candidate | exact set固定後のchange cone内検証、必要な短いlive-auto／human | 影響外の無条件再試験、全capacity／soak |
| 4 | RC／正式release受入 | 人間でしか確認できないUI、capacity、soak、rollback、全体主張 | なし。ただしnon-claimは明示する |

Tier 2の軽量横断pulseは、少なくともauthenticated hello、変更sliceの代表的な成功、
代表的なerror、必要な場合のevent、observer／WireScope decodeを一往復させる。目的はGREENを出す
ことでなく、surface間のsemantic drift、runner gap、環境前提の誤認を安く発見することである。

仕様形成中はTier 0〜2を反復する。合意済みcontractと共有fixtureが収束した後にのみ
Tier 3へ入る。beta番号やartifact versionが存在することだけでTier 3と見なさない。

## 7. Change coneとPASSの再利用

candidateのsource／artifact identityが変わったらexact setは失効する。ただし、これは過去の観測事実を
すべて無効にする意味ではない。coordinatorは変更からrelease主張へ至るchange coneを作り、
影響するcontract、component、artifact、environment、test assertionを列挙する。

再利用の最小条件は次のとおり。

- 元のtestの主張とnon-claimが特定できる。
- 実行したsource／artifact／fixture／environment identityが特定できる。
- 今回の変更がその主張へ影響しない理由を言語化できる。
- security、protocol、永続化、並行性等の横断依存を「同じファイルを触っていない」だけで非影響にしない。

代表的な戻り方は次のとおり。

| 変更 | 原則として再実施する範囲 |
| --- | --- |
| wire shape／version | plugin codec、影響client adapter、validator、共有fixture、代表live |
| pluginの局所不具合 | plugin決定論的testと当該methodの短いlive。非影響UIは再利用可 |
| client UI／表示 | 当該clientと、observer shapeへ影響する場合のWireScope |
| packaging／archive metadata | 再現性、digest、license／RECORD。gameplay liveは原則再利用 |
| harness／runbook／hostのみ | start／ready／stopと代表pulse。product全回帰は原則再利用 |

## 8. 通常dev integration harness

通常dev integration harnessはpublic deploymentの縮小版ではなく、人間とagentが同じserver consoleと
candidateを扱う暖機である。必要時に起動し、終了後は次のtestで再利用できる。次を正準操作にする。

- reviewed artifactの配置とdigest照合
- `start`／`status`／`attach`／`stop`に相当する一義的な入口
- Paper起動、plugin起動、credential health、listenerの個別readiness
- 二重起動、port競合、別runtimeへの誤配置の防止
- 人間がconsoleを直接確認し、detach／reattachできること

container、system service、特定process supervisorを一律の既定にしない。現在の通常devが`run.sh`と
名前付きScreenを使う事実はbackstageのhost写像とStack runbookで扱い、論理contractを特定hostのpathや
Screenへ固定しない。毎gateの再構築、OS service化、container化は別の要求がある場合だけ行う。

## 9. Gate manifestと手作業の排除

横断gateの動く状態は、少なくとも次を持つmachine-readable gate manifestへ投影する。

- gate ID、coordinator、knowledge commit、contract maturity
- component source／artifact／fixture identityと取得元
- exact setのfreeze状態
- change cone、必要test tier、実行済み・再利用・未実施assertion
- target harness／environment lease、authorized next action、停止条件
- evidenceとnon-claim、release／close状態

正本はDECISIONS、説明文書、component source、Stack lock、evidenceに残し、manifestはそれらを一回の
gateに束ねる機械的投影とする。exact schemaと生成ツールはStack／knowledgeの後続実装で固定するが、
b6の最初のTier 2横断前までに使える形へする。knowledge SHA、tag target、remote commitは自由文から転記せず、
Git／provider APIから取得して存在と一致を検証する。

## 10. 正準進行

1. 仕様形成：Tier 0〜2でcontract、共有fixture、代表pulseを収束させる。
2. gate定義：scope、contract commit、maturity、change cone、必要tier、target topology、non-claimを固定する。
3. component準備：各repoがpush済みcommit、artifact identity、影響内test、残差分を返す。
4. exact set凍結：coordinatorが一組のsource／artifact／schema／policyを固定する。
5. 環境準備：常設harnessを既定とし、必要な場合だけStackが許可されたsetをdeploy／doctorする。
6. 統一実施票：coordinatorが再利用PASS、実行するassertion、順序、担当、停止条件を一票で示す。
7. 実機検証：Tier 3はchange cone内の短いlive-autoを先に行い、人間でしか判定できない箇所だけlive-humanを行う。
8. evidence着地：各担当の素材をknowledgeがformal record／artifactへ収容する。
9. 横断判定：coordinatorが`GREEN`／`HOLD`／`RED`と未主張範囲を記録する。
10. release：human release ownerの批准後、各repo担当またはgate coordinatorが指定identityを公開する。複数repoを一括公開する場合も、tag target、asset、公開範囲を一つの承認対象として先に示す。
11. close：公開identity、default branch統合／保持先、handoff全件の着地を再確認し、gateを閉じる。

candidate commit、artifact bytes、schema、policyのいずれかが変わった場合、旧exact setを失効させる。change coneの
影響段階まで戻って再凍結・必要な場合だけ再deployする。shared環境へ未push worktreeや一時buildを差し込まない。

試験が失敗した場合は観測を保持してcoordinatorへ戻す。その場のad hoc patchで同じ試験を続けず、component
側で修正、決定論的test、push、artifact再固定を行う。統一実施票に無い追加試験を正式gate根拠へ使う場合は、
coordinatorがscopeと主張を更新する。

## 11. Release gate notesの役割

`release-gate-notes_ja.md`は、版ごとの動く進行状態を集約する。各gateは少なくとも次を持つ。

- gate coordinator
- human release owner
- current phase
- contract maturity／required test tier／change cone
- exact compatibility setとfreeze状態
- 再利用するPASSとnon-claim
- target deployment／profile／lock
- gate manifest identity
- authorized next action

設計判断はDECISIONS、実機結果はevidence、実マシン情報はbackstageへ置き、このファイルへ複製しない。

## 12. Release close

releaseの公開だけでcloseとしない。各componentについて次を確認する。

- release／tag targetが意図したsourceとartifactへ固定された。
- release sourceをdefault branchへ統合した、または統合しない理由と保持branch／tagを明示した。
- `handoff-materials/`を「正式evidenceへ昇格」「後続slice／担当へ引継ぎ」「失効・破棄」のいずれかへ全件分類した。
- 引継ぎは引継ぎ先、参照identity、次の一手が特定できる。破棄は他の正本／evidenceから非参照であることを確認してから行う。
- gate manifest、release gate notes、NOTESの現在地が次のmilestoneと矛盾しない。

## 13. 既存決定との関係

- `2026-07-01-04`／`2026-07-01-05`：release gate notesへの集約とknowledge側最終判定を維持し、単一進行責任とphase制御を追加する。
- `2026-07-06-03`／`2026-07-21-04`：evidenceのtest classとvisibility境界を維持する。
- `2026-07-21-03`：Stack／backstage境界を維持し、runbookの目的とmachine写像を精密化する。
- `2026-07-23-01`：deployment／profile／environment／order／lockの分離を維持する。
- `2026-07-19-05`：主張を証拠のスコープから越境させない。
- `2026-08-23-01`：単一coordinatorと責務分離を維持し、test tier、change cone、常設dev harness、gate manifest、release closeを追加する。

## 14. 短期betaの軽量release mode

b7〜b9のように短期間で反復できるbetaは、初回stableの完成版を一度で証明する工程でなく、実装を利用可能な
公開identityへ早く載せ、実使用の問題を次の判断へ返す観察単位として扱う。既知の問題を隠して出す意味ではない。

軽量betaの既定確認は次で足りる。

- 変更componentのtargeted test／build
- wire変更時の共有fixtureまたは同等のcomponent間shape照合
- 既存host-native通常dev harnessでの変更slice代表往復
- Minecraft／browser／UXなど人間でしか判定できない箇所だけの短いlive-human
- default branch／tag／artifact／release notes identityの公開前後照合

影響外の全回帰、capacity／soak、ケータリング型再構築、Docker化、public deployment、全surfaceで同一試験を
繰り返すことは自動要求しない。security、credential、永続データ破損、権限、破壊的wire変更など、失敗時の影響が
beta利用者の観察で回収できない変更は軽量modeだけで閉じず、change coneに応じて検証を強める。

公開後に問題が見つかった場合、公開済みtagを差し替えない。観測を保持し、影響範囲まで遡って修正し、通常は次の
betaへroll forwardする。緊急性が高ければrelease説明、撤回、hotfixを個別判断する。

knowledge担当がreleaseまでの進行、各開発repoへの指示、exact set固定、最終公開操作を一続きで扱ってよい。
component担当は実装と局所判断へ集中し、human release ownerは必要なUX確認と公開承認を行う。担当agentのmodel／
providerはroleの固定条件にせず、今回のようにknowledgeをCodex、開発repoを軽量なClaude modelとする分担も選べる。

repo間搬送は当面、会話で人間が内容を見ながら票を渡す。固定fileと自動収集への移行は、手作業の反復箇所と
見落とし防止効果が十分観測できた後に判断する。machine-readable manifestや固定搬送fileの未実装だけでbetaを
HOLDにしない。
