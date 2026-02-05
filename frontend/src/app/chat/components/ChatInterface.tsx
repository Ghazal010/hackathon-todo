'use client';

import React, { useState, useEffect, useRef } from 'react';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolCalls?: any[];
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Call the chat API on backend server
      const response = await fetch(`http://localhost:8000/api/${localStorage.getItem('user_id') || 'demo@example.com'}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      // Add AI response
      const aiMessage: Message = {
        id: data.message_id || Date.now(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        toolCalls: data.tool_calls,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage: Message = {
        id: Date.now(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const examples = [
    "Add buy groceries to my list",
    "Show me my tasks",
    "Mark task 1 as done",
    "Delete task 2"
  ];

  return (
    <div className="flex flex-col h-[600px] bg-gray-50 rounded-lg">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-2xl font-semibold text-purple-700 mb-2">
              Welcome to AI Task Assistant! 🤖
            </div>
            <p className="text-gray-600 mb-6">
              Chat naturally to manage your tasks. Try one of these examples:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
              {examples.map((example, index) => (
                <button
                  key={index}
                  onClick={() => setInput(example)}
                  className="bg-white hover:bg-purple-50 border border-purple-200 rounded-lg p-3 text-left text-purple-800 transition-colors"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-purple-500 text-white rounded-br-none'
                    : 'bg-white border border-gray-200 rounded-bl-none'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>
                <div
                  className={`text-xs mt-1 ${
                    msg.role === 'user' ? 'text-purple-200' : 'text-gray-500'
                  }`}
                >
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-none px-4 py-3 max-w-[80%]">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></div>
                </div>
                <span className="text-gray-500 text-sm">AI is typing...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type a message to your AI assistant..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            rows={1}
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="bg-purple-500 hover:bg-purple-600 disabled:bg-purple-300 text-white px-6 py-3 rounded-lg transition-colors font-medium"
          >
            Send
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          Chat naturally: "Add buy groceries", "Show my tasks", "Mark task 1 as done"
        </div>
      </div>
    </div>
  );
}