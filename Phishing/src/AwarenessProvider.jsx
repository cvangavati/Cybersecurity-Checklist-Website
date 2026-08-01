import React, { useEffect, useState } from 'react';
import { AwarenessBanner } from './AwarenessBanner';
import { AwarenessModal } from './AwarenessModal';

export function AwarenessProvider({ userId, trigger }) {
  const [message, setMessage] = useState(null);

  useEffect(() => {
    let cancelled = false;

    fetch(
      `/api/awareness/next?userId=${encodeURIComponent(userId || 'u1')}&trigger=${encodeURIComponent(trigger || 'login_success')}`
    )
      .then((res) => {
        if (!res.ok) {
          return null;
        }
        return res.json();
      })
      .then((data) => {
        if (!cancelled && data && data.message) {
          setMessage(data.message);
        }
      })
      .catch(() => {});

    return () => {
      cancelled = true;
    };
  }, [userId, trigger]);

  if (!message) {
    return null;
  }

  const isModal = message.class === 'risk_event' || message.class === 'urgent';
  const onAction = () => {};

  return isModal ? (
    <AwarenessModal message={message} onAction={onAction} onClose={() => setMessage(null)} />
  ) : (
    <AwarenessBanner message={message} onAction={onAction} />
  );
}
