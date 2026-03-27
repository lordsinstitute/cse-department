'use client';

import { useEffect, useState } from 'react';
import { api, wsUrl } from '@/lib/api';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';

type Alert = {
  id: number;
  created_at: string;
  src_ip: string;
  dst_ip: string;
  src_port: number;
  dst_port: number;
  protocol: string;
  attack_type: string;
  severity: string;
  score: number;
  confidence: number;
  uncertainty: number;
  summary: string;
  mitre_techniques: string[];
};

type Stats = {
  total_alerts: number;
  by_severity: Record<string, number>;
  by_attack_type: Record<string, number>;
  top_source_ips: { ip: string; count: number }[];
};

const SEVERITY_COLORS: Record<string, string> = {
  critical: '#da3633',
  high: '#e06e27',
  medium: '#d29922',
  low: '#58a6ff',
  info: '#8b949e',
};

// Better colors for attack types (pie chart)
const ATTACK_TYPE_COLORS = [
  '#e06e27', // Red - Critical attacks
  '#da3633', // Dark red - High severity
  '#d29922', // Amber - Medium severity
  '#58a6ff', // Blue - Low severity
  '#8b949e', // Gray - Info/benign
  '#3fb950', // Green - Normal traffic
  '#a5a5ff', // Light purple
  '#ff6b9d', // Pink
  '#00d4ff', // Cyan
  '#ffa500', // Orange
  '#9d4edd', // Purple
  '#06ffa5', // Mint green
];

// Map severity names to display names
const SEVERITY_DISPLAY_NAMES: Record<string, string> = {
  critical: 'Critical',
  high: 'High',
  medium: 'Medium',
  low: 'Low',
  info: 'Normal',
};

export default function DashboardPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const [alertsRes, statsRes] = await Promise.all([
          api<Alert[]>('/api/alerts?limit=100'),
          api<Stats>('/api/stats'),
        ]);
        setAlerts(alertsRes);
        setStats(statsRes);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  useEffect(() => {
    const ws = new WebSocket(wsUrl('/ws/alerts'));
    ws.onopen = () => setWsConnected(true);
    ws.onclose = () => setWsConnected(false);
    ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data);
        if (msg.type === 'alert' && msg.data) {
          setAlerts((prev) => [msg.data, ...prev].slice(0, 200));
          setStats((s) =>
            s
              ? {
                  ...s,
                  total_alerts: s.total_alerts + 1,
                  by_severity: {
                    ...s.by_severity,
                    [msg.data.severity]: (s.by_severity[msg.data.severity] || 0) + 1,
                  },
                  by_attack_type: {
                    ...s.by_attack_type,
                    [msg.data.attack_type]: (s.by_attack_type[msg.data.attack_type] || 0) + 1,
                  },
                }
              : s
          );
        }
      } catch (_) {}
    };
    return () => ws.close();
  }, []);

  const severityData = stats
    ? Object.entries(stats.by_severity || {}).map(([name, value]) => ({ 
      name: SEVERITY_DISPLAY_NAMES[name] || name,
       value 
      }))
    : [];
  const attackData = stats
    ? Object.entries(stats.by_attack_type || {}).map(([name, value]) => ({ name, value }))
    : [];

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-6">
      <div className="flex items-center gap-2">
        <span className={`h-2 w-2 rounded-full ${wsConnected ? 'bg-soc-green' : 'bg-soc-red'}`} />
        <span className="text-sm text-gray-400">
          {wsConnected ? 'Live' : 'Disconnected'} — Real-Time Alerts
        </span>
      </div>

      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="border border-soc-border rounded-lg bg-soc-panel p-4">
            <p className="text-sm text-gray-400">Total Alerts</p>
            <p className="text-2xl font-mono text-soc-green">{stats.total_alerts}</p>
          </div>
          <div className="border border-soc-border rounded-lg bg-soc-panel p-4 md:col-span-2">
            <p className="text-sm text-gray-400 mb-2">By Severity</p>
            <div className="h-32">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={severityData} layout="vertical" margin={{ left: 60 }}>
                  <XAxis type="number" stroke="#8b949e" />
                  <YAxis type="category" dataKey="name" stroke="#8b949e" width={50} />
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d' }}
                  labelStyle={{ color: '#e6edf3' }} itemStyle={{ color: '#e6edf3' }} />
                  <Bar dataKey="value" fill="#3fb950" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {attackData.length > 0 && (
        <div className="border border-soc-border rounded-lg bg-soc-panel p-4">
          <p className="text-sm text-gray-400 mb-2">By Attack Type</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={attackData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ name, value }) => `${name} ${value}`}
                >
                  {attackData.map((_, i) => (
                    <Cell key={i} fill={ATTACK_TYPE_COLORS[i % ATTACK_TYPE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d',borderRadius: '6px',
                    padding: '8px' }}
                    labelStyle={{ color: '#e6edf3', fontWeight: 'bold' }}
                  itemStyle={{ color: '#e6edf3' }}
                  cursor={{ fill: 'transparent' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      <div className="border border-soc-border rounded-lg bg-soc-panel overflow-hidden">
        <h2 className="px-4 py-3 border-b border-soc-border text-soc-green font-mono">Alert Stream</h2>
        {loading ? (
          <p className="p-4 text-gray-400">Loading...</p>
        ) : (
          <div className="overflow-x-auto max-h-[60vh] overflow-y-auto">
            <table className="w-full text-sm">
              <thead className="bg-soc-bg sticky top-0">
                <tr>
                  <th className="text-left p-2 font-mono">Time</th>
                  <th className="text-left p-2 font-mono">Src IP</th>
                  <th className="text-left p-2 font-mono">Dst IP</th>
                  <th className="text-left p-2">Ports</th>
                  <th className="text-left p-2">Attack</th>
                  <th className="text-left p-2">Severity</th>
                  <th className="text-left p-2">Conf / Uncert</th>
                  <th className="text-left p-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((a) => (
                  <tr key={a.id} className="border-t border-soc-border hover:bg-soc-bg/50">
                    <td className="p-2 font-mono text-gray-400">
                      {new Date(a.created_at).toLocaleTimeString()}
                    </td>
                    <td className="p-2 font-mono text-soc-blue">{a.src_ip}</td>
                    <td className="p-2 font-mono text-soc-blue">{a.dst_ip}</td>
                    <td className="p-2 font-mono">{a.src_port} → {a.dst_port}</td>
                    <td className="p-2">{a.attack_type}</td>
                    <td className="p-2">
                      <span className={`severity-${a.severity} px-2 py-0.5 rounded border text-xs`}>
                        {a.severity}
                      </span>
                    </td>
                    <td className="p-2 font-mono text-xs">
                      {(a.confidence * 100).toFixed(0)}% / {(a.uncertainty * 100).toFixed(0)}%
                    </td>
                    <td className="p-2">
                      <a
                        href={`/dashboard/explain?id=${a.id}`}
                        className="text-soc-blue hover:underline text-xs"
                      >
                        Explain
                      </a>
                      {' · '}
                      <a
                        href={`/dashboard/feedback?alert_id=${a.id}`}
                        className="text-soc-amber hover:underline text-xs"
                      >
                        Feedback
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
