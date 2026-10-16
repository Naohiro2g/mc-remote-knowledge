from pathlib import Path
import json,hashlib,zipfile,shutil,struct,sys
metadata=json.loads(Path(sys.argv[1]).read_text())
archive=Path(sys.argv[2])
commit='c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b'
run=37808012407
sha=lambda b:hashlib.sha256(b).hexdigest()
def file_sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
assert not metadata['expired']
assert metadata['workflow_run']['head_sha']==commit
assert metadata['workflow_run']['id']==run
assert metadata['name']=='scratch-candidate-'+commit
assert archive.stat().st_size==metadata['size_in_bytes']
assert 'sha256:'+file_sha(archive)==metadata['digest']
out=Path('candidate/ci-'+str(run));out.mkdir(exist_ok=True)
reports=[]
with zipfile.ZipFile(archive) as outer:
 manifest=json.loads(outer.read('candidate-manifest.json'))
 assert manifest['source']['commit']==commit
 for artifact in manifest['artifacts']:
  info=outer.getinfo(artifact['file']);assert info.file_size==artifact['bytes']
  h=hashlib.sha256()
  with outer.open(info) as f:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  assert h.hexdigest()==artifact['sha256'],artifact['file']
 pairs=set()
 for entry in manifest['artifacts']:
  if entry['role']!='scratch-local':continue
  pairs.add((entry['os'],entry['arch']))
  name=entry['file'];target=out/name
  with outer.open(name) as src,target.open('wb') as dest:shutil.copyfileobj(src,dest)
  sidecar=name.removesuffix('.zip')+'.artifact.json'
  (out/sidecar).write_bytes(outer.read(sidecar))
  identity=json.loads((out/sidecar).read_bytes())
  assert identity['source_commit']==commit and identity['working_tree_dirty'] is False
  assert identity['bytes']==target.stat().st_size and identity['sha256']==file_sha(target)
  with zipfile.ZipFile(target) as inner:
   prefix=name.removesuffix('.zip')+'/'
   assert all(p.startswith(prefix) and '..' not in Path(p).parts for p in inner.namelist())
   data=json.loads(inner.read(prefix+'identity.json'))
   assert data['version']=='2320.0.0b10'
   assert (data['os'],data['arch'])==(entry['os'],entry['arch'])
   assert data['source']['commit']==commit and data['source']['working_tree_dirty'] is False
   assert sha(inner.read(prefix+data['source']['archive']))==data['source']['archive_sha256']
   if entry['os']=='windows':
    binary=inner.read(prefix+'runtime/node.exe');assert binary[:2]==b'MZ'
    start=struct.unpack_from('<I',binary,0x3c)[0];assert binary[start:start+4]==b'PE\0\0'
    assert struct.unpack_from('<H',binary,start+4)[0]==0x8664
   elif entry['os']=='macos':
    binary=inner.read(prefix+'runtime/bin/node');assert binary[:4]==bytes.fromhex('cffaedfe')
    assert struct.unpack_from('<I',binary,4)[0]==0x0100000c
   else:
    binary=inner.read(prefix+'runtime/bin/node');assert binary[:4]==b'\x7fELF'
    assert struct.unpack_from('<H',binary,18)[0]==62
   review=json.loads(inner.read(prefix+'licenses/review.json'))
   overrides=json.loads(inner.read(prefix+'licenses/supplemental-sources.json'))
   for pkg in overrides['entries']:
    for f in pkg['files']:
     b=inner.read(prefix+'licenses/supplemental/'+f['path'].removeprefix('licenses/'))
     assert len(b)==f['bytes'] and sha(b)==f['sha256']
   assert all(e['files'] for e in review['entries'] if e['distribution']=='runtime')
   for file in ['licenses/Node-LICENSE','licenses/Scratch-AGPL-3.0.txt','licenses/Scratch-TRADEMARK','licenses/Bridge-AGPL-3.0.txt','licenses/ws-LICENSE','NOTICE_ja.md','SOURCE_ja.md']:
    assert inner.getinfo(prefix+file).file_size>0
   report={**entry,'local_path':str(target),'identity':data,'license_review':{k:v for k,v in review.items() if k!='entries'}}
   (out/(entry['os']+'-license-review.json')).write_bytes(inner.read(prefix+'licenses/review.json'))
   reports.append(report)
 assert pairs=={('windows','x64'),('macos','arm64'),('linux','x64')}
 (out/'candidate-manifest.json').write_bytes(outer.read('candidate-manifest.json'))
result={'source_commit':commit,'workflow_run_id':run,'artifact':metadata,'outer_sha256':file_sha(archive),'outer_bytes':archive.stat().st_size,'zips':reports,'all_manifest_artifacts_verified':True}
Path('/tmp/scratch-b10-ci-candidate-verification.json').write_text(json.dumps(result,indent=2)+'\n')
for r in reports:print(r['os'],r['arch'],r['bytes'],r['sha256'],r['license_review'])
print('outer artifact and all manifest artifacts verified; binary architectures/source/license supplement identities PASS')
