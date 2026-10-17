"""Collect publisher metadata without selecting or deploying server artifacts."""
import concurrent.futures
import json
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent
URLS = {
    **{p: f'https://api.modrinth.com/v2/project/{p}/version' for p in
       ('worldedit', 'directionhud', 'luckperms', 'advanced-portals', 'discordsrv', 'otterlib')},
    'geyser': 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest',
    'floodgate': 'https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest',
    'paper263': 'https://fill.papermc.io/v3/projects/paper/versions/26.3/builds',
}

def fetch(item):
    name, url = item
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'mc-remote-stack-compatibility-research/1.0 (https://github.com/Naohiro2g/mc-remote-stack)'})
        with urllib.request.urlopen(req, timeout=40) as response:
            data = json.load(response)
        (OUT / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        if name in ('geyser', 'floodgate'):
            return name, {k: data.get(k) for k in ('version', 'build', 'time')}
        if name == 'paper263':
            builds = data if isinstance(data, list) else data.get('builds', [])
            stable = [b for b in builds if b.get('channel') == 'STABLE']
            return name, {'stable_count': len(stable), 'latest_stable': stable[:1]}
        selected = [v for v in data if any(l in v['loaders'] for l in ('bukkit', 'paper', 'spigot', 'purpur', 'folia'))]
        return name, [{'id': v['id'], 'version': v['version_number'], 'type': v['version_type'],
                       'loaders': v['loaders'], 'supports263': '26.3' in v['game_versions'],
                       'latest_games': v['game_versions'][-7:], 'dependencies': v['dependencies']}
                      for v in selected[:4]]
    except Exception as error:
        return name, {'error': str(error)}

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    print(json.dumps(dict(pool.map(fetch, URLS.items())), ensure_ascii=False, indent=2))
