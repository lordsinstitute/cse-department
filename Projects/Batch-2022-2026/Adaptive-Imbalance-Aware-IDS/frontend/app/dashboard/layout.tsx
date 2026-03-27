export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-soc-bg">
      <header className="border-b border-soc-border bg-soc-panel sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-lg font-bold text-soc-green font-mono">NIDS SOC</h1>
          <nav className="flex gap-4 text-sm">
            <a href="/dashboard" className="text-soc-blue hover:underline">Alerts</a>
            <a href="/dashboard/explain" className="text-gray-400 hover:text-white">Explain</a>
            <a href="/dashboard/feedback" className="text-gray-400 hover:text-white">Feedback</a>
            <a href="/dashboard/drift" className="text-gray-400 hover:text-white">Drift</a>
            <a href="/dashboard/training" className="text-gray-400 hover:text-white">Training</a>
          </nav>
        </div>
      </header>
      {children}
    </div>
  );
}
