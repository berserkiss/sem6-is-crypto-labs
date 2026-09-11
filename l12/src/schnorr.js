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

// Генерация параметров p, q, g для Шнорра
async function generateKeys(bitsQ = 160, bitsP = 512) {
  let q, p, g, k, h;
  // 1. Сгенерировать q (простое)
  q = await generateLargePrime(bitsQ);
  // 2. Найти p = kq + 1, где p простое
  while (true) {
    k = bigInt.randBetween(bigInt(2).pow(bitsP - bitsQ - 1), bigInt(2).pow(bitsP - bitsQ));
    p = q.multiply(k).add(1);
    if (p.isProbablePrime(10)) break;
  }
  // 3. Найти g: g = h^{(p-1)/q} mod p, h случайное
  while (true) {
    h = bigInt.randBetween(2, p.minus(2));
    g = h.modPow(p.minus(1).divide(q), p);
    if (!g.equals(1)) break;
  }
  // 4. Секретный ключ x, открытый ключ y = g^{-x} mod p
  const x = bigInt.randBetween(1, q.minus(1));
  const y = g.modPow(q.minus(x), p);
  return { publicKey: { p, q, g, y }, privateKey: { p, q, g, x } };
}

// Старый тестовый вариант (оставлен для отладки)
function generateKeysTest() {
  const p = bigInt(23);
  const q = bigInt(11);
  const g = bigInt(2);
  const x = bigInt.randBetween(1, q.minus(1));
  const y = g.modPow(q.minus(x), p);
  return { publicKey: { p, q, g, y }, privateKey: { p, q, g, x } };
}

function signMessage(privateKey, message) {
  const { p, q, g, x } = Object.fromEntries(Object.entries(privateKey).map(([k, v]) => [k, bigInt(v)]));
  let k;
  do { k = bigInt.randBetween(1, q.minus(1)); } while (k.isZero());
  const a = g.modPow(k, p);
  const h = bigInt(crypto.createHash('sha256').update(Buffer.concat([Buffer.from(message), Buffer.from(a.toString())])).digest('hex'), 16).mod(q);
  const b = k.add(x.multiply(h)).mod(q);
  return { h: h.toString(), b: b.toString() };
}

function verifySignature(publicKey, message, signature) {
  const { p, q, g, y } = Object.fromEntries(Object.entries(publicKey).map(([k, v]) => [k, bigInt(v)]));
  const h = bigInt(signature.h), b = bigInt(signature.b);
  const X = g.modPow(b, p).multiply(y.modPow(h, p)).mod(p);
  const h2 = bigInt(crypto.createHash('sha256').update(Buffer.concat([Buffer.from(message), Buffer.from(X.toString())])).digest('hex'), 16).mod(q);
  return h2.equals(h);
}

module.exports = { generateKeys, signMessage, verifySignature, generateKeysTest }; 