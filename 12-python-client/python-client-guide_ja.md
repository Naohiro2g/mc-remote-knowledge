# マイクラリモコン　セットアップと使い方ガイド

このガイドは、マイクラリモコン（Python版）を使い始めるための手順と、
よくあるつまずきの解決方法をまとめたものです。対象は初めてプログラミングをする方も含みます。

---

## 1. はじめてのセットアップ

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

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `from mc_constants import ...` が赤線／エラー | まだ一度も実行していない | 先に一度スクリプトを実行する。VS Codeなら再生ボタン |
| `mc_constants.py` が変な場所に作られる | 実行フォルダがズレている | `.vscode` 設定が有効か確認。ターミナルなら `cd` でスクリプトのフォルダへ |
| `PLATFORM` を変えても反映されない（Jupyter） | カーネルのキャッシュ | カーネルを再起動する |
| プレイヤーが動かない／接続できない | `param_mc_remote.py` の設定 | `PLAYER_NAME` と `ADRS_MCR` を確認 |
| import の順番でエラー | 自動整形で並べ替えられた | `mc_remote` を `mc_constants` より先に書く |

---

## 8. 新プロトコル安定版の認証導線

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
