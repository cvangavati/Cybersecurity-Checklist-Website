# MFA TOTP

A Node.js implementation of TOTP (Time-based One-Time Password) multi-factor
authentication — the same standard used by Google Authenticator, Authy, and
1Password.

## Structure

```
mfa-totp/
├── lib/
│   ├── totp.js               # Recommended: built on the otplib library
│   └── totp-from-scratch.js  # No dependencies — pure Node crypto, for learning
├── examples/
│   ├── basic-usage.js        # Full flow using lib/totp.js
│   └── from-scratch-usage.js # Full flow using the dependency-free version
├── package.json
└── README.md
```

## Setup

```bash
npm install
```

## Run the examples

```bash
npm run example          # otplib-based version
npm run example:scratch  # dependency-free version
```

## Typical MFA enrollment flow

1. **Enable MFA**: call `generateSecret()` and save it (encrypted) against the
   user's account.
2. **Show a QR code**: call `generateQrCode(email, appName, secret)` and
   render the returned data URL as an `<img>` so the user can scan it with
   their authenticator app.
3. **Confirm setup**: ask the user to enter the current code from their app
   and confirm it with `verifyToken()` before marking MFA as active.
4. **Login verification**: on every future login, after password check,
   prompt for the 6-digit code and verify with `verifyToken()`.

## Security notes

- Store secrets encrypted at rest, never in plain text.
- Rate-limit verification attempts (e.g. 5 tries per 5 minutes) to prevent
  brute-forcing the 6-digit code.
- Provide backup/recovery codes in case the user loses their device.
- The `window` parameter in the from-scratch version (and otplib's internal
  window) allows for small clock drift between server and client — don't set
  it too high or you weaken the security window.

## License

MIT
