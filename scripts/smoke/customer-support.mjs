import assert from 'node:assert/strict';

export function run() {
  const tickets = [
    { id: 't1', openedMins: 30, slaMins: 60 },
    { id: 't2', openedMins: 75, slaMins: 60 },
  ];
  const breached = tickets.filter((t) => t.openedMins > t.slaMins).map((t) => t.id);
  assert.deepEqual(breached, ['t2']);
  return { category: 'customer-support', breached };
}
