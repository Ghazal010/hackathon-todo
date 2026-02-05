'use client';

import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-purple-800 mb-2">AI Task Assistant</h1>
            <p className="text-lg text-purple-600">
              Chat naturally to manage your tasks
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <ChatInterface />
          </div>
        </div>
      </div>
    </div>
  );
}