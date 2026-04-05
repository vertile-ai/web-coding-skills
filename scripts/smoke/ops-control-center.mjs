import assert from 'node:assert/strict';

export function run() {
  const alerts = [
    { id: 'a1', severity: 'critical' },
    { id: 'a2', severity: 'warning' },
  ];
  const route = alerts.map((a) => (a.severity === 'critical' ? 'on-call' : 'queue'));
  assert.deepEqual(route, ['on-call', 'queue']);
  return { category: 'ops-control-center', routed: route.length };
}
