from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,csv,base64,hashlib
repo=Path(__file__).resolve().parents[3]
packet=Path(__file__).resolve().parents[1]
sha='5beaad2557abbc6e90ada03edf7d0a2918fa7a52'
tree=json.loads(Path('/tmp/scratch-cleanup-knowledge-tree.json').read_text())
assert tree['sha']==sha and not tree.get('truncated')
entries={e['path']:e for e in tree['tree'] if e['type']=='blob'}
rows=list(csv.DictReader((packet/'materials/evidence-source-inventory.tsv').open(),delimiter='\t'))
for source in sorted((repo/'handoff-materials/2026-10-05-b9-close').rglob('*')):
 if source.is_file():
  relative=str(source.relative_to(repo/'handoff-materials/2026-10-05-b9-close'))
  data=source.read_bytes()
  rows.append({'directory':'2026-10-05-b9-close','path':relative,'bytes':str(len(data)),
               'sha256':hashlib.sha256(data).hexdigest(),
               'proposed_knowledge_path':'14-evidence/artifacts/2026-10-05-b9-release/scratch/close/'+relative})
prefix='14-evidence/artifacts/2026-10-05-b9-dev-live/scratch/segment-3/'
known={f['proposed_knowledge_path'] for f in rows}
for path in sorted(entries):
 if path.startswith(prefix) and path not in known:
  relative=path[len(prefix):]; source=repo/'handoff-materials/2026-10-05-b9-scratch-dev'/relative
  data=source.read_bytes()
  rows.append({'directory':'2026-10-05-b9-scratch-dev','path':relative,'bytes':str(len(data)),
               'sha256':hashlib.sha256(data).hexdigest(),'proposed_knowledge_path':path})
expected_changed={
 '2026-09-30-block-picker-names/materials/browser-smoke.log',
 '2026-10-03-wirescope-column-width/materials/artifact-build.log',
 '2026-10-03-wirescope-column-width/materials/build.log',
 '2026-10-03-wirescope-column-width/materials/test.log'}
cache=Path('/tmp/scratch-cleanup-evidence-blobs');cache.mkdir(exist_ok=True)
def verify(f):
 relative=Path(f['directory'])/f['path']; source=repo/'handoff-materials'/relative
 original=source.read_bytes()
 assert len(original)==int(f['bytes']) and hashlib.sha256(original).hexdigest()==f['sha256']
 entry=entries[f['proposed_knowledge_path']]
 saved=cache/entry['sha']
 if saved.exists():data=saved.read_bytes()
 else:
  blob=json.loads(subprocess.check_output(['gh','api','repos/Naohiro2g/mc-remote-knowledge/git/blobs/'+entry['sha']],timeout=60))
  data=base64.b64decode(blob['content']);saved.write_bytes(data)
 assert len(data)==entry['size'] and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['sha']
 if str(relative) in expected_changed:
  assert data==original.replace(str(Path.home()).encode(),b'~')
  comparison='home path replacement only'
 else:
  assert data==original
  comparison='full bytes equal'
 return {'source':'handoff-materials/'+str(relative),'source_bytes':len(original),'source_sha256':f['sha256'],
         'knowledge_path':entry['path'],'knowledge_bytes':len(data),'knowledge_sha256':hashlib.sha256(data).hexdigest(),
         'knowledge_git_blob_sha':entry['sha'],'comparison':comparison,'passed':True}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(verify,rows))
assert len(results)==180
report={'knowledge_contract_commit':sha,'files':results,'passed':True,'full_bytes_equal':176,'home_path_replacement_only':4,
        'source_bytes':sum(r['source_bytes'] for r in results),'deleted':False}
(packet/'materials/evidence-receipt-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='files'}))
