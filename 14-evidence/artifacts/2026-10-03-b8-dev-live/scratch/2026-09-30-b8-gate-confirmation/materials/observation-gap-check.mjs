import {readFileSync} from 'node:fs';
import {parseObserverSnapshot} from '../../../mc-remote/live/src/observer.ts';

const source = readFileSync('packages/scratch-gui/src/lib/mcremote-wirescope-source.js', 'utf8');
const {toWireScopeSnapshot} = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const fixture = JSON.parse(readFileSync('mc-remote/live/test/fixtures/scratch-main-lifecycle.json', 'utf8'))[0];
const hello = {
    protocol: '23.2.0', mc_version: '1.21.11', supported_mc_versions: ['1.21.11'],
    catalogHash: null, world_constants: {y_sea: 62}, dimension: 'minecraft:overworld', origin: [0, 0, 0]
};
const cases = [
    ['particle-qualified', 'world.spawnParticle', [0, 0, 0, 0, 0, 0, 'minecraft:flame', 0, 1]],
    ['particle-short', 'world.spawnParticle', [0, 0, 0, 0, 0, 0, 'flame', 0, 1]],
    ['particle-typed', 'world.spawnParticle', [0, 0, 0, 0, 0, 0, {particle_id: 'minecraft:flame'}, 0, 1]],
    ['particle-fast', 'world.spawnParticle', [0, 0, 0, 0, 0, 0, 'minecraft:flame', 0, 1], true],
    ['entity-qualified', 'world.spawnEntity', [0, 0, 0, 'minecraft:cow']],
    ['entity-short', 'world.spawnEntity', [0, 0, 0, 'cow']],
    ['nearby', 'world.getNearbyEntities', [0, 0, 0, 5, 2]],
    ['get-pose', 'entity.getPose', ['mcr_eh_example']],
    ['set-pose', 'entity.setPose', ['mcr_eh_example', 'overworld', 0, 0, 0, 0, 0]],
    ['remove', 'entity.remove', ['mcr_eh_example']],
    ['sound', 'world.playSound', [0, 0, 0, 'entity.cow.ambient']],
    ['block-sound', 'world.playBlockSound', [0, 0, 0, 'place']]
];
const results = cases.map(([id, method, params, notification]) => {
    const requestId = notification ? null : 1;
    const snapshot = structuredClone(fixture);
    snapshot.streams[0].hello.protocol = '23.2.0';
    snapshot.streams[0].frames = [{sequence: 1, observed_at: 1, direction: 'send', request_id: requestId,
        method, payload: {params}}];
    let validatorError = null;
    try {
        parseObserverSnapshot(snapshot);
    } catch (error) {
        validatorError = error.message;
    }
    const observation = {status: 'connected', displayAlias: 'TEST-ONLY', hello, frameLog: [{
        sequence: 1, timestamp: 1, direction: 'send', id: requestId, method,
        payload: {jsonrpc: '2.0', ...(notification ? {} : {id: requestId}), method, params}
    }]};
    const projected = toWireScopeSnapshot(observation, 'test-only', 1);
    return {id, method, validatorAccepted: validatorError === null, validatorError,
        scratchProjectedFrameCount: projected.streams[0].frames.length};
});
console.log(JSON.stringify({testClass: 'unit/deterministic gap audit', sourceBase:
    '5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe', results}, null, 2));
