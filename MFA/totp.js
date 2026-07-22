const { authenticator } = require('otplib');
const qrcode = require('qrcode');

/**
 * Generate a new base32 secret for a user.
 */
function generateSecret() {
  return authenticator.generateSecret();
}

/**
 * Build an otpauth:// URI and QR code data URL for the user to scan
 * with Google Authenticator, Authy, 1Password, etc.
 *
 * @param {string} accountName - usually the user's email
 * @param {string} issuer - your app's name
 * @param {string} secret - the user's base32 secret
 */
async function generateQrCode(accountName, issuer, secret) {
  const otpauth = authenticator.keyuri(accountName, issuer, secret);
  const qrDataUrl = await qrcode.toDataURL(otpauth);
  return { otpauth, qrDataUrl };
}

/**
 * Verify a 6-digit code the user typed in.
 */
function verifyToken(token, secret) {
  try {
    return authenticator.verify({ token, secret });
  } catch (err) {
    return false;
  }
}

/**
 * Get the current valid code (useful for testing/debugging only —
 * never expose this in a real app).
 */
function getCurrentToken(secret) {
  return authenticator.generate(secret);
}

module.exports = {
  generateSecret,
  generateQrCode,
  verifyToken,
  getCurrentToken,
};
