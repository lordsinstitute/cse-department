'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import api from '@/lib/api';

type HeaderProps = {
  isAdmin?: boolean;
  isUser?: boolean;
};

export default function Header({ isAdmin, isUser }: HeaderProps) {
  const { logout } = useAuth();
  const { addToast } = useToast();
  const router = useRouter();

  const handleLogout = async () => {
    const endpoint = isAdmin ? '/api/admin/logout' : '/api/user/logout';
    try {
      await api.post(endpoint);
    } catch {
      // Silently ignore — clear auth regardless
    }
    logout();
    addToast('Logged out successfully', 'info');
    router.push('/');
  };

  return (
    <header className="bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            Spam Detection for Smart Home Devices
          </Link>
          <nav>
            <ul className="flex space-x-6">
              {isAdmin ? (
                <>
                  <li>
                    <Link href="/admin/upload" className="hover:text-blue-200">
                      Upload Dataset
                    </Link>
                  </li>
                  <li>
                    <Link href="/admin/compare-algorithms" className="hover:text-blue-200">
                      Compare Algorithms
                    </Link>
                  </li>
                  <li>
                    <Link href="/admin/create-model" className="hover:text-blue-200">
                      Create Model
                    </Link>
                  </li>
                  <li>
                    <button onClick={handleLogout} className="hover:text-blue-200">
                      Logout
                    </button>
                  </li>
                </>
              ) : isUser ? (
                <>
                  <li>
                    <Link href="/user/predict" className="hover:text-blue-200">
                      Predict
                    </Link>
                  </li>
                  <li>
                    <Link href="/user/ingest" className="hover:text-blue-200">
                      Bulk Ingest
                    </Link>
                  </li>
                  <li>
                    <button onClick={handleLogout} className="hover:text-blue-200">
                      Logout
                    </button>
                  </li>
                </>
              ) : (
                <>
                  <li>
                    <Link href="/admin" className="hover:text-blue-200">
                      Admin
                    </Link>
                  </li>
                  <li>
                    <Link href="/user" className="hover:text-blue-200">
                      User
                    </Link>
                  </li>
                </>
              )}
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}
