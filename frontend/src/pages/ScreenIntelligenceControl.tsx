import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { wsService } from '../services/websocket';
import { Monitor, CameraOff, Activity, Layers, ScanText, RefreshCw } from 'lucide-react';
import { API_BASE_URL } from '../services/api';

export const ScreenIntelligenceControl: React.FC = () => {
  const [status, setStatus] = useState<any>(null);
  const [monitors, setMonitors] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [selectedMonitor, setSelectedMonitor] = useState(1);
  const [loadingAction, setLoadingAction] = useState<string | null>(null);

  const fetchState = async () => {
    try {
      setStatus(await api.getScreenStatus());
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    api.getScreenMonitors().then(res => setMonitors(res.monitors || [])).catch(console.error);
    fetchState();
    
    const interval = setInterval(fetchState, 1000);
    
    const unsub = wsService.subscribe((data) => {
      try {
        const parsed = JSON.parse(data);
        if (parsed.type === 'CORE_EVENT') {
          const type = parsed.event.type;
          if (type.includes('SCREEN') || type.includes('WINDOW') || type.includes('OCR') || type.includes('UI')) {
            setEvents(prev => [parsed.event, ...prev].slice(0, 50));
          }
        }
      } catch (e) {}
    });

    return () => {
      clearInterval(interval);
      unsub();
    };
  }, []);

  const handleAction = async (action: string, params: any = {}) => {
    setLoadingAction(action);
    try {
      await api.screenAction(action, params);
      await fetchState();
    } catch (e) {
      console.error(e);
    }
    setLoadingAction(null);
  };

  const isScreenRunning = status?.active;

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400">Screen Intelligence</h1>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-4 bg-black/40 px-4 py-2 rounded-lg border border-white/10">
            <span className="text-xs text-white/50 uppercase font-bold flex gap-1 items-center">
              <Activity size={14} className="text-emerald-400" /> FPS: <span className="text-white font-mono">{status?.fps || 0}</span>
            </span>
            <span className="text-xs text-white/50 uppercase font-bold flex gap-1 items-center">
              LATENCY: <span className="text-white font-mono">{status?.latency || 0}ms</span>
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6 flex-1 min-h-0">
        {/* Left Column: Controls & Stats */}
        <div className="flex flex-col gap-6 col-span-1 min-h-0">
          <div className="glass-panel p-6">
            <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4 flex items-center gap-2"><Monitor size={16} /> Capture Controls</h2>
            
            <div className="flex flex-col gap-4">
               <select 
                 value={selectedMonitor} 
                 onChange={e => setSelectedMonitor(Number(e.target.value))}
                 className="bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-white text-sm"
               >
                 {monitors.map((m: any) => (
                   <option key={m.index} value={m.index}>Monitor {m.index} ({m.width}x{m.height})</option>
                 ))}
               </select>
               
               <button 
                 onClick={() => handleAction(isScreenRunning ? 'STOP_SCREEN_CAPTURE' : 'START_SCREEN_CAPTURE', { monitor: selectedMonitor })}
                 className={`px-4 py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors
                   ${isScreenRunning ? 'bg-red-600 hover:bg-red-500 text-white' : 'bg-blue-600 hover:bg-blue-500 text-white'}`}>
                 {isScreenRunning ? <CameraOff size={18} /> : <Monitor size={18} />}
                 {isScreenRunning ? 'Stop Capture' : 'Start Capture'}
               </button>
            </div>
            
            <div className="mt-6 border-t border-white/10 pt-4 space-y-3">
              <button 
                onClick={() => handleAction('READ_UI_TREE')}
                disabled={loadingAction === 'READ_UI_TREE'}
                className="w-full px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg flex items-center justify-center gap-2 text-sm font-bold transition-all disabled:opacity-50">
                {loadingAction === 'READ_UI_TREE' ? <RefreshCw size={16} className="animate-spin" /> : <Layers size={16} className="text-blue-400" />}
                Read Active Window UI Tree
              </button>
              
              <button 
                onClick={() => handleAction('RUN_OCR', { monitor: selectedMonitor })}
                disabled={loadingAction === 'RUN_OCR'}
                className="w-full px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg flex items-center justify-center gap-2 text-sm font-bold transition-all disabled:opacity-50">
                {loadingAction === 'RUN_OCR' ? <RefreshCw size={16} className="animate-spin" /> : <ScanText size={16} className="text-indigo-400" />}
                Run Full Screen OCR
              </button>
            </div>
          </div>
          
          {/* Active Window Context */}
          <div className="glass-panel p-6 flex-1 flex flex-col min-h-0">
             <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4">Context State</h2>
             <div className="space-y-4 overflow-y-auto flex-1 text-sm font-mono text-white/80 pr-2 custom-scrollbar">
                <div>
                  <div className="text-xs text-white/40 mb-1">Active Window</div>
                  <div className="bg-black/30 p-2 rounded border border-white/5 break-words">
                    {status?.state?.active_window?.title || 'None'}
                  </div>
                </div>
                
                {status?.state?.ocr_results && (
                  <div>
                    <div className="text-xs text-white/40 mb-1 flex items-center justify-between">
                      OCR Results
                      <span className="text-[10px] bg-indigo-500/20 text-indigo-300 px-1.5 py-0.5 rounded">{status.state.ocr_results.length} elements</span>
                    </div>
                    <div className="bg-black/30 p-2 rounded border border-white/5 break-words text-[10px] max-h-32 overflow-y-auto custom-scrollbar">
                       {status.state.ocr_results.map((r: any, i: number) => (
                         <div key={i} className="mb-1 border-b border-white/5 pb-1">
                           <span className="text-white">{r.text}</span> <span className="text-white/30 ml-2">({Math.round(r.confidence*100)}%)</span>
                         </div>
                       ))}
                    </div>
                  </div>
                )}
                
                {status?.state?.ui_tree && (
                  <div>
                    <div className="text-xs text-white/40 mb-1">UI Tree (Root)</div>
                    <div className="bg-black/30 p-2 rounded border border-white/5 break-words text-[10px]">
                      Type: {status.state.ui_tree.type}<br/>
                      Name: {status.state.ui_tree.name || '<empty>'}
                    </div>
                  </div>
                )}
             </div>
          </div>
        </div>

        {/* Right Column: Preview & Logs */}
        <div className="col-span-2 flex flex-col gap-6 min-h-0">
           {/* Preview */}
           <div className="glass-panel relative flex items-center justify-center overflow-hidden h-[50%]">
              {isScreenRunning ? (
                <img 
                  src={`${API_BASE_URL}/screen/video_feed?_t=${Date.now()}`} 
                  alt="Desktop Preview" 
                  className="w-full h-full object-contain bg-black"
                />
              ) : (
                <div className="text-white/30 flex flex-col items-center gap-3">
                  <Monitor size={48} />
                  <span>Screen capture offline</span>
                </div>
              )}
           </div>
           
           {/* Event Log */}
           <div className="glass-panel flex flex-col flex-1 min-h-0">
             <div className="p-4 border-b border-white/10 bg-white/5 shrink-0 flex justify-between items-center">
               <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider">Screen Event Log</h2>
               <span className="text-xs px-2 py-1 bg-white/10 rounded text-white/60">{events.length} events</span>
             </div>
             <div className="flex-1 overflow-y-auto p-4 space-y-3 font-mono text-xs custom-scrollbar">
               {events.length === 0 && <div className="text-white/30 text-sm font-sans">No screen events yet...</div>}
               {events.map((ev, i) => (
                 <div key={i} className={`p-3 border rounded-xl ${ev.type.includes('OCR') ? 'border-indigo-500/30 bg-indigo-500/10' : 'border-white/10 bg-black/40'}`}>
                   <div className="flex justify-between text-white/50 mb-2">
                      <span>{new Date(ev.timestamp * 1000).toLocaleTimeString()}</span>
                      <span className={`font-bold ${ev.type.includes('OCR') ? 'text-indigo-400' : 'text-blue-400'}`}>{ev.type}</span>
                   </div>
                   {Object.keys(ev.payload).length > 0 && (
                     <div className="text-white/80 break-words pt-1 border-t border-white/5 max-h-40 overflow-y-auto custom-scrollbar">
                       {ev.type === 'OCR_COMPLETED' ? `Parsed ${ev.payload.results?.length || 0} blocks of text.` : JSON.stringify(ev.payload)}
                     </div>
                   )}
                 </div>
               ))}
             </div>
           </div>
        </div>

      </div>
    </div>
  );
};
