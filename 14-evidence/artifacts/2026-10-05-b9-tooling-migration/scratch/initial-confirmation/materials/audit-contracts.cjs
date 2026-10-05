const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const root = process.cwd();
const fromRoot = Module.createRequire(path.join(root, 'package.json'));
const ts = fromRoot('typescript');
const clone = value => JSON.parse(JSON.stringify(value));
const readJson = relative => JSON.parse(fs.readFileSync(path.join(root, relative), 'utf8'));
const event = fromRoot('./packages/scratch-vm/src/extensions/scratch3_mcremote/event.js');
const McRemote = fromRoot('./packages/scratch-vm/src/extensions/scratch3_mcremote/index.js');

const observerPath = path.join(root, 'mc-remote/live/src/observer.ts');
const observerModule = new Module(observerPath);
observerModule.paths = Module._nodeModulePaths(path.dirname(observerPath));
observerModule._compile(ts.transpileModule(fs.readFileSync(observerPath, 'utf8'), {
    compilerOptions: {target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS}
}).outputText, observerPath);
const {parseObserverSnapshot} = observerModule.exports;

const poll = readJson('mc-remote/protocol/test/fixtures/events-v23.json').poll_result;
const futurePoll = clone(poll);
futurePoll.events[1] = {
    sequence: 2,
    type: 'future_example',
    dimension: 'minecraft:overworld',
    origin: [200, 0, 200],
    future_payload: {example: true}
};

const snapshotFor = (method, result, protocol = '23.2.0') => {
    const snapshot = clone(readJson('mc-remote/live/test/fixtures/scratch-main-lifecycle.json')[0]);
    snapshot.streams[0].hello.protocol = protocol;
    snapshot.streams[0].frames = [{
        sequence: 1,
        observed_at: snapshot.emitted_at,
        direction: 'receive',
        request_id: 1,
        method,
        payload: {result}
    }];
    return snapshot;
};

const rejected = callback => {
    let caught;
    try { callback(); } catch (error) { caught = error; }
    assert(caught, 'The current baseline must reproduce the reported rejection.');
    return {reason: caught.reason || null, message: caught.message};
};

(async () => {
    const baseline = event.validateEventPollResult(poll, 0, event.initialEventStatus());
    assert.equal(baseline.cursor, 3);
    parseObserverSnapshot(snapshotFor('events.poll', poll));
    parseObserverSnapshot(snapshotFor('events.poll', poll, '23.3.0'));
    const scratchUnknown = rejected(() =>
        event.validateEventPollResult(futurePoll, 0, event.initialEventStatus()));
    const observerUnknown = rejected(() =>
        parseObserverSnapshot(snapshotFor('events.poll', futurePoll, '23.3.0')));
    parseObserverSnapshot(snapshotFor('chat.post', null));
    parseObserverSnapshot(snapshotFor('chat.post', true));

    const probe = Object.create(McRemote.prototype);
    let sent;
    probe._request = (method, params) => {
        sent = {method, params};
        return Promise.resolve(null);
    };
    assert.equal(await probe.postToChat({MSG: 'example'}), undefined);
    assert.deepEqual(sent, {method: 'chat.post', params: ['example']});

    process.stdout.write(`${JSON.stringify({
        audit_completed: true,
        known_poll: {scratch_cursor: baseline.cursor, wirescope_accepts: true,
            wirescope_accepts_compatible_minor: '23.3.0'},
        unknown_event: {scratch: scratchUnknown, wirescope: observerUnknown},
        chat_null: {scratch_command_accepts: true, wirescope_accepts: true},
        chat_result_validation: {wirescope_also_accepts_true: true, strict_null_rule_missing: true},
        non_claim: 'This reproduces the current behavior; it does not establish b9 conformance.'
    }, null, 2)}\n`);
})().catch(error => {
    process.stderr.write(`${error.stack}\n`);
    process.exitCode = 1;
});
