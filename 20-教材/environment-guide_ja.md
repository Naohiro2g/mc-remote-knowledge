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

## 教室runtimeの二つの基準構成

- **VPS**: 学校と家庭から同じ公開HTTPS/WSS・Minecraftへ継続接続する構成。
- **ケータリング作戦**: 許可を得て持ち込むUbuntu notebook一台と標準USB Wi-Fi adapterで、Scratch / Bridge / Paper / McRemoteを教室LAN内に提供する`classroom-all-in-one`。

ケータリング構成では、生徒端末は専用SSIDへ接続し、固定gateway IPまたはQR codeから開始する。mDNS名はbest effortで、必ず数値IP fallbackを用意する。HTTP+same-origin WSの簡易modeではMcRemote自体は使えるが、camera、microphone、Web Crypto等のsecure-context機能が制限される可能性を案内する。HTTPSを求める場合は端末へのlocal CA導入か、実domain + DNS-01 + local DNSを選ぶ。

Minecraft identityを守るため`online-mode=true`を維持し、school Ethernet、USB tether等をInternet upstreamに使う。USB Wi-Fi adapterは製品名だけでなくchipset / VID:PID / Ubuntu 24.04 driver / AP mode / 想定台数 / suspend / 発熱を検証済み機材として固定する。学校network上の無許可APにしない。
