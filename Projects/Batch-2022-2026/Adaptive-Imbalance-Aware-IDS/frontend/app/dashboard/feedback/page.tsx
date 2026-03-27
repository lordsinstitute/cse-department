'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';

type FeedbackEntry = {
  id: number;
  alert_id: number;
  analyst_id: number;
  correct_label: string;
  comment: string | null;
  created_at: string;
};

const LABELS = [
  'benign', 'dos', 'ddos', 'port_scan', 'brute_force', 'botnet', 'web_attack',
  'exploit', 'infiltration', 'data_exfiltration', 'malicious', 'unknown',
];

export default function FeedbackPage() {
  const searchParams = useSearchParams();
  const alertId = searchParams.get('alert_id');
  const [list, setList] = useState<FeedbackEntry[]>([]);
  const [correctLabel, setCorrectLabel] = useState('');
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    api<FeedbackEntry[]>(alertId ? `/api/feedback?alert_id=${alertId}` : '/api/feedback?limit=50')
      .then(setList)
      .catch(() => setList([]));
  }, [alertId]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!alertId || !correctLabel) return;
    setSubmitting(true);
    setMessage('');
    try {
      await api('/api/feedback', {
        method: 'POST',
        body: JSON.stringify({
          alert_id: parseInt(alertId, 10),
          correct_label: correctLabel,
          comment: comment || undefined,
        }),
      });
      setMessage('Feedback submitted.');
      setComment('');
      setCorrectLabel('');
      const updated = await api<FeedbackEntry[]>(`/api/feedback?alert_id=${alertId}`);
      setList(updated);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Failed');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-6">
      <h2 className="text-xl font-bold text-soc-green font-mono">ANALYST FEEDBACK</h2>

      {alertId && (
        <div className="border border-soc-border rounded-lg bg-soc-panel p-4">
          <h3 className="text-soc-blue mb-2">Submit feedback for Alert #{alertId}</h3>
          <form onSubmit={submit} className="space-y-3 max-w-md">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Correct label</label>
              <select
                value={correctLabel}
                onChange={(e) => setCorrectLabel(e.target.value)}
                className="w-full px-3 py-2 bg-soc-bg border border-soc-border rounded text-white"
                required
              >
                <option value="">Select...</option>
                {LABELS.map((l) => (
                  <option key={l} value={l}>{l}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Comment (optional)</label>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                className="w-full px-3 py-2 bg-soc-bg border border-soc-border rounded text-white"
                rows={2}
              />
            </div>
            <button
              type="submit"
              disabled={submitting}
              className="px-4 py-2 bg-soc-green/20 text-soc-green border border-soc-green rounded hover:bg-soc-green/30 disabled:opacity-50"
            >
              {submitting ? 'Submitting...' : 'Submit'}
            </button>
            {message && <p className="text-sm text-soc-green">{message}</p>}
          </form>
        </div>
      )}

      <div className="border border-soc-border rounded-lg bg-soc-panel overflow-hidden">
        <h3 className="px-4 py-3 border-b border-soc-border text-soc-blue">Recent feedback</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-soc-bg">
              <tr>
                <th className="text-left p-2 font-mono">ID</th>
                <th className="text-left p-2 font-mono">Alert ID</th>
                <th className="text-left p-2">Correct label</th>
                <th className="text-left p-2">Comment</th>
                <th className="text-left p-2 font-mono">Created</th>
              </tr>
            </thead>
            <tbody>
              {list.map((f) => (
                <tr key={f.id} className="border-t border-soc-border">
                  <td className="p-2 font-mono">{f.id}</td>
                  <td className="p-2 font-mono">
                    <a href={`/dashboard/feedback?alert_id=${f.alert_id}`} className="text-soc-blue hover:underline">
                      {f.alert_id}
                    </a>
                  </td>
                  <td className="p-2">{f.correct_label}</td>
                  <td className="p-2 text-gray-400">{f.comment || '—'}</td>
                  <td className="p-2 font-mono text-gray-400">
                    {new Date(f.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
