const crypto = require('crypto');

function measureTime(fn, ...args) {
  const start = process.hrtime.bigint();
  const result = fn(...args);
  const end = process.hrtime.bigint();
  const ms = Number(end - start) / 1e6;
  return { result, ms };
}

async function measureTimeAsync(fn, ...args) {
  const start = process.hrtime.bigint();
  const result = await fn(...args);
  const end = process.hrtime.bigint();
  const ms = Number(end - start) / 1e6;
  return { result, ms };
}

function hashMessage(message) {
  return crypto.createHash('sha256').update(message).digest('hex');
}

module.exports = { measureTime, measureTimeAsync, hashMessage }; 