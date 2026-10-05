from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,base64,hashlib
sha='099c40b0c312694712653885200f3114ea4bed33'
prefix='14-evidence/artifacts/2026-10-05-b9-dev-live/scratch/segment-3/'
tree=json.loads(Path('/tmp/b9-close-knowledge-tree.json').read_text())
entries=[e for e in tree['tree'] if e['type']=='blob' and e['path'].startswith(prefix)]
root=Path('handoff-materials/2026-10-05-b9-scratch-dev')
cache=Path('/tmp/b9-close-landed-segment3');cache.mkdir(exist_ok=True)
def verify(entry):
 rel=entry['path'][len(prefix):]
 blob=json.loads(subprocess.check_output(['gh','api','repos/Naohiro2g/mc-remote-knowledge/git/blobs/'+entry['sha']],timeout=90))
 data=base64.b64decode(blob['content'])
 assert len(data)==entry['size']
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['sha']
 before=(root/rel).read_bytes()
 p=cache/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 return {'source':str(root/rel),'knowledge_path':entry['path'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
         'local_sha256':hashlib.sha256(before).hexdigest(),'full_bytes_equal':data==before,'knowledge_git_blob_sha':entry['sha']}
with ThreadPoolExecutor(max_workers=4) as executor:results=list(executor.map(verify,entries))
report={'knowledge_contract_commit':sha,'knowledge_contract_path':'00-hub/b9-gate-close-instructions_ja.md',
        'directory':'2026-10-05-b9-scratch-dev','files':results,'passed':all(r['full_bytes_equal'] for r in results),
        'not_included':['private/','runtime/','artifacts/','materials/picker-door.png','materials/picker-gold.png','materials/wirescope-b9-columns.png','materials/wirescope-b9.png']}
p=Path('handoff-materials/2026-10-05-b9-close/materials/landed-evidence-verification.json');p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'files':len(results),'bytes':sum(r['bytes'] for r in results),'full_bytes_equal':report['passed']}))
assert report['passed']
