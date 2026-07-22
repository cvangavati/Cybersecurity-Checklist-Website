// RFC 6238 TOTP implementation using only Node's built-in crypto module.
// No external dependencies. Good for learning how TOTP works under the hood.

const crypto = require('crypto');

function generateSecret(length = 20) {
  return crypto.randomBytes(length);
}

function base32Encode(buffer) {
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
  let bits = '';
  let output = '';
  for (const byte of buffer) bits += byte.toString(2).padStart(8, '0');
  for (let i = 0; i + 5 <= bits.length; i += 5) {
    output += alphabet[parseInt(bits.substr(i, 5), 2)];
  }
  return output;
}

function hotp(secret, counter) {
  const buffer = Buffer.alloc(8);
  buffer.writeBigUInt64BE(BigInt(counter));

  const hmac = crypto.createHmac('sha1', secret).update(buffer).digest();
  const offset = hmac[hmac.length - 1] & 0xf;
  const code =
    ((hmac[offset] & 0x7f) << 24) |
    ((hmac[offset + 1] & 0xff) << 16) |
    ((hmac[offset + 2] & 0xff) << 8) |
    (hmac[offset + 3] & 0xff);

  return (code % 1_000_000).toString().padStart(6, '0');
}

function totp(secret, step = 30) {
  const counter = Math.floor(Date.now() / 1000 / step);
  return hotp(secret, counter);
}

// window = how many steps before/after "now" to accept, to allow for clock drift
function verifyTotp(secret, token, window = 1, step = 30) {
  const counter = Math.floor(Date.now() / 1000 / step);
  for (let i = -window; i <= window; i++) {
    if (hotp(secret, counter + i) === token) return true;
  }
  return false;
}

module.exports = {
  generateSecret,
  base32Encode,
  hotp,
  totp,
  verifyTotp,
};
