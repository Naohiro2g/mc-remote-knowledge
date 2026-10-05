"""Frozen-wheel segment 2 runner; human approval and browser observation required."""
import ast
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from mc_remote import Minecraft
from mc_remote.auth import load_token
from mc_remote.connection import McRpcError

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
WHEEL = Path('/tmp/mcr-b9-python-final-ci/minecraft_remote_api-2320.0.0b9-py3-none-any.whl')
MARKER = 'b9-python-live'
report = {
    'knowledge_contract_commit': '561de98b5c15864ac9b86cb6dcaeef1f20ce635b',
    'exact_set': 'b9-integrated-artifact-set-1',
    'python_source_commit': 'b901c88fe41b67530ff353271683ece9fd453076',
    'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'endpoint_profile': 'normal-dev', 'token_emitted': False,
    'started_at_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'PREPARING', 'checks': {},
}
mc = None
handle = None
frames = []


def checkpoint():
    (OUT / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


def check(name, condition, detail=None):
    report['checks'][name] = {'status': 'PASS' if condition else 'FAIL', 'detail': detail}
    checkpoint()
    print(name + ': ' + report['checks'][name]['status'], flush=True)
    if not condition:
        raise RuntimeError('assertion_failed_' + name)


def command():
    value = input().strip().upper()
    report.setdefault('human_controls', []).append(value if value in {'RUN', 'REISSUE', 'OBSERVED', 'STOP'} else 'INVALID')
    checkpoint()
    return value


def capture():
    if mc is not None and mc._observer is not None and mc._observer.active:
        snapshot = mc._observer.snapshot(frames)
        (OUT / 'observer_snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')


try:
    check('wheel_identity', WHEEL.stat().st_size == 196221 and hashlib.sha256(WHEEL.read_bytes()).hexdigest() == 'e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6')
    check('installed_package', version('minecraft-remote-api') == '2320.0.0b9' and 'site-packages' in str(Path(sys.modules['mc_remote'].__file__).resolve()))
    package = Path(sys.modules['mc_remote'].__file__).resolve().parent
    for name, size, sha in [
        ('wirescope-app.zip', 83854, 'da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad'),
        ('wirescope-app.manifest.json', 2339, 'c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7'),
    ]:
        artifact = package / '_wirescope_app' / name
        check(name, artifact.stat().st_size == size and hashlib.sha256(artifact.read_bytes()).hexdigest() == sha)
    values = {}
    profile = ROOT / 'handoff-materials/2026-10-03-b8-dev-token-upgrade/materials/param_dev.py'
    for node in ast.parse(profile.read_text()).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        values[target.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        pass
    host, port = values['ADRS_MCR'], values['PORT_MCR']
    ssh = subprocess.run(['ssh', '-G', 'm720s2'], capture_output=True, text=True, check=True)
    expected = next(line.split(' ', 1)[1] for line in ssh.stdout.splitlines() if line.startswith('hostname '))
    check('authorized_endpoint', host == expected and port == 25575)
    for key in ('MCREMOTE_API_HOST', 'JRP_API_HOST', 'MCREMOTE_API_PORT', 'JRP_API_PORT'):
        os.environ.pop(key, None)
    report['stage'] = 'authentication-with-pairing-fallback'
    mc = Minecraft.create(host, port, debug=False, handshake=False, sync_catalog=False, wirescope=True)
    mc.conn.request_timeout = 15.0
    check('wirescope_started', mc._wirescope_runtime is not None and mc._observer is not None)
    runtime = mc._wirescope_runtime
    def collect(frame):
        # Observer projections exclude credentials, addresses and player identities.
        # Omit unrelated human chat text from the retained evidence only.
        retained = json.loads(json.dumps(frame))
        if retained.get('method') == 'events.poll':
            for event in retained.get('payload', {}).get('result', {}).get('events', []):
                if event.get('type') == 'chat_posted' and event.get('message') != MARKER:
                    event['message'] = '[UNRELATED CHAT REDACTED]'
        frames.append(retained)
        runtime.pipeline.accept_frame(frame)
    mc._observer.set_frame_consumer(collect)
    key = f'{host}:{port}'
    before = load_token(key)
    hello = mc.authenticate(key, token_type='session', pair=True)
    report['pairing_replaced_stored_token'] = load_token(key) != before
    before = None
    report['hello_result'] = {k: hello[k] for k in ('protocol', 'mc_version', 'supported_mc_versions', 'dimension', 'origin', 'world_constants', 'permissions', 'catalog_hash') if k in hello}
    check('authenticated_hello', hello.get('protocol') == '23.2.0' and hello.get('mc_version') == '1.21.11')
    for _ in range(40):
        if runtime.pipeline.attach_code:
            break
        time.sleep(0.05)
    report['status'] = 'WAITING_FOR_HUMAN_READY'
    checkpoint()
    print('HELLO_OK protocol=23.2.0 mc_version=1.21.11', flush=True)
    print('WIRESCOPE_URL ' + runtime.url, flush=True)
    print('ATTACH_CODE ' + str(runtime.pipeline.attach_code), flush=True)
    print('Send Minecraft chat: ' + MARKER + '; then control RUN. REISSUE renews attach code.', flush=True)
    while True:
        control = command()
        if control == 'REISSUE':
            print('REISSUE_RESULT ' + runtime.pipeline.reissue_code(), flush=True)
            print('ATTACH_CODE ' + str(runtime.pipeline.attach_code), flush=True)
        elif control == 'RUN':
            check('browser_attached', runtime.pipeline._attached and runtime.pipeline.terminal_reason is None)
            break
        elif control == 'STOP':
            raise RuntimeError('human_stopped_before_body')
    report['status'] = 'RUNNING'
    report['stage'] = 'postToChat'
    check('postToChat', mc.postToChat('[b9 Python] representative round trip') is None, 'null decoded as None')
    report['stage'] = 'pollEvents'
    batch = mc.pollEvents(32)
    report['event_batch'] = {
        'types': [event.type for event in batch.events],
        'through_sequence': batch.through_sequence, 'latest_sequence': batch.latest_sequence,
        'filtered_out': batch.filtered_out, 'loss_totals': dict(batch.loss_totals),
    }
    check('pollEvents', any(event.type == 'pickaxe_poke' or (event.type == 'chat_posted' and event.message == MARKER) for event in batch.events))
    report['stage'] = 'player-position-and-context'
    player = mc.getPos()
    initial_origin = hello['origin']
    origin = [math.floor(initial_origin[i] + player['pos'][i]) for i in range(3)]
    mc.setDimension(player['dimension'])
    mc.setBuildOrigin(*origin)
    report['stage'] = 'entity'
    handle = mc.spawnEntity(2, 1, 2, 'cow')
    pose = mc.getEntityPose(handle)
    check('entity_spawn_and_pose', pose['dimension'] == player['dimension'])
    check('entity_remove', mc.removeEntity(handle) is None)
    handle = None
    report['stage'] = 'particle'
    count = mc.spawnParticle(0, 2, 2, 0.2, 0.2, 0.2, {'particle_id': 'dust', 'receiver': 'self', 'data': {'color': [64, 160, 255], 'size': 1}}, 0, 8)
    check('particle', count == 8, {'result': count})
    report['stage'] = 'sound'
    check('sound', mc.playSound(0, 1, 1, 'block.note_block.harp', note=18, volume=0.5, receiver='self') is None)
    capture()
    report['status'] = 'WAITING_FOR_HUMAN_OBSERVATION'
    checkpoint()
    print('BODY_PASS; inspect WireScope frames, then control OBSERVED or STOP.', flush=True)
    control = command()
    report['human_wirescope_observation'] = 'confirmed' if control == 'OBSERVED' else 'not_confirmed'
    check('human_wirescope', control == 'OBSERVED')
    report['status'] = 'PASS'
except BaseException as exc:
    report['status'] = 'FAIL'
    report['exception_type'] = type(exc).__name__
    if isinstance(exc, McRpcError):
        report['code'] = exc.code
        report['reason'] = exc.reason if isinstance(exc.reason, str) and re.fullmatch(r'[a-z_]{1,64}', exc.reason) else 'redacted'
    elif isinstance(exc, RuntimeError) and re.fullmatch(r'[a-zA-Z0-9_.-]{1,100}', str(exc)):
        report['reason'] = str(exc)
    print('STOPPED ' + report.get('reason', report['exception_type']), flush=True)
finally:
    if mc is not None:
        if handle is not None:
            try:
                mc.removeEntity(handle)
                report['emergency_entity_cleanup'] = 'PASS'
            except Exception as exc:
                report['emergency_entity_cleanup'] = type(exc).__name__
                report['status'] = 'FAIL'
        try:
            capture()
        except Exception as exc:
            report['snapshot_error_type'] = type(exc).__name__
        try:
            mc.close()
            report['close'] = 'PASS'
        except Exception as exc:
            report['close'] = type(exc).__name__
            report['status'] = 'FAIL'
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    checkpoint()
    print('FINAL ' + report['status'], flush=True)

sys.exit(0 if report['status'] == 'PASS' else 1)
