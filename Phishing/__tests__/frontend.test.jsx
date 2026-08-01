/** @jest-environment jsdom */

import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AwarenessBanner } from '../src/AwarenessBanner';
import { ReportPhishingForm } from '../src/ReportPhishingForm';

describe('phishing awareness UI', () => {
  test('renders the banner and dispatches an action', async () => {
    const user = userEvent.setup();
    const onAction = jest.fn();
    render(
      <AwarenessBanner
        message={{ id: 'm1', class: 'standard', title: 'Test title', body: 'Test body', actions: ['report_phishing'] }}
        onAction={onAction}
      />
    );

    expect(screen.getByText('Test title')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Report phishing' }));
    expect(onAction).toHaveBeenCalledWith('report_phishing');
  });

  test('submits the report form payload', async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();
    render(<ReportPhishingForm onSubmit={onSubmit} />);

    await user.selectOptions(screen.getByLabelText(/Channel/i), 'sms');
    await user.type(screen.getByLabelText(/Details/i), 'Suspicious link');
    await user.click(screen.getByRole('button', { name: /send report/i }));

    expect(onSubmit).toHaveBeenCalledWith({ channel: 'sms', note: 'Suspicious link' });
  });
});