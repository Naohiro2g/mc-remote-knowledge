import hashlib
import json
from pathlib import Path
import subprocess
import tarfile

ROOT = Path('/tmp/codex-rc1-release-scratch')
TOOLING_SOURCE = '6447f6e8cbfbeeb9d229990b5c4f6e82a5875666'
SCRATCH_SOURCE = 'ec79b3b0e364e722d6926a0932eb4bf088ddd3a1'
COMMON = {
    'wirescope-app.zip': (83854, 'da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad'),
    'wirescope-app.manifest.json': (2339, '3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235'),
    'bridge.oci.tar': (114626048, '3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c'),
}
SCRATCH = {
    **COMMON,
    'mc-remote-scratch-LAN-2321.0.0rc1-windows-x64.zip': (261848009, '86bbaf9a278683315ffe2ebd4f19d56ba53f5501289e4cddfc22f284d8d4e209'),
    'mc-remote-scratch-LAN-2321.0.0rc1-macos-arm64.zip': (266199673, 'bdfff47b8c1210a359ed65a8be6fca26624546e3c04add125063968acc091412'),
    'mc-remote-scratch-LAN-2321.0.0rc1-linux-x64.zip': (271455727, 'b76b574803c58403e38438d2569917bd72ca95f039026f12ed3a294edfcfba54'),
    'scratch-gui.tar.gz': (138835708, '2dafb257c511989946da021591191cc1501e0d1a9211cc559373ed7de30f19c2'),
    'contracts.tar.gz': (1908, '48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390'),
    'scratch.oci.tar': (325822464, '88d81fba1aca0194c85f638cf19c66a1a2087748f32ff501bdb1dd283ea1d0c5'),
}
DIGESTS = {
    'bridge.oci.tar': '305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf',
    'scratch.oci.tar': '75e76edb6b8a1de4fb896184b5c26bed7cb1791296f82903e6b1ec4a1a5ab840',
}


def hashfile(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


if __name__ == '__main__':
    results = []
    for label, expected, commit in [('tooling', COMMON, TOOLING_SOURCE), ('scratch', SCRATCH, SCRATCH_SOURCE)]:
        manifest = json.loads((ROOT / label / 'candidate-manifest.json').read_text())
        assert manifest['source']['commit'] == commit
        for filename, (size, sha) in expected.items():
            path = ROOT / label / filename
            actual = hashfile(path)
            assert (path.stat().st_size, actual) == (size, sha), filename
            result = dict(component=label, file=filename, bytes=size, sha256=sha, frozen_match=True)
            if filename in DIGESTS:
                with tarfile.open(path) as archive:
                    layout = json.loads(archive.extractfile('index.json').read())
                    assert len(layout['manifests']) == 1
                    descriptor = layout['manifests'][0]
                    body = archive.extractfile('blobs/' + descriptor['digest'].replace(':', '/')).read()
                index_sha = hashlib.sha256(body).hexdigest()
                assert descriptor['digest'] == f'sha256:{index_sha}'
                assert index_sha == DIGESTS[filename], filename
                result['digest'] = f'sha256:{index_sha}'
            results.append(result)
    fixtures = {
        'chat-event-compat-v23.2.1.json': (32384, 'eead244a7340c315cb63e1e77ede0fe9cf48162c06fedbeef36d941950d5000d'),
        'entity-particle-v23.2.1.json': (36483, '0319ff8373a96798cf5e9e421a804729fd33a0fa53e96adc12c93ed7994777ae'),
    }
    for name, expected in fixtures.items():
        data = subprocess.check_output(['git', '-C', '/tmp/mc-remote-tooling-rc1', 'show',
            f'{TOOLING_SOURCE}:packages/protocol/test/fixtures/{name}'])
        assert (len(data), hashlib.sha256(data).hexdigest()) == expected, name
        results.append(dict(component='tooling-fixture', file=name, bytes=expected[0], sha256=expected[1], frozen_match=True))
    (ROOT / 'frozen-verification.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'PASS: {len(results)} file identities; both OCI index digests match frozen values')
