import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Key, Save, Play, CheckCircle2, XCircle, AlertCircle, Cpu, Wifi } from 'lucide-react';

export function ProviderSettings() {
  const [apiKey, setApiKey] = useState('');
  const [maskedKey, setMaskedKey] = useState<string | null>(null);
  const [model, setModel] = useState('llama3-8b-8192');
  const [status, setStatus] = useState<'idle' | 'saving' | 'testing' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');
  const [diagnostics, setDiagnostics] = useState<{
    status: 'connected' | 'disconnected';
    latency: number | null;
    model: string | null;
    lastError: string | null;
  }>({
    status: 'disconnected',
    latency: null,
    model: null,
    lastError: null,
  });

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const config = await api.getProviderConfig();
      setModel(config.model);
      if (config.has_key) {
        setMaskedKey(config.masked_key);
      }
    } catch (e) {
      console.error('Failed to load provider config', e);
    }
  };

  const handleSave = async () => {
    setStatus('saving');
    setMessage('');
    try {
      // If the user hasn't typed a new key, we just send undefined so it doesn't overwrite
      const payload = {
        model,
        ...(apiKey ? { api_key: apiKey } : {})
      };
      
      await api.saveProviderConfig(payload);
      setStatus('success');
      setMessage('Configuration saved securely.');
      setApiKey(''); // Clear the input field for security
      await loadConfig();
    } catch (e: any) {
      setStatus('error');
      setMessage(e.message || 'Failed to save configuration');
    }
  };

  const handleTest = async () => {
    setStatus('testing');
    setMessage('');
    setDiagnostics(prev => ({ ...prev, lastError: null }));
    try {
      const result = await api.testProviderConnection();
      setStatus('success');
      setMessage(`Connection successful! Latency: ${result.latency_ms}ms`);
      setDiagnostics({
        status: 'connected',
        latency: result.latency_ms,
        model: result.model,
        lastError: null,
      });
    } catch (e: any) {
      setStatus('error');
      setMessage(e.message || 'Connection failed');
      setDiagnostics({
        status: 'disconnected',
        latency: null,
        model: null,
        lastError: e.message || 'Connection failed',
      });
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto h-full flex flex-col gap-6">
      <div className="flex items-center gap-3 mb-4">
        <Key className="w-8 h-8 text-primary" />
        <div>
          <h1 className="text-3xl font-bold">Provider Configuration</h1>
          <p className="text-muted-foreground mt-1">Configure your LLM provider and authentication.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="col-span-2 space-y-6">
          <div className="bg-card rounded-xl p-6 border border-border shadow-sm space-y-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Cpu className="w-5 h-5 text-blue-400" /> Groq API Settings
            </h2>
            
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">API Key</label>
                <input 
                  type="password" 
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder={maskedKey ? maskedKey : "Enter your Groq API Key..."}
                  className="w-full bg-background border border-border rounded-lg px-4 py-2 font-mono"
                />
                <p className="text-xs text-muted-foreground">
                  Your key is stored securely in the local database and never exposed to the frontend.
                </p>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Model Selection</label>
                <select 
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  className="w-full bg-background border border-border rounded-lg px-4 py-2"
                >
                  <option value="llama3-8b-8192">LLaMA3 8B (Fastest)</option>
                  <option value="llama3-70b-8192">LLaMA3 70B (Most Capable)</option>
                  <option value="mixtral-8x7b-32768">Mixtral 8x7B (Large Context)</option>
                </select>
              </div>
            </div>

            <div className="flex gap-4 pt-4 border-t border-border">
              <button 
                onClick={handleSave}
                disabled={status === 'saving' || status === 'testing'}
                className="flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2 rounded-lg font-medium hover:bg-primary/90 transition-colors disabled:opacity-50"
              >
                <Save className="w-4 h-4" /> Save Configuration
              </button>
              
              <button 
                onClick={handleTest}
                disabled={status === 'saving' || status === 'testing' || (!maskedKey && !apiKey)}
                className="flex items-center gap-2 bg-secondary text-secondary-foreground px-6 py-2 rounded-lg font-medium hover:bg-secondary/80 transition-colors disabled:opacity-50"
              >
                <Play className="w-4 h-4" /> Test Connection
              </button>
            </div>

            {message && (
              <div className={`p-4 rounded-lg flex items-start gap-3 ${status === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-green-500/10 text-green-400 border border-green-500/20'}`}>
                {status === 'error' ? <XCircle className="w-5 h-5 shrink-0" /> : <CheckCircle2 className="w-5 h-5 shrink-0" />}
                <p>{message}</p>
              </div>
            )}
          </div>
        </div>

        <div className="col-span-1 space-y-6">
          <div className="bg-card rounded-xl p-6 border border-border shadow-sm space-y-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Wifi className="w-5 h-5 text-purple-400" /> Diagnostics
            </h2>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center py-2 border-b border-border">
                <span className="text-muted-foreground">Status</span>
                <span className={`font-medium flex items-center gap-2 ${diagnostics.status === 'connected' ? 'text-green-400' : 'text-orange-400'}`}>
                  <span className={`w-2 h-2 rounded-full ${diagnostics.status === 'connected' ? 'bg-green-400' : 'bg-orange-400'}`}></span>
                  {diagnostics.status === 'connected' ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              
              <div className="flex justify-between items-center py-2 border-b border-border">
                <span className="text-muted-foreground">Provider</span>
                <span className="font-medium">Groq</span>
              </div>
              
              <div className="flex justify-between items-center py-2 border-b border-border">
                <span className="text-muted-foreground">Active Model</span>
                <span className="font-medium font-mono text-sm">{diagnostics.model || 'Unknown'}</span>
              </div>
              
              <div className="flex justify-between items-center py-2 border-b border-border">
                <span className="text-muted-foreground">Latency</span>
                <span className="font-medium font-mono">
                  {diagnostics.latency !== null ? `${diagnostics.latency} ms` : '--'}
                </span>
              </div>
            </div>

            {diagnostics.lastError && (
              <div className="bg-red-500/10 p-3 rounded-lg border border-red-500/20">
                <div className="flex items-center gap-2 text-red-400 mb-1">
                  <AlertCircle className="w-4 h-4" />
                  <span className="font-medium text-sm">Last Error</span>
                </div>
                <p className="text-xs text-red-300 break-words font-mono">
                  {diagnostics.lastError}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
