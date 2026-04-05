import assert from 'node:assert/strict';
import { run as runOps } from './ops-control-center.mjs';
import { run as runField } from './field-service.mjs';
import { run as runInvoice } from './invoice-ops.mjs';
import { run as runSupport } from './customer-support.mjs';
import { run as runJob } from './job-board.mjs';
import { run as runTele } from './telehealth-portal.mjs';

const results = [runOps(), runField(), runInvoice(), runSupport(), runJob(), runTele()];
assert.equal(results.length, 6);
console.log('tier3-smoke-pass', JSON.stringify(results, null, 2));
