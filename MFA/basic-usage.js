const { generateSecret, generateQrCode, verifyToken, getCurrentToken } = require('../lib/totp');

async function main() {
  // 1. When a user enables MFA, generate and save a secret to their account
  const secret = generateSecret();
  console.log('Generated secret (store this encrypted in your DB):', secret);

  // 2. Show them a QR code to scan with their authenticator app
  const { otpauth, qrDataUrl } = await generateQrCode('user@example.com', 'MyApp', secret);
  console.log('otpauth URI:', otpauth);
  console.log('QR code data URL (render as <img src="...">):', qrDataUrl.slice(0, 60) + '...');

  // 3. Simulate the user entering the current code from their app
  const currentCode = getCurrentToken(secret); // in real life, this comes from the user's phone
  console.log('Current code (simulated user input):', currentCode);

  // 4. Verify it on login
  const isValid = verifyToken(currentCode, secret);
  console.log('Verification result:', isValid ? 'VALID ✅' : 'INVALID ❌');

  // 5. A wrong code should fail
  console.log('Wrong code check:', verifyToken('000000', secret) ? 'VALID ✅' : 'INVALID ❌');
}

main();
