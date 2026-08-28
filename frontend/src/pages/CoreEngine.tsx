import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { wsService } from '../services/websocket';

export const CoreEngine: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [modules, setModules] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    // Initial fetch
    const fetchCore = async () => {
      try {
        const statusRes = await api.getCoreStatus();
        setMetrics(statusRes.diagnostics);
        const modRes = await api.getCoreModules();
        setModules(modRes);
        const tskRes = await api.getCoreTasks();
        setTasks(tskRes);
      } catch (e) {
        console.error(e);
      }
    };
    
    fetchCore();
    const interval = setInterval(fetchCore, 2000);
    
    // Subscribe to WS events
    const unsub = wsService.subscribe((data) => {
      try {
        const parsed = JSON.parse(data);
        if (parsed.type === 'CORE_EVENT') {
          setEvents(prev => [parsed.event, ...prev].slice(0, 100)); // Keep last 100
        }
      } catch (e) {
        // ignore
      }
    });

    return () => {
      clearInterval(interval);
      unsub();
    };
  }, []);

  const handleSimulate = async (action: string) => {
    try {
      await api.simulateInput(action);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">Core Engine</h1>
        <div className="space-x-3">
          <button onClick={() => handleSimulate("OPEN_APPLICATION")} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-sm font-medium transition-colors">
            Simulate App Open
          </button>
          <button onClick={() => handleSimulate("SYSTEM_SETTINGS")} className="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded-lg text-sm font-medium transition-colors">
            Simulate Settings Open
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Diagnostics */}
        <div className="glass-panel p-6 flex flex-col justify-center">
          <h2 className="text-sm font-medium text-white/50 mb-4 uppercase tracking-wider">Engine Health</h2>
          {metrics ? (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-white/70">CPU</span>
                <span className="font-mono text-indigo-400">{metrics.cpu_percent}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/70">RAM</span>
                <span className="font-mono text-purple-400">{metrics.memory_used_mb} MB ({metrics.memory_percent}%)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/70">Status</span>
                <span className="font-mono text-green-400">{metrics.status}</span>
              </div>
            </div>
          ) : (
            <div className="text-white/30 text-sm">Loading metrics...</div>
          )}
        </div>

        {/* Modules */}
        <div className="glass-panel p-6 col-span-2">
           <h2 className="text-sm font-medium text-white/50 mb-4 uppercase tracking-wider">Active Managers</h2>
           <div className="grid grid-cols-3 gap-3">
             {modules ? Object.keys(modules).map(key => (
               <div key={key} className="p-2 border border-white/10 rounded-lg bg-white/5 flex items-center justify-between">
                 <span className="text-xs truncate">{key.replace('_manager', '').replace('_', ' ')}</span>
                 <div className="w-2 h-2 rounded-full bg-green-500"></div>
               </div>
             )) : <div className="text-white/30 text-sm">Loading modules...</div>}
           </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 flex-1 min-h-[300px]">
        {/* Tasks */}
        <div className="glass-panel flex flex-col overflow-hidden">
          <div className="p-4 border-b border-white/10 bg-white/5 shrink-0">
            <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider">Task Queue</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {tasks.length === 0 && <div className="text-white/30 text-sm">No tasks tracked...</div>}
            {tasks.map(task => (
              <div key={task.id} className="p-3 border border-white/10 rounded-xl bg-[#1a1a1f] text-sm flex justify-between items-center">
                <div className="truncate pr-4 flex-1">
                  <div className="font-medium text-white">{task.name}</div>
                  <div className="text-xs text-white/40 font-mono mt-1">{task.id}</div>
                </div>
                <div className={`px-2 py-1 rounded text-xs font-mono font-bold
                  ${task.status === 'RUNNING' ? 'bg-blue-500/20 text-blue-400' : 
                    task.status === 'COMPLETED' ? 'bg-green-500/20 text-green-400' :
                    task.status === 'FAILED' ? 'bg-red-500/20 text-red-400' : 'bg-gray-500/20 text-gray-400'}`}>
                  {task.status}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Event Stream */}
        <div className="glass-panel flex flex-col overflow-hidden">
          <div className="p-4 border-b border-white/10 bg-white/5 shrink-0">
            <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider">Event Stream</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-xs">
            {events.length === 0 && <div className="text-white/30">Listening for engine events...</div>}
            {events.map((ev, i) => (
              <div key={i} className="py-2 border-b border-white/5 flex gap-4 text-white/80">
                <span className="text-white/30 shrink-0">{new Date(ev.timestamp * 1000).toISOString().split('T')[1].slice(0,8)}</span>
                <span className="text-indigo-400 shrink-0 w-32 truncate" title={ev.source}>[{ev.source}]</span>
                <span className="text-emerald-400 font-bold shrink-0">{ev.type}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
