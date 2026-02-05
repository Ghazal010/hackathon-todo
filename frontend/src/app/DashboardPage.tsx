'use client';

import { useAuth } from './context/AuthContext';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import TodoApp from './components/TodoApp';

export default function DashboardPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <p>Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return <TodoApp />;
}