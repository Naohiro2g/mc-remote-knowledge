from pathlib import Path
import hashlib
import json
import re
import tarfile
import zipfile

root = Path(__file__).resolve().parents[1]
repo = root.parents[1]
source = '7fbbf034488760d8fc7e034bf23f3e08e6e1807d'
tooling = 'dc1ab834183e29f2eb03059b07e99d2b463776ee'
tag = 'v2320.0.0b9'
candidate = (root / 'materials/frozen-candidate-workflow.yml').read_text()
release = (root / 'materials/frozen-release-workflow.yml').read_text()
candidate_version = re.findall(r'^\s+RELEASE_VERSION=(.+)$', candidate, re.MULTILINE)
release_version = re.findall(r'^\s+RELEASE_VERSION=(.+)$', release, re.MULTILINE)
assert candidate_version == ['2320.0.0b9']
assert release_version == ['${{ steps.release.outputs.tag }}']
assert (repo / '.github/workflows/mc-remote-images.yml').read_text() == release
assert (repo / '.github/workflows/mc-remote-candidate.yml').read_text() == candidate

with zipfile.ZipFile(repo / 'handoff-materials/2026-10-05-b9-tooling-migration/artifacts/scratch-candidate-7fbbf03448.zip') as archive:
    manifest = json.loads(archive.read(next(n for n in archive.namelist() if n.endswith('candidate-manifest.json'))))
    artifact = next(a for a in manifest['artifacts'] if a['role'] == 'scratch')
    assert manifest['source']['commit'] == source
    entry = next(n for n in archive.namelist() if n.endswith(artifact['file']))
    digest = hashlib.sha256()
    with archive.open(entry) as stream:
        for chunk in iter(lambda: stream.read(1048576), b''):
            digest.update(chunk)
    assert archive.getinfo(entry).file_size == artifact['bytes']
    assert digest.hexdigest() == artifact['sha256']
    blobs = {}
    with archive.open(entry) as stream, tarfile.open(fileobj=stream, mode='r|') as tar:
        for member in tar:
            if member.isfile() and member.size < 100000:
                content = tar.extractfile(member).read()
                try:
                    value = json.loads(content)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
                if member.name.startswith('blobs/sha256/'):
                    assert hashlib.sha256(content).hexdigest() == member.name.rsplit('/', 1)[1]
                blobs[member.name] = value

assert 'blobs/sha256/' + artifact['digest'].split(':', 1)[1] in blobs
configs = []
for name, blob in blobs.items():
    labels = blob.get('config', {}).get('Labels', {}) if isinstance(blob, dict) else {}
    if labels.get('org.opencontainers.image.source') == 'https://github.com/Naohiro2g/scratch-editor':
        assert labels['org.opencontainers.image.revision'] == source
        assert labels['org.opencontainers.image.version'] == candidate_version[0]
        configs.append({'config_digest': name.rsplit('/', 1)[1], 'architecture': blob['architecture'],
                        'revision': labels['org.opencontainers.image.revision'],
                        'version': labels['org.opencontainers.image.version']})
assert {config['architecture'] for config in configs} == {'amd64', 'arm64'}
scratch_ref = json.loads((root / 'materials/scratch-develop-ref.json').read_text())
tooling_ref = json.loads((root / 'materials/tooling-main-ref.json').read_text())
assert scratch_ref['object']['sha'] == source
assert tooling_ref['object']['sha'] == tooling
result = {
    'knowledge_contract_commit': 'd6d59d91032230a959b7288807179e1bd8100041',
    'exact_set': 'b9-integrated-artifact-set-1', 'tag': tag,
    'scratch_source': source, 'tooling_source': tooling,
    'frozen_scratch_oci': artifact, 'frozen_image_configs': configs,
    'candidate_release_version': candidate_version[0],
    'release_workflow_version_expression': release_version[0],
    'release_workflow_resolved_version': tag,
    'preflight_result': 'STOP: version label input mismatch prevents the frozen OCI digest from being reproduced',
    'non_claim': 'No new image was built; no actual new OCI digest or runtime failure was observed.',
    'publication_operations_performed': False,
    'scratch_b9_tag_refs': json.loads((root / 'materials/scratch-b9-tag-refs.json').read_text()),
    'tooling_b9_tag_refs': json.loads((root / 'materials/tooling-b9-tag-refs.json').read_text()),
}
(root / 'materials/release-input-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'preflight': 'STOP', 'frozen_archive_hash_verified': True,
                  'image_configs_verified': len(configs), 'remote_refs_match_frozen_sources': True,
                  'candidate_version': candidate_version[0], 'release_version': tag}, ensure_ascii=False))
