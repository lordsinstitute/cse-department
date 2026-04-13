'use client';

const TOKEN_KEY = 'iot_access_token';
const ROLE_KEY = 'iot_user_role';

export function saveAuth(token: string, role: string): void {
  sessionStorage.setItem(TOKEN_KEY, token);
  sessionStorage.setItem(ROLE_KEY, role);
}

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return sessionStorage.getItem(TOKEN_KEY);
}

export function getRole(): 'admin' | 'user' | null {
  if (typeof window === 'undefined') return null;
  const role = sessionStorage.getItem(ROLE_KEY);
  return (role as 'admin' | 'user') || null;
}

export function clearAuth(): void {
  sessionStorage.removeItem(TOKEN_KEY);
  sessionStorage.removeItem(ROLE_KEY);
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}
