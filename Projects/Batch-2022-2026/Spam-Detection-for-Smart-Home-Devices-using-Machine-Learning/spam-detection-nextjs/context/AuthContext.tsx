'use client';

import React, { createContext, useContext, useEffect, useReducer } from 'react';
import { saveAuth, getToken, getRole, clearAuth } from '@/lib/auth';

interface AuthState {
  token: string | null;
  role: 'admin' | 'user' | null;
  isLoading: boolean;
}

type AuthAction =
  | { type: 'LOGIN'; token: string; role: 'admin' | 'user' }
  | { type: 'LOGOUT' }
  | { type: 'HYDRATED' };

interface AuthContextValue extends AuthState {
  login: (token: string, role: 'admin' | 'user') => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN':
      return { token: action.token, role: action.role, isLoading: false };
    case 'LOGOUT':
      return { token: null, role: null, isLoading: false };
    case 'HYDRATED':
      return { ...state, isLoading: false };
    default:
      return state;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, {
    token: null,
    role: null,
    isLoading: true,
  });

  // Hydrate from sessionStorage on mount
  useEffect(() => {
    const token = getToken();
    const role = getRole();
    if (token && role) {
      dispatch({ type: 'LOGIN', token, role });
    } else {
      dispatch({ type: 'HYDRATED' });
    }
  }, []);

  const login = (token: string, role: 'admin' | 'user') => {
    saveAuth(token, role);
    dispatch({ type: 'LOGIN', token, role });
  };

  const logout = () => {
    clearAuth();
    dispatch({ type: 'LOGOUT' });
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
