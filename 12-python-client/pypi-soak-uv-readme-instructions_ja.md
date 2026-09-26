# TestPyPI soak と uv 前提 README 再構築の指示書（Python）

> status: 実施中。根拠は `2026-09-26-03`（機構モード soak）、`2026-09-26-04`（README の目安）、`2026-09-27-01`（soak の対象を post3 へ）、`2026-09-27-02`（Python 対応範囲）。
> Python 担当の搬送票（2026-09-26、`docs/uv-readme@09c8b28`／`release/b7-post3-testpypi@19787fc`、未 merge）を受けて A-2 と A-3② を改訂した。

minecraft-remote-api を機構モード soak へ入れる（versioning-design §10.9）。`2301.0.0b7.post3` を TestPyPI へ出して遷移ゲート①〜④を実際に回し、並行して README を uv 前提へ作り直す。
PyPI.org への公開、McRemote、mature への移行判定はこの指示に含めない。mature への移行は human owner が soak の記録を見て判定する。

## A. TestPyPI soak

### 人間だけが行う前提作業

- TestPyPI アカウント：2FA でのログインを human owner が確認済み（2026-09-26）。既存の release は `1214.10.0`〜`1214.10.2`（2025-03-29 UTC）。当時は API token を作って `poetry publish --build --repository test-pypi` で手動アップロードしており、その token は現在アカウントに残っていない。Trusted Publisher は未登録。project 名とその owner がこのアカウントであることを担当が確認し、既存の release は消さない。以後の公開は Trusted Publishing だけを使う。
- TestPyPI 側の Trusted Publisher 登録（repo、workflow file、environment の指定）。担当は登録に必要な値を返し、登録は human owner が行う。

### 担当の作業

1. `2026-09-06-02` の正式段階の固定 trigger に、TestPyPI への publish step を Trusted Publishing（OIDC）で追加する。
   PyPI.org への publish step は、この指示では有効にしない。後で切り替えられる形にするかどうかは担当の設計に任せる。手作業の一回きりの upload は正式経路にしない。
2. `v2301.0.0b7.post3`（Python だけの docs／metadata 版、以後の `.postN` を含む）を固定 trigger から TestPyPI へ publish する。GitHub Release の wheel／sdist と digest を照合する。post2 の tag は動かさない（`2026-09-27-01`）。
3. 遷移ゲートを回して記録する（versioning-design §10.9）。
   - ① 再現可能な publish：手順が workflow と runbook だけで反復できること。
   - ② soak／yank の1サイクル：fresh な uv project に TestPyPI から exact-pin で入れ、`sb-beta.mc-remote.com` に接続してホームページの `hello.py` を実行する。その後 yank し、範囲指定と `--prerelease allow` での解決から外れることと、exact-pin では取得できることを確認してから、unyank する。無指定の解決はもともと pre-release を選ばないので、yank の確認には使えない。
   - ③ 退避手順：yank／unyank の手順、版番号は永久に消費されること、出し直しは `.postN` で行うことを runbook に書く。PyPI.org／TestPyPI の owner、2FA、2人目の maintainer の有無を記録する。
   - ④ exact-pin runbook：利用目的ごと（学習者の hello、beta tester、OSS 開発者）に exact-pin の手順を検証する。PyPI.org 上の無指定取得（`uv add minecraft-remote-api`）が従来の stable（1214.x）のままであることも確認する。初学者に試してもらった結果は記録に残すが、合否の基準にはしない。
4. TestPyPI には依存 package が揃っていないことがある。本 package だけを TestPyPI から取り、依存は PyPI.org から取る uv の index 設定を runbook に書く。

### 返却物

- workflow 変更の branch／commit、TestPyPI の release URL、publish run のログ
- ①〜④それぞれの実施記録と、runbook の path
- non-claim：PyPI.org への publish はしていない。mature 判定はしていない。

## B. uv 前提の README 再構築

ホームページの Python 手順（knowledge `d5a7e92`、`30-広告宣伝/homepage/index.html`）を正とし、README はそれに追従する。

1. ファーストビュー：uv の導入 → `uv init` → `uv add` → `uv run hello.py`。`uv add` の対象は、現在は git tag（`minecraft-remote-api @ git+…@v2301.0.0b7.post2`）とし、post3 の公開後は GitHub Release の wheel URL、PyPI に載った後は exact-pin に差し替える。「3行・3ステップ」は目安で、再現性のために省けない手順は残す（`2026-09-26-04`）。Deep-hiding と冒頭の言語方針 Note は従来どおり（`2026-09-08-01`／`2026-09-08-02`）。
2. Jupyter の節：`uv add --dev ipykernel`、VS Code でカーネルに `.venv` を選ぶ手順、JupyterLab を使う場合（`uv add --dev jupyterlab`、`uv run jupyter lab`）。自作の .py や `mc_remote` 自体を書き換えたら、カーネルを再起動してから import し直すことを明確に案内する。autoreload は勧めない（構造の変更に追従しきれず、原因の見えない不具合になる）。見出しには安定したアンカーを付け、そのアンカーを返す。返却された `#jupyter` をホームページのリンク先にした。
3. pyenv／pip／Poetry から uv への移行ガイド：README 本文から外した文書（`docs/` など）として作る。旧コマンドとの対応表、既存の venv や `requirements.txt`／Poetry project からの移り方を含める。移行ツールを使うかどうかは担当が確認して決める。

### 返却物

- 変更した branch／commit と path
- Jupyter の節のアンカー
- README の手順どおりに fresh 環境で `uv run hello.py` まで通した記録（接続先と日時）
