export function useAwareness() {
  return {
    async nextMessage(userId, trigger) {
      const response = await fetch(
        `/api/awareness/next?userId=${encodeURIComponent(userId)}&trigger=${encodeURIComponent(trigger)}`
      );
      return response.ok ? response.json() : null;
    },
    async report(userId, payload) {
      const response = await fetch('/api/awareness/report', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ userId, ...payload }),
      });
      return response.ok ? response.json() : null;
    },
  };
}

export default useAwareness;
