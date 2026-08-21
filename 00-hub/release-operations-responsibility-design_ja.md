# Release運用と責務分担

この文書は、公開runbook、物理マシン、deployment、横断release gateを、誰がどの正本で
扱うかを説明する。拘束層は`2026-08-21-03`／`2026-08-21-04`、個々のgateの現在地は
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
- component間の依存順と着手依頼
- exact compatibility setの凍結と失効
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

一般的なhost準備はexact set凍結前にも進められる。candidate artifactの配置とshared環境でのgate試験は、
coordinatorがexact setと許可済み操作を示した後に行う。Stack担当はcomponent候補やproduct contractを
独自に変更しない。

### 人間参加者

Minecraft、Scratch、browser等で人間操作が必要な箇所だけを統一実施票に沿って行い、観測事実を返す。
試験中にscope、candidate、順序を独自変更せず、単独で横断GREENを宣言しない。

### Knowledge担当とhuman release owner

knowledge担当はcontract照合、sanitized evidenceの正式authoring、横断判定を行う。human release ownerは
公開tag、release、registry publish、public deploy等の外部状態を変える最終操作を批准する。

## 6. 正準進行

1. gate定義：scope、contract commit、必要なcomponent、evidence、target topology、non-claimを固定する。
2. component準備：各repoがpush済みcommit、artifact identity、決定論的test、残差分を返す。
3. exact set凍結：coordinatorが一組のsource／artifact／schema／policyを固定する。
4. 環境準備：Stack担当が許可されたsetをorder／lockへ投影し、apply／doctor結果を返す。
5. 統一実施票：coordinatorが順序、担当、停止条件、redaction境界を一票で示す。
6. 実機検証：live-autoを先に行い、必要な箇所だけlive-humanを行う。
7. evidence着地：各担当の素材をknowledgeがformal record／artifactへ収容する。
8. 横断判定：coordinatorが`GREEN`／`HOLD`／`RED`と未主張範囲を記録する。
9. release：human release ownerの批准後、各repo担当が指定identityを公開する。
10. close：公開identityを再確認し、release gate notesと必要なDECISIONSを閉じる。

candidate commit、artifact bytes、schema、policyのいずれかが変わった場合、旧exact setを失効させる。影響する
段階まで戻って再凍結・再deployする。shared環境へ未push worktreeや一時buildを差し込まない。

試験が失敗した場合は観測を保持してcoordinatorへ戻す。その場のad hoc patchで同じ試験を続けず、component
側で修正、決定論的test、push、artifact再固定を行う。統一実施票に無い追加試験を正式gate根拠へ使う場合は、
coordinatorがscopeと主張を更新する。

## 7. Release gate notesの役割

`release-gate-notes_ja.md`は、版ごとの動く進行状態を集約する。各gateは少なくとも次を持つ。

- gate coordinator
- human release owner
- current phase
- exact compatibility setとfreeze状態
- target deployment／profile／lock
- authorized next action

設計判断はDECISIONS、実機結果はevidence、実マシン情報はbackstageへ置き、このファイルへ複製しない。

## 8. 既存決定との関係

- `2026-07-01-04`／`2026-07-01-05`：release gate notesへの集約とknowledge側最終判定を維持し、単一進行責任とphase制御を追加する。
- `2026-07-06-03`／`2026-07-21-04`：evidenceのtest classとvisibility境界を維持する。
- `2026-07-21-03`：Stack／backstage境界を維持し、runbookの目的とmachine写像を精密化する。
- `2026-07-23-01`：deployment／profile／environment／order／lockの分離を維持する。
- `2026-07-19-05`：主張を証拠のスコープから越境させない。
