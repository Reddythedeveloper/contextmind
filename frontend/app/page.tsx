'use client';

import React, { useState, useEffect } from 'react';
import ChatWindow from '../components/ChatWindow';
import DocumentUploader from '../components/DocumentUploader';
import PersonaPanel from '../components/PersonaPanel';
import ChatSidebar from '../components/ChatSidebar';
import { Brain, Menu, X } from 'lucide-react';

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const createNewSession = () => {
    const newSession = crypto.randomUUID();
    localStorage.setItem('contextmind_current_session', newSession);
    setSessionId(newSession);
  };

  useEffect(() => {
    // Try to get current session from localStorage
    const savedSession = localStorage.getItem('contextmind_current_session');
    if (savedSession) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setSessionId(savedSession);
    } else {
      createNewSession();
    }
  }, []);

  const handleSessionSelect = (id: string) => {
    localStorage.setItem('contextmind_current_session', id);
    setSessionId(id);
  };

  const handleNewChat = () => {
    createNewSession();
  };

  if (!sessionId) {
    return <div className="h-screen bg-slate-900" />;
  }

  return (
    <main className="flex h-screen bg-slate-100 font-sans text-slate-900 overflow-hidden">
      {/* ChatGPT-style Sidebar */}
      {isSidebarOpen && (
        <ChatSidebar 
          currentSessionId={sessionId} 
          onSessionSelect={handleSessionSelect}
          onNewChat={handleNewChat}
        />
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-14 bg-white border-b flex items-center px-4 justify-between shrink-0">
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-1.5 hover:bg-slate-100 rounded-lg transition-colors text-slate-500"
            >
              {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
            <div className="flex items-center gap-2">
              <div className="bg-blue-600 p-1 rounded-md text-white shadow-sm">
                <Brain size={18} />
              </div>
              <h1 className="text-sm font-bold tracking-tight text-slate-800">ContextMind</h1>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
             <div className="hidden sm:flex flex-col items-end">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">Current Session</span>
                <span className="text-[10px] font-mono text-blue-600 font-bold">{sessionId.slice(0, 8)}</span>
             </div>
          </div>
        </header>

        <div className="flex-1 flex overflow-hidden p-4 gap-4">
          <div className="flex-1 flex flex-col gap-4 min-w-0">
            <DocumentUploader sessionId={sessionId} />
            <div className="flex-1 min-h-0">
              {/* Key prop forces re-mount of ChatWindow when sessionId changes */}
              <ChatWindow key={sessionId} sessionId={sessionId} />
            </div>
          </div>
          <div className="hidden lg:block">
            <PersonaPanel />
          </div>
        </div>
      </div>
    </main>
  );
}
