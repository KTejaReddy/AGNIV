import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Brain, Key, Send, AlertTriangle, CheckCircle, Clock, Database, Code, Shield } from 'lucide-react';

export const CognitiveControl: React.FC = () => {
  const [status, setStatus] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [context, setContext] = useState<any>(null);
  const [apiKey, setApiKey] = useState('');
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchState = async () => {
    try {
      setStatus(await api.getCognitiveStatus());
      const hist = await api.getCognitiveHistory();
      setHistory(hist.history || []);
      setContext(await api.getCognitiveContext());
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleSetKey = async () => {
    try {
      await api.setGroqKey(apiKey);
      setApiKey('');
      alert("API Key updated");
    } catch (e) {
      console.error(e);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    try {
      await api.processCognitiveInput(input);
      setInput('');
      await fetchState();
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-fuchsia-400 to-purple-400">Cognitive Engine</h1>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-4 bg-black/40 px-4 py-2 rounded-lg border border-white/10">
            <span className="text-xs text-white/50 uppercase font-bold flex gap-1 items-center">
              <Clock size={14} className="text-purple-400" /> LATENCY: <span className="text-white font-mono">{status?.latency || 0}ms</span>
            </span>
            <span className="text-xs text-white/50 uppercase font-bold flex gap-1 items-center">
               PROVIDER: <span className="text-white font-mono">{status?.provider || 'none'}</span>
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6 flex-1 min-h-0">
        {/* Left Column: Context & Diagnostics */}
        <div className="flex flex-col gap-6 col-span-1 min-h-0">
          
          <div className="glass-panel p-6">
            <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4 flex items-center gap-2"><Key size={16} /> Provider Config</h2>
            <div className="flex gap-2">
              <input 
                type="password" 
                value={apiKey} 
                onChange={e => setApiKey(e.target.value)} 
                placeholder="Groq API Key (gsk_...)"
                className="flex-1 bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-white text-sm"
              />
              <button 
                onClick={handleSetKey}
                className="bg-purple-600 hover:bg-purple-500 text-white px-3 py-2 rounded-lg font-bold text-sm transition-colors">
                Save
              </button>
            </div>
          </div>

          <div className="glass-panel p-6 flex-1 flex flex-col min-h-0">
             <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4 flex items-center gap-2"><Database size={16} /> Unified Context</h2>
             <div className="flex-1 bg-black/40 border border-white/5 rounded p-3 overflow-y-auto custom-scrollbar font-mono text-[10px] text-white/70">
                {context ? (
                  <pre>{JSON.stringify(context, null, 2)}</pre>
                ) : (
                  <span className="text-white/30">No context loaded</span>
                )}
             </div>
          </div>
          
        </div>

        {/* Middle Column: Chat / Interaction */}
        <div className="glass-panel col-span-1 flex flex-col min-h-0">
           <div className="p-4 border-b border-white/10 bg-white/5 shrink-0">
             <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider flex items-center gap-2"><Brain size={16}/> Reasoning Stream</h2>
           </div>
           
           <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar flex flex-col-reverse">
             {/* Render from bottom up */}
             {[...history].reverse().map((msg, i) => (
               <div key={i} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                 <div className="text-[10px] text-white/30 mb-1">{msg.role} • {new Date(msg.timestamp * 1000).toLocaleTimeString()}</div>
                 <div className={`p-3 rounded-2xl max-w-[90%] text-sm ${msg.role === 'user' ? 'bg-purple-600 text-white' : 'bg-white/10 text-white border border-white/5'}`}>
                   {msg.content}
                 </div>
               </div>
             ))}
           </div>
           
           <div className="p-4 border-t border-white/10 bg-black/20 shrink-0">
             <div className="flex gap-2">
               <input 
                  type="text" 
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleSend()}
                  disabled={loading}
                  placeholder="Test cognitive engine..."
                  className="flex-1 bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-white text-sm"
               />
               <button 
                  onClick={handleSend}
                  disabled={loading}
                  className="bg-fuchsia-600 hover:bg-fuchsia-500 disabled:opacity-50 text-white px-4 py-3 rounded-lg font-bold transition-colors flex items-center justify-center">
                  {loading ? <Clock size={18} className="animate-spin" /> : <Send size={18} />}
               </button>
             </div>
           </div>
        </div>

        {/* Right Column: Execution State & Pipeline */}
        <div className="glass-panel col-span-1 flex flex-col min-h-0">
           <div className="p-4 border-b border-white/10 bg-white/5 shrink-0">
             <h2 className="text-sm font-medium text-white/50 uppercase tracking-wider flex items-center gap-2"><Code size={16}/> Pipeline State</h2>
           </div>
           
           <div className="flex-1 p-6 space-y-6 overflow-y-auto custom-scrollbar">
              
              <div>
                <div className="text-xs text-white/40 mb-2 uppercase tracking-wide font-bold">Execution Path</div>
                <div className="flex gap-2">
                   {['RULE', 'GROQ', 'REJECT', 'CLARIFY'].map(path => (
                     <div key={path} className={`px-3 py-1 rounded text-xs font-bold border ${status?.execution_path === path ? 'bg-purple-500/20 border-purple-500 text-purple-300' : 'bg-white/5 border-white/10 text-white/30'}`}>
                       {path}
                     </div>
                   ))}
                </div>
              </div>
              
              <div>
                <div className="text-xs text-white/40 mb-2 uppercase tracking-wide font-bold">Latest Parsed Intent</div>
                <div className="bg-black/30 p-3 rounded border border-white/5 font-mono text-xs text-white/80">
                  {status?.intent ? (
                    <pre className="whitespace-pre-wrap">{JSON.stringify(status.intent, null, 2)}</pre>
                  ) : (
                    <span className="text-white/30">Waiting for inference...</span>
                  )}
                </div>
              </div>

              <div>
                <div className="text-xs text-white/40 mb-2 uppercase tracking-wide font-bold flex items-center gap-1"><Shield size={14}/> Validation</div>
                <div className="bg-black/30 p-3 rounded border border-white/5 font-mono text-xs text-white/80 flex items-start gap-2">
                  {status?.intent?.type === 'ACTION' ? (
                     <>
                        <CheckCircle size={14} className="text-emerald-400 mt-0.5 shrink-0" />
                        <span>Action [{status.intent.action}] was validated securely by the ExecutionValidator.</span>
                     </>
                  ) : (
                     <>
                        <AlertTriangle size={14} className="text-amber-400 mt-0.5 shrink-0" />
                        <span>No executable action in current intent.</span>
                     </>
                  )}
                </div>
              </div>

           </div>
        </div>

      </div>
    </div>
  );
};
