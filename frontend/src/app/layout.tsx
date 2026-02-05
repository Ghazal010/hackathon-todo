import './globals.css'
import './components/todo-styles.css'
import type { Metadata } from 'next'
import Header from './components/Header'
import { AuthProvider } from './context/AuthContext'

export const metadata: Metadata = {
  title: 'DreamFlow - Beautiful Todo App',
  description: 'Your elegant task companion',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <Header />
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  )
}
