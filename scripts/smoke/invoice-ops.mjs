import assert from 'node:assert/strict';

export function run() {
  const lines = [120, 80];
  const taxRate = 0.1;
  const subtotal = lines.reduce((a, b) => a + b, 0);
  const total = subtotal + subtotal * taxRate;
  assert.equal(total, 220);
  return { category: 'invoice-ops', total };
}
