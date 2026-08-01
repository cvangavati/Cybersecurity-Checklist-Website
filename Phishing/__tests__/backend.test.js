const request = require('supertest');
const { createServer } = require('../server');

describe('phishing awareness API', () => {
  test('returns a message when a trigger matches content', async () => {
    const app = createServer();
    const response = await request(app).get('/api/awareness/next?userId=u1&trigger=login_success');

    expect(response.status).toBe(200);
    expect(response.body.message).toBeDefined();
    expect(response.body.message.id).toBeDefined();
  });

  test('records a report and lists it', async () => {
    const app = createServer();
    const reportResponse = await request(app).post('/api/awareness/report').send({
      userId: 'u1',
      channel: 'email',
      note: 'suspicious message',
    });

    expect(reportResponse.status).toBe(202);
    expect(reportResponse.body.reportId).toBeDefined();

    const listResponse = await request(app).get('/api/awareness/reports');
    expect(listResponse.status).toBe(200);
    expect(listResponse.body.reports.length).toBeGreaterThan(0);
  });
});