import React, { useEffect, useState } from 'react';
import { useSettingsStore } from '../store/settingsStore';

export const Settings: React.FC = () => {
  const { theme, language, developerMode, updateSetting, loadSettings } = useSettingsStore();
  const [localTheme, setLocalTheme] = useState(theme);
  const [localLang, setLocalLang] = useState(language);
  const [localDev, setLocalDev] = useState(developerMode);

  useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  useEffect(() => {
    setLocalTheme(theme);
    setLocalLang(language);
    setLocalDev(developerMode);
  }, [theme, language, developerMode]);

  const handleSave = () => {
    updateSetting('theme', localTheme);
    updateSetting('language', localLang);
    updateSetting('developerMode', localDev);
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto pb-8">
      <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">Settings</h1>
      
      <div className="glass-panel p-6 space-y-8">
        
        {/* Appearance */}
        <section className="space-y-4">
          <h2 className="text-lg font-semibold text-indigo-400 border-b border-white/10 pb-2">Appearance</h2>
          
          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium">Theme</div>
              <div className="text-xs text-white/50">Select application theme</div>
            </div>
            <select 
              value={localTheme} 
              onChange={e => setLocalTheme(e.target.value)}
              className="bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm outline-none focus:border-indigo-500 transition-colors"
            >
              <option value="dark">Dark</option>
              <option value="light">Light</option>
            </select>
          </div>
        </section>

        {/* System */}
        <section className="space-y-4">
          <h2 className="text-lg font-semibold text-indigo-400 border-b border-white/10 pb-2">System</h2>
          
          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium">Language</div>
              <div className="text-xs text-white/50">Core system language</div>
            </div>
            <select 
              value={localLang} 
              onChange={e => setLocalLang(e.target.value)}
              className="bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm outline-none focus:border-indigo-500 transition-colors"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
            </select>
          </div>
        </section>

        {/* Developer */}
        <section className="space-y-4">
          <h2 className="text-lg font-semibold text-indigo-400 border-b border-white/10 pb-2">Developer</h2>
          
          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium">Developer Mode</div>
              <div className="text-xs text-white/50">Enable advanced debugging tools</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" checked={localDev} onChange={e => setLocalDev(e.target.checked)} />
              <div className="w-11 h-6 bg-white/10 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-500"></div>
            </label>
          </div>
        </section>

        <div className="pt-4 flex justify-end">
          <button 
            onClick={handleSave}
            className="px-6 py-2 bg-white text-black hover:bg-white/90 rounded-lg transition-colors font-medium shadow-lg shadow-white/10"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};
