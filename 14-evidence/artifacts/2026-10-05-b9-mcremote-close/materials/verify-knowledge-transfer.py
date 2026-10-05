#!/usr/bin/env python3
"""Compare local McRemote live materials with the specified remote SSOT commit."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

COMMIT = '099c40b0c312694712653885200f3114ea4bed33'
REPO = 'Naohiro2g/mc-remote-knowledge'
LOCAL_ROOT = Path('handoff-materials')
OUTPUT = LOCAL_ROOT / '2026-10-05-b9-mcremote-close' / 'materials'
REMOTE_ROOT = '14-evidence/artifacts/2026-10-05-b9-dev-live/mcremote'
MAPPINGS = [('2026-10-05-b9-dev-restart', 'segment-0'),
            ('2026-10-05-b9-mcremote-live-auto', 'segment-1')]

def api(path):
    proc = subprocess.run(['gh', 'api', f'repos/{REPO}/contents/{path}?ref={COMMIT}'],
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return json.loads(proc.stdout)

def files_under(path):
    result = []
    for item in api(path):
        if item['type'] == 'dir':
            result.extend(files_under(item['path']))
        else:
            assert item['type'] == 'file', item['path']
            result.append(item)
    return result

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def fetch(item):
    response = api(item['path'])
    assert response['encoding'] == 'base64'
    raw = base64.b64decode(response['content'])
    assert len(raw) == item['size']
    git_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert git_blob == item['sha'] == response['sha']
    return item, raw

def main():
    comparisons = []
    remote_copy = Path(tempfile.mkdtemp(prefix='mcremote-b9-close-formal-'))
    for local_name, segment in MAPPINGS:
        remote_path = f'{REMOTE_ROOT}/{segment}'
        items = files_under(remote_path)
        local_folder = LOCAL_ROOT / local_name
        remote_relpaths = set()
        with ThreadPoolExecutor(max_workers=4) as pool:
            for item, remote_raw in pool.map(fetch, items):
                relative = str(Path(item['path']).relative_to(remote_path))
                remote_relpaths.add(relative)
                destination = remote_copy / segment / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(remote_raw)
                source = local_folder / relative
                assert source.is_file(), source
                local_raw = source.read_bytes()
                transform = None
                normalized = local_raw
                if local_name == '2026-10-05-b9-dev-restart' and relative in (
                    'materials/restart-result_ja.md', 'materials/deployment-result.json'):
                    normalized = local_raw.replace(str(Path.home()).encode() + b'/', b'~/')
                    transform = 'documented sanitization: home directory prefix -> ~/'
                entry = {'local_path': str(source), 'knowledge_path': item['path'],
                         'local_bytes': len(local_raw), 'local_sha256': sha(local_raw),
                         'knowledge_bytes': len(remote_raw), 'knowledge_sha256': sha(remote_raw),
                         'git_blob_sha': item['sha'], 'bytes_equal': local_raw == remote_raw,
                         'documented_transform': transform,
                         'after_documented_transform_equal': normalized == remote_raw}
                comparisons.append(entry)
        local_relpaths = {str(p.relative_to(local_folder)) for p in local_folder.rglob('*') if p.is_file()}
        excluded = sorted(local_relpaths - remote_relpaths)
        assert all('__pycache__' in Path(p).parts for p in excluded), excluded
        comparisons.append({'directory': local_name, 'remote_files': len(items),
                            'local_only_excluded': excluded})
    errors = [e['local_path'] for e in comparisons if 'local_path' in e and not e['after_documented_transform_equal']]
    result = {'knowledge_commit': COMMIT, 'status': 'FAIL' if errors else 'PASS',
              'errors': errors, 'comparisons': comparisons}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / 'live-transfer-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'verified_files': sum('local_path' in e for e in comparisons),
                      'exact_matches': sum(e.get('bytes_equal', False) for e in comparisons),
                      'documented_sanitization_matches': sum(bool(e.get('documented_transform')) and e['after_documented_transform_equal'] for e in comparisons),
                      'errors': errors}, ensure_ascii=False))
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
