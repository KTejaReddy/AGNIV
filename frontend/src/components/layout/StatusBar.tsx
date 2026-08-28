import React, { useEffect, useState } from 'react';
import { wsService } from '../../services/websocket';
import { useSettingsStore } from '../../store/settingsStore';

export const StatusBar: React.FC = () => {
  const [wsConnected, setWsConnected] = useState(wsService.isConnected);
  const isLoading = useSettingsStore(state => state.isLoading);

  useEffect(() => {
    wsService.connect();
    const unsub = wsService.subscribe((data) => {
      try {
        const parsed = JSON.parse(data);
        if (parsed.type === 'WS_STATUS') {
          setWsConnected(parsed.connected);
        }
      } catch (e) {
        // ignore
      }
    });

    return () => unsub();
  }, []);

  return (
    <footer className="h-8 shrink-0 border-t border-white/5 bg-[#0a0a0c]/80 flex items-center px-4 text-xs z-20 justify-between">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]'}`} />
          <span className="text-white/60">{wsConnected ? 'Engine Connected' : 'Engine Disconnected'}</span>
        </div>
      </div>
      <div>
        <span className="text-white/40">{isLoading ? 'Loading...' : 'Ready'}</span>
      </div>
    </footer>
  );
};
