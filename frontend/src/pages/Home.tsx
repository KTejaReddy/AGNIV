import React from 'react';
import { Activity, Brain, Monitor, Mic, Search, Code, Zap } from 'lucide-react';
import { useRuntimeStore } from '../store/useRuntimeStore';
import { useSettingsStore } from '../store/settingsStore';
import { Fireball } from '../components/Fireball';

export const Home: React.FC = () => {
  const { coreState, timeline } = useRuntimeStore();
  const { developerMode } = useSettingsStore();

  if (!developerMode) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-transparent pointer-events-auto">
        <Fireball />
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col gap-6 p-4">
      
      {/* Top Section: AI Core & Quick Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* The Animated AI Core */}
        <div className="lg:col-span-1 glass-panel p-8 flex flex-col items-center justify-center min-h-[300px]">
          <div className="w-full h-48 flex items-center justify-center">
            <Fireball />
          </div>
          
          <div className="mt-8 text-center">
            <h2 className="text-2xl font-bold tracking-widest uppercase mb-1">AGNIV</h2>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10">
              <span className={`w-2 h-2 rounded-full ${
                coreState === 'idle' ? 'bg-indigo-400' :
                coreState === 'listening' ? 'bg-emerald-400' :
                coreState === 'thinking' ? 'bg-purple-400' :
                coreState === 'executing' ? 'bg-amber-400' : 'bg-red-400'
              } animate-pulse`} />
              <span className="text-xs font-medium uppercase tracking-wider text-white/70">
                {coreState}
              </span>
            </div>
          </div>
        </div>

        {/* Runtime Pipeline & Quick Stats */}
        <div className="lg:col-span-2 glass-panel p-6 flex flex-col">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-indigo-400" /> Live Pipeline
          </h3>
          
          <div className="flex-1 flex items-center justify-between px-8 relative">
            {/* Connecting Line */}
            <div className="absolute left-12 right-12 top-1/2 -translate-y-1/2 h-1 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-emerald-500/20 rounded-full" />
            
            <div className="flex flex-col items-center gap-2 z-10">
              <div className="w-12 h-12 rounded-full glass flex items-center justify-center bg-indigo-500/20">
                <Mic className="w-5 h-5 text-indigo-400" />
              </div>
              <span className="text-xs font-medium text-white/60">Input</span>
            </div>

            <div className="flex flex-col items-center gap-2 z-10">
              <div className="w-12 h-12 rounded-full glass flex items-center justify-center bg-purple-500/20">
                <Brain className="w-5 h-5 text-purple-400" />
              </div>
              <span className="text-xs font-medium text-white/60">Reasoning</span>
            </div>

            <div className="flex flex-col items-center gap-2 z-10">
              <div className="w-12 h-12 rounded-full glass flex items-center justify-center bg-emerald-500/20">
                <Monitor className="w-5 h-5 text-emerald-400" />
              </div>
              <span className="text-xs font-medium text-white/60">Execution</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        
        {/* Quick Actions */}
        <div className="lg:col-span-2 glass-panel p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-400" /> Quick Actions
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            
            <button className="flex flex-col items-center gap-3 p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors group">
              <div className="p-3 rounded-full bg-blue-500/20 text-blue-400 group-hover:scale-110 transition-transform">
                <Search className="w-6 h-6" />
              </div>
              <span className="font-medium text-sm">Explain Screen</span>
            </button>

            <button className="flex flex-col items-center gap-3 p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors group">
              <div className="p-3 rounded-full bg-emerald-500/20 text-emerald-400 group-hover:scale-110 transition-transform">
                <Code className="w-6 h-6" />
              </div>
              <span className="font-medium text-sm">Coding Mode</span>
            </button>

            <button className="flex flex-col items-center gap-3 p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors group">
              <div className="p-3 rounded-full bg-purple-500/20 text-purple-400 group-hover:scale-110 transition-transform">
                <Monitor className="w-6 h-6" />
              </div>
              <span className="font-medium text-sm">Browser Assistant</span>
            </button>

          </div>
        </div>

        {/* Live Timeline */}
        <div className="lg:col-span-1 glass-panel p-6 flex flex-col h-full max-h-[400px]">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" /> Live Timeline
          </h3>
          <div className="flex-1 overflow-y-auto space-y-4 pr-2">
            {timeline.map((item, idx) => (
              <div key={idx} className="flex gap-3 text-sm">
                <span className="text-white/40 font-mono shrink-0">{item.time}</span>
                <span className="text-white/80">{item.text}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};
