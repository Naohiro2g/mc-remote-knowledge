import copy
import hashlib
import json
import shutil
import tarfile
import zipfile
from pathlib import Path

handoff = Path(__file__).resolve().parents[1]
repository = handoff.parent.parent
source = repository / 'handoff-materials/2026-10-05-b9-tooling-migration'
archive = source / 'artifacts/scratch-candidate-7fbbf03448.zip'
expected_commit = '7fbbf034488760d8fc7e034bf23f3e08e6e1807d'
expected_tooling = 'dc1ab834183e29f2eb03059b07e99d2b463776ee'
runtime = handoff / 'runtime'
artifacts = handoff / 'artifacts'
private = handoff / 'private'
for directory in (runtime, artifacts, private):
    directory.mkdir(parents=True, exist_ok=True)

with archive.open('rb') as stream:
    assert hashlib.file_digest(stream, 'sha256').hexdigest() == (
        '27ade4f9b3d6a1e4b0cf814ef346b75613df8e8d446c82793b345665be9c4d7c')
with zipfile.ZipFile(archive) as package:
    manifest_bytes = package.read('candidate-manifest.json')
    assert hashlib.sha256(manifest_bytes).hexdigest() == (
        '239f7f94cf31e732eff173744da105408b00b182d0aad73507623ea09b43bc6b')
    manifest = json.loads(manifest_bytes)
    assert manifest['source']['commit'] == expected_commit
    assert manifest['tooling']['commit'] == expected_tooling
    assert manifest['version'] == '2320.0.0b9'
    (artifacts / 'candidate-manifest.json').write_bytes(manifest_bytes)
    used = [item for item in manifest['artifacts'] if item['role'] in (
        'scratch-gui', 'bridge', 'wirescope', 'wirescope-manifest')]
    for item in used:
        destination = artifacts / item['file']
        with package.open(item['file']) as stream, destination.open('wb') as output:
            shutil.copyfileobj(stream, output)
        assert destination.stat().st_size == item['bytes']
        with destination.open('rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == item['sha256']

scratch = runtime / 'scratch'
scratch.mkdir(exist_ok=True)
with tarfile.open(artifacts / 'scratch-gui.tar.gz', 'r:gz') as package:
    assert all(item.name == 'build' or item.name.startswith('build/') for item in package)
    package.extractall(scratch, filter='data')
wirescope = runtime / 'wirescope'
wirescope.mkdir(exist_ok=True)
with zipfile.ZipFile(artifacts / 'wirescope-app.zip') as package:
    for name in package.namelist():
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
    package.extractall(wirescope)

bridge_artifact = next(item for item in used if item['role'] == 'bridge')
bridge = runtime / 'bridge'
bridge.mkdir(exist_ok=True)
with tarfile.open(artifacts / 'bridge.oci.tar', 'r:') as package:
    def blob(digest):
        return package.extractfile('blobs/sha256/' + digest.split(':')[1])

    index_bytes = package.extractfile('index.json').read()
    if 'sha256:' + hashlib.sha256(index_bytes).hexdigest() == bridge_artifact['digest']:
        index = json.loads(index_bytes)
    else:
        assert bridge_artifact['digest'] in [item['digest'] for item in json.loads(index_bytes)['manifests']]
        index = json.load(blob(bridge_artifact['digest']))
    selected = next(item for item in index['manifests'] if item.get('platform') == {
        'architecture': 'amd64', 'os': 'linux'})
    image = json.load(blob(selected['digest']))
    config = json.load(blob(image['config']['digest']))
    assert config['config']['Labels']['org.opencontainers.image.revision'] == expected_tooling
    assert config['config']['Labels']['org.opencontainers.image.source'] == (
        'https://github.com/Naohiro2g/minecraft-remote-tooling')
    for layer in image['layers']:
        with blob(layer['digest']) as stream:
            assert 'sha256:' + hashlib.file_digest(stream, 'sha256').hexdigest() == layer['digest']
        with tarfile.open(fileobj=blob(layer['digest']), mode='r:*') as content:
            for item in content:
                name = item.name.removeprefix('./')
                if not name.startswith('app/') or name == 'app/':
                    continue
                item = copy.copy(item)
                item.name = name.removeprefix('app/')
                assert '..' not in Path(item.name).parts
                assert not Path(item.name).name.startswith('.wh.')
                assert item.isfile() or item.isdir()
                content.extract(item, bridge, filter='data')
assert (bridge / 'dist/main.js').is_file()
assert (bridge / 'node_modules/ws/index.js').is_file()

settings = json.loads((repository / 'handoff-materials/2026-10-03-b8-scratch-live-gate/private/deployment.json').read_text())
assert settings['runtime_config']['connection_enabled'] is True
assert 'http://localhost:8611' in settings['bridge_env']['BRIDGE_ORIGIN_ALLOWLIST'].split(',')
(private / 'deployment.json').write_text(json.dumps(settings, ensure_ascii=False, indent=2) + '\n')
shutil.copyfile(repository / 'handoff-materials/2026-10-03-b8-scratch-live-gate/private/start-local.cjs',
                private / 'start-local.cjs')
identity = {
    'source': manifest['source'], 'version': manifest['version'], 'tooling': manifest['tooling'],
    'artifacts': used, 'bridge_platform': 'linux/amd64',
    'bridge_execution': 'OCI /app files extracted; host-native Node, not container execution',
    'runtime_files': [
        {'path': str(path.relative_to(runtime)), 'bytes': path.stat().st_size,
         'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted(runtime.rglob('*')) if path.is_file()
    ],
}
(handoff / 'materials/runtime-identity.json').write_text(json.dumps(identity, indent=2) + '\n')
print('Prepared frozen b9 GUI, Bridge and WireScope:', manifest['source']['commit'])
print('Runtime files verified:', len(identity['runtime_files']))
