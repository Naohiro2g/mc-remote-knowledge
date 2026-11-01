"""Recheck the unchanged stable JAR using the existing isolated Paper pulse."""
import argparse
import json
import subprocess
import sys
import time
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--runtime', type=Path, required=True)
parser.add_argument('--java', type=Path, required=True)
parser.add_argument('--mc', required=True)
parser.add_argument('--build', type=int, required=True)
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()
materials = Path(__file__).resolve().parent
sys.path.insert(0, str(args.repo / 'scripts'))
from compatibility_pulse import RecordedRpc, digest, require_reason, sanitize

candidate = args.repo / 'handoff-materials/2026-10-22-rc2-publication-stable-candidate/materials'
jar = candidate / 'mc-remote-2321.0.0.jar'
source = (candidate / 'stable-source-commit.txt').read_text().strip()
assert source == '525c31823a8efb736463aec471c2756089546391'
assert jar.stat().st_size == 315868
assert digest(jar) == 'e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab'
with zipfile.ZipFile(jar) as archive:
    assert archive.read('minecraft-targets.json') == (candidate / 'minecraft-targets.json').read_bytes()
home = args.runtime / args.mc
metadata = json.loads((args.runtime / 'metadata' / f'paper-{args.mc}-{args.build}.json').read_text())
assert metadata['id'] == args.build
server_sha = metadata['downloads']['server:default']['checksums']['sha256']
assert digest(home / 'paper.jar') == server_sha
assert digest(home / 'plugins' / jar.name) == digest(jar)
assert list((home / 'plugins').glob('*.jar')) == [home / 'plugins' / jar.name]
token_file = args.runtime / f'token-{args.mc}'
assert token_file.stat().st_mode & 0o077 == 0
identity = {
    'source_commit': source, 'minecraft_version': args.mc, 'paper_build': args.build,
    'jar_sha256': digest(jar), 'paper_server_sha256': server_sha,
    'java_version': subprocess.run([str(args.java), '-version'], capture_output=True, text=True, check=True).stderr.strip(),
}
assert 'Temurin' in identity['java_version']
expected_java = {'1.21.11': '21.0.13+9', '26.3': '25.0.5+8'}[args.mc]
assert expected_java in identity['java_version']
flags = ['-Xms256M', '-Xmx1536M', '-XX:ActiveProcessorCount=2']
lifecycle = {**identity, 'java_vendor': 'Eclipse Adoptium', 'java_distribution': 'Eclipse Temurin',
             'jvm_flags': flags, 'server_args': ['nogui'], 'observations': []}


def write_json(path, value):
    path.write_text(json.dumps(sanitize(value), ensure_ascii=False, indent=2) + '\n')


for restarted in (False, True):
    label = 'restart' if restarted else 'full'
    started = time.monotonic()
    raw_log = args.runtime / f'{args.mc}-{label}.log'
    auth_transcript = []
    with raw_log.open('w') as log:
        proc = subprocess.Popen([str(args.java), *flags, '-jar', 'paper.jar', 'nogui'], cwd=home,
                                stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT, text=True)
        try:
            deadline = time.monotonic() + 300
            while 'Done (' not in raw_log.read_text(errors='replace'):
                if proc.poll() is not None:
                    raise RuntimeError(f'{label} exited during startup; see raw log')
                if time.monotonic() > deadline:
                    raise TimeoutError(f'{label} startup timeout; see raw log')
                time.sleep(0.5)
            startup_seconds = round(time.monotonic() - started, 2)
            print(f'{args.mc} {label} ready after {startup_seconds}s', flush=True)
            rpc = RecordedRpc(args.port, auth_transcript)
            try:
                require_reason('authentication enforced', rpc.call('hello', {'protocol': '23.2.1'}), 'auth_required')
            finally:
                rpc.close()
            output = materials / f'{"restart-pulse" if restarted else "pulse"}-{args.mc}.json'
            command = [sys.executable, str(args.repo / 'scripts/compatibility_pulse.py'),
                       '--port', str(args.port), '--expect-mc', args.mc, '--jar', str(jar),
                       '--targets', str(candidate / 'minecraft-targets.json'),
                       '--token-file', str(token_file), '--output', str(output)]
            if restarted:
                command.append('--restart-only')
            subprocess.run(command, check=True, timeout=180)
            pulse = json.loads(output.read_text())
            pulse.update(identity)
            write_json(output, pulse)
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
    text = raw_log.read_text(errors='replace')
    observation = {
        'enabled': 'Enabling McRemote v2321.0.0' in text,
        'disabled': 'Disabling McRemote v2321.0.0' in text,
        'ready': 'Done (' in text and 'Credential domain health: HEALTHY' in text,
        'auth_enforcement_on': auth_transcript[0]['response']['error']['data']['reason'] == 'auth_required',
        'exit_code': proc.returncode, 'normal_stop': 'Stopping server' in text,
        'startup_seconds': startup_seconds, 'total_seconds': round(time.monotonic() - started, 2),
    }
    assert all(observation[k] for k in ('enabled', 'disabled', 'ready', 'auth_enforcement_on', 'normal_stop'))
    assert proc.returncode == 0
    assert 'Could not pass event' not in text and 'generated an exception' not in text
    lifecycle['observations'].append(observation)
    write_json(materials / f'auth-enforcement-{label}-{args.mc}.json', {**identity, 'status': 'PASS', 'transcript': auth_transcript})
    print(f'{args.mc} {label} stopped normally', flush=True)

write_json(materials / f'lifecycle-{args.mc}.json', lifecycle)
subprocess.run([sys.executable, str(args.repo / 'scripts/prepare_minecraft_verification.py'),
                '--pulse', str(materials / f'pulse-{args.mc}.json'),
                '--restart-pulse', str(materials / f'restart-pulse-{args.mc}.json'),
                '--lifecycle', str(materials / f'lifecycle-{args.mc}.json'),
                '--output-dir', str(materials)], check=True)
assert digest(jar) == identity['jar_sha256']
assert digest(home / 'paper.jar') == server_sha
print(f'PASS {args.mc}: same stable JAR, Temurin {expected_java}, full pulse and ordinary restart', flush=True)
