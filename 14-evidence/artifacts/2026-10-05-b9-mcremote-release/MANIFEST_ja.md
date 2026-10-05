# B9 McRemote公開結果の搬送素材

- repo / surface: McRemote / Codex。
- authorization: knowledge `d6d59d91032230a959b7288807179e1bd8100041`、`00-hub/release-gate-notes_ja.md` B9 release authorization。最新runtime `6df2d14033a4646ce958737c06849725fcaee51e` も読み、同refのMcRemote公開指示が同一であることを確認。
- source: `feat/b9-contract-packaging@5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`。
- exact set: `b9-integrated-artifact-set-1`。
- tag: `v1.21.11-2320.0.0b9`。
- frozen JAR: `mc-remote-1.21.11-2320.0.0b9.jar`、261,016 bytes、SHA-256 `4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e`。
- 先行条件: tooling `v2320.0.0b9`公開済み（Release ID403384824、prerelease ON、draft OFF、WireScope ZIPとmanifestのdigestは凍結値一致）。
- 手順: mainへ凍結sourceをfast-forward、同commitへannotated tag、tag CI candidateの実JAR digestを照合、GitHub prerelease公開、固定Release workflowでcandidate昇格、公開asset／manifest／tag／mainをread-only照合。
- 状態: 公開完了。main／tag target `5cb33eb`、tag CI `37268144239` SUCCESS、Release workflow `37268629380` SUCCESS。公開JAR本体は凍結値とbyte一致、manifestの参照identityも一致。
- 分類②: B9 knowledge coordinatorへ、上記knowledge SHA／exact set／tag／source／JARを参照identityとして移管。正式knowledge authoringはknowledge側。
- 確認票: [materials/confirmation_ja.md](materials/confirmation_ja.md)、最終集計 [materials/release-result.json](materials/release-result.json)、現存7搬送directoryの分類 [materials/handoff-classification_ja.md](materials/handoff-classification_ja.md)。
- Release: https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2320.0.0b9
