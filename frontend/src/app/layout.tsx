import './globals.css'
import './components/todo-styles.css'
import type { Metadata } from 'next'
import Header from './components/Header'

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
        <Header />
        <main>{children}</main>
      </body>
    </html>
  )
}
