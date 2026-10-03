# B8 Python candidate 追記（2026-09-30）

確認票は受領済みのため再提出せず、訂正SHAに従った自repoの進捗とidentityを追記します。

- repo: `Naohiro2g/minecraft-remote-api`
- branch: `codex/b8-python-entity-particle`
- commit: `fc6c700b1588a1d052499314f47e8e7e5b06ae27`（commit/push済、GitHub branch API照合済）
- artifact / protocol: `2320.0.0b8` / `23.2.0`
- knowledge contract commit: 実際に読んだ `16668c5e5152d593c4b184939c9a9e723529d6e9`
- knowledge path: `00-hub/release-gate-notes_ja.md` 2026-09-30節、`00-hub/DECISIONS_ja.md` 2026-09-28-01/02・2026-09-30-01/02/06、`10-protocol/wire-format-design_ja.md` §5.0.2・§5.8.3
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー

## 自repoの変更と検証

- `spawnEntity`、`spawnParticle`（文字列とParticleSpec）、`playSound`で無印IDを拒否せず、そのまま送る。observerも同じ規則。blockは既存のまま無印をそのまま送る。resource IDをcase変換・trimしない。出力IDのcanonical規律は維持。
- `playSound(x,y,z,sound_id,options?)`と`playBlockSound(x,y,z,kind,options?)`を追加。連続／整数座標、optionsの省略と明示nullを保持。block中心の加算・音高の計算・SoundGroup補正をclientで行わず、server result nullとreasonを確認。全BuildModeで1 request、retryなし。Python observerは両method・options・null resultを認識し、未知fieldや不正値のrequestをdrop、server errorのreasonをsanitized表示。
- `from mc_remote import Minecraft`はPEP 562による遅延参照。サブモジュールreload後の再importでdirect importと同じ新しいclass。TYPE_CHECKINGとdirに対応。実際のVS Code/Jupyter補完表示は未確認。
- `pygame-ce`を必須依存から外し、extra `pygame`で`pygame-ce>=2.5`を宣言。core wheelはpygameなしでimport PASS。extraのwheel導入でpygame-ce 2.5.8を取得できた。repoのuv.lockは2.5.7をpin。
- entity lifecycle／nearby／ParticleSpec／self dust 81点graphは先行実装を収容。
- Windows入口手順はtracked `docs/windows-b8-entry_ja.md`（uv→init Python3.13→凍結Release wheel URL→import→JupyterLab→Notebook import）。URLはcoordinatorから受け取る欄。失敗時はGit for Windowsの通常ルートへ。実機担当はknowledge側で指定予定。Windows実機、Release URL、Jupyter起動は未実施。LinuxではGitをPATHから外してinit3.13→local wheel add→importまでPASS。
- READMEにはB8 surfaceとpygame追加手順、Windows入口手順へのリンクを追加。README全面再編の残件は元確認票から変わらず、完了扱いにしない。

実行した検査:

1. `uv --cache-dir /tmp/mcr-b8-uv-cache run --offline --with pytest pytest -q` → **588 passed**（loopback socketのsandbox拒否後、権限付きで再実行）。B8対象3 fileは335 passed、その中の現共有fixture投影は54 tests。
2. `uv --cache-dir /tmp/mcr-b8-uv-cache lock --check --offline`、`git diff --check` → PASS。
3. clean commit archiveから `uv build --offline --force-pep517`。先行buildとwheel/sdist byte-for-byte一致。
4. `scripts/check_wirescope_wheel.py` → 同梱ZIP/manifest、RECORD、license、source URL PASS。
5. isolated wheel core import（pygameなし）、Python3.13 Gitなしlocal wheel導入、pygame extra導入 → PASS。
6. CI: https://github.com/Naohiro2g/minecraft-remote-api/actions/runs/36718297434 （exact source SHA、全job成功、成果物照合済み）。

## CI candidate artifacts（返却する主identity）

[CI run 36718297434](https://github.com/Naohiro2g/minecraft-remote-api/actions/runs/36718297434)はcompleted/success。
Python 3.10／3.11／3.12／3.13の4 jobとbuild-candidateがsuccess。
workflow artifact `minecraft-remote-api-dist` ID `11097400766`、archive 375100 bytes、
SHA-256 `a04021bf7dccf80ee0764e544ba4105d2e8d06ad0f51c872dd6ebf2298e01207`。
取得してmanifest/source commit/bundled source/各digestを照合済み。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| minecraft_remote_api-2320.0.0b8-py3-none-any.whl | 192394 | 8ce5382381091a54c739b78e695b85a52a3b0485ef10dc20671b90c0049510a8 |
| minecraft_remote_api-2320.0.0b8.tar.gz | 185422 | 90242c9922750a0338139cb884823fbe17e1ead0b3c5deb317080cb4c95e64b4 |
| manifest.json | 672 | d2e726f589ffa761fc04cb3203e9d7c24676e8cf55af6fe3cc7b9a5a975aa058 |

`materials/ci-36718297434/`に保存。同梱WireScope/license検査もCI wheelでPASS。
manifestの`release_tag`はnull、`source_commit`は上記Python SHA、
`bundled_wirescope_source_commit`は`5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`。
今後のgate inputにはこのCI成果物のidentityを返す。tag／Releaseは未公開。

## local artifact（比較用。CI identityと混ぜない）

| file | bytes | SHA-256 |
| --- | ---: | --- |
| minecraft_remote_api-2320.0.0b8-py3-none-any.whl | 192369 | ff4d2842279896586646cc35c5b28ce7feacc1251a0ef75dc19cba6d2fc42af6 |
| minecraft_remote_api-2320.0.0b8.tar.gz | 185422 | 90242c9922750a0338139cb884823fbe17e1ead0b3c5deb317080cb4c95e64b4 |

同じdirectoryの`candidate-fc6c700/`に保存。
localとCIのwheelは異なる。ZIP全entryの比較で、差はWHEELのGenerator
（local PEP 517 backend uv 0.11.33／CI uv 0.11.7）とそのRECORD行のみ。
METADATA・Python code・同梱app・licenseは同一で、sdistはbyte-for-byte同一。
localの再現性PASSをCI wheelとのbyte-for-byte一致と読み替えない。`manifest.json`はrelease_tag=null、source_commit=上記Python commit、
`bundled_wirescope_source_commit=5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`。release inputの凍結・公開はまだしない。

## Scratch successor待ちと未検証境界

- 読み取り確認したScratch headsは前回と同一。fixture `agent/b8-owner-fixture@0735a9c957d069f719bee9c91e8be0f9322f4920`、WireScope `agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`。
- 現共有fixture `entity-particle-v23.2.json`は20967 bytes／SHA-256 `09c1565bf81d33c92d6282e6e20d926559168cb9d780c07d30ad2f9f5895640e`、59 cases。サウンドとresource IDのsuccessor caseは未取得。
- 同梱WireScope ZIP 81222 bytes／SHA-256 `870c5bf33c7af5fe720fde0514a3192865dfc1057707bbbba405bbf238642a15`、manifest 2321 bytes／SHA-256 `fb4db540cedde45eb7a4ad2fa56cfe387352ce6f99203663d0db788f2b38b8aa`。23.2.0の初期entity／particle対応のみ。サウンドmethodと無印IDの共通validator追従はScratch successorを待って入れ替える。Pythonのobserver追従だけでcommon app対応完了とはしない。
- 現app28 tests／Python26frames受理の既存PASSは初期範囲だけに限定し、新sound/resource IDの証拠として再利用しない。
- browser接続はこの環境で`privileged native pipe bridge is not available; browser-client is not trusted`。DOM操作・click/type・screenshot・localhostの実操作は未検証。
- 他repoへの変更、shared環境の変更、real server往復、2-player、人間参加試験、tag/release/PyPI公開、移管は実施していない。
- 10/3向けにPython独自surfaceはcandidate化済み。残る自repo作業はScratch successorのfixture/app取り込みと、そのidentity・projection検証。横断freeze・live・Windows・最終gate判定はcoordinator側。

## 次の担当が再開する条件

Scratchからsuccessorのexact source/artifact identityを受け取る。fixtureはexact bytesを取り込みsource.json/hashを更新。
同梱WireScopeはowner発行のZIP/manifestを照合してpinsとsource URLを更新し、対象検証を回す。
candidateが変わるのでcommit/push後に旧identityを差し戻し、wheel/sdist・bundled_wirescope_source_commitを追記する。
当面scratch-editor所有の取得経路は変えず、b9移管時にcoordinator指定へ追従する。
