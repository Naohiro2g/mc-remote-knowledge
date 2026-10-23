# Phase E／F 具体化の案（草稿）

> 状態：2026-10-23にcoordinatorが起案し、同日human ownerがa〜dを判断した（下の「判断」）。決定は`2026-10-23-01`。

`2026-10-22-07`で、TS（Phase G）とC#（Phase I）の実装は、Phase E（比較）とF（conformanceの一般化）を
knowledgeで具体化してから始めると決めた。この文書は、その具体化の進め方の案である。

## 要約：進め方の案

- **0. Javaの追従**：初回stableの後の最初のsliceで、Javaを`2321.0.0`へ追従させる（決定済み、`2026-09-30-04`）。
  Javaは今b6（`23.0.0`）が基準で、追従しないと二つの独立実装を同じ版で比べられない
- **E1. Protocol Inventory**：行はmethodの一覧と、method以外の能力。列はProtocol、McRemote、Python、Java、Scratch、
  共有fixture。各担当が自分の列を確認票で返し、knowledgeが一つの表にまとめる
- **E2. 分類と判断**：各行をProtocol、client共通、言語固有、sample、未確定に分け、未確定を決定で決める
- **F1. fixture**：新しいclientがhelloからsetBlock／getBlockまでを独立に作れるだけのfixtureを、最初の範囲として
  そろえる。scripted peerのcase（`protocol_mismatch`など）もデータで書く
- **F2. 配り方**：fixtureはtoolingに置いたまま、各clientが固定したcommitで読む。共通のtest runnerは作らない
- **F3. 合格**：各clientのCIでF1のfixtureが全件PASSし、実McRemoteを相手にしたpulseが1本通ること
- **その後**：F1の範囲がそろったら、TSの実装を始める

## 要約：判断（human owner 2026-10-23）

- **a. 開始の時期**：E1の確認票は11/1の後に出し、Javaの追従と同じ票にする。10/31まではstableを優先する（案のとおり）
- **b. Phase D**：JavaのDX（catalog、補完）の評価を独立したgateにせず、E1の票へ入れる（案のとおり、「DE1へ」）
- **c. fixtureのlicense**：toolingのfixtureのディレクトリだけをMITにする。toolingのほかはAGPL-3.0のまま。
  clientはMITなので、fixtureをcopyしたりtestで読んだりできる（PythonとJavaが今copyで持っていることも、これで扱いが決まる）
- **d. TSとC#の順番**：基本はロードマップどおりTSを先にし、C#の実装はTSのPhase Bが通ってから始める。ただし、
  C#／Unityの到達目標は具体化してあるので、その準備を並行して進める（計画はhuman ownerがpush）

---

## 1. いまの前提

| 対象 | 状態 | 出典 |
| --- | --- | --- |
| Protocol SSOT | 人間が読むcontractは`10-protocol/wire-format-design_ja.md`。method一覧の生成用に`api-reference-metadata.json`（版、分類、用途だけ） | `2026-09-30-05` |
| 共有fixture | ownerはminecraft-remote-tooling。公開b8の12件。Scratchは固定commitで取り込み、McRemote、Python、Javaはcopyで持つ | `2026-10-05-01` |
| Python | `2321.0.0`（protocol `23.2.1`） | `00-hub/release-gate-notes_ja.md` |
| Java | Phase Cの代表capabilityまで。基準はb6（`23.0.0`）。Phase Dは未評価。初回stableの後に`2321.0.0`へ追従し、移管を再検証する | `2026-09-30-04`、`16-java-client/` |
| TS／C# | bootstrapまで（TS `6758b9e`、C# `4b295a0`） | `17-typescript-client/`、`18-csharp-client/` |

## 2. 進め方の詳細

### 0. Javaの追従（決定済みのもの）

初回stableの後の最初のsliceで、Javaが`2321.0.0`へ追従する。Phase Eで「二つの独立実装」を比べる前提になる。

### E1. Protocol Inventoryを作る

- 行：`api-reference-metadata.json`のmethodと、methodでない能力
  （hello／protocol negotiation、authentication／pairing、flushと順序、events cursor、error reason、catalog／constants、
  helloの`world_constants`）
- 列：Protocol（SSOTの節）、McRemote、Python、Java、Scratch、共有fixture
- セル：投影あり／部分／なし、と根拠（file、test名）
- 埋め方：各担当が自分の列を確認票で返す。coordinatorは実装を調べない。knowledgeが一つの表にまとめる
- 置き場所：`10-protocol/protocol-inventory_ja.md`（人が読む表）。機械で読む形は、F1で要るとわかってから作る

### E2. 分類して、未確定を決める

各行をロードマップ§14の分類（Protocol／Client共通意味論／言語固有／Application・sample／未確定）へ分ける。
「未確定」はSSOTで判断し、決定へ入れる。後の版へ送る部分は、同じcommitでNOTESに再開条件つきの行を置く。

### F1. 新しいclientが作れるだけのfixtureを決める

最初の範囲は、TS／C#のPhase B相当の縦slice（helloからsetBlock／getBlockまで）に足りる分だけにする。

- framing（改行区切りJSON-RPC 2.0）、hello／negotiation（`protocol_mismatch`を含む）、authentication／pairing、
  `world.setBlock`／`world.getBlock`（BlockValueのencode／decode）、error reasonの形、close
- scripted peerのcase（`client → hello`、`peer → protocol_mismatch`など）を、データとして書く
- 今の12件で足りない分を、tooling担当が足す

### F2. 配り方

fixtureはtoolingに置き続け、各clientは固定したcommitで読む（TSは`2026-10-22-07`で決定済み）。
共通のtest runnerは作らず、各言語が自分のtest runnerでloaderを書く（ロードマップ§19）。

### F3. 合格の定義

各clientのCIで、F1の範囲のfixtureが全件PASSすること。あわせて、実McRemoteを相手にしたlive-autoのpulseを1本通す。

### その後

F1の範囲がそろったら、TS（Phase G）の実装を始める。C#の実装はTSのPhase Bが通ってから始め、C#／Unityの準備は並行して進める（判断d）。

## 3. 次の操作

- tooling担当：共有fixtureのディレクトリにMITのLICENSEを置く（`2026-10-23-01`③）。依頼の時期は、stableの凍結
  （10/31）の作業と重ねない範囲でcoordinatorが決める
- coordinator：初回stableの後、E1の確認票（Javaの追従とPhase Dを含む）を起案する
