import assert from 'node:assert/strict';

export function run() {
  const jobs = [{ id: 'j1', zone: 'N' }, { id: 'j2', zone: 'S' }];
  const techs = { N: 'tech-a', S: 'tech-b' };
  const assigned = jobs.map((j) => ({ ...j, tech: techs[j.zone] }));
  assert.equal(assigned[0].tech, 'tech-a');
  assert.equal(assigned[1].tech, 'tech-b');
  return { category: 'field-service', assigned: assigned.length };
}
