import React, { useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Cpu, LayoutDashboard, MonitorSmartphone, Mic, 
  Eye, MonitorPlay, Brain, MessageSquare, BookOpen, 
  Workflow, Wrench, Database, Sparkles, Accessibility, 
  Puzzle, FileText, Settings, Activity,
  Home, Monitor, Users, ListTree, Zap, HardDrive, 
  ActivitySquare, Blocks, CheckSquare, Search
} from 'lucide-react';
import { useSettingsStore } from '../../store/settingsStore';

export const Sidebar: React.FC = () => {
  const { developerMode, loadSettings } = useSettingsStore();

  useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  const coreLinks = [
    { to: '/', icon: Home, label: 'AI Core' },
    { to: '/settings/provider', icon: Cpu, label: 'Provider Config' },
    { to: '/settings', icon: Settings, label: 'Settings' },
  ];

  const devLinks = [
    { to: '/diagnostics', icon: Activity, label: 'Diagnostics' },
    { to: '/core', icon: Cpu, label: 'Core Engine' },
    { to: '/desktop', icon: Monitor, label: 'Desktop Control' },
    { to: '/voice', icon: Mic, label: 'Voice Engine' },
    { to: '/perception', icon: Eye, label: 'Perception Engine' },
    { to: '/screen', icon: Monitor, label: 'Screen Intelligence' },
    { to: '/cognitive', icon: Brain, label: 'Cognitive Engine' },
    { to: '/interaction', icon: Users, label: 'Human Interaction' },
    { to: '/knowledge', icon: Database, label: 'Knowledge Engine' },
    { to: '/workflow', icon: ListTree, label: 'Workflow Engine' },
    { to: '/skills', icon: Zap, label: 'Skills Engine' },
    { to: '/memory', icon: HardDrive, label: 'Memory' },
    { to: '/adaptive', icon: Brain, label: 'Adaptive Engine' },
    { to: '/accessibility', icon: ActivitySquare, label: 'Accessibility Suite' },
    { to: '/plugins', icon: Blocks, label: 'Extensions SDK' },
    { to: '/logs', icon: Activity, label: 'Logs' },
  ];

  const links = developerMode ? [...coreLinks, ...devLinks] : coreLinks;

  return (
    <aside className="w-64 glass z-20 flex flex-col pt-8 pb-4">
      <div className="px-6 mb-8 flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 shadow-lg pulse-glow" />
        <h1 className="text-xl font-bold tracking-wide">AGNIV</h1>
      </div>
      
      <nav className="flex-1 px-4 space-y-1 overflow-y-auto">
        {links.map(link => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => 
              `flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-300 ${
                isActive 
                  ? 'bg-white/10 text-white shadow-md' 
                  : 'text-white/60 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <link.icon size={18} />
            <span className="font-medium text-sm">{link.label}</span>
          </NavLink>
        ))}
      </nav>

      {developerMode && (
        <div className="px-4 pt-4 mt-auto border-t border-white/5">
          <div className="text-xs text-orange-400 font-medium px-2 uppercase tracking-widest text-center">
            Developer Mode Active
          </div>
        </div>
      )}
    </aside>
  );
};
