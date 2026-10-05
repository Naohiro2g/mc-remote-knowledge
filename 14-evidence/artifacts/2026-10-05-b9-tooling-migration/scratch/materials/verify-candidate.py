import hashlib
import json
from pathlib import Path
import sys
import tarfile
import zipfile

folder = Path(__file__).parent
metadata = json.loads((folder / 'scratch-candidate-artifact.json').read_text())
run = json.loads((folder / 'scratch-candidate-run.json').read_text())
archive = Path(sys.argv[1])
expected_source = '7fbbf034488760d8fc7e034bf23f3e08e6e1807d'
assert run['conclusion'] == 'success' and run['head_sha'] == expected_source
assert metadata['workflow_run']['head_sha'] == expected_source
assert not metadata['expired'] and archive.stat().st_size == metadata['size_in_bytes']
with archive.open('rb') as stream:
    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
assert 'sha256:' + digest == metadata['digest']
with zipfile.ZipFile(archive) as z:
    manifest_bytes = z.read('candidate-manifest.json')
    manifest = json.loads(manifest_bytes)
    assert manifest['source']['commit'] == expected_source
    assert manifest['source']['repository'] == 'https://github.com/Naohiro2g/scratch-editor'
    lock = json.loads((folder / 'tooling-lock.json').read_text())
    assert manifest['tooling'] == lock['source']
    assert len(manifest['artifacts']) == 6
    assert set(z.namelist()) == {item['file'] for item in manifest['artifacts']} | {'candidate-manifest.json'}
    for item in manifest['artifacts']:
        assert z.getinfo(item['file']).file_size == item['bytes']
        with z.open(item['file']) as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == item['sha256']
        pinned = next((f for f in lock['artifacts']['files'] if f['file'] == item['file']), None)
        if pinned:
            assert item['bytes'] == pinned['bytes'] and item['sha256'] == pinned['sha256']
    def inspect_oci(file, expected_digest, source_repo, source_commit, version):
        blobs = {}
        root = None
        with z.open(file) as stream:
            with tarfile.open(fileobj=stream, mode='r|') as tar:
                for member in tar:
                    if not member.isfile() or member.size > 1024 * 1024:
                        continue
                    if member.name == 'index.json':
                        root = tar.extractfile(member).read()
                    elif member.name.startswith('blobs/sha256/'):
                        content = tar.extractfile(member).read()
                        sha = hashlib.sha256(content).hexdigest()
                        assert member.name == 'blobs/sha256/' + sha
                        blobs['sha256:' + sha] = content
        assert root is not None
        if 'sha256:' + hashlib.sha256(root).hexdigest() == expected_digest:
            doc = json.loads(root)
        else:
            assert expected_digest in [entry['digest'] for entry in json.loads(root)['manifests']]
            doc = json.loads(blobs[expected_digest])
        platforms = []
        def walk(doc):
            if 'manifests' in doc:
                for entry in doc['manifests']:
                    if entry.get('platform', {}).get('architecture') == 'unknown':
                        continue
                    walk(json.loads(blobs[entry['digest']]))
            elif 'config' in doc:
                config = json.loads(blobs[doc['config']['digest']])
                labels = config['config']['Labels']
                assert labels['org.opencontainers.image.source'] == source_repo
                assert labels['org.opencontainers.image.revision'] == source_commit
                assert labels['org.opencontainers.image.version'] == version
                platforms.append(config['os'] + '/' + config['architecture'])
        walk(doc)
        assert sorted(platforms) == ['linux/amd64', 'linux/arm64']
        return platforms
    oci = {}
    for item in manifest['artifacts']:
        if item['role'] == 'scratch':
            oci['scratch'] = inspect_oci(item['file'], item['digest'], manifest['source']['repository'],
                                         expected_source, '2320.0.0b9')
        if item['role'] == 'bridge':
            assert item['digest'] == lock['artifacts']['bridge_digest']
            oci['bridge'] = inspect_oci(item['file'], item['digest'],
                                       'https://github.com/' + lock['source']['repository'],
                                       lock['source']['commit'], 'sha-' + lock['source']['commit'])
    found = set()
    with z.open('scratch-gui.tar.gz') as stream:
        with tarfile.open(fileobj=stream, mode='r|gz') as tar:
            for entry in tar:
                if entry.name == 'build/index.html':
                    assert entry.size > 0
                    found.add('index')
                if entry.name == 'build/mc-remote-runtime-config.json':
                    runtime = json.load(tar.extractfile(entry))
                    assert runtime['schema_version'] == 1 and runtime['connection_enabled'] is False
                    found.add('runtime-config')
                if entry.name == 'build/mc-remote-product-config.json':
                    assert json.load(tar.extractfile(entry))['schema_version'] == 1
                    found.add('product-config')
                if len(found) == 3:
                    break
    assert len(found) == 3
    result = {'verified': True, 'source_commit': expected_source,
              'artifact_id': metadata['id'], 'outer_bytes': metadata['size_in_bytes'],
              'outer_sha256': digest, 'artifacts': manifest['artifacts'],
              'candidate_manifest': {'bytes': len(manifest_bytes),
                                     'sha256': hashlib.sha256(manifest_bytes).hexdigest()},
              'oci_platforms': oci, 'gui_configs_valid_and_connection_disabled': True}
    (folder / 'scratch-candidate-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    (folder / 'scratch-candidate-manifest.json').write_bytes(manifest_bytes)
    (folder / 'final-wirescope-app.manifest.json').write_bytes(z.read('wirescope-app.manifest.json'))
print(json.dumps(result, indent=2))
