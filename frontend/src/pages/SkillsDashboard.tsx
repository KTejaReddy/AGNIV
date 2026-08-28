import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Box, Play, AlertTriangle, Book, Search, Layers, Cpu, Code, Zap, FileText } from 'lucide-react';

export const SkillsDashboard: React.FC = () => {
  const [skills, setSkills] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [selectedSkill, setSelectedSkill] = useState<any>(null);

  const fetchSkills = async () => {
    try {
      const data = await api.getSkills();
      setSkills(data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleRun = async (skillId: string) => {
    try {
      await api.runSkill(skillId);
      alert('Skill executed (check Workflow/Action logs)');
    } catch (e: any) {
      alert(`Error: ${e.message || 'Execution failed'}`);
    }
  };

  const handleToggle = async (skill: any) => {
    try {
      if (skill.is_enabled) {
        await api.disableSkill(skill.id);
      } else {
        await api.enableSkill(skill.id);
      }
      fetchSkills();
      if (selectedSkill?.id === skill.id) {
        setSelectedSkill({ ...skill, is_enabled: !skill.is_enabled });
      }
    } catch (e) {
      console.error(e);
    }
  };

  const categories = ['ALL', ...Array.from(new Set(skills.map(s => s.category)))];

  const filteredSkills = skills.filter(s => {
    if (selectedCategory !== 'ALL' && s.category !== selectedCategory) return false;
    if (searchQuery && !s.name.toLowerCase().includes(searchQuery.toLowerCase()) && !s.description.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  const getIcon = (iconName: string) => {
    switch(iconName) {
      case 'monitor': return <Monitor size={24} />;
      case 'globe': return <Globe size={24} />;
      case 'cpu': return <Cpu size={24} />;
      case 'folder': return <Folder size={24} />;
      case 'clipboard': return <Clipboard size={24} />;
      default: return <Box size={24} />;
    }
  };
  
  // Dummy icon components just to avoid importing all from lucide if not needed
  const Monitor = ({size}: any) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>;
  const Globe = ({size}: any) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>;
  const Folder = ({size}: any) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>;
  const Clipboard = ({size}: any) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>;

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400 flex items-center gap-3">
          <Zap size={32} className="text-purple-400" />
          Skills Engine
        </h1>
        <div className="text-sm font-medium text-white/50 bg-black/40 px-4 py-2 rounded-full border border-white/10">
           {skills.length} Installed Skills
        </div>
      </div>

      <div className="grid grid-cols-4 gap-6 flex-1 min-h-0">
        
        {/* Left Column: List & Filters */}
        <div className="flex flex-col gap-6 col-span-2 min-h-0">
          <div className="glass-panel p-4 flex flex-col h-full">
            
            <div className="flex gap-4 mb-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" size={16} />
                <input 
                  type="text" 
                  placeholder="Search skills..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-black/40 border border-white/10 rounded-lg pl-9 pr-4 py-2 text-sm text-white focus:outline-none focus:border-purple-500/50"
                />
              </div>
            </div>
            
            <div className="flex gap-2 overflow-x-auto pb-2 custom-scrollbar mb-2">
              {categories.map((cat, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-3 py-1 rounded-full text-xs font-bold whitespace-nowrap transition-colors ${selectedCategory === cat ? 'bg-purple-500/30 text-purple-300 border border-purple-500/50' : 'bg-black/40 text-white/50 border border-white/10 hover:bg-white/10'}`}
                >
                  {cat}
                </button>
              ))}
            </div>

            <div className="flex-1 overflow-y-auto custom-scrollbar space-y-3 mt-2 pr-2">
               {filteredSkills.map((s, i) => (
                 <div 
                  key={i} 
                  onClick={() => setSelectedSkill(s)}
                  className={`bg-white/5 hover:bg-white/10 p-4 rounded-xl border cursor-pointer transition-all ${selectedSkill?.id === s.id ? 'border-purple-500/50 bg-purple-500/10' : 'border-white/5'}`}
                 >
                   <div className="flex items-start gap-4">
                     <div className={`p-3 rounded-lg ${s.is_enabled ? 'bg-purple-500/20 text-purple-400' : 'bg-slate-500/20 text-slate-400'}`}>
                        {getIcon(s.icon)}
                     </div>
                     <div className="flex-1 min-w-0">
                       <div className="flex justify-between items-start mb-1">
                         <h3 className={`font-bold truncate ${s.is_enabled ? 'text-white' : 'text-white/40'}`}>{s.name}</h3>
                         <div className="text-[10px] px-2 py-0.5 rounded-full bg-black/40 text-white/50">{s.category}</div>
                       </div>
                       <p className="text-xs text-white/50 line-clamp-2">{s.description}</p>
                       <div className="flex gap-2 mt-3">
                         {s.tags.map((t: string, j: number) => (
                           <span key={j} className="text-[9px] uppercase tracking-wider text-purple-300/60 bg-purple-500/10 px-1.5 py-0.5 rounded">#{t}</span>
                         ))}
                       </div>
                     </div>
                   </div>
                 </div>
               ))}
               {filteredSkills.length === 0 && (
                 <div className="h-32 flex items-center justify-center text-white/30 text-sm italic">
                   No skills found.
                 </div>
               )}
            </div>
          </div>
        </div>

        {/* Right Column: Skill Details */}
        <div className="col-span-2 min-h-0">
          <div className="glass-panel p-6 h-full overflow-y-auto custom-scrollbar">
            {selectedSkill ? (
              <div className="space-y-6 flex flex-col h-full">
                <div className="flex items-start gap-4 pb-6 border-b border-white/10">
                   <div className={`p-4 rounded-2xl ${selectedSkill.is_enabled ? 'bg-purple-500/20 text-purple-400' : 'bg-slate-500/20 text-slate-400'}`}>
                      {getIcon(selectedSkill.icon)}
                   </div>
                   <div className="flex-1">
                     <h2 className="text-2xl font-bold text-white mb-1">{selectedSkill.name}</h2>
                     <div className="flex gap-3 text-xs text-white/40 mb-3">
                       <span>v{selectedSkill.version}</span>
                       <span>•</span>
                       <span>By {selectedSkill.author}</span>
                       <span>•</span>
                       <span className="font-mono">{selectedSkill.id}</span>
                     </div>
                     <p className="text-sm text-white/70">{selectedSkill.description}</p>
                   </div>
                </div>

                <div className="flex gap-3">
                  <button 
                    onClick={() => handleRun(selectedSkill.id)}
                    disabled={!selectedSkill.is_enabled}
                    className="flex-1 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 disabled:hover:bg-purple-600 text-white font-bold py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
                  >
                    <Play size={18} /> Run Skill
                  </button>
                  <button 
                    onClick={() => handleToggle(selectedSkill)}
                    className="px-6 py-3 rounded-lg border border-white/10 hover:bg-white/5 font-bold text-sm transition-colors"
                  >
                    {selectedSkill.is_enabled ? 'Disable' : 'Enable'}
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-black/30 p-4 rounded-xl border border-white/5">
                    <h4 className="text-xs font-bold text-white/40 uppercase tracking-wider mb-3 flex items-center gap-2">
                      <Layers size={14} /> Required Capabilities
                    </h4>
                    {selectedSkill.required_capabilities.length > 0 ? (
                      <div className="space-y-2">
                        {selectedSkill.required_capabilities.map((c: string, i: number) => (
                          <div key={i} className="text-xs font-mono text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded inline-block mr-2 mb-2">
                            {c}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-xs text-white/30 italic">None required</div>
                    )}
                  </div>
                  
                  <div className="bg-black/30 p-4 rounded-xl border border-white/5">
                    <h4 className="text-xs font-bold text-white/40 uppercase tracking-wider mb-3 flex items-center gap-2">
                      <Code size={14} /> Required Workflows
                    </h4>
                    {selectedSkill.required_workflows.length > 0 ? (
                      <div className="space-y-2">
                        {selectedSkill.required_workflows.map((w: string, i: number) => (
                          <div key={i} className="text-xs font-mono text-blue-400 bg-blue-400/10 px-2 py-1 rounded inline-block mr-2 mb-2">
                            {w}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-xs text-white/30 italic">None required</div>
                    )}
                  </div>
                </div>
                
                <div className="flex-1"></div>
                
                {!selectedSkill.is_enabled && (
                  <div className="bg-orange-500/10 border border-orange-500/20 text-orange-400 p-4 rounded-lg flex items-start gap-3 text-sm">
                    <AlertTriangle size={18} className="shrink-0 mt-0.5" />
                    <div>
                      <strong className="block mb-1">Skill is disabled</strong>
                      This skill has been disabled and cannot be executed by the Cognitive Engine or manually.
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-white/20 space-y-4">
                <Box size={48} className="opacity-50" />
                <span className="text-sm font-medium">Select a skill to view details</span>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};
