import React from 'react';
import { labelFor } from './actionLabels';
import styles from './AwarenessBanner.module.css';

export function AwarenessBanner({ message, onAction }) {
  const isUrgent = message.class === 'urgent';

  return (
    <section
      role="status"
      aria-live="polite"
      data-testid="awareness-banner"
      data-message-id={message.id}
      data-message-class={message.class}
      className={isUrgent ? styles.urgent : styles.banner}
    >
      <h2 className={styles.title}>{message.title}</h2>
      <p className={styles.body}>{message.body}</p>
      <div className={styles.actions}>
        {message.actions.map((action) => (
          <button
            key={action}
            type="button"
            className={styles.action}
            data-action={action}
            onClick={() => onAction(action)}
          >
            {labelFor(action)}
          </button>
        ))}
      </div>
    </section>
  );
}
