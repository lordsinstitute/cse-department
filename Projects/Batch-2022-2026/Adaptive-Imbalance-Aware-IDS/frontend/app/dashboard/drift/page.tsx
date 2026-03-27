'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

type DriftFeature = {
  feature_name: string;
  baseline_mean: number;
  baseline_std: number;
  current_mean: number;
  current_std: number;
  pvalue: number;
  drifted: boolean;
};

type DriftStatus = {
  drifted: boolean;
  pvalue_threshold: number;
  features: DriftFeature[];
  baseline_size: number;
  recent_size: number;
  message?: string;
};

export default function DriftPage() {
  const [status, setStatus] = useState<DriftStatus | null>(null);
  const [history, setHistory] = useState<Record<string, unknown>[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api<DriftStatus>('/api/drift'),
      api<Record<string, unknown>[]>('/api/drift/history?limit=50'),
    ])
      .then(([s, h]) => {
        setStatus(s);
        setHistory(h);
      })
      .catch(() => setStatus(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="p-4 text-gray-400">Loading...</p>;

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-6">
      <h2 className="text-xl font-bold text-soc-green font-mono">DRIFT MONITORING</h2>

      {status && (
        <>
          <div className="flex items-center gap-4">
            <span className={`px-3 py-1 rounded border ${status.drifted ? 'border-soc-red text-soc-red bg-soc-red/10' : 'border-soc-green text-soc-green bg-soc-green/10'}`}>
              {status.drifted ? 'Drift detected' : 'No drift'}
            </span>
            <span className="text-sm text-gray-400">
              Baseline: {status.baseline_size} · Recent: {status.recent_size} · p-value threshold: {status.pvalue_threshold}
            </span>
          </div>

          {status.message && <p className="text-gray-400">{status.message}</p>}

          <div className="border border-soc-border rounded-lg bg-soc-panel overflow-hidden">
            <h3 className="px-4 py-3 border-b border-soc-border text-soc-blue">Per-feature drift</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-soc-bg">
                  <tr>
                    <th className="text-left p-2 font-mono">Feature</th>
                    <th className="text-left p-2">Baseline mean</th>
                    <th className="text-left p-2">Current mean</th>
                    <th className="text-left p-2">p-value</th>
                    <th className="text-left p-2">Drifted</th>
                  </tr>
                </thead>
                <tbody>
                  {(status.features || []).map((f) => (
                    <tr key={f.feature_name} className="border-t border-soc-border">
                      <td className="p-2 font-mono">{f.feature_name}</td>
                      <td className="p-2 font-mono">{f.baseline_mean.toFixed(4)}</td>
                      <td className="p-2 font-mono">{f.current_mean.toFixed(4)}</td>
                      <td className="p-2 font-mono">{f.pvalue.toFixed(4)}</td>
                      <td className="p-2">
                        {f.drifted ? <span className="text-soc-red">Yes</span> : <span className="text-soc-green">No</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      <div className="border border-soc-border rounded-lg bg-soc-panel p-4">
        <h3 className="text-soc-blue mb-2">Drift History (snapshots)</h3>
        <pre className="text-xs font-mono text-gray-400 overflow-auto max-h-64">
          {JSON.stringify(history, null, 2)}
        </pre>
      </div>
    </div>
  );
}
