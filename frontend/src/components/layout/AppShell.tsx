import React from 'react';
import { Sidebar } from './Sidebar';
import { TopHeader } from './TopHeader';
import { StatusBar } from './StatusBar';
import { Outlet } from 'react-router-dom';
import { CommandPalette } from '../CommandPalette';
import { Overlays } from '../Overlays';
import { DebugOverlay } from '../DebugOverlay';
import { useSettingsStore } from '../../store/settingsStore';

export const AppShell: React.FC = () => {
  const { developerMode } = useSettingsStore();

  return (
    <div className={`flex h-screen w-screen overflow-hidden text-white selection:bg-white/30 font-sans ${developerMode ? 'bg-[#0A0A0C]' : 'bg-transparent'}`}>
      {developerMode && (
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 via-purple-500/5 to-transparent pointer-events-none" />
      )}
      
      <CommandPalette />
      <Overlays />
      <DebugOverlay />

      {developerMode && <Sidebar />}
      
      <div className="flex flex-col flex-1 z-10 w-full h-full relative">
        {developerMode && <TopHeader />}
        
        <main className={`flex-1 overflow-y-auto relative ${developerMode ? 'p-6' : 'p-0 w-full h-full'}`}>
          <Outlet />
        </main>
        
        {developerMode && <StatusBar />}
      </div>
    </div>
  );
};
