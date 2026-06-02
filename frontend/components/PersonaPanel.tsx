'use client';

import React from 'react';
import { User, Brain, Sliders, Zap } from 'lucide-react';

export default function PersonaPanel() {
  // Mock data - would come from an API in Phase 4/5
  const persona = {
    expertise: 'Intermediate',
    style: 'Detailed',
    interests: ['AI Architecture', 'SaaS', 'Fintech'],
    recentTopics: ['RAG', 'Vector DBs', 'Python'],
  };

  return (
    <div className="w-80 bg-white border-l h-full flex flex-col shadow-sm">
      <div className="p-4 border-b flex items-center gap-2 bg-slate-50">
        <Brain className="text-blue-600" size={20} />
        <h2 className="font-bold text-slate-800">Persona Intelligence</h2>
      </div>
      
      <div className="p-4 space-y-6 flex-1 overflow-y-auto">
        <section>
          <div className="flex items-center gap-2 mb-2">
            <User size={16} className="text-slate-400" />
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Expertise Level</h3>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-slate-700">{persona.expertise}</span>
            <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500 w-2/3" />
            </div>
          </div>
        </section>

        <section>
          <div className="flex items-center gap-2 mb-2">
            <Sliders size={16} className="text-slate-400" />
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Response Style</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {['Concise', 'Balanced', 'Detailed'].map((s) => (
              <span key={s} className={`px-2 py-1 rounded text-xs font-medium ${
                persona.style === s ? 'bg-blue-100 text-blue-700 border border-blue-200' : 'bg-slate-50 text-slate-500 border'
              }`}>
                {s}
              </span>
            ))}
          </div>
        </section>

        <section>
          <div className="flex items-center gap-2 mb-2">
            <Zap size={16} className="text-slate-400" />
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Interests</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {persona.interests.map((interest) => (
              <span key={interest} className="px-2 py-1 bg-slate-100 text-slate-700 rounded-full text-xs border">
                {interest}
              </span>
            ))}
          </div>
        </section>

        <section className="bg-blue-50 p-3 rounded-lg border border-blue-100">
          <p className="text-[10px] text-blue-600 font-medium leading-relaxed">
            ContextMind is learning from your behavior. Your persona updates automatically after each conversation.
          </p>
        </section>
      </div>
    </div>
  );
}
