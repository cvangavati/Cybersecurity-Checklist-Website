class ReportStore {
  constructor({ now = () => Date.now() } = {}) {
    this.now = now;
    this.reports = [];
  }

  add(report) {
    const entry = {
      id: `rpt_${this.now()}`,
      createdAt: this.now(),
      ...report,
    };
    this.reports.push(entry);
    return entry;
  }

  list() {
    return this.reports;
  }
}

module.exports = { ReportStore };
