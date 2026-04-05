import assert from 'node:assert/strict';

export function run() {
  const intake = { consent: true, insurance: true, identity: true };
  const eligible = Object.values(intake).every(Boolean);
  assert.equal(eligible, true);
  return { category: 'telehealth-portal', eligible };
}
