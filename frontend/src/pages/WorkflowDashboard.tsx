import React, { useEffect, useState, useRef } from 'react';
import { api } from '../services/api';
import { Play, Pause, Square, ListTree, CheckCircle2, XCircle, Clock, AlertCircle } from 'lucide-react';
import ForceGraph2D from 'react-force-graph-2d';

export const WorkflowDashboard: React.FC = () => {
  const [workflows, setWorkflows] = useState<{active: any[], queued: any[]}>({ active: [], queued: [] });
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedInstance, setSelectedInstance] = useState<any>(null);
  const graphRef = useRef<any>();

  const fetchData = async () => {
    try {
      const wfs = await api.getWorkflows();
      setWorkflows(wfs);
      const tpls = await api.getTemplates();
      setTemplates(tpls);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleRun = async (templateId: string) => {
    await api.runWorkflow(templateId);
    fetchData();
  };

  const handlePause = async (instanceId: string) => {
    await api.pauseWorkflow(instanceId);
    fetchData();
  };

  const handleResume = async (instanceId: string) => {
    await api.resumeWorkflow(instanceId);
    fetchData();
  };

  const handleCancel = async (instanceId: string) => {
    await api.cancelWorkflow(instanceId);
    fetchData();
  };

  const activeWorkflow = selectedInstance || workflows.active[0] || workflows.queued[0];

  // Build Graph Data
  const getGraphData = () => {
    if (!activeWorkflow) return { nodes: [], links: [] };
    const nodes = activeWorkflow.steps.map((s: any) => ({
      id: s.id,
      name: s.capability,
      state: s.state
    }));
    
    const links: any[] = [];
    activeWorkflow.steps.forEach((s: any) => {
      s.depends_on.forEach((dep: string) => {
        links.push({ source: dep, target: s.id });
      });
      // Also sequential links if no explicit dependency
      if (s.depends_on.length === 0) {
        const idx = activeWorkflow.steps.findIndex((x: any) => x.id === s.id);
        if (idx > 0) {
          links.push({ source: activeWorkflow.steps[idx - 1].id, target: s.id });
        }
      }
    });
    
    return { nodes, links };
  };

  const getNodeColor = (state: string) => {
    switch(state) {
      case 'COMPLETED': return '#10b981';
      case 'RUNNING': return '#3b82f6';
      case 'FAILED': return '#ef4444';
      default: return '#64748b';
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400 flex items-center gap-3">
          <ListTree size={32} className="text-blue-400" />
          Workflow Engine
        </h1>
      </div>

      <div className="grid grid-cols-4 gap-6 flex-1 min-h-0">
        
        {/* Left Column: Templates & Queue */}
        <div className="flex flex-col gap-6 col-span-1 min-h-0">
          
          <div className="glass-panel p-4 flex flex-col min-h-0 h-1/2">
            <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4">Templates</h2>
            <div className="flex-1 overflow-y-auto custom-scrollbar space-y-2">
               {templates.map((tpl, i) => (
                 <div key={i} className="bg-white/5 p-3 rounded border border-white/5">
                   <div className="flex justify-between items-start mb-1">
                     <div className="text-xs font-bold text-blue-400">{tpl.name}</div>
                     <button onClick={() => handleRun(tpl.id)} className="bg-blue-500/20 text-blue-400 hover:bg-blue-500/40 px-2 py-1 rounded text-[10px] font-bold transition-colors">
                       RUN
                     </button>
                   </div>
                   <div className="text-[10px] text-white/60 mb-2">{tpl.description}</div>
                   <div className="flex gap-1 flex-wrap">
                      {tpl.steps.map((s: any, j: number) => (
                        <div key={j} className="text-[8px] bg-black/40 px-1 py-0.5 rounded text-white/40">{s.capability}</div>
                      ))}
                   </div>
                 </div>
               ))}
            </div>
          </div>

          <div className="glass-panel p-4 flex-1 overflow-y-auto custom-scrollbar">
            <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4">Active & Queued</h2>
            <div className="space-y-2">
              {workflows.active.map((w, i) => (
                <div key={i} onClick={() => setSelectedInstance(w)} className={`bg-white/5 hover:bg-white/10 p-3 rounded border cursor-pointer transition-colors ${activeWorkflow?.instance_id === w.instance_id ? 'border-blue-500/50' : 'border-white/5'}`}>
                   <div className="flex justify-between items-center mb-2">
                     <div className="text-xs font-bold text-white">{w.name}</div>
                     <div className="text-[10px] bg-blue-500/20 text-blue-400 px-1.5 py-0.5 rounded animate-pulse">{w.state}</div>
                   </div>
                   
                   <div className="w-full bg-black/50 rounded-full h-1.5 mb-2 overflow-hidden">
                      <div className="bg-blue-500 h-1.5 rounded-full transition-all duration-300" style={{ width: `${w.progress}%` }}></div>
                   </div>
                   
                   <div className="flex gap-2 justify-end">
                      {w.state === 'RUNNING' && <button onClick={(e) => { e.stopPropagation(); handlePause(w.instance_id); }} className="text-white/40 hover:text-orange-400"><Pause size={12} /></button>}
                      {w.state === 'PAUSED' && <button onClick={(e) => { e.stopPropagation(); handleResume(w.instance_id); }} className="text-white/40 hover:text-emerald-400"><Play size={12} /></button>}
                      <button onClick={(e) => { e.stopPropagation(); handleCancel(w.instance_id); }} className="text-white/40 hover:text-red-400"><Square size={12} /></button>
                   </div>
                </div>
              ))}
              {workflows.queued.map((w, i) => (
                <div key={`q-${i}`} className="bg-white/5 p-3 rounded border border-white/5 opacity-50">
                   <div className="flex justify-between items-center">
                     <div className="text-xs font-bold text-white">{w.name}</div>
                     <div className="text-[10px] bg-white/10 text-white/50 px-1.5 py-0.5 rounded">QUEUED</div>
                   </div>
                </div>
              ))}
              {workflows.active.length === 0 && workflows.queued.length === 0 && (
                <div className="text-xs text-white/30 italic text-center py-4">No workflows running</div>
              )}
            </div>
          </div>
          
        </div>

        {/* Right Column: Interactive Graph & Details */}
        <div className="col-span-3 flex flex-col gap-6 min-h-0">
            
            <div className="glass-panel flex-1 relative overflow-hidden group border border-white/10 flex flex-col">
               <div className="absolute top-4 left-4 z-10 flex flex-col gap-1">
                 <div className="text-sm font-bold text-white">{activeWorkflow?.name || 'Execution Graph'}</div>
                 {activeWorkflow && (
                   <div className="text-xs text-white/50">{activeWorkflow.instance_id}</div>
                 )}
               </div>
               
               <div className="flex-1">
                 {activeWorkflow ? (
                   <ForceGraph2D
                      ref={graphRef}
                      graphData={getGraphData()}
                      width={800} 
                      height={400}
                      nodeLabel="name"
                      nodeColor={(node: any) => getNodeColor(node.state)}
                      nodeRelSize={6}
                      linkColor={() => 'rgba(255,255,255,0.1)'}
                      linkDirectionalArrowLength={3.5}
                      linkDirectionalArrowRelPos={1}
                      backgroundColor="#00000000"
                   />
                 ) : (
                   <div className="h-full flex items-center justify-center text-white/30 text-sm">
                      Select or Run a Workflow to view Execution Graph
                   </div>
                 )}
               </div>
               
               <div className="absolute bottom-4 left-4 flex gap-4 bg-black/60 p-3 rounded-lg border border-white/10 backdrop-blur-md">
                 <div className="flex items-center gap-2 text-xs"><div className="w-2 h-2 rounded-full bg-slate-500"/> Pending</div>
                 <div className="flex items-center gap-2 text-xs"><div className="w-2 h-2 rounded-full bg-blue-500"/> Running</div>
                 <div className="flex items-center gap-2 text-xs"><div className="w-2 h-2 rounded-full bg-emerald-500"/> Completed</div>
                 <div className="flex items-center gap-2 text-xs"><div className="w-2 h-2 rounded-full bg-red-500"/> Failed</div>
               </div>
            </div>

            <div className="glass-panel h-48 p-4 overflow-y-auto custom-scrollbar">
               <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4">Step Execution Log</h2>
               <div className="space-y-2">
                 {activeWorkflow?.steps.map((s: any, i: number) => (
                    <div key={i} className="flex items-start gap-3 bg-black/20 p-2 rounded border border-white/5">
                      <div className="mt-0.5">
                        {s.state === 'COMPLETED' && <CheckCircle2 size={14} className="text-emerald-400" />}
                        {s.state === 'RUNNING' && <Clock size={14} className="text-blue-400 animate-spin" />}
                        {s.state === 'FAILED' && <XCircle size={14} className="text-red-400" />}
                        {s.state === 'PENDING' && <AlertCircle size={14} className="text-slate-500" />}
                      </div>
                      <div className="flex-1">
                        <div className="flex justify-between">
                           <div className="text-xs font-bold text-white">{s.capability}</div>
                           <div className="text-[10px] text-white/30 font-mono">{s.id}</div>
                        </div>
                        <div className="text-[10px] text-white/50 mt-1">
                          Params: {JSON.stringify(s.parameters)}
                        </div>
                        {s.error && (
                          <div className="text-[10px] text-red-400 mt-1">Error: {s.error}</div>
                        )}
                        {s.result && (
                          <div className="text-[10px] text-emerald-400 mt-1">Result: {JSON.stringify(s.result)}</div>
                        )}
                      </div>
                    </div>
                 ))}
                 {!activeWorkflow && (
                   <div className="text-xs text-white/30 italic text-center">No active workflow</div>
                 )}
               </div>
            </div>
            
        </div>

      </div>
    </div>
  );
};
