import pathlib
import re

root = pathlib.Path(__file__).parent
for path in sorted(root.iterdir()):
    if not path.is_file() or path.name == 'classify_scrambled_files.py':
        continue
    content = path.read_text(encoding='utf-8', errors='replace')
    head = content[:1400]
    tags = []
    if re.search(r'"name"\s*:\s*"phishing-awareness-messaging"', head):
        tags.append('package.json (phishing-awareness)')
    if re.search(r'"name"\s*:\s*"security-pipeline"', head):
        tags.append('package.json (security-pipeline)')
    if re.search(r'"name"\s*:\s*"brute-force-login-protection"', head):
        tags.append('package.json (brute-force-login)')
    if re.search(r'"name"\s*:\s*"vulnerable-dependency-fixture"', head):
        tags.append('package.json (vulnerable-fixture)')
    if 'Core authentication + lockout logic' in head:
        tags.append('Lockout/Auth.js')
    if 'AttemptStore: storage abstraction' in head:
        tags.append('Lockout/attemptStore.js')
    if 'Central configuration for the brute-force protection service' in head:
        tags.append('Lockout/config.js')
    if 'Shared contract test suite for AttemptStore implementations' in head:
        tags.append('Lockout/store.contract.test.js')
    if 'Phishing-Awareness Messaging System' in head:
        tags.append('Phishing/README.md')
    if 'Brute-Force Login Protection' in head:
        tags.append('Lockout/README.md')
    if '# Detection fixtures (deliberately vulnerable)' in head:
        tags.append('security-pipeline/README.md')
    if '#!/usr/bin/env bash' in head:
        tags.append('shell script')
    if '"locale": "en"' in head:
        tags.append('content/en.json')
    if '"locale": "es"' in head:
        tags.append('content/es.json')
    if 'function selectNextMessage' in head or 'export function selectNextMessage' in head:
        tags.append('Phishing/selectNextMessage.js')
    if 'createServer' in head or 'loadContent' in head:
        tags.append('Phishing/server.js')
    if 'AwarenessProvider' in head and 'render(' in head:
        tags.append('Phishing/frontend test or component')
    if 'moduleNameMapper' in head and 'jest' in head:
        tags.append('Phishing/jest config/package.json')
    if 'node_modules/' in head and 'npm-debug.log' in head:
        tags.append('.gitignore')
    if 'Apache License' in head or 'Apache License' in content:
        tags.append('LICENSE')
    if 'function useAwareness' in head or 'export function useAwareness' in head:
        tags.append('Phishing/src/useAwareness.js')
    if 'AWAIT' in head or 'async' in head:
        pass
    print(path.name)
    print('  tags:', tags or ['unknown'])
    print('  first lines:')
    for i, line in enumerate(head.splitlines()[:10], 1):
        print(f'    {i}: {line}')
    print()
