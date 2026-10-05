from pathlib import Path
import hashlib,json
repo=Path(__file__).resolve().parents[3]
root=repo/'handoff-materials/2026-10-06-stack-backstage-handoff'
stack=repo.parent/'mc-remote-stack'
receipt=stack/'handoff-materials/2026-10-06-stack-backstage-handoff/materials/RECEIPT_ja.md'
received=stack/'handoff-materials/2026-10-06-stack-backstage-handoff/materials/received-inventory.json'
source_inventory=json.loads((root/'materials/stack-source-inventory.json').read_text())
received_inventory=json.loads(received.read_text())
expected={f['path']:f for f in source_inventory['files']}
assert {f['path'] for f in received_inventory['files']}==set(expected)
results=[]
for f in received_inventory['files']:
 for k in ('path','received_path'):
  p=Path(f[k]);assert not p.is_absolute() and '..' not in p.parts
 source=repo/f['path']; target=stack/f['received_path']
 assert target.resolve().is_relative_to(stack.resolve())
 a=source.read_bytes();b=target.read_bytes(); sha=hashlib.sha256(a).hexdigest()
 assert a==b and len(a)==expected[f['path']]['bytes']==f['bytes']
 assert sha==expected[f['path']]['sha256']==f['sha256']
 results.append({**f,'full_bytes_equal':True,'independently_verified_by_scratch':True})
raw=receipt.read_bytes();assert len(raw)==9247
assert hashlib.sha256(raw).hexdigest()=='ed5dbd56488b259e86f8040d2500bd10f8d1173da2502ac9a682d82282954483'
(root/'materials/STACK_RECEIPT_ja.md').write_bytes(raw)
(root/'materials/stack-received-inventory.json').write_bytes(received.read_bytes())
report={'knowledge_contract_commit':'5beaad2557abbc6e90ada03edf7d0a2918fa7a52',
        'receiver_commit_reported':received_inventory['receiver_commit'],
        'receipt':{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},
        'files':results,'passed':True,'deleted':False,
        'non_claim':'This checks receipt and transferred file contents. Stack source, tests, service state, and remote integration were not independently revalidated.'}
(root/'materials/stack-receipt-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'files':len(results),'bytes':sum(f['bytes'] for f in results),'full_bytes_equal':True,'deleted':False}))
