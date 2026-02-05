'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Bot, LayoutList, User, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Header() {
  const pathname = usePathname();
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <div className="bg-white text-purple-600 rounded-lg p-2">
              <LayoutList size={24} />
            </div>
            <h1 className="text-2xl font-bold">DreamFlow</h1>
          </Link>

          <nav className="flex items-center space-x-1">
            {isAuthenticated ? (
              <>
                <Link
                  href="/"
                  className={`px-4 py-2 rounded-lg transition-colors flex items-center space-x-2 ${
                    pathname === '/'
                      ? 'bg-white/20 text-white'
                      : 'hover:bg-white/10'
                  }`}
                >
                  <LayoutList size={18} />
                  <span>Tasks</span>
                </Link>
                <Link
                  href="/chat"
                  className={`px-4 py-2 rounded-lg transition-colors flex items-center space-x-2 ${
                    pathname === '/chat'
                      ? 'bg-white/20 text-white'
                      : 'hover:bg-white/10'
                  }`}
                >
                  <Bot size={18} />
                  <span>AI Chat</span>
                </Link>
                <div className="relative group">
                  <button className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-white/10 transition-colors">
                    <User size={18} />
                    <span>{user?.username || 'Account'}</span>
                  </button>
                  <div className="absolute right-0 mt-2 w-48 bg-white text-gray-800 rounded-lg shadow-lg py-2 hidden group-hover:block z-50">
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center space-x-2"
                    >
                      <LogOut size={16} />
                      <span>Logout</span>
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
                >
                  Login
                </Link>
                <Link
                  href="/signup"
                  className="px-4 py-2 rounded-lg bg-white/20 hover:bg-white/30 transition-colors"
                >
                  Sign Up
                </Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}