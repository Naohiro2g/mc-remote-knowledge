from pathlib import Path
import json,hashlib,subprocess
repo=Path(__file__).resolve().parents[3]
packet=Path(__file__).resolve().parents[1]
plan=json.loads((packet/'materials/cleanup-plan.json').read_text())
assert not plan['executed'] and len(plan['files'])==232
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()=='7fbbf034488760d8fc7e034bf23f3e08e6e1807d'
subprocess.run(['git','diff','--exit-code'],cwd=repo,check=True)
subprocess.run(['git','diff','--cached','--exit-code'],cwd=repo,check=True)
process=json.loads(Path('/tmp/scratch-handoff-process-audit.json').read_text())
targets={f['path'] for f in plan['files']}
assert process['known_b9_pid_alive']
assert not targets&{f['file'] for f in process['open_file_references']+process['command_argument_references']}
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as stream:
  for data in iter(lambda:stream.read(1024*1024),b''):h.update(data)
 return h.hexdigest()
for f in plan['files']:
 relative=Path(f['path']);assert not relative.is_absolute() and '..' not in relative.parts
 assert relative.parts[0]=='handoff-materials' and 'runtime' not in relative.parts
 if 'private' in relative.parts:assert relative.parts[1:3]==('2026-10-03-b8-scratch-live-human','private') and relative.suffix=='.png'
 p=repo/relative;assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(repo/'handoff-materials')
 assert p.stat().st_size==f['bytes'] and digest(p)==f['sha256']
for f in plan['protected']:
 p=repo/f['path'];assert p.is_file()
 if f['sha256']:assert digest(p)==f['sha256']
parents=set();deleted=[]
for f in plan['files']:
 p=repo/f['path'];p.unlink();deleted.append(f['path'])
 for parent in p.parents:
  if parent==repo/'handoff-materials':break
  parents.add(parent)
empty=[]
for p in sorted(parents,key=lambda p:len(p.parts),reverse=True):
 if p.exists() and not any(p.iterdir()):p.rmdir();empty.append(str(p.relative_to(repo)))
for f in plan['protected']:
 p=repo/f['path'];assert p.is_file()
 if f['sha256']:assert digest(p)==f['sha256']
assert all(not (repo/f).exists() for f in deleted)
report={'knowledge_contract_commit':plan['knowledge_contract_commit'],'deleted_files':len(deleted),'deleted_bytes':plan['bytes'],
        'deleted_categories':plan['counts'],'deleted_source_directories':sorted(f for f in empty if len(Path(f).parts)==2),
        'removed_empty_directories':empty,'protected_files_verified':len(plan['protected']),
        'protected_non_log_bytes_unchanged':True,'all_protected_files_still_present':True,
        'references_checked':{'known_b9_pid_alive':True,'open_or_argument_reference_to_targets':False,
                             'uninspectable_processes':len(process['permission_errors']),
                             'boundary':'Some desktop and system process descriptors are inaccessible. Service launchers, runtime inputs and all temporary private/browser files are retained.'},
        'services_mutated':False,'source_mutated':False,'other_repos_mutated':False,'passed':True}
(packet/'materials/cleanup-result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
Path('/tmp/scratch-handoff-protected-before.json').write_text(json.dumps(plan.pop('protected'),ensure_ascii=False,indent=2)+'\n')
plan.update(executed=True,protected_files_verified=report['protected_files_verified'])
(packet/'materials/cleanup-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['removed_empty_directories','references_checked','deleted_source_directories']},ensure_ascii=False))
