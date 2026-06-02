'use client';

import React, { useState } from 'react';
import ChatWindow from '../components/ChatWindow';
import DocumentUploader from '../components/DocumentUploader';
import PersonaPanel from '../components/PersonaPanel';
import { Brain } from 'lucide-react';

export default function Home() {
  const [sessionId] = useState(() => crypto.randomUUID());

  return (
    <main className="flex h-screen bg-slate-100 font-sans text-slate-900">
      {/* Sidebar / Context */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-16 bg-white border-b flex items-center px-6 justify-between shrink-0">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-1.5 rounded-lg text-white">
              <Brain size={24} />
            </div>
            <h1 className="text-xl font-bold tracking-tight">ContextMind</h1>
          </div>
          <div className="text-xs text-slate-400 font-mono">
            Session: {sessionId.slice(0, 8)}
          </div>
        </header>

        <div className="flex-1 flex overflow-hidden p-6 gap-6">
          <div className="flex-1 flex flex-col gap-6">
            <DocumentUploader />
            <div className="flex-1 min-h-0">
              <ChatWindow sessionId={sessionId} />
            </div>
          </div>
          <PersonaPanel />
        </div>
      </div>
    </main>
  );
}
