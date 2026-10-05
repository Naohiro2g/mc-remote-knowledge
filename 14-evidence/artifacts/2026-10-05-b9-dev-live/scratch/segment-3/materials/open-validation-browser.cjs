const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
const handoff = path.resolve(__dirname, '..');
const repository = path.resolve(handoff, '../..');
const {chromium} = createRequire(path.join(repository, 'packages/scratch-gui/package.json'))('@playwright/test');

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--remote-debugging-port=9269', '--remote-debugging-address=127.0.0.1',
            '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
    });
    const context = await browser.newContext({locale: 'ja-JP', viewport: {width: 1600, height: 1100},
        timezoneId: 'Asia/Tokyo'});
    const page = await context.newPage();
    await page.addInitScript(() => {
        window.__REACT_DEVTOOLS_GLOBAL_HOOK__ = {
            supportsFiber: true,
            inject: () => 1,
            onCommitFiberRoot: (_id, root) => {window.__b9ValidationRoot = root;},
            onCommitFiberUnmount: () => {}
        };
    });
    await page.goto('http://localhost:8611/?extension=mcremote', {waitUntil: 'domcontentloaded', timeout: 30000});
    await page.waitForFunction(() => {
        const find = node => {
            if (!node) return null;
            const app = node.stateNode;
            if (app && app.workspace && app.ScratchBlocks && app.props.vm &&
                app.ScratchBlocks.Blocks.mcremote_connect) return app;
            return find(node.child) || find(node.sibling);
        };
        const app = window.__b9ValidationRoot && find(window.__b9ValidationRoot.current);
        if (!app || !app.props.vm.editingTarget) return false;
        window.__b9ValidationApp = app;
        return true;
    }, null, {timeout: 30000});
    fs.writeFileSync(path.join(handoff, 'private/browser-state.json'), JSON.stringify({
        process_pid: process.pid, cdp_url: 'http://127.0.0.1:9269', editor_url: page.url(),
        source_commit: '7fbbf034488760d8fc7e034bf23f3e08e6e1807d'
    }, null, 2) + '\n');
    const blockId = await page.evaluate(() => {
        const app = window.__b9ValidationApp;
        const vm = app.props.vm;
        window.__b9ValidationObservation = null;
        vm.runtime.on('MCREMOTE_OBSERVATION_UPDATE', snapshot => {
            window.__b9ValidationObservation = snapshot;
        });
        const block = app.workspace.newBlock('mcremote_connect');
        block.initSvg();
        block.render();
        block.moveBy(140, 140);
        return block.id;
    });
    await page.waitForFunction(id => !!window.__b9ValidationApp.props.vm.editingTarget.blocks.getBlock(id), blockId);
    await page.evaluate(id => window.__b9ValidationApp.props.vm.runtime.toggleScript(id, {stackClick: true}), blockId);
    await page.waitForFunction(() => {
        const vm = window.__b9ValidationApp.props.vm;
        return !!vm.runtime._primitives.mcremote_pairCommand({}, {target: vm.editingTarget});
    }, null, {timeout: 20000});
    const command = await page.evaluate(() => {
        const vm = window.__b9ValidationApp.props.vm;
        return vm.runtime._primitives.mcremote_pairCommand({}, {target: vm.editingTarget});
    });
    console.log('PAIR_COMMAND: ' + command);
    console.log('Independent Chromium is waiting for human approval.');
    let authenticatedReported = false;
    const interval = setInterval(async () => {
        try {
            const state = await page.evaluate(() => {
                const observation = window.__b9ValidationObservation;
                return observation ? {status: observation.status, hello: observation.hello,
                    pairCode: observation.pairCode, reason: observation.lastError && observation.lastError.reason} : null;
            });
            if (state && state.status === 'connected' && !authenticatedReported) {
                authenticatedReported = true;
                if (state.hello.protocol !== '23.2.0' || state.hello.mc_version !== '1.21.11') {
                    console.log('FAIL: authenticated hello version mismatch');
                    return;
                }
                fs.writeFileSync(path.join(handoff, 'materials/independent-browser-hello.json'), JSON.stringify({
                    source_commit: '7fbbf034488760d8fc7e034bf23f3e08e6e1807d',
                    client_version: '2320.0.0b9', new_pairing_completed: true,
                    protocol: state.hello.protocol, mc_version: state.hello.mc_version,
                    pairing_command: command, status: 'connected'
                }, null, 2) + '\n');
                console.log('CONNECTED: b9 Scratch, protocol 23.2.0, MC 1.21.11');
            } else if (state && ['closed', 'error'].includes(state.status) && !authenticatedReported) {
                console.log('Connection status:', state.status, state.reason || 'none');
                clearInterval(interval);
            }
        } catch (error) {
            console.error(error.message);
            clearInterval(interval);
        }
    }, 1000);
    const stop = async () => {clearInterval(interval); await browser.close(); process.exit(0);};
    process.on('SIGINT', stop);
    process.on('SIGTERM', stop);
    await new Promise(() => {});
})().catch(error => {console.error(error.message); process.exit(1);});
