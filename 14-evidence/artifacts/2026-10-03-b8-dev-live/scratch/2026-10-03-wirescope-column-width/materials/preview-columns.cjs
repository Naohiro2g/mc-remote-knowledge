const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {createRequire}=require('node:module');
const root=path.resolve(__dirname,'../../..');
const {chromium}=createRequire(path.join(root,'packages/scratch-gui/package.json'))('@playwright/test');
const live=JSON.parse(fs.readFileSync(path.join(root,'handoff-materials/2026-10-03-b8-scratch-live-gate/materials/live-results.json')));
const recorded=live.block_runs.flatMap(run=>run.frames);
const pose=recorded.filter(frame=>frame.method==='entity.getPose').slice(0,2);
const dust=recorded.filter(frame=>frame.method==='world.spawnParticle' && frame.payload.params &&
    frame.payload.params[6].particle_id==='minecraft:dust').slice(0,1);
const sound=recorded.filter(frame=>frame.method==='world.playSound').slice(0,2);
const notification=recorded.find(frame=>frame.method==='world.spawnParticle' && frame.direction==='send' &&
    !Object.prototype.hasOwnProperty.call(frame.payload,'id'));
const frames=[...new Map([...pose,...dust,...sound,notification].map(frame=>[frame.sequence,frame])).values()]
    .sort((a,b)=>a.sequence-b.sequence).map(frame=>({sequence:frame.sequence,observed_at:frame.timestamp,
        direction:frame.direction,request_id:frame.id ?? null,method:frame.method,
        payload:Object.fromEntries(Object.entries(frame.payload).filter(([key])=>['params','result','error'].includes(key)))}));
const snapshot={schema:'mcremote.observer',schema_version:1,emitted_at:Date.now(),
    target:{id:'column-width-preview',display_alias:'LAYOUT-PREVIEW-000001',source_kind:'scratch'},
    streams:[{id:'main',kind:'main',status:'connected',hello:{protocol:'23.2.0',mc_version:'1.21.11',
        supported_mc_versions:['1.21.11'],catalog_hash:null,dimension:'minecraft:overworld',origin:[200,0,200],
        world_constants:{y_sea:62},permissions:{online:true,offline:true,build_range:1000}},frames}]};

const serve=(directory,port)=>new Promise((resolve,reject)=>{
    const server=http.createServer((request,response)=>{
        const pathname=new URL(request.url,'http://localhost').pathname;
        if (pathname==='/replay.html') {
            response.writeHead(200,{'Content-Type':'text/html'});
            response.end('<!doctype html><title>Saved-frame layout preview source</title><p>Saved-frame layout preview; no Minecraft connection</p>');
            return;
        }
        const file=path.resolve(directory,'.'+(pathname==='/'?'/index.html':pathname));
        if (!file.startsWith(directory+path.sep)) {response.writeHead(403);response.end();return;}
        try {
            const body=fs.readFileSync(file);
            response.writeHead(200,{'Content-Type':({'.html':'text/html','.js':'application/javascript','.css':'text/css'}[path.extname(file)]||'application/octet-stream')});
            response.end(body);
        } catch {response.writeHead(404);response.end();}
    });
    server.once('error',reject);
    server.listen(port,'127.0.0.1',()=>resolve(server));
});

(async()=>{
    const servers=[];
    const contexts=[];
    let browser;
    const results=[];
    try {
        servers.push(await serve(path.join(__dirname,'preview-app'),4184));
        servers.push(await serve(path.join(root,'handoff-materials/2026-10-03-b8-scratch-live-gate/runtime/wirescope'),4185));
        browser=await chromium.connectOverCDP('http://127.0.0.1:9238');
        for (const locale of ['ja-JP','en-US','ja-Hira']) {
            const context=await browser.newContext({locale,viewport:{width:1280,height:1000},timezoneId:'Asia/Tokyo'});
            contexts.push(context);
            const source=await context.newPage();
            await source.goto('http://localhost:4184/replay.html');
            await source.evaluate(snapshot=>{
                window.addEventListener('message',event=>{
                    if (event.data.type!=='mcremote.wirescope.ready' ||
                        !['http://127.0.0.1:4184','http://127.0.0.1:4185'].includes(event.origin)) return;
                    const channel=new MessageChannel();
                    const grant=crypto.randomUUID();
                    channel.port1.onmessage=message=>{
                        if (message.data.type==='mcremote.wirescope.redeem' && message.data.grant===grant) {
                            channel.port1.postMessage({type:'mcremote.wirescope.snapshot',protocol_version:1,
                                snapshot,history_window:{dropped_frames:0}});
                        }
                    };
                    event.source.postMessage({type:'mcremote.wirescope.attach',protocol_version:1},event.origin,[channel.port2]);
                    channel.port1.postMessage({type:'mcremote.wirescope.grant',protocol_version:1,grant,expires_at:Date.now()+30000});
                });
            },snapshot);
            const variants={};
            for (const [name,port] of [['before',4185],['after',4184]]) {
                const popup=source.waitForEvent('popup');
                await source.evaluate(port=>window.open(`http://127.0.0.1:${port}/`,'_blank'),port);
                const page=await popup;
                await page.waitForSelector('td.payload',{timeout:10000});
                const measure=()=>page.evaluate(()=>{
                    const row=[...document.querySelectorAll('tbody tr')].find(row=>row.querySelector('.direction wbr') ||
                        row.querySelector('.direction').textContent.includes('未確認') ||
                        row.querySelector('.direction').textContent.includes('unconfirmed') ||
                        row.querySelector('.direction').textContent.includes('みかくにん'));
                    const direction=row.querySelector('.direction');
                    const range=document.createRange();range.selectNodeContents(direction);
                    const lines=new Set([...range.getClientRects()].filter(rect=>rect.width>0 && rect.height>0).map(rect=>Math.round(rect.top)));
                    const time=row.querySelector('.frame-time');
                    const cells=[...row.cells].map(cell=>cell.getBoundingClientRect().width);
                    const wrap=document.querySelector('.table-wrap');
                    return {timeWidth:time.getBoundingClientRect().width,directionWidth:direction.getBoundingClientRect().width,
                        payloadWidth:row.querySelector('.payload').getBoundingClientRect().width,directionLines:lines.size,
                        directionText:direction.textContent,timeText:time.textContent,tooltip:time.querySelector('time').title,
                        tableWidth:row.closest('table').getBoundingClientRect().width,viewportWidth:wrap.clientWidth,
                        timeFits:time.scrollWidth<=time.clientWidth,cells};
                });
                variants[name]={desktop:await measure()};
                if (locale==='ja-JP') {
                    await page.locator('.table-wrap').screenshot({path:path.join(__dirname,`columns-${name}.png`)});
                }
                await page.setViewportSize({width:600,height:900});
                variants[name].narrow=await measure();
                await page.close();
            }
            assert(variants.after.desktop.timeWidth<variants.before.desktop.timeWidth);
            assert(variants.after.desktop.directionWidth<variants.before.desktop.directionWidth);
            assert(variants.after.desktop.payloadWidth>variants.before.desktop.payloadWidth);
            assert.equal(variants.after.desktop.directionLines,2);
            assert.equal(variants.after.desktop.directionText,variants.before.desktop.directionText);
            assert.equal(variants.after.desktop.timeText,variants.before.desktop.timeText);
            assert.equal(variants.after.desktop.tooltip,variants.before.desktop.tooltip);
            assert.equal(variants.after.narrow.timeFits,true);
            results.push({locale,...variants});
        }
        fs.writeFileSync(path.join(__dirname,'column-measurements.json'),JSON.stringify({result:'PASS',
            testClass:'browser UI with saved live frames; no MC connection',results},null,2));
        console.log(JSON.stringify({result:'PASS',results}));
    } finally {
        await Promise.all(contexts.map(context=>context.close()));
        if (browser) await browser.close();
        await Promise.all(servers.map(server=>new Promise(resolve=>server.close(resolve))));
    }
})().catch(error=>{console.error(error);process.exit(1);});
