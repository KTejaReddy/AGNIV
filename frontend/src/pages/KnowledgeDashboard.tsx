import React, { useEffect, useState, useRef, useCallback } from 'react';
import { api } from '../services/api';
import { Search, Database, Share2, Info, ChevronRight, Layers } from 'lucide-react';
import ForceGraph2D from 'react-force-graph-2d';

export const KnowledgeDashboard: React.FC = () => {
  const [graphData, setGraphData] = useState<{nodes: any[], links: any[]}>({ nodes: [], links: [] });
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  
  const graphRef = useRef<any>();

  const fetchGraph = async () => {
    try {
      const data = await api.getKnowledgeGraph();
      setGraphData(data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchGraph();
    // In a real app we might poll or listen to websockets, for now just load once
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }
    try {
      const results = await api.searchKnowledge(searchQuery);
      setSearchResults(results);
    } catch (e) {
      console.error(e);
    }
  };

  const handleNodeClick = useCallback((node: any) => {
    setSelectedNode(node);
    // Center graph on node
    if (graphRef.current) {
      graphRef.current.centerAt(node.x, node.y, 1000);
      graphRef.current.zoom(4, 2000);
    }
  }, [graphRef]);

  // Render nodes based on category
  const getNodeColor = (type: string) => {
    switch (type) {
      case 'SYSTEM': return '#f97316'; // orange
      case 'CATEGORY': return '#3b82f6'; // blue
      case 'CAPABILITY': return '#10b981'; // emerald
      case 'APPLICATION': return '#8b5cf6'; // purple
      default: return '#64748b'; // slate
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-orange-400 to-rose-400 flex items-center gap-3">
          <Database size={32} className="text-orange-400" />
          Knowledge Engine
        </h1>
        <div className="text-sm font-medium text-white/50 bg-black/40 px-4 py-2 rounded-full border border-white/10 flex items-center gap-2">
           <Layers size={16} className="text-emerald-400" />
           {graphData.nodes.length} Nodes
        </div>
      </div>

      <div className="grid grid-cols-4 gap-6 flex-1 min-h-0">
        
        {/* Left Column: Search & Details */}
        <div className="flex flex-col gap-6 col-span-1 min-h-0">
          
          <div className="glass-panel p-4 flex flex-col min-h-0 h-1/2">
            <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Search size={16} /> Search Engine
            </h2>
            <form onSubmit={handleSearch} className="mb-4">
              <input 
                type="text" 
                placeholder="Search knowledge base..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-orange-500/50"
              />
            </form>
            <div className="flex-1 overflow-y-auto custom-scrollbar space-y-2">
               {searchResults.map((res, i) => (
                 <div 
                  key={i} 
                  onClick={() => {
                    const node = graphData.nodes.find(n => n.id === res.id);
                    if (node) handleNodeClick(node);
                  }}
                  className="bg-white/5 hover:bg-white/10 p-3 rounded border border-white/5 cursor-pointer transition-colors"
                 >
                   <div className="text-xs font-bold text-orange-400 mb-1">{res.id}</div>
                   <div className="text-[10px] text-white/60">{res.data.description}</div>
                   <div className="mt-2 text-[8px] bg-black/40 inline-block px-1.5 py-0.5 rounded text-white/40">{res.data.type}</div>
                 </div>
               ))}
               {searchQuery && searchResults.length === 0 && (
                 <div className="text-xs text-white/30 italic text-center p-4">No results found</div>
               )}
            </div>
          </div>

          <div className="glass-panel p-4 flex-1 overflow-y-auto custom-scrollbar">
            <h2 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Info size={16} /> Node Details
            </h2>
            {selectedNode ? (
              <div className="space-y-4">
                <div className="flex items-center gap-3 border-b border-white/10 pb-4">
                  <div className="w-4 h-4 rounded-full" style={{ backgroundColor: getNodeColor(selectedNode.type) }} />
                  <div>
                    <div className="text-lg font-bold text-white leading-tight">{selectedNode.name}</div>
                    <div className="text-xs text-white/50 uppercase font-mono mt-1">{selectedNode.type}</div>
                  </div>
                </div>
                <div>
                  <div className="text-xs font-medium text-white/40 mb-1 uppercase">Description</div>
                  <div className="text-sm text-white/80">{selectedNode.description || 'No description available.'}</div>
                </div>
                
                <div>
                  <div className="text-xs font-medium text-white/40 mb-2 uppercase">Relationships</div>
                  <div className="space-y-1">
                    {graphData.links.filter(l => l.source.id === selectedNode.id || l.source === selectedNode.id).map((l, i) => (
                      <div key={i} className="text-xs flex items-center gap-2 bg-black/30 p-1.5 rounded border border-white/5">
                        <Share2 size={12} className="text-white/30" />
                        <span className="text-orange-400/70">{l.label}</span>
                        <ChevronRight size={10} className="text-white/20" />
                        <span className="text-white/80 font-mono truncate">{l.target.id || l.target}</span>
                      </div>
                    ))}
                    {graphData.links.filter(l => l.target.id === selectedNode.id || l.target === selectedNode.id).map((l, i) => (
                      <div key={`tgt-${i}`} className="text-xs flex items-center gap-2 bg-black/30 p-1.5 rounded border border-white/5">
                        <span className="text-white/80 font-mono truncate">{l.source.id || l.source}</span>
                        <ChevronRight size={10} className="text-white/20" />
                        <span className="text-emerald-400/70">{l.label}</span>
                        <Share2 size={12} className="text-white/30" />
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-white/20 space-y-3">
                <Share2 size={32} />
                <span className="text-xs font-medium">Select a node in the graph</span>
              </div>
            )}
          </div>
          
        </div>

        {/* Right Column: Interactive Graph Visualization */}
        <div className="glass-panel col-span-3 min-h-0 relative overflow-hidden group border border-white/10">
           {graphData.nodes.length > 0 ? (
             <ForceGraph2D
                ref={graphRef}
                graphData={graphData}
                width={800} // Approximate width, ideally would use AutoSizer
                height={600}
                nodeLabel="name"
                nodeColor={(node: any) => getNodeColor(node.type)}
                nodeRelSize={6}
                linkColor={() => 'rgba(255,255,255,0.1)'}
                linkDirectionalArrowLength={3.5}
                linkDirectionalArrowRelPos={1}
                onNodeClick={handleNodeClick}
                backgroundColor="#00000000"
             />
           ) : (
             <div className="absolute inset-0 flex items-center justify-center text-white/30 text-sm">
                Loading Knowledge Graph...
             </div>
           )}
           
           <div className="absolute bottom-4 left-4 flex gap-4 bg-black/60 p-3 rounded-lg border border-white/10 backdrop-blur-md">
             <div className="flex items-center gap-2 text-xs"><div className="w-2 h-2 rounded-full bg-orange-500"/> System</div>
             <div className="flex items-center gap-2 text-xs"><div className="w-2 h-2 rounded-full bg-blue-500"/> Category</div>
             <div className="flex items-center gap-2 text-xs"><div className="w-2 h-2 rounded-full bg-emerald-500"/> Capability</div>
             <div className="flex items-center gap-2 text-xs"><div className="w-2 h-2 rounded-full bg-purple-500"/> Application</div>
           </div>
        </div>

      </div>
    </div>
  );
};
