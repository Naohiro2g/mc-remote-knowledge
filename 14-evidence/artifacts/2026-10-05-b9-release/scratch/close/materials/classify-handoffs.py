from pathlib import Path
import csv,hashlib,ipaddress,json,re
root=Path('handoff-materials'); out=root/'2026-10-05-b9-close/materials'
landed=json.loads((out/'landed-evidence-verification.json').read_text())
verified={str(Path(f['source']).relative_to(root/'2026-10-05-b9-scratch-dev')) for f in landed['files']}
plans={
'2026-10-04-b9-scratch-confirmation':('当時の移管評価と契約監査・確認票を残す','14-evidence/artifacts/2026-10-05-b9-tooling-migration/scratch/initial-confirmation/'),
'2026-10-05-b9-tooling-migration':('移管前後の照合とfixture発行・consumer pin・CIの観測を残す','14-evidence/artifacts/2026-10-05-b9-tooling-migration/scratch/'),
'2026-10-05-b9-release':('公開前の停止・packaging差の原因・承認後のactual OCI照合と公開操作を残す','14-evidence/artifacts/2026-10-05-b9-release/scratch/'),
'2026-10-05-b9-scratch-dev':('収容済み18 fileは③、未収容4 PNGは①、現行配信runtime/privateは②','14-evidence/artifacts/2026-10-05-b9-dev-live/scratch/segment-3/'),
'2026-09-30-block-picker-names':('b8の名前表示・検索の初期ブラウザ観測と局所決定搬送素材','14-evidence/artifacts/2026-10-03-b8-dev-live/scratch/2026-09-30-block-picker-names/'),
'2026-10-01-b8-fixture-preflight':('b8凍結時の正式一覧とb9移管時の全13件照合で役目を終えた',''),
'2026-10-01-b8-local-playtest':('ローカル試運転の画像・UI観測は①、現行8601系の起動設定等は②','14-evidence/artifacts/2026-10-03-b8-dev-live/scratch/2026-10-01-b8-local-playtest/'),
'2026-10-02-home-scratch-contract-reply':('Stack問い合わせの回答はStack担当への引継ぎ・受領確認待ち',''),
'2026-10-02-stack-wss-reply':('StackのWSS 401検査修正の回答・再現を引き継ぐ',''),
'2026-10-03-wirescope-column-width':('b9へ採用・移管済み。人間承認の元画像と観測は①、旧preview/buildは③','14-evidence/artifacts/2026-10-03-b8-dev-live/scratch/2026-10-03-wirescope-column-width/'),
'2026-10-01-b8-candidate-b7-fixes':('旧candidateのみ。検証本文はb8 evidenceへ移管済みで、b8/b9公開物へ置換済み',''),
'2026-10-02-b8-candidate-local-fixes':('旧candidateのみ。検証本文はb8 evidenceへ移管済みで、b8/b9公開物へ置換済み',''),
'2026-10-03-b8-publication':('残っている2 assetは公開b8 Releaseと同じ内容',''),
'2026-10-03-b8-scratch-live-gate':('残るruntime/privateは手元b9配信の戻し先とprivate opsの引継ぎ',''),
'2026-10-03-b8-scratch-live-human':('残るprivate原画像はbackstageへ移す対象。sanitizeした正式evidenceは収容済み',''),
}
def category(name,rel):
 if '__pycache__' in rel.parts:return 3
 if name=='2026-10-05-b9-scratch-dev':
  if rel.parts[0] in {'runtime','private'}:return 2
  if str(rel) in verified or rel.parts[0]=='artifacts':return 3
  assert rel.suffix=='.png',rel
  return 1
 if name=='2026-10-05-b9-release':
  if rel.parts[0]=='artifacts':
   if str(rel).startswith('artifacts/published-comparison/') and 'assets' not in rel.parts:return 1
   return 3
  return 1
 if name=='2026-10-05-b9-tooling-migration':
  if rel.parts[0]=='artifacts' or rel.suffix=='.zip':return 3
  return 1
 if name=='2026-10-03-wirescope-column-width':
  if 'preview-app' in rel.parts or rel.name in {'wirescope-app.zip','commit-message.txt'}:return 3
  return 1
 if name=='2026-10-01-b8-local-playtest':
  if rel.name in {'start-scratch.cjs','runtime-config.json','check-bridge.cjs','check-ui.cjs','bridge-server.log','scratch-server.log','wirescope-server.log'}:return 2
  return 1
 if name in {'2026-10-02-home-scratch-contract-reply','2026-10-02-stack-wss-reply','2026-10-03-b8-scratch-live-gate','2026-10-03-b8-scratch-live-human'}:return 2
 if name in {'2026-10-01-b8-fixture-preflight','2026-10-01-b8-candidate-b7-fixes','2026-10-02-b8-candidate-local-fixes','2026-10-03-b8-publication'}:return 3
 return 1
results=[]; evidence=[]; discard=[]; flags=[]
for name,(reason,dest) in plans.items():
 counts={str(k):{'files':0,'bytes':0} for k in (1,2,3)}
 for p in sorted((root/name).rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(root/name); c=category(name,rel); size=p.stat().st_size
  counts[str(c)]['files']+=1;counts[str(c)]['bytes']+=size
  if c==1:
   data=p.read_bytes(); row={'directory':name,'path':str(rel),'bytes':size,'sha256':hashlib.sha256(data).hexdigest(),'proposed_knowledge_path':dest+str(rel)};evidence.append(row)
   if p.suffix not in {'.png','.zip','.gz'}:
    text=data.decode(errors='replace')
    addresses=[]
    for s in re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b',text):
     try:ip=ipaddress.ip_address(s)
     except ValueError:continue
     if ip.is_private and not (ip.is_loopback or s.startswith(('192.0.2.','198.51.100.','203.0.113.'))):addresses.append(s)
    if addresses:flags.append({'directory':name,'path':str(rel),'private_address_match_count':len(addresses)})
  elif c==3:discard.append({'directory':name,'path':str(rel),'bytes':size})
 results.append({'directory':name,'categories':[int(c) for c,v in counts.items() if v['files']], 'counts':counts,'reason':reason,'proposed_knowledge_root':dest or None})
report={'knowledge_contract_commit':'099c40b0c312694712653885200f3114ea4bed33','knowledge_contract_path':'00-hub/b9-gate-close-instructions_ja.md','directories':results,'evidence_files':evidence,'discard_candidates':discard,'deleted':False,'private_address_scan_flags':flags,'scan_non_claim':'The address scan is a supplementary check, not a complete credential or image privacy review. private/ and runtime/ are excluded from evidence.'}
(out/'classification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
with (out/'EVIDENCE_FILES.tsv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=['directory','path','bytes','sha256','proposed_knowledge_path'],delimiter='\t');writer.writeheader();writer.writerows(evidence)
print(json.dumps({'directories':len(results),'evidence_files':len(evidence),'evidence_bytes':sum(x['bytes'] for x in evidence),'discard_candidates':len(discard),'privacy_flags':flags},ensure_ascii=False))
