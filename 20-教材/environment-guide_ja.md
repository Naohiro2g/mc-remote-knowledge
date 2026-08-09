# 教材の実行環境前提（生徒・OSS）

教材・サンプルが想定する実行環境の前提。setup 手順やツール選定（特にエージェント設定の配布方式）の判断根拠になる。横断決定 [00-hub/DECISIONS_ja.md](../00-hub/DECISIONS_ja.md) `2026-06-22-05`、外部事実 `F-gitwin-symlink` と整合。

## 想定環境

- **生徒**: Windows メインが基本で、**Git for Windows** を利用する。原則 **Developer Mode（または admin）を有効**にしておく（無効だと symlink 等の制約がきつく、教材の前提を満たしにくい）。
- **OSS 貢献者**: 同様に Git for Windows＋Developer Mode/admin、または Linux/macOS。
- **運用者**: Ubuntu メイン、macOS あり、Windows は必要最小限。

## 方向性

近い将来、Windows / macOS とも **Linux-native な環境を中心に据える**見込み（AI エージェント時代を見据えた各社戦略）。生徒向け環境でもこれを採る想定。**Git for Windows は当面残す**が、将来的には外せる見込み。

## ツール選定への含意

- `core.symlinks=true`＋`SeCreateSymbolicLinkPrivilege`（Developer Mode/admin）が揃えば symlink は動くが、揃わないと commit 済み symlink がリンク先文字列入りのプレーンファイルに化けて壊れる〔`F-gitwin-symlink`〕。
- したがって配布物は**権限非依存・全 OS 一律で動く方式を既定**にする。例：エージェント設定は `CLAUDE.md` の `@AGENTS.md` import を既定とし、symlink は任意代替（[DECISIONS](../00-hub/DECISIONS_ja.md) `2026-06-22-05`）。
- Linux-native 環境が標準化すれば symlink 制約自体が消えるため、import 既定でも将来の損はない。

## Python教材はuvを正面にする

WindowsでPython本体、virtual environment、dependency、lock、実行を一つの導線へまとめるため、pyenv + Poetryから`uv`へ移行する。初回授業はtemplateと`uv run`で制作へ到達させ、`pyproject.toml`やpackage管理はAPIを作る段階で開示する。設定を省略するのでなく、学ぶ意味が生じる順へ後ろ倒しする。

### starter template に課される条件（`2026-08-02-05`）

Python の定数（`mc_constants.py`）は**同梱されず、初回の接続成功で獲得する**。補完が効かない状態そのものを「まず接続せよ」という入口として使う設計なので、教材側に二つの条件が掛かる。

- **初回 Hello World は `mc_constants` を import せずに成立させる**。補完が無い状態で書けるプログラムを最初に置く。ここで定数を使う教材にすると、初日に「補完が効かない・import が失敗する」という形で設計が破綻する。
- **starter template に生成物の ignore 規則を同梱する**。`mc_constants.py` と `mc_constants.manifest.json` が commit されると、それを clone した生徒が接続せずに補完を得てしまい、しかも中身は別サーバー由来になり得る。template 側で ignore 済みにしておけば、生徒の最初の操作を `init` ではなく Hello World のまま維持できる。

任意の空ディレクトリから始める一般利用者向けには別途 project init を用意する（`12-python-client/mc-constants-design_ja.md` §2.5）。教材導線は `Hello World → hello 成功 → catalog 取得 → projection 生成 → 補完が現れる` を保つ。

### Hello World の定義と before / after の観察（`2026-08-03-01`）

**McRemote の Hello World は chat だけではない。** chat へ Hello を送ることと、ブロックを1個置くことの2つを最小成果とする。chat だけでは世界が変わらず、remote control を体験しない。

初回コードは `mc_constants` を import せずに成立させ、ブロック名は namespace を省略した文字列（`"sea_lantern"`）で書く。server が `minecraft:` を補完する入力 tolerate 規則（`2026-06-27-02`）を、説明せずに体験できる。Y 座標も抽象定数を先に与えず `62 + 5` のように計算して置く。

**補完の獲得は、説明ではなく操作で観察させる。** 「Hello World の後に補完が増えます」と書くだけでは、学習者は接続前の状態を見ていないので差分にならない。定数 import をコメントアウトした状態で配布し、次の順で進める。

1. **接続前**：一度コメントを外す。unresolved import の警告が出て、`block.` を打っても候補が出ず、実行すると `ModuleNotFoundError` で止まることを観察する。確認したらコメントへ戻す。
2. **実行**：Hello World を走らせる。pairing、chat、ブロック1個、projection 生成（`mc_constants.py` と manifest）が起きる。
3. **接続後**：エディタを必要に応じて reload し、再びコメントを外す。import が解決し、`block.` の候補が出て、`world_info.Y_SEA` が使えることを観察する。

接続後に置くブロックは**初回とは別の X 座標**にして、2つを並べる。before / after がエディタの中だけでなく、**マイクラの世界に2つのブロックとして並んで見える**。

この一連で、次の3つを同じ導線の中で扱える。

- コメントは実行対象ではない（外すと警告やエラーの対象になる）
- editor の warning と runtime の error は別のもの
- projection の actionable warning は補完更新だけが失敗し、接続と建築は継続する（`2026-08-02-06` ⑦）

## deploymentと教室runtimeの基準構成

**ケータリング型**は、preset・order・lock・artifactを使い、準備済みdeploymentを対象hostへ成立させる
構築方式である。特定PCや教室topologyの名前ではない（`2026-07-25-03`／`2026-07-25-04`）。

- **公開VPS profile**：学校と家庭から同じ公開HTTPS／WSS／Minecraftへ継続接続する。
- **`classroom-all-in-one` profile**：Ubuntu notebook、AP、Scratch、Bridge、Paper、McRemote等を一台へ
  まとめる教室向け参考構成。ケータリング型の一例であり定義そのものではない。
- **deployment LAN profile**：stationやMinecraftをLAN、VPN、閉域網内で提供する。all-in-one hostである
  必要はない。
- **限定公開／OSS operator profile**：利用者が管理するLANまたはHTTPS deploymentとして提供する。

WireScopeを使う場合、browserは対象deploymentのtop-level WireScopeを直接開く。QRはそのtop-level URLを
示し、公開案内pageからlocal resourceをfetchしない（`2026-08-10-02`）。

`classroom-all-in-one`構成では、生徒端末は専用SSIDへ接続し、固定gateway IPまたはQR codeから開始する。
mDNS名はbest effortで、必ず数値IP fallbackを用意する。HTTP＋same-origin WSの簡易modeではMcRemote自体は
使えるが、camera、microphone、Web Crypto等のsecure-context機能が制限される可能性を案内する。HTTPSを
求める場合は端末へのlocal CA導入か、実domain＋DNS-01＋local DNSを選ぶ。

Minecraft identityを守るため`online-mode=true`を維持し、school Ethernet、USB tether等をInternet upstreamに使う。USB Wi-Fi adapterは製品名だけでなくchipset / VID:PID / Ubuntu 24.04 driver / AP mode / 想定台数 / suspend / 発熱を検証済み機材として固定する。学校network上の無許可APにしない。
