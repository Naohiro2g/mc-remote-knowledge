# 設計記録: マルチプラットフォーム対応（Gradle / Architectury / ターゲット選定）

> マイクラリモコン設計記録
> 関連: モノリポ構想、Paper / NeoForge / Forge / Fabric 対応
> 結節点: [versioning-design] の protocol 概念が各プラットフォームの対応版を一意に決める。

---

## 1. コンセプト: mod サーバーへの「同居」

vanilla（Paper）の「最新を追う」世界とは別に、**mod の世界には「踊り場」的バージョンが存在し、各々が独立したエコシステム（コミュニティ）として並行存在する**。

```text
1.18.1, 1.19.1, 1.20.1, 1.21.1 …
  - Forge/Fabric/NeoForge のメジャー対応が安定する節目
  - 主要 mod が揃い、modpack が組まれる
  - コミュニティが「固定」し、数年単位で生き続ける
```

マイクラリモコンを、これらの踊り場の mod サーバーに**同居できる形**で提供する。とくに Mekanism + Create との同居を想定。

### 教育的・実用的メリット

- protocol が同じなら、Python / Scratch 側のコードは MC バージョンや踊り場を**横断して再利用可能**。
- 学習者（8〜80歳）は MC バージョンを意識せず、「protocol 対応のリモコン API」を1つ覚えれば全踊り場で同じコードが動く。
- 教材・サンプルコード（`mc_remote_samples`）がバージョン横断で活きる。

---

## 2. モノリポ構想

プラグイン（Paper）と mod は別系統だが、**モノリポを目指す**。コア（のコア）は共通。

### 強みの前提: 「ゆるい依存」

> プラグインと Minecraft の依存は極めてゆるく、1.18.1 から 26.2 まで、現状ほぼ無修正で通っているはず。

マイクラリモコンが触る MC API は極めて狭い:

```text
- ブロック set/get（座標 → 種類）
- エンティティ操作（spawn, 座標, 種類）
- プレイヤー情報（位置, 権限）
- ワールドアクセス（複数 world 対応）
- TCP/wss リスナーのライフサイクル（25575）
- 権限チェック（PermissionProvider）
```

接触面が狭いからこそ、バージョン差・ローダー差を吸収するアダプタが薄く済む。一般の大型 mod では不可能だが、マイクラリモコンの設計だから成立する。

### モノリポ構造（案）

```text
mc-remote/  (monorepo root)
├─ core/                  ← protocol 実装・コマンド処理・状態管理（MC/ローダー非依存）
├─ platform-paper/        ← Paper/Bukkit アダプタ → mc-remote-1.21.11-221.x.x.jar
├─ platform-neoforge/     ← NeoForge アダプタ
│   └─ 1.21.1/
├─ platform-forge/        ← Forge アダプタ（1.20.1 まで）
│   └─ 1.20.1/
├─ platform-fabric/       ← Fabric アダプタ
│   ├─ 1.20.1/  1.21.1/  1.21.11/
└─ protocol/              ← protocol 仕様 SSOT → 各言語 constants/docs 生成
```

### 二軸の差分吸収

- **横（ローダー差）= Architectury** が吸収（Fabric/Forge/NeoForge）。
- **縦（MC バージョン差）= 自前の薄い mc-adapter** が吸収。Architectury 自体にはバージョン跨ぎ機構はない。
- Paper（Bukkit）は Architectury の枠外なので、**ビルド系統が2つ**モノリポに同居する（通常 Gradle + paper-api / Architectury 構成）。Gradle マルチプロジェクトで束ねる。

### core と platform の境界

各プラットフォームが提供すべき抽象（アダプタ・インターフェース）を上記「ゆるい依存」の6項目に保てば、モノリポはクリーンに保てる。

---

## 3. Architectury の役割（差分吸収の仕組み）

> 詳細な技術解析は別セッションに切り出し。ここでは設計判断に必要な要点のみ。

- **Loom**: 難読化（obf）↔ 可読マッピングの remap を自動化する Gradle プラグイン。Architectury Loom はそれを Forge/NeoForge に拡張したフォーク。
- **Architectury API**（実行時の共通 API）: レジストリ登録・ネットワークパケット・イベントなど、ローダーごとに書き方が違う部分を統一 API で包む。
- **@ExpectPlatform**（コンパイル時の差分注入）: common で宣言、各ローダーで実装。ビルド時に差し替え。
- 理想構成: common に 80〜90%、各ローダーは薄いアダプタ。

注意: Architectury は**ローダー差（横）**を吸収するが、**MC バージョン差（縦）**は吸収しない。縦は MC 版ごとの別 source set / サブプロジェクト + 自前の薄いアダプタで対応。

---

## 4. ターゲット選定（優先順位）

### 決定: NeoForge 1.21.1 を最優先

**裏付け（2026年6月時点の調査）:**

- NeoForge 公式（2025年振り返り）: 1.21 はリリース18ヶ月後も最も人気の高い NeoForge バージョンで、16,000+ mod を蓄積、成長率は 1.20.1 Forge を上回る。1.21.1 NeoForm アーティファクトが全インストールで使われる実質的な基盤。
- Mekanism: 最新リリースが 1.21.1 / NeoForge 向け（2026年4月時点で活発更新）。
- Create 系: NeoForge 1.21.1 ベースの modpack が現役（CreateVerse 等）。
- 大型 modpack（ATM10 等）も NeoForge 1.21/1.21.1 が中心。
- → **「Create + Mekanism を載せる現実のサーバー」はほぼ NeoForge 1.21.1 に集結。**

### 優先順位

```text
1. NeoForge 1.21.1   ← 確定（最優先）
2. Forge 1.20.1      ← 生きている踊り場（実用コミュニティあり）
3. Fabric 1.21.11    ← 更新あり
（Forge 切り捨ても選択肢。要・勢力図調査）
```

### バージョン潮流の認識

- Forge は 1.20.1 までが最後の大きな踊り場。1.21.1 以降は NeoForge へスイッチが大きな流れ。
- **Forge 1.21.1 は実運用ではほぼ選ばれない「過渡期の徒花」**（ただし教材としては比較軸に使える。[ai-learning-design] 参照）。
- 26 系（26.1〜）: NeoForge 公式は移行を推奨（非難読化のメリット）。だが Create/Mekanism 級の重量級エコシステムは未追従で、コミュニティは 1.21.1 に固着。**「適度に追いかける」方針**で正解。マイクラリモコンは依存がゆるいため、エコシステムが 26 に固まった時点で薄いアダプタ追加で対応可能。
- 1.21.1 は当面「長命な踊り場」になる見込み（1.20.1 が Forge 最後の踊り場として今も生きているのと同じ構図）。Phase 2 でここに投資する価値は高い。

---

## 5. 権限（PermissionProvider）の扱い

現状コードはすでに以下の構成:

```text
PermissionProvider
  ├─ LuckPermsProvider   （あれば使う）
  └─ FallbackProvider    （現状: フォールバック時は建築範囲だけが変わる）
```

- LuckPerms は NeoForge/Forge/Fabric 版が公式に存在し、1.20.1 / 1.21.1 ともにカバー。「LuckPerms 前提」は mod 環境でも維持可能。
- 認証の核（`pair_code` / `session_token` / long-lived credential＝旧 `player_token`・`2026-08-02-01` で改名）は LuckPerms 非依存。LuckPerms は**認可**部分のみ。
- この PermissionProvider インターフェースを mod 展開時もそのまま流用できる。Phase 1（Paper）では LuckPermsProvider のみ実装、インターフェースは既に切れている。
- **build range は paired UUID から load した LuckPerms User の effective meta として解決する**（`2026-08-06-01`）。`LuckPermsPermissionManager` は既存の `QueryOptions` を使い、
  `user.getCachedData().getMetaData(queryOptions).getMetaValue(buildRangeMetaKey)` の結果を整数化して返す。
  primary group の `Group#getCachedData()` だけを直接読まず、user node・継承 group・context・weight・meta stacking の優先順位を McRemote 側で再実装しない。
  hello の `permissions.buildRange` と実際の build guard は、この同じ `PermissionProvider` の値解決経路を使う。
  `QueryOptions` の既存 `server=global` context、meta key `luckperm_permissions.build.range`、meta 欠落または整数 parse 失敗時の `0`、
  LuckPerms 不在時の `FallbackPermissionManager` は維持する。負値の契約は本決定で追加・変更しない。

---

## 6. 段取り（ロードマップ）

```text
Phase 1: Paper 版で Python / Scratch クライアント整備
         + バージョンごとの分岐・リリース構成を確立
         （クライアントは protocol だけを見る = サーバー実装系統に非依存）

Phase 2: NeoForge 1.21.1 をトライ
         → モノリポ構造（Paper + 1 mod の2系統）を構築・検証
         → Architectury 横軸 + 自前アダプタ縦軸の二軸分担を確立

Phase 3: Forge 1.20.1 / Fabric 各踊り場へ展開
         → 3系統目以降は型ができている
         → Forge 切り捨て判断はここで（要・勢力図調査）
```

---

## 7. 未決事項・要調査（別セッション）

- mod ローダー／踊り場の勢力図精査（Forge 切り捨て可否、Fabric 優先度、1.18.1/1.19.1 を入れるか）。Phase 3 の意思決定ゲートとして切り出し。
- Architectury の技術詳細解析（@ExpectPlatform の実装パターン、ビルド設定）。
- Mekanism 等の大型 mod が内部で Architectury を使うか／Forge→NeoForge 移行で何が変わったか（registry, capability→data attachment, event bus 等）。コントリビュート参加を見据えた調査。
- Paper ビルド系統と Architectury ビルド系統を Gradle でどう束ねるか（includeBuild 等）の具体設計。Phase 2 で最初にぶつかる構造課題。

---

## 8. Paper版のavailability guardと観測

公開betaで優先するsecurity workは接続時PoPではなく、攻撃と正規の大量処理に共通して効くavailability guardである（DECISIONS `2026-07-16-03`）。pluginは次のbudgetを別々に持ち、一つの曖昧なrate limitへ畳まない。

- 認証前: 同時connection、accept rate、frame size、idle / hello timeout、pair begin / poll rate、pending pair数。
- 認証後: UUID別session、connection別inflight、queue depth、queue待ち時間、per-session / player / global work budget、backpressure / cancel。
- Minecraft workload: block変更数、entity生成、chunk load/generation、explosion/TNT、tickへ投入した実時間。

bulk APIは「大きいから拒否」だけにせず、bounded queueへ受け、Paper APIでmain threadの仕事を複数tickへ分割する。session間をfairに回し、上限超過はreasonとretry可能性を返す。connectionを閉じるべきprotocol abuseと、一時的backpressureを区別する。exact capはalphaの授業相当scenario / TNT / buggy loop / reconnect floodで較正し、実装前に推測で固定しない。

観測は次の責務分担にする。

- Cockpit: host CPU / memory / swap / disk / network / process。
- Paper同梱sparkとspark API: MSPT、tick、GC、heap、plugin/JVM workload。
- McRemote: connection / session / inflight / queue / work / reject / throttle / cancel metric。

spark APIはsoft dependencyにし、利用不能時は固定capで動作を継続する。telemetryでcapを調整する場合はhysteresisと回復待ちを持たせ、metric欠落を「負荷ゼロ」と解釈しない。詳細profile採取はoperator操作に限定し、通常logや公開証跡へtoken、player情報、IPを出さない。Paper APIは仕事を安全にscheduleする面、spark APIは観測入力であり、互いの代替ではない。

長期player credential storeはworld dataと別lifecycleに置く。通常world restoreで触らず、revoke履歴を含む新しいstoreを復元できないdisaster recoveryでは、古いstoreを信頼するより全credential失効・再pairを既定とする。Proof of Possession用のkey / nonce / signature schemaは未批准であり、現在のplugin data modelへ先行追加しない。**この「revoke履歴」を独立backendとして具体化した実装契約は §9**（`2026-08-02-01`）。

---

## 9. long-lived credential の永続化と失効耐性（確定 `2026-08-02-01`）

§8 末尾の「world data と別 lifecycle」を実装契約へ具体化した節。wire 側の正本は `10-protocol/wire-format-design_ja.md` §6.5 / §6.6 / §7.3 で、本節は **plugin 内部の構造・順序・失敗時挙動**を持つ。両者の境界＝wire は観測可能な意味だけを定義し、線形化や backend 構造を露出しない。

### 9.1 二 backend への分離

永続状態を、rollback domain の異なる二つの backend へ分ける。

- **`CredentialStore`**（管理用 snapshot）：`credential_id` / `token_hash`（SHA-256）/ `player_uuid` / `type` / `device` / `issued_at` / `last_used_at` / `expires_at` / `revoked_at` を持つ atomic snapshot。`credential_id` は server 生成 UUID＝公開してよい管理用 ID。日時は UTC ISO 8601。`device` は表示用ラベルで認証要素ではない（trim 後 1〜64 文字・重複可）。
- **`RevocationAuthority`**（失効の正本）：credential domain manifest と **create-only tombstone**。認証・`list`・active limit・`current` 判定へ**常に overlay** する。

**snapshot の `revoked_at` を revoke の security 正本にしない。** snapshot は管理用 projection であり、失効の真偽は authority が持つ。この非対称が、snapshot だけを巻き戻す rollback から revoke を守る。

**session token（`mcrs_`）も同じ snapshot へ収容する**（`2026-08-02-08`）。ただし `RevocationAuthority` の overlay 対象にはしない＝session token は revoke を持たず、無効化が `expires_at` という絶対時刻の評価と credential domain reset（§9.5）だけで決まるため、**snapshot を巻き戻しても「期限切れが期限内へ戻る」ことが起きず rollback 安全**である。したがって tombstone 機構は long-lived credential にのみ必要。session record は §6.6 の管理 wire（`auth.listCredentials` / `auth.revoke`）の対象にせず、long-lived の active 上限（§9 冒頭の 16）にも数えない。

**実装到達点（2026-08-18）**：b4候補`dab6908494290c894d8efbe6828707e544860fa1`はsession tokenを
in-memory storeだけに保持しており、本節のsnapshot収容を未実装である。同一b4 runtimeの通常再起動後、期限内tokenが
`auth_required`となることをhome-alphaで確認した。これは本契約の撤回理由ではなく実装差分であり、正式根拠は
[b4 home-alpha統合・認証再起動evidence](../14-evidence/records/2026-08-17-b4-home-alpha-integration_ja.md)とする。

record が 0 件でも domain を検証できるよう、snapshot は header を持つ。

```json
{
  "schema_version": 1,
  "credential_domain_id": "...",
  "records": []
}
```

authority は manifest を持つ。

```json
{
  "schema_version": 1,
  "credential_domain_id": "..."
}
```

各 tombstone は最低限これを持つ。

```json
{
  "schema_version": 1,
  "credential_domain_id": "...",
  "credential_id": "...",
  "token_hash": "...",
  "player_uuid": "...",
  "revoked_at": "..."
}
```

### 9.2 domain 整合と fail close

- 未知 `schema_version`、authority の欠落・破損、snapshot と authority の `credential_domain_id` 不一致は、いずれも**空 store 扱いにせず fail closed** とする。
- snapshot record 側にも domain を重複保持する場合、header との不一致を corruption として fail closed にする。
- store を読めない場合、**空 store として通常起動しない**。store 障害で auth enforcement を OFF へ落とさない（`2026-07-04-03` 項5 の「トグルは開発順序の道具、リリース既定は enforced」と同旨）。
- 起動時に snapshot と authority の双方が無い場合も、空 state を自動生成しない（§9.5）。
- 起動時に `credential_id` と `token_hash` の重複・矛盾を検査する。
- 可用性は認証を緩めることでなく、授業前 doctor・bootstrap 完了確認・domain health 確認・mount / path preflight・明示 reset 導線で確保する。**自動的な無認証 fallback は行わない。**

### 9.3 revoke の線形化点

`auth.revoke` と `auth.logout` はこの順で処理する。

1. `credential_id`・token hash・所有 UUID を解決し、要求元 UUID が所有者であることを検証する。既存の正当な tombstone から解決できる再試行は idempotent に扱う。
2. authority と同じ directory の create-only temporary file へ tombstone を書き切る。
3. temporary file の `fsync` を完了する。
4. final へ非上書き publish し、authority directory の `fsync` を完了する。**ここを revoke の線形化点とする。**
5. 対象 credential で認証された**全ての** active `RemoteSession` を終了対象として mark する（同一 UUID は最大 16 の並行セッションを持てる＝`2026-07-04-03` 項7。一つでも残すと revoke 済み credential が既存接続を通じて動き続ける）。
6. 管理用 projection である snapshot の `revoked_at` 更新を試みる。
7. revoke 成功 response を返す。
8. step 5 で mark した**全 session** の socket を close する。

step 4 以降は credential が失効済みであり、**step 6 が失敗しても revoke 成功を失敗へ戻さない**。authority overlay により認証拒否・`list` からの除外・active limit からの除外・`current` からの除外を維持し、server health を degraded にして snapshot reconcile 対象へ送る。

`credential_store_unavailable` を返すのは **authority durable commit 前の失敗**、または起動・read 時に snapshot / authority の信頼性を確立できない場合に限る。**線形化後の snapshot projection 失敗には返さない。**

非上書き publish と directory `fsync` の境界で I/O 結果が不確定な場合は、authority を unhealthy として認証を fail closed にする。この reason は token が active であることを保証しない。正当な既存 final があれば directory `fsync` を再試行して commit へ進める。線形化直後の crash や response 喪失では client が結果を受け取れないまま revoke 済みになり得るが、再試行または旧 token での再接続により `token_revoked` へ収束する。

### 9.4 create-only file backend 契約

初期 `RevocationAuthority` の file backend はこれを満たす。

- server 生成 UUID を canonical 検証した値だけを final filename に使い、**wire の ID を path として信用しない**。
- authority と同じ directory へ temporary file を `CREATE_NEW` で作る。
- 全内容の write、file `fsync`、final への原子的な非上書き publish、directory `fsync` を行う。
- `REPLACE_EXISTING` 相当を使用せず、対象 filesystem での非上書き性を実装 test で実証する。
- final が既存なら全内容を検証し、同じ schema / domain / ID / hash / UUID で必要な directory `fsync` を完了できた場合だけ idempotent success とする。
- 同じ ID で内容が異なる final、壊れた final、未知 schema、symlink、非 regular file は無視せず authority corruption として fail closed にする。
- 中断された temporary file と final tombstone を名前空間・形式で区別する。

保存 path と serialization は plugin 内部実装であり **wire 契約にしない**。別 backend（SQLite 等）へ交換しても、同じ線形化・create-only / idempotency・domain 整合・durable-before-success を保証する。

### 9.5 bootstrap / reset の所有境界

- **stack**：`CredentialStore` と `RevocationAuthority` の保存 resource を profile に従って用意・mount し、明示 bootstrap / reset の operator 承認と transaction を管理する。
- **plugin**：domain ID 生成、manifest、snapshot、tombstone の形式と生成処理の正本を持つ。
- stack は plugin 内部 JSON を独自生成せず、plugin 所有の明示管理 surface を呼ぶ。
- 二 backend を atomic commit できないため、途中失敗は domain 欠落・不一致として fail closed にする。
- bootstrap の再試行は、双方が空、または plugin 所有の同一 bootstrap transaction の安全な途中状態と検証でき、credential record / tombstone がまだ無い場合だけ許可する。
- **reset は通常起動時の自動修復ではない。** 全 credential 失効を伴う明示操作とする。

### 9.6 rollback / disaster recovery

- world restore と credential snapshot restore は **revocation authority を書き戻さない**。
- snapshot が revoke 前へ戻っても、authority tombstone により旧 credential を拒否する。
- authority を読めない・信頼できない・snapshot と domain が一致しない場合は fail closed にする。
- host 全損等で current authority を回収できなければ、古い snapshot を昇格せず、**新 domain ＋ 空 snapshot で全 credential 失効・再ペアリング**とする（§8 末尾および `2026-07-16-03` の安全側既定）。ただしこれは**明示的な restore / recovery 操作に限る**＝通常起動時の store 破損を検出して黙って空 store へ置換してはいけない。
- offline catering では cloud authority を必須にせず、local 分離により通常 rollback だけを保護する。
- VPS で host 全損後の credential 継続を保証する場合は、revoke 線形化前に off-host authority の durable commit まで同期完了させる。非同期複製だけで継続性を主張せず、remote freshness を証明できない復旧は全失効へ倒す。

### 9.7 plugin が保証する範囲と deployment が保証する範囲

rollback domain は物理 volume の個数ではなく、**ある rollback 操作が何を書き戻すかという write set** で決まる。同一 filesystem でも snapshot path だけを戻す操作なら別 domain として機能し、逆に別 volume でも VM snapshot や storage 全体を同時点へ戻せば両方が戻る。plugin から物理的な保護強度は判定できない。したがって契約を二層に分ける。

**plugin が保証する**：`CredentialStore` と `RevocationAuthority` が別 backend 境界であること、保存先を独立して設定できること、snapshot header と authority manifest の domain 検証、create-only tombstone、authority durable commit を revoke 線形化点にすること、authority の欠落・破損・domain mismatch での fail closed、authority と snapshot を同じものとして扱わないこと。加えて plugin が検証できる範囲として、同一 canonical path の拒否、一方が他方の配下になる設定の拒否、同一 backend identity を判定できる場合の拒否。**「別 volume であること」「VM snapshot から独立していること」は検証も保証もしない。**

**deployment が保証する**：authority を保護対象 rollback の write set から外すこと、profile ごとの同一 filesystem / 別 volume / off-host の選択、その構成でどの障害まで保護できるかの宣言、backup / restore / doctor による構成の検証。

> plugin が保証するのは domain 整合、authority overlay、revoke 線形化である。authority が対象 rollback の write set 外にあること、および物理的な分離強度は deployment profile が保証する。**snapshot と authority を同時に rollback した場合の revoke 維持を、plugin 単独では保証しない。**

**二 volume は plugin の起動不変条件にしない。** stack profile の推奨構成として扱う。

### 9.8 旧 `mcrp_` からの移行

`2026-08-02-01` が `player_token` / `mcrp_` を long-lived credential / `mcrl_` へ改名した際の移行規則。

- 現行実装の `mcrp_` は server 側が in-memory で、**再起動を越える移行対象 record が存在しない**。したがって server-side migration は行わない。
- 新実装は `mcrp_` を**新規発行しない**。
- 保存済み `mcrp_` は `token_not_found` 等の**既存**認証 reason で無効化する（移行専用の新 reason を足さない）。
- client は破棄して一度だけ `mcrl_` を再取得する＝`2026-07-04-03` 項3 の破棄・再ペアリング側のフローにそのまま乗る。
- **一時的な二重 prefix 発行期間は設けない。**
- plugin / Python / Scratch の wire 変更は**同一互換単位で着地させる**。
- **改名は §9.1〜§9.6 の実装と同時に行う**（2026-08-02 の McRemote 着地確認で明確化）。`mcrp_` / `player_token` は config・`TokenStore`・pairing 試験など現行実装そのものに残っており、**名称だけ先に変えると実装と wire 契約が不整合になる**。`CredentialStore` と `RevocationAuthority` の導入に合わせて一括で移行する。

### 9.9 検証、credential checkpoint、gate（`2026-08-06-02`）

#### 9.9.1 McRemote が所有する checkpoint

credential health projection は常駐 telemetry ではなく、**Stack doctor が明示要求した時点の checkpoint 応答**である。heartbeat、定期更新、常駐 polling、起動時または health 遷移時の自発更新は行わない。

- Stack が container-local console から `credential checkpoint <checkpoint_id>` を実行したときだけ生成する。command は console-only とし、player command、RCON、McRemote wire へ公開しない。
- `checkpoint_id` は Stack が doctor run ごとに生成する非 null の不透明な nonce である。McRemote は要求値を projection へそのまま相関値として返し、現在性を時刻から推測しない。
- McRemote は checkpoint のたびに snapshot、revocation authority、credential domain の完全な read / schema / integrity / domain consistency 検証を行う。backend を変更せず、reconcile、bootstrap、reset、修復を副作用として起動しない。
- 検証結果は `/data/plugins/McRemote/credential-health.json` へ atomic publish する。途中書き込みを final path で観測させず、publish 失敗時に古い file の `checkpoint_id` を新しい run の結果として扱わせない。
- schema v1 の top-level は `schema`（固定値 `mcremote.credential-health`）、`schema_version`（`1`）、`emitted_at`、`checkpoint_id`、`health`、`reasons`、`credential_snapshot`、`revocation_authority`、`domain_consistency`、`reconcile_pending` とする。credential record、token / token hash、player UUID、device label を projection へ含めない。
- `credential_snapshot`、`revocation_authority`、`domain_consistency` の nested object shape と enum vocabulary は McRemote と Stack が同じ schema revision の fixture で固定し、双方の parser / writer test を通してから利用可能とする。未確定の値を Stack が寛容に推測しない。

checkpoint は観測 surface であり、§9.5 の bootstrap / reset transaction ではない。外部 transaction ID を checkpoint へ流用せず、doctor、通常起動、restore から bootstrap / reset を自動実行しない。bootstrap / reset の冪等再試行と transaction 所有権は未確定の別論点として残す。

#### 9.9.2 Stack consumer 境界

Stack doctor は次を満たす。

1. deployment 単位で doctor を直列化し、一回の run につき新しい `checkpoint_id` を一つ生成する。
2. Stack CLI 内部から container-local console helper を使って checkpoint command を投入する。operator に直接 Docker command を要求せず、RCON と McRemote wire を代替 transport にしない。
3. 同一 run 内の短い bounded read / retry だけを許し、projection file を 16 KiB 以下の UTF-8 regular file・non-symlink として読む。
4. schema 名、version、必須 field、enum、field 間の整合、`checkpoint_id` の完全一致を検証する。欠落、timeout、上限超過、unknown version / enum、矛盾、nonce 不一致は fail closed にする。
5. `emitted_at` は形式と明白な未来値だけを sanity check し、固定秒数の freshness window には使わない。古い `HEALTHY` の排除は同一 doctor run の nonce 一致で行う。
6. snapshot / authority の内部 JSON を解析・生成・修復せず、plugin 所有 projection の公開 schema だけを consume する。
7. console helper の前提である `CREATE_CONSOLE_IN_PIPE=true` を render / doctor で確認する。実行 UID / GID は preset lock と render へ固定して container 実体と照合するか、同等に再現可能な実証契約を持つ。権限の偶然一致を runtime contract にしない。

#### 9.9.3 公開 gate

実装の検証項目と、公開導線を開く gate の開放条件は `2026-08-02-03`（DECISIONS 未確定節）が持つ。Stack 側の world restore と recovery archive import が credential を書き戻さない deterministic write-set 試験は実施済み。credential checkpoint は同条件 (6) の doctor 観測契約を具体化するが、**契約確定だけでは gate を開かない**。`RevocationAuthority` 本体、二 backend profile、checkpoint の両 repo test、runtime UID / GID の再現可能性、plugin live test、live restore 後の authority 継続が正式証跡として揃うまで gate は閉じたままとする。

### 9.10 b3後の停止点と再開順序（`2026-08-07-01`）

b3 の横断スコープは credential lifecycle の完了を待たずに閉じる。§9 の contract、実装済み部分、unit／live evidence は破棄せず後続 slice の入力にするが、long-lived の一般公開、Python 既定化、Stack 一般 profile への露出は行わない。

ケータリング実践で session の期限切れ、server 再起動、複数日にまたがる利用に伴う再 pairing の負荷を観測し、長期 credential の実需要が確認された後に再開を横断決定する。再開後は次の順序を守る。

1. `auth.listCredentials`／`auth.revoke`／`auth.logout` の plugin・client／CLI・conformance・live evidence を正式な管理面として閉じる。
2. §9.9 の checkpoint と Stack doctor を共通 fixture、deterministic test、実 profile で接続する。
3. 秘密を公開 artifact／logへ出さない live runner を固定する。
4. snapshot rollback、authority 継続、backup 非包含、失敗時 rollback を一つの transaction として閉じる。
5. 明示 reset、途中失敗からの再試行、authority 喪失時の新 domain＋全失効＋再 pairingを含む災害復旧を閉じる。

段階の途中で公開 gate を開かない。b3完了とlong-lived公開可否を同一判定へ戻さず、最終的な開放条件は引き続き §9.9.3 と `2026-08-02-03` が持つ。観察と再開判断の正本は `00-hub/authentication-roadmap_ja.md`。

## 10. b5／b6のevent・entity・dispatcher基盤

b5は、イベントを受けて調べ、生成・操作するAPIを支える大規模な共通基盤を閉じる段である
（DECISIONS `2026-08-16-04`〜`07`）。b6はこの基盤上の中規模API追加に限定し、別のidentity、
transport、queueを作らない。

### 10.1 Event captureとepoch別ring

Bukkit Event objectをsession寿命へ持ち越さず、listener実行中にimmutable DTOへ変換する。paired playerの
対象eventは、そのplayerへ束縛された全active connection epochへ複製する。epochごとに独立した有限ringと
1始まりの単調増加sequenceを持ち、reconnect時に全て破棄する。

- overflowは最古から退去し、`overflow_dropped_total`へ加算する。
- resource admissionで投入不能なら`capacity_dropped_total`へ加算する。
- pollは非破壊で、response喪失後も同じcursorを再取得できる。
- `events.clear`による削除だけを`explicitly_discarded_total`へ加算する。
- event DTOに発生時点のworld／originをcaptureし、後続のbuild state変更で書き換えない。
- right-clickのmain／off-hand二重発火は相関判定して1件へ正規化する。

ring件数、総byte、poll limitのexact値はunit／load／live試験で較正するruntime policyであり、本節から
推測しない。compact JSON-RPC responseの61,440 bytes上限はwire contractとして先に適用する。

### 10.2 Entity handle registry

registryはconnection epochごとに`mceh_` handleとentityの対応を保持し、同一epoch／同一entityへは同じ
handleを返す。handleはUUIDや認可情報を符号化せず、操作ごとにepoch ownershipとpermissionを再検証する。
playerはregistryへ収容しない。

spawnではworld変更前にhandle slot、permission、chunk／work admissionを一括確認する。slotを予約できない
場合は`entity_capacity_exhausted`で終了し、副作用を起こさない。spawn失敗時は予約を解放する。
disconnect／reconnect、remove成功、外部world移動でhandleを失効させる。成功した`entity.setPose`による
world移動ではissued worldを更新する。

Paper上でremoved／unloaded／world-changedをどこまで安定して判別できるかは実装試験で確認し、判別不能な
状態を推測でreasonへ割り当てない。

### 10.3 Dispatcherとavailability admission

dispatcherは位置配列だけを前提にせず、b6のsign／typed particleまで有限なstructured JSON paramsを
検証済みDTOとしてhandlerへ渡せる構造にする。permission、handle capacity、入力byte、chunk走査、work量を
副作用前に検証する。

`backpressure`は副作用前の一時的拒否、`work_limit_exceeded`は入力縮小が必要な拒否、
`entity_capacity_exhausted`はhandle capacity拒否である。副作用開始後に結果を確定できない場合は
`internal_error`とし、spawn後のresponse喪失を含めclientへ自動retryを許さない。

`world.getHeight`のcolumn走査、nearby entityのradius／件数／chunk走査、particle count、sign更新は
§8のper-session／player／global work budgetへ計上する。`world.setSign`は全入力検証後に変更し、
更新失敗時の完全rollback方法をPaper実装で実証する。

### 10.4 実装・検証の停止線

`world.getHeight`候補は搬送元worktreeでunit 26件、Gradle build、diff checkまで合格したが未commitである。
event listener、ring、handle、spawn、Paper状態reason、sign rollbackは未実装・未実証であり、設計確定を
到達証拠へ読み替えない。plugin fixture完了と、Python／Scratch／WireScopeを含むcompatibility setおよび
real-browser E2Eを別gateとして扱う。
