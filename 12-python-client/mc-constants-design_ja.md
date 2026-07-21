# 【内部記録】mc_constants 自動生成アーキテクチャ ― 設計判断まとめ

> 用途: 次期開発セッション・リファクタリングのベース資料（内部用）。
> ユーザー向け説明は `python-client-guide_ja.md`（同ディレクトリ）を参照。

---

## 0. 全体像

`minecraft-remote-api` を改修し、`PLATFORM` 指定に応じてブロックID等の定数を
動的に切り替える機構を導入する。`param_mc_remote.py` は「設定専用」に純化し、
機能（定数）のインポートは自動生成される `mc_constants.py` に分離する。

```text
(ユーザーの作業ディレクトリ)
├── param_mc_remote.py      # 生徒が設定（Git管理外）
├── param_mc_remote.template.py  # テンプレート（Git管理）
├── hello.py
└── mc_constants.py         # 自動生成（Git管理する／同梱する）

(ライブラリ側)
└── mc_remote/
    ├── __init__.py         # import時に _loader を起動
    ├── _loader.py          # 生成ロジック・バージョン選択・world_info計算
    ├── minecraft.py / vec3.py
    └── mc_constants/
        ├── block/    v1_21_11.py, v1_20_1.py, ...（ほぼ全バージョン）
        ├── entity/   v1_21_5.py, ...（飛び飛び）
        └── particle/ v1_21_5.py, ...（飛び飛び）
```

---

## 0.1 `param_mc_remote.py` を分離する理由（テンプレ＋gitignore）

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
| 1 | 定数の渡し方 | **re-export 方式**（`import vX_Y_Z as block`）を維持 | 現行で補完が効いている実績あり。実体ベタ書き展開は不要 |
| 2 | 生成先パス | **CWD 一本化** + `sys.path.insert(0, target_dir)` | 全実行形態で「いま居る場所」に生成し、読み込みも保証 |
| 3 | VS Code 再生ボタン | `.vscode/settings.json` に `executeInFileDir: true` 同梱 | CWDをファイル位置に固定。階層が深いと実行できない既存問題も解消 |
| 4 | VS Code デバッガ | `.vscode/launch.json` に `cwd: ${fileDirname}` 同梱 | 再生ボタンとデバッガで生成先を一致させる |
| 5 | デフォルト版 | **1.21.11**（`_loader` のデフォルトも同値） | 1.21 系の最終・安定版 |
| 6 | `mc_constants.py` のGit | **`.gitignore` しない**。デフォルト版を同梱 | クローン直後から補完が効く。diff が学習上むしろ有用 |
| 7 | フォールバック | **カテゴリ別**に「要求以下で最新」を選択 | block と entity/particle でファイルの揃い方が違うため |
| 8 | フォールバック内訳 | 生成ファイルの**ヘッダーに明記** | 「block だけ別バージョン」の混乱を防ぐ。diff も読める |
| 9 | 最低保証 | ファイル皆無時は `v1_21_11` へ | 旧版の `replace('.', '_')` は不正ファイル名→ImportErrorだった |
| 10 | Jupyter キャッシュ | **カーネル再起動**をガイド（コード側は reload で緩和） | キャッシュクリアより簡単・確実 |
| 11 | mcpi / 1.13未満 | **先送り**。コアは共通化、拡張手順を文書化 | 数値ID・座標系・APIが相当異なる。枠だけ残さない |

---

## 2. 検討経緯（なぜそうしたか）

### 2.1 補完（IDE）の扱い ― re-export で十分

- 当初「`as` エイリアス越しの属性補完は効かない場合がある」と懸念したが、
  **現行構成（`import mc_remote.block_id as block`）で補完が効いている**実績により撤回。
- 参照先（`vX_Y_Z.py`）がモジュールレベルのベタ書き代入なら、Pylance は
  インストール済みパッケージを解決して `block.GOLD_BLOCK` を補完できる。
- 新版の `from mc_remote.mc_constants.block import v1_21_11 as block` も同じ理屈で効く。
  → **実体ベタ書き展開や .pyi スタブ生成は不要**。re-export を維持する。

### 2.2 生成先パス ― 「正解の1パス」を当てにいかない

- `sys.path[0]` / `sys.argv[0]` / `os.getcwd()` はいずれも
  REPL・Jupyter・pytest・デバッガのどこかで期待とズレる。
- 「賢く当てる」方向は例外が増え続けるため放棄。
- 方針: **生成先は CWD に固定**し、「生成した場所が読めること」を
  `sys.path.insert(0, cwd)` で**能動的に保証**する。(A)書き出し先と(B)読み込み解決を分離。
- 各環境での CWD は `.vscode` 設定（再生ボタン/デバッガ）で固定し、
  Jupyter はノートブック位置=CWD（通常）+ reload/再起動ガイドで吸収。

### 2.3 Pylance（静的補完）は実行時挿入では効かない

- `sys.path.insert` は**実行時**の解決にのみ有効。静的解析には効かない。
- → クローン直後の補完・赤線解消のため、**デフォルト版 `mc_constants.py` を同梱**する。
  これが #6（gitignoreしない）の根拠。

### 2.4 カテゴリ別フォールバック ― ファイルの揃い方の非対称性

- block はほぼ全バージョンあり、entity/particle は変化が少なく飛び飛び。
- `_select_version` を**カテゴリディレクトリごとに**呼ぶことで、
  各カテゴリが独立に「要求以下で最新」へフォールバックする。
- 結果として生成ファイルは「block=v1_21_11 / entity=v1_21_5」のように
  カテゴリで別バージョンを指すことがある。→ ヘッダーに内訳を明記（#8）。

### 2.5 mcpi / 1.13未満の先送り

- mcpi は数値ID・Y座標系・API が Java版と大きく異なる。
- 1.13（平坦化）境界も同様にブロックID体系が激変する。
- 当面サポートは**平坦化後（1.13以降）の1系統のみ**。
- 旧版コードにあった mcpi 専用バイパス分岐は**一旦コアから外す**
  （動かないコードパスを抱えない）。
- ただし**コアロジック（バージョン探索・生成・world_info計算）は共通化**したまま維持し、
  将来は「定数ファイルを1枚追加 + world_info に分岐を1つ追加」で拡張できる構造にする。

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
- **フォールバックは「最近傍」ではなく「要求以下で最新」**: 例えば block に
  `v1_21_11` と `v1_20_1` しか無い状態で `PLATFORM="1.21.8"` を指定すると、
  1.21.8 ≤ の最新は `v1_20_1` になる（1.21.11 は要求より新しいので選ばれない）。
  block はファイルが密なので実害は出にくいが、「上に丸めない」点は仕様として認識しておく。
  もし「直近の上位版に丸めたい」要件が出たら nearest-neighbor へ変更する余地あり（現状は不要）。
- **将来のmcpi統合**: 数値ID対応・座標系の差異吸収・setBlock等のAPI差異を
  別途設計する必要がある。本改修のスコープ外。

---

## 4. 拡張手順メモ（将来 新バージョン/旧系統を足すとき）

1. 対応する定数ファイルを追加する。
   - 例: 新しいJava版 → `mc_remote/mc_constants/block/vX_Y_Z.py` を追加。
   - entity/particle は変化があったバージョンのみ追加すればよい（無い分はフォールバック）。
2. world_info の値が変わる境界なら `_calculate_world_info` に分岐を1つ足す。
3. mcpi など別体系を足す場合は、`_select_version` / `_calculate_world_info` に
   バイパスを再導入し、`param_mc_remote.template.py` の選択肢コメントを開放する。
   コア（生成・sys.path保証）はそのまま流用できる。
