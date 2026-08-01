const express = require('express');
const path = require('path');
const fs = require('fs');
const config = require('./messagingConfig');
const { selectNextMessage } = require('./selectNextMessage');
const { MessageStateStore } = require('./stores/messageStateStore');
const { ReportStore } = require('./stores/reportStore');
const { UserProfileStore } = require('./stores/userProfileStore');

function loadContent(contentDir) {
  const en = JSON.parse(fs.readFileSync(path.join(contentDir, 'en.json'), 'utf8'));
  const es = JSON.parse(fs.readFileSync(path.join(contentDir, 'es.json'), 'utf8'));
  return { en, es };
}

function createServer({
  content = loadContent(path.join(__dirname, 'content')),
  now = () => Date.now(),
  messageStateStore = new MessageStateStore({ now }),
  reportStore = new ReportStore({ now }),
  userProfileStore = new UserProfileStore(),
} = {}) {
  const app = express();
  app.use(express.json());

  app.get('/api/awareness/next', (req, res) => {
    const { userId = 'u1', trigger = 'login_success', locale = 'en' } = req.query;
    const localeData = content[locale] || content.en || { messages: [] };
    const profile = userProfileStore.get(userId) || {};
    const history = messageStateStore.getHistory(userId);
    const eligible = (localeData.messages || []).filter((message) =>
      message.triggerAffinity.includes(trigger)
    );
    const standardMessages = eligible.filter((message) => message.class === 'standard');
    const message = selectNextMessage(profile, history, standardMessages);

    if (!message) {
      return res.status(204).send();
    }

    return res.status(200).json({ message });
  });

  app.post('/api/awareness/event', (req, res) => {
    const { userId, messageId, action } = req.body || {};
    if (!userId || !messageId || !action) {
      return res.status(400).json({ error: 'invalid event' });
    }
    messageStateStore.recordEvent(userId, messageId, action);
    return res.status(202).json({ status: 'recorded' });
  });

  app.post('/api/awareness/report', (req, res) => {
    const { userId, channel, note } = req.body || {};
    if (!userId || !channel || !note) {
      return res.status(400).json({ error: 'invalid report' });
    }
    const report = reportStore.add({ userId, channel, note });
    return res.status(202).json({ reportId: report.id, message: 'Thanks for reporting.' });
  });

  app.post('/api/risk-event', (req, res) => {
    const { userId, type } = req.body || {};
    if (!userId || !type) {
      return res.status(400).json({ error: 'invalid risk event' });
    }
    messageStateStore.recordRiskEvent(userId, type);
    return res.status(202).json({ status: 'recorded' });
  });

  app.post('/api/awareness/campaign', (req, res) => {
    const { id, title, body, expiresAt } = req.body || {};
    if (!id || !title || !body || !expiresAt) {
      return res.status(400).json({ error: 'invalid campaign' });
    }
    return res.status(201).json({ id, title, body, expiresAt });
  });

  app.get('/api/awareness/reports', (_req, res) => {
    res.status(200).json({ reports: reportStore.list() });
  });

  return app;
}

if (require.main === module) {
  const app = createServer();
  app.listen(process.env.PORT || 4000, () => {
    console.log('listening');
  });
}

module.exports = { createServer, loadContent };
