import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'NIDS SOC Dashboard',
  description: 'Network Intrusion Detection System - Security Operations Center',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-soc-bg text-gray-100 antialiased">{children}</body>
    </html>
  );
}
