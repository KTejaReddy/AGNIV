import React from 'react';
import { Blocks } from 'lucide-react';

export const Plugins: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto h-full flex flex-col">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">Plugins</h1>
        <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors text-sm font-medium shadow-lg shadow-indigo-500/20">
          Install Plugin
        </button>
      </div>
      
      <div className="flex-1 glass-panel p-12 flex flex-col items-center justify-center text-center">
        <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mb-4">
          <Blocks className="w-8 h-8 text-white/40" />
        </div>
        <h3 className="text-xl font-semibold mb-2">No plugins installed</h3>
        <p className="text-white/40 max-w-md">
          The plugin framework is ready, but no plugins are currently loaded. Future phases will introduce voice, vision, and AI capability plugins.
        </p>
      </div>
    </div>
  );
};
