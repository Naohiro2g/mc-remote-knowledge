# McRemoteの安定版の候補のTemurinでの確認（2026-10-29〜31）

> test class: `live-auto`。1年ぶりの安定版（2321.0.0）の横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-22の節）で、Javaの配布元を
> Temurinに決めた（`2026-10-29-01`）ことを受けて、McRemote担当が安定版の候補のJARをTemurinの最新のパッチで動かし直した。
> 確認票はknowledge `d012c91`を読んだもの（1.21.11の実行は`99898e5`の指示）。素材は
> `14-evidence/artifacts/2026-11-01-stable-gate-close/mcremote/2026-10-29-stable-temurin-validation/`（6 file）。
> 人の確認（rc2、Windows 11、Java 25.0.2、Paper 26.3 #214）はやり直していない（human owner 2026-10-29「人間確認は不要」）。

## identity

- McRemote：`agent/stable-2321-candidate@525c31823a8efb736463aec471c2756089546391`（このcommitが後の`v2321.0.0`）。CI `39720103168`、
  artifact `12399974471`の`mc-remote-2321.0.0.jar` 315,868 bytes `e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab`。
  作り直していない

| 実行日 | Paper | Paper JARのSHA-256 | Java |
| --- | --- | --- | --- |
| 2026-10-29 | 1.21.11 #132（54,846,016 bytes） | `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba` | Temurin `21.0.13+9` |
| 2026-10-31 | 26.3 #231（55,258,607 bytes） | `a836a016be7ac52352eb3a1efb6857bb42ee73a6c78d46e292f7e87742edb0e6` | Temurin `25.0.5+8` |

- どちらのJavaも配布元はEclipse Adoptium。`java -version`の出力は素材の確認票にある
- 置き場所：手元のLinuxの隔離したPaper。ゲームはloopbackにbindし、McRemoteだけを入れ、LuckPermsなしのfallbackの権限
- 起動の設定：`-Xms256M -Xmx1536M -XX:ActiveProcessorCount=2`と`nogui`（これまでの隔離した確認と同じ）

## 結果

**両方PASS**。

- 通常のpulse 8 groups、通常の再起動の後のpulse 4 groups、tokenなしの`hello`の拒否（`auth_required`）、有効化、credentialの
  health、正常な停止（exit 0）
- 26.3の2回の起動logはERROR／FATALが0件
- coordinatorが照合した（2026-10-31）：`mc-remote-verification-1.21.11.json`（63,705 bytes、
  `34dcf75c54434768463ab69e1e311029fa575044f6765b25a7c82e988e7127fe`）と`mc-remote-verification-26.3.json`（63,667 bytes、
  `00c4c675a7483793e97bb5853a13d23ac21c28afa501f5cf690e540c8c431545`）が票の値と一致。中の`source_commit`、JAR、Paperのbuildと
  SHA-256、`java -version`、`result`、pulse・再起動・lifecycleの`status`が票と合う。#132と#231のbytesとSHA-256はPaperの公式のAPIと一致

## 確かめていないこと

VPS、LuckPermsのある構成、人のゲームの操作と表示、負荷と長時間。公開VPSの26.3のセットでの確認は
`14-evidence/records/2026-10-31-stack-paper231-temurin25-heap3g_ja.md`にある。

## 素材

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `confirmation_ja.md` | 8,632 | `fe5924d513c64341bd6447f207fe8178465fc331a7a2fc99741d4a13c927018f` |
| `mc-remote-verification-1.21.11.json` | 63,705 | `34dcf75c54434768463ab69e1e311029fa575044f6765b25a7c82e988e7127fe` |
| `mc-remote-verification-26.3.json` | 63,667 | `00c4c675a7483793e97bb5853a13d23ac21c28afa501f5cf690e540c8c431545` |
| `auth-enforcement-full-1.21.11.json` | 889 | `ecd0d37197aff4b5112c4b537d88e3c242adbdfd37efcbc7f3f2bb4b3b9fdcc1` |
| `auth-enforcement-full-26.3.json` | 881 | `02bd25001388f0bceda73cfdc24dac755f885027f3ede8813c259c73b25e36ca` |
| `run-runtime-validation.py` | 6,587 | `2445751e71600c92359ac28e1e6858d3208b00315af5191823676aab40f508e2` |

`confirmation_ja.md`は、gate notesにある元の票（8,634 bytes、`179f61e41dc7bf7e0b95ca715e05ee784d96fa6df3ce3e493ac0b8e1a0f5bdaa`）の
home directoryのpathを`/USER_HOME`にしたもの（McRemote担当）。観測のJSONは元と同じbytes。tokenは`[REDACTED_TOKEN]`。`mcr_eh_`の値は
隔離したworldで作ったentityのhandleで、秘密ではない。
