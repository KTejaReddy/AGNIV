import React, { useEffect, useState, useRef, useCallback } from 'react';
import { api } from '../services/api';
import { HardDrive, Search, Trash2, Download, Filter, BrainCircuit, PlayCircle, Network, Clock, ShieldAlert } from 'lucide-react';
import ForceGraph2D from 'react-force-graph-2d';

export const MemoryDashboard: React.FC = () => {
  const [memories, setMemories] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('ALL');
  const [selectedImportance, setSelectedImportance] = useState('ALL');
  const [activeTab, setActiveTab] = useState<'timeline' | 'graph'>('timeline');
  const graphRef = useRef<any>();

  const fetchMemories = async () => {
    try {
      if (searchQuery) {
        const data = await api.searchMemories(searchQuery);
        setMemories(data);
      } else {
        const data = await api.getMemories();
        setMemories(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchMemories();
  }, [searchQuery]);

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to permanently delete this memory?')) {
      try {
        await api.deleteMemory(id);
        fetchMemories();
      } catch (e) {
        console.error(e);
      }
    }
  };

  const getImportanceColor = (imp: string) => {
    switch (imp) {
      case 'CRITICAL': return 'text-red-400 bg-red-400/10 border-red-400/20';
      case 'HIGH': return 'text-orange-400 bg-orange-400/10 border-orange-400/20';
      case 'MEDIUM': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      case 'LOW': return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
      case 'TEMPORARY': return 'text-purple-400 bg-purple-400/10 border-purple-400/20';
      default: return 'text-white bg-white/10 border-white/20';
    }
  };

  const filteredMemories = memories.filter(m => {
    if (selectedType !== 'ALL' && m.type !== selectedType) return false;
    if (selectedImportance !== 'ALL' && m.importance !== selectedImportance) return false;
    return true;
  });

  const types = ['ALL', ...Array.from(new Set(memories.map(m => m.type)))];
  const importances = ['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'TEMPORARY'];

  // Graph Data construction
  const graphData = { nodes: [] as any[], links: [] as any[] };
  if (activeTab === 'graph') {
    const nodesMap = new Map();
    filteredMemories.forEach(m => {
      nodesMap.set(m.id, { id: m.id, name: m.title, val: 5, color: '#a855f7', type: 'memory' });
      
      m.related_skills.forEach((s: string) => {
        if (!nodesMap.has(s)) nodesMap.set(s, { id: s, name: s, val: 3, color: '#3b82f6', type: 'skill' });
        graphData.links.push({ source: m.id, target: s });
      });
      m.related_workflows.forEach((w: string) => {
        if (!nodesMap.has(w)) nodesMap.set(w, { id: w, name: w, val: 3, color: '#10b981', type: 'workflow' });
        graphData.links.push({ source: m.id, target: w });
      });
    });
    graphData.nodes = Array.from(nodesMap.values());
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400 flex items-center gap-3">
          <HardDrive size={32} className="text-blue-400" />
          Memory Engine
        </h1>
        <div className="flex gap-2">
          <button 
            onClick={() => setActiveTab('timeline')}
            className={`px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-colors ${activeTab === 'timeline' ? 'bg-blue-600 text-white' : 'bg-black/40 text-white/50 hover:bg-white/10'}`}
          >
            <Clock size={16} /> Timeline
          </button>
          <button 
            onClick={() => setActiveTab('graph')}
            className={`px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-colors ${activeTab === 'graph' ? 'bg-indigo-600 text-white' : 'bg-black/40 text-white/50 hover:bg-white/10'}`}
          >
            <Network size={16} /> Semantic Graph
          </button>
        </div>
      </div>

      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" size={16} />
          <input 
            type="text" 
            placeholder="Search memories..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-black/40 border border-white/10 rounded-lg pl-9 pr-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500/50"
          />
        </div>
        <select 
          value={selectedType} 
          onChange={(e) => setSelectedType(e.target.value)}
          className="bg-black/40 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500/50"
        >
          {types.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <select 
          value={selectedImportance} 
          onChange={(e) => setSelectedImportance(e.target.value)}
          className="bg-black/40 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500/50"
        >
          {importances.map(i => <option key={i} value={i}>{i}</option>)}
        </select>
        <button className="bg-black/40 hover:bg-white/10 border border-white/10 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors text-sm font-bold">
          <Download size={16} /> Export
        </button>
      </div>

      <div className="flex-1 min-h-0 glass-panel overflow-hidden relative">
        {activeTab === 'timeline' ? (
          <div className="h-full overflow-y-auto custom-scrollbar p-6 space-y-4">
            {filteredMemories.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-white/30">
                <BrainCircuit size={48} className="mb-4 opacity-50" />
                <p>No memories found. AGNIV is still observing.</p>
              </div>
            ) : (
              filteredMemories.map((m, i) => (
                <div key={i} className="bg-black/40 border border-white/5 rounded-xl p-5 hover:bg-white/5 transition-colors group">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold text-lg text-white">{m.title}</h3>
                    <div className="flex items-center gap-2">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getImportanceColor(m.importance)}`}>
                        {m.importance}
                      </span>
                      <button onClick={() => handleDelete(m.id)} className="text-white/20 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                  
                  <p className="text-sm text-white/70 mb-4">{m.summary}</p>
                  
                  <div className="flex flex-wrap gap-4 text-xs">
                    <div className="flex items-center gap-1 text-white/40">
                      <Clock size={14} /> 
                      {new Date(m.timestamp * 1000).toLocaleString()}
                    </div>
                    
                    <div className="flex items-center gap-1 text-white/40">
                      <Filter size={14} /> 
                      {m.type}
                    </div>

                    {(m.related_skills.length > 0 || m.related_workflows.length > 0) && (
                      <div className="flex gap-2 ml-auto">
                        {m.related_skills.map((s: string, j: number) => (
                          <span key={j} className="text-blue-300 bg-blue-500/10 px-2 py-0.5 rounded font-mono">Skill: {s}</span>
                        ))}
                        {m.related_workflows.map((w: string, j: number) => (
                          <span key={j} className="text-emerald-300 bg-emerald-500/10 px-2 py-0.5 rounded font-mono">Workflow: {w}</span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          <div className="w-full h-full bg-black/50">
            {graphData.nodes.length > 0 ? (
              <ForceGraph2D
                ref={graphRef}
                graphData={graphData}
                nodeLabel="name"
                nodeColor="color"
                linkColor={() => 'rgba(255,255,255,0.1)'}
                nodeRelSize={6}
                width={800}
                height={600}
                cooldownTicks={100}
                onEngineStop={() => {
                  if (graphRef.current) {
                    graphRef.current.zoomToFit(400);
                  }
                }}
              />
            ) : (
               <div className="h-full flex items-center justify-center text-white/30">
                 No connections to graph yet.
               </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
