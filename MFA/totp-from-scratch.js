const { generateSecret, totp, verifyTotp } = require('../lib/totp-from-scratch');

const secret = generateSecret();
const code = totp(secret);

console.log('Secret (hex):', secret.toString('hex'));
console.log('Current code:', code);
console.log('Valid?', verifyTotp(secret, code));
console.log('Wrong code valid?', verifyTotp(secret, '000000'));
