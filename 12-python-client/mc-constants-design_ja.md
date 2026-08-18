# 【内部記録】mc_constants 自動生成アーキテクチャ ― 設計判断まとめ

> 用途: 次期開発セッション・リファクタリングのベース資料（内部用）。
> ユーザー向け説明は `python-client-guide_ja.md`（同ディレクトリ）を参照。

> **改訂履歴**：初版は「同梱した静的バージョン別ファイル群から import 時に生成する」設計だった。
> `2026-07-29-04` で catalog のデータ源が稼働中サーバー（`catalog.get`）へ移り、
> `2026-08-02-04` が `states` schema と signature 導出を、
> `2026-08-02-05` が projection lifecycle（**非同梱・接続後獲得**）を確定し、
> `2026-08-06-04` が PC グローバル cache の root path と優先順を確定した。
> `2026-08-19-02` はprotocol 22のblock値を`block_id`と`state`へ分離し、projectionを
> 文字列ref生成器でなくID／state入力支援として位置づけ直した。
> 本文は現行設計に更新済み。**旧設計に属する記述は残していない**が、
> 判断理由は §2 に「なぜ反転したか」として保存する。
> 公開利用面は`python-client-guide_ja.md`、block値の共通形は
> `10-protocol/block-value-design_ja.md`を正とする。

---

## 0. 全体像

定数は**稼働中サーバーの registry から取得して生成する**（projection）。
`param_mc_remote.py` は「設定専用」に純化し、機能（定数）は
接続後に生成される `mc_constants.py` に分離する。ライブラリは projection を同梱しない。

```text
(ユーザーの作業ディレクトリ = projection の生成先 = CWD)
├── param_mc_remote.py             # 生徒が設定（Git管理外）
├── param_mc_remote.template.py    # テンプレート（Git管理）
├── hello.py                       # 初回はここだけで成立する（mc_constants を import しない）
├── mc_constants.py                # projection（Git管理しない・接続後に生成）
└── mc_constants.manifest.json     # projection manifest（Git管理しない）

(PC グローバルキャッシュ)
└── ~/.cache/mcremote/             # XDG 未設定時の fallback。catalogHash キーで横断共有

(ライブラリ側)
└── mc_remote/
    ├── __init__.py
    ├── catalog.py                 # catalog.get・検証・BlockSpec入力支援
    ├── _constants_codegen.py      # projection generator
    └── minecraft.py / vec3.py
```

PC グローバル cache の root は `2026-08-06-04` により、次の優先順で解決する。

1. `$MCREMOTE_CACHE_DIR` が設定されていれば、その値。
2. 未設定なら `$XDG_CACHE_HOME/mcremote`。
3. `XDG_CACHE_HOME` も未設定なら `~/.cache/mcremote`。

旧 `~/.cache/mc-remote` を読書きする互換分岐や自動移行は設けない。catalog cache は公開 game／mod data であり、
credential store（`~/.config/mcremote`）とは directory と削除境界を分ける。

**同梱物は無い**（`2026-08-02-05`）。clone 直後は補完が効かず、
初回の認証済み hello を通してその環境がサーバーから補完能力を獲得する。
`.pyi` は b3 の生成物に含めない（「不要」ではなく Pylance 実測前のため未採用）。

---

## 0.1 `param_mc_remote.py` を分離する理由（environment adapter）

> **役割の明示（`2026-08-03-01`）**：これは「古い設定ファイル」ではなく **environment adapter** である。
> プログラム本体を環境を越えて共有可能にし、同じコードをディレクトリごとに異なる接続先・建築原点で使え、
> 接続先という環境固有値を共有コードへ直接書かず、private な接続先を Git へ収容しない。
> `Minecraft.create(address="server.example", ...)` のように環境値をプログラム中へ直書きする形は教材例にしない。
>
> **現行 template の内容**＝`ADRS_MCR`（既定は公式 sandbox `sb.mc-remote.com`・公開値なので template に収容）／
> `PORT_MCR`／`BUILD_ORIGIN`。**`PLAYER_NAME` と `PLATFORM` は削除**（前者は identity が pairing で確定＝`2026-06-15-02`、
> 後者は版と registry が hello と catalog で確定＝`2026-08-02-05`）。**旧 `PLAYER_ORIGIN` は `BUILD_ORIGIN` へ改名**
> ＝build model は `setBuildOrigin` / `build.setOrigin` に確定済みで（`2026-06-25-01` / `2026-06-26-04`）、
> `setBuildOrigin(PO.x, ...)` の `PO` が `PLAYER_ORIGIN` だと1行に同じ概念の2つの呼び名が出る。
>
> **現物の所在**＝`param_mc_remote.template.py` は dev repo `minecraft-remote-api`（commit `99adef5d` 時点）に存在しない。
> historical reference は `mc-remote-knowledge-archive/12-python-client/reference/param_mc_remote.template.py` にあるが
> `PLAYER_NAME` と `PLATFORM` を含み失効している。archive 版をそのまま復活させず、役割を維持して内容を現代化する。



`param_mc_remote.py`（gitignore・個人コピー）と `param_mc_remote.template.py`
（Git管理・追従可）を分ける根拠は次の2点。**プレイヤー名の保護ではない**
（identity は pair で確定するため `PLAYER_NAME` はコードに書かない。
DECISIONS `2026-06-15-02` / `2026-06-19-01`）。

1. **非Sandbox のサーバー名/IP を GitHub に上げない。** 既定の `sb.mc-remote.com`
   （Sandbox・公開）はテンプレに入れてよいが、クラス用・自宅サーバー等の非公開
   アドレスは秘密。それを書いた個人コピー（param）を gitignore で守る。
2. **`git pull` 衝突の回避。** param はユーザーが環境ごとに書き換える設定
   （接続先・`PLATFORM`）。テンプレと個人コピーを分ければ、upstream 更新が
   個人の編集を上書き・衝突させない。

認証 token は param に入れない。保存先はクライアント形態で異なる
（Python/CLI = `~/.config/mcremote/`、Scratch = ブラウザの `localStorage`。
ブラウザは FS に触れないため localStorage 一択）。
token の保存先は credential policy の一部であり、constants artifact へ埋め込まない。client 実装側で接続先ごとに分離し、project file や生成 constants へ保存しない。

---

## 1. 決定事項一覧（結論）

| # | 項目 | 決定 | 理由 |
| --- | --- | --- | --- |
| 1 | 定数の渡し方 | **値を直接埋めた自己完結形**（`2026-08-02-05`。旧「re-export 方式」は前提消滅） | データが wire から来るため re-export する元ファイルが存在しない。平坦なモジュールレベル代入なら補完は効く（§2.1） |
| 2 | 生成先パス | **CWD 一本化** + `sys.path.insert(0, target_dir)`。project 探索規則は新設しない | 全実行形態で「いま居る場所」に生成し、読み込みも保証（§2.2 は現行のまま有効） |
| 3 | VS Code 再生ボタン | `.vscode/settings.json` に `executeInFileDir: true` | CWDをファイル位置に固定。階層が深いと実行できない既存問題も解消 |
| 4 | VS Code デバッガ | `.vscode/launch.json` に `cwd: ${fileDirname}` | 再生ボタンとデバッガで生成先を一致させる |
| 5 | デフォルト版 | **持たない**（`2026-08-02-05`。旧「1.21.11 を既定として同梱」を廃止） | catalog が稼働中サーバー由来になり、同梱版は実サーバーを代表しない |
| 6 | `mc_constants.py` のGit | **`.gitignore` する**。同梱もしない（`2026-08-02-05` で旧決定を反転） | 補完が効かない状態そのものを接続への入口にする教材設計。失っているのではなく得ている（§2.3） |
| 7 | フォールバック | **持たない**（旧「カテゴリ別に要求以下で最新」は前提消滅） | catalog は `catalog.get` が block / entity / particle を一括で返す。版を跨いで探す対象が無い（§2.4） |
| 8 | 生成物の素性 | **projection manifest** に記録（`catalogHash` / projection key / generator version / projection schema version / `artifacts` の `sha256`） | 旧「ヘッダーに fallback 内訳を明記」の後継。再生成判定と改竄・欠損検出を兼ねる |
| 9 | 生成物が無い場合 | **生成しない**。代替版へフォールバックしない | 接続前に補完が無いことは正常な状態。偽の定数を置くと誤情報になる |
| 10 | Jupyter キャッシュ | **カーネル再起動**をガイド（コード側は reload で緩和） | キャッシュクリアより簡単・確実 |
| 11 | mcpi / 1.13未満 | **先送り**。コアは共通化、拡張手順を文書化 | 数値ID・座標系・APIが相当異なる。枠だけ残さない |
| 12 | `.pyi` | **b3 では生成しない**（`2026-08-02-05`） | 「不要」ではなく「実現可能だが Pylance 実測前なので未採用」。state 補完 prototype として後続スライス |
| 13 | ignore の供給 | starter template または明示的な project init が設置する。generator は `.gitignore` を暗黙編集しない | 非同梱は ignore が実際に効いて初めて成立する（§2.5） |

---

## 2. 検討経緯（なぜそうしたか）

### 2.1 補完（IDE）の扱い ― 平坦な代入で足りる

- 当初「`as` エイリアス越しの属性補完は効かない場合がある」と懸念したが、
  **モジュールレベルのベタ書き代入なら Pylance が `block.GOLD_BLOCK` を補完できる**という実績により撤回。
- **この実測結果は現行設計でも生きている**。projection が平坦な代入である限り、
  **ブロック名の補完は `.py` 単独で効く**。
- したがって `.pyi` が買うのは **state 補完だけ**（どの property を持つか・どんな値を取るか）で、
  ブロック名補完には寄与しない。b3 で `.pyi` を出さない判断（決定 #12）はここに立脚する。
  加えて **stale な `.pyi` は静的解析で `.py` より優先される**ため、
  残存すると実行時 API と静的表示が黙って食い違う。
- re-export（`import vX_Y_Z as block`）そのものは前提が消えた。
  catalog が wire から来る以上、re-export する元のバージョン別ファイルが存在しない。

### 2.2 生成先パス ― 「正解の1パス」を当てにいかない

- `sys.path[0]` / `sys.argv[0]` / `os.getcwd()` はいずれも
  REPL・Jupyter・pytest・デバッガのどこかで期待とズレる。
- 「賢く当てる」方向は例外が増え続けるため放棄。
- 方針: **生成先は CWD に固定**し、「生成した場所が読めること」を
  `sys.path.insert(0, cwd)` で**能動的に保証**する。(A)書き出し先と(B)読み込み解決を分離。
- 各環境での CWD は `.vscode` 設定（再生ボタン/デバッガ）で固定し、
  Jupyter はノートブック位置=CWD（通常）+ reload/再起動ガイドで吸収。

### 2.3 同梱の反転 ― 失っているのではなく得ている

事実関係は変わっていない。`sys.path.insert` は**実行時**の解決にのみ有効で、静的解析には効かない。
したがって clone 直後に補完を効かせたければ、何かを同梱するしかない。

旧設計はこの理由で「デフォルト版 `mc_constants.py` を同梱し Git 管理する」を選んだ。
現行はこの利益を**意図的に手放す**（`2026-08-02-05`）。

- catalog が稼働中サーバー由来になった以上、同梱版は**実サーバーを代表しない**。
  同梱してもそれは「どこかのサーバーの過去の姿」で、
  接続先の mod 構成が違えば誤った候補を出す。
- 補完が効かない状態そのものが、**「まず接続せよ」という入口**になる。
  Hello World → hello 成功 → catalog 取得 → projection 生成 → 補完が現れる、
  という状態変化を通して、接続・hello・catalog の関係を学習可能にする。
- **これは fallback 不足ではなくカリキュラム設計**。失っているのではなく得ている。

代償として、初回の教材導線は補完なしで書けなければならない。
**初回 Hello World は `mc_constants` を import せずに成立する**構成にする（決定 #6・`2026-08-02-05` ⑤）。

### 2.4 版跨ぎフォールバックの消滅

旧設計では block がほぼ全バージョン、entity/particle が飛び飛びという
**同梱ファイルの揃い方の非対称**があり、カテゴリごとに「要求以下で最新」を選ぶ必要があった。

現行では `catalog.get` が block / entity / particle を**単一 response で一括**して返す（wire §7.2.1）。
3カテゴリは常に同じ `catalogHash` に属し、揃い方の非対称が存在しない。
版を跨いで探す対象も無い（探索先は接続中のサーバーだけ）。
したがって `_select_version` 相当のフォールバック機構は不要になった。

**「上に丸めない」等のフォールバック仕様上の注意点も消滅**した。
接続先が持っていないブロックは、補完に出ないだけでなく、
実際に使えば server が `unknown_block` を返す（wire §7.3）＝正しい失敗になる。

### 2.5 ignore 供給 ― 方針は設定が効いて初めて成立する

「非同梱・Git 管理外」は文書上の宣言では成立しない。`.gitignore` が実際に効いて初めて成立する。

- リポジトリ自身の `.gitignore` は、**そのリポジトリ内で生成した場合しか保護しない**。
  生徒が別ディレクトリで始めたプロジェクトには伝播しない。
- 効かなければ生徒が `mc_constants.py` を commit し、
  それを clone した別の生徒は**接続せずに補完を得る**。
  しかも中身は別サーバー由来かもしれない。設計の柱が静かに崩れる。

したがって b3 では次のどちらかを実在させる（`2026-08-02-05` ⑨）。

- **公式カリキュラム経路**＝starter template に ignore 規則を同梱する。
  生徒の最初の操作は init ではなく Hello World のままにできる。
  starter が持つのは `param_mc_remote.template.py`・ignore 規則・**定数 import をコメントアウトした `hello.py`**・
  接続後に補完を使う次段階のサンプル。`mc_constants.py` と manifest は含めない（`2026-08-03-01` ⑤）。
  **starter の存在自体が b3 完了条件**（`2026-08-02-05` ⑨）。
  なお `mc_remote_samples` は入口として近いが `setPlayer` / `PLAYER_NAME` / 静的 `block_id` / 旧 sandbox 説明を含むため、
  現状のまま公式 starter として案内しない。
- **一般経路**＝任意の空ディレクトリから始める利用者向けに、
  明示的で冪等な project init を提供する。既存 `.gitignore` を上書きせず、必要な規則だけを追加・検証する。
  `mcremote init` は commit `99adef5d` 時点で実在し、ignore 規則の冪等追加を行う。
  **`init` が template まで生成するかは任意の拡張**で、b3 の条件ではない（`2026-08-03-01` ⑤）。

**generator が実行時に `.gitignore` を無断編集してはならない。**
Git 管理下なのに ignore 設定が無い場合は、接続自体は成功させたうえで
projection を作らず、init を促す actionable warning を出す。
この失敗で接続・Hello World・建築を止めない。

### 2.6 mcpi / 1.13未満の先送り

- mcpi は数値ID・Y座標系・API が Java版と大きく異なる。
- 1.13（平坦化）境界も同様にブロックID体系が激変する。
- 当面サポートは**平坦化後（1.13以降）の1系統のみ**。
- 旧版コードにあった mcpi 専用バイパス分岐は**一旦コアから外す**
  （動かないコードパスを抱えない）。
- ただし**コアロジック（生成・`sys.path` 保証・world_info 計算）は共通化**したまま維持する。
  バージョン探索は現行では不要（§2.4）。

---

## 3. 既知の注意点・残課題

- **import順序依存**: `mc_remote` を `mc_constants` より先に import する必要がある。
  自動整形（isort等）で並べ替えられると壊れる。ユーザーガイドで注意喚起済み。
  将来、`mc_remote` 側から `block` を直接提供するAPIを足せば順序依存を消せるが、
  補完の都合（実ファイル経由）とトレードオフになるため現状は据え置き。
- **world_info の境界判定**: 現状は 1.18 境界のみ。1.13未満を将来サポートする際に
  要拡張（`_calculate_world_info` の else 節は当面到達しない）。
- **pytest のCWD**: 通常リポジトリルート。テストで固定 PLATFORM を使う想定なら
  問題化しにくいが、生成物がルートに出る点は留意。
- **stale shadow の防止**: checksum は検出材料であって防止手段ではない。
  生成物を同一 generation として stage する／manifest を最後に置換する／
  manifest 外または checksum 不一致の生成物を放置しない／更新失敗時に新旧を混在させない、
  の4点を契約として守る（`2026-08-02-05` ⑧）。将来 `.pyi` を足したときに効く。
- **並行生成**: 同一 project に対する projection 生成は project-local lock で直列化する。
  中断・不整合を検出したら次回 hello で再生成する。生成失敗時に前回の正常な projection を
  上書き・削除しない。
- **一プロジェクト一バージョン**: 有効な projection は project に1組だけ。
  ただし**この制約は補完にのみ掛かり、実行時の接続先は制約しない**。
  別 `catalogHash` のサーバーへ接続すれば projection を切り替える。
  前回 hash と現在 hash が異なる場合は stale であることを明示警告する。
- **state 補完の実現可能性**: `.pyi` 採用可否を決めるには
  **state signature の異なり数**（`2026-08-02-04` の導出規則による）、stub サイズ、
  解析時間、補完遅延の実測が要る。異なり数が小さければ静的型は安く手に入り、
  大きければ維持不能と結論できる。どちらに転んでも判断がつく測定として先に行う。
  protocol 22の実行時escape hatchは文字列`block_state_ref`でなく、
  `state: Mapping[str, str | int | bool]`である。Python identifierにできないmod propertyも
  mappingのkeyとして保持し、`block_id`とstateを再結合しない。
- **将来のmcpi統合**: 数値ID対応・座標系の差異吸収・setBlock等のAPI差異を
  別途設計する必要がある。本改修のスコープ外。

---

## 4. 拡張手順メモ

**新しい Minecraft バージョンへの対応は不要**になった。projection は接続先の registry から
生成されるので、サーバーが新版になれば `catalogHash` が変わり、次回 hello で作り直される。
ライブラリ側に足すファイルは無い。

手を入れる必要があるのは次の場合だけ。

1. **generator の出力形を変える**とき（`.pyi` の追加、型注釈の付与等）。
   projection schema version を上げる。同じ catalog でも全プロジェクトで再生成される（決定 #8）。
2. **world_info の値が変わる境界**を足すとき。現状は 1.18 境界のみ。
3. **mcpi など別体系**を足すとき。`_calculate_world_info` にバイパスを再導入し、
   `param_mc_remote.template.py` の選択肢コメントを開放する。
   コア（生成・`sys.path` 保証・manifest）はそのまま流用できる。
   ただし mcpi には `catalog.get` に相当する registry 取得が無いため、
   projection の入力源そのものを別途設計する必要がある。
