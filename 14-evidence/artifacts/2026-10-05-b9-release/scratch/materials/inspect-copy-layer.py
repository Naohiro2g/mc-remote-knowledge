from pathlib import Path
import hashlib
import json
import tarfile
import zipfile

root = Path(__file__).resolve().parents[1]
repo = root.parents[1]
comparison = json.loads((root / 'materials/scratch-oci-comparison.json').read_text())
frozen = repo / 'handoff-materials/2026-10-05-b9-tooling-migration/artifacts/scratch-candidate-7fbbf03448.zip'
rebuilt = root / 'artifacts/scratch-release-preflight-7fbbf03448.zip'


def inspect(path, requested):
    result = {}
    with zipfile.ZipFile(path) as archive:
        manifest = json.loads(archive.read(next(name for name in archive.namelist() if name.endswith('candidate-manifest.json'))))
        entry = next(name for name in archive.namelist() if name.endswith('scratch.oci.tar'))
        with archive.open(entry) as stream, tarfile.open(fileobj=stream, mode='r|') as outer:
            for member in outer:
                digest = 'sha256:' + member.name.rsplit('/', 1)[-1]
                if digest not in requested or not member.isfile():
                    continue
                records = {}
                with tarfile.open(fileobj=outer.extractfile(member), mode='r|*') as layer:
                    for item in layer:
                        content_hash = None
                        if item.isfile():
                            content_hash = hashlib.sha256()
                            with layer.extractfile(item) as data:
                                for chunk in iter(lambda: data.read(1048576), b''):
                                    content_hash.update(chunk)
                            content_hash = content_hash.hexdigest()
                        assert item.name not in records
                        records[item.name] = {
                            'type': item.type.decode(), 'linkname': item.linkname,
                            'size': item.size, 'content_sha256': content_hash,
                            'mode': item.mode, 'uid': item.uid, 'gid': item.gid,
                            'uname': item.uname, 'gname': item.gname,
                            'mtime': item.mtime, 'pax_headers': item.pax_headers,
                        }
                result[digest] = records
    assert set(result) == set(requested)
    return manifest, result


requested_old = {platform['frozen_layers'][-1] for platform in comparison['platforms']}
requested_new = {platform['rebuilt_layers'][-1] for platform in comparison['platforms']}
old_manifest, old_layers = inspect(frozen, requested_old)
new_manifest, new_layers = inspect(rebuilt, requested_new)
results = []
content_keys = ('type', 'linkname', 'size', 'content_sha256')
for platform in comparison['platforms']:
    old = old_layers[platform['frozen_layers'][-1]]
    new = new_layers[platform['rebuilt_layers'][-1]]
    added = sorted(new.keys() - old.keys())
    removed = sorted(old.keys() - new.keys())
    content_changes = []
    metadata_changes = []
    for name in sorted(old.keys() & new.keys()):
        if any(old[name][key] != new[name][key] for key in content_keys):
            content_changes.append({'path': name, 'before': {key: old[name][key] for key in content_keys},
                                    'after': {key: new[name][key] for key in content_keys}})
        metadata = {key: {'before': old[name][key], 'after': new[name][key]}
                    for key in old[name] if key not in content_keys and old[name][key] != new[name][key]}
        if metadata:
            metadata_changes.append({'path': name, 'changes': metadata})
    fields = sorted({key for item in metadata_changes for key in item['changes']})
    results.append({'architecture': platform['architecture'], 'frozen_entry_count': len(old),
                    'rebuilt_entry_count': len(new), 'added_paths': added, 'removed_paths': removed,
                    'content_changes': content_changes, 'metadata_change_count': len(metadata_changes),
                    'metadata_changed_fields': fields, 'metadata_changes': metadata_changes,
                    'file_contents_types_and_links_equal': not (added or removed or content_changes)})
old_gui = next(item for item in old_manifest['artifacts'] if item['role'] == 'scratch-gui')
new_gui = next(item for item in new_manifest['artifacts'] if item['role'] == 'scratch-gui')
report = {'knowledge_contract_commit': 'ede3d0fc8d548e76eefadc93b6dd415f9dce7b1b',
          'normalized_gui_archive': {'frozen': old_gui, 'rebuilt': new_gui,
                                     'sha256_equal': old_gui['sha256'] == new_gui['sha256']},
          'platforms': results,
          'publication_still_stopped': True,
          'non_claim': 'File-level inspection does not override the coordinator condition requiring identical layer digests.'}
(root / 'materials/copy-layer-inspection.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'normalized_gui_sha256_equal': report['normalized_gui_archive']['sha256_equal'],
                  'platforms': [{key: item[key] for key in ('architecture', 'frozen_entry_count',
                                'rebuilt_entry_count', 'file_contents_types_and_links_equal',
                                'metadata_change_count', 'metadata_changed_fields')} for item in results]}))
