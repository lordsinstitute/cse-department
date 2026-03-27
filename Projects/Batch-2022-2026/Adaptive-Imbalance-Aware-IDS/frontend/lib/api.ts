const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:9000';

function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('nids_token');
}

export async function api<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error((err as { detail?: string }).detail || res.statusText);
  }
  return res.json();
}

export function wsUrl(path: string): string {
  const base = process.env.NEXT_PUBLIC_WS_URL || 'ws://127.0.0.1:9000';
  return `${base}${path}`;
}

export const apiUrl = API_URL;
