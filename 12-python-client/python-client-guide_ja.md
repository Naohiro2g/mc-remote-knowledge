# マイクラリモコン　セットアップと使い方ガイド

このガイドは、マイクラリモコン（Python版）を使い始めるための手順と、
よくあるつまずきの解決方法をまとめたものです。対象は初めてプログラミングをする方も含みます。

> ## ⚠ この文書は現行設計と食い違っています（2026-08-02 時点・本文未改訂）
>
> **この文書を根拠に実装しないでください。** 次の2点が失効しています。
>
> 1. **定数ファイルの作られ方**（§2 / §3 / §4 / §6 / §7）。`2026-08-02-05` で
>    「既定版を同梱し、`import mc_remote` の瞬間に生成する」から
>    **「同梱せず、認証済み hello の成功後に生成する」**へ改訂されました。
>    `PLATFORM` でバージョンを選ぶ仕組みも、カテゴリ別フォールバックも、
>    生成物を Git に含める方針も、いずれも現行ではありません。
> 2. **プレイヤーの特定方法**（§1 / §7）。`2026-06-15-02` で identity は
>    pair により確定するようになり、`PLAYER_NAME` をコードに書く前提は失効しています。
>
> 現行の正本は [mc-constants-design_ja.md](mc-constants-design_ja.md)、
> wire 契約は [10-protocol/wire-format-design_ja.md](../10-protocol/wire-format-design_ja.md) §7.2 / §7.2.1 です。
>
> 本文の改訂は、`minecraft-remote-api` dev リポの実装事実を確認票で固定してから行います
> （`00-hub/NOTES_ja.md` 2026-07-22 の未了2件）。knowledge 側の設計文書だけで
> 推測修正すると、生徒が読む文書に未検証の手順を載せることになるためです。

---

## 1. はじめてのセットアップ

> **⚠ 一部失効**：`PLAYER_NAME` は書きません（`2026-06-15-02`＝identity は pair で確定）。
> `PLATFORM` も、同梱された版から選ぶ設定ではなくなりました（`2026-08-02-05`）。
> **template をコピーする手順そのものは残ります**（`2026-08-03-01`）＝`param_mc_remote` は
> 「プログラム本体を環境を越えて共有可能にする」ための environment adapter で、
> ディレクトリごとに接続先と建築原点を持ち、private なアドレスを Git へ入れない役割を担います。
> 現行 template が持つのは `ADRS_MCR`（既定は公式 sandbox）・`PORT_MCR`・**`BUILD_ORIGIN`**（旧 `PLAYER_ORIGIN`）。
> 公式 sandbox を使うならコピー後の変更は不要です。
> 本文の手順の書き直しは、starter に template が実在してから行います。

### 手順

1. リポジトリをクローン（またはダウンロード）します。
2. `param_mc_remote.template.py` をコピーして、`param_mc_remote.py` という名前で保存します。

   ```bash
   cp param_mc_remote.template.py param_mc_remote.py
   ```

3. `param_mc_remote.py` を開き、自分の環境に合わせて書き換えます。
   - `PLAYER_NAME` … Minecraft内でのあなたのプレイヤー名
   - `PLATFORM` … 使うMinecraftのバージョン（初期値は `"1.21.11"`）

`param_mc_remote.py` は Git管理の対象外（`.gitignore`）です。
プレイヤー名や接続先を書いても、誤って公開される心配はありません。

---

## 2. プログラムの書き方（import の順序）

> **⚠ 失効**：`import mc_remote` の瞬間に `mc_constants.py` が作られる、という前提が変わりました。
> 現行では**認証済み hello が成功した後**に生成されます（`2026-08-02-05`）。
> したがって初回は `mc_constants` が存在せず、**最初のプログラムは `mc_constants` を import せずに書きます**。
> import 順序の注意自体が残るかどうかも、実装確認後に判断します。

マイクラリモコンでは、`import` の順序が大切です。次の順で書いてください。

```python
import param_mc_remote as param
from param_mc_remote import PLAYER_ORIGIN as PO

# ★必ず先に mc_remote をインポートする
from mc_remote import Minecraft

# ★その後で、自動生成された mc_constants から定数を読む
from mc_constants import block, world_info
```

### なぜこの順番なのか

`from mc_remote import Minecraft` を実行した瞬間に、いま作業しているフォルダに
**`mc_constants.py`** という定数ファイルが自動で作られます（または更新されます）。

`from mc_constants import block` はこのファイルを読むので、
**先に `mc_remote` を読んでおく必要がある**のです。

> エディタの自動整形（import の並べ替え）を使っていると、この順序が崩れて
> エラーになることがあります。並べ替え機能はオフにしておくと安心です。

---

## 3. `mc_constants.py` ってなに？

> **⚠ 失効**：以下の説明は旧設計のものです。
>
> **実装で確認済み（2026-08-02 監査）**：`PLATFORM` は現行実装に存在せず、版選択にも fallback にも使われません。
> `block` / `entity` / `particle` は接続先サーバーから**一括で取得**されるため
> 「entity だけ少し前のバージョンで代替」は起きません。このファイルは
> リポジトリの `.gitignore` により **Git に含まれません**。
>
> **決定済みだが未実装**：ヘッダーの内訳を **projection manifest**（別ファイル）へ移すことは
> `2026-08-02-05` で確定していますが、監査時点で manifest は生成されていません。
> 「いまどのバージョンか」を manifest の `catalogHash` で見る運用は、実装後に有効になります。

`PLATFORM` で指定したバージョンに合わせて、ブロックIDや高さの定数を
自動でそろえてくれるファイルです。中身の例：

```python
# ==========================================
# このファイルは mc_remote によって自動生成されました。
# 編集しないでください（PLATFORM を変えて再実行すると上書きされます）。
#   PLATFORM = "1.21.11"
#   block   : v1_21_11  (完全一致)
#   entity  : v1_21_5   (1.21.11 の定義が無いため直近版で代替)
#   particle: v1_21_5   (1.21.11 の定義が無いため直近版で代替)
# ==========================================
...
```

- **このファイルは自分で編集しないでください。** 実行のたびに自動で作り直されます。
- `block` はほぼ全バージョン分そろっていますが、`entity` や `particle` は
  変化が少ないため、少し前のバージョンで代替されることがあります（上の例の通り）。
  通常はこれで問題なく動きます。
- このファイルはGitに含まれます。`PLATFORM` を変えて実行すると中身が変わるので、
  「いまどのバージョンの定数を使っているか」が diff で見えます。

---

## 4. 入力補助（補完）について

> **⚠ 失効**：デフォルト版の同梱は `2026-08-02-05` で**廃止**されました。
> クローン直後は補完が効きません。これは不具合ではなく意図した設計で、
> 最初の接続（Hello World）を成功させることで、その環境がサーバーから補完を獲得します。
> 補完が出ないときは「まだ一度も接続していない」というサインです。

VS Code などで `block.` まで入力すると、そのバージョンに存在するブロックIDが
候補として表示されます。

クローンした直後から補完が効くように、デフォルト版（1.21.11）の `mc_constants.py` を
あらかじめ同梱しています。`PLATFORM` を変えて一度実行すると、その新しいバージョンに
合わせた補完に切り替わります。

---

## 5. VS Code を使うときの設定（同梱済み）

このリポジトリには `.vscode/` フォルダが含まれており、次の2つが設定済みです。

| ファイル | 役割 |
| --- | --- |
| `settings.json` | 右上の**再生ボタン**で実行したとき、実行フォルダをファイルの場所に合わせる |
| `launch.json` | **デバッガ（F5）**で実行したとき、実行フォルダをファイルの場所に合わせる |

この設定があるおかげで、`examples/` のような深い階層にあるスクリプトでも、
そのフォルダに `mc_constants.py` が作られ、正しく読み込めます。

> 以前、フォルダの階層が深いと実行できない、というつまずきがありました。
> この設定でその問題は解消されます。クローンしたまま使えば自動で有効になります。

---

## 6. Jupyter Notebook を使うときの注意

Jupyter は一度読み込んだ `mc_constants` を**記憶（キャッシュ）**します。
そのため、`PLATFORM` を変えてセルを実行し直しても、
**前のバージョンのまま**になることがあります。

### 解決方法

`PLATFORM` を変えたら、**カーネルを再起動**してください。
（メニューの「Kernel」→「Restart」）。これが一番簡単で確実です。

再起動後、最初から順にセルを実行すれば、新しい `PLATFORM` が反映されます。

---

## 7. 困ったときは

> **⚠ 一部失効**：`PLATFORM` を変えて反映させる行と、`PLAYER_NAME` を確認する行は
> 現行では成立しません。`from mc_constants import ...` の赤線は「まだ一度も**接続**していない」
> が現行の原因で、対処は「スクリプトを一度実行する」ではなく「一度サーバーへ接続する」です。

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `from mc_constants import ...` が赤線／エラー | まだ一度も実行していない | 先に一度スクリプトを実行する。VS Codeなら再生ボタン |
| `mc_constants.py` が変な場所に作られる | 実行フォルダがズレている | `.vscode` 設定が有効か確認。ターミナルなら `cd` でスクリプトのフォルダへ |
| `PLATFORM` を変えても反映されない（Jupyter） | カーネルのキャッシュ | カーネルを再起動する |
| プレイヤーが動かない／接続できない | `param_mc_remote.py` の設定 | `PLAYER_NAME` と `ADRS_MCR` を確認 |
| import の順番でエラー | 自動整形で並べ替えられた | `mc_remote` を `mc_constants` より先に書く |

---

## 8. 新プロトコル安定版の認証導線

> ## ⚠ この節は「将来の導線」です。現行の手順ではありません
>
> **`mcremote login` は実装されていません。** 以下のコマンドはいずれも現時点では実行できません。
> （2026-08-02 の監査時点では CLI 自体が存在しませんでしたが、commit `99adef5d` で
> `[project.scripts]` の `mcremote` が実装されました。ただし subcommand は **`init` のみ**で、
> `login` / `status` / `logout` / `devices` / `revoke` はまだありません。）
>
> **現行の正面入口は引数なしの `Minecraft.create()` です**（`2026-08-02-06`）。
> Scratch の［接続］に相当し、初回は pair code を表示して Minecraft 内での承認を待ちます。
> ログイン操作が別にあるのではなく、接続フローの中に認証体験が入っています。
> 非対話環境（CI・batch）では `pair=False` を明示し、pairing が必要なら即座にエラーを受け取ります。
> **TTY による自動判定は行いません**（Jupyter や IDE は TTY でなくても対話環境のため）。
>
> 本節のうち失効しているのは次の3点です。
>
> 1. `player_token` は `2026-08-02-01` で **long-lived credential**（`mcrl_`）へ改名されました。
> 2. 「hash-only 永続 store、last-used、device 別 list / revoke が完成してから既定にする」は
>    条件を3つしか挙げていません。正本は versioning-design §10.11.2 の6条件で、開放条件は
>    `2026-08-02-03` が持ちます。**現時点で gate は閉じており、Python の既定は `session` のままです。**
> 3. 「`Minecraft.create()` を非対話にする」は `2026-08-02-06` で改訂され、対話が既定になりました。
>
> 将来 CLI が実装された場合も、通常教材の前提ではなく補助導線（事前設定・CI への credential 供給・
> 認証障害の復旧・credential 一覧 / logout / revoke）に位置づけます。

Pythonの建築コードとログイン操作を分ける。installed CLIの正面名は`mcremote`とし、公式betaへ初めて接続する例は次の形にする。

```bash
mcremote login --channel beta
```

`--channel stable|beta|alpha`は公式接続先profileを選ぶ。packageのbeta版を選ぶ引数ではないため、裸の`mcremote login beta`は使わない。自前serverは明示的にhost / portを渡す。

```bash
mcremote login --host example.com --port 25575
```

CLIはpair code表示、Minecraft内での承認待ち、credential保存、hello確認までを行い、少なくとも`login / status / logout / devices / revoke`を持つ。継続利用するPython端末は、server側のhash-only永続store、last-used、device別list / revokeが完成してから長期`player_token`を既定にする。共有PC・一時利用は`mcremote login --channel beta --session`のように明示して短期`session_token`を使う。

通常の`Minecraft.create()`は非対話にする。credential未登録、期限切れ、revoke、store消失時に標準出力でpairを始めてblocking待ちせず、実行すべき`mcremote login ...`を含むactionable exceptionを返す。自動pairはtest / devの明示opt-inだけに残す。

credential storeは接続先profile / targetごとに分け、別channelや別Sandboxへtokenを黙って送らない。tokenをsource code、通常log、URL、sample repositoryへ書かない。現在のplayer tokenはbearer credentialであり、Proof of Possession用の端末鍵生成・keychain・challenge署名はこのrelease導線の必須条件にしない。

---

## 9. WireScope（b3後の計画）

> **この節は将来計画です。現行の `mcremote` には `wirescope` subcommand はありません。**

独立 WireScope は Scratch 版と Python 版で別々の UI app を作らず、共通の
`@mc-remote/live` web app を使う（`2026-08-06-03`）。Python 側は Scratch の b3 前先行実装が固定した
observer schema、security allowlist、lifecycle fixture、source adapter 契約へ b3 release 後に追従する。

入口は引数なしの次の形とする。

```bash
mcremote wirescope
```

Python adapter と local relay は、`Minecraft.create()` で成立した main stream 1件を初版の観察対象とし、
共通 WireScope app へ Scratch と同じ observer schema で渡す。schema は初版から `streams[]` を持ち、
将来の明示 substream API と複数 source／stream の検索・比較へ追加的に拡張できる形にする。
`1 stream = 1 connection = 1 build state` は維持し、target と stream の ID を同一化しない。

WireScope は初期段階では read-only である。`auth.*`、token、pair code、player UUID、credential 情報を
observer feed へ渡さず、history、grant、observer session を project file や local credential store へ
永続化しない。Python 追従の完成分は b4 へ同梱できるが、本決定だけで b4 blocker にはしない。
Scratch からの command 発行はさらに後段の予約であり、Python adapter や初期 read-only app へ
自動的に追加しない。
