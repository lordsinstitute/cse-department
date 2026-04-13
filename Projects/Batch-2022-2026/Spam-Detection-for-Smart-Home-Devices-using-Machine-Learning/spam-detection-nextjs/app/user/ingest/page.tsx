'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import ProtectedRoute from '@/components/ProtectedRoute';
import LoadingSpinner from '@/components/LoadingSpinner';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { useToast } from '@/context/ToastContext';
import api from '@/lib/api';
import type { ApiResponse, BatchPredictionResult } from '@/types/api';

type IngestMode = 'json-single' | 'json-batch' | 'csv';

const PARAM_LABELS = [
  'PCA-1: Source ID / Address',
  'PCA-2: Source Type / Location',
  'PCA-3: Destination Service Address',
  'PCA-4: Destination Service Type',
  'PCA-5: Destination Location',
  'PCA-6: Accessed Node Address',
  'PCA-7: Accessed Node Type',
  'PCA-8: Operation',
  'PCA-9: Value',
  'PCA-10: Combined Features',
];

export default function IngestPage() {
  const [mode, setMode] = useState<IngestMode>('csv');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<BatchPredictionResult | null>(null);

  // CSV state
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [downloadCsv, setDownloadCsv] = useState(false);

  // JSON single state
  const [singleParams, setSingleParams] = useState<string[]>(Array(10).fill(''));

  // JSON batch state
  const [batchJson, setBatchJson] = useState('');

  const { addToast } = useToast();

  // ── CSV ingestion ──────────────────────────────────────────────────────────
  const handleCsvSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!csvFile) return addToast('Please select a CSV file', 'error');

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', csvFile);

    if (downloadCsv) {
      try {
        const res = await api.post('/api/ingest/csv?format=csv', formData, {
          responseType: 'blob',
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        const url = URL.createObjectURL(res.data);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'predictions.csv';
        a.click();
        URL.revokeObjectURL(url);
        addToast('Predictions CSV downloaded', 'success');
      } catch {
        addToast('Failed to process CSV', 'error');
      } finally {
        setIsLoading(false);
      }
      return;
    }

    try {
      const res = await api.post<ApiResponse<BatchPredictionResult>>(
        '/api/ingest/csv',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setResults(res.data.data!);
      addToast(`Processed ${res.data.data!.total} records`, 'success');
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { message?: string } } }).response?.data?.message ||
        'Failed to process CSV';
      addToast(msg, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  // ── JSON single ────────────────────────────────────────────────────────────
  const handleSingleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const params = singleParams.map(Number);
    if (params.some(isNaN)) return addToast('All 10 parameters must be numeric', 'error');

    setIsLoading(true);
    try {
      const res = await api.post<ApiResponse<{ prediction: 0 | 1; label: string; prediction_id: number }>>(
        '/api/ingest',
        { parameters: params }
      );
      const { prediction, label } = res.data.data!;
      setResults({
        results: [{ index: 0, prediction, label: label as 'spam' | 'valid', prediction_id: res.data.data!.prediction_id }],
        total: 1,
        spam_count: prediction,
        valid_count: 1 - prediction,
      });
      addToast(`Result: ${label.toUpperCase()}`, prediction === 1 ? 'error' : 'success');
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { message?: string } } }).response?.data?.message ||
        'Prediction failed';
      addToast(msg, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  // ── JSON batch ─────────────────────────────────────────────────────────────
  const handleBatchSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    let records: number[][];
    try {
      records = JSON.parse(batchJson);
      if (!Array.isArray(records)) throw new Error('Must be an array');
    } catch {
      return addToast('Invalid JSON. Must be an array of arrays: [[f0..f9], ...]', 'error');
    }

    setIsLoading(true);
    try {
      const res = await api.post<ApiResponse<BatchPredictionResult>>('/api/ingest/batch', { records });
      setResults(res.data.data!);
      addToast(`Processed ${res.data.data!.total} records`, 'success');
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { message?: string } } }).response?.data?.message ||
        'Batch prediction failed';
      addToast(msg, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ErrorBoundary>
      <ProtectedRoute requiredRole="user">
        <div className="min-h-screen flex flex-col">
          <Header isUser={true} />
          <main className="flex-grow container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold mb-2">Data Ingestion API</h1>
              <p className="text-gray-500 mb-6">
                Submit IoT sensor records for bulk spam detection via JSON or CSV.
              </p>

              {/* Mode Tabs */}
              <div className="flex gap-2 mb-6 border-b">
                {([
                  { id: 'csv', label: 'CSV Upload' },
                  { id: 'json-single', label: 'Single JSON Record' },
                  { id: 'json-batch', label: 'Batch JSON' },
                ] as { id: IngestMode; label: string }[]).map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => { setMode(tab.id); setResults(null); }}
                    className={`px-5 py-2 font-medium rounded-t ${
                      mode === tab.id
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                {/* CSV Mode */}
                {mode === 'csv' && (
                  <form onSubmit={handleCsvSubmit}>
                    <h2 className="text-xl font-semibold mb-4">Upload CSV File</h2>
                    <p className="text-sm text-gray-500 mb-4">
                      CSV must contain 10 columns named <code className="bg-gray-100 px-1 rounded">p0–p9</code> or
                      the first 10 columns will be used as PCA components.
                      Maximum 5,000 rows.
                    </p>
                    <input
                      type="file"
                      accept=".csv"
                      onChange={(e) => setCsvFile(e.target.files?.[0] ?? null)}
                      className="block w-full text-sm border rounded p-2 mb-4"
                    />
                    <label className="flex items-center gap-2 text-sm mb-4">
                      <input
                        type="checkbox"
                        checked={downloadCsv}
                        onChange={(e) => setDownloadCsv(e.target.checked)}
                      />
                      Download results as CSV (with prediction column appended)
                    </label>
                    <button
                      type="submit"
                      disabled={!csvFile || isLoading}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-60"
                    >
                      {isLoading ? 'Processing...' : 'Run Predictions'}
                    </button>
                  </form>
                )}

                {/* Single JSON Mode */}
                {mode === 'json-single' && (
                  <form onSubmit={handleSingleSubmit}>
                    <h2 className="text-xl font-semibold mb-4">Single Record (JSON)</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                      {PARAM_LABELS.map((label, i) => (
                        <div key={i}>
                          <label className="block text-xs text-gray-600 mb-1">{label}</label>
                          <input
                            type="number"
                            step="any"
                            value={singleParams[i]}
                            onChange={(e) => {
                              const p = [...singleParams];
                              p[i] = e.target.value;
                              setSingleParams(p);
                            }}
                            className="w-full border rounded px-3 py-1.5 text-sm"
                            placeholder="e.g. -2.34"
                            required
                          />
                        </div>
                      ))}
                    </div>
                    <button
                      type="submit"
                      disabled={isLoading}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-60"
                    >
                      {isLoading ? 'Predicting...' : 'Predict'}
                    </button>
                  </form>
                )}

                {/* Batch JSON Mode */}
                {mode === 'json-batch' && (
                  <form onSubmit={handleBatchSubmit}>
                    <h2 className="text-xl font-semibold mb-4">Batch Records (JSON)</h2>
                    <p className="text-sm text-gray-500 mb-2">
                      Paste a JSON array of records. Each record must be an array of 10 numbers.
                      Maximum 1,000 records.
                    </p>
                    <pre className="text-xs bg-gray-50 p-2 rounded mb-3 text-gray-600">
                      {`[[-2.28, -0.60, -0.35, -0.18, 0.13, 0.08, -0.03, -0.03, -0.02, 0.004],\n [3.90, -0.54, -1.33, -0.60, -0.34, -0.28, -0.47, -0.03, 0.005, -0.03]]`}
                    </pre>
                    <textarea
                      value={batchJson}
                      onChange={(e) => setBatchJson(e.target.value)}
                      rows={8}
                      className="w-full border rounded px-3 py-2 text-sm font-mono mb-4"
                      placeholder='[[-2.28, -0.60, ...], [...]]'
                    />
                    <button
                      type="submit"
                      disabled={!batchJson.trim() || isLoading}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-60"
                    >
                      {isLoading ? 'Processing...' : 'Run Batch Prediction'}
                    </button>
                  </form>
                )}
              </div>

              {/* Results */}
              {isLoading && (
                <div className="flex justify-center py-8">
                  <LoadingSpinner label="Running predictions..." />
                </div>
              )}

              {results && !isLoading && (
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h2 className="text-xl font-semibold mb-4">Results</h2>
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="bg-blue-50 rounded-lg p-4 text-center">
                      <p className="text-3xl font-bold text-blue-700">{results.total}</p>
                      <p className="text-sm text-gray-600">Total Records</p>
                    </div>
                    <div className="bg-red-50 rounded-lg p-4 text-center">
                      <p className="text-3xl font-bold text-red-700">{results.spam_count}</p>
                      <p className="text-sm text-gray-600">Spam Detected</p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4 text-center">
                      <p className="text-3xl font-bold text-green-700">{results.valid_count}</p>
                      <p className="text-sm text-gray-600">Valid Behavior</p>
                    </div>
                  </div>

                  {results.results.length <= 100 && (
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm border-collapse">
                        <thead>
                          <tr className="bg-gray-50">
                            <th className="border px-3 py-2 text-left">Row</th>
                            <th className="border px-3 py-2 text-left">Prediction</th>
                            <th className="border px-3 py-2 text-left">Label</th>
                            <th className="border px-3 py-2 text-left">ID</th>
                          </tr>
                        </thead>
                        <tbody>
                          {results.results.map((r, i) => (
                            <tr key={i} className={r.prediction === 1 ? 'bg-red-50' : ''}>
                              <td className="border px-3 py-1">{r.row ?? r.index ?? i}</td>
                              <td className="border px-3 py-1">{r.prediction}</td>
                              <td className="border px-3 py-1">
                                <span
                                  className={`font-semibold ${
                                    r.prediction === 1 ? 'text-red-700' : 'text-green-700'
                                  }`}
                                >
                                  {r.label.toUpperCase()}
                                </span>
                              </td>
                              <td className="border px-3 py-1 text-gray-400">{r.prediction_id}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                  {results.results.length > 100 && (
                    <p className="text-gray-500 text-sm">
                      Showing summary only for large batches. Use the CSV download option to get
                      full results.
                    </p>
                  )}
                </div>
              )}
            </div>
          </main>
        </div>
      </ProtectedRoute>
    </ErrorBoundary>
  );
}
