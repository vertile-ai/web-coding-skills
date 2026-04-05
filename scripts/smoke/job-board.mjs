import assert from 'node:assert/strict';

export function run() {
  const applicants = [
    { id: 'u1', score: 82 },
    { id: 'u2', score: 91 },
    { id: 'u3', score: 77 },
  ];
  const ranked = [...applicants].sort((a, b) => b.score - a.score);
  assert.equal(ranked[0].id, 'u2');
  return { category: 'job-board', top: ranked[0].id };
}
