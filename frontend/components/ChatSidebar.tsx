'use client';

import React, { useEffect, useState } from 'react';
import { MessageSquare, Plus, Trash2, Layout } from 'lucide-react';
import { listSessions, deleteSession } from '../lib/api';

interface ChatSidebarProps {
  currentSessionId: string | null;
  onSessionSelect: (sessionId: string) => void;
  onNewChat: () => void;
}

export default function ChatSidebar({ currentSessionId, onSessionSelect, onNewChat }: ChatSidebarProps) {
  const [sessions, setSessions] = useState<{ session_id: string, title?: string }[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchSessions = async () => {
    try {
      const data = await listSessions();
      setSessions(data);
    } catch (err) {
      console.error('Failed to fetch sessions', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchSessions();
  }, [currentSessionId]);

  const handleDelete = async (e: React.MouseEvent, sessionId: string) => {
    e.stopPropagation();
    if (confirm('Delete this chat?')) {
      try {
        await deleteSession(sessionId);
        await fetchSessions();
        if (currentSessionId === sessionId) {
          onNewChat();
        }
      } catch (err) {
        console.error('Failed to delete session', err);
      }
    }
  };

  return (
    <div className="w-64 bg-slate-900 text-slate-300 h-full flex flex-col shrink-0">
      <div className="p-4">
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors shadow-lg shadow-blue-900/20"
        >
          <Plus size={18} />
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1 custom-scrollbar">
        <div className="px-2 mb-2">
          <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Recent Chats</h3>
        </div>
        
        {loading ? (
          <div className="px-4 py-2 text-xs text-slate-500">Loading...</div>
        ) : (
          sessions
            .filter((s, index, self) => s.session_id && self.findIndex(t => t.session_id === s.session_id) === index)
            .map((session) => (
              <div
                key={session.session_id}
                onClick={() => session.session_id && onSessionSelect(session.session_id)}
                className={`group flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all ${
                  currentSessionId === session.session_id
                    ? 'bg-slate-800 text-white border border-slate-700'
                    : 'hover:bg-slate-800/50 hover:text-slate-200'
                }`}
              >
              <div className="flex items-center gap-3 overflow-hidden">
                <MessageSquare size={14} className={currentSessionId === session.session_id ? 'text-blue-400' : 'text-slate-500'} />
                <span className="text-xs font-medium truncate">
                  {session.title || `Chat ${(session.session_id || '').slice(0, 8)}`}
                </span>
              </div>
              <button
                onClick={(e) => handleDelete(e, session.session_id)}
                className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-400 transition-opacity"
              >
                <Trash2 size={12} />
              </button>
            </div>
          ))
        )}
      </div>

      <div className="p-4 border-t border-slate-800 flex items-center gap-3">
        <div className="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center text-blue-400">
          <Layout size={16} />
        </div>
        <div>
          <p className="text-[10px] font-bold text-slate-500 uppercase">ContextMind</p>
          <p className="text-[10px] text-slate-400">v1.0 - Stable</p>
        </div>
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #1e293b;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #334155;
        }
      `}</style>
    </div>
  );
}
