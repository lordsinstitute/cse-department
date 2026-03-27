'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-soc-border bg-soc-panel/80 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-xl font-bold text-soc-green font-mono">NIDS SOC</h1>
          <nav className="flex gap-4">
            <Link href="/login" className="text-soc-blue hover:underline">Login</Link>
            <Link href="/dashboard" className="text-soc-blue hover:underline">Dashboard</Link>
          </nav>
        </div>
      </header>
      <main className="flex-1 flex items-center justify-center p-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-soc-green mb-2">Network Intrusion Detection System</h2>
          <p className="text-gray-400 mb-6">Real-time alerts, explainability, drift monitoring, and analyst feedback.</p>
          <Link
            href="/dashboard"
            className="inline-block px-6 py-3 bg-soc-green/20 text-soc-green border border-soc-green rounded hover:bg-soc-green/30"
          >
            Open Dashboard
          </Link>
        </div>
      </main>
    </div>
  );
}
