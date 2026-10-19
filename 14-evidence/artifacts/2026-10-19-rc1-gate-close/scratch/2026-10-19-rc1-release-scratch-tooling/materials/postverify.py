import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, '/tmp/codex-rc1-release-scratch')
from verify_frozen import ROOT, COMMON, SCRATCH, TOOLING_SOURCE, SCRATCH_SOURCE, hashfile


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path]))


receipts = []
for repo, branch, head, tag_source, expected, run in [
    ('minecraft-remote-tooling', 'main', TOOLING_SOURCE, TOOLING_SOURCE, COMMON, 39053886890),
    ('scratch-editor', 'develop', 'f20e55eb53f192eab6cdc4f0d5aae4f52b2dc8db', SCRATCH_SOURCE,
     {k: v for k, v in SCRATCH.items() if k not in ['scratch.oci.tar', 'bridge.oci.tar']}, 39072595749),
]:
    prefix = f'repos/Naohiro2g/{repo}'
    release = api(prefix + '/releases/tags/v2321.0.0rc1')
    assert release['draft'] is False and release['prerelease'] is True
    assert api(prefix + f'/git/ref/heads/{branch}')['object']['sha'] == head
    assert api(prefix + '/commits/v2321.0.0rc1')['sha'] == tag_source
    tag_ref = api(prefix + '/git/ref/tags/v2321.0.0rc1')
    if repo == 'scratch-editor':
        manifest = ROOT / 'scratch/manifest.json'
        expected = {**expected, 'manifest.json': (manifest.stat().st_size, hashfile(manifest))}
    assert set(a['name'] for a in release['assets']) == set(expected)
    for asset in release['assets']:
        size, sha = expected[asset['name']]
        assert (asset['size'], asset['digest'], asset['state']) == (size, 'sha256:' + sha, 'uploaded')
        if asset['name'] == 'manifest.json':
            data = subprocess.check_output(['gh', 'api', '-H', 'Accept: application/octet-stream',
                prefix + '/releases/assets/' + str(asset['id'])])
            assert (len(data), hashlib.sha256(data).hexdigest()) == (size, sha)
            (ROOT / 'scratch-public-manifest.json').write_bytes(data)
    latest = subprocess.run(['gh', 'api', prefix + '/releases/latest'], capture_output=True, text=True)
    if latest.returncode == 0:
        latest_tag = json.loads(latest.stdout)['tag_name']
        assert latest_tag != 'v2321.0.0rc1'
    else:
        assert '404' in latest.stderr, latest.stderr
        latest_tag = None
    receipt = dict(repository=f'Naohiro2g/{repo}', default_branch=branch, default_branch_head=head,
        tag='v2321.0.0rc1', tag_commit=tag_source, tag_ref=tag_ref,
        release_id=release['id'], release_url=release['html_url'], published_at=release['published_at'],
        prerelease=release['prerelease'], draft=release['draft'], latest_release_tag=latest_tag,
        candidate_run_id=run, public_run_id=None, publication_method='CLI promotion of frozen artifacts',
        assets=[{key: asset[key] for key in ['id', 'name', 'size', 'digest', 'browser_download_url']}
                for asset in release['assets']])
    receipts.append(receipt)
    print(repo + ': public release, branch, tag, latest and all asset digests PASS', flush=True)
assert receipts[0]['published_at'] < receipts[1]['published_at']
state = api('repos/Naohiro2g/scratch-editor/actions/workflows/mc-remote-images.yml')['state']
assert state == 'active', state
(ROOT / 'public-release-receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
print('Publication order and automatic workflow restoration: PASS')
