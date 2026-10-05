"""Read-only verification of the authorized b9 release and package indexes."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

VERSION = '2320.0.0b9'
TAG = 'v' + VERSION
SOURCE = 'b901c88fe41b67530ff353271683ece9fd453076'
TOOLING = 'dc1ab834183e29f2eb03059b07e99d2b463776ee'
EXPECTED = {
    'minecraft_remote_api-2320.0.0b9-py3-none-any.whl': (196221, 'e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6'),
    'minecraft_remote_api-2320.0.0b9.tar.gz': (190627, 'bd027b8b94ff775bfb7a3c02ada9716ad8785e5499180bb0cfb26f1da4afe479'),
}
OUT = Path(__file__).resolve().parent


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'mc-remote-b9-release-verification'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def api(path):
    return json.loads(subprocess.run(['gh', 'api', 'repos/Naohiro2g/minecraft-remote-api/' + path], capture_output=True, text=True, check=True).stdout)


def verify_file(name, body):
    actual = (len(body), hashlib.sha256(body).hexdigest())
    assert actual == EXPECTED[name], name
    return {'file': name, 'bytes': actual[0], 'sha256': actual[1]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('channel', choices=('release', 'testpypi', 'pypi'))
    channel = parser.parse_args().channel
    report = {'channel': channel, 'version': VERSION, 'source_commit': SOURCE,
              'knowledge_contract_commit': '6df2d14033a4646ce958737c06849725fcaee51e',
              'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'status': 'FAIL'}
    try:
        if channel == 'release':
            release = api('releases/tags/' + TAG)
            assert release['prerelease'] and not release['draft']
            assert release['name'] == 'minecraft-remote-api ' + VERSION
            assert api('git/ref/tags/' + TAG)['object']['sha'] == SOURCE
            assert api('git/ref/heads/main')['object']['sha'] == SOURCE
            latest = api('releases/latest')['tag_name']
            assert latest == 'v1214.10.11'
            report.update(release_id=release['id'], url=release['html_url'], prerelease=True, draft=False, latest=latest)
            assets = {item['name']: item for item in release['assets']}
            assert set(assets) == set(EXPECTED) | {'manifest.json'}
            rows = []
            for name in list(EXPECTED) + ['manifest.json']:
                asset = assets[name]
                body = fetch(asset['browser_download_url'])
                sha = hashlib.sha256(body).hexdigest()
                assert len(body) == asset['size'] and 'sha256:' + sha == asset['digest']
                if name in EXPECTED:
                    row = verify_file(name, body)
                else:
                    row = {'file': name, 'bytes': len(body), 'sha256': sha}
                    manifest = json.loads(body)
                    assert manifest['release_tag'] == TAG and manifest['source_commit'] == SOURCE
                    assert manifest['bundled_wirescope_source_commit'] == TOOLING
                    assert {a['file']: a['sha256'] for a in manifest['artifacts']} == {n: s for n, (_, s) in EXPECTED.items()}
                    (OUT / 'release-manifest.json').write_bytes(body)
                rows.append({**row, 'url': asset['browser_download_url'], 'anonymous_download': True})
            report['artifacts'] = rows
        else:
            domain = 'test.pypi.org' if channel == 'testpypi' else 'pypi.org'
            url = f'https://{domain}/pypi/minecraft-remote-api/{VERSION}/json'
            published = json.loads(fetch(url))
            assert published['info']['version'] == VERSION
            entries = {item['filename']: item for item in published['urls']}
            assert set(entries) == set(EXPECTED)
            rows = []
            for name, (size, sha) in EXPECTED.items():
                entry = entries[name]
                assert entry['size'] == size and entry['digests']['sha256'] == sha and not entry['yanked']
                row = verify_file(name, fetch(entry['url']))
                rows.append({**row, 'url': entry['url'], 'yanked': False})
            report.update(url=f'https://{domain}/project/minecraft-remote-api/{VERSION}/', metadata_url=url, artifacts=rows)
        report['status'] = 'PASS'
    finally:
        (OUT / (channel + '-verification.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(channel + ': PASS (published file bytes/SHA-256 match frozen identity)')


if __name__ == '__main__':
    main()
