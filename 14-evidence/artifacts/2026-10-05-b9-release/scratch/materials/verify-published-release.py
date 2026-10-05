from pathlib import Path
import hashlib
import json
import subprocess

root=Path(__file__).resolve().parents[1]
repo='Naohiro2g/scratch-editor'
tag='v2320.0.0b9'
source='7fbbf034488760d8fc7e034bf23f3e08e6e1807d'
run=37270517123
expected={
 'wirescope-app.zip':(83854,'da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad'),
 'wirescope-app.manifest.json':(2339,'c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7'),
 'contracts.tar.gz':(1908,'48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390')}
def api(path): return json.loads(subprocess.check_output(['gh','api','repos/'+repo+'/'+path]))
release=api('releases/tags/'+tag)
assert release['prerelease'] is True and release['draft'] is False
assert release['name']=='mc-remote Scratch 2320.0.0b9'
assert api('commits/'+tag)['sha']==api('commits/develop')['sha']==source
workflow=api(f'actions/runs/{run}')
assert workflow['conclusion']=='success' and workflow['head_sha']==source and workflow['event']=='release'
folder=root/'artifacts/published-assets'; folder.mkdir(exist_ok=True)
subprocess.run(['gh','release','download',tag,'--repo',repo,'--dir',str(folder),'--clobber'],check=True)
results=[]
for asset in release['assets']:
 data=(folder/asset['name']).read_bytes(); size=len(data); sha=hashlib.sha256(data).hexdigest()
 assert asset['size']==size
 assert asset['digest']=='sha256:'+sha
 if asset['name'] in expected: assert (size,sha)==expected[asset['name']]
 results.append({'file':asset['name'],'id':asset['id'],'bytes':size,'sha256':sha,'url':asset['browser_download_url']})
assert set(a['file'] for a in results)==set(expected)|{'manifest.json'}
manifest=json.loads((folder/'manifest.json').read_text())
assert manifest['schema']=='mc-remote.release-manifest' and manifest['schema_version']==1
assert manifest['release_tag']==tag and manifest['source_commit']==source
roles={a['role']:a for a in manifest['artifacts']}
assert set(roles)=={'scratch','bridge','wirescope','wirescope-manifest','contracts'}
assert roles['bridge']['digest']=='sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f'
assert roles['bridge']['locator']=='ghcr.io/naohiro2g/mc-remote-bridge'
assert roles['scratch']['locator']=='ghcr.io/naohiro2g/mc-remote-scratch'
for role in ('wirescope','wirescope-manifest','contracts'):
 a=roles[role]; assert a['kind']=='https-file'; assert a['sha256']==expected[a['file']][1]
identity={'knowledge_contract_commit':'7eec4255e1b820cf996dc71c42b34d672dea44f8','release_id':release['id'],'url':release['html_url'],
          'tag_target':source,'develop':source,'prerelease':True,'draft':False,'make_latest_requested':False,
          'workflow_run':run,'workflow_url':workflow['html_url'],'assets':results,'manifest':manifest}
(root/'materials/scratch-release-public-identity.json').write_text(json.dumps(identity,indent=2)+'\n')
(root/'materials/scratch-release-workflow.json').write_text(json.dumps(workflow,indent=2)+'\n')
(root/'materials/scratch-release-public-provider.json').write_text(json.dumps(release,indent=2)+'\n')
print(json.dumps(identity,indent=2))
