## Release gate 確認票・追記（2026-10-01）

- 対象 repo: Naohiro2g/minecraft-remote-api
- 対象 branch/commit: `codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470`（push済、GitHub branch API一致）
- release / channel: `2320.0.0b8` / candidate（未公開）、protocol `23.2.0`
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: 横断exact set凍結前のcomponent取り込み完了。自repoの実装／unit・deterministic／CIまで。
- knowledge contract path: `00-hub/release-gate-notes_ja.md` 2026-09-30節、`10-protocol/wire-format-design_ja.md` §5.0.2／§5.8.3。
- knowledge contract commit: 実際に読んだ `fd29db757c07f993155842ecc88b1c39558611a9`。runtimeとsound notes §3.3は `4f0b46f27a1f1e31a47b7a1f9aa79254e3b153a6`（wireはfd29db7とbyte-for-byte同一）。
- authorized next actionの根拠: user「提案の形に変更してください」、coordinator「df34849から同梱WireScopeを作り直し、CI成果物identityを追記」。
- change cone: サウンドのkeyword-only引数／None省略／pitch-note排他、successor fixtureとconsumer、指定sourceのWireScope再生成・pins・source URL、B8利用例。
- exact compatibility set / freeze status: 自repoのsourceとCI artifactを返す。横断setはcoordinatorが扱う。旧Python `fc6c700`を現candidate inputとして使わない。
- test class: unit/deterministic。shared・live-auto・live-humanは実施しない。

### 実装の結果

playSound／playBlockSoundは `volume=`、`pitch=`、`note=`、`receiver=` をkeyword-onlyで受ける。
volume/pitch/noteの既定はNone（wireから省略）、receiverはworld。両pitch/note指定は送信前にValueError。
note=0／volume=0は送る。通常の音の既定1.0とblockのSoundGroup既定を保持。
旧candidateの第5位置options dictは使えず、dict変数は `**controls` で渡す。
音名換算はユーザーコードのまま。

### WireScope再生成の照合

同梱source commit（`bundled_wirescope_source_commit`）:
`df34849d2502a498a06c5fe07a91d03e925124eb`。

| artifact | bytes | SHA-256 | coordinator提示との照合 |
| --- | ---: | --- | --- |
| wirescope-app.zip | 83746 | `4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07` | 一致 |
| wirescope-app.manifest.json | 2321 | `45d56d5012c2c0b21631597e160363d93bcf3e736b74cc0b8a1041afc8101413` | 一致 |

read-onlyな使い捨てcloneでsource commitをcheckoutし、node24.19.0、owner lockfileの依存で
`npm run build:artifact --workspace=@mc-remote/live -- --source-commit df34849d2502a498a06c5fe07a91d03e925124eb`。
ZIP/manifest/source commitを照合してから同梱し、runtime・wheel checker・metadata/testのpinsを更新。
ownerの実装変更、owner repoのcommit/pushは行わない。

fixtureは `054a3af017f1abb8cc01cf85b3bc83181e648e19`の
`mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`をexact bytesで取り込み。
36481 bytes／`ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`／111 cases。
指定WireScope source treeのfixture bytesとも一致。fixture内のcontract SHAは`0318332a2b3395a5d74b46d7da6946030a2fc172`。
Python consumerは143 tests（元54＋sound keyword projection37＋raw observer37＋resource matrix15）。
server-only検索・WorkAdmission・handle transaction 6ケースはinventoryに含め、Pythonでserver内部を実証したとはしない。
wire nullの拒否とPython Noneの省略も区別。

### 検証

- `uv --cache-dir /tmp/mcr-b8-uv-cache run --offline --with pytest pytest -q` → **685 passed**（loopback socketのため権限付き）。
- B8対象3 file → **432 passed**。consumer143 testsを含む。
- 共通app対象 `observer.test.ts`／`sound-resource-observer.test.ts`／`artifact.test.ts` → **37 passed**。
- Python successor snapshot **79 frames**（sound37／resource15のrawケース＋keyword生成request/result）を、共通appのbuild済みproduction `parseObserverSnapshot`が受理。
- `uv lock --check --offline`、`git diff --check`、PEP517 build、wheel checker（ZIP/manifest/source/license/RECORD）→ PASS。
- clean source archiveから再buildしたlocal wheel/sdistが検証済みlocal成果物とbyte-for-byte一致。
- isolated Python3.13のpygameなしwheelで短いimport、keyword専用・0・None既定・両指定ValueError・同梱app読み込み→ PASS。
- [CI 36860299749](https://github.com/Naohiro2g/minecraft-remote-api/actions/runs/36860299749) → exact commit、completed/success。Python3.10〜3.13とbuild-candidate全success。

### CI成果物（返却する主identity）

workflow artifact `minecraft-remote-api-dist` ID `11161896597`。
archive 381099 bytes／SHA-256 `4238ff22ebe49bd173e4a315275a575808c53e130245d4043bb7b1eb2b41f347`。
provider API digestと取得ZIPが一致。manifestはsource_commit／bundled sourceと各artifact digestが一致。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| minecraft_remote_api-2320.0.0b8-py3-none-any.whl | 195068 | `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180` |
| minecraft_remote_api-2320.0.0b8.tar.gz | 188775 | `9d56d92b10936787e1eebc1cf85a521ea19aa2e57b391f474eb695b0ba3fad32` |

manifest.json: 672 bytes／`f51bcd8a2936bce46736f2196d6a209113106558cce5ae445472e1d98066c353`。
release_tag=null。CI wheelの同梱app/license検査PASS。
local PEP517 wheelはuv0.11.33、CI wheelはuv0.11.7。ZIP entry比較ではGeneratorとそのRECORDだけが異なり、
Python code/METADATA/app/licenseは同一。sdistはbyte-for-byte同一。localのwheel digestをCI identityと混ぜない。

### 未検証の境界・次の一手

実serverの往復、shared環境の変更、2-player、人間の視聴覚、real-browser UI、Windows実機、VS Code/Jupyter補完表示は未実施。
既存のbrowser runtime接続不能から実browser操作PASSへ読み替えない。
他repoの実装、tooling移管、tag/Release/PyPI公開は実施しない。
Windowsは最新gateで公開直後にhuman ownerがRelease wheel URLから確かめる位置づけ。
README全体の残件は今回の範囲外で残る。横断gateの最終判定はcoordinatorが行う。

## セッションクローズ票

- repo / surface: minecraft-remote-api / Codex
- branch/commit: codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470
- 作業範囲 / 今回やったこと: 新sound surface、successor fixtureと共通app取り込み、検証、commit/push、CI成果物照合。
- 変更ファイル: Minecraft/sound_value、bundled ZIP/manifestとpins、shared fixture/provenance、consumer/tests、B8利用例。
- 検証: 上記のunit/deterministic/CIとartifact照合。
- 未完了: coordinatorのexact set凍結と実機試験、Windows・補完表示・README残件、release。
- 次に読むもの / 次の一手: coordinatorが出す次の実施票。追加の自repo修正があればidentityを更新して返す。
- 未着地の搬送物: 本追記、sound-surface-handoff_ja.mdのPython局所決定。
- NOTES/DECISIONS: local NOTESへ反映。knowledgeのauthoring/配置は行わない。
- 注意点: 旧fc6c700 candidateではなく52d35f5＋CI artifactを使う。shared/human/releaseは今回未許可。
