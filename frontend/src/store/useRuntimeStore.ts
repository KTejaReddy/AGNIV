import { create } from 'zustand';

export type CoreState = 'idle' | 'listening' | 'transcribing' | 'thinking' | 'planning' | 'executing' | 'speaking' | 'sleeping' | 'error';

export interface TelemetryData {
  distance: number;
  handSpeed: number;
  voiceVolume: number;
  headRotation?: { x: number; y: number; z: number };
}

export interface DebugState {
  sessionId?: string;
  currentPlan?: any;
  currentCapability?: string;
  currentStep?: number;
  lastGroqLatency?: number;
  conversationHistoryLength?: number;
  contextSize?: number;
  lastEvent?: string;
}

interface RuntimeState {
  coreState: CoreState;
  timeline: { time: string; text: string }[];
  telemetry: TelemetryData;
  debugState: DebugState | null;
  setCoreState: (state: CoreState) => void;
  addTimelineEvent: (text: string) => void;
  updateTelemetry: (data: Partial<TelemetryData>) => void;
  updateDebugState: (data: any) => void;
}

export const useRuntimeStore = create<RuntimeState>((set) => ({
  coreState: 'idle',
  timeline: [],
  debugState: null,
  telemetry: {
    distance: 50,
    handSpeed: 0,
    voiceVolume: 0,
    headRotation: { x: 0, y: 0, z: 0 }
  },
  setCoreState: (state) => set({ coreState: state }),
  addTimelineEvent: (text) => set((state) => ({
    timeline: [{ time: new Date().toLocaleTimeString(), text }, ...state.timeline].slice(0, 50)
  })),
  updateTelemetry: (data) => set((state) => ({
    telemetry: { ...state.telemetry, ...data }
  })),
  updateDebugState: (data) => set({ debugState: data })
}));
