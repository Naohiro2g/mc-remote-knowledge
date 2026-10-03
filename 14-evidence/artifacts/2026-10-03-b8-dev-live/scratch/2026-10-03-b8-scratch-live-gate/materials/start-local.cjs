const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {spawn} = require('node:child_process');
const {createRequire} = require('node:module');

const handoff = path.resolve(__dirname, '..');
const repository = path.resolve(handoff, '../..');
const settings = JSON.parse(fs.readFileSync(path.join(handoff, 'private/deployment.json')));
const requireGui = createRequire(path.join(repository, 'packages/scratch-gui/package.json'));
const Ajv = requireGui('ajv');
const validate = new Ajv({allErrors: true}).compile(JSON.parse(
    fs.readFileSync(path.join(repository, 'packages/scratch-gui/contracts/runtime-config/schema.json'))
));
if (!validate(settings.runtime_config)) throw new Error(JSON.stringify(validate.errors));
const configBytes = Buffer.from(JSON.stringify(settings.runtime_config));
const mime = {'.html':'text/html; charset=utf-8', '.js':'text/javascript', '.css':'text/css',
    '.json':'application/json', '.svg':'image/svg+xml', '.png':'image/png', '.jpg':'image/jpeg',
    '.woff':'font/woff', '.woff2':'font/woff2', '.map':'application/json'};
const servers = [];
let bridge;
let stopping = false;
const stop = () => {
    if (stopping) return;
    stopping = true;
    for (const server of servers) server.close();
    if (bridge) bridge.kill('SIGTERM');
};
function serve(root, port, runtimeConfig) {
    const server = http.createServer((request, response) => {
        let pathname;
        try { pathname = decodeURIComponent(new URL(request.url, 'http://127.0.0.1').pathname); }
        catch { response.writeHead(400).end(); return; }
        response.setHeader('Cache-Control', 'no-store');
        if (runtimeConfig && pathname === '/mc-remote-runtime-config.json') {
            response.writeHead(200, {'Content-Type':'application/json'}).end(configBytes);
            return;
        }
        const file = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
        if (!file.startsWith(root + path.sep)) { response.writeHead(403).end(); return; }
        fs.stat(file, (error, info) => {
            if (error || !info.isFile()) { response.writeHead(404).end(); return; }
            response.writeHead(200, {'Content-Type':mime[path.extname(file)] || 'application/octet-stream'});
            fs.createReadStream(file).on('error', () => response.destroy()).pipe(response);
        });
    });
    servers.push(server);
    server.on('error', error => { console.error(error.message); process.exitCode = 1; stop(); });
    server.listen(port, '127.0.0.1', () => console.log(`Frozen static app ready on localhost:${port}`));
}
serve(path.join(handoff, 'runtime/scratch/build'), 8611, true);
serve(path.join(handoff, 'runtime/wirescope'), 4183, false);
const bridgeDirectory = path.join(handoff, 'runtime/bridge');
bridge = spawn(process.execPath, [path.join(bridgeDirectory, 'dist/main.js')], {
    cwd: bridgeDirectory,
    env: {...process.env, ...settings.bridge_env},
    stdio: ['ignore', 'inherit', 'inherit']
});
bridge.on('error', error => { console.error(error.message); process.exitCode = 1; stop(); });
bridge.on('exit', code => { if (!stopping) { process.exitCode = code || 1; stop(); } });
process.on('SIGINT', stop);
process.on('SIGTERM', stop);
