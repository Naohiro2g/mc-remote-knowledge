const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
const handoff = path.resolve(__dirname, '..');
const repository = path.resolve(handoff, '../..');
const {chromium} = createRequire(path.join(repository, 'packages/scratch-gui/package.json'))('@playwright/test');
const settings = JSON.parse(fs.readFileSync(path.join(handoff, 'private/deployment.json')));
const resultPath = path.join(handoff, 'materials/representative-results.json');
const results = JSON.parse(fs.readFileSync(resultPath));
const redact = value => {
    if (Array.isArray(value)) return value.map(redact);
    if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) =>
        [key, /token|pairing.?id|credential|uuid|player.?id|connectiontarget|sandbox/i.test(key) ? '[redacted]' : redact(item)]));
    if (typeof value === 'string') return value.replaceAll(settings.runtime_config.default_sandbox, '[private target]')
        .replace(/\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/gi, '[redacted uuid]')
        .replace(/mcr[sl]_[A-Za-z0-9_-]+/g, '[redacted token]');
    return value;
};

(async () => {
    const browser = await chromium.connectOverCDP('http://127.0.0.1:9269');
    const pages = browser.contexts().flatMap(context => context.pages());
    const editor = pages.find(page => page.url().startsWith('http://localhost:8611/'));
    const scope = pages.find(page => page.url().startsWith(settings.runtime_config.wirescope_url));
    assert(editor && scope, 'Independent browser tabs missing');
    assert.equal(results.runs.length, 12);
    assert(results.runs.every(run => run.passed));
    assert(results.cleanup.entity_removed && results.cleanup.original_block_restored);
    const methods = ['hello', 'chat.post', 'world.setBlock', 'world.getBlock', 'world.spawnEntity',
        'entity.getPose', 'world.spawnParticle', 'world.playSound', 'entity.remove'];
    const observed = await scope.evaluate(() => {
        const rows = [...document.querySelectorAll('tbody tr')];
        const first = rows.find(row => row.querySelector('td.frame-time'));
        return {row_count: rows.length, status: document.querySelector('.status-card')?.innerText,
            columns: first && {time: first.querySelector('td.frame-time').getBoundingClientRect().width,
                direction: first.querySelector('td.direction').getBoundingClientRect().width},
            rows: rows.map(row => ({sequence: Number(row.querySelector('td.sequence')?.textContent),
                method: row.querySelector('td.method')?.textContent,
                direction: row.querySelector('td.direction')?.classList.contains('direction-send') ? 'send' : 'receive',
                time: row.querySelector('td.frame-time')?.textContent}))};
    });
    for (const method of methods) {
        assert(observed.rows.some(row => row.method === method && row.direction === 'send'), method + ' send absent');
        assert(observed.rows.some(row => row.method === method && row.direction === 'receive'), method + ' receive absent');
    }
    const expectedFrames = results.runs.flatMap(run => run.frames).filter(frame => methods.includes(frame.method));
    for (const frame of expectedFrames) {
        assert(observed.rows.some(row => row.sequence === frame.sequence && row.method === frame.method &&
            row.direction === frame.direction), `Missing frame ${frame.sequence} ${frame.method}`);
    }
    const text = await scope.locator('body').innerText();
    assert(!text.includes(settings.runtime_config.default_sandbox));
    assert(!/mcr[sl]_[A-Za-z0-9_-]+/.test(text));
    const mask = scope.locator('td.payload').filter({hasText:
        /pairing_id|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/i});
    await scope.screenshot({path: path.join(handoff, 'materials/wirescope-b9.png'), fullPage: true, mask: [mask]});
    await scope.screenshot({path: path.join(handoff, 'materials/wirescope-b9-columns.png'),
        clip: {x: 0, y: 0, width: 1600, height: 900}, mask: [mask]});
    results.wirescope = {...observed, expected_methods_visible: methods,
        representative_frames_verified: expectedFrames.length, time_direction_human_review: 'pending'};
    results.screenshot_masked_payloads = await mask.count();
    results.frames = redact(await editor.evaluate(methods => window.__b9ValidationObservation.frameLog.filter(frame =>
        methods.includes(frame.method)), methods));
    results.harness_diagnostics = [
        'Added missing text shadow field when constructing test blocks; candidate unchanged.',
        'Closed previous reporter bubble via workspace background click before each script; manual UI report then succeeds.',
        'Matched WireScope assertions to source allowlist: auth methods and catalog.get are intentionally excluded.'
    ];
    results.browser_checks_passed = true;
    results.passed = true;
    delete results.failure;
    fs.writeFileSync(resultPath, JSON.stringify(redact(results), null, 2) + '\n');
    console.log(JSON.stringify({browser_checks_passed: true, runs: results.runs.length,
        frames_verified: expectedFrames.length, columns: observed.columns, human_width_review: 'pending'}));
    process.exit(0);
})().catch(error => {console.error(error.message); process.exit(1);});
