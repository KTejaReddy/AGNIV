import React, { useState, useEffect } from 'react';
import { Mic, Activity, CheckCircle2 } from 'lucide-react';
import { useRuntimeStore } from '../store/useRuntimeStore';

export const Overlays: React.FC = () => {
  const { coreState } = useRuntimeStore();
  const [toast, setToast] = useState<{ message: string, type: 'info' | 'success' } | null>(null);

  // Still allow Alt+T to mock a toast for demonstration
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.altKey && e.code === 'KeyT') {
        setToast({ message: 'Workflow executed successfully.', type: 'success' });
        setTimeout(() => setToast(null), 3000);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <>
      {/* Voice Overlay */}
      {coreState !== 'idle' && (
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 animate-in slide-in-from-bottom-10 fade-in duration-300 pointer-events-none">
          <div className="glass-panel px-6 py-3 flex items-center gap-4 rounded-full border border-indigo-500/30 shadow-[0_0_30px_rgba(99,102,241,0.2)]">
            <div className={`p-2 rounded-full ${
              coreState === 'listening' ? 'bg-emerald-500/20 text-emerald-400 animate-pulse' :
              coreState === 'thinking' ? 'bg-purple-500/20 text-purple-400 animate-spin' :
              'bg-blue-500/20 text-blue-400'
            }`}>
              {coreState === 'thinking' ? <Activity className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </div>
            <div className="font-medium text-white/90">
              {coreState === 'listening' ? 'Listening...' :
               coreState === 'thinking' ? 'Thinking...' :
               coreState === 'executing' ? 'Executing Workflow...' :
               'Processing...'}
            </div>
          </div>
        </div>
      )}

      {/* Toast Notification */}
      {toast && (
        <div className="fixed top-8 right-8 z-50 animate-in slide-in-from-right fade-in duration-300 pointer-events-none">
          <div className="glass-panel px-4 py-3 flex items-center gap-3 rounded-xl border border-emerald-500/30">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <span className="font-medium text-sm">{toast.message}</span>
          </div>
        </div>
      )}
    </>
  );
};
