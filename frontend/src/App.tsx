import React from 'react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { AppShell } from './components/layout/AppShell';
import { Diagnostics } from './pages/Diagnostics';
import { Memory } from './pages/Memory';
import { Plugins } from './pages/Plugins';
import { Logs } from './pages/Logs';
import { Settings } from './pages/Settings';
import { CoreEngine } from './pages/CoreEngine';
import { DesktopControl } from './pages/DesktopControl';
import { VoiceControl } from './pages/VoiceControl';
import { PerceptionControl } from './pages/PerceptionControl';
import { ScreenIntelligenceControl } from './pages/ScreenIntelligenceControl';
import { CognitiveControl } from './pages/CognitiveControl';
import { InteractionControl } from './pages/InteractionControl';
import { KnowledgeDashboard } from './pages/KnowledgeDashboard';
import { WorkflowDashboard } from './pages/WorkflowDashboard';
import { SkillsDashboard } from './pages/SkillsDashboard';
import { MemoryDashboard } from './pages/MemoryDashboard';
import { AdaptiveDashboard } from './pages/AdaptiveDashboard';
import { AccessibilityDashboard } from './pages/AccessibilityDashboard';
import { ExtensionsDashboard } from './pages/ExtensionsDashboard';

import { ProviderSettings } from './pages/ProviderSettings';

import { Home } from './pages/Home';
import { useRuntimeStore } from './store/useRuntimeStore';
import { useEffect } from 'react';

function App() {
  const { setCoreState, addTimelineEvent } = useRuntimeStore();

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      addTimelineEvent('System initialized successfully');
      addTimelineEvent('Living Runtime connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'CORE_EVENT') {
          const payload = data.event;
          
          if (payload.type === 'RUNTIME_STATE_CHANGE') {
            useRuntimeStore.getState().setCoreState(payload.payload.state);
          } else if (payload.type === 'TELEMETRY_UPDATE') {
            useRuntimeStore.getState().updateTelemetry(payload.payload);
          } else if (payload.type === 'DEBUG_OVERLAY_UPDATE') {
            useRuntimeStore.getState().updateDebugState(payload.payload);
          } else {
            // Log general events to timeline
            useRuntimeStore.getState().addTimelineEvent(`[${payload.source}] ${payload.type}`);
          }
        }
      } catch (e) {
        console.error('WS parse error', e);
      }
    };

    ws.onerror = () => {
      setCoreState('error');
      addTimelineEvent('Connection to core lost');
    };

    return () => {
      if (ws.readyState === 1) {
        ws.close();
      }
    };
  }, [setCoreState, addTimelineEvent]);

  return (
    <MemoryRouter>
      <Routes>
        <Route path="/" element={<AppShell />}>
          <Route index element={<Home />} />
          <Route path="diagnostics" element={<Diagnostics />} />
          <Route path="core" element={<CoreEngine />} />
          <Route path="desktop" element={<DesktopControl />} />
          <Route path="voice" element={<VoiceControl />} />
          <Route path="perception" element={<PerceptionControl />} />
          <Route path="screen" element={<ScreenIntelligenceControl />} />
          <Route path="cognitive" element={<CognitiveControl />} />
          <Route path="interaction" element={<InteractionControl />} />
          <Route path="knowledge" element={<KnowledgeDashboard />} />
          <Route path="workflow" element={<WorkflowDashboard />} />
          <Route path="skills" element={<SkillsDashboard />} />
          <Route path="memory" element={<MemoryDashboard />} />
          <Route path="adaptive" element={<AdaptiveDashboard />} />
          <Route path="accessibility" element={<AccessibilityDashboard />} />
          <Route path="plugins" element={<ExtensionsDashboard />} />
          <Route path="logs" element={<Logs />} />
          <Route path="settings/provider" element={<ProviderSettings />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </MemoryRouter>
  );
}

export default App;
