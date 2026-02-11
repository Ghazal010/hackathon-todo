'use client';

import { useAuth } from './context/AuthContext';
import TodoApp from './components/TodoApp';

export default function DashboardPage() {
  const { isAuthenticated } = useAuth();

  // Allow unauthenticated users to see the main interface
  // They can access login/signup when they choose to

  return <TodoApp />;
}