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
- 認証の核（`pair_code` / `session_token` / `player_token`）は LuckPerms 非依存。LuckPerms は**認可**部分のみ。
- この PermissionProvider インターフェースを mod 展開時もそのまま流用できる。Phase 1（Paper）では LuckPermsProvider のみ実装、インターフェースは既に切れている。

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

長期player credential storeはworld dataと別lifecycleに置く。通常world restoreで触らず、revoke履歴を含む新しいstoreを復元できないdisaster recoveryでは、古いstoreを信頼するより全credential失効・再pairを既定とする。Proof of Possession用のkey / nonce / signature schemaは未批准であり、現在のplugin data modelへ先行追加しない。
