import React from 'react';
import { labelFor } from './actionLabels';

export function AwarenessModal({ message, onAction, onClose }) {
  return (
    <div role="dialog" aria-modal="true" data-testid="awareness-modal">
      <h2>{message.title}</h2>
      <p>{message.body}</p>
      <div>
        {message.actions.map((action) => (
          <button key={action} type="button" onClick={() => onAction(action)}>
            {labelFor(action)}
          </button>
        ))}
      </div>
      <button type="button" onClick={onClose}>Close</button>
    </div>
  );
}
