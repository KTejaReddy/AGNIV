export const API_BASE_URL = 'http://localhost:8000';

export const api = {
  getSystemInfo: async () => {
    const res = await fetch(`${API_BASE_URL}/system`);
    return res.json();
  },
  getSetting: async (key: string) => {
    const res = await fetch(`${API_BASE_URL}/settings/${key}`);
    return res.json();
  },
  setSetting: async (key: string, value: any) => {
    const res = await fetch(`${API_BASE_URL}/settings/${key}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ value }),
    });
    return res.json();
  },
  getLogs: async () => {
    const res = await fetch(`${API_BASE_URL}/logs`);
    return res.json();
  },
  
  // Core Engine endpoints
  getCoreStatus: async () => {
    const res = await fetch(`${API_BASE_URL}/core/status`);
    return res.json();
  },
  verifyDiagnostics: async () => {
    const res = await fetch(`${API_BASE_URL}/core/diagnostics/verify`, { method: 'POST' });
    return res.json();
  },
  getCoreModules: async () => {
    const res = await fetch(`${API_BASE_URL}/core/modules`);
    return res.json();
  },
  getCoreTasks: async () => {
    const res = await fetch(`${API_BASE_URL}/core/tasks`);
    return res.json();
  },
  getCoreCapabilities: async () => {
    const res = await fetch(`${API_BASE_URL}/core/capabilities`);
    return res.json();
  },
  getCorePermissions: async () => {
    const res = await fetch(`${API_BASE_URL}/core/permissions`);
    return res.json();
  },
  getCoreSessions: async () => {
    const res = await fetch(`${API_BASE_URL}/core/sessions`);
    return res.json();
  },
  simulateInput: async (action: string) => {
    const res = await fetch(`${API_BASE_URL}/core/simulate_input`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action }),
    });
    return res.json();
  },

  // Desktop endpoints
  desktopAction: async (category: string, action: string, params: any = {}) => {
    const url = category === 'screenshot' 
      ? `${API_BASE_URL}/desktop/screenshot`
      : `${API_BASE_URL}/desktop/${category}/${action}`;
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    return res.json();
  },

  // Voice endpoints
  getVoiceStatus: async () => {
    const res = await fetch(`${API_BASE_URL}/voice/status`);
    return res.json();
  },
  getVoiceDevices: async () => {
    const res = await fetch(`${API_BASE_URL}/voice/devices`);
    return res.json();
  },
  voiceAction: async (action: string, params: any = {}) => {
    const res = await fetch(`${API_BASE_URL}/voice/action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, parameters: params }),
    });
    return res.json();
  },

  // Perception endpoints
  getPerceptionStatus: async () => {
    const res = await fetch(`${API_BASE_URL}/perception/status`);
    return res.json();
  },
  getPerceptionDevices: async () => {
    const res = await fetch(`${API_BASE_URL}/perception/devices`);
    return res.json();
  },
  perceptionAction: async (action: string, params: any = {}) => {
    const res = await fetch(`${API_BASE_URL}/perception/action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, parameters: params }),
    });
    return res.json();
  },
  // Screen endpoints
  getScreenStatus: async () => {
    const res = await fetch(`${API_BASE_URL}/screen/status`);
    return res.json();
  },
  getScreenMonitors: async () => {
    const res = await fetch(`${API_BASE_URL}/screen/monitors`);
    return res.json();
  },
  screenAction: async (action: string, params: any = {}) => {
    const res = await fetch(`${API_BASE_URL}/screen/action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, parameters: params }),
    });
    return res.json();
  },
  // Cognitive endpoints
  getCognitiveStatus: async () => {
    const res = await fetch(`${API_BASE_URL}/cognitive/status`);
    return res.json();
  },
  getCognitiveContext: async () => {
    const res = await fetch(`${API_BASE_URL}/cognitive/context`);
    return res.json();
  },
  getCognitiveHistory: async () => {
    const res = await fetch(`${API_BASE_URL}/cognitive/history`);
    return res.json();
  },
  getProviderConfig: async () => {
    const res = await fetch(`${API_BASE_URL}/provider/config`);
    return res.json();
  },
  saveProviderConfig: async (config: { api_key?: string; model: string }) => {
    const res = await fetch(`${API_BASE_URL}/provider/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    return res.json();
  },
  testProviderConnection: async () => {
    const res = await fetch(`${API_BASE_URL}/provider/test`, { method: 'POST' });
    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Connection failed');
    }
    return res.json();
  },
  processCognitiveInput: async (text: string) => {
    const res = await fetch(`${API_BASE_URL}/cognitive/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    return res.json();
  },
  // Interaction endpoints
  getInteractionStatus: async () => {
    const res = await fetch(`${API_BASE_URL}/interaction/status`);
    return res.json();
  },
  confirmInteraction: async (accepted: boolean) => {
    const res = await fetch(`${API_BASE_URL}/interaction/confirm`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ accepted }),
    });
    return res.json();
  },
  simulateGesture: async (gesture: string) => {
    const res = await fetch(`${API_BASE_URL}/interaction/simulate_gesture`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gesture }),
    });
    return res.json();
  },
  // Knowledge endpoints
  getKnowledgeGraph: async () => {
    const res = await fetch(`${API_BASE_URL}/knowledge/graph`);
    return res.json();
  },
  searchKnowledge: async (q: string) => {
    const res = await fetch(`${API_BASE_URL}/knowledge/search?q=${encodeURIComponent(q)}`);
    return res.json();
  },
  // Workflow endpoints
  getWorkflows: async () => {
    const res = await fetch(`${API_BASE_URL}/workflow/`);
    return res.json();
  },
  getTemplates: async () => {
    const res = await fetch(`${API_BASE_URL}/workflow/templates`);
    return res.json();
  },
  runWorkflow: async (templateId: string) => {
    const res = await fetch(`${API_BASE_URL}/workflow/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ template_id: templateId }),
    });
    return res.json();
  },
  pauseWorkflow: async (instanceId: string) => {
    const res = await fetch(`${API_BASE_URL}/workflow/${instanceId}/pause`, { method: 'POST' });
    return res.json();
  },
  resumeWorkflow: async (instanceId: string) => {
    const res = await fetch(`${API_BASE_URL}/workflow/${instanceId}/resume`, { method: 'POST' });
    return res.json();
  },
  cancelWorkflow: async (instanceId: string) => {
    const res = await fetch(`${API_BASE_URL}/workflow/${instanceId}/cancel`, { method: 'POST' });
    return res.json();
  },
  // Skills endpoints
  getSkills: async () => {
    const res = await fetch(`${API_BASE_URL}/skills/`);
    return res.json();
  },
  runSkill: async (skillId: string) => {
    const res = await fetch(`${API_BASE_URL}/skills/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skill_id: skillId }),
    });
    return res.json();
  },
  enableSkill: async (skillId: string) => {
    const res = await fetch(`${API_BASE_URL}/skills/${skillId}/enable`, { method: 'POST' });
    return res.json();
  },
  disableSkill: async (skillId: string) => {
    const res = await fetch(`${API_BASE_URL}/skills/${skillId}/disable`, { method: 'POST' });
    return res.json();
  },
  // Memory endpoints
  getMemories: async () => {
    const res = await fetch(`${API_BASE_URL}/memory/`);
    return res.json();
  },
  searchMemories: async (q: string) => {
    const res = await fetch(`${API_BASE_URL}/memory/search?q=${encodeURIComponent(q)}`);
    return res.json();
  },
  deleteMemory: async (memoryId: string) => {
    const res = await fetch(`${API_BASE_URL}/memory/${memoryId}`, { method: 'DELETE' });
    return res.json();
  },
  // Adaptive endpoints
  getSuggestions: async () => {
    const res = await fetch(`${API_BASE_URL}/adaptive/suggestions`);
    return res.json();
  },
  getPatterns: async () => {
    const res = await fetch(`${API_BASE_URL}/adaptive/patterns`);
    return res.json();
  },
  getAdaptiveHistory: async () => {
    const res = await fetch(`${API_BASE_URL}/adaptive/history`);
    return res.json();
  },
  submitAdaptiveFeedback: async (suggestionId: string, feedback: string) => {
    const res = await fetch(`${API_BASE_URL}/adaptive/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ suggestion_id: suggestionId, feedback })
    });
    return res.json();
  },
  // Accessibility endpoints
  getAccessibilityProfile: async () => {
    const res = await fetch(`${API_BASE_URL}/accessibility/profile`);
    return res.json();
  },
  setAccessibilityProfile: async (profile: string) => {
    const res = await fetch(`${API_BASE_URL}/accessibility/profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile })
    });
    return res.json();
  },
  getRecognizedSigns: async () => {
    const res = await fetch(`${API_BASE_URL}/accessibility/sign`);
    return res.json();
  },
  triggerScreenReader: async () => {
    const res = await fetch(`${API_BASE_URL}/accessibility/read`, { method: 'POST' });
    return res.json();
  },
  getAccessibilitySettings: async () => {
    const res = await fetch(`${API_BASE_URL}/accessibility/settings`);
    return res.json();
  },
  updateAccessibilitySettings: async (settings: any) => {
    const res = await fetch(`${API_BASE_URL}/accessibility/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings)
    });
    return res.json();
  },
  // Extension SDK endpoints
  listExtensions: async () => {
    const res = await fetch(`${API_BASE_URL}/extensions/`);
    return res.json();
  },
  getExtensionStats: async () => {
    const res = await fetch(`${API_BASE_URL}/extensions/stats`);
    return res.json();
  },
  enableExtension: async (extId: string) => {
    const res = await fetch(`${API_BASE_URL}/extensions/${extId}/enable`, { method: 'POST' });
    return res.json();
  },
  disableExtension: async (extId: string) => {
    const res = await fetch(`${API_BASE_URL}/extensions/${extId}/disable`, { method: 'POST' });
    return res.json();
  },
  uninstallExtension: async (extId: string) => {
    const res = await fetch(`${API_BASE_URL}/extensions/${extId}/uninstall`, { method: 'POST' });
    return res.json();
  },
  scanExtensions: async () => {
    const res = await fetch(`${API_BASE_URL}/extensions/scan`, { method: 'POST' });
    return res.json();
  },
  validateExtensionManifest: async (manifest: any) => {
    const res = await fetch(`${API_BASE_URL}/extensions/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(manifest)
    });
    return res.json();
  }
};

