"""Isolated rc2 config/lifecycle validation; raw logs and tokens stay in /tmp."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MATERIALS = Path(__file__).resolve().parent
RUNTIME = Path('/tmp/mcremote-rc2-pulse')
BASELINE = Path('/tmp/mcremote-rc1-pulse')
SOURCE = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
JAR = MATERIALS / 'mc-remote-2321.0.0rc2.jar'
RC1 = BASELINE / '1.21.11/plugins/mc-remote-2321.0.0rc1.jar'
sys.path.insert(0, str(REPO / 'scripts'))
from compatibility_pulse import RecordedRpc, result, require_reason, digest, sanitize

assert digest(RC1) == '917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37'
JAR_SHA = digest(JAR)
(MATERIALS / 'source-commit.txt').write_text(SOURCE + '\n')


def write_json(path, value):
    path.write_text(json.dumps(sanitize(value), ensure_ascii=False, indent=2) + '\n')


def boot(home, java, label, action=None, rejected=False):
    log_path = RUNTIME / f'{home.name}-{label}.log'
    with log_path.open('w') as log:
        proc = subprocess.Popen([str(java), '-Xms256M', '-Xmx1536M', '-XX:ActiveProcessorCount=2',
                                 '-jar', 'paper.jar', 'nogui'], cwd=home, stdin=subprocess.PIPE,
                                stdout=log, stderr=subprocess.STDOUT, text=True)
        try:
            deadline = time.monotonic() + 180
            if rejected:
                proc.wait(timeout=180)
            else:
                while 'Done (' not in log_path.read_text(errors='replace'):
                    if proc.poll() is not None:
                        raise RuntimeError(f'{home.name} {label} exited during startup; {log_path}')
                    if time.monotonic() > deadline:
                        raise TimeoutError(f'{home.name} {label} startup timeout; {log_path}')
                    time.sleep(0.5)
                if action:
                    action()
        finally:
            if proc.poll() is None:
                proc.stdin.write('stop\n')
                proc.stdin.flush()
                try:
                    proc.wait(timeout=90)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                    raise
    text = log_path.read_text(errors='replace')
    assert proc.returncode == 0, (home.name, label, proc.returncode, str(log_path))
    assert 'Stopping server' in text, (label, str(log_path))
    print(home.name, label, 'stopped normally', flush=True)
    return text


for mc, build, port, java_version in [('1.21.11', 132, 29314, '21.0.2'), ('26.3', 203, 29464, '25.0.2')]:
    home = RUNTIME / mc
    java = Path('/USER_HOME/.local/share/mise/installs/java') / java_version / 'bin/java'
    token_file = RUNTIME / f'token-{mc}'
    token_file.chmod(0o600)
    token = token_file.read_text().strip()
    metadata = json.loads((BASELINE / 'metadata' / f'paper-{mc}-{build}.json').read_text())
    server_sha = metadata['downloads']['server:default']['checksums']['sha256']
    assert digest(home / 'paper.jar') == server_sha
    identity = {'source_commit': SOURCE, 'minecraft_version': mc, 'paper_build': build,
                'paper_server_sha256': server_sha, 'jar_sha256': JAR_SHA,
                'java_version': subprocess.run([str(java), '-version'], text=True, capture_output=True,
                                               check=True).stderr.strip()}
    config = home / 'plugins/McRemote/config.yml'
    with zipfile.ZipFile(JAR) as archive:
        modern = archive.read('config.yml').decode().replace('api_port: 25575', f'api_port: {port}')
    assert f'api_port: {port}' in modern
    config.write_text(modern)
    shutil.copyfile(JAR, home / 'plugins' / JAR.name)
    assert digest(home / 'plugins' / JAR.name) == JAR_SHA
    lifecycle = {'source_commit': SOURCE, 'minecraft_version': mc, 'jar_sha256': JAR_SHA, 'observations': []}
    auth_transcript = []

    def authenticated_checks():
        rpc = RecordedRpc(port, auth_transcript)
        try:
            require_reason('authentication enforced', rpc.call('hello', {'protocol': '23.2.1'}), 'auth_required')
        finally:
            rpc.close()

    def pulse(restarted=False, name=None):
        authenticated_checks()
        path = MATERIALS / (name or f'{"restart-pulse" if restarted else "pulse"}-{mc}.json')
        cmd = [sys.executable, str(REPO / 'scripts/compatibility_pulse.py'), '--port', str(port),
               '--expect-mc', mc, '--jar', str(JAR), '--targets', str(MATERIALS / 'minecraft-targets.json'),
               '--token-file', str(token_file), '--output', str(path)]
        if restarted:
            cmd.append('--restart-only')
        subprocess.run(cmd, check=True, timeout=180)
        report = json.loads(path.read_text())
        assert report['transcript'][0]['response']['result']['protocol'] == '23.2.1'
        report.update(identity)
        write_json(path, report)

    for restarted in (False, True):
        text = boot(home, java, 'restart' if restarted else 'modern', lambda: pulse(restarted))
        observation = {'enabled': 'Enabling McRemote v2321.0.0rc2' in text,
                       'disabled': 'Disabling McRemote v2321.0.0rc2' in text,
                       'ready': 'Done (' in text and 'Credential domain health: HEALTHY' in text,
                       'auth_enforcement_on': auth_transcript[-1]['response']['error']['data']['reason'] == 'auth_required',
                       'exit_code': 0}
        assert all(observation[k] for k in ('enabled', 'disabled', 'ready', 'auth_enforcement_on'))
        lifecycle['observations'].append(observation)
    write_json(MATERIALS / f'lifecycle-{mc}.json', lifecycle)
    subprocess.run([sys.executable, str(REPO / 'scripts/prepare_minecraft_verification.py'),
                    '--pulse', str(MATERIALS / f'pulse-{mc}.json'), '--restart-pulse',
                    str(MATERIALS / f'restart-pulse-{mc}.json'), '--lifecycle',
                    str(MATERIALS / f'lifecycle-{mc}.json'), '--output-dir', str(MATERIALS)], check=True)

    # Both old and new keys exist: rc2 must still stop, leave config/credentials untouched, and never open its API.
    legacy = modern + '\nb5:\n  entity_handle_capacity: 8\nb7:\n  lightning:\n    global_per_tick: 5\n'
    config.write_text(legacy)
    before = digest(config)
    db = home / 'plugins/McRemote/credential-store/snapshot.json.sqlite'
    before_db = digest(db)
    text = boot(home, java, 'legacy-rejected', rejected=True)
    required = ['Stopping the entire Paper server', "'b5.entity_handle_capacity'", "'entities.handle_capacity'",
                "'b7.lightning.global_per_tick'", "'lightning.global_per_tick'",
                'remove the b5: and b7: sections', 'restart Paper', 'Stopping server']
    assert all(item in text for item in required), str(RUNTIME / f'{mc}-legacy-rejected.log')
    assert 'Server started at port' not in text
    assert 'Auth enforcement:' not in text
    assert digest(config) == before
    assert digest(db) == before_db
    excerpt = [line for line in text.splitlines() if 'McRemote' in line or 'Stopping server' in line]
    write_json(MATERIALS / f'legacy-rejection-{mc}.json', {**identity, 'status': 'PASS',
               'paper_process_exited': True, 'exit_code': 0, 'api_not_opened': True,
               'config_unchanged': True, 'credentials_unchanged': True, 'log_excerpt': excerpt})

    # Let the actual released rc1 migrate a legacy config, then preserve the resulting file byte-for-byte in rc2.
    legacy_for_rc1 = legacy.replace('  handle_capacity: 256\n', '').replace('  global_per_tick: 2\n', '')
    assert legacy_for_rc1 != legacy
    config.write_text(legacy_for_rc1)
    (home / 'plugins' / JAR.name).unlink()
    shutil.copyfile(RC1, home / 'plugins' / RC1.name)
    text = boot(home, java, 'rc1-migration')
    assert 'Moved legacy config values:' in text
    assert 'b5.entity_handle_capacity -> entities.handle_capacity' in text
    assert 'b7.lightning.global_per_tick -> lightning.global_per_tick' in text
    migrated = config.read_text()
    assert not re.search(r'^b[57]:', migrated, flags=re.M)
    assert re.search(r'^  handle_capacity: 8$', migrated, flags=re.M)
    assert re.search(r'^  global_per_tick: 5$', migrated, flags=re.M)
    migrated_sha = digest(config)
    (home / 'plugins' / RC1.name).unlink()
    shutil.copyfile(JAR, home / 'plugins' / JAR.name)
    text = boot(home, java, 'rc1-migrated-config', lambda: pulse(True, f'rc1-migrated-pulse-{mc}.json'))
    assert 'Enabling McRemote v2321.0.0rc2' in text
    assert 'Moved legacy config values:' not in text
    assert digest(config) == migrated_sha
    write_json(MATERIALS / f'rc1-migrated-config-{mc}.json', {**identity, 'status': 'PASS',
               'rc1_jar_sha256': digest(RC1), 'actual_rc1_migration_observed': True,
               'rc2_config_byte_unchanged': True, 'config_sha256': migrated_sha,
               'entity_handle_capacity': 8, 'lightning_global_per_tick': 5,
               'authenticated_read_write_pulse': f'rc1-migrated-pulse-{mc}.json'})

assert digest(JAR) == JAR_SHA
print('PASS both Minecraft versions: modern config, ordinary restart, Paper stop, actual rc1-migrated config', flush=True)
