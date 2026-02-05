# Feature: Chat UI - Frontend

## Overview
Build a beautiful, responsive chat interface using Next.js that connects to the FastAPI chat endpoint. The UI should feel like a premium messaging app with your purple theme colors.

## User Story
As a user, I want a clean and beautiful chat interface where I can type natural language commands to manage my tasks, see AI responses, and have a smooth conversation experience.

## Color Scheme (Your Purple Theme)
```
Primary Light:   #F5CCE8  → Background, hover states
Primary Medium:  #EC9DED  → AI message bubbles
Primary Dark:    #C880B7  → Buttons, user message bubbles
Primary Deeper: #9F6BA0  → Active states, icons
Primary Darkest: #4A2040  → Header, text headings
```

## Acceptance Criteria

### Must Have
- [ ] Chat layout with header, message list, and input area
- [ ] User messages on RIGHT side (purple bubble)
- [ ] AI messages on LEFT side (light pink bubble)
- [ ] Typing indicator ("AI is typing...")
- [ ] Send button + Enter key support
- [ ] Auto-scroll to latest message
- [ ] Timestamps on messages
- [ ] Loading state on send
- [ ] Error message display
- [ ] Empty state (first time user)
- [ ] Responsive on mobile and desktop
- [ ] Conversation persists on page refresh

### Nice to Have
- [ ] Message sent animation
- [ ] Smooth scroll behavior
- [ ] Quick action buttons (Add Task, Show Tasks)
- [ ] Dark mode support
- [ ] Copy message text
- [ ] Task card display inside chat (formatted)

## UI Layout

### Desktop View
```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  BG: #4A2040                                           │  │
│  │  🤖 TaskFlow AI          [conversation list] [settings]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                                                        │  │
│  │  BG: #FAFAFA (light gray)                              │  │
│  │                                                        │  │
│  │  ┌─────────────────────────┐                           │  │
│  │  │ BG: #FFFFFF             │                           │  │
│  │  │ Border: #F5CCE8         │                           │  │
│  │  │ 🤖 Hi! I'm your task   │                           │  │
│  │  │ assistant. How can I   │                           │  │
│  │  │ help you today?        │                           │  │
│  │  │ 10:30 AM               │                           │  │
│  │  └─────────────────────────┘                           │  │
│  │                                                        │  │
│  │                           ┌─────────────────────────┐  │  │
│  │                           │ BG: #C880B7             │  │  │
│  │                           │ Text: White             │  │  │
│  │                           │ Add buy groceries  🤖   │  │  │
│  │                           │ 10:31 AM                │  │  │
│  │                           └─────────────────────────┘  │  │
│  │                                                        │  │
│  │  ┌─────────────────────────┐                           │  │
│  │  │ ✅ Task added!          │                           │  │
│  │  │                         │                           │  │
│  │  │ ┌───────────────────┐   │                           │  │
│  │  │ │ [1] ⬜ Buy groceries│   │                           │  │
│  │  │ │     Just now      │   │                           │  │
│  │  │ └───────────────────┘   │                           │  │
│  │  │ 10:31 AM                │                           │  │
│  │  └─────────────────────────┘                           │  │
│  │                                                        │  │
│  │  🤖 is typing...                                       │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  BG: #FFFFFF  Border-top: #EC9DED                      │  │
│  │                                                        │  │
│  │  ┌─────────────────────────────┐  ┌─────────────────┐  │  │
│  │  │  Type your message...       │  │   Send 🚀       │  │  │
│  │  │  Border: #EC9DED            │  │   BG: #C880B7   │  │  │
│  │  └─────────────────────────────┘  └─────────────────┘  │  │
│  │                                                        │  │
│  │  Quick Actions:                                        │  │
│  │  [📋 Show Tasks] [➕ Add Task] [✅ Completed]          │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Mobile View
```
┌──────────────────────┐
│  BG: #4A2040         │
│  ← 🤖 TaskFlow AI   │
├──────────────────────┤
│                      │
│  ┌────────────────┐  │
│  │ 🤖 Hi! I'm    │  │
│  │ your task     │  │
│  │ assistant!    │  │
│  │ 10:30 AM      │  │
│  └────────────────┘  │
│                      │
│         ┌──────────┐ │
│         │ Add buy  │ │
│         │ groceries│ │
│         │ 10:31 AM │ │
│         └──────────┘ │
│                      │
│  ┌────────────────┐  │
│  │ ✅ Task added! │  │
│  │ [1] ⬜ Buy     │  │
│  │     groceries  │  │
│  │ 10:31 AM       │  │
│  └────────────────┘  │
│                      │
├──────────────────────┤
│  ┌────────────┐ 🚀  │
│  │ Message... │     │
│  └────────────┘     │
│  [📋][➕][✅]       │
└──────────────────────┘
```

## Component Structure

```
frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx                  # Chat page layout
│   └── layout.tsx
├── components/
│   ├── chat/
│   │   ├── ChatInterface.tsx         # Main chat wrapper
│   │   ├── ChatHeader.tsx            # Top header bar
│   │   ├── MessageList.tsx           # Scrollable messages
│   │   ├── MessageBubble.tsx         # Single message bubble
│   │   ├── TaskCard.tsx              # Task display inside chat
│   │   ├── ChatInput.tsx             # Input + send button
│   │   ├── QuickActions.tsx          # Quick action buttons
│   │   ├── TypingIndicator.tsx       # "AI is typing..."
│   │   └── EmptyState.tsx            # First time user view
│   └── ui/
│       └── ... (shadcn components)
├── hooks/
│   └── useChat.ts                    # Chat logic hook
└── lib/
    └── api.ts                        # API calls
```

## Component Implementation

### 1. Chat Page Layout

**File:** `frontend/app/chat/page.tsx`

```tsx
import ChatInterface from '@/components/chat/ChatInterface'

export default function ChatPage() {
  return (
    <div className="flex h-screen bg-gray-50">
      <ChatInterface />
    </div>
  )
}
```

### 2. useChat Hook (All Logic Here)

**File:** `frontend/hooks/useChat.ts`

```tsx
'use client'
import { useState, useEffect, useRef } from 'react'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  createdAt: string
}

interface ToolCall {
  function: string
  arguments: Record<string, any>
  result: Record<string, any>
}

export function useChat(userId: string) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [conversationId, setConversationId] = useState<number | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  // Load conversation from localStorage on mount
  useEffect(() => {
    const savedConvId = localStorage.getItem('conversation_id')
    if (savedConvId) {
      setConversationId(Number(savedConvId))
      loadHistory(Number(savedConvId))
    }
  }, [])

  // Load conversation history
  const loadHistory = async (convId: number) => {
    try {
      const res = await fetch(`/api/chat/history/${convId}`, {
        headers: { 'Content-Type': 'application/json' }
      })
      if (res.ok) {
        const data = await res.json()
        setMessages(data.messages)
      }
    } catch (err) {
      console.error('Failed to load history:', err)
    }
  }

  // Send message
  const sendMessage = async () => {
    const trimmed = input.trim()
    if (!trimmed || loading) return

    // Add user message immediately
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: trimmed,
      createdAt: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: trimmed,
          conversation_id: conversationId
        })
      })

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`)
      }

      const data = await res.json()

      // Save conversation ID
      if (!conversationId) {
        setConversationId(data.conversation_id)
        localStorage.setItem('conversation_id', String(data.conversation_id))
      }

      // Add AI response
      const aiMessage: Message = {
        id: data.message_id,
        role: 'assistant',
        content: data.response,
        createdAt: new Date().toISOString()
      }
      setMessages(prev => [...prev, aiMessage])

    } catch (err) {
      setError('Failed to send message. Please try again.')
      // Remove user message on error
      setMessages(prev => prev.slice(0, -1))
    } finally {
      setLoading(false)
    }
  }

  // Handle Enter key
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  // Quick action
  const sendQuickAction = (text: string) => {
    setInput(text)
  }

  // Start new conversation
  const newConversation = () => {
    setMessages([])
    setConversationId(null)
    localStorage.removeItem('conversation_id')
  }

  return {
    messages,
    input,
    loading,
    error,
    conversationId,
    messagesEndRef,
    setInput,
    sendMessage,
    handleKeyPress,
    sendQuickAction,
    newConversation
  }
}
```

### 3. ChatInterface (Main Wrapper)

**File:** `frontend/components/chat/ChatInterface.tsx`

```tsx
'use client'
import ChatHeader from './ChatHeader'
import MessageList from './MessageList'
import ChatInput from './ChatInput'
import EmptyState from './EmptyState'
import { useChat } from '@/hooks/useChat'

export default function ChatInterface() {
  const chat = useChat('current_user_id') // Replace with actual user ID

  return (
    <div className="flex flex-col h-screen w-full">
      {/* Header */}
      <ChatHeader onNewConversation={chat.newConversation} />

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-gray-50 p-4">
        {chat.messages.length === 0 ? (
          <EmptyState onQuickAction={chat.sendQuickAction} />
        ) : (
          <MessageList
            messages={chat.messages}
            loading={chat.loading}
            messagesEndRef={chat.messagesEndRef}
          />
        )}
      </div>

      {/* Error Display */}
      {chat.error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 text-sm">
          {chat.error}
        </div>
      )}

      {/* Input Area */}
      <ChatInput
        input={chat.input}
        loading={chat.loading}
        onChange={chat.setInput}
        onSend={chat.sendMessage}
        onKeyPress={chat.handleKeyPress}
        onQuickAction={chat.sendQuickAction}
      />
    </div>
  )
}
```

### 4. ChatHeader

**File:** `frontend/components/chat/ChatHeader.tsx`

```tsx
interface ChatHeaderProps {
  onNewConversation: () => void
}

export default function ChatHeader({ onNewConversation }: ChatHeaderProps) {
  return (
    <div
      className="flex items-center justify-between px-6 py-4 text-white shadow-md"
      style={{ backgroundColor: '#4A2040' }}
    >
      {/* Left - Logo & Title */}
      <div className="flex items-center gap-3">
        <div
          className="w-10 h-10 rounded-full flex items-center justify-center text-xl"
          style={{ backgroundColor: '#C880B7' }}
        >
          🤖
        </div>
        <div>
          <h1 className="text-lg font-bold">TaskFlow AI</h1>
          <p className="text-xs opacity-75">Always here to help</p>
        </div>
      </div>

      {/* Right - Actions */}
      <div className="flex items-center gap-3">
        <button
          onClick={onNewConversation}
          className="text-sm px-3 py-1 rounded-lg transition hover:opacity-80"
          style={{ backgroundColor: '#C880B7' }}
        >
          ✏️ New Chat
        </button>
      </div>
    </div>
  )
}
```

### 5. MessageList

**File:** `frontend/components/chat/MessageList.tsx`

```tsx
import { RefObject } from 'react'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  createdAt: string
}

interface MessageListProps {
  messages: Message[]
  loading: boolean
  messagesEndRef: RefObject<HTMLDivElement>
}

export default function MessageList({ messages, loading, messagesEndRef }: MessageListProps) {
  return (
    <div className="flex flex-col gap-4">
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}

      {/* Typing Indicator */}
      {loading && <TypingIndicator />}

      {/* Scroll Anchor */}
      <div ref={messagesEndRef} />
    </div>
  )
}
```

### 6. MessageBubble

**File:** `frontend/components/chat/MessageBubble.tsx`

```tsx
interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  createdAt: string
}

interface MessageBubbleProps {
  message: Message
}

// Format time → "10:30 AM"
function formatTime(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Detect task list in message and render as cards
function renderContent(content: string) {
  // Split content into lines
  const lines = content.split('\n')

  return lines.map((line, index) => {
    // Detect task pattern: [ID] ☐/✅ Title
    const taskMatch = line.match(/^\[(\d+)\]\s*(⬜|✅|☐)\s*(.+)$/)

    if (taskMatch) {
      const [, id, status, title] = taskMatch
      const isComplete = status === '✅'

      return (
        <div
          key={index}
          className="my-1 px-3 py-2 rounded-lg"
          style={{
            backgroundColor: isComplete ? '#F5CCE8' : '#FFFFFF',
            border: `1px solid ${isComplete ? '#EC9DED' : '#E5E5E5'}`
          }}
        >
          <span className="mr-2">{isComplete ? '✅' : '⬜'}</span>
          <span
            className={`font-medium ${isComplete ? 'line-through' : ''}`}
            style={{ color: '#4A2040' }}
          >
            [{id}] {title}
          </span>
        </div>
      )
    }

    // Normal text line
    return (
      <p key={index} className="text-sm leading-relaxed">
        {line || '\u00A0'}
      </p>
    )
  })
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
      {/* Sender Label */}
      <span
        className="text-xs mb-1 font-semibold"
        style={{ color: '#9F6BA0' }}
      >
        {isUser ? 'You' : '🤖 TaskFlow AI'}
      </span>

      {/* Bubble */}
      <div
        className="max-w-xs sm:max-w-sm md:max-w-md rounded-2xl px-4 py-3 shadow-sm"
        style={{
          backgroundColor: isUser ? '#C880B7' : '#FFFFFF',
          color: isUser ? '#FFFFFF' : '#1F2937',
          borderBottomRightRadius: isUser ? '4px' : '16px',
          borderBottomLeftRadius: isUser ? '16px' : '4px',
          border: isUser ? 'none' : '1px solid #F5CCE8'
        }}
      >
        {/* Content */}
        <div className="flex flex-col gap-1">
          {isUser ? (
            <p className="text-sm">{message.content}</p>
          ) : (
            renderContent(message.content)
          )}
        </div>
      </div>

      {/* Timestamp */}
      <span className="text-xs mt-1 text-gray-400">
        {formatTime(message.createdAt)}
      </span>
    </div>
  )
}
```

### 7. TypingIndicator

**File:** `frontend/components/chat/TypingIndicator.tsx`

```tsx
export default function TypingIndicator() {
  return (
    <div className="flex flex-col items-start">
      <span className="text-xs mb-1 font-semibold" style={{ color: '#9F6BA0' }}>
        🤖 TaskFlow AI
      </span>
      <div
        className="flex items-center gap-1 px-4 py-3 rounded-2xl shadow-sm"
        style={{
          backgroundColor: '#FFFFFF',
          border: '1px solid #F5CCE8',
          borderBottomLeftRadius: '4px'
        }}
      >
        <span className="text-xs text-gray-400 italic">AI is typing</span>
        <div className="flex gap-1 ml-1">
          <span
            className="w-2 h-2 rounded-full animate-bounce"
            style={{ backgroundColor: '#C880B7', animationDelay: '0ms' }}
          />
          <span
            className="w-2 h-2 rounded-full animate-bounce"
            style={{ backgroundColor: '#C880B7', animationDelay: '150ms' }}
          />
          <span
            className="w-2 h-2 rounded-full animate-bounce"
            style={{ backgroundColor: '#C880B7', animationDelay: '300ms' }}
          />
        </div>
      </div>
    </div>
  )
}
```

### 8. ChatInput

**File:** `frontend/components/chat/ChatInput.tsx`

```tsx
import QuickActions from './QuickActions'

interface ChatInputProps {
  input: string
  loading: boolean
  onChange: (value: string) => void
  onSend: () => void
  onKeyPress: (e: React.KeyboardEvent) => void
  onQuickAction: (text: string) => void
}

export default function ChatInput({
  input, loading, onChange, onSend, onKeyPress, onQuickAction
}: ChatInputProps) {
  return (
    <div
      className="bg-white px-4 py-3 shadow-lg"
      style={{ borderTop: '1px solid #EC9DED' }}
    >
      {/* Input Row */}
      <div className="flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={onKeyPress}
          disabled={loading}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 rounded-full text-sm outline-none transition"
          style={{
            border: '2px solid #EC9DED',
            backgroundColor: '#FAFAFA'
          }}
          onFocus={(e) => (e.target.style.borderColor = '#C880B7')}
          onBlur={(e) => (e.target.style.borderColor = '#EC9DED')}
        />

        {/* Send Button */}
        <button
          onClick={onSend}
          disabled={loading || !input.trim()}
          className="w-10 h-10 rounded-full text-white flex items-center justify-center transition shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ backgroundColor: '#C880B7' }}
        >
          {loading ? '⏳' : '🚀'}
        </button>
      </div>

      {/* Quick Actions */}
      <QuickActions onAction={onQuickAction} />
    </div>
  )
}
```

### 9. QuickActions

**File:** `frontend/components/chat/QuickActions.tsx`

```tsx
interface QuickActionsProps {
  onAction: (text: string) => void
}

const actions = [
  { label: '📋 Show Tasks', text: 'Show me all my tasks' },
  { label: '➕ Add Task', text: 'I want to add a new task: ' },
  { label: '✅ Completed', text: 'Show my completed tasks' },
  { label: '⏳ Pending', text: 'What tasks are pending?' }
]

export default function QuickActions({ onAction }: QuickActionsProps) {
  return (
    <div className="flex flex-wrap gap-2 mt-3">
      {actions.map((action) => (
        <button
          key={action.label}
          onClick={() => onAction(action.text)}
          className="text-xs px-3 py-1 rounded-full transition hover:opacity-80"
          style={{
            backgroundColor: '#F5CCE8',
            color: '#4A2040',
            border: '1px solid #EC9DED'
          }}
        >
          {action.label}
        </button>
      ))}
    </div>
  )
}
```

### 10. EmptyState

**File:** `frontend/components/chat/EmptyState.tsx`

```tsx
interface EmptyStateProps {
  onQuickAction: (text: string) => void
}

const suggestions = [
  { emoji: '📝', text: 'Add buy groceries', description: 'Create a new task' },
  { emoji: '📋', text: 'Show me all my tasks', description: 'View your task list' },
  { emoji: '✅', text: 'Show completed tasks', description: 'See what you finished' },
  { emoji: '🔍', text: 'What is pending?', description: 'Check pending tasks' }
]

export default function EmptyState({ onQuickAction }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full py-16 px-4">
      {/* Logo */}
      <div
        className="w-20 h-20 rounded-full flex items-center justify-center text-4xl mb-4 shadow-lg"
        style={{ backgroundColor: '#F5CCE8' }}
      >
        🤖
      </div>

      {/* Title */}
      <h2 className="text-2xl font-bold mb-2" style={{ color: '#4A2040' }}>
        Hi there! 👋
      </h2>

      {/* Subtitle */}
      <p className="text-gray-500 text-center max-w-sm mb-8">
        I'm your AI task assistant. I can help you manage your tasks using natural language.
        Just type what you need!
      </p>

      {/* Suggestions */}
      <div className="w-full max-w-md flex flex-col gap-3">
        <p className="text-xs font-semibold text-center" style={{ color: '#9F6BA0' }}>
          TRY THESE:
        </p>
        {suggestions.map((s, i) => (
          <button
            key={i}
            onClick={() => onQuickAction(s.text)}
            className="flex items-center gap-3 px-4 py-3 rounded-xl bg-white shadow-sm transition hover:shadow-md text-left"
            style={{ border: '1px solid #F5CCE8' }}
          >
            <span className="text-xl">{s.emoji}</span>
            <div>
              <p className="text-sm font-medium" style={{ color: '#4A2040' }}>
                "{s.text}"
              </p>
              <p className="text-xs text-gray-400">{s.description}</p>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
```

## Responsive Design

### Breakpoints
```
Mobile:  < 640px   → Full width, compact bubbles
Tablet:  640-1024px → Max width bubbles 80%
Desktop: > 1024px  → Max width bubbles 60%
```

### Mobile Adjustments
```css
/* Max bubble width */
@media (max-width: 640px) {
  .bubble { max-width: 75%; }
  .input { padding: 8px; }
  .quick-actions { gap: 4px; }
}
```

## Animation & Transitions

### 1. Message Appear
```css
/* New messages slide up */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

.message { animation: slideUp 0.3s ease-out; }
```

### 2. Typing Dots (Already in TypingIndicator)
```css
/* Bouncing dots */
.dot { animation: bounce 1s infinite; }
.dot:nth-child(2) { animation-delay: 150ms; }
.dot:nth-child(3) { animation-delay: 300ms; }
```

### 3. Send Button Pulse
```css
button:hover { transform: scale(1.05); }
button:active { transform: scale(0.95); }
```

## Error States

### 1. Network Error
```
┌─────────────────────────────────┐
│ ❌ Failed to send message.      │
│    Please check your connection │
│    [Retry]                      │
└─────────────────────────────────┘
```

### 2. AI Error
```
┌─────────────────────────────────┐
│ 🤖 Sorry, I encountered an     │
│    error. Please try again.     │
└─────────────────────────────────┘
```

### 3. Empty Input
```
/* Send button disabled */
opacity: 50%
cursor: not-allowed
```

## Testing

### Test 1: Send Message
1. Type "Add buy groceries"
2. Press Enter or click Send
3. ✅ User bubble appears on right
4. ✅ Typing indicator shows
5. ✅ AI response appears on left

### Test 2: Quick Actions
1. Click "📋 Show Tasks"
2. ✅ Input fills with "Show me all my tasks"
3. Press Enter
4. ✅ Tasks displayed in chat

### Test 3: Conversation Persistence
1. Send a few messages
2. Refresh page
3. ✅ Old messages still visible

### Test 4: Mobile
1. Open on phone/tablet
2. ✅ Layout adjusts properly
3. ✅ Bubbles readable
4. ✅ Input accessible

### Test 5: Empty State
1. Start new conversation
2. ✅ Welcome screen shows
3. Click suggestion
4. ✅ Message sends

## Success Criteria

- [ ] Chat layout renders correctly
- [ ] User/AI bubbles positioned correctly
- [ ] Purple theme applied consistently
- [ ] Typing indicator works
- [ ] Send via button and Enter key
- [ ] Auto-scroll on new messages
- [ ] Quick actions work