# Release gate 確認票（Temurin再確認・1.21.11と26.3）

- 対象 repo: `Naohiro2g/McRemote`
- 対象 branch/commit: `agent/stable-2321-candidate@525c31823a8efb736463aec471c2756089546391`。GitHub APIの同commitと照合済み。公開文書2点はworking treeで更新、未commit。
- release / channel: `2321.0.0`／初回stable候補。protocol `23.2.1`。
- gate coordinator: knowledge担当session。
- human release owner: プロジェクトオーナー。
- current phase: knowledgeの横断gateはOPEN。両対応版のTemurin再確認結果を返す。
- contract maturity / required test tier: 既存契約のrelease候補。変更はJava実行環境で、既存の隔離live-autoを再実施する。
- knowledge contract path: `00-hub/stable-gate-work-instructions_ja.md` 共通・McRemote追補3、`00-hub/release-gate-notes_ja.md` 初回stableの節、`00-hub/DECISIONS_ja.md` `2026-10-29-01`。
- knowledge contract commit: `d012c910f16d8c89921c8265124049a8c732ab1d`。remote mainとの一致を確認し、上記3文書を実読した。1.21.11実行時の指示は`99898e558f4bd08c2ad043c4ab09b69089408619`。その観測recordは変更していない。
- gate manifest identity: 追加のmanifest指定はない。追補3に指定されたsourceとJARのbytes・SHA-256を使った。
- change cone: 同じstable候補JARを、1.21.11はTemurin 21.0.13+9、26.3はTemurin 25.0.5+8で実行。26.3のPaperはhuman ownerが確定した#231。公開READMEとJava・miseガイドは確定した運用方針へ更新済み。
- reused PASS / rationale: 既存候補のCI `39720103168`とartifact `12399974471`のidentityを維持する。新JDKでの動作は今回の追加観測。rc2の人による確認、旧JDKでの結果は当時の環境のまま残す。横断のPASS再利用の判断はcoordinatorへ返す。
- exact compatibility set / freeze status: 両対応版を下記identityで確認済み。26.3 #231のbytes・SHA-256はknowledge、公式API、取得したJARで一致。横断setの凍結判定は行っていない。
- target deployment / profile / lock: 手元Linuxの隔離Paper。ゲームはloopbackへbindし、APIは専用portへlocalhostから接続。McRemoteのみ、LuckPermsなしのfallback。worldと有効な検証用long-lived credentialは既存の隔離fixtureからコピーし、元の環境へ書き込んでいない。
- authorized next action: 指示3の両対応版の自動再確認を完了し、coordinatorへ結果を返す。
- test class: `live-auto`。公開文書は隔離したmise設定でコマンドと生成設定を確認。
- 実行した command / 手順: 下記。両対応版の通常起動と再起動で`-Xms256M -Xmx1536M -XX:ActiveProcessorCount=2`、`nogui`を使用。従来の隔離検証と同じ起動フラグ。
- 結果: 両対応版で通常pulse 8群、通常再起動後pulse 4群、各起動で認証要求・有効化・credential health・正常停止PASS。26.3の両起動ログはERROR／FATAL 0件。詳細は下記。
- evidence record / artifact: このpacketは素材。正式record案は`14-evidence/records/2026-10-29-mcremote-stable-temurin-runtime_ja.md`、artifact案は同名の`14-evidence/artifacts/`配下。配置と採番はknowledge側。素材は本票と同じfolder内のsanitized JSON。
- 未検証の境界: VPS、LuckPermsありの実構成、人のゲーム操作・表示、負荷・長時間試験。人の確認は指示どおり再実施していない。
- security / compatibility / rollback の確認: 認証なしhelloの`auth_required`、有効tokenによる接続・編集、通常再起動後の同credentialによる再接続を確認。raw token・UUID・DB・worldをpacketへ含めず、JSON内のredactionを検査。既存の履歴素材・候補JAR・起動フラグを変更していない。
- 判定を求める事項: coordinatorに両対応版の結果を返し、横断gateでの採用・凍結の判断を求める。component／横断gateの最終判定は行わない。

## 確認した実体

| 項目 | 値 |
| --- | --- |
| McRemote | `mc-remote-2321.0.0.jar`、315,868 bytes |
| JAR SHA-256 | `e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab` |
| source | `525c31823a8efb736463aec471c2756089546391` |
| Java vendor / distribution | Eclipse Adoptium／Eclipse Temurin |
| 今回のCI | なし。既存候補のJARを手元で再確認し、再buildしていない |

| 実行日 | Paper | Paper JAR bytes | Paper JAR SHA-256 | Temurin |
| --- | --- | --- | --- | --- |
| 2026-10-29 | `1.21.11 #132` | 54,846,016 | `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba` | `21.0.13+9` |
| 2026-10-31 | `26.3 #231` | 55,258,607 | `a836a016be7ac52352eb3a1efb6857bb42ee73a6c78d46e292f7e87742edb0e6` | `25.0.5+8` |

26.3 #231は、最新knowledgeのMcRemote追補3と[Paper公式API](https://fill.papermc.io/v3/projects/paper/versions/26.3/builds/231)、取得したJARのbytes・SHA-256を照合した。起動ログでも`Paper 26.3-231-main@8a170a3`を観測した。

Java 21の`java -version`実測出力:

```text
openjdk version "21.0.13" 2026-10-20 LTS
OpenJDK Runtime Environment Temurin-21.0.13+9 (build 21.0.13+9-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.13+9 (build 21.0.13+9-LTS, mixed mode, sharing)
```

Java 25の`java -version`実測出力:

```text
openjdk version "25.0.5" 2026-10-20 LTS
OpenJDK Runtime Environment Temurin-25.0.5+8 (build 25.0.5+8-LTS)
OpenJDK 64-Bit Server VM Temurin-25.0.5+8 (build 25.0.5+8-LTS, mixed mode, sharing)
```

## 実行手順と結果

```sh
python3 handoff-materials/2026-10-29-stable-temurin-validation/materials/run-runtime-validation.py \
  --repo "$PWD" \
  --runtime /tmp/mcremote-stable-temurin-20261029 \
  --java /USER_HOME/.local/share/mise/installs/java/21.0.13+9.0.LTS/bin/java \
  --mc 1.21.11 --build 132 --port 29714

python3 handoff-materials/2026-10-29-stable-temurin-validation/materials/run-runtime-validation.py \
  --repo "$PWD" \
  --runtime /tmp/mcremote-stable-temurin-20261029 \
  --java /USER_HOME/.local/share/mise/installs/java/25.0.5+8.0.LTS/bin/java \
  --mc 26.3 --build 231 --port 29764
```

同手順は既存の`scripts/compatibility_pulse.py`と`scripts/prepare_minecraft_verification.py`を呼び出した。新しい自動化の製品機能ではない。

- 通常起動：有効化とcredential health、認証なしhelloの拒否を確認。認証した接続、対応版宣言、catalog、構造化blockの設置・取得、32,768 blockの一括操作と通知flush、上限超過の拒否、看板・装飾、entity handle、event poll、particle・chatの8群PASS。
- 通常停止・再起動：両対応版の各Javaプロセスがexit 0で停止し、McRemoteの無効化を観測。再起動後、同credentialで接続し、建築と読み戻しを含む4群PASS。
- 起動待ち＋検証＋停止の実測：1.21.11は初回59.74秒／再起動34.34秒、26.3は初回45.17秒／再起動32.07秒。環境準備・文書更新・結果整理の時間は含まない。

各recordは通常pulse、再起動後pulse、lifecycleを内包する。

| 素材 | bytes | SHA-256 |
| --- | --- | --- |
| `mc-remote-verification-1.21.11.json` | 63,705 | `34dcf75c54434768463ab69e1e311029fa575044f6765b25a7c82e988e7127fe` |
| `mc-remote-verification-26.3.json` | 63,667 | `00c4c675a7483793e97bb5853a13d23ac21c28afa501f5cf690e540c8c431545` |

## 公開文書と着地確認

- `README.md`：Temurin Java 21／25、最新パッチ推奨、系列指定、明示的な更新、詳細ガイドへの導線へ変更。
- `docs/java-mise_ja.md`：mise導入・シェル設定、Bash補完、`mise ls java`、系列別の選択と起動、パッチ追従、既存環境の確認・整理を記載。教材・ホームページのhow-toへの転用元として保持する。
- Java 21／25それぞれの`mise use`、系列指定の`mise.toml`生成、`mise ls java`、Temurinの実体確認を、userの設定から分離した一時環境で実行してPASS。Bash補完の生成、コード例の構文、相対リンクも確認。userの`mise.toml`は変更していない。
- Java搬送票の16,370 bytesとSHA-256 `3647d06dfb0122d54ca5c4cce4264dfa6541106ed3e967ba8bc5ec855b1e7825`は全件一致し、knowledgeの決定・追補との着地照合OK。調整された「今回の起動フラグは変更しない」も確認。
- 元の`handoff-materials/2026-10-29-java-temurin-policy/`は、human ownerの追加指示で教材・ホームページのhow-toへの転用まで分類②で保持。主票1点のまま内容は変更していない。
