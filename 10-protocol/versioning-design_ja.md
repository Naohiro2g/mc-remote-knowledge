# 設計記録: プラグイン／Pythonモジュールのバージョニング

> マイクラリモコン（Code2CreateClub / mc-remote.com）設計記録
> 関連: `Naohiro2g/McRemote`（プラグイン）, `Naohiro2g/minecraft-remote-api`（API）
> 結節点: 本文書のプロトコル概念は [platform-design] のマルチプラットフォーム展開、[debug-session-design] の通信仕様と直結する。

---

## 1. 背景・きっかけ

マイクラ 26.1 からのバージョニング変更が出発点。従来の方式を見直し、**プロトコルの概念を導入**して、コンポーネントごとのバージョニングを独立・自然化する。

### 従来方式（現状）

```text
プラグイン: mc-remote-1.21.4-1.0.13.jar
モジュール: minecraft-remote-api 1214.10.13
```

- プラグインは MC バージョンを名前に含むため、対応表が不要。
- モジュールは「バージョニングの常識」である3つ組（semver）に収めるため、MCバージョン部を `1214` のように圧縮していた。
- 問題点: モジュールのバージョン空間が窮屈。MC版・修正・機能追加が `1214.10.13` という1つの数列に押し込まれ、自然な semantic versioning ができない。

---

## 2. 決定: プロトコルバージョンの導入

接続性（プラグイン ↔ クライアント間の通信互換）を表す独立した軸として **プロトコルバージョン**を導入する。

```text
protocol 2.2.1
  plugin: mc-remote-1.21.11-221.2.7
  api:    minecraft-remote-api==221.1.2

protocol 1.4.0
  plugin: mc-remote-1.21.8-140.0.0
  api:    minecraft-remote-api==140.0.0
```

### 設計例（判断履歴つき）

```text
param_mc_remote改造版:
  protocol 1.7.0
  plugin   mc-remote-1.21.11-170.0.0
  api      minecraft-remote-api==170.0.0

world階層対応:
  protocol 2.1.0
  plugin   mc-remote-26.1.0-210.0.0
  api      minecraft-remote-api==210.0.0

同じMC/別protocol:
  protocol 2.2.0
  plugin   mc-remote-26.1.0-220.0.0
  api      minecraft-remote-api==220.0.0
```

最後の例（同じ MC 26.1.0 で protocol 2.1.0 と 2.2.0 が併存）が、**プロトコルを MC バージョンから独立させた意義**を端的に示す。

---

## 3. プロトコルバージョンの増分ルール（semver の意味づけ）

**接続性をキーに据える。**

| 区分 | 意味 | 例 |
| ------ | ------ | ----- |
| メジャー | wss 追加、構造的な変化 | コマンドフォーマットの非互換変更、新トランスポート層 |
| マイナー | API の追加・変更（後方互換） | 新コマンド、新パラメータの追加 |
| パッチ | バグフィックス | 判定バグ修正、座標オフセット修正 |

この定義により、**「protocol が同じならプラグインと API は混在して使える」**という保証が成立する。プラグイン・API それぞれが独立して更新されても、protocol が一致する限り相互運用できる。

---

## 4. 独立性の設計判断

### なぜ MC バージョンと protocol を分離するか

- **古い MC サーバーの固定運用**を許容するため。ユーザーが特定の MC バージョンに固着して使う可能性がある（とくに mod サーバー。詳細は [platform-design]）。
- MC バージョンに対しては**対応表が必要**になるが、その代わりにモジュールのバージョニングが窮屈でなくなる。トレードオフとして対応表を受け入れる。

### コンポーネント間の決定連鎖

```text
プラグインが決まる
   → protocol が決まる
      → Python モジュールが決まる
      → Scratch / Java など他言語プラットフォームの対応版も決まる
```

protocol が「ハブ」となり、各言語クライアントの対応バージョンを一意に導く。

---

## 5. 範囲許容（version range）の扱い

「どの組み合わせを許容するか」の方針。

### 範囲が現れる3ケース

1. **バグフィックス・マイナーの後方互換**: 同一 protocol 内で `plugin 221.2.0〜221.2.7`, `api 221.1.0〜221.1.2` のような幅。ユーザーは手持ちの中間版を使いたい。
2. **MC バージョンの互換範囲**: 1つのプラグインビルドが複数 MC で動くか（MC 本体の後方互換性に依存）。
3. **古い MC サーバー対応・移行期間**: 旧 protocol を EOL 予定日まで保守。

### mod 文脈での「範囲」の正体（重要）

mod の世界では連続範囲ではなく、**離散的な「踊り場」集合**として範囲が現れる（詳細は [platform-design]）。

```text
protocol 2.2.0 の supported_mc_versions:
  - 1.18.1
  - 1.19.1
  - 1.20.1
  - 1.21.1
（1.18.2 や 1.19.4 は含まない = 踊り場ではないから）
```

これは「範囲」ではなく「飛び石的な踊り場リスト」。`mc_constants.py` のフォールバック設計（block 密 / entity, particle 飛び飛び）の思想とも一致する。

---

## 6. 互換性表の構造化（ドキュメント自動化）

各 protocol 発表時に、リポジトリのルートへ機械可読な互換性記述を置く。

```json
{
  "protocol": "2.2.1",
  "released": "2026-06-16",
  "status": "stable",
  "components": {
    "plugin": {
      "min": "221.2.0",
      "latest": "221.2.7",
      "jar_pattern": "mc-remote-[MC_VERSION]-221.2.*.jar"
    },
    "api": {
      "min": "221.0.0",
      "latest": "221.1.2",
      "pypi": "minecraft-remote-api>=221.0.0,<222.0.0"
    }
  },
  "supported_mc_versions": ["1.21.11", "1.21.10", "1.21.4"],
  "breaking_changes": [],
  "backward_compatible_with": ["2.2.0", "2.1.0"]
}
```

利点: ドキュメント自動生成、CI での互換性チェック、ユーザーへの組み合わせ提示が容易。

> protocol 仕様の SSOT（Single Source of Truth）は、`mc_constants.py` 自動生成パイプライン（WS3）と統合する余地がある。protocol は共通、constants は踊り場（MC版）依存、という分離を一貫させる。

---

## 7. 運用方針の確定（旧・未決3点の決着）

DECISIONS `2026-06-19-02` で確定。

### 7.1 supported_mc_versions ― 厳密管理から開始

- **「1ビルド=1MC版」の厳密管理（範囲なし）から始める。**
- 複数 MC を1ビルドに列挙するのは、テスト体制（踊り場ごとの動作確認）が整ってから。
- 却下：最初から複数 MC 列挙 ＝ 未テストの組み合わせを「対応」と宣言してしまうリスク・リリース工数増。

### 7.2 旧 protocol の EOL ポリシー

- **現行メジャー＋直前メジャー1本を active 保守**（マイナー/パッチを継続）。
- それ以前のメジャーは **critical fix のみ**、かつ **事前告知してから EOL**。
- 狙い：移行期間を1メジャー分は確保しつつ、保守対象を青天井にしない。

### 7.3 互換性表 ― JSON / `protocol.json`

- **フォーマットは JSON**（CI チェック・機械可読が素直）。却下：YAML。
- **各コードリポのルートに `protocol.json`** を置く（§6 の構造）。
- **SSOT は本 10-protocol**。コードリポの `protocol.json` はここから配布（コピー／生成）する派生物。protocol が変わったらまずここを直し、各リポへ反映する。

---

## 8. hello による protocol ネゴシエーション

接続互換の判定を**契約側で一意に定義**し、plugin / api が**同一規則**を実装する
（判定がリポごとにズレないように）。hello でサーバが版を通知する枠組みは
DECISIONS `2026-06-15-04` の延長。本節は DECISIONS `2026-06-19-03` で確定。

### 8.1 広告（サーバ → クライアント）

接続時の `hello` で、プラグインが次を通知する。

- `protocol`（例 `2.2.1`）
- `mc_version`（稼働中の MC 版）
- `supported_mc_versions`（踊り場リスト）

### 8.2 互換判定（クライアント側）

クライアントは自分が要求する protocol（`client`）とサーバの protocol（`plugin`）を
semver の意味づけ（§3）に従って突き合わせる。

| 区分 | 判定 | 理由 |
| --- | --- | --- |
| メジャー | **一致を必須**（`plugin.major == client.major`） | メジャー差は非互換 |
| マイナー | **`plugin.minor >= client.minor` を要求** | プラグインがクライアントの要求機能（後方互換追加）を満たしていること |
| パッチ | 不問 | バグfixのみで互換性に影響しない |

### 8.3 不一致時

- 接続を**拒否**し、エラー `PROTOCOL_MISMATCH` を返す。
- エラーには「サーバの protocol」「クライアントが必要とする protocol」を含め、
  ユーザーが組み合わせを直せるようにする。

> 通信仕様（hello のフレーム構造・エラーフォーマット）の詳細は [wire-format-design](wire-format-design_ja.md) 側に置き、
> 本節は**版判定のルール**（契約）に限定する。両者が食い違ったら本節（契約）が正。
> hello の版フィールド（wire-format-design §6 の `v`）は本節の protocol 版に一本化する。

---

## 9. 初版リリースとバージョン採番（MC 1.21.11 / protocol 20.0.0）

新スキーム最初の正式リリースを次で確定する（DECISIONS `2026-06-19-04`）。

```text
初版（対象 MC 1.21.11）:
  protocol 20.0.0
  plugin   mc-remote-1.21.11-2000.0.0
  api      minecraft-remote-api==2000.0.0   ← epoch 不使用
```

- 旧版（api `〜1214.10.13` / plugin `〜1.0.13`）は**ベータ（semver の 0.x 相当）扱い**とし、ここで仕切り直す。

### 9.1 なぜ 1.0.0 / 100 でなく 20.0.0 / 2000 か

- PyPI は**バージョンが後戻りできない**（番号の大きい方が「最新」）。旧 `minecraft-remote-api==1214.10.13` が既にあるため、**同じパッケージ・epoch 無し**で出す新版は**1214 を越える番号**でなければ「最新」として配られない（素の `pip install` が旧版を拾う罠）。
- クリーンに `100`（protocol 1.0.0）から始めるには番号を盛るか epoch が要る。番号を盛る案を採用し、**protocol を 20.0.0、fold して 2000** とした。`2000 > 1214` で plain 順序で勝てる。
- **メジャー「20」は破壊的変更が19回あった意味ではない。** 旧 PyPI 番号 1214 を epoch 無しで越えるための初期値であり、丸い数で「リセット＝新世代」を示すために選んだ。

### 9.2 却下した代替案

- **epoch（`minecraft-remote-api==1!100.0.0`）**：PEP 440 標準で技術的には最善だが、`1!` 記法が馴染み薄く取り違えやすいので不採用。
- **パッケージ改名**：`minecraft-remote-api`（配布名）と `mc_remote`（import 名）は、`mc-remote`/`mc_remote` の取り違え事故を避けるため**意図的に遠ざけている**。改名はこの設計を壊し移行コストも高いので不採用。
- **protocol は 1.0.0 のまま番号だけ盛る案**：protocol semver は正直になるが、plugin/api の番号と protocol の「同じ数で揃う」対称性（§2）が消えるため不採用。

### 9.3 fold（畳み込み）規則の確認

- protocol `X.Y.Z` → 数字を連結して plugin/api のメジャー番号にする（例 20.0.0 → `2000`）。
- パースは**右から patch・minor を各1桁**、**残り全部がメジャー**。
- 不変条件：**メジャーは多桁可**（20〜99 は4桁の 2000〜9999 に収まる。100 以上で桁が伸びるが右からのパースは崩れない）。**minor と patch は 0–9 を維持**する（10 以上にすると連結が曖昧になる）。

---

## 10. リリースチャンネルと pre-release ラダー（聴衆×チャンネル×昇格ゲート）

DECISIONS `2026-06-25-02`（ラダー）・`2026-06-25-03`（初版 retro-mark）・`2026-06-25-04`（成熟度軸）を `2026-07-16-01` で改訂。pre-release 接尾辞は §9 の採番（fold）と**非衝突**：接尾辞は X.Y.Z core の外に付き、fold は core のみ参照する（§9.3）。`b1`/`rc1` のカウンタが2桁に伸びても minor/patch の 0–9 不変条件には触れない。

### 10.1 組織原理

各段は「次に広い聴衆へ artifact を開く」こと。**境界の本体は段名ではなく遷移ゲート**であり、「段に入る条件（内容イベント）」と「段を出る条件（公開イベント）」は別の遷移＝**段境界の上下の縁**に割り当てる（1ラベルに二軸を overload しない）。この単調拡大は artifact の凍結度と既定取得可能性の説明であり、実行環境の価値、利用者の習熟度、公式提供の優先順位を表さない（`2026-07-22-01`）。

ラダー（聴衆×内容）に直交して、運用側の**リリース機構の成熟度**という第2軸がある（§10.9）。段は版ごとに毎回昇る不変構造、成熟度はプロジェクト全体の一度きりの片道遷移で、版番号には乗らない。

> 用語：本節は「段（rung）」に統一する。聴衆×内容で区切られた1つの帯域を指す（旧稿の「帯」「rung」は同義）。

### 10.2 段・聴衆・チャンネル

チャンネル列は固定値ではなく**現在の機構モード（§10.9）を引く関数**。モード依存はbeta / rc段であり、deployment環境の`alpha` / `beta` / `stable`とは別軸である。

| 段 | 招く聴衆 | 配布面（plugin / api） | この段に入るゲート |
| --- | --- | --- | --- |
| tag前（版段ではない） | 開発グループ | alpha環境へsource commitを直接配備 | 統合して動かす価値がある |
| `bN` | 学習者・支援者・OSS開発者・貢献者（opt-in） | **bootstrap**: GitHub(pre) / GitHub(pre)　**mature**: Modrinth(beta ch) / PyPI(pre) | 公開previewにできるsliceが動く |
| `rcN` | さらに広い利用者（opt-in） | **bootstrap**: GitHub(pre) / GitHub(pre)　**mature**: Modrinth(beta ch) / PyPI(pre) | **API 凍結**（＝教材を書いてよい合図） |
| `N`（stable） | 全員（既定取得可） | Modrinth / PyPI | 全コンポーネント mature ＋ soak（§10.9 AND 律速） |

#### 10.2.1 公式実行環境の役割と優先度

artifact の `bN` / `rcN` / `N` と、deployment 環境の `beta` / `stable` は関係するが別軸である。`stable` は凍結・soak 済みの再現性と低摩擦な入口、`beta` は tag 済み preview を用いた観察・検証・学習・貢献の主活動面を担う。これは品質・重要度・習熟度の上下関係ではなく、教室では目的に応じて選択・切替できる。教材・案内・広告宣伝の正面は対象者・目的・beta の安定度・必要な支援量で選ぶ。現状の公式提供は beta 優先で、運用資源上両立できない場合は beta を優先する（`2026-07-22-01`）。

環境は単一の全体版番号ではなく、互換性を検証したcomponent構成である。環境ごとのprofile / manifestがplugin・API・Scratch等のexact artifactを個別に選び、採用版・必要なdigest・検証根拠を更新可能な状態値として持つ。環境名からcomponent版を機械的に導出せず、全componentが同じ`bN`で進むことも恒久条件にしない。現在の同期はbootstrap期の状態であり、安定期にはcomponentごとの更新周期と各環境の採用構成が分岐し得る。ここでは互換性・再現性・exact選択だけを不変条件とし、具体的な組合せの正本は`mc-remote-stack`の構成定義に置く（`2026-07-22-02`）。

公式環境も一般利用者へ公開するものと同じモジュール・artifact・profile / manifest機構で組み立て、公式専用の非公開forkやartifactを通常成立条件にしない。ただし、特定profile、component構成、物理配置、host、常設形態まで利用者環境と同一にする規則ではない。目的に応じた構成選択とprivateな運用overlayを許し、公開contractと構成機構をdogfoodingする（`2026-07-22-03`）。

### 10.3 遷移ゲート（境界の本体）

- **tag前→b ＝ 公開previewにできるsliceのtag。** 大きなbetaを待たず、価値のある単位で`b1` / `b2` / `b3`…を切る。
- **b→rc ＝ API 凍結。** 凍ったら広い利用者向け教材を固定できる＝**教材執筆 OK の合図**。`20-教材` は rc タグを固定教材の green light とするが、学習者がbetaで観察・検証することを禁止しない。
- **rc→N ＝ soak 通過 ＋ 全コンポーネント mature（§10.9）。** 既定 install に昇格（不可逆）。
- **mode 遷移（bootstrap→mature）** はコンポーネント別・プロジェクト片道（§10.9）。聴衆ゲートとは種類が違うので別建て。

### 10.4 exact-pin 正準（ホスト先と既定到達性の分離）

正準手順は **`uv add "minecraft-remote-api==<exact>"`**（exact-pin）。素の `pip`/`uv add`（無指定）は pre-release を既定でスキップして最新 stable を拾うため、**beta / rcを公開チャンネルに置いても無指定経路では踏まない**。これはpackage managerの既定取得挙動であり、stableを学習上の上位・主環境とする政策ではない。`--pre` に依存せず、学習者・支援者・beta / rcテスターは教材または目的に応じて選んだ対象版をexact-pinする。`pip`自体も正準手順では非推奨（uv統一 `2026-06-24-02`）。

帰結：bootstrap期のpre-releaseはGitHubに留める。publish / support / yankが成熟したcomponentは`bN`からModrinth beta channel / PyPI pre-releaseへ出せる。いずれもexact-pinのopt-inであり、stableの既定取得を置き換えない。

### 10.5 接尾辞と表記

- 正準接尾辞は **`b1` / `rc1`**（PEP 440 一本化）。plugin/api は §2 の番号対称性（§9.2 で再掲）を pre-release 段でも保ち、**core 番号＋接尾辞**（例 `2100.0.0b1`）を揃える。Git tag / artifact 名の全文字列は各 surface の責務に合わせる（plugin は §10.12.1）。
- **なぜ `-beta.1` でなく `b1` か（強制選択）**：api は PyPI で配るため PEP 440 の正規化が**不可避かつ正準**で、何を書いても PyPI は `-beta.1` を `b1` に畳んで保存する＝`b1` 側は動かせない地面。一方 GitHub の pre-release は文字列と無関係な明示フラグ（どの表記でも手で立てる＝柔らかい側）。よって**動かせない側（PyPI=`b1`）に錨を下ろし、柔らかい側（GitHub）は手で扱う**のが筋。`-beta.1` を選ぶと PyPI 正準（`b1`）とタグ表示（`-beta.1`）が二文字列に割れ、core 番号＋接尾辞の揃いが壊れる。
- **core 番号＋接尾辞を揃える射程**：割れるのは pre-release 接尾辞だけで、**安定版の core 番号 `2100.0.0` は全エコシステムで同一**（ただの数字、どのレジストリも受理）。`b1` で揃えるのは**現状2チャンネル限定の便宜**であって普遍法則ではない――他言語レジストリ（npm/crates.io=`-beta.1`、RubyGems=`.beta1`、Maven=`-beta1`…）は各自の正準形を強制し、**全てを満たす単一の pre-release 接尾辞は存在しない**。相互運用は文字列でなく protocol（§3）が保証するので suffix が割れても interop は不変。将来の他言語クライアント方針は §10.13。
- **段名 `rc` と Modrinth チャンネル名 `beta` は意図的に一致しない**：Modrinth に rc チャンネルが無いため、rc ビルドは Modrinth の `beta` channel に載せる。既知マッピングであり不整合ではない（Modrinth 仕様が変わるまで固定）。
- **成熟度は版文字列に焼かない**（`rc1-gh` 等は不採用、§10.8）。命名は内容軸（API 凍結度）だけを表し、機構モードは版に乗らない。

### 10.6 alpha は環境名でありrelease接尾辞にしない

`alpha`はtag前のGitHub source commitを動かす非公開統合環境であり、`aN` releaseを予約・採番しない。配備時はsource commit、build provenance、artifact hashを記録するが、公開artifactの版を増やさない。alphaで価値あるsliceが確認できたら次の`bN`をtagしてbeta環境へ昇格する。tagなしsnapshotを`b2+`等の擬似版でbetaへ置かず、betaを小刻みに出す。

### 10.7 初版 2000.0.0 の扱いとラダー初適用版

新スキーム初版 `2000.0.0`（protocol 20.0.0, §9）は GitHub に final として出てしまったが、本来ベータ相当だった。plugin（`v1.21.11-2000.0.0`）は **GitHub 側で pre-release に retro-mark 済み**（Latest を旧 `v1.21.8-1.4.0` へ戻した）。api 側は 2000.0.0 を GitHub/PyPI とも未公開のため対象なし＝可逆窓を最大限保持（DECISIONS `2026-06-25-03`）。`2026-06-19-04` の採番（2000.0.0・fold 規則）は不変で、変えるのは公開チャンネル状態のみ。

setWorld/setBuildOrigin 分割は**コマンド署名の非互換変更＝§3 のメジャー昇格**にあたり、かつ**初版 2000.0.0 には未収録**（次のベータに収録）。これを載せる最初のラダー適用版は **protocol 21.0.0 ＝ `2100.0.0b1` 始まり**（`2100.0.0b1 → … → rc1 → 2100.0.0`）。

### 10.8 却下した代替案

- **1ラベルに内容軸と公開軸を overload**（beta が「凍結」も「公開」も同時に意味）：内容無変更で audience を広げるだけなのに番号を切り直す矛盾。→ 段境界の上下の縁に分離。
- **公開範囲を版番号に焼く**（scope を suffix 化）：scope はチャンネル集合＝分布で、版文字列上の点ではない。→ scope は host＋pre-release flag＋Modrinth channel で持つ。
- **`--pre` を教えて beta を既定経路で配る**：生徒環境に pre-release 混入事故。→ exact-pin 正準で根を断つ。
- **成熟度に関係なくbetaをGitHub限定に固定**：初期の誤取得防止には効くが、publish / exact-pin / yank運用が成熟した後もOSS開発者の取得導線を狭める。→ bootstrapはGitHub、matureはModrinth/PyPIまで広げる。
- **成熟度を pre-release 接尾辞で表す**（`rc1-gh` 等）：版文字列に運用都合を焼くと §10.5 の表記一本化が崩れ、mature 化したとき過去版文字列が陳腐化。成熟度は版でなくプロジェクト状態に属す（§10.9）。

### 10.9 リリース機構の成熟度（bootstrap / mature）と非対称成熟

**機構モード**は「公開チャンネルへ安全に publish できる運用成熟度」を表すプロジェクト状態。ラダーの段ではなく、段に直交する第2軸。正本は `grand-design-roadmap`（相マーカー流＝低 drift で1行保持、`2026-06-24-03`）。

- **bootstrap**：beta / rcをGitHub留め（pre-release）。今Modrinth/PyPIへ出すのに二の足を踏む状態は「未熟だから劣る」ではなく「bootstrapモードだからGitHub留めが正準」。
- **mature**：beta / rcを公開チャンネル（Modrinth beta ch / PyPI pre）へ。

**mode 遷移ゲート（bootstrap→mature）**：①公開チャンネルへのpublishが再現可能（手作業一発勝負でなく手順書／`gh` / `uv publish`で反復可能）②soak / yankの運用を最低1サイクル通した ③退避手順を確認済み（PyPI yank・Modrinth channel変更/版削除で戻せる）④**exact-pin runbookを利用目的ごとに検証済み**（選んだbeta / rcを取得する明示手順と、stableの無指定取得を混同しない）。

**非対称成熟（コンポーネント別 mode）**：api 側はクライアントが今後増え（他言語・ブリッジ等）、成熟タイミングは多岐にずれる。よって **mode は plugin/api 別に持つ**（`plugin=bootstrap / api=mature` 等を許す）。「PyPI は出せるが Modrinth はまだ」を待たせず表現するため。

**合わせ込みは命名でなく stable 昇格ゲートに置く（AND 律速）**：同一 protocol の plugin/api は「同じ番号なら混在可」が契約（§3）。命名 `b1`/`rc1` は一本化（§10.5）し版に成熟度を焼かないので、命名の一本化とmodeの多値化は同じ層で衝突しない。beta / rcの公開先はcomponentごとに成熟でき、残る合わせ込みは **rc→N 昇格の足並み**に集約：

| protocol N の状態 | plugin mode | api mode | その protocol の最大到達段 |
| --- | --- | --- | --- |
| 両方 bootstrap | GitHub | GitHub | rc（GitHub 留め） |
| 片方だけ mature | 公開/GitHub | GitHub/公開 | **rc 止まり**（公開側も rc のまま soak） |
| 両方 mature ＋ soak 通過 | 公開 | 公開 | **N（stable）に同時昇格** |

**stable 昇格＝全コンポーネント mature ＋ soak の AND 律速**（最遅コンポーネントに律速）。それまで「公開済みは rc 止まり・遅れている側は GitHub 留め rc」で揃える。

却下＝mode 単一強制（非対称成熟を表現できず出せる側を待たせる）／stable をコンポーネント別に先行昇格（番号同一・混在可契約 §3 が崩れ「plugin stable・api rc」をユーザーが踏む）。

### 10.10 緊急避難：final の pre-release ダウングレード（チャンネル別 demotion）

final を誤って出した／soak 前に Latest 化した場合の退避手段。**チャンネルごとに可逆性が違う**ため、最も可逆な層で気づくほど安い。§10.9 の mode 遷移ゲート③「退避手順を確認済み」が参照する一般表。

| チャンネル | demotion 手段 | 可逆性 |
| --- | --- | --- |
| GitHub | release の **pre-release フラグを ON**（`gh release edit <tag> --prerelease`）。Latest から外れ素の取得経路に出なくなる | **完全可逆**（フラグはいつでも戻せる・版番号を消費しない） |
| PyPI | **yank**（`pip`/`uv` の既定解決から除外、明示 pin のみ取得可） | 版番号は**永久消費**（同番号の re-upload 不可。yank 解除は可だが番号は戻らない） |
| Modrinth | 版の channel を `release`→`beta` に変更、または版削除 | channel 変更は可逆・削除は不可逆寄り |

- **GitHub フラグが最も安い緊急避難**＝公開チャンネル（PyPI/Modrinth）へ出す前なら完全可逆。`2000.0.0`（plugin）がこの適用第1例（§10.7、`2026-06-25-03`）。
- 公開チャンネルに出た後は yank／削除しか無く版番号を消費する。**rc を bootstrap 中は GitHub 留めにする設計（§10.9）は、この退避コスト差から導かれる**＝最も可逆な層で soak し、不可逆な公開チャンネルへは AND 律速で慎重に昇格する。

### 10.11 protocol 21.0.0 のスコープと beta 段階構築

protocol 21.0.0 を載せる配布系列は `2100.0.0b1` から始まり、旧スキーム（実質未出荷の 2000.0.0／legacy 1214.x）に対する**新スキーム major** を1本に束ねる。protocol 自体には beta 概念を持たせず、b1 は package / GitHub release 側の prerelease 段階として扱う（DECISIONS `2026-06-25-05` / `2026-06-27-01`）。

**段階構築の割り当て**：

- **b1 ＝ build model**：`setWorld(dimension)`／`setBuildOrigin(x,y,z)`（両者セッション中変更可）、`setPlayer` 除去、build state＝stream 個別（`2026-06-24-01`）、座標 絶対y＝origin y＋dy（`2026-06-25-01`、Y_SEA は hello 経由の情報定数で座標式に不使用）、既定原点 (200,0,200)。hello の版/ワールド定数通知・protocol ネゴ（`2026-06-15-04`/`2026-06-19-03`）もここで可。
- **後続 bN ＝ 認証**：pair/hello/token/LuckPerms（`2026-06-11-02`/`2026-06-15-01`）。hello に auth フィールドを足すのはこの段。
- **b→rc（API凍結＝教材執筆OK、`2026-06-25-02`）**：build model も認証も固まってから。
- **rc soak → `2100.0.0` stable**：新スキーム初の公開版（認証込み）。

**束ねの根拠**：メジャーに束ねること＝一度に凍結すること、ではない。beta は凍結前に内容を積み上げる機構なので、1メジャー内でも build model を先・認証を後に置け、分割が認証の安定化に人質を取られない。R2 はリリース節目であって protocol メジャー境界ではなく、1つの R2 が1メジャーを beta 段階構築で運べる。却下＝認証を別メジャー 22.0.0 に分離（stable 未到達の使い捨て 21 か、R2 が却下する無認証 stable を一度公開するかのどちらかで移行も二度）。

**足並み**：plugin/api は同一 protocol を名乗る限り混在可（§3）。core 番号＋接尾辞は揃える（§2）＝plugin は version `2100.0.0b1`、PythonAPI は `minecraft-remote-api==2100.0.0b1`。plugin の Git tag / release title / JAR artifact 名は §10.12.1 で分離し、`mc-target` は plugin 確認票で固定する。scratch-editor の b1 GitHub tag は component prefix を付けて `scratch-editor-2100.0.0b1` とする（DECISIONS `2026-07-02-04`）。hello 互換はメジャー一致必須（§8）ゆえ分割は両側同時実装。bN はbootstrap中GitHub限定、component成熟後はPyPI/Modrinthのpre-release面へも同じ版を出せる（§10.9）。

**`setPlayer` の終い方**：b1 でクリーン除去（互換エイリアス無し）。identity は pair/hello が持ち（`2026-06-15-02`）、旧 `setPlayer(name,x,y,z)` は name 無意味・y 規約変化で忠実エミュ不能。protocol メジャー不一致は接続拒否（§8）ゆえ in-band 互換は interop に無益。移行窓は legacy 1214.x ライン（EOL ポリシー §7.2＝現行＋直前1メジャー active）。

### 10.11.1 b2 のスコープ（確定）

b2（package `2100.0.0b2` / protocol 21.0.0 積み上げ・凍結前）のスコープ。正本決定は DECISIONS `2026-07-04-03`（出典: claude.ai 確定搬送票 2026-07-03）、item 8 の改訂は `2026-07-07-02`。b2以降の開発・実機ゲートは `1.21.11` / Java21 の floor artifact を正準とし、rc 前に最終リリース対象 MC バージョンを決める（`2026-07-08-02`）。`2026-07-04-02` の b2 主 mc-target=`26.1.2` は当時の戦術束縛として履歴に残し、本節の現行運用は floor-up に改訂する。b1 findings の b2 合流（world_constants 追従・CME 修正＝各リポ `protocol-21.0.0-b2` ブランチに既在）は `2026-07-04-01` を参照（本スコープに先行合流済み）。

**【核（b2 完了ゲート直結）】**

1. 認証実装: pair フロー（pair_begin → 6桁 pair_code → /mcremote pair → UUID 確定 → session_token / player_token 発行）。正本は plugin、bridge は透明中継。**wire 形の正本＝wire §6.5**（poll トポロジ・`auth.*` 名前空間・reason enum を確定 `2026-07-04-06`）。
2. hello の auth フィールド具体化 → hello ペイロード全体を ratify（wire §6 の残起案解消）。named object への非破壊フィールド追加であり封筒変更なし。
3. エラーコードの認証/認可分離（TOKEN_EXPIRED/REVOKED/NOT_FOUND/INVALID → token 破棄・再ペアリング / PERMISSION_DENIED → token 温存・操作拒否）。
4. LuckPerms 連携（mcr.online / mcr.offline / mcr.build.range、認可は常に UUID → LuckPerms、不在時フォールバック分岐を保持）。
5. auth enforcement トグル（plugin config）: 検証実装と強制を分離し、開発中は未強制で3リポ（plugin / python / scratch）が非同期に着地できるようにする。トグル ON が b2 完了ゲート。リリース既定値は enforced（R2「認証必須へ一斉切替」と整合、トグルは開発順序の道具）。
6. Scratch を能動参加させる（b2 は3リポ足並み）: 接続ブロック・ペアコード表示・ペアリング完了ハット・localStorage token・認証系エラーでの token 破棄→再ペアリング。Scratch の接続先選択は、作品に保存されるブロック引数ではなくブラウザ実行環境の GUI 設定として扱う。一般導線では `[マインクラフトに接続]` のみを出し、旧 `[(sandbox) に接続]` 相当はデバッグ用 URL / 上級者導線に留める。b2 では固定プリセットの接続先メニュー、選択値保存、VM への現在 sandbox route 注入を最小範囲に含める。
7. 同一 UUID の並行セッション上限 = 16（決め打ち・plugin config で調整可）。

**【準核（核を人質に取らない切り離し可能単位）】**

8. player.getPos / player.setPos 新設（名前空間ドット名、API 層 camelCase 対応）。pair により「誰の位置か」が構造的に解決されるため b2 が設計上正しい配置。`player.getPos` は paired player の現在 world と現在位置を返し、座標はその stream の build origin 相対（result は `{world,pos:[x,y,z]}`）。`player.setPos` は明示 world と相対座標（wire params `[world,x,y,z]`）を受け、server が `absolute = stream.origin + relative` を計算して指定 world へ次元跨ぎ teleport する。`player.*` は stream.origin を共有するが stream.world には暗黙依存しないため、次元不一致（プレイヤー在次元 ≠ build world）論点は world 明示で解消する。権限は LuckPerms に委譲し、独自 teleport 権限体系は作らない。基本 reason は `permission_denied` / `player_offline` / `unknown_world` / `invalid_params`。これにより chat.post / setBlock / setBlocks / getBlock / player.getPos / player.setPos の入門語彙が揃い、b→rc の凍結対象語彙が b2 で完成する。
9. セッションライフサイクル定義を wire 仕様の一節（§6 隣接）として正式化: イベント（旗押し直し / 切断→再接続 / タブ複製 / ブラウザ再起動 / token 失効）× 層（identity / build state / プロジェクト保存）の挙動表。骨子＝identity は接続を跨ぐ（token 継続・再ペアリング不要）、build state は stream 個別で接続と共に死に再接続時は既定値から（プログラムから再導出可能ゆえサーバー復元しない）、保存は接続と無関係（token・接続状態・接続先はプロジェクトファイルに一切入らない）。接続ブロックは冪等（接続済みなら no-op で既存接続を再利用）。Scratch token は接続先別に保存し、認証系 reason では現在接続先の token だけを破棄し、`permission_denied` では温存する。Python は同一意味論の呼び出し規律として投影。**【2026-07-05 扉①（post-b2 種・DECISIONS `2026-07-05-02` / `2026-07-21-07`）】本節の文言は N≥1（main / substream の複数ストリーム）が自然に読める形にし「1クライアント=1ストリーム」へ固定しない。identity/build state/保存の層分けは N に非依存。**
10. WS close 時の _pending reject 修正（getBlock / getPos / setPos 等の切断ハング解消）。接続状態 UI の実装と同じ工事で回収する。
11. demo_00 に一度きりのペアリング設定セルを追加（R2 項目の消化）。
12. Bedrock/Geyser UUID 実機確認（pair 実装後1回通す、既存決定の実行タイミング固定）。

**【並行・軽量（protocol 非接触）】**

13. WireScope v0 = Scratch 接続パネルとして実装: 6桁ペアコード表示・接続状態インジケータ（未接続→pair待ち→接続→切断）・現在の接続先（表示名と sandbox route）・hello 応答情報（protocol / mc_version / world_constants / permissions）・自クライアントの送受信フレームログ。サーバ→クライアント async push には触れない（bN/debug 統合のまま）。「wire を覗く」教育アングルの最初の実物。**【2026-07-05 扉②（post-b2 種・DECISIONS `2026-07-05-02` / `2026-07-20-08` / `2026-07-21-07`）】フレームログ表示モデルにストリーム識別子欄を最初から持たせる（N=1 でも破綻せず main / substream へ前方互換）。接続状態は色だけに依存せず、アイコン・テキストを併用する。**

**【b3 送り】**

14. catalog 一式（catalogHash 実値化・plugin レジストリ書き出し・PC グローバルキャッシュ・catalog validator・Python kwargs 砂糖）。hub NOTES の「入力 API 形＝b2」マークは「catalog が来る段」の意味であり b3 に読み替える。
15. Scratch 旧 `.sb3` 読み込み不可 / 保存後 load 不可の GUI 互換修正。b2 では接続先 / token が `.sb3` に保存されないことを serialization smoke で確認し、旧ファイル互換・保存後再ロード互換は b3 の save/load 互換テストで扱う。

**【bN のまま】**

16. async error/log push / ライブ画面本格版（`2026-07-01-08` どおり）。
17. 逆方向ペアリング対策のデプロイ単位オプション（私有サーバー運用が R2 リリースに含まれるか確定した時点で再判断）。

**整合参照**（搬送票の根拠/検証欄より）: 本スコープは claude.ai サーフェスでの横断検討によるもので、検証不能な実装依存項目は含まない。実装量見積り・§7⑤権限既定値・catalog 書き出しコストは各リポ現場確認で裏取りする。既存決定との整合: §10.11（bN=認証）、`2026-06-27-05`（catalogHash 常在）、`2026-06-24-01`（build state=stream 個別）、`2026-07-01-08`（async push は bN）、`2026-06-26-01`（hello 残起案=auth）、scratch-plan（pair UX 設計済み）、R2 locked decisions。

### 10.11.2 b3を膨らませず、PoPをrelease gateから外す

b3の責務は§10.11.1項14のcatalog一式と項15のScratch `.sb3` save/load互換に維持する。credential lifecycle、DoS guard、PoPをb3へ混ぜない。

b3後の最優先は、公開betaを安全に運用するためのavailability sliceである。認証前connection / frame / timeout / pairing rateと、認証後session / inflight / queue / tick workload / backpressureを別々に実装・検証し、Cockpit、Paper同梱spark / spark API、McRemote metricで観測する。正規の大量建築やTNTを禁止せず、budget、tick分割、fairness、cancelでbounded degradationと回復を確認する。

長期`player_token`の公開導線は、hash-only永続store、device label、last-used、list / revoke、world rollbackからの分離、safe restoreが揃うsliceまで待つ。Pythonの明示CLI loginと非対話`Minecraft.create()`はこのlifecycleへ含める。Scratchは引き続きsession tokenのみを使う。

接続時PoPはb4 / rc / public betaの必須要件にしない。token文字列だけを別端末で再利用する攻撃へのhardeningとして、token漏洩実績、長期credentialの普及、高価値world等のtriggerが立った時に再評価する。全command署名、独自secure channel、native TLS、mTLS、WebAuthnも現在のbeta gateへ含めない。採用を決めるまでexact algorithm、公開鍵encoding、canonical signature input、challenge wire shapeを批准しない。

上記のavailabilityとcredential lifecycleを一つの大きな`b4`へ固定せず、公開previewにできるsliceごとに次の`bN`を切る。PoPを外したことを理由に長期bearer tokenを先行公開せず、lifecycle gateは独立に維持する（DECISIONS `2026-07-16-01` / `2026-07-16-03`）。

### 10.12 pre-release 状態は明示操作（自動認識は PyPI のみ）

版文字列から pre-release 状態が**自動認識される面**と、**明示操作が要る面**を分ける（DECISIONS `2026-06-25-06`）。§10.5／`2026-06-25-02` が core 番号＋接尾辞（PEP 440 `b1`）を揃える方針を選んだ帰結。

| 面 | pre-release の決まり方 | `2100.0.0b1` の扱い |
| --- | --- | --- |
| PyPI（api） | PEP 440 で**自動**。素 `pip` は既定で pre を拾わず `--pre` 必要 | 自動で pre-release 扱い ✓ |
| GitHub（plugin） | リリースオブジェクトの `prerelease` **明示フラグ**。`2100.0.0b1` は **SemVer として不正**（patch が数値でない）ため、タグ名を SemVer で判定する CI/Action を噛ませても pre とは判定されない | 自動では立たない＝**手動フラグ必須** |
| Modrinth（plugin） | version type / release channel（release/beta/alpha）が**明示フィールド**。版番号からは導出しない | channel を**明示指定** |

**運用律**：

- plugin の beta GitHub release は **`--prerelease` を明示**し、**Latest に出さない**。手動フラグが load-bearing で、立て忘れると GitHub が beta を Latest に選び初学者の更新チェッカが掴む（`2000.0.0` の失敗 `2026-06-25-03` と同型）。tag / artifact 名は §10.12.1。
- scratch-editor の beta tag は、b1 の既存 `scratch-editor-2100.0.0b1` は履歴として保持し、b2 以降は repo-local tag `v<mc-remote-version>` を使う。GitHub リリース時に **`--prerelease` を明示**し、**Latest に出さない**（DECISIONS `2026-07-02-04`、`2026-07-11-02`）。
- Scratch b2 の自動 CI は既存 workflow 権限不整合により job 開始前 `startup_failure` だったが、批准済み個別 test / deployment / smoke 証跡を根拠に b2 release は留保付き受理する。**次回 Scratch release は権限不整合を事前に解消し、release source に対する CI PASS を gate 必須条件とする**。b2 を `CI PASS` と遡及記録しない（DECISIONS `2026-07-11-03`）。
- 開発・運用体制がbootstrapの間、McRemote pluginのreleaseはGitHub release / JAR asset作成までとし、server deploymentをtag push / release workflowから分離する。beta環境はtag済みrelease assetを入力にする別工程とし、現在の`2100.0.0b2`を最初の対象にする。Modrinth / PyPI publishはcomponentのmature gate通過後に広げる（DECISIONS `2026-07-16-01`）。
- Modrinthへ出すbeta / rcは **`beta` channel**、stableは **`release` channel**を明示指定する。

自動認識を効かせるために SemVer ハイフン形（`2100.0.0-beta.1`）へ変える案は、**§10.5 で既に却下済み**（PyPI正規化で`b1`に畳まれ表示が割れ§2対称性が壊れる）＝結論は同じで、ここでは「自動認識のため」と動機が増えるだけ。GitHub prerelease flagもModrinth channelも版番号から自動導出せず、配布先ごとに明示する。

### 10.12.1 plugin の tag / release / artifact 名

plugin は Git tag / GitHub release title / JAR artifact 名を分離する（DECISIONS `2026-07-03-01`）。

| 面 | 形式 | 例 |
| --- | --- | --- |
| Git tag | `v<mc-target>-<mc-remote-version>` | `v26.2-2100.0.0b1` |
| GitHub release title | `McRemote <mc-target> / <mc-remote-version>` | `McRemote 26.2 / 2100.0.0b1` |
| JAR artifact | `mc-remote-<mc-target>-<mc-remote-version>.jar` | `mc-remote-26.2-2100.0.0b1.jar` |

`mc-target` は plugin が実際に対象にする Minecraft/Paper 系列で、確認票で固定する。これは単純な patch increment では推測しない。たとえば Paper 26.2 stable へ移る場合は `26.2` を使い、`1.21.11` の次を `1.21.12` として扱わない。

PythonAPI は repo-local tag `v<mc-remote-version>`（例 `v2100.0.0b2`）と package `minecraft-remote-api==<mc-remote-version>` を使う。Scratch editor も b2 以降は repo-local tag `v<mc-remote-version>` を使う。plugin だけは対応 MC バージョンを tag から特定する必要があるため、上表の `v<mc-target>-<mc-remote-version>` とする。scratch-editor b1 の `scratch-editor-2100.0.0b1` は既存 release identity として変更しない（DECISIONS `2026-07-11-02`）。

### 10.12.2 bN の mc-target 束縛（床値規則）

bN（beta）の mc-target は開発都合で**床値**（サポート対象範囲の最古版）に縛る。踊り場価値とは独立に選んでよい。mature後にbNをModrinth/PyPIへ出しても、目的を持ってexact-pinする公開previewであり、stableの無指定取得導線には乗らない。rc/stable の mc-target はリリース時判断とし、Paper の現況（stable 化状態、`F-paper-support-flags`）を参照して「床のまま出す」か「天井へ上げる」かを決める。方向は常に**床で開発・上へ移植**であり、下方移植を要する構え（天井で開発し後から床へ下げる）は取らない。DECISIONS `2026-07-04-04`。b2以降の現行適用は `1.21.11` / Java21 floor で進め、rc 前に最終リリース対象 MC バージョンを決める（`2026-07-08-02`）。`2026-07-04-02` の b2 mc-target=`26.1.2` は当時の戦術束縛として履歴に残す。

**なぜ床値か（3つの非対称）**：

- **方向の非対称**：床→天井の移植は加算的で、問題が deprecation 警告として早く見える。天井→床は減算的で「古い版に無い API・構造を知らずに踏む」がターゲットを下げた瞬間、リリース圧下で初めて発覚する。床値開発は最小サポート版で開発する古典的ライブラリ戦略と同型。
- **枝の非対称**：床に縛れば Paper の stable 化が早い/遅いどちらの枝でも詰まない。天井に留まると遅い枝で下方移植が発生する。
- **コストの非対称**：Java 21→25・ワールドデータ構造変化は 1.21.11 系↔26.x 系間のギャップであり 26.1.2↔26.2 間ではない＝床に縛るコストがほぼゼロで非対称の利益だけ取れる。リモコンの「ゆるい依存」（接触 API 6項目）が移植コストをさらに下げる。

版の時計（Mojang の四半期リズム `F-mojang-release-cadence`）は規則的だが Paper stable 化ラグ（`F-paper-support-flags`）は不規則ゆえ、二変数予測に依存せず床値規則で予測不要にする。`supported_mc_versions` は離散踊り場リスト（§5）＋当面1ビルド=1MC版（§7.1）なので、床束縛は後から天井版（例 26.2）対応を足すことを妨げない。

**開発の床 vs 配布の床（Java21↔25 境界への拡張）**：§10.12.2 の床値規則は mc-target 宣言（配布の床）の規則だが、1.21.11(Java21)↔26.x(Java25) のように JVM 互換が片方向に割れる境界では「開発の床」も固定する＝コードが依存してよい最小 API・Java を Java21/1.21.11 互換ベースラインに置く。Java21 バイトコードは JVM25 で動くが逆は不可（UnsupportedClassVersionError）ゆえ床開発の成果物のみ両系に届く。実装形は単一コードベース＝Java21 互換の共有コア＋薄い platform-paper アダプタで、必要なら mc-target ごとに artifact を分ける（mc-remote-1.21.11-<ver> / mc-remote-26.1.2-<ver> 等）。1.21.11 は凍結リリース（b1）とは別に active な床トラックとして維持を既定とし、ドロップは固定日付・固定版・固定トリガーを置かず毎リリースの都度判断（rc/stable の天井判断と同型）＝Paper 現況（F-paper-support-flags）・踊り場生態系現況・Java21 互換維持コスト・実利用を入力に畳む。b2以降は複数 MC トラックの並走確認を必須にせず、1.21.11 floor で機能を収束させ、rc 前の凍結判断で 1.21.11 / 26.1.2 / 26.2 / 複数 artifact のどれにするかを決める。Java21↔25 のギャップは mod 生態系にも効いて 1.21.x 踊り場を長命化させる公算が高く、維持既定はその想定に整合。backport は方向・土台・Java 互換の非対称ゆえ採らない。DECISIONS `2026-07-04-05` / `2026-07-08-02`。

### 10.13 他言語クライアントの pre-release（将来・作り込まない）

api はクライアントが今後増える（他言語・ブリッジ、`2026-06-25-04` 非対称成熟）。各言語レジストリは pre-release の**正準表記と判定機構が異なる**ため、`b1`（PyPI）を全クライアント共通表記と見なすと最初の非 PyPI クライアントで破綻する。原則だけ置き、設計は最初の非 PyPI クライアントが立つときに落とす（YAGNI）。

**不変条件（割れない部分）**：

- **core 番号 `2100.0.0` は全エコシステム共通**（安定版は同一文字列）。
- **相互運用は protocol（§3）で保証**＝pre-release 文字列が割れても interop は不変。
- SSOT は論理版（protocol N ＋ 段）＋ core 番号。pre-release 接尾辞は**各エコシステムのネイティブ表記でレンダリングする派生物**。

**pre-release 判定マトリクス（§10.12 の一般化）**：チャンネルは「文字列を強制するレジストリ」と「自由文字列＋明示フラグのサーフェス」に分かれる。

| チャンネル | 種別 | pre-release 表記 | pre 判定 |
| --- | --- | --- | --- |
| PyPI（Python） | レジストリ | `2100.0.0b1` | 自動（PEP 440） |
| npm（JS/TS） | レジストリ | `2100.0.0-beta.1` | 自動＋dist-tag |
| crates.io（Rust） | レジストリ | `2100.0.0-beta.1` | 自動（SemVer） |
| Maven（Java） | レジストリ | `2100.0.0-beta1`/`-RC1`（`-SNAPSHOT` は別物） | 概ね手動運用 |
| NuGet（.NET） | レジストリ | `2100.0.0-beta1` | 自動（ハイフンラベル） |
| RubyGems（Ruby） | レジストリ | `2100.0.0.beta1` | 自動（英字検出） |
| GitHub / Modrinth | サーフェス | 任意 | 明示フラグ／channel |

新クライアント追加時は、その言語のレジストリ行を確定し、`b1`／`-beta.1` 等の表記差は core 共通の派生レンダリングとして扱う（§10.12 の明示操作律も、自動判定が効かないレジストリ・サーフェスへ同じ形で適用）。
