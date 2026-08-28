import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { User, UserCheck, Eye, EyeOff, Hand, MessageSquare, CheckCircle2, XCircle, Bell } from 'lucide-react';

export const InteractionControl: React.FC = () => {
  const [status, setStatus] = useState<any>(null);

  const fetchState = async () => {
    try {
      setStatus(await api.getInteractionStatus());
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleSimulateGesture = async (gesture: string) => {
    try {
      await api.simulateGesture(gesture);
      await fetchState();
    } catch (e) {
      console.error(e);
    }
  };

  const handleConfirm = async (accepted: boolean) => {
    try {
      await api.confirmInteraction(accepted);
      await fetchState();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-orange-400 to-rose-400">Human Interaction</h1>
      </div>

      <div className="grid grid-cols-3 gap-6 flex-1 min-h-0">
        
        {/* Left Column: State & Simulation */}
        <div className="flex flex-col gap-6 col-span-1 min-h-0">
          
          <div className="glass-panel p-6">
            <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4 flex items-center gap-2">Live Context</h2>
            
            <div className="space-y-4">
               <div className="flex items-center justify-between p-3 bg-black/40 rounded-lg border border-white/5">
                 <div className="flex items-center gap-2">
                   {status?.presence === 'USER_ACTIVE' ? <UserCheck className="text-emerald-400" size={18}/> : <User className="text-white/30" size={18}/>}
                   <span className="text-sm font-medium">Presence</span>
                 </div>
                 <span className="text-xs font-mono font-bold text-white/70">{status?.presence || 'UNKNOWN'}</span>
               </div>
               
               <div className="flex items-center justify-between p-3 bg-black/40 rounded-lg border border-white/5">
                 <div className="flex items-center gap-2">
                   {status?.attention === 'LOOKING_AT_SCREEN' || status?.attention === 'TALKING' ? <Eye className="text-blue-400" size={18}/> : <EyeOff className="text-white/30" size={18}/>}
                   <span className="text-sm font-medium">Attention</span>
                 </div>
                 <span className="text-xs font-mono font-bold text-white/70">{status?.attention || 'UNKNOWN'}</span>
               </div>

               <div className="flex items-center justify-between p-3 bg-black/40 rounded-lg border border-white/5">
                 <div className="flex items-center gap-2">
                   <Bell className="text-amber-400" size={18}/>
                   <span className="text-sm font-medium">Notification Mode</span>
                 </div>
                 <span className="text-xs font-mono font-bold text-white/70">{status?.notification_mode || 'IMMEDIATE'}</span>
               </div>
            </div>
          </div>

          <div className="glass-panel p-6 flex-1">
             <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4 flex items-center gap-2"><Hand size={16} /> Simulate Gestures</h2>
             <div className="grid grid-cols-2 gap-3">
               <button onClick={() => handleSimulateGesture('Thumb_Up')} className="bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg p-3 text-sm font-bold transition-all text-emerald-400">👍 Thumbs Up</button>
               <button onClick={() => handleSimulateGesture('Thumb_Down')} className="bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg p-3 text-sm font-bold transition-all text-red-400">👎 Thumbs Down</button>
               <button onClick={() => handleSimulateGesture('Open_Palm')} className="bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg p-3 text-sm font-bold transition-all text-blue-400">👋 Wave (Palm)</button>
               <button onClick={() => handleSimulateGesture('Closed_Fist')} className="bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg p-3 text-sm font-bold transition-all text-amber-400">✊ Stop (Fist)</button>
             </div>
             <p className="text-[10px] text-white/30 mt-4 leading-relaxed">
               Clicking these buttons injects mock GESTURE payloads directly into the Interaction Manager, bypassing the need to have your camera active.
             </p>
          </div>
          
        </div>

        {/* Middle Column: Event Timeline */}
        <div className="glass-panel col-span-1 flex flex-col min-h-0">
           <div className="p-4 border-b border-white/10 bg-white/5 shrink-0">
             <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider flex items-center gap-2">Interaction Timeline</h2>
           </div>
           
           <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar flex flex-col-reverse">
             {status?.events && [...status.events].reverse().map((ev: any, i: number) => (
               <div key={i} className="flex gap-3">
                 <div className="flex flex-col items-center">
                   <div className="w-2 h-2 rounded-full bg-orange-500 mt-1.5" />
                   {i !== status.events.length - 1 && <div className="w-0.5 h-full bg-white/5 my-1" />}
                 </div>
                 <div className="flex-1 pb-4">
                   <div className="text-xs font-bold text-orange-400 mb-1">{ev.type}</div>
                   <div className="text-[10px] font-mono text-white/50 break-words bg-black/20 p-2 rounded border border-white/5">
                     {JSON.stringify(ev.payload)}
                   </div>
                 </div>
               </div>
             ))}
             {(!status?.events || status.events.length === 0) && (
               <div className="text-white/30 text-sm italic p-4 text-center">No interactions yet.</div>
             )}
           </div>
        </div>

        {/* Right Column: Pending Confirmations */}
        <div className="glass-panel col-span-1 flex flex-col min-h-0">
           <div className="p-4 border-b border-white/10 bg-white/5 shrink-0 flex items-center justify-between">
             <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider flex items-center gap-2">Pending Confirmations</h2>
             <span className="text-xs bg-orange-500/20 text-orange-400 px-2 py-0.5 rounded-full font-bold">{status?.pending_confirmations?.length || 0}</span>
           </div>
           
           <div className="flex-1 p-4 overflow-y-auto custom-scrollbar">
              {status?.pending_confirmations?.length > 0 ? (
                status.pending_confirmations.map((conf: any) => (
                  <div key={conf.id} className="bg-orange-500/10 border border-orange-500/30 rounded-xl p-4 mb-4">
                    <div className="text-xs text-orange-300 font-bold mb-2 uppercase tracking-wide">Action Requested</div>
                    <div className="text-lg font-bold text-white mb-1">{conf.action}</div>
                    <div className="text-xs font-mono text-white/60 mb-4">{JSON.stringify(conf.params)}</div>
                    
                    <div className="flex gap-2 mt-4">
                      <button onClick={() => handleConfirm(true)} className="flex-1 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 border border-emerald-500/50 py-2 rounded-lg font-bold text-sm flex items-center justify-center gap-2 transition-colors">
                        <CheckCircle2 size={16} /> Accept
                      </button>
                      <button onClick={() => handleConfirm(false)} className="flex-1 bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500/50 py-2 rounded-lg font-bold text-sm flex items-center justify-center gap-2 transition-colors">
                        <XCircle size={16} /> Reject
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-white/30 space-y-3">
                  <CheckCircle2 size={48} className="opacity-20" />
                  <span className="text-sm font-medium">No pending confirmations</span>
                </div>
              )}
           </div>
        </div>

      </div>
    </div>
  );
};
