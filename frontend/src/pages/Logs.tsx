import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export const Logs: React.FC = () => {
  const [logs, setLogs] = useState<string[]>([]);
  
  useEffect(() => {
    api.getLogs().then(data => setLogs(data.logs)).catch(console.error);
    const interval = setInterval(() => {
      api.getLogs().then(data => setLogs(data.logs)).catch(console.error);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto h-full flex flex-col pb-6">
      <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">System Logs</h1>
      
      <div className="flex-1 glass-panel p-4 overflow-hidden flex flex-col bg-[#050505]">
        <div className="flex-1 overflow-y-auto font-mono text-xs whitespace-pre-wrap text-white/70 scroll-smooth">
          {logs.length > 0 ? (
            logs.map((log, i) => (
              <div key={i} className={`py-1 border-b border-white/5 ${log.includes('ERROR') ? 'text-red-400' : log.includes('WARN') ? 'text-yellow-400' : ''}`}>
                {log}
              </div>
            ))
          ) : (
            <div className="text-white/40 italic p-4">No logs available...</div>
          )}
        </div>
      </div>
    </div>
  );
};
