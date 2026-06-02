'use client';

import React, { useEffect, useState } from 'react';
import { User, Brain, Sliders, Zap, Check } from 'lucide-react';
import { getPersona, updatePersona } from '../lib/api';

export default function PersonaPanel() {
  const [persona, setPersona] = useState({
    expertise_level: 'intermediate',
    response_style: 'detailed',
    interests: [] as string[],
  });
  const [isLoading, setIsLoading] = useState(true);

  const fetchPersona = async () => {
    try {
      const data = await getPersona();
      setPersona(data);
    } catch (err) {
      console.error('Failed to fetch persona', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchPersona();
  }, []);

  const handleUpdate = async (update: { expertise_level?: string; response_style?: string; interests?: string[] }) => {
    try {
      const updated = await updatePersona(update);
      setPersona(updated);
    } catch (err) {
      console.error('Failed to update persona', err);
    }
  };

  if (isLoading) return <div className="w-80 p-4">Loading...</div>;

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
          <div className="grid grid-cols-3 gap-2">
            {['beginner', 'intermediate', 'expert'].map((level) => (
              <button
                key={level}
                onClick={() => handleUpdate({ expertise_level: level })}
                className={`px-2 py-1 rounded text-[10px] font-medium capitalize border transition-colors ${
                  persona.expertise_level === level ? 'bg-blue-600 text-white border-blue-700' : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </section>

        <section>
          <div className="flex items-center gap-2 mb-2">
            <Sliders size={16} className="text-slate-400" />
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Response Style</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {['concise', 'balanced', 'detailed'].map((s) => (
              <button
                key={s}
                onClick={() => handleUpdate({ response_style: s })}
                className={`px-2 py-1 rounded text-xs font-medium capitalize border transition-colors ${
                  persona.response_style === s ? 'bg-blue-100 text-blue-700 border-blue-200' : 'bg-slate-50 text-slate-500 border-slate-100 hover:bg-slate-100'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </section>

        <section>
          <div className="flex items-center gap-2 mb-2">
            <Zap size={16} className="text-slate-400" />
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Interests</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {['Finance', 'Tech', 'Medicine', 'AI', 'Law'].map((interest) => {
              const isActive = persona.interests.includes(interest);
              return (
                <button
                  key={interest}
                  onClick={() => {
                    const newInterests = isActive
                      ? persona.interests.filter((i) => i !== interest)
                      : [...persona.interests, interest];
                    handleUpdate({ interests: newInterests });
                  }}
                  className={`px-2 py-1 rounded-full text-xs border transition-colors flex items-center gap-1 ${
                    isActive ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  {interest}
                  {isActive && <Check size={10} />}
                </button>
              );
            })}
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
