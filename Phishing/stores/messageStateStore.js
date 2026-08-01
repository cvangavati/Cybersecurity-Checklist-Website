class MessageStateStore {
  constructor({ now = () => Date.now() } = {}) {
    this.now = now;
    this.states = new Map();
  }

  getState(userId) {
    if (!this.states.has(userId)) {
      this.states.set(userId, { history: [], events: [], suppressions: new Set() });
    }
    return this.states.get(userId);
  }

  getHistory(userId) {
    return this.getState(userId).history;
  }

  isSuppressed(userId, messageId) {
    return this.getState(userId).suppressions.has(messageId);
  }

  recordEvent(userId, messageId, action) {
    const state = this.getState(userId);
    state.events.push({ messageId, action, at: this.now() });
    if (action === 'dismissed') {
      const dismissCount = state.events.filter((event) => event.messageId === messageId && event.action === 'dismissed').length;
      if (dismissCount >= 2) {
        state.suppressions.add(messageId);
      }
    }
    if (action === 'shown') {
      state.history.push(messageId);
    }
  }

  recordRiskEvent(userId, type) {
    const state = this.getState(userId);
    state.riskEvents = state.riskEvents || [];
    state.riskEvents.push({ type, at: this.now() });
  }
}

module.exports = { MessageStateStore };
