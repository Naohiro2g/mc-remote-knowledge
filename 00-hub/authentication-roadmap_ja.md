# 認証ロードマップ

> 認証基盤の現在地、long-lived credential の公開 gate、再開条件と実装順序の横断正本。決定 `2026-08-07-01` を人間向けに投影する。

## 1. 現在地

b3 の横断スコープは完了として閉じる。ここでいう完了は、`10-protocol/versioning-design_ja.md` §10.11.1 項14のcatalog一式、`2026-07-27-01`で改訂されたScratch現行roadmap §2.3、各 component の b3 release gate を閉じ、次の利用者価値へ進むという roadmap 上の区切りである。旧§10.11.1項15は当初計画の履歴であり、残 gate へ戻さない。

credential lifecycle、checkpoint、rollback resistance、reset／災害復旧は §10.11.2 どおり b3 の責務ではない。したがって、それらの未完了を理由に b3 を開いたままにせず、逆に b3 完了を long-lived credential の公開承認とも読まない。

公開面は引き続き次の状態を維持する。

- 既定 credential は `session`。
- Python の既定を `long_lived` へ切り替えない。
- Scratch は session token のみを使う。
- Stack の一般 profile、利用者ガイド、一般利用者向け preset、公開教材へ long-lived 導線を出さない。検証専用の isolated alpha は公開導線と同一視しない。
- `2026-08-02-01`、`2026-08-02-03`、`2026-08-06-02` の設計、実装、既存 evidence は破棄せず、後続 slice の入力として保持する。

## 2. ここからの優先順

1. b3 の横断スコープを閉じる。
2. long-lived credential の公開 gate を閉じたまま、credential-lifecycle slice を後続へ送る。
3. b4 へ送った利用者向け機能を進める。
4. ケータリング実践から、環境の再構築時間、pairing の負荷、現場で実際に止まった箇所と復旧行動を集める。
5. 実利用で長期 credential の需要が確認された後に、credential-lifecycle slice の再開を横断決定する。

long-lived 実装が存在すること、設計が確定していること、開発者にとって便利であることだけでは再開 trigger にしない。session の期限切れ、server 再起動、複数日にまたがる継続利用等により、再 pairing が現場の利用を実質的に妨げることを観測したときに需要として扱う。固定の数値閾値は現段階で捏造せず、sanitized な実践記録を参照して人間が再開を決める。

### 2.1 b4 の復旧境界

b4では利用者が書いたScratch／Pythonの建築コードを既定の保護対象とする（`2026-08-18-01`）。
復旧はコード保存→空環境再構築→再pairing→必要なら現行正準記法へ書き換え→再実行を基準にする。
同一b4 runtimeの通常再起動を跨ぐ期限内session token認証は`2026-08-02-08`どおり実装・実機確認する一方、
b3によるb4 session recordの読込、downgrade中のtoken継続、world／接続／WireScope状態の完全復元は
b4 blockerにしない。

この境界はcredential lifecycleを不要とする判断ではない。long-lived公開、checkpoint＋doctor、snapshot rollback、
reset／災害復旧、world backup／restoreは後続の運用品質sliceとして維持する。b4 exact setでは
same-b4再起動後のtoken再利用とb4再適用後のtoken再利用がPASSし、未実装checkpointをStack doctorが
`doctor_credential_health_unsupported`としてfail closedにした。正式根拠は
`2026-08-18-b4-session-persistence-home-alpha`と
`2026-08-18-b4-code-preservation-recovery-live-human`である。

## 3. ケータリング実践で残す観察

各実践では、可能な範囲で次を残す。

- **再構築時間**：再構築の原因と範囲、開始条件、利用可能と判定した終了条件、所要時間。
- **pairing 負荷**：必要になった pairing／再 pairing の回数、操作の往復、やり直しの原因、複数人・複数端末・複数接続先で負荷が増えた箇所。
- **失敗点**：失敗した段階、公開可能な stable reason／症状、検出方法、復旧行動、復旧までに必要だった人間介入。
- **long-lived 需要の有無**：session のままで支障がなかったか、継続 credential があれば避けられた中断だったか。

token、`pairing_id`、player UUID、private host／route、account、秘密を含む raw log は収集物へ入れない。pair codeは約120秒・一回限りの表示・操作用コードでありcredentialではないため、通常log、transcript、公開evidenceへそのまま収録でき、redactionを要求しない。正式な横断根拠にする場合は `14-evidence/` の visibility と redaction 規律に従う。

## 4. credential-lifecycle 再開後の順序

再開を決めた後は、次の順序で slice を閉じる。

1. **正式 list／revoke／logout API**
   - wire 名 `auth.listCredentials`／`auth.revoke`／`auth.logout` は既に批准済みであり、ここでの「正式」は再命名ではない。
   - plugin、利用者向け client／CLI、error と token 温存規則、所有者境界、conformance、live evidence を一つの公開可能な管理面として閉じる。
2. **checkpoint＋doctor**
   - `2026-08-06-02` の nonce 付き明示 checkpoint と Stack doctor consumer を共通 fixture、deterministic test、実 profile で接続する。
3. **secret-safe live runner**
   - token、`pairing_id`、credential、UUID、private endpoint を公開 artifact や process log へ漏らさず、発行、一覧、失効、logout、再接続を反復検証できる runner を固定する。pair codeと表示用pair commandは通常log／evidenceへ残してよい。
4. **snapshot rollback transaction**
   - revoke 済み credential と非 revoke credential を区別したまま snapshot rollback、再起動、authority 継続、backup 非包含、失敗時 rollback を一つの transaction として検証する。
5. **reset／災害復旧**
   - 明示 reset、途中失敗からの再試行、current authority を回収できない場合の新 domain＋全失効＋再 pairing、復旧後 doctor を閉じる。

前段の完了だけで公開 gate を部分的に開かない。公開可否は全体が `2026-08-02-03` の安全条件を満たした時点で別途判定する。

## 5. 維持する境界

- long-lived を永久に禁止しない。需要が確認されるまで優先度を下げ、公開 gate を閉じる判断である。
- 既存の `CredentialStore`／`RevocationAuthority`、線形化点、fail-close、rollback domain 分離を簡略化しない。
- checkpoint を bootstrap／reset transaction と同一化しない。
- world restore へ credential restore を暗黙追加しない。
- b4 の利用者向け機能を credential-lifecycle 完了で律速しない。

## 6. 却下した進め方

- b3 を credential lifecycle 完了まで開いたままにする。
- 利用需要の観測前に long-lived を既定化または一般公開する。
- long-lived 実装が存在することを、そのまま公開需要の証拠とする。
- list／revoke／logout、doctor、rollback、reset を一つの巨大 slice として同時に完成させる。
- 一部の管理 API や happy-path live test だけで公開 gate を開く。
- 既存設計と evidence を破棄して、需要確認後にゼロから設計し直す。
