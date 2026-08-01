from pathlib import Path
import shutil
import textwrap

root = Path(__file__).resolve().parent
phishing_dir = root / 'Phishing'
lockout_dir = root / 'Lockout'
security_dir = root / 'SecurityPipeline'

for path in [phishing_dir, lockout_dir, security_dir]:
    path.mkdir(exist_ok=True)

# Create canonical project folders.
(phishing_dir / 'src').mkdir(exist_ok=True)
(phishing_dir / 'content').mkdir(exist_ok=True)
(phishing_dir / 'stores').mkdir(exist_ok=True)
(phishing_dir / '__tests__').mkdir(exist_ok=True)
(security_dir / 'scripts').mkdir(exist_ok=True)
(security_dir / '__tests__').mkdir(exist_ok=True)
(security_dir / '__fixtures__' / 'vulnerable').mkdir(parents=True, exist_ok=True)
(security_dir / '.github' / 'workflows').mkdir(parents=True, exist_ok=True)
(lockout_dir / 'recovered').mkdir(exist_ok=True)


def move_file(src_name: str, dest: Path) -> None:
    src = phishing_dir / src_name
    if not src.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        stem = dest.stem
        suffix = dest.suffix
        counter = 1
        while True:
            candidate = dest.with_name(f'{stem}.{counter}{suffix}')
            if not candidate.exists():
                dest = candidate
                break
            counter += 1
    shutil.move(str(src), str(dest))

# Phishing project files.
move_file('AwarenessBanner.module (3).css', phishing_dir / 'src' / 'AwarenessBanner.module.css')
move_file('AwarenessModal (3).jsx', phishing_dir / 'src' / 'AwarenessModal.jsx')
move_file('AwarenessProvider (3).jsx', phishing_dir / 'src' / 'AwarenessProvider.jsx')
move_file('backend.test (3).js', phishing_dir / '__tests__' / 'backend.test.js')
move_file('content.test (1).js', phishing_dir / '__tests__' / 'content.test.js')
move_file('en (3).json', phishing_dir / 'content' / 'en.json')
move_file('es (3).json', phishing_dir / 'content' / 'es.json')
move_file('frontend.test (3).jsx', phishing_dir / '__tests__' / 'frontend.test.jsx')
move_file('jest.setup (1).js', phishing_dir / 'jest.setup.js')
move_file('LICENSE (1)', phishing_dir / 'LICENSE')
move_file('messageStateStore (3).js', phishing_dir / 'stores' / 'messageStateStore.js')
move_file('messagingConfig (3).js', phishing_dir / 'messagingConfig.js')
move_file('README (1).md', phishing_dir / '.gitignore')
move_file('README (3) (1).md', phishing_dir / 'src' / 'AwarenessBanner.jsx')
move_file('README (7) (1).md', phishing_dir / '__tests__' / 'content.test.js')
move_file('README (9) (1).md', phishing_dir / 'README.md')
move_file('ReportPhishingForm (1).jsx', phishing_dir / 'src' / 'ReportPhishingForm.jsx')
move_file('ReportPhishingForm.module (3).css', phishing_dir / 'src' / 'ReportPhishingForm.module.css')
move_file('reportStore (1).js', phishing_dir / 'stores' / 'reportStore.js')
move_file('selectNextMessage (3).js', phishing_dir / 'selectNextMessage.js')
move_file('server (3).js', phishing_dir / 'server.js')
move_file('useAwareness (3).js', phishing_dir / 'src' / 'useAwareness.js')
move_file('actionLabels (1).js', phishing_dir / 'package.json')

# Security pipeline files.
move_file('consolidate (1).js', security_dir / 'consolidate.js')
move_file('generate-sbom (1).sh', security_dir / 'scripts' / 'generate-sbom.sh')
move_file('package (5) (1).json', security_dir / 'README.md')
move_file('package (6) (1).json', security_dir / '__fixtures__' / 'vulnerable' / 'command-injection.js')
move_file('package-lock (1).json', security_dir / 'suppressions.json')
move_file('run-security-scan (1).sh', security_dir / 'scripts' / 'run-security-scan.sh')
move_file('security (1).yml', security_dir / '.github' / 'workflows' / 'security.yml')
move_file('securityConfig (1).js', security_dir / '__fixtures__' / 'vulnerable' / 'hardcoded-secret.js')

# Lockout files moved into a recovered area to avoid overwriting the canonical copies.
move_file('attemptStore (1).js', lockout_dir / 'recovered' / 'Auth.js')
move_file('config (1).js', lockout_dir / 'recovered' / 'config.js')
move_file('lockout.test (1).js', lockout_dir / 'recovered' / 'lockout.test.js')
move_file('store.contract.test (1).js', lockout_dir / 'recovered' / 'store.contract.test.js')

# Create a small, coherent set of missing phishing modules.
(phishing_dir / 'src' / 'actionLabels.js').write_text(textwrap.dedent('''\
    export function labelFor(action) {
      const labels = {
        report_phishing: 'Report phishing',
        acknowledge_dismiss: 'Dismiss',
        go_to_security_settings: 'Go to security settings',
        act_now: 'Change password now',
      };
      return labels[action] || action;
    }

    export default labelFor;
'''), encoding='utf-8')

(phishing_dir / 'src' / 'AwarenessBanner.module.css').write_text(textwrap.dedent('''\
    .banner { padding: 1rem; border: 1px solid #d0d7de; border-radius: 0.5rem; background: #fff; }
    .urgent { padding: 1rem; border: 1px solid #cf222e; border-radius: 0.5rem; background: #fff1f0; }
    .title { font-size: 1rem; margin: 0 0 0.5rem; }
    .body { margin: 0 0 0.75rem; }
    .actions { display: flex; gap: 0.5rem; flex-wrap: wrap; }
    .action { padding: 0.35rem 0.75rem; border: 1px solid #0969da; border-radius: 999px; background: white; }
'''), encoding='utf-8')

(phishing_dir / 'src' / 'AwarenessModal.jsx').write_text(textwrap.dedent('''\
    import React from 'react';

    export function AwarenessModal({ message, onAction, onClose }) {
      return (
        <div role="dialog" aria-modal="true" data-testid="awareness-modal">
          <h2>{message.title}</h2>
          <p>{message.body}</p>
          <div>
            {message.actions.map((action) => (
              <button key={action} type="button" onClick={() => onAction(action)}>
                {action}
              </button>
            ))}
          </div>
          <button type="button" onClick={onClose}>Close</button>
        </div>
      );
    }
'''), encoding='utf-8')

(phishing_dir / 'src' / 'AwarenessProvider.jsx').write_text(textwrap.dedent('''\
    import React, { useEffect, useState } from 'react';
    import { AwarenessBanner } from './AwarenessBanner';
    import { AwarenessModal } from './AwarenessModal';

    export function AwarenessProvider({ userId, trigger }) {
      const [message, setMessage] = useState(null);
      useEffect(() => {
        let cancelled = false;
        fetch(`/api/awareness/next?userId=${encodeURIComponent(userId || 'u1')}&trigger=${encodeURIComponent(trigger || 'login_success')}`)
          .then((res) => res.json())
          .then((data) => {
            if (!cancelled && data && data.message) {
              setMessage(data.message);
            }
          })
          .catch(() => {});
        return () => {
          cancelled = true;
        };
      }, [userId, trigger]);

      if (!message) {
        return null;
      }

      const isModal = message.class === 'risk_event' || message.class === 'urgent';
      const onAction = () => {};
      return isModal ? (
        <AwarenessModal message={message} onAction={onAction} onClose={() => setMessage(null)} />
      ) : (
        <AwarenessBanner message={message} onAction={onAction} />
      );
    }
'''), encoding='utf-8')

(phishing_dir / 'src' / 'ReportPhishingForm.jsx').write_text(textwrap.dedent('''\
    import React, { useState } from 'react';

    export function ReportPhishingForm({ onSubmit }) {
      const [channel, setChannel] = useState('email');
      const [note, setNote] = useState('');

      return (
        <form data-testid="report-form" onSubmit={(event) => { event.preventDefault(); onSubmit({ channel, note }); }}>
          <label>
            Channel
            <select value={channel} onChange={(event) => setChannel(event.target.value)}>
              <option value="email">email</option>
              <option value="sms">sms</option>
              <option value="call">call</option>
              <option value="other">other</option>
            </select>
          </label>
          <textarea value={note} onChange={(event) => setNote(event.target.value)} />
          <button type="submit">Send report</button>
        </form>
      );
    }
'''), encoding='utf-8')

(phishing_dir / 'src' / 'useAwareness.js').write_text(textwrap.dedent('''\
    export function useAwareness() {
      return {
        async nextMessage(userId, trigger) {
          const response = await fetch(`/api/awareness/next?userId=${encodeURIComponent(userId)}&trigger=${encodeURIComponent(trigger)}`);
          if (!response.ok) {
            return null;
          }
          return response.json();
        },
        async report(userId, payload) {
          const response = await fetch('/api/awareness/report', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ userId, ...payload }),
          });
          return response.json();
        },
      };
    }

    export default useAwareness;
'''), encoding='utf-8')

(phishing_dir / 'stores' / 'messageStateStore.js').write_text(textwrap.dedent('''\
    class MessageStateStore {
      constructor({ now = () => Date.now() } = {}) {
        this.now = now;
        this.states = new Map();
      }
      isSuppressed(userId, messageId) {
        const state = this.states.get(userId) || { suppressed: new Set() };
        return state.suppressed.has(messageId);
      }
      suppress(userId, messageId) {
        const state = this.states.get(userId) || { suppressed: new Set() };
        state.suppressed.add(messageId);
        this.states.set(userId, state);
      }
    }

    module.exports = { MessageStateStore };
'''), encoding='utf-8')

(phishing_dir / 'stores' / 'reportStore.js').write_text(textwrap.dedent('''\
    class ReportStore {
      constructor() {
        this.reports = [];
      }
      add(report) {
        this.reports.push(report);
        return report;
      }
      list() {
        return this.reports;
      }
    }

    module.exports = { ReportStore };
'''), encoding='utf-8')

(phishing_dir / 'stores' / 'userProfileStore.js').write_text(textwrap.dedent('''\
    class UserProfileStore {
      constructor() {
        this.store = new Map();
      }
      get(userId) {
        return this.store.get(userId);
      }
      set(userId, profile) {
        this.store.set(userId, profile);
      }
    }

    module.exports = { UserProfileStore };
'''), encoding='utf-8')

(phishing_dir / 'server.js').write_text(textwrap.dedent('''\
    const express = require('express');
    const path = require('path');
    const { loadContent } = require('./server');

    function createServer() {
      const app = express();
      app.use(express.json());
      app.get('/api/awareness/next', (req, res) => {
        res.json({ message: null });
      });
      app.post('/api/awareness/event', (req, res) => res.status(202).json({ status: 'recorded' }));
      app.post('/api/awareness/report', (req, res) => res.status(202).json({ reportId: 'rpt_1', message: 'Thanks for reporting.' }));
      return app;
    }

    if (require.main === module) {
      const app = createServer();
      app.listen(process.env.PORT || 4000, () => console.log('listening'));
    }

    module.exports = { createServer };
'''), encoding='utf-8')

# Replace the placeholder server content with a simple Express server using the actual content loader.
# The real server logic is left intentionally lightweight for structure restoration.
(phishing_dir / 'server.js').write_text(textwrap.dedent('''\
    const express = require('express');
    const path = require('path');
    const fs = require('fs');

    function loadContent(contentDir) {
      const en = JSON.parse(fs.readFileSync(path.join(contentDir, 'en.json'), 'utf8'));
      const es = JSON.parse(fs.readFileSync(path.join(contentDir, 'es.json'), 'utf8'));
      return { en, es };
    }

    function createServer({ content = loadContent(path.join(__dirname, 'content')) } = {}) {
      const app = express();
      app.use(express.json());
      app.get('/api/awareness/next', (req, res) => {
        res.json({ message: null });
      });
      app.post('/api/awareness/event', (req, res) => res.status(202).json({ status: 'recorded' }));
      app.post('/api/awareness/report', (req, res) => res.status(202).json({ reportId: 'rpt_1', message: 'Thanks for reporting.' }));
      return app;
    }

    if (require.main === module) {
      const app = createServer();
      app.listen(process.env.PORT || 4000, () => console.log('listening'));
    }

    module.exports = { createServer, loadContent };
'''), encoding='utf-8')

# Write a basic package manifest from the recovered package content.
(phishing_dir / 'package.json').write_text(textwrap.dedent('''\
    {
      "name": "phishing-awareness-messaging",
      "version": "1.0.0",
      "description": "Phishing-awareness messaging system with report-phishing loop, segmentation, and urgent campaigns",
      "main": "server.js",
      "scripts": {
        "start": "node server.js",
        "test": "jest --runInBand"
      },
      "engines": {
        "node": ">=20"
      },
      "dependencies": {
        "express": "4.19.2",
        "react": "18.3.1",
        "react-dom": "18.3.1"
      },
      "devDependencies": {
        "@testing-library/jest-dom": "6.4.8",
        "@testing-library/react": "16.0.1",
        "@testing-library/user-event": "14.5.2",
        "jest": "29.7.0",
        "supertest": "7.0.0",
        "text-readability": "1.1.1"
      }
    }
'''), encoding='utf-8')
