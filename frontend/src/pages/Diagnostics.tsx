import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Activity, Server, Cpu, HardDrive, CheckCircle2, XCircle, AlertCircle, Play, AlertTriangle } from 'lucide-react';

export const Diagnostics: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [error, setError] = useState('');
  const [verifying, setVerifying] = useState(false);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await api.getCoreStatus();
        setMetrics(res.diagnostics);
        setError('');
      } catch (err) {
        setError('Failed to fetch diagnostics');
      }
    };
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 500);
    return () => clearInterval(interval);
  }, []);

  const handleVerify = async () => {
    setVerifying(true);
    try {
      await api.verifyDiagnostics();
    } catch (e) {
      console.error(e);
    }
    setVerifying(false);
  };

  if (!metrics) return <div className="p-8">Loading diagnostics...</div>;

  const m = metrics;
  const subsystems = m.subsystems || {};
  const rs = m.runtime_state || {};
  const pl = m.pipeline || {};
  const fail = m.failure_inspector;
  const events = m.recent_events || [];

  return (
    <div className="flex flex-col gap-6 p-6 h-screen overflow-y-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold flex items-center gap-3">
          <Activity className="w-6 h-6 text-indigo-400" />
          Runtime Inspector
        </h1>
        <div className="flex items-center gap-4">
          <button 
            onClick={handleVerify} 
            disabled={verifying}
            className="px-4 py-2 bg-indigo-500/20 text-indigo-400 rounded-lg hover:bg-indigo-500/30 flex items-center gap-2 transition"
          >
            {verifying ? <Activity className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            Verify
          </button>
          <div className="flex items-center gap-2">
            <span className="text-sm text-white/60">Health</span>
            <div className={`px-3 py-1 rounded-full font-mono font-medium ${m.health_score === 100 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
              {m.health_score?.toFixed(1)}%
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-500/20 text-red-400 rounded-xl border border-red-500/30">
          {error}
        </div>
      )}

      {/* Failure Inspector Panel */}
      {fail && (
        <div className="p-6 bg-red-900/20 border border-red-500/50 rounded-xl flex gap-4 animate-pulse">
          <AlertTriangle className="w-8 h-8 text-red-500 flex-shrink-0" />
          <div className="flex flex-col gap-2">
            <h3 className="text-xl font-bold text-red-500">FAILURE: {fail.feature}</h3>
            <p className="text-red-400/80"><span className="font-semibold text-white">Reason:</span> {fail.failure}</p>
            <p className="text-red-400/80"><span className="font-semibold text-white">Root Cause:</span> {fail.root_cause}</p>
            <p className="text-red-400/80"><span className="font-semibold text-white">Location:</span> {fail.file} :: {fail.function}</p>
            <p className="text-yellow-400 mt-2"><span className="font-semibold">Suggested Fix:</span> {fail.suggested_fix}</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        
        {/* Left Col: Subsystems & Pipeline */}
        <div className="flex flex-col gap-6 xl:col-span-2">
          
          <div className="glass-panel p-6">
            <h3 className="text-lg font-medium mb-4">Live Pipeline</h3>
            <div className="flex items-center gap-2 overflow-x-auto pb-2">
              {["Wake Word", "Speech Recognition", "Transcript", "Groq", "Execution Plan", "Capability", "Desktop", "TTS", "Listening"].map((stage, i, arr) => (
                <React.Fragment key={stage}>
                  <div className={`px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all duration-300 ${
                    pl.active_stage === stage ? 'bg-indigo-500 text-white shadow-[0_0_15px_rgba(99,102,241,0.5)] scale-105' : 'bg-white/5 text-white/40'
                  }`}>
                    {stage}
                  </div>
                  {i < arr.length - 1 && <div className="text-white/20">→</div>}
                </React.Fragment>
              ))}
            </div>
          </div>

          <div className="glass-panel p-6">
            <h3 className="text-lg font-medium mb-4">Subsystems</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(subsystems).map(([name, data]: [string, any]) => {
                const s = data.status;
                let color = "text-white/40";
                if (s.includes("🟢")) color = "text-emerald-400";
                if (s.includes("🟡")) color = "text-amber-400";
                if (s.includes("🔴")) color = "text-red-400";

                return (
                  <div key={name} className="bg-white/5 rounded-lg p-3 flex flex-col gap-1 border border-white/5">
                    <span className="text-xs text-white/60 font-medium truncate" title={name}>{name}</span>
                    <span className={`text-sm font-bold ${color}`}>{s}</span>
                    <div className="flex justify-between text-[10px] text-white/40 mt-1">
                      <span>Init: {data.is_initialized ? 'Yes' : 'No'}</span>
                      <span>Run: {data.is_running ? 'Yes' : 'No'}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </div>

        {/* Right Col: Runtime State & Timeline */}
        <div className="flex flex-col gap-6 h-full">
          
          <div className="glass-panel p-6">
            <h3 className="text-lg font-medium mb-4">Runtime State</h3>
            <div className="flex flex-col gap-3 text-sm">
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-white/50">Session UUID</span>
                <span className="font-mono text-white/90">{rs.session_uuid}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-white/50">Current Goal</span>
                <span className="font-mono text-blue-400 truncate max-w-[150px]">{rs.current_goal}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-white/50">Conversation Len</span>
                <span className="font-mono text-white/90">{rs.conversation_length}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-white/50">Capability</span>
                <span className="font-mono text-purple-400">{rs.current_capability}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-white/50">Workflow</span>
                <span className="font-mono text-emerald-400 truncate max-w-[150px]">{rs.current_workflow}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-white/50">Memory Size</span>
                <span className="font-mono text-white/90">{rs.current_memory_context_size}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-white/50">TTS / STT State</span>
                <span className="font-mono text-amber-400">{rs.current_tts_state} / {rs.current_stt_state}</span>
              </div>
            </div>
          </div>

          <div className="glass-panel p-6 flex-1 flex flex-col min-h-[300px]">
            <h3 className="text-lg font-medium mb-4">Event Timeline</h3>
            <div className="flex-1 overflow-y-auto flex flex-col gap-2 font-mono text-xs pr-2 custom-scrollbar">
              {events.slice().reverse().map((e: any, i: number) => (
                <div key={i} className="flex gap-2 p-2 rounded bg-white/5 hover:bg-white/10 transition">
                  <span className="text-white/40 min-w-[60px] truncate">[{e.source}]</span>
                  <span className="text-indigo-300">{e.type}</span>
                </div>
              ))}
              {events.length === 0 && <div className="text-white/40 p-4 text-center">No events yet...</div>}
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
