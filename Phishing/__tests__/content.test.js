const path = require('path');
const fs = require('fs');

function loadContent(contentDir) {
  const en = JSON.parse(fs.readFileSync(path.join(contentDir, 'en.json'), 'utf8'));
  const es = JSON.parse(fs.readFileSync(path.join(contentDir, 'es.json'), 'utf8'));
  return { en, es };
}

describe('phishing content', () => {
  test('English and Spanish bundles both contain messages', () => {
    const content = loadContent(path.join(__dirname, '..', 'content'));
    expect(Array.isArray(content.en.messages)).toBe(true);
    expect(Array.isArray(content.es.messages)).toBe(true);
    expect(content.en.messages.length).toBeGreaterThan(0);
    expect(content.es.messages.length).toBeGreaterThan(0);
  });

  test('the English content contains the password warning message', () => {
    const content = loadContent(path.join(__dirname, '..', 'content'));
    const message = content.en.messages.find((entry) => entry.id === 'm4');
    expect(message).toBeDefined();
    expect(message.body).toContain('password');
  });
});