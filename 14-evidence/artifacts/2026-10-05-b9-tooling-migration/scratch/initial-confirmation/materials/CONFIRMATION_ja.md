## Release gate 確認票

- 対象 repo: `Naohiro2g/scratch-editor`
- 対象 branch/commit: default branch `develop@00c01460e2f994c4ed5f097070cae41867c320a9`。保持branch `agent/b8-compatibility@1ecd531221ed88523594284a5bc963bad97a2f83`にはb9用のWireScope列幅commit `01cdb0bfee`がある
- release / channel: b9予定、protocol `23.2.0`、artifact `2320.0.0b9`。現在の実装のclient identityは公開b8のまま。b9 candidate未作成
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: 確認票の返却。移管の現ownerとして調査と比較を行った
- contract maturity / required test tier: 批准済み契約2件（`2026-10-03-01`／`2026-10-03-02`）への適合箇所と移管材料を調査。依頼のTier 2。今回の実行は決定論的な監査probeと静的照合であり、移管後consumer test／Tier 3はまだ行っていない
- knowledge contract path: `00-hub/b9-gate-confirmation-instructions_ja.md`、`00-hub/release-gate-notes_ja.md`（2026-10-04）、`00-hub/DECISIONS_ja.md`（契約2件）、`10-protocol/protocol-tooling-migration-plan_ja.md`、`10-protocol/protocol-tooling-migration-human-guide_ja.md`、`00-hub/NOTES_ja.md`（該当park行）、b8 closeの`FIXTURES_ja.md`
- knowledge contract commit: `ceba53099fa001fea6b83d68deadc1eb9e0038fe`（実際に読んだremote main）。指定された`71814e4`→`06b069`の差分はJava向け質問とINDEXの追記だけで、Scratch節は不変。`06b069`とこのSHAの確認票依頼は同一blob `55c9b9dcf43f42ba9789f8c687741cf036eb9ad9`
- gate manifest identity: b9について未提示
- change cone: 調査のみ。将来の変更候補は未知eventへの対応、WireScopeの`chat.post` result検証、protocol mirror、追加fixture、toolingのowner／取得経路／CI／release収集、列幅、picker alias。詳細は同梱`ASSESSMENT_ja.md`
- reused PASS / rationale: 公開b8のfixture12件を現在の作業ツリーと正式一覧へ再照合し、全件byte一致・bytes／SHA-256一致。b7是正3件は公開b8の祖先にある修正と既存test・正式記録を参照。今回b8の全suite／liveを再実行したとは主張しない
- exact compatibility set / freeze status: b8の`b8-integrated-artifact-set-1`が基準。b9 exact set未凍結
- target deployment / profile / lock: 本票には接続先・新しいlockの提示なし。deployment操作なし
- authorized next action: 自repoの現状調査と確認票返却。topologyと実行範囲のhuman owner判断前の移管操作はしない
- test class: `unit/deterministic`（監査probe・fixtureのbyte／digest照合）
- 実行した command / 手順:
  - GitHub APIで提示SHAの実在・親子関係、依頼の差分、現在のmainを確認し、必要なSSOTを固定SHAから読んだ
  - `node handoff-materials/2026-10-04-b9-scratch-confirmation/materials/audit-contracts.cjs`
  - `python3 handoff-materials/2026-10-04-b9-scratch-confirmation/materials/audit-fixtures.py`
  - source／package metadata／fixture読込／CI／release workflow／artifact generatorを静的調査
- 結果:
  - `chat.post`: Scratchの命令は応答resultを捨てるため`null`で壊れない。WireScopeは`null`を受けるが、`true`等も受ける。protocol mirrorに`ChatPostResult = null`はまだなく、WireScopeの専用null検証も未実装
  - 未知event: Scratch VMは`invalid_event_response`でpoll応答を拒否し、pollerを止める。WireScopeは未知typeのframeを含むsnapshotを拒否する。compatible minor `23.3.0`の既知eventは受けるが、未知eventで拒否することを再現した。契約`2026-10-03-02`への対応が必要
  - shared fixture: 契約2件のcaseは追加可能。公開b8の12件はbyte一致の起点として維持し、追加fixtureで既知／未知混在・未知だけ・cursor／loss保持・`chat.post` nullを扱う案。現時点で追加・発行していない
  - WireScope列幅: `01cdb0b`はhuman ownerの確認済みでb9へ送った変更。そのままb9へ含める材料がある。現在developには入っていない
  - 移管: 共通TypeScript tooling monorepo＋Bridgeの現在のtransport機能維持＋fixtureはGit SHA pin／browser appは生成ZIP取得を推奨。最終決定ではない。候補ごとの範囲・工数・既存park repoの扱いは別紙
  - b7是正3件は全てb8に入った。picker aliasは未実装。名前辞書の置き場所・exact schema・二段表示は実装済み、読み上げの人間確認は未実施
- evidence record / artifact: 正式起点はknowledge `14-evidence/artifacts/2026-10-03-b8-dev-live/scratch/2026-10-03-b8-close-inventory/FIXTURES_ja.md`。今回のdev材料は`handoff-materials/2026-10-04-b9-scratch-confirmation/`（本票・別紙・再現script・監査結果・fixture baseline metadata・SHA-256一覧）。正式evidenceへの配置はknowledge側
- 未検証の境界: 新ownerのstandalone install／build／CI、移管後consumer、artifact再現、McRemote／Pythonの現checkout、new candidate、shared接続、real-browser／live-human、読み上げ。製品sourceの変更、fixture発行、repository作成・移動、取得先変更、tag／release公開は今回行っていない
- security / compatibility / rollback の確認: runtimeの直接package importはなく、主な結合はfixture testとbuild／release収集。Origin／target allowlist・TLS終端・one-shot transportは現行境界を維持する案。rollbackは公開b8 source `691576f60b7f0824e1753bd6823901d01fbe2422`とそのlock／fixture／既存Release setを使う。具体的な適用はcoordinator／Stack側。新ownerのcommit・lock・source URLを変えるdetached manifestはdigestが変わるため、artifact一致の判定対象を明確にしたい
- 判定を求める事項:
  1. topology、移す範囲、既存park repoを使うか新repoを作るか、Git SHA pin／生成artifactの取得方法
  2. artifact一致を、fixture全12件と変更していない配布物のbyte一致に置き、出どころが変わるmanifest／OCI metadataのdigest変更を区別してよいか。b9の契約対応・列幅変更と移管だけの差分を分けて照合する案
  3. 10/6までに上記を決められるなら、共通monorepo案はScratch／新owner側で概算2〜4作業日、他consumer切替・exact set・liveは各担当とcoordinatorの材料を待つ。10/10は条件付きの見込みで、確約しない。詳細なrepo分割やBridge置換は同日程に含めない案

これは現状と推奨材料の返却であり、component／横断gateの最終判定ではない。
