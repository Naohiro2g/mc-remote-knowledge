# long-lived credential lifecycle live-human evidence

## Record

- test ID: `2026-08-02-long-lived-credential-lifecycle-live-human`
- test class: `unit/deterministic` + `live-human`
- result: PASS（下記 Claim boundary の範囲）
- observed at: 2026-08-02（初版）/ 2026-08-03（Addendum＝完了条件 4・5・7）
- source repository: `Naohiro2g/McRemote`
- source branch: `feature/long-lived-credential`
- credential implementation commit: `7b1a98934d69451cd53559bc595464ab1e21d68e`
- restart test harness commit: `8dc575ef7dc2bf4bb0c8e5611c085286e06c6c7a`
- multi-session test harness commit: `ce63dda8eabc948debe5359ed05dc0df4f8b4b61`
- revoke-persistence harness commit: `ecf967f`（Addendum）
- **built and installed JAR SHA-256: `1ea1baa3545988d083d185eded38d39754b8dc7fe7a910ac0f42726a8d952869`**
- knowledge contract: `2026-08-02-01` / `2026-08-02-03` / `2026-07-16-03` / `2026-07-04-03` 項3・項7
- knowledge contract commit（搬送時に読まれた版）: `a2615c668082e79e3ca2f48cab9143b0ee57295d`

秘密実値は含まない。placeholder と除去対象の定義は
[artifacts/redactions.json](../artifacts/2026-08-02-long-lived-credential-lifecycle-live-human/redactions.json)。
raw terminal transcript と server raw log は受領・搬送していない。

## Anchor の性質と受理判断

**JAR digest を一次 anchor、commit を二次 anchor とする。**

build output と installed plugin の JAR SHA-256 は一致した。一方、JAR build 時の working tree には
別作業（catalog hardening）の未コミット Java 変更が4ファイル（`BlockEditCommands.java` /
`BlockQueryCommands.java` / `BlockRef.java` / `CatalogService.java`）存在した。credential 関連の
Java source は implementation commit から変更されていないが、**JAR 全体が単一 clean commit から
再現可能だったとは主張しない**。

knowledge 側はこの境界で受理した。理由は次の3点。

1. build output と installed の digest が一致しており、**subject artifact 自体は固定されている**。
   「この挙動はこのバイナリで観測された」は後からでも検証できる。失われているのは再現性であって
   証跡の同一性ではない。
2. claim は credential lifecycle に限定されており、b3 catalog release readiness や
   commit-exact artifact の根拠には使わない。
3. `2026-08-02-03` の gate は stack 側条件を含むため、この証跡だけでは開かない。**clean build での
   通し試験は gate を開く回に合流させる**方が人手の使い方として合理的で、いま再走しても
   gate を開けない証跡をもう一本作ることになる。

## Subject

`2026-08-02-01` が確定した long-lived credential lifecycle と、
`11-plugin/platform-design_ja.md` §9 のうち実 server で観測できる性質。

- `mcrl_` credential の発行と `auth.listCredentials.current`
- server restart を跨いだ同一 credential の再利用
- `auth.logout` / `auth.revoke` 後の `token_revoked`
- **同一 credential で認証済みの2 session を revoke 後に全て close**（§9.3 step 5 / step 8）
- 非 current credential の個別 revoke と list からの除外
- **revoke 状態が通常再起動を跨いで維持されること**（authority tombstone の耐久性）
- **server 保存物と通常 log に raw bearer credential が存在しないこと**
- credential domain が restart 前後で同一かつ `HEALTHY`

## Runtime identity

| 項目 | 値 |
| --- | --- |
| package / plugin version | `1.21.11-2100.0.0b3` |
| protocol | `21.0.0` |
| Minecraft | `1.21.11` |
| Paper | `1.21.11-130` |
| Java | `25.0.3` |
| auth enforcement | `true` |
| credential domain health | `HEALTHY` |
| transport | loopback test connection |

package 名は稼働 artifact の version 表示であり、long-lived credential を b3 release scope へ
含める主張ではない。

## Scope items and claims

| Scope item / claim | Constraint | Observation | Result |
| --- | --- | --- | --- |
| long-lived 発行 | `auth.enforcement=true`、対象 player 在線 | `auth.pairPoll` が `long_lived` token を1件返し、hello 成功後の list で current 1件を識別 | PASS |
| client token 保管 | Git worktree 外の明示 path | mode `0600`、token 原文を stdout へ出さず、失効確認後に削除 | PASS |
| restart 継続 | logout せず server を通常 restart | restart 前後で同一の pseudonymous credential、domain health `HEALTHY`、同一 domain。保存 token で pairing なし hello / catalog / list 成功 | PASS |
| logout | current long-lived credential | `auth.logout` が `revoked:true` を返し、新規接続 hello が `token_revoked` | PASS |
| 非 current の個別 revoke | 同一 player UUID に属する明示 credential ID | `auth.revoke` 成功後、list active 数が 2→1 となり対象が消え、current は維持 | PASS |
| **全 session close** | 同一 current credential で2 TCP session を hello 済み | current への `auth.revoke` 成功 response 後、**両 session で EOF** を観測 | PASS |
| revoke 後の再接続 | 上記 current token を fresh TCP connection で提示 | hello が `token_revoked` | PASS |
| **revoke 状態の再起動耐性**（Addendum） | revoke 後に server を通常 restart | 再起動後も同じ token の hello が `token_revoked`。`authority_tombstones=1` が再起動を跨いで維持され、`revoked_projection=true` | PASS |
| **保存物・log の hash-only 性**（Addendum） | plugin data 10ファイルと通常 `latest.log`、再起動の前後 | `raw_exact=0` / `raw_body=0` / `bearer_patterns=0`。`snapshot_records=1` と `authority_tombstones=1` はいずれも hash-only | PASS |
| **list の metadata**（Addendum） | `auth.listCredentials` の応答 schema | device 一致、`issued_at` / `last_used_at` は UTC、`expires_at=null` | PASS |
| deterministic failure matrix | file backend / rollback / corruption を JUnit で再実行 | `CredentialServiceTest` 13件、failures / errors / skipped 0 | PASS |

restart 試験と multi-session 試験の hello 後には、server 取り違え防止の補助確認として
`world_constants.y_sea=62`、同一 `catalogHash`、`catalog.get` hash 一致も観測した。
これらは credential claim の前提確認に使うが、**本 evidence から catalog schema や
b3 release readiness を主張しない**。

## `2026-08-02-01` 完了条件の充足

| # | 条件 | class | 結果 |
| --- | --- | --- | --- |
| 1 | `mcrl_` を発行できる | live-human | PASS |
| 2 | 通常停止・再起動後、同じ token で hello 成功 | live-human | PASS |
| 3 | 再起動後も同じ player UUID へ束縛 | live-human | PASS |
| 4 | server 保存物・通常 log に生 token が存在しない | live-human | PASS（Addendum） |
| 5 | `listCredentials` で device / 時刻 / current を確認できる | live-human | PASS（Addendum） |
| 6 | `revokeCredential` 後、同 token の hello が即失敗 | live-human | PASS |
| 7 | revoke 状態が再起動後も維持される | live-human | PASS（Addendum） |
| 8 | revoke 時に既存接続も終了する | live-human | PASS |
| 9 | store 破損・保存失敗時に無認証へ fallback しない | **unit のみ** | PASS（live 未実施） |
| 10 | 複数 device の credential を個別に revoke できる | live-human | PASS |
| 11 | PoP なしの bearer credential であることを文書化する | 文書課題 | **未完** |

## Claim boundary / 未検証

本 evidence は次を主張しない。

- Stack profile の別 path / volume mount、backup 除外、doctor、world restore との組合せ
- VM snapshot や host 全損に対する物理 rollback 耐性
- off-host authority 複製
- 16 credential 上限の実 server 到達試験（unit のみ）
- LuckPerms 権限差を伴う credential 管理
- 3 session 以上、network partition、process kill、revoke 線形化点の途中 crash
- b3 catalog 全体、Python client 公開 UX、Scratch UX、release readiness
- 稼働 JAR 全体が単一 clean commit から再現可能であること

`2026-08-02-03` の gate は**閉じたまま**。本 evidence は plugin 側の観測可能な性質を支えるが、
gate の開放条件のうち stack 側（profile / mount topology / backup 非包含 / doctor / live restore）は
未着手である。

## Human checkpoints and invalid trials

- 人間は Minecraft 内の pair command 実行を担当した。
- 最初の multi-session 用 pair 試行では、人間が別の Minecraft server へ接続していた。API 側の
  `pairPoll` は pending のまま、別 server 側は unknown pair code となった。この試行は期限切れで
  credential を発行せず、valid matrix へ含めない。
- 正しい server へ接続し、server console の online player 確認後に新しい pair code を発行して成功した。
- それ以前に、raw token を保存しない旧 test harness で long-lived credential を1件発行していた。
  server は hash-only のため token 原文を復元できず、管理 record だけが active として残った。
  multi-session 試験で新 current credential からこの非 current credential を明示 revoke し、
  list からの除外を確認した。
- この method correction により、restart 試験用 harness は token 原文を表示せず Git 外の `0600`
  file へ明示保存し、失効後の reconnect 確認に成功したときだけ削除する形になった。
- 最終 active 数は、active 1件を観測後にその current を revoke した状態から導出できる。ただし
  revoke 後は認証 credential が無いため、**post-revoke list で0件を直接観測してはいない**。

## Artifacts

- [client-transcript-sanitized.txt](../artifacts/2026-08-02-long-lived-credential-lifecycle-live-human/client-transcript-sanitized.txt) — 発行・restart 継続・logout・multi-session revoke の再構成 transcript
- [revoke-persistence-transcript-sanitized.txt](../artifacts/2026-08-02-long-lived-credential-lifecycle-live-human/revoke-persistence-transcript-sanitized.txt) — Addendum。保存物監査と revoke 後再起動
- [server-identity-sanitized.txt](../artifacts/2026-08-02-long-lived-credential-lifecycle-live-human/server-identity-sanitized.txt) — Paper `latest.log` の identity 行と JAR digest
- [unit-test-summary.txt](../artifacts/2026-08-02-long-lived-credential-lifecycle-live-human/unit-test-summary.txt) — `CredentialServiceTest` 13件の内訳
- [redactions.json](../artifacts/2026-08-02-long-lived-credential-lifecycle-live-human/redactions.json) — placeholder と除去対象の定義
