// Run: node ApisLM_SDK/test/dpp.test.mjs  (after `npx tsc -p ApisLM_SDK`; uses Node's built-in test runner)
import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { DPPGenerator } = require('../dist/dpp-generator.js');

const { privateKey, publicKey } = crypto.generateKeyPairSync('ed25519');
const priv = privateKey.export({ type: 'pkcs8', format: 'pem' });
const pub = publicKey.export({ type: 'spki', format: 'pem' });
const data = { batchId: 'B-1', apiaryLocation: { lat: 30, lng: 31, name: 'A' }, harvestDate: '2026-05-01', floralSource: ['clover'], metrics: { moisturePercent: 17.5, totalWeightKg: 120 } };

test('valid passport verifies', () => {
  const p = new DPPGenerator(priv).generateSignedPassport(data);
  assert.equal(DPPGenerator.verifyPassport(p, pub), true);
});
test('key order does not matter', () => {
  const p = new DPPGenerator(priv).generateSignedPassport(data);
  const { signature, ...rest } = p;
  assert.equal(DPPGenerator.verifyPassport({ signature, metrics: rest.metrics, floralSource: rest.floralSource, harvestDate: rest.harvestDate, apiaryLocation: rest.apiaryLocation, batchId: rest.batchId }, pub), true);
});
test('tampered data is rejected', () => {
  const p = new DPPGenerator(priv).generateSignedPassport(data);
  assert.equal(DPPGenerator.verifyPassport({ ...p, metrics: { ...p.metrics, totalWeightKg: 999 } }, pub), false);
});
test('wrong key, missing or garbage signature are rejected', () => {
  const p = new DPPGenerator(priv).generateSignedPassport(data);
  const other = crypto.generateKeyPairSync('ed25519').publicKey.export({ type: 'spki', format: 'pem' });
  assert.equal(DPPGenerator.verifyPassport(p, other), false);
  assert.equal(DPPGenerator.verifyPassport({ ...p, signature: undefined }, pub), false);
  assert.equal(DPPGenerator.verifyPassport({ ...p, signature: '!!!' }, pub), false);
  assert.equal(DPPGenerator.verifyPassport(p, 'not a key'), false);
});
test('non-Ed25519 key is refused', () => {
  const rsa = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey.export({ type: 'pkcs8', format: 'pem' });
  assert.throws(() => new DPPGenerator(rsa));
});
