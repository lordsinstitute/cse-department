'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

type Run = {
  id: number;
  created_at: string;
  datasets: string[];
  model_type: string;
  status: string;
  metrics: Record<string, unknown>;
  artifact_path: string;
};

type DatasetsInfo = Record<string, { configured: boolean; path: string }>;

export default function TrainingPage() {
  const [runs, setRuns] = useState<Run[]>([]);
  const [datasets, setDatasets] = useState<DatasetsInfo>({});
  const [selected, setSelected] = useState<string[]>([]);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    api<Run[]>('/api/training/runs').then(setRuns).catch(() => setRuns([]));
    api<DatasetsInfo>('/api/training/datasets').then(setDatasets).catch(() => setDatasets({}));
  }, []);

  async function startTraining() {
    if (selected.length === 0) return;
    setStarting(true);
    try {
      await api('/api/training/run', {
        method: 'POST',
        body: JSON.stringify({
          datasets: selected,
          max_rows_per_dataset: 50000,
          class_weight: 'balanced',
          C: 1.0,
        }),
      });
      const updated = await api<Run[]>('/api/training/runs');
      setRuns(updated);
      setSelected([]);
    } catch (e) {
      console.error(e);
    } finally {
      setStarting(false);
    }
  }

  function toggle(name: string) {
    setSelected((s) => (s.includes(name) ? s.filter((x) => x !== name) : [...s, name]));
  }

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-6">
      <h2 className="text-xl font-bold text-soc-green font-mono">DATASET & TRAINING</h2>

      <div className="border border-soc-border rounded-lg bg-soc-panel p-4">
        <h3 className="text-soc-blue mb-2">Start Training (SVM, class-weighted, F1 / minority recall)</h3>
        <p className="text-sm text-gray-400 mb-3">Select datasets: NSL-KDD, UNSW-NB15, CIC-IDS2017/2018, BoT-IoT</p>
        <div className="flex flex-wrap gap-2 mb-3">
          {Object.entries(datasets).map(([name, info]) => (
            <label key={name} className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={selected.includes(name)}
                onChange={() => toggle(name)}
                disabled={!info.configured}
                className="rounded border-soc-border"
              />
              <span className={info.configured ? 'text-white' : 'text-gray-500'}>{name}</span>
              {!info.configured && <span className="text-xs text-gray-500">(not configured)</span>}
            </label>
          ))}
        </div>
        <button
          onClick={startTraining}
          disabled={selected.length === 0 || starting}
          className="px-4 py-2 bg-soc-green/20 text-soc-green border border-soc-green rounded hover:bg-soc-green/30 disabled:opacity-50"
        >
          {starting ? 'Starting...' : 'Start training'}
        </button>
      </div>

      <div className="border border-soc-border rounded-lg bg-soc-panel overflow-hidden">
        <h3 className="px-4 py-3 border-b border-soc-border text-soc-blue">Training Runs</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-soc-bg">
              <tr>
                <th className="text-left p-2 font-mono">ID</th>
                <th className="text-left p-2">Created</th>
                <th className="text-left p-2">Datasets</th>
                <th className="text-left p-2">Status</th>
                <th className="text-left p-2">Metrics</th>
                <th className="text-left p-2">Artifact</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((r) => (
                <tr key={r.id} className="border-t border-soc-border">
                  <td className="p-2 font-mono">{r.id}</td>
                  <td className="p-2 font-mono text-gray-400">
                    {r.created_at ? new Date(r.created_at).toLocaleString() : '—'}
                  </td>
                  <td className="p-2">{r.datasets?.join(', ') || '—'}</td>
                  <td className="p-2">
                    <span className={r.status === 'completed' ? 'text-soc-green' : r.status === 'failed' ? 'text-soc-red' : 'text-soc-amber'}>
                      {r.status}
                    </span>
                  </td>
                  <td className="p-2 font-mono text-xs">
                    {r.metrics && (
                      <span>
                        F1: {(r.metrics.test_f1_weighted as number)?.toFixed(3)} · minority recall: {(r.metrics.test_minority_recall as number)?.toFixed(3)}
                      </span>
                    )}
                  </td>
                  <td className="p-2 font-mono text-gray-400 text-xs">{r.artifact_path || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
