'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import ProtectedRoute from '@/components/ProtectedRoute';
import LoadingSpinner from '@/components/LoadingSpinner';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { useToast } from '@/context/ToastContext';
import api from '@/lib/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { AlgorithmMetrics, ApiResponse } from '@/types/api';

const algorithmTabs = [
  { id: 'bagging', name: 'Bagging Classifier' },
  { id: 'gnb', name: 'Gaussian Naive Bayes' },
  { id: 'adaboost', name: 'AdaBoost Classifier' },
  { id: 'voting', name: 'Voting Classifier' },
  { id: 'dt', name: 'Decision Tree Classifier' },
  { id: 'compare', name: 'Compare All' },
];

const imageSrcMap: Record<string, string> = {
  bagging: '/pimg/bag.jpg',
  gnb: '/pimg/gnb.jpg',
  adaboost: '/pimg/ab.jpg',
  voting: '/pimg/vc.jpg',
  dt: '/pimg/dt.jpg',
};

export default function CompareAlgorithms() {
  const [algorithms, setAlgorithms] = useState<AlgorithmMetrics[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('bagging');
  const { addToast } = useToast();

  const fetchResults = async () => {
    setIsLoading(true);
    try {
      const res = await api.get<ApiResponse<{ algorithms: AlgorithmMetrics[] }>>(
        '/api/admin/compare-algorithms'
      );
      setAlgorithms(res.data.data!.algorithms);
      addToast('Algorithm comparison complete', 'success');
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { message?: string } } }).response?.data?.message ||
        'Failed to run algorithm comparison';
      addToast(msg, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const currentAlgo = algorithms.find(
    (a) => a.name.toLowerCase().replace(/ /g, '') === activeTab.replace(/-/g, '')
  ) ?? algorithms.find((_, i) => algorithmTabs[i]?.id === activeTab);

  return (
    <ErrorBoundary>
      <ProtectedRoute requiredRole="admin">
        <div className="min-h-screen flex flex-col">
          <Header isAdmin={true} />
          <main className="flex-grow container mx-auto px-4 py-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold">Compare ML Algorithms</h1>
                <button
                  onClick={fetchResults}
                  disabled={isLoading}
                  className="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-60"
                >
                  {isLoading ? 'Running...' : 'Run Comparison'}
                </button>
              </div>

              {isLoading ? (
                <div className="flex justify-center items-center h-64">
                  <LoadingSpinner size="lg" label="Training 5 models, this may take a while..." />
                </div>
              ) : algorithms.length === 0 ? (
                <div className="text-center py-16 text-gray-500">
                  <p className="text-lg mb-2">No results yet.</p>
                  <p className="text-sm">Click &quot;Run Comparison&quot; to train and compare all algorithms.</p>
                </div>
              ) : (
                <>
                  <ul className="flex flex-wrap border-b mb-6">
                    {algorithmTabs.map((tab) => (
                      <li key={tab.id} className="mr-1">
                        <button
                          onClick={() => setActiveTab(tab.id)}
                          className={`inline-block px-4 py-2 font-semibold ${
                            activeTab === tab.id
                              ? 'border-l border-t border-r rounded-t text-blue-700 bg-white'
                              : 'text-blue-500 hover:text-blue-800 bg-gray-50'
                          }`}
                        >
                          {tab.name}
                        </button>
                      </li>
                    ))}
                  </ul>

                  {activeTab === 'compare' ? (
                    <ResponsiveContainer width="100%" height={400}>
                      <BarChart data={algorithms}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis domain={[0, 100]} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="accuracy" fill="#8884d8" name="Accuracy %" />
                        <Bar dataKey="precision" fill="#82ca9d" name="Precision %" />
                        <Bar dataKey="recall" fill="#ffc658" name="Recall %" />
                        <Bar dataKey="fscore" fill="#ff8042" name="F1 Score %" />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <div>
                        {currentAlgo && (
                          <>
                            <h2 className="text-xl font-semibold mb-4">{currentAlgo.name} Metrics</h2>
                            {[
                              { label: 'Accuracy', value: currentAlgo.accuracy, color: 'blue' },
                              { label: 'Precision', value: currentAlgo.precision, color: 'green' },
                              { label: 'Recall', value: currentAlgo.recall, color: 'purple' },
                              { label: 'F1 Score', value: currentAlgo.fscore, color: 'orange' },
                            ].map(({ label, value, color }) => (
                              <div key={label} className="p-4 border rounded mb-3">
                                <p className="font-medium">
                                  {label}:{' '}
                                  <span className={`font-bold text-${color}-700`}>
                                    {value.toFixed(2)}%
                                  </span>
                                </p>
                              </div>
                            ))}
                          </>
                        )}
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg flex items-center justify-center">
                        {imageSrcMap[activeTab] && (
                          <img
                            src={`http://localhost:5020/static/pimg/${imageSrcMap[activeTab].split('/').pop()}`}
                            alt="Learning curve"
                            className="max-w-full h-auto max-h-96"
                          />
                        )}
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </main>
        </div>
      </ProtectedRoute>
    </ErrorBoundary>
  );
}
