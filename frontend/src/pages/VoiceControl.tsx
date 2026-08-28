import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { wsService } from '../services/websocket';
import { Mic, MicOff, Volume2, VolumeX } from 'lucide-react';

export const VoiceControl: React.FC = () => {
  const [status, setStatus] = useState<any>(null);
  const [devices, setDevices] = useState<any>({ microphones: [], voices: [] });
  const [events, setEvents] = useState<any[]>([]);
  const [ttsInput, setTtsInput] = useState('');

  const fetchState = async () => {
    try {
      setStatus(await api.getVoiceStatus());
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    api.getVoiceDevices().then(setDevices).catch(console.error);
    fetchState();
    
    const interval = setInterval(fetchState, 2000);
    
    const unsub = wsService.subscribe((data) => {
      try {
        const parsed = JSON.parse(data);
        if (parsed.type === 'CORE_EVENT') {
          const type = parsed.event.type;
          if (type.includes('LISTENING') || type.includes('SPEECH') || type.includes('WAKE_WORD')) {
            setEvents(prev => [parsed.event, ...prev].slice(0, 50));
            // Immediately fetch state on important voice events
            fetchState();
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
      await api.voiceAction(action, params);
      fetchState();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-emerald-400">Voice Engine</h1>
        <div className="flex items-center gap-3">
          <div className={`px-4 py-2 rounded-lg text-sm font-bold tracking-widest uppercase flex items-center gap-2
            ${status?.state === 'LISTENING' ? 'bg-red-500/20 text-red-400 animate-pulse' : 
              status?.state === 'SPEAKING' ? 'bg-blue-500/20 text-blue-400' :
              status?.state === 'MUTED' ? 'bg-gray-500/20 text-gray-400' :
              'bg-emerald-500/20 text-emerald-400'}`}>
            {status?.state === 'LISTENING' ? <Mic size={16}/> : 
             status?.state === 'SPEAKING' ? <Volume2 size={16}/> :
             status?.state === 'MUTED' ? <MicOff size={16}/> : <Mic size={16}/>}
            {status?.state || 'IDLE'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6 flex-1">
        {/* Controls */}
        <div className="glass-panel p-6 col-span-2 flex flex-col">
          <h2 className="text-lg font-medium text-white mb-6">Speech Controls</h2>
          
          <div className="space-y-6">
            <div className="flex gap-4">
               <button 
                 onClick={() => handleAction(status?.state === 'LISTENING' ? 'STOP_LISTENING' : 'START_LISTENING')}
                 className={`flex-1 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-colors
                   ${status?.state === 'LISTENING' ? 'bg-red-600 hover:bg-red-500 text-white' : 'bg-emerald-600 hover:bg-emerald-500 text-white'}`}>
                 {status?.state === 'LISTENING' ? <MicOff /> : <Mic />}
                 {status?.state === 'LISTENING' ? 'Stop Listening' : 'Push To Talk'}
               </button>
            </div>

            <div className="bg-white/5 border border-white/10 rounded-xl p-4 space-y-4">
              <h3 className="text-sm font-bold text-white/50 uppercase">Text To Speech (TTS)</h3>
              <div className="flex gap-3">
                <input 
                  type="text" 
                  value={ttsInput} 
                  onChange={(e) => setTtsInput(e.target.value)}
                  placeholder="Type something for AGNIV to say..."
                  className="flex-1 bg-black/40 border border-white/10 rounded-lg px-4 py-2 text-white text-sm"
                />
                <button 
                  onClick={() => handleAction('SPEAK_TEXT', { text: ttsInput })}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg font-medium text-white transition-colors"
                >
                  Speak
                </button>
                <button 
                  onClick={() => handleAction('CANCEL_SPEECH')}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg font-medium text-white transition-colors"
                  title="Cancel Queue"
                >
                  <VolumeX size={18} />
                </button>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6 pt-4 border-t border-white/10">
              <div>
                <label className="text-xs text-white/50 uppercase font-bold block mb-2">Microphone Device</label>
                <select className="w-full bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-white text-sm">
                  {devices.microphones.map((m: string, i: number) => <option key={i}>{m}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs text-white/50 uppercase font-bold block mb-2">Voice Output</label>
                <select className="w-full bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-white text-sm">
                  {devices.voices.map((v: any, i: number) => <option key={i}>{v.name}</option>)}
                </select>
              </div>
            </div>
          </div>
          
          <div className="mt-8 flex-1 bg-black/40 border border-white/10 rounded-xl p-4 overflow-y-auto">
             <h3 className="text-xs text-white/50 uppercase font-bold mb-3">Live Transcript</h3>
             <div className="space-y-2 font-mono text-sm">
               {status?.history?.length === 0 && <span className="text-white/30 italic">No speech detected yet...</span>}
               {status?.history?.map((t: string, i: number) => (
                 <div key={i} className="text-white/80">{">"} {t}</div>
               ))}
               {status?.transcript && (
                 <div className="text-emerald-400 font-bold">{">"} {status.transcript} <span className="animate-pulse">_</span></div>
               )}
             </div>
          </div>

        </div>

        {/* Event Log */}
        <div className="glass-panel flex flex-col overflow-hidden">
          <div className="p-4 border-b border-white/10 bg-white/5 shrink-0">
            <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider">Voice Events</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3 font-mono text-xs">
            {events.length === 0 && <div className="text-white/30 text-sm font-sans">No voice events yet...</div>}
            {events.map((ev, i) => (
              <div key={i} className="p-3 border border-white/10 bg-black/40 rounded-xl">
                <div className="flex justify-between text-white/50 mb-2">
                   <span>{new Date(ev.timestamp * 1000).toLocaleTimeString()}</span>
                   <span className="font-bold text-emerald-400">{ev.type}</span>
                </div>
                {Object.keys(ev.payload).length > 0 && (
                  <div className="text-white/80 break-words pt-1 border-t border-white/5">
                    {ev.payload.text || JSON.stringify(ev.payload)}
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
