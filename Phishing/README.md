# Phishing Awareness Messaging

This package contains a small demo of a phishing-awareness experience for a web app.
It exposes an Express API that serves training messages based on triggers and a React UI that renders the banner or modal content.

## What is included

- A server with endpoints for the next awareness message, report submission, and report listing.
- Locale content in English and Spanish.
- A deterministic message-selection helper.
- React components for the awareness banner, modal, and reporting form.

## Running locally

```bash
cd Phishing
npm install
npm test
npm start
```

The API listens on port 4000 by default.
