'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Bot, LayoutList } from 'lucide-react';

export default function Header() {
  const pathname = usePathname();

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

          <nav className="flex space-x-1">
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
          </nav>
        </div>
      </div>
    </header>
  );
}