import React from 'react';
import { useRuntimeStore } from '../store/useRuntimeStore';
import '../styles/debug-overlay.css';

export const DebugOverlay: React.FC = () => {
  const { debugState, coreState, telemetry } = useRuntimeStore();

  // Only render in dev mode
  if (!import.meta.env.DEV) {
    return null;
  }

  // Early return if debugState hasn't populated yet
  if (!debugState) {
    return (
      <div className="debug-overlay">
        <h3>Runtime Debug Overlay (Dev Mode)</h3>
        <p>Waiting for backend connection...</p>
      </div>
    );
  }

  return (
    <div className="debug-overlay">
      <h3>Runtime Debug Overlay</h3>
      
      <div className="debug-section">
        <h4>System & UI</h4>
        <div>Core State: <span>{coreState}</span></div>
        <div>Telemetry: <span>Spd:{telemetry.handSpeed.toFixed(1)} Dist:{telemetry.distance.toFixed(1)} Vol:{telemetry.voiceVolume.toFixed(1)}</span></div>
        <div>Living Runtime: <span>{debugState.runtime?.status || 'Unknown'} (Presence: {debugState.runtime?.presence || 'Unknown'})</span></div>
        <div>Last Event: <span>{debugState.runtime?.last_event?.type || 'None'}</span></div>
      </div>

      <div className="debug-section">
        <h4>Perception (Phase G)</h4>
        <div>Camera Connected: <span>{debugState.perception?.camera_connected ? 'Yes' : 'No'}</span></div>
        <div>Current FPS: <span>{debugState.perception?.fps || 0}</span></div>
        <div>Hand Landmarks: <span>{debugState.perception?.hand_landmarks ? 'Detected' : 'None'}</span></div>
        <div>Face Landmarks: <span>{debugState.perception?.face_landmarks ? 'Detected' : 'None'}</span></div>
        <div>Body Landmarks: <span>{debugState.perception?.body_landmarks ? 'Detected' : 'None'}</span></div>
        <div>Current Gesture: <span>{debugState.perception?.current_gesture || 'None'}</span></div>
      </div>

      <div className="debug-section">
        <h4>Voice (Phase F)</h4>
        <div>Voice State: <span>{debugState.voice?.state || 'Idle'}</span></div>
        <div>Wake Word: <span>{debugState.voice?.wake_word ? 'Detected' : 'None'}</span></div>
      </div>

      <div className="debug-section">
        <h4>Cognitive (Phase E)</h4>
        <div>Groq Status: <span>{debugState.cognitive?.groq_status || 'Unknown'}</span></div>
      </div>

      <div className="debug-section">
        <h4>Screen (Phase H)</h4>
        <div>Capture State: <span>{debugState.screen?.capture_state ? 'Active' : 'Inactive'}</span></div>
      </div>

      <div className="debug-section">
        <h4>Other Subsystems</h4>
        <div>Workflow: <span>{debugState.systems?.workflow || 'None'}</span></div>
        <div>Skill: <span>{debugState.systems?.skill || 'None'}</span></div>
        <div>Memory: <span>{debugState.systems?.memory || 'None'}</span></div>
        <div>Desktop: <span>{debugState.systems?.desktop || 'None'}</span></div>
      </div>
    </div>
  );
};
