import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Brain, Activity, Clock, ShieldAlert, ThumbsUp, ThumbsDown, XCircle, BellOff, Sparkles, CheckCircle2 } from 'lucide-react';

export const AdaptiveDashboard: React.FC = () => {
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [patterns, setPatterns] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);

  const fetchData = async () => {
    try {
      const [suggs, pats, hist] = await Promise.all([
        api.getSuggestions(),
        api.getPatterns(),
        api.getAdaptiveHistory()
      ]);
      setSuggestions(suggs);
      setPatterns(pats);
      setHistory(hist);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleFeedback = async (id: string, feedback: string) => {
    try {
      await api.submitAdaptiveFeedback(id, feedback);
      fetchData();
    } catch (e) {
      console.error(e);
    }
  };

  const getConfidenceColor = (conf: string) => {
    switch(conf) {
      case 'VERY_HIGH': return 'text-purple-400 bg-purple-400/10 border-purple-400/20';
      case 'HIGH': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      case 'MEDIUM': return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
      default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500 flex items-center gap-3">
            <Brain size={32} className="text-purple-400" />
            Adaptive Intelligence
          </h1>
          <p className="text-white/50 mt-1">Observing your systemic behavior to suggest actionable improvements.</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6 flex-1 min-h-0">
        {/* Left Column: Suggestions */}
        <div className="col-span-8 flex flex-col gap-4 min-h-0">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Sparkles size={20} className="text-yellow-400" /> 
            Active Suggestions
          </h2>
          <div className="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
            {suggestions.length === 0 ? (
              <div className="glass-panel h-full flex flex-col items-center justify-center text-white/30 p-8 text-center">
                <Brain size={48} className="mb-4 opacity-50" />
                <p className="text-lg">No new suggestions.</p>
                <p className="text-sm">AGNIV is currently observing your behavior to find new optimizations.</p>
              </div>
            ) : (
              suggestions.map((s, i) => (
                <div key={i} className="glass-panel p-6 border border-purple-500/20 relative overflow-hidden group">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 blur-3xl -z-10 rounded-full group-hover:bg-purple-500/20 transition-all"></div>
                  
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-bold text-white">{s.title}</h3>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getConfidenceColor(s.confidence)}`}>
                      {s.confidence} CONFIDENCE
                    </span>
                  </div>
                  
                  <p className="text-white/80 mb-4">{s.description}</p>
                  
                  <div className="bg-black/40 rounded-lg p-4 mb-6 text-sm border border-white/5">
                    <p className="text-white/60 mb-2"><strong className="text-white/80">Reason:</strong> {s.reason}</p>
                    <div className="flex flex-wrap gap-4 mt-3 pt-3 border-t border-white/10">
                      <div className="flex items-center gap-2 text-emerald-400">
                        <Activity size={14} /> Impact: {s.impact}
                      </div>
                      <div className="flex items-center gap-2 text-blue-400">
                        <Clock size={14} /> Saves {s.estimated_time_saved}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex gap-3">
                    <button 
                      onClick={() => handleFeedback(s.id, 'ACCEPT')}
                      className="flex-1 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/30 py-2 rounded-lg font-bold flex justify-center items-center gap-2 transition-colors"
                    >
                      <CheckCircle2 size={18} /> Accept
                    </button>
                    <button 
                      onClick={() => handleFeedback(s.id, 'REJECT')}
                      className="flex-1 bg-white/5 hover:bg-white/10 text-white/70 border border-white/10 py-2 rounded-lg font-bold flex justify-center items-center gap-2 transition-colors"
                    >
                      <XCircle size={18} /> Reject
                    </button>
                    <button 
                      onClick={() => handleFeedback(s.id, 'REMIND_LATER')}
                      className="px-4 bg-white/5 hover:bg-white/10 text-white/70 border border-white/10 rounded-lg transition-colors"
                      title="Remind Later"
                    >
                      <Clock size={18} />
                    </button>
                    <button 
                      onClick={() => handleFeedback(s.id, 'NEVER_SUGGEST_AGAIN')}
                      className="px-4 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-lg transition-colors"
                      title="Never Suggest Again"
                    >
                      <BellOff size={18} />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Column: Patterns & History */}
        <div className="col-span-4 flex flex-col gap-6 min-h-0">
          
          <div className="flex-1 flex flex-col min-h-0">
            <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-4">
              <Activity size={18} className="text-pink-400" />
              Detected Patterns
            </h2>
            <div className="glass-panel flex-1 overflow-y-auto custom-scrollbar p-4 space-y-3">
              {patterns.length === 0 ? (
                <p className="text-white/30 text-center py-4 text-sm">No patterns detected yet.</p>
              ) : (
                patterns.map((p, i) => (
                  <div key={i} className="bg-black/40 border border-white/5 rounded-lg p-3">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs font-bold text-pink-400">{p.type}</span>
                      <span className="text-[10px] text-white/40">{p.frequency} occurrences</span>
                    </div>
                    <p className="text-sm text-white/80 font-mono truncate">{p.context_data.raw_context}</p>
                  </div>
                ))
              )}
            </div>
          </div>
          
          <div className="flex-1 flex flex-col min-h-0">
            <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-4">
              <Clock size={18} className="text-blue-400" />
              Feedback History
            </h2>
            <div className="glass-panel flex-1 overflow-y-auto custom-scrollbar p-4 space-y-3">
              {history.length === 0 ? (
                <p className="text-white/30 text-center py-4 text-sm">No feedback history.</p>
              ) : (
                [...history].reverse().map((h, i) => (
                  <div key={i} className="bg-black/40 border border-white/5 rounded-lg p-3 text-sm">
                    <p className="text-white mb-1 truncate">{h.title}</p>
                    <div className="flex justify-between items-center text-[10px]">
                      <span className={`font-bold ${
                        h.feedback === 'ACCEPT' ? 'text-emerald-400' :
                        h.feedback === 'REJECT' ? 'text-slate-400' :
                        h.feedback === 'NEVER_SUGGEST_AGAIN' ? 'text-red-400' : 'text-blue-400'
                      }`}>{h.feedback}</span>
                      <span className="text-white/30">{new Date(h.timestamp * 1000).toLocaleTimeString()}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};
