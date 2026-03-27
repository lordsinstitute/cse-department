'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';

type ExplainResult = {
  feature_values: Record<string, number>;
  feature_importance: Record<string, number>;
  top_contributors: { feature: string; value: number; importance: number; impact: number }[];
  prediction: { attack_type: string; severity: string; confidence: number; uncertainty: number; summary: string };
};

export default function ExplainPage() {
  const searchParams = useSearchParams();
  const alertId = searchParams.get('id');
  const [explain, setExplain] = useState<ExplainResult | null>(null);
  const [globalImp, setGlobalImp] = useState<Record<string, number> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (alertId) {
      setLoading(true);
      setError('');
      api<ExplainResult>(`/api/explain/alert/${alertId}`, { method: 'POST' })
        .then(setExplain)
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }
  }, [alertId]);

  useEffect(() => {
    api<Record<string, number>>('/api/explain/global')
      .then(setGlobalImp)
      .catch(() => setGlobalImp(null));
  }, []);

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-6">
      <h2 className="text-xl font-bold text-soc-green font-mono">EXPLAINABILITY</h2>

      {alertId && (
        <div className="border border-soc-border rounded-lg bg-soc-panel p-4">
          <h3 className="text-soc-blue mb-2">Alert #{alertId} — Explanation</h3>
          {loading && <p className="text-gray-400">Loading...</p>}
          {error && <p className="text-soc-red">{error}</p>}
          {explain && (
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-400">Prediction</p>
                <p className="font-mono">{explain.prediction.summary}</p>
                <p className="text-sm mt-1">
                  Attack: {explain.prediction.attack_type} · Severity: {explain.prediction.severity} ·
                  Confidence: {(explain.prediction.confidence * 100).toFixed(0)}% ·
                  Uncertainty: {(explain.prediction.uncertainty * 100).toFixed(0)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-400 mb-2">Top Contributing Features</p>
                <ul className="space-y-1">
                  {explain.top_contributors.slice(0, 10).map((c, i) => (
                    <li key={i} className="flex justify-between font-mono text-sm">
                      <span>{c.feature}</span>
                      <span>value={c.value.toFixed(2)} impact={c.impact.toFixed(4)}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      {globalImp && (
        <div className="border border-soc-border rounded-lg bg-soc-panel p-4">
          <h3 className="text-soc-blue mb-2">Global feature importance</h3>
          <div className="flex flex-wrap gap-2">
            {Object.entries(globalImp)
              .sort((a, b) => b[1] - a[1])
              .map(([name, val]) => (
                <span
                  key={name}
                  className="px-2 py-1 rounded bg-soc-bg border border-soc-border font-mono text-xs"
                  title={String(val)}
                >
                  {name}: {(val * 100).toFixed(1)}%
                </span>
              ))}
          </div>
        </div>
      )}

      {!alertId && (
        <p className="text-gray-400">Select an alert from the dashboard and click Explain.</p>
      )}
    </div>
  );
}
