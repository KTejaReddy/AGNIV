import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { wsService } from '../services/websocket';

export const DesktopControl: React.FC = () => {
  const [capabilities, setCapabilities] = useState<any>({});
  const [events, setEvents] = useState<any[]>([]);
  const [url, setUrl] = useState('https://google.com');

  useEffect(() => {
    const fetchCaps = async () => {
      try {
        const caps = await api.getCoreCapabilities();
        setCapabilities(caps);
      } catch (e) {
        console.error(e);
      }
    };
    fetchCaps();

    const unsub = wsService.subscribe((data) => {
      try {
        const parsed = JSON.parse(data);
        if (parsed.type === 'CORE_EVENT') {
          // Filter to just TASK events or desktop events
          if (parsed.event.type.startsWith('TASK_') || parsed.event.type.startsWith('CAPABILITY_')) {
            setEvents(prev => [parsed.event, ...prev].slice(0, 50));
          }
        }
      } catch (e) {
        // ignore
      }
    });
    return () => unsub();
  }, []);

  const handleAction = async (category: string, action: string, params: any = {}) => {
    try {
      await api.desktopAction(category, action, params);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">Desktop Control</h1>
      </div>

      <div className="grid grid-cols-3 gap-6 flex-1">
        {/* Actions Panel */}
        <div className="glass-panel p-6 col-span-2 overflow-y-auto max-h-[70vh]">
          <h2 className="text-lg font-medium text-white mb-6">Manual Execution Hub</h2>
          
          <div className="space-y-8">
            {/* System */}
            <div>
              <h3 className="text-sm text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">System</h3>
              <div className="flex flex-wrap gap-3">
                <button onClick={() => handleAction('system', 'volume', { level: 80 })} className="px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm border border-white/10 transition-colors">Vol 80%</button>
                <button onClick={() => handleAction('system', 'mute')} className="px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm border border-white/10 transition-colors">Mute</button>
                <button onClick={() => handleAction('system', 'brightness', { level: 50 })} className="px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm border border-white/10 transition-colors">Brightness 50%</button>
                <button onClick={() => handleAction('screenshot', 'screenshot')} className="px-3 py-2 bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 rounded-lg text-sm border border-blue-500/30 transition-colors">Screenshot</button>
              </div>
            </div>

            {/* Browser */}
            <div>
              <h3 className="text-sm text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Browser</h3>
              <div className="flex gap-3">
                <input type="text" value={url} onChange={e => setUrl(e.target.value)} className="flex-1 bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-sm text-white" />
                <button onClick={() => handleAction('browser', 'open', { url })} className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition-colors">Open URL</button>
              </div>
            </div>

            {/* Clipboard */}
            <div>
              <h3 className="text-sm text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Clipboard</h3>
              <div className="flex gap-3">
                <button onClick={() => handleAction('clipboard', 'read')} className="px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm border border-white/10 transition-colors">Read Clipboard</button>
                <button onClick={() => handleAction('clipboard', 'copy', { text: "Hello from AGNIV" })} className="px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm border border-white/10 transition-colors">Copy "Hello"</button>
                <button onClick={() => handleAction('clipboard', 'clear')} className="px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm border border-white/10 transition-colors">Clear</button>
              </div>
            </div>
            
            {/* Windows */}
            <div>
              <h3 className="text-sm text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Windows</h3>
              <div className="flex gap-3">
                <button onClick={() => handleAction('windows', 'list')} className="px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm border border-white/10 transition-colors">List Windows</button>
              </div>
            </div>

            {/* Registry Preview */}
            <div className="mt-8">
               <h3 className="text-sm text-white/50 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Registered Capabilities ({Object.keys(capabilities).length})</h3>
               <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto pr-2">
                 {Object.keys(capabilities).map(key => (
                   <div key={key} className="text-xs text-white/60 p-2 bg-black/20 rounded truncate" title={capabilities[key].description}>
                     {key} <span className="text-emerald-500 ml-1">v{capabilities[key].version}</span>
                   </div>
                 ))}
               </div>
            </div>

          </div>
        </div>

        {/* Task Log */}
        <div className="glass-panel flex flex-col overflow-hidden">
          <div className="p-4 border-b border-white/10 bg-white/5 shrink-0">
            <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider">Execution History</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3 font-mono text-xs">
            {events.length === 0 && <div className="text-white/30 text-sm font-sans">No tasks executed yet...</div>}
            {events.map((ev, i) => (
              <div key={i} className={`p-3 border rounded-xl 
                ${ev.type.includes('COMPLETED') || ev.type.includes('EXECUTED') ? 'border-emerald-500/20 bg-emerald-500/5' : 
                  ev.type.includes('FAILED') || ev.type.includes('DENIED') ? 'border-red-500/20 bg-red-500/5' : 
                  'border-white/10 bg-black/40'}`}>
                <div className="flex justify-between text-white/50 mb-2">
                   <span>{new Date(ev.timestamp * 1000).toLocaleTimeString()}</span>
                   <span className="font-bold text-white/80">{ev.type}</span>
                </div>
                <div className="text-white break-words">
                  {JSON.stringify(ev.payload, null, 2)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
