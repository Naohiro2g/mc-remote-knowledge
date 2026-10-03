import hashlib
import json
import re
from pathlib import Path

materials = Path(__file__).resolve().parent
handoff = materials.parent
raw = json.loads((handoff / 'private/browser-state.json').read_text())
data = raw['data']
identity = json.loads((materials / 'frozen-identities.json').read_text())
identity.pop('live_started')
result = {
    'identity': identity,
    'authenticated_hello': data['authenticatedHello'],
    'execution': 'Frozen production GUI in independent Google Chrome; real Scratch blocks executed by VM sequencer',
    'block_runs': data['results'],
    'picker': data['picker'],
    'b7_numeric_and_idle_poll': data['b7'],
    'server_backpressure': data['backpressure']['summary'],
    'runner_corrections': data['runnerCorrection'],
    'cleanup': data['finished'],
    'human_wirescope_review': json.loads((materials / 'human-review.json').read_text())
    if (materials / 'human-review.json').exists() else 'NOTRUN: acknowledgment pending',
    'live_human_segment_4': 'NOTRUN: outside this agent segment',
    'non_claim': ['No component/cross-repo GREEN', 'No audible/visual Minecraft effect claim',
                  'No source/artifact/fixture change', 'No tag/release publication'],
}
poll = result['b7_numeric_and_idle_poll']
poll['retainedFrameSequenceAdvanced'] = poll.pop('pollSequenceAdvanced')
poll['actualPollSequenceAdvanced'] = poll['internalFrameSequenceAfter'] > poll['internalFrameSequenceBefore']
for run in result['block_runs']:
    if run['opcode'] == 'setBuildMode' and 'TRACE_DELAY' not in run['args']:
        run['test_class'] = 'initial runner input error; not a product PASS'
        run['reason'] = 'invalid_trace_delay'
payload = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
private = json.loads((handoff / 'private/deployment.json').read_text())
for value in [private['host_alias'], private['runtime_config']['default_sandbox']]:
    assert value not in payload, 'Private deployment address in result'
assert not re.search(r'"(?:token|pairing_id|uuid)"\s*:', payload, re.I)
assert not re.search(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', payload, re.I)
(materials / 'live-results.json').write_text(payload)
images = ['picker-gold.png', 'picker-door.png', 'picker-default-state.png', 'wirescope-final.png']
image_identity = {}
for filename in images:
    blob = (materials / filename).read_bytes()
    image_identity[filename] = {'bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest()}
(materials / 'image-identities.json').write_text(json.dumps(image_identity, indent=2) + '\n')
dom = (materials / 'wirescope-final-dom.txt').read_text()
assert private['runtime_config']['default_sandbox'] not in dom
assert not re.search(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', dom, re.I)
for method in ['world.getNearbyEntities', 'entity.getPose', 'entity.setPose', 'entity.remove',
               'world.spawnParticle', 'world.playSound', 'world.playBlockSound']:
    assert method in dom, f'Missing rendered method: {method}'
assert '送信済み・結果未確認' in dom
print(json.dumps({'export': 'PASS', 'privacy_check': 'PASS', 'block_runs': len(data['results']),
                  'rendered_methods': 7, 'images': len(images)}, ensure_ascii=False))
