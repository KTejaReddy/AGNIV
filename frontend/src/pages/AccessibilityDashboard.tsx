import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Ear, EyeOff, ActivitySquare, Settings2, Hand, Volume2, Type, ToggleLeft, ToggleRight, BookOpen } from 'lucide-react';

export const AccessibilityDashboard: React.FC = () => {
  const [profile, setProfile] = useState<string>('GENERAL');
  const [settings, setSettings] = useState<any>({});
  const [signs, setSigns] = useState<any[]>([]);

  const fetchData = async () => {
    try {
      const [profData, setts, sigData] = await Promise.all([
        api.getAccessibilityProfile(),
        api.getAccessibilitySettings(),
        api.getRecognizedSigns()
      ]);
      setProfile(profData.profile);
      setSettings(setts);
      setSigns(sigData);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000); // Polling for signs
    return () => clearInterval(interval);
  }, []);

  const handleProfileChange = async (newProfile: string) => {
    await api.setAccessibilityProfile(newProfile);
    fetchData();
  };

  const toggleSetting = async (key: string) => {
    const updated = { ...settings, [key]: !settings[key] };
    await api.updateAccessibilitySettings(updated);
    fetchData();
  };

  const triggerRead = async () => {
    await api.triggerScreenReader();
  };

  const dictionary = [
    { gesture: 'Palm Open', sign: 'Hello' },
    { gesture: 'Thumbs Up', sign: 'Yes' },
    { gesture: 'Thumbs Down', sign: 'No' },
    { gesture: 'Peace Sign', sign: 'Peace' },
    { gesture: 'Fist', sign: 'Stop' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-cyan-500 flex items-center gap-3">
            <ActivitySquare size={32} className="text-teal-400" />
            Accessibility Suite
          </h1>
          <p className="text-white/50 mt-1">Universal multimodal communication & control.</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6 flex-1 min-h-0">
        
        {/* Left Col: Profiles & Settings */}
        <div className="col-span-4 flex flex-col gap-6 min-h-0">
          <div className="glass-panel p-6">
            <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <Settings2 size={18} className="text-teal-400" />
              Active Profile
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {[
                { id: 'GENERAL', icon: ActivitySquare, label: 'General' },
                { id: 'DEAF', icon: Ear, label: 'Deaf / HoH' },
                { id: 'BLIND', icon: EyeOff, label: 'Blind / Low Vision' },
                { id: 'MOTOR', icon: Hand, label: 'Motor' }
              ].map(p => (
                <button
                  key={p.id}
                  onClick={() => handleProfileChange(p.id)}
                  className={`flex flex-col items-center gap-2 p-3 rounded-lg border transition-all ${
                    profile === p.id 
                    ? 'bg-teal-500/20 border-teal-500/50 text-teal-300'
                    : 'bg-white/5 border-white/10 text-white/50 hover:bg-white/10'
                  }`}
                >
                  <p.icon size={24} />
                  <span className="text-xs font-bold">{p.label}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="glass-panel p-6 flex-1 overflow-y-auto custom-scrollbar">
            <h2 className="text-lg font-bold text-white mb-4">Core Settings</h2>
            <div className="space-y-4">
              {[
                { key: 'sign_recognition_enabled', label: 'Sign Language Recognition', icon: Hand },
                { key: 'live_captions_enabled', label: 'Live Captions', icon: Type },
                { key: 'screen_reader_enabled', label: 'Screen Reader', icon: Volume2 },
                { key: 'gesture_confirmations_enabled', label: 'Gesture Confirmations', icon: ActivitySquare }
              ].map(s => (
                <div key={s.key} className="flex justify-between items-center bg-black/30 p-3 rounded-lg border border-white/5">
                  <div className="flex items-center gap-3 text-white/80">
                    <s.icon size={16} className="text-white/40" />
                    <span className="text-sm font-medium">{s.label}</span>
                  </div>
                  <button onClick={() => toggleSetting(s.key)}>
                    {settings[s.key] ? (
                      <ToggleRight size={28} className="text-teal-400" />
                    ) : (
                      <ToggleLeft size={28} className="text-white/20" />
                    )}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Col: Features Dashboard */}
        <div className="col-span-8 flex flex-col gap-6 min-h-0">
          
          <div className="grid grid-cols-2 gap-6 h-1/2">
            
            {/* Screen Reader & Captions */}
            <div className="glass-panel p-6 flex flex-col">
              <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <Volume2 size={18} className="text-blue-400" />
                Screen Reader & Voice
              </h2>
              <button 
                onClick={triggerRead}
                disabled={!settings.screen_reader_enabled}
                className="bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 border border-blue-500/30 py-3 rounded-lg font-bold flex justify-center items-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed mb-6"
              >
                <BookOpen size={18} /> Read Active Window
              </button>
              
              <div className="flex-1 bg-black/60 rounded-lg border border-white/10 p-4 relative overflow-hidden flex flex-col">
                <div className="absolute top-2 left-2 flex gap-1">
                  <div className="w-2 h-2 rounded-full bg-red-500"></div>
                  <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                </div>
                <div className="flex-1 flex items-center justify-center pt-4">
                  {settings.live_captions_enabled ? (
                    <div className="text-center">
                      <p className="text-xl font-bold text-white tracking-wide leading-relaxed">
                        <span className="bg-black/80 px-2 py-1 rounded">Waiting for speech...</span>
                      </p>
                      <p className="text-xs text-white/30 mt-4">(Live Captions Active via WebSocket)</p>
                    </div>
                  ) : (
                    <p className="text-white/30 text-sm">Live Captions Disabled</p>
                  )}
                </div>
              </div>
            </div>

            {/* Sign Language Dictionary */}
            <div className="glass-panel p-6 flex flex-col">
              <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <Hand size={18} className="text-pink-400" />
                Sign Language Dictionary
              </h2>
              <div className="flex-1 overflow-y-auto custom-scrollbar space-y-2 pr-2">
                {dictionary.map((d, i) => (
                  <div key={i} className="flex justify-between items-center p-3 bg-black/40 border border-white/5 rounded-lg">
                    <span className="text-white/60 text-sm font-mono">{d.gesture}</span>
                    <span className="text-pink-300 font-bold bg-pink-500/10 px-3 py-1 rounded-md">{d.sign}</span>
                  </div>
                ))}
              </div>
            </div>
            
          </div>

          {/* Recognized Signs Timeline */}
          <div className="glass-panel flex-1 flex flex-col min-h-0">
            <div className="p-4 border-b border-white/10">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <ActivitySquare size={18} className="text-teal-400" />
                Sign Recognition Feed
              </h2>
            </div>
            <div className="flex-1 overflow-y-auto custom-scrollbar p-6">
              {!settings.sign_recognition_enabled ? (
                <div className="h-full flex flex-col items-center justify-center text-white/30">
                  <Hand size={48} className="mb-4 opacity-30" />
                  <p>Sign Language Recognition is disabled.</p>
                </div>
              ) : signs.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-white/30">
                  <p>Waiting for gestures from Perception Engine...</p>
                </div>
              ) : (
                <div className="flex gap-4 overflow-x-auto pb-4 custom-scrollbar">
                  {[...signs].reverse().map((s, i) => (
                    <div key={i} className="min-w-[150px] bg-teal-500/10 border border-teal-500/20 p-4 rounded-xl flex flex-col items-center justify-center gap-2 shrink-0">
                      <span className="text-3xl font-bold text-teal-300">{s.sign_name}</span>
                      <div className="flex justify-between w-full text-[10px] text-teal-300/50 mt-2">
                        <span>{(s.confidence * 100).toFixed(0)}% Conf</span>
                        <span>{new Date(s.timestamp * 1000).toLocaleTimeString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
};
