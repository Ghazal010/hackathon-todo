import { useAuth } from './context/AuthContext';
import { redirect } from 'next/navigation';
import TodoApp from './components/TodoApp';

export default function Home() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    // If not authenticated, redirect to login page
    redirect('/login');
  }

  return <TodoApp />;
}