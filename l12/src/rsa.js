const forge = require('node-forge');

function generateKeys() {
  const keypair = forge.pki.rsa.generateKeyPair({ bits: 2048, e: 0x10001 });
  return {
    publicKey: forge.pki.publicKeyToPem(keypair.publicKey),
    privateKey: forge.pki.privateKeyToPem(keypair.privateKey)
  };
}

function signMessage(privateKeyPem, message) {
  const privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
  const md = forge.md.sha256.create();
  md.update(message, 'utf8');
  const signature = privateKey.sign(md);
  return forge.util.encode64(signature);
}

function verifySignature(publicKeyPem, message, signatureB64) {
  const publicKey = forge.pki.publicKeyFromPem(publicKeyPem);
  const md = forge.md.sha256.create();
  md.update(message, 'utf8');
  const signature = forge.util.decode64(signatureB64);
  return publicKey.verify(md.digest().bytes(), signature);
}

module.exports = { generateKeys, signMessage, verifySignature }; 