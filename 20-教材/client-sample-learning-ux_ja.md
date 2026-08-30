# Client sampleの配置と多言語学習UX

## 1. 骨格

Minecraft Remoteのsampleは、一か所へ集約するのではなく、役割の異なる二つの面で育てる。

| 面 | owner | 主な役割 |
| --- | --- | --- |
| Client Library開発repoの`examples` | 各Client Library repo | 現行Client APIと同時にbuild／testできる、README隣接の最短実行例 |
| `mc_remote_samples` | sample repo | 同じconceptを言語ごとに比較し、観察、改造、再構成へ進むconcept-firstな学習面 |

各Client Library repoのexamplesは、API利用法の鮮度と言語固有の自然な入口を守る。`mc_remote_samples`は、それらを
一つの共通実装へ置き換えず、同じMinecraft Remote capabilityが各言語でどう見えるかを比較可能にする。

拘束は`2026-08-30-01`、sample全体の段階とmetadataは
[README・sample近代化ロードマップ](../00-hub/readme-sample-modernization-roadmap_ja.md)、多言語展開の順序は
[多言語Client Libraryロードマップ](../10-protocol/polyglot-client-roadmap_ja.md)を正とする。

## 2. Client Library repoが所有する最小examples

各Client Library repoは、少なくとも次を満たす小さな実行可能examplesを持つ。

- top-level READMEから最初の成功へ直接辿れる。
- 同じcheckoutのClient Libraryと一緒にbuild／testできる。
- public Client APIの変更時に、READMEと利用例のずれを同じrepoで発見できる。
- 接続、必要なpairing、期待結果、world変更範囲、cleanupを短く説明する。
- Python、Java、TypeScript、C#、Scratchそれぞれに自然な書き方と実行方法を使う。

この面は、現行Client APIの利用例に最も近いownerである。一方、Protocol、wire shape、cross-client semanticsの
正本ではない。sampleから共通の意味や曖昧さを発見した場合は、Protocol／Client Libraryの正本へ戻す。

Client repoへconcept／application sampleを追加することも妨げない。ただし、全言語比較のためだけに同じfile構造や
行構成を機械複製しない。

## 3. `mc_remote_samples`が所有するconcept-first比較面

`mc_remote_samples`の第一の案内軸は言語でなくconceptとする。たとえば次のように並べる。

```text
hello / pairing
chat
set and read block
axis and coordinates
events
building
```

各conceptから、その時点で存在するPython、Java、Scratch、将来のTypeScript／C#実装へ辿れるようにする。全言語が
同じfeature levelで揃うことは要求せず、未実装、検証対象版、推奨状態を明示する。

比較面は必ずしも全codeを自repoへ複製しない。Client repoの正準exampleへlinkしてもよく、比較教材として独立した
実装を置いてもよい。独立実装を置く場合は、owner、対象Client／Protocol版、参照元、学習目的を明示し、Client repoの
copyが黙って漂流する状態を作らない。

同じconceptの各言語版は、同じ外部意味と観察対象を共有してよいが、同じclass構成、変数名、制御構造、file名を
要求しない。比較するのはcodeの逐語対応ではなく、次である。

- 何をMinecraftへ依頼するか。
- Minecraft上で何が起きるか。
- どのClient APIとProtocol capabilityへ投影されるか。
- どの部分が言語固有か。
- world変更とcleanupがどこまで同じか。

## 4. 学習者の進み方

基本導線は次とする。

```text
Client repoの最小exampleを動かす
        ↓
Minecraft上の結果を観察する
        ↓
一箇所を言語nativeに書き換える
        ↓
mc_remote_samplesで同じconceptの別言語表現と比べる
        ↓
必要ならWireScopeでwireへの投影を観察する
        ↓
自分の作品または再構成sampleへ進む
```

入口は比較から始めてもよい。この順序は固定curriculumではなく、最短実行面、比較面、観察面を行き来できるための
地図である。

## 5. sample metadata

各実行例またはconcept一覧は、規模に応じて次を示す。

- concept名または安定したconcept ID
- 言語、Client Libraryのversion／source identity、minimum Protocol
- 確認したMinecraft／Paper target
- prerequisites、接続、pairing、実行方法
- 期待結果
- 実world変更かplayer限定の一時表示か
- 変更範囲、cleanup、完全復元にbackupが要るか
- 利用するClient APIと主要Protocol capability
- sample段階（minimum／concept／application／reconstruction）
- source ownerまたは正準exampleへのlink
- 現在の検証状態

広い範囲を破壊的に変更するsampleは、実行commandより前に範囲とbackup要否を示す。

## 6. Java Phase Bで得た最初の実体

`Naohiro2g/minecraft-remote-java@f259b396bfbde6e37e65b3c7916c25af37dc6a29`は、この配置を具体化した
最初のJava sliceである。

- `examples/`をClient Libraryと同じGradle buildへ接続した。
- READMEから`MyWorld`、Hello、Set and Read、AxisFlatへ辿れる。
- pairing、chat、block write／readを実Minecraft 1.21.11で確認した。
- AxisFlatはPython版と同じ幾何を使う一方、Javaに自然なclassとrunnerで実装した。
- world変更範囲、部分cleanup、完全復元にはbackupが必要なことを明示した。

これは`mc_remote_samples`の多言語再編が完了した証拠ではない。Java exampleを比較面へどう案内するか、および
Python／Scratchの既存sampleをどうconceptへ対応付けるかは、既存資産をinventoryしながら段階的に行う。

## 7. Scratchの投影

ScratchではJava／Pythonと同じsource file構造を要求しない。project、sprite、定義block、block stack等の
Scratch固有artifactを使い、同じconcept、期待結果、変更範囲、保存／cleanup境界へ対応付ける。

一般用途TypeScript Client LibraryとScratch Clientを同一物にしないのと同様に、Scratch sampleをTypeScript exampleの
機械投影として扱わない。

## 8. WireScopeの境界

WireScopeは、異なるClient APIが同じProtocol methodへ投影される様子を見る補助観察面にできる。sampleから
WireScopeを開く案内を置いてもよい。

ただし、WireScopeはread-only observerである。sampleを実行するcommand surface、Minecraftを変更するconsole、
pairing／credential操作面へ昇格させない。「つつく」操作が必要な教材では、Client Library、Scratch、または将来の
独立したconsole sourceを使い、observerへcommand権限を追加しない。

## 9. 同期と完了の考え方

- Client API変更では、同じClient repoが所有する最小exampleとREADMEを一緒に確認する。
- `mc_remote_samples`は各Client Library releaseの機械的mirrorまたは自動completion gateにしない。
- 比較面に掲載する実装は、参照するClient／Protocol identityと検証状態を更新する。
- 言語ごとの進度差を許容し、存在しないexampleを空の機械複製で埋めない。
- sampleが独立contractにならないよう、意味の正本へlinkする。

現在の`mc_remote_samples`はPython中心の既存資産を持ち、concept-firstな多言語比較面への移行は未完である。既存sampleを
一括移動せず、inventory、owner確認、concept対応付け、metadata補完の順で改訂する。

## 10. 却下した配置

- 実行可能sampleを`mc_remote_samples`だけへ集約し、Client repoからREADME隣接例をなくす。
- 全Client repoのsampleを共通repoへ機械複製する。
- 比較しやすさのため、各言語へ同じcode構造を強制する。
- Client repoとsample repoへ同じcodeをowner不明のまま二重配置する。
- Client Libraryのfeature levelとsample追加を全言語で同期releaseする。
- 学習者に操作させるため、WireScope observerへcommand権限を追加する。
