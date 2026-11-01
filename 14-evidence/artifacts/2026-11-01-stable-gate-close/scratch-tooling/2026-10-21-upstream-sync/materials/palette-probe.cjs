const {chromium} = require('/tmp/scratch-upstream-sync-20261021/node_modules/playwright');
const fs = require('node:fs');

let activeBrowser;
(async () => {
    const browser = await chromium.launch({headless: true, args: ['--enable-unsafe-swiftshader']});
    activeBrowser = browser;
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(fs.readFileSync('/tmp/codex-upstream-sync-20261021/editor-url.txt', 'utf8') + '?extension=mcremote');
    await page.waitForFunction(() => {
        for (let element = document.querySelector('.blocklySvg'); element; element = element.parentElement) {
            const key = Object.keys(element).find(name => name.startsWith('__reactFiber$'));
            for (let fiber = key && element[key]; fiber; fiber = fiber.return) {
                if (fiber.stateNode && fiber.stateNode.workspace && fiber.stateNode.ScratchBlocks) {
                    window.paletteProbe = fiber.stateNode;
                    return !!fiber.stateNode.workspace.getToolbox().getToolboxItemById('mcremote');
                }
            }
        }
        return false;
    }, {timeout: 30000});
    await page.evaluate(() => document.fonts.ready);
    const categories = await page.evaluate(() => window.paletteProbe.workspace.getToolbox().getToolboxItems()
        .filter(item => item.getName).map(item => ({id: item.getId(), name: item.getName()})));
    const records = [];
    for (const category of categories) {
        await page.evaluate(id => {
            const toolbox = window.paletteProbe.workspace.getToolbox();
            toolbox.setSelectedItem(toolbox.getToolboxItemById(id));
        }, category.id);
        await page.waitForTimeout(1000);
        records.push(await page.evaluate(category => {
            const flyout = window.paletteProbe.workspace.getFlyout();
            const workspace = flyout.getWorkspace();
            const labels = flyout.getContents().filter(item => {
                const element = item.getElement();
                return element.getButtonText && element.getButtonText() === category.name;
            }).map(item => {
                const element = item.getElement();
                const svg = element.getSvgRoot ? element.getSvgRoot() : element.svgGroup_;
                return {y: element.getPosition().y, screenY: svg && svg.getBoundingClientRect().y};
            });
            return {category, scale: workspace.scale, scrollY: workspace.scrollY, scrollTarget: flyout.scrollTarget,
                cached: flyout.getCategoryScrollPosition(category.name), metrics: workspace.getMetrics(), labels};
        }, category));
    }
    const interventions = [];
    for (const action of ['before', 'scrollbar.resize', 'resizeContents', 'svgResize']) {
        await page.evaluate(action => {
            const instance = window.paletteProbe;
            const flyout = instance.workspace.getFlyout();
            if (action === 'scrollbar.resize') flyout.getWorkspace().scrollbar.resize();
            if (action === 'resizeContents') flyout.getWorkspace().resizeContents();
            if (action === 'svgResize') instance.ScratchBlocks.svgResize(instance.workspace);
        }, action);
        await page.waitForTimeout(500);
        interventions.push(await page.evaluate(action => {
            const f = window.paletteProbe.workspace.getFlyout();
            const w = f.getWorkspace();
            const bar = w.scrollbar.vScroll || w.scrollbar;
            const last = window.paletteProbe.workspace.getToolbox().getToolboxItemById('mcremote');
            const position = f.getCategoryScrollPosition(last.getName());
            return {action, error: Math.ceil(position) * w.scale + w.scrollY, scrollTarget: f.scrollTarget,
                ratio: bar.ratio, scrollbarLength: bar.scrollbarLength, handleLength: bar.handleLength,
                oldHostMetrics: bar.oldHostMetrics, metrics: w.getMetrics()};
        }, action));
    }
    await page.screenshot({path: '/tmp/codex-upstream-sync-20261021/palette-probe.png'});
    fs.writeFileSync('/tmp/codex-upstream-sync-20261021/palette-probe.json', JSON.stringify({errors, records, interventions}, null, 2));
    console.log(JSON.stringify({errors, interventions, records: records.map(r => ({category: r.category.name, scale: r.scale,
        scrollY: r.scrollY, cached: r.cached, labelY: r.labels[0] && r.labels[0].y,
        error: r.cached * r.scale + r.scrollY, scrollTarget: r.scrollTarget,
        scrollTop: r.metrics.scrollTop, viewTop: r.metrics.viewTop,
        screenY: r.labels[0] && r.labels[0].screenY}))}, null, 2));
    await browser.close();
})().catch(error => {console.error(error); process.exitCode = 1;})
    .finally(async () => {if (activeBrowser) await activeBrowser.close();});
