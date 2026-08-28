import React, { useEffect, useState, useRef } from 'react';
import { api } from '../services/api';
import { wsService } from '../services/websocket';
import { Eye, EyeOff, Activity } from 'lucide-react';
import { API_BASE_URL } from '../services/api';

export const PerceptionControl: React.FC = () => {
  const [status, setStatus] = useState<any>(null);
  const [devices, setDevices] = useState<any>({ cameras: [] });
  const [events, setEvents] = useState<any[]>([]);
  const [selectedCam, setSelectedCam] = useState(0);

  const fetchState = async () => {
    try {
      setStatus(await api.getPerceptionStatus());
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    api.getPerceptionDevices().then(setDevices).catch(console.error);
    fetchState();
    
    const interval = setInterval(fetchState, 1000);
    
    const unsub = wsService.subscribe((data) => {
      try {
        const parsed = JSON.parse(data);
        if (parsed.type === 'CORE_EVENT') {
          const type = parsed.event.type;
          if (type.includes('CAMERA') || type.includes('DETECTED') || type.includes('TRACKING')) {
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
    try {
      await api.perceptionAction(action, params);
      fetchState();
    } catch (e) {
      console.error(e);
    }
  };

  const isCamRunning = status?.fps !== undefined && status?.fps > 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">Perception Engine</h1>
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

      <div className="grid grid-cols-4 gap-6 flex-1">
        {/* Main View */}
        <div className="glass-panel p-6 col-span-3 flex flex-col gap-6">
          
          <div className="flex gap-4 items-center">
             <select 
               value={selectedCam} 
               onChange={e => setSelectedCam(Number(e.target.value))}
               className="bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-white text-sm"
             >
               {devices.cameras.map((c: number) => <option key={c} value={c}>Camera {c}</option>)}
             </select>
             
             <button 
               onClick={() => handleAction(isCamRunning ? 'STOP_CAMERA' : 'START_CAMERA', { camera_id: selectedCam })}
               className={`px-4 py-2 rounded-lg font-bold flex items-center gap-2 transition-colors
                 ${isCamRunning ? 'bg-red-600 hover:bg-red-500 text-white' : 'bg-purple-600 hover:bg-purple-500 text-white'}`}>
               {isCamRunning ? <EyeOff size={18} /> : <Eye size={18} />}
               {isCamRunning ? 'Stop Camera' : 'Start Camera'}
             </button>
          </div>

          <div className="relative flex-1 bg-black/80 rounded-xl overflow-hidden border border-white/10 flex items-center justify-center min-h-[400px]">
            {isCamRunning ? (
              <img 
                src={`${API_BASE_URL}/perception/video_feed?_t=${Date.now()}`} 
                alt="Live Preview" 
                className="absolute inset-0 w-full h-full object-contain"
              />
            ) : (
              <div className="text-white/30 flex flex-col items-center gap-3">
                <EyeOff size={48} />
                <span>Camera Offline</span>
              </div>
            )}
            
            {/* Overlay State */}
            {isCamRunning && (
              <div className="absolute top-4 right-4 bg-black/60 backdrop-blur-md border border-white/10 rounded-lg p-3 space-y-2">
                 <div className="text-xs font-mono">
                   <span className="text-white/50">GESTURE:</span> <span className="text-emerald-400 font-bold">{status?.state?.gesture || 'NONE'}</span>
                 </div>
              </div>
            )}
          </div>

          <div className="grid grid-cols-4 gap-4">
             <button onClick={() => handleAction('ENABLE_HAND_TRACKING', { enabled: !status?.trackers?.hands })}
               className={`p-3 rounded-lg border text-sm font-bold transition-all ${status?.trackers?.hands ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300' : 'bg-white/5 border-white/10 text-white/50 hover:bg-white/10'}`}>
               Hand Tracking
             </button>
             <button onClick={() => handleAction('ENABLE_FACE_TRACKING', { enabled: !status?.trackers?.face })}
               className={`p-3 rounded-lg border text-sm font-bold transition-all ${status?.trackers?.face ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300' : 'bg-white/5 border-white/10 text-white/50 hover:bg-white/10'}`}>
               Face Tracking
             </button>
             <button onClick={() => handleAction('ENABLE_BODY_TRACKING', { enabled: !status?.trackers?.body })}
               className={`p-3 rounded-lg border text-sm font-bold transition-all ${status?.trackers?.body ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300' : 'bg-white/5 border-white/10 text-white/50 hover:bg-white/10'}`}>
               Body Tracking
             </button>
             <button onClick={() => handleAction('ENABLE_GESTURE_RECOGNITION', { enabled: !status?.trackers?.gestures })}
               className={`p-3 rounded-lg border text-sm font-bold transition-all ${status?.trackers?.gestures ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300' : 'bg-white/5 border-white/10 text-white/50 hover:bg-white/10'}`}>
               Gesture Engine
             </button>
          </div>

        </div>

        {/* Event Log */}
        <div className="glass-panel flex flex-col overflow-hidden">
          <div className="p-4 border-b border-white/10 bg-white/5 shrink-0">
            <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider">Perception Log</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3 font-mono text-xs">
            {events.length === 0 && <div className="text-white/30 text-sm font-sans">No perception events yet...</div>}
            {events.map((ev, i) => (
              <div key={i} className={`p-3 border rounded-xl ${ev.type.includes('GESTURE') ? 'border-purple-500/30 bg-purple-500/10' : 'border-white/10 bg-black/40'}`}>
                <div className="flex justify-between text-white/50 mb-2">
                   <span>{new Date(ev.timestamp * 1000).toLocaleTimeString()}</span>
                   <span className={`font-bold ${ev.type.includes('GESTURE') ? 'text-purple-400' : 'text-white/80'}`}>{ev.type}</span>
                </div>
                {Object.keys(ev.payload).length > 0 && (
                  <div className="text-white/80 break-words pt-1 border-t border-white/5">
                    {JSON.stringify(ev.payload)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
