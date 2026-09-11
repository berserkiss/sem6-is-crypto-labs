const bigInt = require('big-integer');
const crypto = require('crypto');
const forge = require('node-forge');

// Генерация большого простого числа с помощью node-forge
function generateLargePrime(bits) {
  return new Promise((resolve, reject) => {
    forge.prime.generateProbablePrime(bits, (err, num) => {
      if (err) reject(err);
      else resolve(bigInt(num.toString()));
    });
  });
}

// Генерация параметров p, g для Эль-Гамаля
async function generateKeys(bitsP = 512) {
  const p = await generateLargePrime(bitsP);
  // g = 2 обычно подходит, если p — безопасное простое, иначе ищем g > 1
  let g = bigInt(2);
  if (g.modPow(bigInt(2), p).equals(1)) {
    // g=2 не годится, ищем другой g
    for (let candidate = 3; candidate < 100; candidate++) {
      g = bigInt(candidate);
      if (!g.modPow(bigInt(2), p).equals(1)) break;
    }
  }
  const x = bigInt.randBetween(1, p.minus(2));
  const y = g.modPow(x, p);
  return { publicKey: { p, g, y }, privateKey: { p, g, x } };
}

// Старый тестовый вариант (оставлен для отладки)
function generateKeysTest() {
  const p = bigInt(467);
  const g = bigInt(2);
  const x = bigInt.randBetween(1, p.minus(2));
  const y = g.modPow(x, p);
  return { publicKey: { p, g, y }, privateKey: { p, g, x } };
}

function signMessage(privateKey, message) {
  const { p, g, x } = Object.fromEntries(Object.entries(privateKey).map(([k, v]) => [k, bigInt(v)]));
  const h = bigInt(crypto.createHash('sha256').update(message).digest('hex'), 16).mod(p.minus(1));
  let k;
  do { k = bigInt.randBetween(1, p.minus(2)); } while (bigInt.gcd(k, p.minus(1)).notEquals(1));
  const a = g.modPow(k, p);
  const kInv = k.modInv(p.minus(1));
  let b = kInv.multiply(h.subtract(x.multiply(a))).mod(p.minus(1));
  if (b.isNegative()) b = b.add(p.minus(1));
  return { a: a.toString(), b: b.toString() };
}

function verifySignature(publicKey, message, signature) {
  const { p, g, y } = Object.fromEntries(Object.entries(publicKey).map(([k, v]) => [k, bigInt(v)]));
  const a = bigInt(signature.a), b = bigInt(signature.b);
  if (a.lesserOrEquals(0) || a.greaterOrEquals(p)) return false;
  if (b.lesser(0) || b.greaterOrEquals(p.minus(1))) return false;
  const h = bigInt(crypto.createHash('sha256').update(message).digest('hex'), 16).mod(p.minus(1));
  const left = y.modPow(a, p).multiply(a.modPow(b, p)).mod(p);
  const right = g.modPow(h, p);
  return left.equals(right);
}

module.exports = { generateKeys, signMessage, verifySignature, generateKeysTest }; 