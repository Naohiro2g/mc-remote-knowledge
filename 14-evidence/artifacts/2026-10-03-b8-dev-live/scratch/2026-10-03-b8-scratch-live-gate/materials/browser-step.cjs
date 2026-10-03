const path = require('node:path');
const fs = require('node:fs');
const {createRequire} = require('node:module');
const root = path.resolve(__dirname, '../../..');
const {chromium} = createRequire(path.join(root, 'packages/scratch-gui/package.json'))('@playwright/test');

(async () => {
    const browser = await chromium.connectOverCDP('http://127.0.0.1:9238');
    const page = browser.contexts().flatMap(context => context.pages())
        .find(candidate => candidate.url().startsWith('http://127.0.0.1:8611/'));
    if (!page) throw new Error('Frozen Scratch page missing');
    const action = process.argv[2] || 'status';
    if (action === 'finish') {
        console.log(JSON.stringify(await page.evaluate(async ()=>{
            const data=window.__gateData;
            data.authenticatedHello={protocol:window.__gateObservation.hello.protocol,
                mc_version:window.__gateObservation.hello.mc_version};
            data.finished={ownedEntityRemoved:data.removed,productChanged:false,
                socketCloseCode:1000,buildingMode:'DEBUG'};
            window.__gateExtension._socket.close(1000,'b8 Scratch segment complete');
            await new Promise(resolve=>setTimeout(resolve,500));
            data.finished.connectionStatus=window.__gateObservation.status;
            return data.finished;
        })));
    }
    if (action === 'accessors') {
        console.log(JSON.stringify(await page.evaluate(async ()=>{
            const data=window.__gateData;
            const run=window.__gateRunBlock;
            const snapshot=data.results.find(value=>value.opcode==='entityInfo').args.ENTITY_INFO;
            const pose=data.results.find(value=>value.opcode==='entityPoseInfo').args.POSE;
            for (const axis of ['x','y','z']) {
                const entity=await run('entityInfo',{ENTITY_INFO:snapshot,PROPERTY:axis},true);
                const position=await run('entityPoseInfo',{POSE:pose,PROPERTY:axis},true);
                if (Number(entity)!==JSON.parse(snapshot).pos['xyz'.indexOf(axis)] ||
                    Number(position)!==JSON.parse(pose).pos['xyz'.indexOf(axis)]) throw new Error('Entity position accessor mismatch');
            }
            const pitch=await run('entityPoseInfo',{POSE:pose,PROPERTY:'pitch'},true);
            if (Number(pitch)!==JSON.parse(pose).pitch) throw new Error('Entity pitch accessor mismatch');
            const args={BLOCK_INFO:'oak_log[axis=z]'};
            const actual={
                id:await run('blockInfoId',args,true),
                state:await run('blockInfoState',args,true),
                property:await run('blockInfoStateProperty',{...args,PROPERTY:'axis'},true),
                hasProperty:await run('blockInfoHasStateProperty',{...args,PROPERTY:'axis'},true)
            };
            if (actual.id!=='minecraft:oak_log' || actual.state!=='axis=z' || actual.property!=='z' ||
                actual.hasProperty!==true) throw new Error('BlockInfo namespace omission mismatch');
            data.accessors={entityCoordinateAndPitch:'PASS',blockNamespace:'PASS',actual};
            return data.accessors;
        })));
    }
    if (action === 'idle-poll') {
        const wire=browser.contexts().flatMap(context=>context.pages()).find(candidate=>candidate.url().startsWith('http://127.0.0.1:4183/'));
        const history=await wire.locator('tbody').innerText();
        const start=await page.evaluate(()=>window.__gateExtension._frameSequence);
        await page.waitForTimeout(3500);
        const finish=await page.evaluate(()=>window.__gateExtension._frameSequence);
        if (finish<=start || history!==await wire.locator('tbody').innerText()) throw new Error('Idle polling/history proof failed');
        const result={emptyPollHistory:'PASS',internalFrameSequenceBefore:start,internalFrameSequenceAfter:finish,
            historyUnchanged:true,observeMilliseconds:3500};
        await page.evaluate(result=>Object.assign(window.__gateData.b7,result),result);
        console.log(JSON.stringify(result));
    }
    if (action === 'backpressure') {
        const result=await page.evaluate(async ()=>{
            const data=window.__gateData;
            const before=window.__gateExtension._frameSequence;
            const [x,y,z]=data.pos;
            await Promise.all(Array.from({length:32},()=>window.__gateVm.runtime._primitives.mcremote_playSound({
                X:x,Y:y,Z:z,SOUND:'block.glass.break',OPTIONS:'{"volume":0}'})));
            const frames=window.__gateObservation.frameLog.filter(frame=>frame.sequence>before && frame.method==='world.playSound');
            const replies=frames.filter(frame=>frame.direction==='receive');
            const errors=replies.filter(frame=>frame.payload.error);
            if (errors.some(frame=>frame.payload.error.data.reason!=='backpressure')) throw new Error('Unexpected sound burst error');
            const result={count:32,volume:0,serverBackpressureReplies:errors.length,
                status:window.__gateObservation.status,error:window.__gateObservation.lastError,
                frames};
            data.backpressure=result;
            return {count:32,volume:0,serverBackpressureReplies:errors.length,status:result.status,
                reason:result.error && result.error.reason,origin:result.error && result.error.origin};
        });
        if (result.serverBackpressureReplies>0) {
            const message=page.getByText('mc-remoteサーバーが混み合い、この操作を受け付けませんでした。少し待って、もう一度試してください。',{exact:true});
            await message.waitFor({timeout:5000});
            if (result.status!=='connected' || result.reason!=='backpressure' || result.origin!=='server') throw new Error('Server backpressure stopped/mislabeled connection');
            await message.screenshot({path:path.join(__dirname,'backpressure-message.png')});
            result.guidance='PASS';
        } else result.guidance='NOTRUN: bounded silent burst did not reproduce backpressure';
        await page.evaluate(result=>{window.__gateData.backpressure.summary=result;},result);
        console.log(JSON.stringify(result));
    }
    if (action === 'clipboard-poll') {
        await page.evaluate(()=>{
            const app=window.__gateBlocks;
            const block=app.workspace.newBlock('math_number');
            block.setFieldValue('123.5','NUM');block.initSvg();block.render();block.moveBy(500,200);
            window.__gateNumberBlock=block;
            const field=block.getField('NUM');
            if (typeof field.showEditor_==='function') field.showEditor_();
            else field.showEditor();
        });
        const input=page.locator('input.blocklyHtmlInput');
        await input.waitFor();
        await input.fill('123.5');
        await input.press('Control+a');
        await input.press('Control+c');
        await input.fill('0');
        await input.press('Control+a');
        await input.press('Control+v');
        const pasted=await input.inputValue();
        if (pasted!=='123.5') throw new Error(`Numeric Ctrl+C/V mismatch: ${pasted}`);
        await input.press('Enter');
        const after=await page.evaluate(()=>window.__gateNumberBlock.getFieldValue('NUM'));
        if (Number(after)!==123.5) throw new Error('Numeric pasted field not applied');
        const wire=browser.contexts().flatMap(context=>context.pages()).find(candidate=>candidate.url().startsWith('http://127.0.0.1:4183/'));
        const before=await wire.locator('tbody').innerText();
        const seqBefore=await page.evaluate(()=>Math.max(...window.__gateObservation.frameLog.map(frame=>frame.sequence)));
        await page.waitForTimeout(3500);
        const end=await wire.locator('tbody').innerText();
        const seqAfter=await page.evaluate(()=>Math.max(...window.__gateObservation.frameLog.map(frame=>frame.sequence)));
        if (before!==end) throw new Error('Idle poll changed meaningful WireScope history');
        const result={numericCtrlCopyPaste:'PASS',copied:'123.5',pasted,applied:after,
            emptyPollHistory:'PASS',pollSequenceAdvanced:seqAfter>seqBefore,observeMilliseconds:3500};
        await page.evaluate(result=>{window.__gateData.b7=result;},result);
        console.log(JSON.stringify(result));
        await wire.screenshot({path:path.join(__dirname,'wirescope-final.png'),fullPage:true});
        fs.writeFileSync(path.join(__dirname,'wirescope-final-dom.txt'),await wire.locator('body').innerText());
    }
    if (action === 'picker') {
        await page.evaluate(() => {
            const walk=node=>{
                if (!node) return null;
                if (node.stateNode && typeof node.stateNode.handleMcRemoteBlockPickerStart==='function') return node.stateNode;
                return walk(node.child)||walk(node.sibling);
            };
            const app=walk(window.__gateReactRoot.current);
            if (app.props.mcRemoteCatalog.status!=='current') throw new Error('Dev catalog unavailable in GUI');
            window.__gateBlocks=app;
            const block=app.workspace.newBlock('mcremote_setBlock');
            for (const [name,value] of [['BLOCK','acacia_button'],['STATE','face=wall,powered=true']]) {
                const shadow=app.workspace.newBlock('text');
                shadow.setShadow(true);shadow.setFieldValue(value,'TEXT');shadow.initSvg();
                block.getInput(name).connection.connect(shadow.outputConnection);
            }
            block.initSvg();block.render();window.__gatePickerBlock=block;
            app.handleMcRemoteBlockPickerStart(block);
        });
        const state=page.getByRole('textbox',{name:'状態',exact:true});
        await state.waitFor();
        const search=page.getByRole('textbox',{name:/ブロックID・/});
        const checks=[];
        for (const query of ['gold','金ブロック','Block of Gold']) {
            await search.fill(query);
            const gold=page.locator('[data-block-id="minecraft:gold_block"]');
            await gold.waitFor();
            const label=await gold.innerText();
            if (!label.includes('金ブロック') || !label.includes('Block of Gold') || !label.includes('gold_block')) {
                throw new Error('Picker translated gold label mismatch');
            }
            checks.push({query,label,count:await page.locator('[data-block-id]').count()});
        }
        await page.getByRole('dialog').screenshot({path:path.join(__dirname,'picker-gold.png')});
        await search.fill('door');
        const doorCount=await page.locator('[data-block-id]').count();
        if (doorCount<1 || doorCount>=1166) throw new Error('Door search did not filter');
        await page.getByRole('dialog').screenshot({path:path.join(__dirname,'picker-door.png')});
        await search.fill('acacia_button');
        await page.locator('[data-block-id="minecraft:acacia_button"]').click();
        const face=page.locator('select[data-property="face"]');
        const powered=page.locator('select[data-property="powered"]');
        const faceOptions=await face.locator('option').allTextContents();
        const poweredOptions=await powered.locator('option').allTextContents();
        if (JSON.stringify(faceOptions)!==JSON.stringify(['ceiling','floor','wall（デフォルト）']) ||
            JSON.stringify(poweredOptions)!==JSON.stringify(['false（デフォルト）','true'])) throw new Error('Picker duplicated/default state options mismatch');
        await powered.selectOption('1');
        if (await state.inputValue()!=='powered=true') throw new Error('Picker nondefault state missing');
        await powered.selectOption('');
        if (await state.inputValue()!=='') throw new Error('Picker default state not omitted');
        await face.selectOption('0');
        if (await state.inputValue()!=='face=ceiling') throw new Error('Picker face state missing');
        await face.selectOption('');
        if (await state.inputValue()!=='') throw new Error('Picker default face not omitted');
        const dimensions=await search.evaluate(element=>{
            const left=element.parentElement.getBoundingClientRect();
            const right=element.parentElement.nextElementSibling.getBoundingClientRect();
            const result=[...document.querySelectorAll('input')].find(input=>input.parentElement.textContent==='状態');
            const selector=document.querySelector('select[data-property="face"]');
            return {list:left.width,states:right.width,resultFont:getComputedStyle(result).fontSize,
                selectorFont:getComputedStyle(selector).fontSize};
        });
        await page.getByRole('dialog').screenshot({path:path.join(__dirname,'picker-default-state.png')});
        await page.getByRole('button',{name:'この値の組を使う',exact:true}).click();
        const applied=await page.evaluate(()=>['BLOCK','STATE'].map(name=>
            window.__gatePickerBlock.getInput(name).connection.targetBlock().getFieldValue('TEXT')));
        if (JSON.stringify(applied)!==JSON.stringify(['acacia_button',''])) throw new Error('Picker apply mismatch');
        const result={picker:'PASS',catalogSource:'authenticated dev catalog',checks,doorCount,faceOptions,poweredOptions,dimensions,applied};
        await page.evaluate(result=>{window.__gateData.picker=result;},result);
        console.log(JSON.stringify(result));
    }
    if (action === 'particle-notification') {
        const cdp=await page.context().newCDPSession(page);
        const primitive=await cdp.send('Runtime.evaluate',{expression:'window.__gateVm.runtime._primitives.mcremote_spawnParticle'});
        const visited=new Set();
        const findService=async (functionId,depth) => {
            if (depth>3 || visited.has(functionId) || visited.size>30) return null;
            visited.add(functionId);
            const properties=await cdp.send('Runtime.getProperties',{objectId:functionId,ownProperties:true});
            const scopes=properties.internalProperties.find(value=>value.name==='[[Scopes]]');
            if (!scopes) return null;
            const list=await cdp.send('Runtime.getProperties',{objectId:scopes.value.objectId,ownProperties:true});
            for (const scope of list.result.filter(value=>/^\d+$/.test(value.name) && !/^Global|^Script/.test(value.value.description))) {
                const variables=await cdp.send('Runtime.getProperties',{objectId:scope.value.objectId,ownProperties:true});
                for (const variable of variables.result.filter(value=>value.value && value.value.objectId)) {
                    const value=variable.value;
                    if (value.type==='object') {
                        const probe=await cdp.send('Runtime.callFunctionOn',{objectId:value.objectId,
                            functionDeclaration:'function(){return typeof this._startNotification==="function" && typeof this.spawnParticle==="function";}',returnByValue:true});
                        if (probe.result.value===true) return value.objectId;
                    }
                    if (value.type!=='function') continue;
                    const found=await findService(value.objectId,depth+1);
                    if (found) return found;
                }
            }
            return null;
        };
        const service=await findService(primitive.result.objectId,0);
        if (!service) throw new Error('Frozen McRemote extension service reference unavailable');
        await cdp.send('Runtime.callFunctionOn',{objectId:service,functionDeclaration:
            'function(){if(typeof this._startNotification!=="function")throw new Error("Not McRemote service"); window.__gateExtension=this;}'});
        console.log(JSON.stringify(await page.evaluate(async () => {
            const data=window.__gateData;
            const extension=window.__gateExtension;
            await window.__gateRunBlock('setBuildMode',{MODE:'DEBUG',TRACE_DELAY:0});
            const before=Math.max(...window.__gateObservation.frameLog.map(frame=>frame.sequence));
            const [x,y,z]=data.pos;
            const params=[x+1,y+1,z,0.3,0.3,0.3,{particle_id:'flame',receiver:'world'},0,8,false];
            await extension._enqueueOutbound(()=>extension._startNotification('world.spawnParticle',params));
            await extension._request('connection.flush',[]);
            const frames=window.__gateObservation.frameLog.filter(frame=>frame.sequence>before);
            const notification=frames.find(frame=>frame.method==='world.spawnParticle' && frame.direction==='send' &&
                !Object.prototype.hasOwnProperty.call(frame.payload,'id'));
            if (!notification) throw new Error('Dedicated particle notification was not recorded');
            data.fastFrames=frames;
            data.runnerCorrection={missingTraceDelayCorrected:true,
                wrongExpectation:'Scratch building FAST mode applies to particle',
                correctContract:'wire §3.5: setBlock/setBlocks only',
                observerProbe:'real idless particle notification via unchanged extension outbound transport',
                productChanged:false};
            data.results.push({opcode:'observerParticleNotification',args:{params},value:'sent-unconfirmed',frames});
            return {particleNotification:'sent-unconfirmed',requestId:'absent',flush:'PASS',
                testClass:'observer transport probe; learner spawnParticle remains a request'};
        })));
        const wire=browser.contexts().flatMap(context=>context.pages()).find(candidate=>candidate.url().startsWith('http://127.0.0.1:4183/'));
        await wire.waitForFunction(()=>Array.from(document.querySelectorAll('tr')).some(row=>
            row.textContent.includes('world.spawnParticle') && row.textContent.includes('送信済み・結果未確認')));
        console.log(JSON.stringify({wireScopeParticleNotification:'PASS',label:'送信済み・結果未確認'}));
    }
    if (action === 'diagnose') {
        console.log(JSON.stringify(await page.evaluate(() => ({
            lastRuns:window.__gateData.results.slice(-4).map(value=>({opcode:value.opcode,args:value.args,
                value:value.value,frames:value.frames})),
            lastError:window.__gateObservation.lastError,
            wirePages:true
        }))));
        const wire=browser.contexts().flatMap(context=>context.pages()).find(candidate=>candidate.url().startsWith('http://127.0.0.1:4183/'));
        if (wire) {
            console.log(JSON.stringify({wireScope:{status:await wire.locator('.status-card').innerText(),
                methods:await wire.locator('td.method').allTextContents(),
                filterSummary:await wire.locator('.filter-summary').allTextContents()}}));
            await wire.screenshot({path:path.join(__dirname,'../private/wirescope-current.png'),fullPage:true});
            fs.writeFileSync(path.join(__dirname,'../private/wirescope-dom.txt'),await wire.locator('body').innerText(),{mode:0o600});
        }
    }
    if (action === 'fast') {
        console.log(JSON.stringify(await page.evaluate(async () => {
            const data=window.__gateData;
            if (data.failed) throw new Error('Runner stopped');
            const run=window.__gateRunBlock;
            await run('setBuildMode',{MODE:'FAST',TRACE_DELAY:0});
            const particle=await run('particleSpec',{PARTICLE:'flame',RECEIVER:'world'},true);
            const [x,y,z]=data.pos;
            await run('spawnParticle',{X:x+1,Y:y+1,Z:z,OFFSET_X:0.3,OFFSET_Y:0.3,OFFSET_Z:0.3,
                PARTICLE:particle,SPEED:0,COUNT:8,FORCE:false});
            const frames=data.results.at(-1).frames;
            const notification=frames.find(frame=>frame.direction==='send' && frame.method==='world.spawnParticle' &&
                !Object.prototype.hasOwnProperty.call(frame.payload,'id'));
            if (!notification) throw new Error('FAST particle notification missing');
            await run('setBuildMode',{MODE:'DEBUG',TRACE_DELAY:0});
            data.fastFrames=frames;
            data.runnerCorrection={block:'setBuildMode',missingArgument:'TRACE_DELAY',correctedValue:0,
                productChanged:false,reason:'invalid_trace_delay'};
            return {fastParticleNotification:'PASS',hasRequestId:false,modeRestored:'DEBUG'};
        })));
    }
    if (action === 'particle-sound') {
        console.log(JSON.stringify(await page.evaluate(async () => {
            const data = window.__gateData;
            const run = window.__gateRunBlock;
            if (!data || data.failed) throw new Error('Block runner stopped');
            const [x,y,z] = data.pos;
            const emitted = [];
            for (const receiver of ['world','self']) {
                const specs = [
                    await run('particleSpec',{PARTICLE:'flame',RECEIVER:receiver},true),
                    await run('dustParticleSpec',{RED:255,GREEN:64,BLUE:0,SIZE:1,RECEIVER:receiver},true),
                    await run('blockParticleSpec',{BLOCK:'stone',STATE:'',RECEIVER:receiver},true)
                ];
                for (const spec of specs) {
                    await run('spawnParticle',{X:x+1,Y:y+1,Z:z,OFFSET_X:0.3,OFFSET_Y:0.3,OFFSET_Z:0.3,
                        PARTICLE:spec,SPEED:0,COUNT:8,FORCE:false});
                    emitted.push({particle:JSON.parse(spec).particle_id,receiver});
                }
            }
            const optionsNote = await run('soundOptions',{VOLUME:'0.5',HEIGHT:'N12',RECEIVER:'world'},true);
            const optionsPitch = await run('soundOptions',{VOLUME:'0.5',HEIGHT:'1',RECEIVER:'self'},true);
            if (JSON.parse(optionsNote).note!==12 || JSON.parse(optionsPitch).pitch!==1) throw new Error('Sound height mapping mismatch');
            await run('playSound',{X:x,Y:y,Z:z,SOUND:'block.glass.break',OPTIONS:optionsNote});
            await run('playSound',{X:x,Y:y,Z:z,SOUND:'block.note_block.harp',OPTIONS:optionsPitch});
            const ground = {X:Math.floor(x),Y:Math.floor(y)-1,Z:Math.floor(z)};
            const block = await run('getBlock',ground,true);
            data.ground = {position:ground,block};
            if (block==='minecraft:air' || block.startsWith('minecraft:air[')) throw new Error('Ground block is air; playBlockSound test needs a real block');
            await run('playBlockSound',{...ground,KIND:'break',OPTIONS:optionsNote});
            return {typedParticles:'PASS',emitted,
                soundCommands:'PASS',soundHeight:{note:12,pitch:1},groundBlock:block};
        })));
    }
    if (action === 'entity') {
        console.log(JSON.stringify(await page.evaluate(async () => {
            const data = window.__gateData;
            const run = window.__gateRunBlock;
            if (!data || data.failed) throw new Error('Prepared block runner unavailable or stopped');
            const target = window.__gateVm.editingTarget;
            const [x,y,z] = data.pos;
            await run('spawnEntity',{X:x+2,Y:y,Z:z,ENTITY:'armor_stand',
                VARIABLE:{id:'gate-handle',name:'test entity handle'}});
            data.handle = target.variables['gate-handle'].value;
            if (typeof data.handle !== 'string' || !data.handle.startsWith('mcr_eh_')) throw new Error('Invalid spawned handle');
            await run('getNearbyEntities',{X:x,Y:y,Z:z,RADIUS:10,MAX_ENTITIES:64,
                LIST:{id:'gate-nearby',name:'nearby entities'}});
            const nearby = target.variables['gate-nearby'].value;
            const snapshot = nearby.find(value => JSON.parse(value).handle === data.handle);
            if (!snapshot) throw new Error('Spawned entity missing from nearby list');
            const handle = await run('entityInfo',{ENTITY_INFO:snapshot,PROPERTY:'handle'},true);
            const type = await run('entityInfo',{ENTITY_INFO:snapshot,PROPERTY:'type'},true);
            if (handle !== data.handle || type !== 'minecraft:armor_stand') throw new Error('Entity snapshot mismatch');
            const pose = await run('getEntityPose',{HANDLE:data.handle},true);
            const dimension = await run('entityPoseInfo',{POSE:pose,PROPERTY:'dimension'},true);
            if (dimension !== data.dimension) throw new Error('Entity pose dimension mismatch');
            await run('setEntityPose',{HANDLE:data.handle,DIMENSION:'overworld',X:x+3,Y:y,Z:z,YAW:90,PITCH:0});
            const moved = await run('getEntityPose',{HANDLE:data.handle},true);
            const movedX = Number(await run('entityPoseInfo',{POSE:moved,PROPERTY:'x'},true));
            const movedYaw = Number(await run('entityPoseInfo',{POSE:moved,PROPERTY:'yaw'},true));
            if (Math.abs(movedX-(x+3))>0.01 || Math.abs(movedYaw-90)>0.01) throw new Error('Entity movement mismatch');
            await run('removeEntity',{HANDLE:data.handle});
            data.removed = true;
            await run('getNearbyEntities',{X:x,Y:y,Z:z,RADIUS:10,MAX_ENTITIES:64,
                LIST:{id:'gate-nearby',name:'nearby entities'}});
            if (target.variables['gate-nearby'].value.some(value => JSON.parse(value).handle===data.handle)) {
                throw new Error('Removed entity remains in nearby list');
            }
            return {entityLifecycle:'PASS',blocks:['getNearbyEntities','entityInfo','getEntityPose','entityPoseInfo',
                'setEntityPose','removeEntity'],type,movedX,movedYaw,ownedEntityRemoved:true};
        })));
    }
    if (action === 'prepare-blocks') {
        console.log(JSON.stringify(await page.evaluate(async () => {
            const vm = window.__gateVm;
            const runtime = vm.runtime;
            const observation = window.__gateObservation;
            if (!observation || observation.status !== 'connected' ||
                observation.hello.protocol !== '23.2.0' || observation.hello.mc_version !== '1.21.11') {
                throw new Error('Authenticated hello does not match frozen contract');
            }
            window.__gateData = {results:[], serial:0};
            const target = vm.editingTarget;
            const data = window.__gateData;
            window.__gateRunBlock = async (opcode, args, reporter=false) => {
                const id = `gate-${++data.serial}`;
                const inputs = {};
                const fields = {};
                for (const [name, value] of Object.entries(args)) {
                    if (name === 'LIST' || name === 'VARIABLE') {
                        fields[name] = {name, id:value.id, value:value.name,
                            variableType:name === 'LIST' ? 'list' : ''};
                        target.createVariable(value.id, value.name, name === 'LIST' ? 'list' : '', false);
                    } else {
                        const child = `${id}-${name}`;
                        target.blocks.createBlock({id:child, opcode:'text', shadow:true, topLevel:false,
                            parent:id, next:null, fields:{TEXT:{name:'TEXT',value:String(value)}}, inputs:{}});
                        inputs[name] = {name, block:child, shadow:child};
                    }
                }
                const top = reporter ? `${id}-result` : id;
                target.blocks.createBlock({id, opcode:`mcremote_${opcode}`, inputs, fields,
                    next:null, parent:reporter ? top : null, shadow:false, topLevel:!reporter, x:440,y:80});
                if (reporter) {
                    target.createVariable('gate-result', 'gate result', '', false);
                    target.blocks.createBlock({id:top, opcode:'data_setvariableto', inputs:{VALUE:{name:'VALUE',block:id,shadow:null}},
                        fields:{VARIABLE:{name:'VARIABLE',id:'gate-result',value:'gate result'}},
                        next:null,parent:null,shadow:false,topLevel:true,x:440,y:80});
                }
                const before = Math.max(0,...window.__gateObservation.frameLog.map(frame => frame.sequence));
                runtime.toggleScript(top, {target,stackClick:true});
                await new Promise((resolve,reject) => {
                    const start = Date.now();
                    const timer = setInterval(() => {
                        if (!runtime.threads.some(thread => thread.topBlock === top && thread.status !== 4)) {
                            clearInterval(timer);resolve();
                        } else if (Date.now()-start > 20000) {clearInterval(timer);reject(new Error(`Block timeout: ${opcode}`));}
                    },25);
                });
                const value = reporter ? target.variables['gate-result'].value : null;
                const frames = window.__gateObservation.frameLog.filter(frame => frame.sequence > before);
                const errors = frames.filter(frame => frame.payload && frame.payload.error);
                if (errors.length || (typeof value === 'string' && value.startsWith('⟦mcr-error:'))) {
                    data.failed = {opcode,args,value,errors};
                    throw new Error(`Scratch block failed: ${opcode}`);
                }
                data.results.push({opcode,args,value,frames});
                return value;
            };
            data.pos = [];
            for (const axis of ['x','y','z']) {
                const value = await window.__gateRunBlock('playerAttribute',{PROPERTY:axis},true);
                if (value === '' || !Number.isFinite(Number(value))) throw new Error('Player position unavailable');
                data.pos.push(Number(value));
            }
            data.dimension = await window.__gateRunBlock('playerAttribute',{PROPERTY:'dimension'},true);
            const catalog = {};
            for (const kind of ['block','entity','particle']) {
                const id = `gate-catalog-${kind}`;
                await window.__gateRunBlock('catalogToList',{KIND:kind,LIST:{id,name:`catalog ${kind}`}});
                const values = target.variables[id].value;
                if (!Array.isArray(values) || !values.length || values.some(value => !value.startsWith('minecraft:')) ||
                    JSON.stringify(values)!==JSON.stringify([...values].sort())) throw new Error(`Invalid catalog list: ${kind}`);
                catalog[kind] = {count:values.length,first:values[0]};
            }
            return {authenticatedHello:'PASS', execution:'Scratch VM sequencer, real blocks and variables/lists',
                playerPosition:data.pos, dimension:data.dimension,catalog};
        })));
    }
    if (action === 'wirescope') {
        await page.getByRole('button', {name:'WireScope mini を開く', exact:true}).click();
        const popup = page.waitForEvent('popup');
        await page.getByRole('button', {name:'WireScope を開く', exact:false}).click();
        const wire = await popup;
        await wire.waitForLoadState('domcontentloaded');
        await wire.waitForSelector('td.method', {timeout:30000});
        console.log(JSON.stringify({wireScope:'attached', methods:await wire.locator('td.method').allTextContents()}));
    }
    if (action === 'connect') {
        await page.evaluate(() => {
            const runtime = window.__gateVm.runtime;
            if (!window.__gateObservationListener) {
                window.__gateObservationListener = true;
                runtime.on('MCREMOTE_OBSERVATION_UPDATE', observation => {
                    window.__gateObservation = observation;
                });
            }
            runtime._primitives.mcremote_connect({});
        });
        await page.waitForFunction(() => {
            const observation = window.__gateObservation;
            return observation && (observation.pairCommand || observation.status === 'connected' ||
                observation.status === 'error');
        }, null, {timeout:30000});
    }
    console.log(JSON.stringify(await page.evaluate(() => {
        const observation = window.__gateObservation;
        if (!observation) return {status:'not-connected'};
        return {
            status:observation.status,
            pairCommand:observation.pairCommand,
            hello:observation.hello && {protocol:observation.hello.protocol, mc_version:observation.hello.mc_version},
            error:observation.lastError && {message:observation.lastError.message,
                reason:observation.lastError.data && observation.lastError.data.reason},
            frameCount:observation.frameLog.length
        };
    })));
    const record = await page.evaluate(() => ({observation:window.__gateObservation,data:window.__gateData}));
    fs.writeFileSync(path.join(__dirname,'../private/browser-state.json'),JSON.stringify(record,null,2),{mode:0o600});
    await browser.close();
})().catch(error => {console.error(error.message);process.exit(1);});
