#!/usr/bin/env python3
"""Collect the published b8 fixtures and local handoff entry identities."""
import hashlib
import json
import posixpath
import re
import subprocess
from collections import Counter
from pathlib import Path

SOURCE = '691576f60b7f0824e1753bd6823901d01fbe2422'
KNOWLEDGE_CLOSE = '2a8c3eae4e489e67f044111b0d1e6cdd22ead86a'
KNOWLEDGE_RUNTIME = '90cf87fbcd132984ef027a98a263e5911aaf30bf'
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIXES = {
    'Protocol': 'mc-remote/protocol/test/fixtures/',
    'WireScope': 'mc-remote/live/test/fixtures/',
    'Bridge': 'mc-remote/bridge/test/fixtures/',
}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def case_ids(value, prefix):
    ids = []
    if isinstance(value, dict):
        if isinstance(value.get('id'), str) and value['id'].startswith(prefix):
            ids.append(value['id'])
        for item in value.values():
            ids.extend(case_ids(item, prefix))
    elif isinstance(value, list):
        for item in value:
            ids.extend(case_ids(item, prefix))
    return ids


def case_information(name, value):
    if name == 'direction-lightning-v23.1.json':
        ids = case_ids(value, 'B7-')
        assert len(ids) == len(set(ids)) == 93
        return 93, '明示B7 case ID', {'by_id_prefix': dict(sorted(Counter(x.split('-')[1][0] for x in ids).items()))}
    if name == 'entity-particle-v23.2.json':
        groups = {
            'nearby.cases': len(value['nearby']['cases']),
            'nearby.handle_transaction_cases': len(value['nearby']['handle_transaction_cases']),
            'entity_lifecycle.cases': len(value['entity_lifecycle']['cases']),
            'particle_stage_2.cases': len(value['particle_stage_2']['cases']),
            'sound.cases': len(value['sound']['cases']),
            'resource_ids.cases': len(value['resource_ids']['cases']),
        }
        ids = case_ids(value, 'B8-')
        assert len(ids) == len(set(ids)) == sum(groups.values()) == 111
        return 111, '明示B8 case ID', groups
    if name == 'sign-v23.json':
        ids = [key for section in value.values() if isinstance(section, dict)
               for key in section if re.fullmatch(r'B6-S\d+', key)]
        assert len(ids) == len(set(ids)) == 7
        return 7, 'B6-S01〜S07のcase group（group内に複数入力あり）', {'case_group_ids': ids}
    summaries = {
        'block-value-v22.json': lambda: {
            'state_text': len(value['state_text']), 'invalid_state_text': len(value['invalid_state_text']),
            'block_value': len(value['block_value']), 'error_text.malformed': len(value['error_text']['malformed']),
        },
        'dimensions-v22.json': lambda: {key: len(value[key]) for key in ['accepted_refs', 'not_aliases', 'invalid_refs']},
        'events-v23.json': lambda: {'poll_requests.rejected': len(value['poll_requests']['rejected']),
                                 'poll_result.events': len(value['poll_result']['events'])},
        'spawn-v22.json': lambda: {'spawn_particle_named_examples': len(value['spawn_particle']),
                                 'spawn_entity_example': 1, 'spawn_entity_legacy_example': 1},
        'display-alias-v1.json': lambda: {'words': len(value['words']), 'example': 1},
        'observer-session-lifecycle.ndjson': lambda: {'ndjson_records': len(value)},
        'scratch-main-lifecycle.json': lambda: {'snapshots': len(value)},
        'station-attach-v1.json': lambda: {'attach_errors': len(value['attach_errors']),
                                        'bootstrap_ready_examples': 1, 'bootstrap_not_ready_examples': 1},
        'one-shot-transport-v1.json': lambda: {'sample_payload': 1, 'sample_message': 1},
    }
    return None, 'fixture全体のcase数は未定義（sample／record数と区別）', summaries[name]()


paths = git('ls-tree', '-r', '--name-only', SOURCE, *PREFIXES.values()).decode().splitlines()
assert len(paths) == 12
readers = {}
source_files = git('ls-tree', '-r', '--name-only', SOURCE, 'mc-remote', 'packages/scratch-vm', 'packages/scratch-gui').decode().splitlines()
for path in source_files:
    if '/test/' not in path or not path.endswith(('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs')):
        continue
    text = git('show', f'{SOURCE}:{path}').decode()
    for match in re.finditer(r'''(['"])([^'"\n]+/fixtures/[^'"\n]+)\1''', text):
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), match.group(2)))
        if resolved in paths:
            reader = {'path': path, 'line': text.count('\n', 0, match.start()) + 1}
            readers.setdefault(resolved, []).append(reader)

fixtures = []
for path in paths:
    raw = git('show', f'{SOURCE}:{path}')
    parsed = [json.loads(line) for line in raw.splitlines() if line.strip()] if path.endswith('.ndjson') else json.loads(raw)
    count, kind, groups = case_information(Path(path).name, parsed)
    fixture = {
        'owner': next(owner for owner, prefix in PREFIXES.items() if path.startswith(prefix)),
        'path': path, 'bytes': len(raw), 'sha256': digest(raw),
        'case_count': count, 'case_count_kind': kind, 'structure_counts': groups,
        'consumers': readers.get(path, []),
    }
    assert fixture['consumers'], f'Missing consumer: {path}'
    fixtures.append(fixture)
assert Counter(f['owner'] for f in fixtures) == {'Protocol': 7, 'WireScope': 4, 'Bridge': 1}
baseline = json.loads((ROOT / 'handoff-materials/2026-10-03-b8-scratch-live-gate/materials/fixture-inventory.json').read_text())
baseline_items = baseline if isinstance(baseline, list) else baseline['fixtures']
baseline_by_path = {f['path']: f for f in baseline_items}
assert set(baseline_by_path) == set(paths)
for fixture in fixtures:
    old = baseline_by_path[fixture['path']]
    assert (fixture['bytes'], fixture['sha256']) == (old['bytes'], old['sha256'])
write_json('fixture-inventory.json', {'source_commit': SOURCE, 'knowledge_close_commit': KNOWLEDGE_CLOSE,
           'knowledge_runtime_commit': KNOWLEDGE_RUNTIME, 'fixtures': fixtures})

heading = f'''# b9移管の起点：公開b8 sourceのfixture一覧

- 採取元: scratch-editor@`{SOURCE}`（tag `v2320.0.0b8`／developの公開target）。branch先頭`01cdb0b`は採取元ではない。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`のb8 CLOSED節、`10-protocol/protocol-tooling-migration-plan_ja.md`。
- knowledge contract commit: CLOSED節`{KNOWLEDGE_CLOSE}`、最新runtime／INDEX／移管計画`{KNOWLEDGE_RUNTIME}`を実際に読んだ。
- Protocol 7、WireScope 4、Bridge 1の計12 fixture。`git show <source>:<path>`の生bytesからSHA-256を算出し、既存の凍結後棚卸しの全12件と一致。
- case数はfixture内の明示case ID、または名前付きcase groupを数える。統一case定義のないfixtureは「未定義」とし、NDJSONの行数／snapshot数／辞書語数をcase数へ換算しない。

| owner | path | bytes | SHA-256 | case数 |
| --- | --- | ---: | --- | --- |
'''
for f in fixtures:
    count = '未定義' if f['case_count'] is None else str(f['case_count'])
    if f['case_count_kind'].startswith('B6-'):
        count += ' group（B6-S01〜S07）'
    heading += f"| {f['owner']} | `{f['path']}` | {f['bytes']:,} | `{f['sha256']}` | {count} |\n"
heading += '\n## consumerと構造の補足\n\nconsumerは同じ公開source内で実際にfixtureを読み込むtest file。以下の行番号もそのsourceの値。\n\n'
for f in fixtures:
    heading += f"### {Path(f['path']).name}\n\n"
    heading += f"- case数の意味: {f['case_count_kind']}。\n"
    heading += '- 構造の件数: `' + json.dumps(f['structure_counts'], ensure_ascii=False) + '`。\n'
    for reader in f['consumers']:
        url = f"https://github.com/Naohiro2g/scratch-editor/blob/{SOURCE}/{reader['path']}#L{reader['line']}"
        heading += f"- consumer: [{reader['path']}:{reader['line']}]({url})\n"
    heading += '\n'
heading += '''## 依存と配布の境界

- VM runtimeは`@mc-remote/protocol`をimportせずwire定数をinlineで持つ。上記VM testがrepo相対pathでfixtureを直接読む。GUIのWireScope source testもrepo相対pathでProtocol fixtureを読む。
- Protocol owner testは同package内の相対pathで読む。`block-value-v22.json`を直接読むconsumerはVMのBlockValue testで、Protocol package内にこのファイルの直接readerはない。
- WireScope testはProtocol fixtureと自身のobserver／session／station fixtureを読む。WireScope／Bridge「専用」はfixtureの所有分類であり、専用fixtureの一部をVM testも読む。
- Bridge runtimeはpayload透過のtransportでProtocol packageをimportせず、Bridge testはone-shot transport fixtureを読む。
- `spawn-v22.json`の`spawn_entity.result`は歴史的な`mceh_` prefixの例。現行23.2のhandle合格値には使わない。Protocol contract testはparamsだけを利用し、現行handle例をevents fixtureから取得する。
- release manifestの`wirescope`はbrowser app ZIP、`wirescope-manifest`はdetached manifest、`contracts`はScratch GUIの`contracts/` tar。**Protocol fixtureの配布tarではない。**
- 横断consumerについて、参照したknowledge gateにはMcRemote／Pythonが111 case版B8 fixtureを取り込んだ記録がある。移管計画にはJavaもScratch owner由来のfixtureを読むとあるが、Javaはb8／b9の対象外で初回stable後に追従する。これらはSSOTの記録であり、本票の直接reader採取とは区別する。
- McRemote／Python／Java repo内のcopy、reader、取得経路は今回調査していない。これは公開Scratch sourceのowner／repo内consumer一覧であり、他repoの移管可否や適合を主張しない。
- 本票は移管の入力。topology、owner、source、distributionの変更は実施していない。

再採取: repo rootで`python3 handoff-materials/2026-10-03-b8-close-inventory/materials/collect-inventory.py`。
機械可読値: `materials/fixture-inventory.json`。製品fixtureの編集、build、live試験は今回行っていない。
'''
(HERE.parent / 'FIXTURES_ja.md').write_text(heading)

classification = json.loads((HERE / 'classification-input.json').read_text())
actual_dirs = {p.name for p in (ROOT / 'handoff-materials').iterdir() if p.is_dir() and p.name != HERE.parent.name}
assert actual_dirs == {c['directory'] for c in classification}
assert len(classification) == 14
for item in classification:
    entry = ROOT / 'handoff-materials' / item['directory'] / 'MANIFEST_ja.md'
    raw = entry.read_bytes()
    item['entry'] = {'path': entry.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': digest(raw)}
    item['transfer_state'] = 'pending; no transfer or deletion performed'
counts = dict(sorted(Counter(c['category'] for c in classification).items()))
assert counts == {1: 5, 2: 6, 3: 3}
write_json('handoff-classification.json', {
    'knowledge_close_commit': KNOWLEDGE_CLOSE, 'knowledge_runtime_commit': KNOWLEDGE_RUNTIME,
    'source_commit': SOURCE, 'existing_directory_count': 14, 'counts': counts,
    'directories': classification,
    'reply_directory': {'directory': HERE.parent.name, 'category': 1,
        'destination': 'knowledge 14-evidence/records/2026-10-03-b8-scratch-close_ja.mdおよび同artifacts（命名提案）',
        'reason': '今回の全directory分類、凍結fixtureとconsumerの再採取値をb8 close／b9移管の入力として保存する'},
})
handoff_report = f'''# b8 gate close：handoff-materials分類の返却

- 搬送元: scratch-editor / Codex、作成日2026-10-03。
- branch: `agent/b8-compatibility@01cdb0bfee3a681697ffa44db5b890045b74b01c`。公開source／tag／developは`{SOURCE}`。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`のb8 CLOSED節、`00-hub/dev-repo-protocol_ja.md`、`10-protocol/protocol-tooling-migration-plan_ja.md`。
- knowledge contract commit: 指示票`{KNOWLEDGE_CLOSE}`のCLOSED節を実参照。bootstrapした最新remote main `{KNOWLEDGE_RUNTIME}`のruntime／INDEX／移管計画／既存live recordも読んだ。
- 既存14 directoryの分類: **①正式evidence候補5、②後続へ引継ぎ6、③廃棄候補3**。本返信directoryを含めると15件（①6、②6、③3）。
- これは分類と搬送素材の返却。正式配置、外部送信、directory削除、b9移管の実装は行っていない。①の新しいrecord／artifact pathは命名提案で、authoringと配置はknowledge担当。
- ③はcoordinatorによる**本文全文の着地確認と旧素材の非参照確認待ち**。summaryだけの着地で廃棄可とは扱わない。未着地の内容があれば、残して①または②へ再分類する。
- `2026-10-03-b8-publication/HANDOFF-INVENTORY_ja.md`の全②の暫定分類を本票で置き換える。以前の票／export hashは改変せず履歴として残した。

## 既存directoryの全件分類

全pathは`handoff-materials/`からの相対path。

| directory | 分類 | 移す先／引継ぎ先 | 理由 |
| --- | --- | --- | --- |
'''
for item in classification:
    handoff_report += f"| `{item['directory']}/` | {item['category']} | {item['destination']} | {item['reason']} |\n"
handoff_report += '\n## 参照identityと受領後の処理\n\n'
for item in classification:
    handoff_report += f"### {item['directory']}\n\n- 参照identity: `{item['identity']}`。\n- 次の一手: {item['next_action']}\n\n"
handoff_report += f'''## 混在素材の扱いと未完了

- 既存正式live recordは`14-evidence/records/2026-10-03-b8-dev-live_ja.md`。latest `{KNOWLEDGE_RUNTIME}`の本文にも「各担当の返却票を要約した」とある。詳細JSON・画像・再現scriptの全文移管をこのsummaryから推定しない。
- live 2 directoryの`private/`、接続先実値、認証・運用ログ、参加者名を含む原画像は①の公開搬送に含めない。保持先は②`mc-remote-backstage`担当。raw画像はhash参照を使い、公開画像へ採用する場合は別途匿名化する。
- ①のJSON／画像は正式配置前にknowledge担当がredactionを確認する。今回directory全体を公開用archiveへまとめたり、private素材を新しい返信へコピーしたりしていない。
- live-gateの`runtime/`は凍結artifactの展開物。保存済み入力との同一性を参照し、稼働サービスのpath参照終了と必要素材の移管を確認してから③へ回す。今回サービス停止・設定変更は行っていない。
- 旧candidateの大きなGUI／Bridge入力archiveを全部knowledgeへ複製する要求ではない。正式記録へticket全文・artifact identity・検証結果を移し、再取得経路／参照の要否をcoordinatorが確認した後だけ重複archiveを整理する。
- ②の受領、①の正式配置、③の確認結果は未受領。現状は全件ローカル保持。entry MANIFESTのbytes／SHA-256を`materials/handoff-classification.json`へ記録した。
- 本返信directory `2026-10-03-b8-close-inventory/` は①。同close recordとartifactへ分類一覧・fixture一覧・採取script・JSONを移す提案。fixture一覧は`10-protocol/protocol-tooling-migration-plan_ja.md`から参照するb8基線にも使う。

## fixture一覧と検証

- 完全一覧: [FIXTURES_ja.md](FIXTURES_ja.md)。公開sourceからProtocol 7、WireScope 4、Bridge 1の計12件。
- B7明示caseは93、B8は111（nearby19＋handle7＋entity7＋particle26＋sound37＋resource ID15）、signは7個の名前付きcase group。他9 fixtureの全体case数は未定義とし、構造の件数を別欄に出した。
- `git show`による12件のbytes／SHA-256と既存凍結後棚卸しとの照合PASS。readerは同sourceのtest内のrepo相対import／require／URL参照を解決して採取した。
- 全14 directoryに重複なく分類を付けたことをscriptで確認。機械可読一覧は`materials/handoff-classification.json`／`fixture-inventory.json`。
- 再採取: `python3 handoff-materials/2026-10-03-b8-close-inventory/materials/collect-inventory.py`。
- 製品source／fixtureの変更、build、live再試験、commit／pushなし。公開sourceとb9列幅branchを維持。knowledge／Stack／backstage repoへの書込みなし。
'''
(HERE.parent / 'HANDOFFS_ja.md').write_text(handoff_report)
print(json.dumps({'source': SOURCE, 'fixtures': len(fixtures), 'handoff_counts': counts,
                  'frozen_fixture_bytes_and_hashes': '12/12 matched'}, ensure_ascii=False))
