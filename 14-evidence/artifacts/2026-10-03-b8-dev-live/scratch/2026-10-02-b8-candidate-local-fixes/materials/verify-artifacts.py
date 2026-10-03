from pathlib import Path
import hashlib
import json
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
MATERIALS = Path(__file__).resolve().parent
SOURCE = '691576f60b7f0824e1753bd6823901d01fbe2422'
FIXTURE_SHA = 'ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2'

def sha256(data):
    return hashlib.sha256(data).hexdigest()

assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == SOURCE
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], cwd=ROOT, text=True).strip()
fixture_path = ROOT / 'mc-remote/protocol/test/fixtures/entity-particle-v23.2.json'
fixture_bytes = fixture_path.read_bytes()
assert sha256(fixture_bytes) == FIXTURE_SHA
fixture = json.loads(fixture_bytes)
case_counts = {key: len(value['cases']) for key, value in fixture.items()
               if isinstance(value, dict) and isinstance(value.get('cases'), list)}
case_counts['nearby.handle_transaction_cases'] = len(fixture['nearby']['handle_transaction_cases'])
assert sum(case_counts.values()) == 111

manifest = json.loads((MATERIALS / 'wirescope-app.manifest.json').read_text())
assert manifest['source']['commit'] == SOURCE
assert manifest['build']['input_identity']['source_commit'] == SOURCE
assert manifest['build']['input_identity']['package_lock_sha256'] == sha256((ROOT/'package-lock.json').read_bytes())
assert manifest['build']['input_identity']['package_json_sha256'] == sha256((ROOT/'mc-remote/live/package.json').read_bytes())
archive = MATERIALS / 'wirescope-app.zip'
assert manifest['archive']['sha256'] == sha256(archive.read_bytes())
with zipfile.ZipFile(archive) as zipped:
    assert set(zipped.namelist()) == {asset['path'] for asset in manifest['assets']}
    for asset in manifest['assets']:
        data = zipped.read(asset['path'])
        assert len(data) == asset['bytes'] and sha256(data) == asset['sha256'], asset['path']

archive_counts = {}
for filename, source_directory, inputs in [
    ('scratch-image-inputs.tar.gz', ROOT/'packages/scratch-gui', ['Dockerfile.mc-remote', 'build']),
    ('bridge-image-inputs.tar.gz', ROOT/'mc-remote/bridge', ['Dockerfile', 'package.json', 'dist', 'node_modules/ws']),
    ('contracts.tar.gz', ROOT/'packages/scratch-gui', ['contracts']),
]:
    expected = set()
    for name in inputs:
        path = source_directory / name
        if path.is_file(): expected.add(name)
        else: expected.update(p.relative_to(source_directory).as_posix() for p in path.rglob('*') if p.is_file())
    with tarfile.open(MATERIALS/filename) as packed:
        members = packed.getmembers()
        actual = {member.name for member in members if member.isfile()}
        assert actual == expected, (filename, actual ^ expected)
        for member in members:
            assert member.uid == member.gid == 0 and member.mtime == 315532800, member.name
            assert member.isdir() or member.isfile(), member.name
            if member.isfile():
                data = packed.extractfile(member).read()
                assert sha256(data) == sha256((source_directory/member.name).read_bytes()), member.name
        archive_counts[filename] = len(actual)
        if filename == 'scratch-image-inputs.tar.gz':
            config = json.loads(packed.extractfile('build/mc-remote-runtime-config.json').read())
            assert config['schema_version'] == 1 and config['connection_enabled'] is False
        if filename == 'bridge-image-inputs.tar.gz':
            ws_version = json.loads(packed.extractfile('node_modules/ws/package.json').read())['version']
            assert ws_version == '8.18.3'

files = {}
previous = ROOT/'handoff-materials/2026-10-01-b8-candidate-b7-fixes/materials'
for filename in ['scratch-image-inputs.tar.gz', 'bridge-image-inputs.tar.gz',
                 'wirescope-app.zip', 'wirescope-app.manifest.json', 'contracts.tar.gz']:
    data = (MATERIALS/filename).read_bytes()
    files[filename] = {'bytes':len(data), 'sha256':sha256(data),
                       'unchanged_from_previous_candidate':data == (previous/filename).read_bytes()}
assert files['bridge-image-inputs.tar.gz']['unchanged_from_previous_candidate']
assert files['wirescope-app.zip']['unchanged_from_previous_candidate']
assert files['contracts.tar.gz']['unchanged_from_previous_candidate']
assert not files['scratch-image-inputs.tar.gz']['unchanged_from_previous_candidate']
assert not files['wirescope-app.manifest.json']['unchanged_from_previous_candidate']
result = {'result':'PASS', 'test_class':'unit/deterministic', 'source_commit':SOURCE,
          'fixture':{'bytes':len(fixture_bytes), 'sha256':FIXTURE_SHA,
                     'case_count':sum(case_counts.values()), 'case_groups':case_counts},
          'wirescope_assets':len(manifest['assets']), 'archive_file_counts':archive_counts,
          'bridge_ws_version':ws_version, 'gui_runtime_config':{'schema_version':1,'connection_enabled':False},
          'files':files}
(MATERIALS/'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
