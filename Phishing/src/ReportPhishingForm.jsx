import React, { useState } from 'react';
import styles from './ReportPhishingForm.module.css';

export function ReportPhishingForm({ onSubmit }) {
  const [channel, setChannel] = useState('email');
  const [note, setNote] = useState('');

  return (
    <form
      className={styles.form}
      data-testid="report-form"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit({ channel, note });
      }}
    >
      <label className={styles.label}>
        Channel
        <select className={styles.select} value={channel} onChange={(event) => setChannel(event.target.value)}>
          <option value="email">email</option>
          <option value="sms">sms</option>
          <option value="call">call</option>
          <option value="other">other</option>
        </select>
      </label>
      <label className={styles.label}>
        Details
        <textarea className={styles.textarea} value={note} onChange={(event) => setNote(event.target.value)} />
      </label>
      <button className={styles.button} type="submit">Send report</button>
    </form>
  );
}
