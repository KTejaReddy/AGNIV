import React, { useState, useEffect, useRef } from 'react';
import { Search, Command, Zap } from 'lucide-react';
import { api } from '../services/api';

export const CommandPalette: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl + Space to open command palette
      if (e.ctrlKey && e.code === 'Space') {
        e.preventDefault();
        setIsOpen(prev => !prev);
      }
      
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleExecute = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      // Send raw text to cognitive engine
      await api.processCognitiveInput(query);
      setIsOpen(false);
      setQuery('');
    } catch (e) {
      console.error('Command failed', e);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] bg-black/40 backdrop-blur-sm" onClick={() => setIsOpen(false)}>
      <div 
        className="w-full max-w-2xl glass-panel shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200"
        onClick={e => e.stopPropagation()}
      >
        <form onSubmit={handleExecute} className="flex items-center gap-3 p-4 border-b border-white/10">
          <Command className="w-6 h-6 text-indigo-400" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command or ask a question..."
            className="flex-1 bg-transparent text-xl outline-none placeholder:text-white/30"
          />
          <button type="submit" className="hidden">Submit</button>
        </form>
        
        {query && (
          <div className="p-2 bg-black/20">
            <button 
              onClick={handleExecute}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 text-left transition-colors"
            >
              <div className="p-2 rounded-lg bg-indigo-500/20 text-indigo-400">
                <Zap className="w-5 h-5" />
              </div>
              <div>
                <div className="font-medium">Execute Command</div>
                <div className="text-sm text-white/50">Send "{query}" to Cognitive Engine</div>
              </div>
            </button>
          </div>
        )}
        
        {!query && (
          <div className="p-4 flex gap-4 text-xs font-medium text-white/40 justify-center">
            <span className="flex items-center gap-1"><kbd className="bg-white/10 px-1.5 py-0.5 rounded">Esc</kbd> to close</span>
            <span className="flex items-center gap-1"><kbd className="bg-white/10 px-1.5 py-0.5 rounded">Enter</kbd> to execute</span>
          </div>
        )}
      </div>
    </div>
  );
};
