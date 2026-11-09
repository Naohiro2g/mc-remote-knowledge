from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.parse,urllib.request

root=Path('/tmp/stack-homepage-sync')
files=json.loads((root/'homepage-files.json').read_text())
def verify(item):
    name,expected=item
    url='https://mc-remote.com/'+urllib.parse.quote(name)
    with urllib.request.urlopen(url,timeout=30) as r:
        body=r.read(); status=r.status
    git_sha=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    return {'path':name,'http_status':status,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'matches_knowledge':git_sha==expected}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results=list(pool.map(verify,sorted(files.items())))
failed=[r for r in results if r['http_status']!=200 or not r['matches_knowledge']]
summary={'knowledge_commit':'4d600d21822df002ac4f07cf033962315344fbbe','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'total_files':len(results),'scratch_files':sum(r['path'].startswith('api/scratch/') for r in results),'failed':failed,'all_https_files_match':not failed}
(root/'https-files.json').write_text(json.dumps(results,indent=2)+'\n')
(root/'https-result.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
assert not failed
