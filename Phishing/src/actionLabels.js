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
