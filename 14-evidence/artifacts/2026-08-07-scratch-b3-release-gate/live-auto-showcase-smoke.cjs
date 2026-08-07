const {chromium} = require('playwright');

const baseUrl = process.argv[2];
const expectedIdentity = process.argv[3];
if (!baseUrl || !expectedIdentity) {
    console.error('usage: node live-auto-showcase-smoke.cjs <base-url> <expected-identity>');
    process.exit(1);
}

const fail = message => {
    throw new Error(message);
};

(async () => {
    const browser = await chromium.launch({headless: true});
    try {
        const page = await browser.newPage({locale: 'ja-JP'});
        const websocketUrls = [];
        page.on('websocket', socket => websocketUrls.push(socket.url()));

        await page.goto(`${baseUrl}?extension=mcremote`, {
            waitUntil: 'domcontentloaded',
            timeout: 120000
        });
        await page.waitForTimeout(15000);

        const bodyText = await page.locator('body').innerText();
        if (!bodyText.includes('Showcase build')) fail('showcase notice heading is not visible');
        if (!bodyText.includes('This page is a showcase with the Minecraft connection turned off.')) {
            fail('showcase notice body is not visible');
        }
        if (await page.getByText(/^(接続する|connect)$/).count() === 0) fail('connect block is not present');

        const runtimeResult = await page.evaluate(async () => {
            const queue = [];
            for (const element of document.querySelectorAll('*')) {
                for (const key of Object.keys(element)) {
                    if (key.startsWith('__reactFiber$')) queue.push(element[key]);
                }
            }
            const seen = new Set();
            let vm = null;
            while (queue.length > 0 && !vm) {
                const fiber = queue.shift();
                if (!fiber || seen.has(fiber)) continue;
                seen.add(fiber);
                for (const props of [fiber.memoizedProps, fiber.pendingProps]) {
                    if (props && props.vm && props.vm.runtime && props.vm.runtime.getOpcodeFunction) {
                        vm = props.vm;
                        break;
                    }
                }
                queue.push(fiber.child, fiber.sibling);
            }
            if (!vm) throw new Error('Scratch VM was not found in the mounted page');
            const connect = vm.runtime.getOpcodeFunction('mcremote_connect');
            if (typeof connect !== 'function') throw new Error('mcremote_connect primitive is not registered');
            let reason = '';
            try {
                await connect();
            } catch (error) {
                reason = error && (error.reason || error.message) || String(error);
            }
            return {
                reason,
                runtimeConfig: vm.getMcRemoteRuntimeConfig()
            };
        });

        if (runtimeResult.reason !== 'connection_disabled') {
            fail(`connect rejection was ${runtimeResult.reason || 'missing'}, expected connection_disabled`);
        }
        if (runtimeResult.runtimeConfig.connectionEnabled !== false) {
            fail('built VM runtime reports connectionEnabled other than false');
        }
        if (runtimeResult.runtimeConfig.releaseIdentity !== expectedIdentity) {
            fail(`release identity was ${runtimeResult.runtimeConfig.releaseIdentity}`);
        }
        if (websocketUrls.length !== 0) fail(`showcase opened WebSocket(s): ${websocketUrls.join(', ')}`);

        console.log('showcase_notice=PASS');
        console.log('connect_block_present=PASS');
        console.log('connect_rejection=connection_disabled');
        console.log('runtime_connection_enabled=false');
        console.log(`release_identity=${expectedIdentity}`);
        console.log('websocket_count=0');
    } finally {
        await browser.close();
    }
})().catch(error => {
    console.error(error.stack || error.message || String(error));
    process.exitCode = 1;
});
