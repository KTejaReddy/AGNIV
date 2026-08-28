import { create } from 'zustand';
import { api } from '../services/api';

interface SettingsState {
  theme: string;
  language: string;
  developerMode: boolean;
  isLoading: boolean;
  loadSettings: () => Promise<void>;
  updateSetting: (key: string, value: any) => Promise<void>;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  theme: 'dark',
  language: 'en',
  developerMode: false,
  isLoading: false,

  loadSettings: async () => {
    set({ isLoading: true });
    try {
      const themeRes = await api.getSetting('theme');
      const langRes = await api.getSetting('language');
      const devRes = await api.getSetting('developerMode');
      set({
        theme: themeRes.value || 'dark',
        language: langRes.value || 'en',
        developerMode: devRes.value === true || devRes.value === 'true'
      });
    } catch (e) {
      console.error('Failed to load settings', e);
    } finally {
      set({ isLoading: false });
    }
  },

  updateSetting: async (key: string, value: any) => {
    try {
      await api.setSetting(key, value);
      set({ [key]: value } as any);
    } catch (e) {
      console.error(`Failed to update ${key}`, e);
    }
  }
}));
