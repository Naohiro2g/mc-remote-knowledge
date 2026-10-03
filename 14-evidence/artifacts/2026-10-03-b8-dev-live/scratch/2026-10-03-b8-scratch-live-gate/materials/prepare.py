from pathlib import Path
import hashlib
import json
import re
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
MATERIALS = Path(__file__).resolve().parent
HANDOFF = MATERIALS.parent
SOURCE = '691576f60b7f0824e1753bd6823901d01fbe2422'
KNOWLEDGE = '749ba60dc8c18938e50ce66b8e820aac4401c69e'
ARTIFACTS = ROOT / 'handoff-materials/2026-10-02-b8-candidate-local-fixes/materials'

assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == SOURCE
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], cwd=ROOT, text=True).strip()
fixture_rows = []
for owner, directory in [('Protocol', 'mc-remote/protocol/test/fixtures'),
                         ('WireScope', 'mc-remote/live/test/fixtures'),
                         ('Bridge', 'mc-remote/bridge/test/fixtures')]:
    for path in sorted((ROOT / directory).iterdir()):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        assert data == subprocess.check_output(['git', 'show', SOURCE + ':' + relative], cwd=ROOT)
        record = {'owner': owner, 'path': relative, 'bytes': len(data),
                  'sha256': hashlib.sha256(data).hexdigest()}
        if path.suffix == '.json':
            fixture = json.loads(data)
            if isinstance(fixture, dict):
                record['schema'] = fixture.get('schema') or fixture.get('schema_version')
                record['protocol'] = fixture.get('protocol')
            ids = re.findall(r'"id"\s*:\s*"(B[78]-[^\"]+)"', data.decode())
            if ids:
                record['explicit_case_ids'] = len(ids)
        elif path.suffix == '.ndjson':
            record['line_count'] = len(data.splitlines())
        fixture_rows.append(record)
assert len(fixture_rows) == 12
b8 = next(record for record in fixture_rows if record['path'].endswith('entity-particle-v23.2.json'))
assert b8['bytes'] == 36481 and b8['explicit_case_ids'] == 111
assert b8['sha256'] == 'ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2'
expected = json.loads((ARTIFACTS / 'verification.json').read_text())
identities = {}
for name, record in expected['files'].items():
    data = (ARTIFACTS / name).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert len(data) == record['bytes'] and digest == record['sha256'], name
    identities[name] = {'bytes': len(data), 'sha256': digest}
manifest = json.loads((ARTIFACTS / 'wirescope-app.manifest.json').read_text())
assert manifest['source']['commit'] == SOURCE
(MATERIALS / 'frozen-identities.json').write_text(json.dumps({
    'exact_set': 'b8-integrated-artifact-set-1', 'knowledge_commit': KNOWLEDGE,
    'source_commit': SOURCE, 'files': identities, 'b8_fixture': b8,
    'result': 'PASS', 'live_started': False,
}, ensure_ascii=False, indent=2) + '\n')
(MATERIALS / 'fixture-inventory.json').write_text(json.dumps({
    'source_commit': SOURCE, 'knowledge_commit': KNOWLEDGE, 'fixtures': fixture_rows,
}, ensure_ascii=False, indent=2) + '\n')
with (MATERIALS / 'fixture-consumers.txt').open('w') as destination:
    result = subprocess.run([
        'git', 'grep', '-n', '-E', 'fixtures/|@mc-remote/protocol', SOURCE, '--',
        'mc-remote/protocol/test', 'mc-remote/live/src', 'mc-remote/live/test',
        'mc-remote/bridge/src', 'mc-remote/bridge/test',
        'packages/scratch-vm/src/extensions/scratch3_mcremote', 'packages/scratch-vm/test/unit',
        'packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js',
        '.github/workflows/mc-remote-images.yml',
    ], cwd=ROOT, stdout=destination, text=True)
    assert result.returncode in (0, 1)
for filename, label in [('scratch-image-inputs.tar.gz', 'scratch'),
                        ('bridge-image-inputs.tar.gz', 'bridge')]:
    destination = HANDOFF / 'runtime' / label
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(ARTIFACTS / filename) as archive:
        archive.extractall(destination, filter='data')
        for member in archive.getmembers():
            if member.isfile():
                assert archive.extractfile(member).read() == (destination / member.name).read_bytes()
destination = HANDOFF / 'runtime/wirescope'
destination.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(ARTIFACTS / 'wirescope-app.zip') as archive:
    assert set(archive.namelist()) == {asset['path'] for asset in manifest['assets']}
    for asset in manifest['assets']:
        path = destination / asset['path']
        path.parent.mkdir(parents=True, exist_ok=True)
        data = archive.read(asset['path'])
        assert len(data) == asset['bytes'] and hashlib.sha256(data).hexdigest() == asset['sha256']
        path.write_bytes(data)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == asset['sha256']
print('PASS: 12 fixture inventories from frozen Git source; artifact identities and staged contents verified.')
print('No listener started; no remote connection or Minecraft operation.')
