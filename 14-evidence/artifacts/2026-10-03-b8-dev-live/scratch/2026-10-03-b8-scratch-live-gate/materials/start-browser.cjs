const path = require('node:path');
const {createRequire} = require('node:module');
const root = path.resolve(__dirname, '../../..');
const {chromium} = createRequire(path.join(root, 'packages/scratch-gui/package.json'))('@playwright/test');

(async () => {
    const browser = await chromium.launch({headless: true, executablePath:'/usr/bin/google-chrome',
        args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader',
            '--remote-debugging-port=9238','--remote-debugging-address=127.0.0.1']});
    const context = await browser.newContext({viewport:{width:1440,height:1000},locale:'ja-JP'});
    const page = await context.newPage();
    await page.addInitScript(() => {
        window.__REACT_DEVTOOLS_GLOBAL_HOOK__ = {
            supportsFiber:true,inject:()=>1,
            onCommitFiberRoot:(_id,root)=>{window.__gateReactRoot=root;},
            onCommitFiberUnmount:()=>{}
        };
    });
    await page.goto('http://127.0.0.1:8611/?extension=mcremote',
        {waitUntil:'domcontentloaded',timeout:120000});
    await page.waitForFunction(() => {
        const walk = node => {
            if (!node) return null;
            const instance=node.stateNode;
            if (instance && typeof instance.handleMcRemoteBlockPickerStart==='function') return instance;
            return walk(node.child)||walk(node.sibling);
        };
        const app=window.__gateReactRoot && walk(window.__gateReactRoot.current);
        if (!app || !app.props.vm.runtime._primitives.mcremote_connect) return false;
        window.__gateVm=app.props.vm;
        return true;
    },null,{timeout:60000});
    console.log('Frozen Scratch browser ready; no MC connection requested. CDP port 9238.');
    const shutdown=async()=>{await browser.close();process.exit(0);};
    process.on('SIGTERM',shutdown);
    process.on('SIGINT',shutdown);
    await new Promise(()=>{});
})().catch(error=>{console.error(error);process.exitCode=1;});
