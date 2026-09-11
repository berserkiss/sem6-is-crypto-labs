const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const rsa = require('./rsa');
const elgamal = require('./elgamal');
const schnorr = require('./schnorr');
const { measureTime, measureTimeAsync } = require('./utils');

const app = express();
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '../public')));

app.post('/api/:algo/generate', async (req, res) => {
  let keys, ms;
  if (req.params.algo === 'rsa') {
    ({ result: keys, ms } = measureTime(rsa.generateKeys));
  } else if (req.params.algo === 'elgamal') {
    ({ result: keys, ms } = await measureTimeAsync(elgamal.generateKeys));
  } else if (req.params.algo === 'schnorr') {
    ({ result: keys, ms } = await measureTimeAsync(schnorr.generateKeys));
  } else {
    return res.status(400).json({ error: 'Unknown algorithm' });
  }
  res.json({ keys, ms });
});

app.post('/api/:algo/sign', (req, res) => {
  const { privateKey, message } = req.body;
  let signature, ms;
  if (req.params.algo === 'rsa') {
    ({ result: signature, ms } = measureTime(rsa.signMessage, privateKey, message));
  } else if (req.params.algo === 'elgamal') {
    ({ result: signature, ms } = measureTime(elgamal.signMessage, privateKey, message));
  } else if (req.params.algo === 'schnorr') {
    ({ result: signature, ms } = measureTime(schnorr.signMessage, privateKey, message));
  } else {
    return res.status(400).json({ error: 'Unknown algorithm' });
  }
  res.json({ signature, ms });
});

app.post('/api/:algo/verify', (req, res) => {
  const { publicKey, message, signature } = req.body;
  let valid, ms;
  if (req.params.algo === 'rsa') {
    ({ result: valid, ms } = measureTime(rsa.verifySignature, publicKey, message, signature));
  } else if (req.params.algo === 'elgamal') {
    ({ result: valid, ms } = measureTime(elgamal.verifySignature, publicKey, message, signature));
  } else if (req.params.algo === 'schnorr') {
    ({ result: valid, ms } = measureTime(schnorr.verifySignature, publicKey, message, signature));
  } else {
    return res.status(400).json({ error: 'Unknown algorithm' });
  }
  res.json({ valid, ms });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
}); 