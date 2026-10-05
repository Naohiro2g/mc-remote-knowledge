const assert = require('node:assert/strict');
const path = require('node:path');
const {createRequire} = require('node:module');
const requireGui = createRequire(path.resolve('packages/scratch-gui/package.json'));
const {chromium} = requireGui('@playwright/test');
const names = requireGui('./src/lib/mcremote-block-names/1.21.11.json');
const outputDirectory = path.resolve('handoff-materials/2026-09-30-block-picker-names/materials');

(async () => {
    const browser = await chromium.launch({headless: true});
    try {
        const page = await browser.newPage({locale: 'ja-JP', viewport: {width: 1280, height: 1000}});
        const mojangRequests = [];
        page.on('request', request => {
            if (/mojang\.com|resources\.download\.minecraft\.net/.test(request.url())) {
                mojangRequests.push(request.url());
            }
        });
        await page.addInitScript(() => {
            window.__REACT_DEVTOOLS_GLOBAL_HOOK__ = {
                supportsFiber: true,
                inject: () => 1,
                onCommitFiberRoot: (_id, root) => { window.__pickerTestRoot = root; },
                onCommitFiberUnmount: () => {}
            };
        });
        await page.goto('http://127.0.0.1:8601/?extension=mcremote', {waitUntil: 'domcontentloaded'});
        await page.waitForFunction(() => {
            const walk = node => {
                if (!node) return null;
                const instance = node.stateNode;
                if (instance && typeof instance.handleMcRemoteBlockPickerStart === 'function') return instance;
                return walk(node.child) || walk(node.sibling);
            };
            const blocks = window.__pickerTestRoot && walk(window.__pickerTestRoot.current);
            if (!blocks || !blocks.workspace || !blocks.ScratchBlocks.Blocks.mcremote_setBlock) return false;
            window.__pickerTestBlocks = blocks;
            return true;
        }, null, {timeout: 30000});
        const blockCatalog = Object.fromEntries(Object.keys(names).map(id => [id, {states: {}, default_state: {}}]));
        blockCatalog['minecraft:oak_log'] = {states: {axis: ['x', 'y', 'z']}, default_state: {axis: 'y'}};
        blockCatalog['examplemod:ruby_block'] = {states: {}, default_state: {}};
        await page.evaluate(block => {
            window.__pickerTestBlocks.props.vm.emit('MCREMOTE_CATALOG_UPDATE', {
                status: 'current',
                mcVersion: '1.21.11',
                catalogHash: 'browser-fixture-only',
                source: 'network',
                catalog: {block}
            });
        }, blockCatalog);
        await page.waitForFunction(() => window.__pickerTestBlocks.props.mcRemoteCatalog.status === 'current');
        await page.evaluate(() => {
            const app = window.__pickerTestBlocks;
            const block = app.workspace.newBlock('mcremote_setBlock');
            for (const [input, value] of [['BLOCK', 'stone'], ['STATE', '']]) {
                const text = app.workspace.newBlock('text');
                text.setShadow(true);
                text.setFieldValue(value, 'TEXT');
                text.initSvg();
                block.getInput(input).connection.connect(text.outputConnection);
            }
            block.initSvg();
            block.render();
            window.__pickerTestBlock = block;
            app.handleMcRemoteBlockPickerStart(block);
        });
        const search = page.getByRole('textbox', {name: /ブロックID・/});
        const screenshots = [];
        for (const [query, count] of [['gold', 5], ['door', 42]]) {
            await search.fill(query);
            await page.getByText(`${count}件`, {exact: true}).waitFor();
            const choices = page.locator('button[data-block-id]');
            assert.equal(await choices.count(), count);
            const alignment = await choices.first().locator('span').last().evaluate(element =>
                getComputedStyle(element).textAlign);
            assert.equal(alignment, 'right');
            const borderWidth = await choices.first().evaluate(element =>
                parseFloat(getComputedStyle(element).borderBottomWidth));
            assert(borderWidth > 0);
            const screenshot = path.join(outputDirectory, `block-picker-${query}.png`);
            await page.screenshot({path: screenshot});
            screenshots.push(screenshot);
        }
        await page.locator('[data-block-id="minecraft:waxed_weathered_copper_trapdoor"]').scrollIntoViewIfNeeded();
        await page.screenshot({path: path.join(outputDirectory, 'block-picker-door-long.png')});
        await search.fill('gold 金ブロック');
        const gold = page.getByRole('button', {name: /^gold_block 金ブロック/});
        await gold.waitFor({state: 'visible'});
        assert((await gold.innerText()).includes('Block of Gold'));
        assert.equal(await page.getByRole('button', {name: /^oak_log/}).count(), 0);
        await page.screenshot({path: path.join(outputDirectory, 'block-picker.png')});
        await search.fill('gold 木');
        await page.getByText('検索に一致するブロックがありません。', {exact: true}).waitFor();
        await search.fill('BLOCK OF GOLD');
        await gold.click();
        await page.getByRole('button', {name: 'この値の組を使う', exact: true}).click();
        const values = await page.evaluate(() => {
            const block = window.__pickerTestBlock;
            return ['BLOCK', 'STATE'].map(input => block.getInput(input).connection.targetBlock().getFieldValue('TEXT'));
        });
        assert.deepEqual(values, ['gold_block', '']);
        assert.deepEqual(mojangRequests, []);
        console.log(JSON.stringify({result: 'PASS',testClass: 'deterministic browser fixture',
            display: 'gold_block 金ブロック / Block of Gold', searches: ['Japanese + ID AND', 'no matches', 'English AND'],
            applied: values, mojangRequests: mojangRequests.length, results: {gold: 5, door: 42}, screenshots}));
    } finally {
        await browser.close();
    }
})().catch(error => { console.error(error); process.exitCode = 1; });
