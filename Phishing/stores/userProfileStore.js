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
