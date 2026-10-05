import hashlib
import json
import shutil
import zipfile
from pathlib import Path

materials = Path(__file__).resolve().parent
root = materials.parents[2]
source = '01cdb0bfee3a681697ffa44db5b890045b74b01c'
build = root / 'mc-remote/live/dist/artifacts'
names = ['wirescope-app.zip', 'wirescope-app.manifest.json']
identities = {}
for name in names:
    target = materials / name
    shutil.copy2(build / name, target)
    blob = target.read_bytes()
    identities[name] = {'bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest()}
manifest = json.loads((materials / names[1]).read_text())
assert manifest['source']['commit'] == source
assert manifest['build']['input_identity']['source_commit'] == source
assert manifest['archive']['sha256'] == identities[names[0]]['sha256']
inputs = manifest['build']['input_identity']
assert inputs['package_json_sha256'] == hashlib.sha256((root / 'mc-remote/live/package.json').read_bytes()).hexdigest()
assert inputs['package_lock_sha256'] == hashlib.sha256((root / 'package-lock.json').read_bytes()).hexdigest()
with zipfile.ZipFile(materials / names[0]) as archive:
    assert sorted(archive.namelist()) == sorted(asset['path'] for asset in manifest['assets'])
    for asset in manifest['assets']:
        blob = archive.read(asset['path'])
        assert len(blob) == asset['bytes']
        assert hashlib.sha256(blob).hexdigest() == asset['sha256']
old = root / 'handoff-materials/2026-10-02-b8-candidate-local-fixes/materials'
baseline = root / 'handoff-materials/2026-10-03-b8-scratch-live-gate/materials/frozen-identities.json'
frozen = json.loads(baseline.read_text())
for name, expected in frozen['files'].items():
    blob = (old / name).read_bytes()
    assert len(blob) == expected['bytes']
    assert hashlib.sha256(blob).hexdigest() == expected['sha256']
fixture = frozen['b8_fixture']
blob = (root / fixture['path']).read_bytes()
assert len(blob) == fixture['bytes']
assert hashlib.sha256(blob).hexdigest() == fixture['sha256']
result = {'result': 'PASS', 'source_commit': source, 'proposed_artifacts': identities,
          'assets_verified': len(manifest['assets']), 'frozen_set_preserved': frozen['exact_set'],
          'fixture_unchanged': fixture}
(materials / 'artifact-identities.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
