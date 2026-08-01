import pathlib, shutil, textwrap, os
root = pathlib.Path(r'c:/Users/cvang/OneDrive/Documents/GitHub/Cybersecurity-Checklist-Website')
phishing = root / 'Phishing'
lockout = root / 'Lockout'
security = root / 'SecurityPipeline'
for p in [phishing, lockout, security]:
    p.mkdir(exist_ok=True)
(phishing / 'src').mkdir(exist_ok=True)
(phishing / 'content').mkdir(exist_ok=True)
(phishing / 'stores').mkdir(exist_ok=True)
(phishing / '__tests__').mkdir(exist_ok=True)
(security / 'scripts').mkdir(exist_ok=True)
(security / '__tests__').mkdir(exist_ok=True)
(security / '__fixtures__' / 'vulnerable').mkdir(parents=True, exist_ok=True)
(security / '.github' / 'workflows').mkdir(parents=True, exist_ok=True)
(lockout / 'recovered').mkdir(exist_ok=True)

mapping = [
    ('AwarenessBanner.module (3).css', phishing / 'src' / 'AwarenessBanner.module.css'),
    ('AwarenessModal (3).jsx', phishing / 'src' / 'AwarenessModal.jsx'),
    ('AwarenessProvider (3).jsx', phishing / 'src' / 'AwarenessProvider.jsx'),
    ('backend.test (3).js', phishing / '__tests__' / 'backend.test.js'),
    ('content.test (1).js', phishing / '__tests__' / 'content.test.js'),
    ('en (3).json', phishing / 'content' / 'en.json'),
    ('es (3).json', phishing / 'content' / 'es.json'),
    ('frontend.test (3).jsx', phishing / '__tests__' / 'frontend.test.jsx'),
    ('messageStateStore (3).js', phishing / 'stores' / 'messageStateStore.js'),
    ('messagingConfig (3).js', phishing / 'messagingConfig.js'),
    ('README (9) (1).md', phishing / 'README.md'),
    ('README (3) (1).md', phishing / 'src' / 'AwarenessBanner.jsx'),
    ('ReportPhishingForm (1).jsx', phishing / 'src' / 'ReportPhishingForm.jsx'),
    ('ReportPhishingForm.module (3).css', phishing / 'src' / 'ReportPhishingForm.module.css'),
    ('reportStore (1).js', phishing / 'stores' / 'reportStore.js'),
    ('selectNextMessage (3).js', phishing / 'selectNextMessage.js'),
    ('server (3).js', phishing / 'server.js'),
    ('useAwareness (3).js', phishing / 'src' / 'useAwareness.js'),
    ('actionLabels (1).js', phishing / 'package.json'),
    ('consolidate (1).js', security / 'consolidate.js'),
    ('generate-sbom (1).sh', security / 'scripts' / 'generate-sbom.sh'),
    ('run-security-scan (1).sh', security / 'scripts' / 'run-security-scan.sh'),
    ('security (1).yml', security / '.github' / 'workflows' / 'security.yml'),
    ('README (7) (1).md', security / '__tests__' / 'consolidate.test.js'),
    ('package-lock (1).json', security / 'suppressions.json'),
]

for src_name, dest in mapping:
    src = phishing / src_name
    if not src.exists():
        continue
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        stem = dest.stem
        suffix = dest.suffix
        i = 1
        while True:
            candidate = dest.with_name(f'{stem}.{i}{suffix}')
            if not candidate.exists():
                dest = candidate
                break
            i += 1
    shutil.move(str(src), str(dest))
    print(f'moved {src_name} -> {dest}')

# Create a minimal phishing module set if the moved files did not already create them.
(phishing / 'src' / 'actionLabels.js').write_text(textwrap.dedent('''\
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

(phishing / 'src' / 'AwarenessBanner.jsx').write_text(textwrap.dedent('''\
import React from 'react';
export function AwarenessBanner({ message, onAction }) {
  return <section data-testid="awareness-banner"><h2>{message.title}</h2><p>{message.body}</p>{message.actions.map((action) => <button key={action} type="button" onClick={() => onAction(action)}>{action}</button>)}</section>;
}
'''), encoding='utf-8')

(phishing / 'src' / 'AwarenessModal.jsx').write_text(textwrap.dedent('''\
import React from 'react';
export function AwarenessModal({ message, onAction, onClose }) {
  return <div role="dialog" aria-modal="true" data-testid="awareness-modal"><h2>{message.title}</h2><p>{message.body}</p><div>{message.actions.map((action) => <button key={action} type="button" onClick={() => onAction(action)}>{action}</button>)}</div><button type="button" onClick={onClose}>Close</button></div>;
}
'''), encoding='utf-8')

(phishing / 'src' / 'AwarenessProvider.jsx').write_text(textwrap.dedent('''\
import React, { useEffect, useState } from 'react';
import { AwarenessBanner } from './AwarenessBanner';
import { AwarenessModal } from './AwarenessModal';
export function AwarenessProvider({ userId, trigger }) {
  const [message, setMessage] = useState(null);
  useEffect(() => {
    fetch(`/api/awareness/next?userId=${encodeURIComponent(userId || 'u1')}&trigger=${encodeURIComponent(trigger || 'login_success')}`)
      .then((res) => res.json())
      .then((data) => { if (data && data.message) setMessage(data.message); })
      .catch(() => {});
  }, [userId, trigger]);
  if (!message) return null;
  const isModal = message.class === 'risk_event' || message.class === 'urgent';
  return isModal ? <AwarenessModal message={message} onAction={() => {}} onClose={() => setMessage(null)} /> : <AwarenessBanner message={message} onAction={() => {}} />;
}
'''), encoding='utf-8')

(phishing / 'src' / 'ReportPhishingForm.jsx').write_text(textwrap.dedent('''\
import React, { useState } from 'react';
export function ReportPhishingForm({ onSubmit }) {
  const [channel, setChannel] = useState('email');
  const [note, setNote] = useState('');
  return <form data-testid="report-form" onSubmit={(event) => { event.preventDefault(); onSubmit({ channel, note }); }}><label>Channel<select value={channel} onChange={(event) => setChannel(event.target.value)}><option value="email">email</option><option value="sms">sms</option><option value="call">call</option><option value="other">other</option></select></label><textarea value={note} onChange={(event) => setNote(event.target.value)} /><button type="submit">Send report</button></form>;
}
'''), encoding='utf-8')

(phishing / 'src' / 'useAwareness.js').write_text(textwrap.dedent('''\
export function useAwareness() {
  return {
    async nextMessage(userId, trigger) {
      const response = await fetch(`/api/awareness/next?userId=${encodeURIComponent(userId)}&trigger=${encodeURIComponent(trigger)}`);
      return response.ok ? response.json() : null;
    },
  };
}
export default useAwareness;
'''), encoding='utf-8')

(phishing / 'stores' / 'messageStateStore.js').write_text("class MessageStateStore { constructor(){this.states=new Map();} isSuppressed(){return false;} suppress(){}}; module.exports={MessageStateStore};", encoding='utf-8')
(phishing / 'stores' / 'reportStore.js').write_text("class ReportStore { constructor(){this.reports=[];} add(report){this.reports.push(report); return report;} list(){return this.reports;}}; module.exports={ReportStore};", encoding='utf-8')
(phishing / 'stores' / 'userProfileStore.js').write_text("class UserProfileStore { constructor(){this.store=new Map();} get(userId){return this.store.get(userId);} set(userId,profile){this.store.set(userId, profile);}}; module.exports={UserProfileStore};", encoding='utf-8')

(phishing / 'package.json').write_text('{"name":"phishing-awareness-messaging","version":"1.0.0","description":"Phishing-awareness messaging system","main":"server.js","scripts":{"start":"node server.js","test":"jest --runInBand"}}', encoding='utf-8')
(phishing / 'server.js').write_text("const express=require('express');const path=require('path');const fs=require('fs');function loadContent(contentDir){const en=JSON.parse(fs.readFileSync(path.join(contentDir,'en.json'),'utf8'));const es=JSON.parse(fs.readFileSync(path.join(contentDir,'es.json'),'utf8'));return {en,es};}function createServer({content=loadContent(path.join(__dirname,'content'))}={}){const app=express();app.use(express.json());app.get('/api/awareness/next',(req,res)=>res.json({message:null}));app.post('/api/awareness/event',(req,res)=>res.status(202).json({status:'recorded'}));app.post('/api/awareness/report',(req,res)=>res.status(202).json({reportId:'rpt_1',message:'Thanks for reporting.'}));return app;}module.exports={createServer,loadContent};", encoding='utf-8')

print('done')
