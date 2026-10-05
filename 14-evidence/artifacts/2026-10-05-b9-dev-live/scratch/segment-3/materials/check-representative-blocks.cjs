const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
const handoff = path.resolve(__dirname, '..');
const repository = path.resolve(handoff, '../..');
const {chromium} = createRequire(path.join(repository, 'packages/scratch-gui/package.json'))('@playwright/test');
const settings = JSON.parse(fs.readFileSync(path.join(handoff, 'private/deployment.json')));
const results = {source_commit: '7fbbf034488760d8fc7e034bf23f3e08e6e1807d',
    tooling_commit: 'dc1ab834183e29f2eb03059b07e99d2b463776ee', runs: [], picker: [], cleanup: {}};
let page;
let scope;
let handle;
let changedBlock = false;
let original;
let placeId;
const point = {X: '3', Y: '130', Z: '3'};

const redact = value => {
    if (Array.isArray(value)) return value.map(redact);
    if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) =>
        [key, /token|pairing.?id|credential|uuid|player.?id|connectiontarget|sandbox/i.test(key) ? '[redacted]' : redact(item)]));
    if (typeof value === 'string') return value.replaceAll(settings.runtime_config.default_sandbox, '[private target]')
        .replace(/\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/gi, '[redacted uuid]')
        .replace(/mcr[sl]_[A-Za-z0-9_-]+/g, '[redacted token]');
    return value;
};

async function make(opcode, changes = {}, nested = {}) {
    const id = await page.evaluate(({opcode, changes, nested}) =>
        window.__b9GateMakeBlock(opcode, changes, nested).id, {opcode, changes, nested});
    await page.waitForFunction(id => !!window.__b9ValidationApp.props.vm.editingTarget.blocks.getBlock(id), id);
    return id;
}

async function run(opcode, changes = {}, nested = {}, existingId) {
    const id = existingId || await make(opcode, changes, nested);
    const workspace = await page.evaluate(() =>
        window.__b9ValidationApp.workspace.getParentSvg().getBoundingClientRect().toJSON());
    await page.mouse.click(workspace.right - 40, workspace.bottom - 40);
    const sequence = await page.evaluate(() => window.__b9ValidationObservation.frameLog.at(-1)?.sequence || 0);
    await page.evaluate(id => window.__b9ValidationApp.props.vm.runtime.toggleScript(id, {stackClick: true}), id);
    await page.waitForFunction(id => !window.__b9ValidationApp.props.vm.runtime.threads.some(t => t.topBlock === id), id,
        {timeout: 15000});
    const outcome = await page.evaluate(({id, sequence}) => ({
        reporter: window.__b9GateReports[id],
        frames: window.__b9ValidationObservation.frameLog.filter(f => f.sequence > sequence && f.method !== 'events.poll')
    }), {id, sequence});
    const errors = outcome.frames.filter(f => f.direction === 'receive' && f.payload.error);
    const record = {opcode, arguments: changes, nested, ...outcome, passed: errors.length === 0};
    results.runs.push(redact(record));
    assert.equal(errors.length, 0, `${opcode}: server returned ${errors[0]?.payload.error.message}`);
    console.log('Block completed:', opcode);
    return outcome;
}

const response = (outcome, method) => {
    const frame = outcome.frames.find(f => f.direction === 'receive' && f.method === method);
    assert(frame, `Missing ${method} reply`);
    assert(Object.hasOwn(frame.payload, 'result'), `No result for ${method}`);
    return frame.payload.result;
};

async function main() {
    const browser = await chromium.connectOverCDP('http://127.0.0.1:9269');
    page = browser.contexts().flatMap(c => c.pages()).find(p => p.url().startsWith('http://localhost:8611/'));
    assert(page, 'Validation Scratch tab missing');
    const hello = await page.evaluate(() => window.__b9ValidationObservation.hello);
    assert.equal(hello.protocol, '23.2.0');
    assert.equal(hello.mc_version, '1.21.11');
    results.hello = {protocol: hello.protocol, mc_version: hello.mc_version};
    scope = browser.contexts().flatMap(context => context.pages()).find(candidate =>
        candidate.url().startsWith(settings.runtime_config.wirescope_url));
    if (!scope) {
        const expand = page.getByRole('button', {name: 'WireScope mini を開く', exact: true});
        if (await expand.count()) await expand.click();
        const popup = page.waitForEvent('popup');
        await page.getByRole('button', {name: 'WireScope を開く', exact: true}).click();
        scope = await popup;
    }
    await scope.waitForSelector('td.payload', {timeout: 15000});
    console.log('Independent WireScope attached to actual Scratch source');
    await page.evaluate(() => {
        const app = window.__b9ValidationApp;
        const vm = app.props.vm;
        window.__b9GateReports = {};
        vm.runtime.on('VISUAL_REPORT', report => {window.__b9GateReports[report.id] = report.value;});
        window.__b9GateVariables = {};
        for (const [kind, name, id, type] of [
            ['handle', 'b9 gate entity handle', 'b9-gate-entity-handle', ''],
            ['catalog', 'b9 gate catalog IDs', 'b9-gate-catalog-list', 'list']
        ]) {
            vm.editingTarget.createVariable(id, name, type, false);
            if (!app.workspace.getVariableById(id)) app.workspace.createVariable(name, type, id);
            window.__b9GateVariables[kind] = {id, name, type};
        }
        let position = 0;
        window.__b9GateMakeBlock = (opcode, changes = {}, nested = {}) => {
            const category = vm.runtime._blockInfo.find(item => item.id === 'mcremote');
            const entry = category.blocks.find(item => item.info && item.info.opcode === opcode);
            if (!entry) throw Error('Unknown block ' + opcode);
            const xml = new DOMParser().parseFromString(entry.xml, 'text/xml').documentElement;
            for (const [name, value] of Object.entries(changes)) {
                const input = [...xml.children].find(child => child.tagName === 'value' && child.getAttribute('name') === name);
                let field = input ? input.querySelector('field') : [...xml.children].find(child =>
                    child.tagName === 'field' && child.getAttribute('name') === name);
                if (input && !field) {
                    field = xml.ownerDocument.createElement('field');
                    field.setAttribute('name', 'TEXT');
                    input.firstElementChild.appendChild(field);
                }
                if (!field) throw Error('Missing block field ' + opcode + '.' + name);
                if (value && typeof value === 'object') {
                    field.setAttribute('id', value.id);
                    field.setAttribute('variabletype', value.type);
                    field.textContent = value.name;
                } else field.textContent = String(value);
            }
            const block = app.ScratchBlocks.Xml.domToBlock(xml, app.workspace);
            for (const [name, spec] of Object.entries(nested)) {
                const reporter = window.__b9GateMakeBlock(spec.opcode, spec.arguments);
                block.getInput(name).connection.connect(reporter.outputConnection);
            }
            block.render();
            if (!block.getParent()) block.moveBy(140, 240 + (position++ * 48));
            return block;
        };
    });

    const chat = await run('postToChat', {MSG: '[mc-remote b9 Scratch] representative block test'});
    assert.equal(response(chat, 'chat.post'), null);
    results.chat_post_null = true;
    const before = await run('getBlock', point);
    original = response(before, 'world.getBlock');
    assert(['minecraft:air', 'minecraft:cave_air', 'minecraft:void_air'].includes(original.block_id),
        'Test location is not empty; refusing to replace an existing block');
    placeId = await make('setBlock', {...point, BLOCK: 'gold_block', STATE: ''});
    const pickerLocation = await page.evaluate(id => {
        const block = window.__b9ValidationApp.workspace.getBlockById(id);
        const bounds = block.getField('PICKER').getSvgRoot().getBoundingClientRect();
        return {x: bounds.x + bounds.width / 2, y: bounds.y + bounds.height / 2};
    }, placeId);
    await page.mouse.click(pickerLocation.x, pickerLocation.y);
    const dialog = page.getByRole('dialog');
    await dialog.waitFor();
    const search = dialog.getByRole('textbox', {name: 'ブロックID・名前で検索', exact: true});
    for (const query of ['gold', '金ブロック', 'Block of Gold', 'door']) {
        await search.fill(query);
        const expected = query === 'door' ? 'minecraft:oak_door' : 'minecraft:gold_block';
        await dialog.locator(`[data-block-id="${expected}"]`).waitFor();
        const choices = await dialog.locator('[data-block-id]').evaluateAll(nodes => nodes.map(node =>
            ({id: node.dataset.blockId, label: node.innerText})));
        assert(choices.length > 0);
        results.picker.push({query, count: choices.length, expected_id_present: true,
            example: choices.find(choice => choice.id === expected)});
        if (query === 'gold') await dialog.screenshot({path: path.join(handoff, 'materials/picker-gold.png')});
        if (query === 'door') await dialog.screenshot({path: path.join(handoff, 'materials/picker-door.png')});
    }
    await search.fill('gold');
    await dialog.locator('[data-block-id="minecraft:gold_block"]').click();
    await dialog.getByRole('button', {name: 'この値の組を使う', exact: true}).click();
    await dialog.waitFor({state: 'hidden'});
    const literals = await page.evaluate(id => {
        const block = window.__b9ValidationApp.workspace.getBlockById(id);
        return Object.fromEntries(['BLOCK', 'STATE'].map(name =>
            [name, block.getInput(name).connection.targetBlock().getFieldValue('TEXT')]));
    }, placeId);
    assert.deepEqual(literals, {BLOCK: 'gold_block', STATE: ''});
    results.picker_applied = literals;
    changedBlock = true;
    const placed = await run('setBlock', {...point, ...literals}, {}, placeId);
    assert.equal(response(placed, 'world.setBlock'), null);
    const after = await run('getBlock', point);
    assert.equal(response(after, 'world.getBlock').block_id, 'minecraft:gold_block');
    results.placement_readback = true;
    const variables = await page.evaluate(() => window.__b9GateVariables);
    const entity = await run('spawnEntity', {...point, ENTITY: 'armor_stand', VARIABLE: variables.handle});
    handle = response(entity, 'world.spawnEntity');
    assert.equal(typeof handle, 'string');
    assert(handle.startsWith('mcr_eh_'));
    const stored = await page.evaluate(id => window.__b9ValidationApp.props.vm.editingTarget.lookupVariableById(id).value,
        variables.handle.id);
    assert.equal(stored, handle);
    const pose = await run('getEntityPose', {HANDLE: handle});
    assert.equal(response(pose, 'entity.getPose').pos.length, 3);
    results.entity_handle_and_pose = true;
    const dust = await run('spawnParticle', {...point, OFFSET_X: '.1', OFFSET_Y: '.1', OFFSET_Z: '.1',
        SPEED: '0', COUNT: '10', FORCE: 'true'}, {PARTICLE: {opcode: 'dustParticleSpec', arguments: {
            RED: '255', GREEN: '0', BLUE: '0', SIZE: '1', RECEIVER: 'self'}}});
    assert.equal(response(dust, 'world.spawnParticle'), 10);
    const particleRequest = dust.frames.find(f => f.direction === 'send' && f.method === 'world.spawnParticle');
    assert.equal(particleRequest.payload.params[6].receiver, 'self');
    const sound = await run('playSound', {...point, SOUND: 'block.note_block.harp'}, {OPTIONS: {
        opcode: 'soundOptions', arguments: {VOLUME: '.25', HEIGHT: 'N12', RECEIVER: 'self'}}});
    assert.equal(response(sound, 'world.playSound'), null);
    const soundRequest = sound.frames.find(f => f.direction === 'send' && f.method === 'world.playSound');
    assert.deepEqual(soundRequest.payload.params[4], {volume: .25, note: 12, receiver: 'self'});
    await run('catalogToList', {KIND: 'block', LIST: variables.catalog});
    const catalog = await page.evaluate(id => window.__b9ValidationApp.props.vm.editingTarget.lookupVariableById(id).value,
        variables.catalog.id);
    assert(catalog.includes('minecraft:gold_block') && catalog.length > 0);
    assert.deepEqual(catalog, [...catalog].sort());
    assert(catalog.every(id => id.startsWith('minecraft:')));
    results.catalog_list = {count: catalog.length, sorted: true, gold_block_present: true, fully_qualified: true};
    const removed = await run('removeEntity', {HANDLE: handle});
    assert.equal(response(removed, 'entity.remove'), null);
    results.cleanup.entity_removed = true;
    handle = null;
    const restored = await run('setBlock', {...point, BLOCK: original.block_id, STATE: ''});
    assert.equal(response(restored, 'world.setBlock'), null);
    changedBlock = false;
    const verified = await run('getBlock', point);
    assert.deepEqual(response(verified, 'world.getBlock'), original);
    results.cleanup.original_block_restored = true;
    const expectedMethods = ['hello', 'chat.post', 'world.setBlock',
        'world.getBlock', 'world.spawnEntity', 'entity.getPose', 'world.spawnParticle', 'world.playSound', 'entity.remove'];
    for (const method of expectedMethods) {
        await scope.waitForFunction(method => [...document.querySelectorAll('td.method')].some(cell => cell.textContent === method), method);
    }
    const visible = await scope.evaluate(() => {
        const rows = [...document.querySelectorAll('tbody tr')];
        const first = rows.find(row => row.querySelector('td.frame-time'));
        return {row_count: rows.length, methods: [...new Set(rows.map(row => row.querySelector('td.method')?.textContent))],
            columns: first && {time: first.querySelector('td.frame-time').getBoundingClientRect().width,
                direction: first.querySelector('td.direction').getBoundingClientRect().width},
            status: document.querySelector('.status-card')?.innerText};
    });
    const text = await scope.locator('body').innerText();
    assert(!text.includes(settings.runtime_config.default_sandbox), 'Private target in WireScope display');
    assert(!/mcr[sl]_[A-Za-z0-9_-]+/.test(text), 'Raw token in WireScope display');
    const maskedPayloads = scope.locator('td.payload').filter({hasText:
        /pairing_id|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/i});
    await scope.screenshot({path: path.join(handoff, 'materials/wirescope-b9.png'), fullPage: true,
        mask: [maskedPayloads]});
    results.screenshot_masked_payloads = await maskedPayloads.count();
    results.wirescope = visible;
    results.wirescope.expected_methods_visible = expectedMethods;
    results.frames = redact(await page.evaluate(methods => window.__b9ValidationObservation.frameLog.filter(frame =>
        methods.includes(frame.method)), expectedMethods));
    results.passed = true;
    console.log('PASS: representative blocks, picker and independent WireScope');
}

(async () => {
    try {await main();} catch (error) {
        results.passed = false;
        results.failure = redact(error.message);
        console.error('FAIL:', results.failure);
        if (page && handle) {
            try {await run('removeEntity', {HANDLE: handle}); results.cleanup.entity_removed = true;}
            catch (cleanupError) {results.cleanup.entity_error = redact(cleanupError.message);}
        }
        if (page && changedBlock && original) {
            try {await run('setBlock', {...point, BLOCK: original.block_id, STATE: ''}); results.cleanup.original_block_restored = true;}
            catch (cleanupError) {results.cleanup.block_error = redact(cleanupError.message);}
        }
    }
    fs.writeFileSync(path.join(handoff, 'materials/representative-results.json'), JSON.stringify(redact(results), null, 2) + '\n');
    process.exit(results.passed ? 0 : 1);
})();
