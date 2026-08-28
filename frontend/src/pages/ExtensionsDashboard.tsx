import React, { useEffect, useState, useCallback } from 'react';
import { Blocks, RefreshCw, CheckCircle2, XCircle, AlertCircle, Clock, ChevronDown, ChevronRight, Zap, BookOpen, ListTree, Plug2, Layout, Ear, Package, Code2, ShieldCheck } from 'lucide-react';
import { api } from '../services/api';

const TYPE_META: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  capability:         { label: 'Capability',         color: 'blue',   icon: Zap },
  skill:              { label: 'Skill',               color: 'purple', icon: BookOpen },
  workflow_pack:      { label: 'Workflow Pack',       color: 'emerald',icon: ListTree },
  integration:        { label: 'Integration',         color: 'yellow', icon: Plug2 },
  ui_panel:           { label: 'UI Panel',            color: 'pink',   icon: Layout },
  accessibility_pack: { label: 'Accessibility Pack',  color: 'teal',   icon: Ear },
};

const STATUS_META: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  enabled:   { label: 'Enabled',   color: 'emerald', icon: CheckCircle2 },
  disabled:  { label: 'Disabled',  color: 'slate',   icon: XCircle },
  installed: { label: 'Installed', color: 'blue',    icon: Clock },
  error:     { label: 'Error',     color: 'red',     icon: AlertCircle },
  pending:   { label: 'Pending',   color: 'yellow',  icon: Clock },
};

function ExtensionCard({ ext, onAction }: { ext: any; onAction: () => void }) {
  const [expanded, setExpanded] = useState(false);
  const [loading, setLoading] = useState(false);

  const typeMeta = TYPE_META[ext.manifest?.type] || { label: ext.manifest?.type, color: 'slate', icon: Package };
  const statusMeta = STATUS_META[ext.status] || { label: ext.status, color: 'slate', icon: AlertCircle };
  const TypeIcon = typeMeta.icon;
  const StatusIcon = statusMeta.icon;

  const handleToggle = async () => {
    setLoading(true);
    try {
      if (ext.status === 'enabled') {
        await api.disableExtension(ext.id);
      } else {
        await api.enableExtension(ext.id);
      }
      onAction();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleUninstall = async () => {
    if (!confirm(`Uninstall "${ext.manifest?.name}"?`)) return;
    setLoading(true);
    try {
      await api.uninstallExtension(ext.id);
      onAction();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const colorMap: Record<string, string> = {
    blue: 'text-blue-400 bg-blue-400/10 border-blue-400/20',
    purple: 'text-purple-400 bg-purple-400/10 border-purple-400/20',
    emerald: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
    yellow: 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20',
    pink: 'text-pink-400 bg-pink-400/10 border-pink-400/20',
    teal: 'text-teal-400 bg-teal-400/10 border-teal-400/20',
    slate: 'text-slate-400 bg-slate-400/10 border-slate-400/20',
    red: 'text-red-400 bg-red-400/10 border-red-400/20',
  };

  return (
    <div className={`glass-panel border overflow-hidden transition-all ${
      ext.status === 'enabled' ? 'border-white/10' : 'border-white/5 opacity-80'
    }`}>
      <div className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3 flex-1 min-w-0">
            <div className={`p-2.5 rounded-lg border flex-shrink-0 ${colorMap[typeMeta.color]}`}>
              <TypeIcon size={18} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h3 className="text-base font-bold text-white truncate">{ext.manifest?.name}</h3>
                <span className="text-[10px] text-white/40 font-mono">v{ext.manifest?.version}</span>
              </div>
              <p className="text-white/60 text-sm mt-0.5 line-clamp-2">{ext.manifest?.description}</p>
              <div className="flex items-center gap-2 mt-2 flex-wrap">
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${colorMap[typeMeta.color]}`}>
                  {typeMeta.label}
                </span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded border flex items-center gap-1 ${colorMap[statusMeta.color]}`}>
                  <StatusIcon size={10} />
                  {statusMeta.label}
                </span>
                {ext.manifest?.tags?.slice(0, 3).map((t: string) => (
                  <span key={t} className="text-[10px] text-white/30 bg-white/5 px-2 py-0.5 rounded font-mono">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 flex-shrink-0">
            <button
              onClick={handleToggle}
              disabled={loading || ext.status === 'error'}
              className={`px-4 py-1.5 rounded-lg text-sm font-bold transition-all disabled:opacity-50 ${
                ext.status === 'enabled'
                  ? 'bg-white/10 hover:bg-white/15 text-white/80 border border-white/10'
                  : 'bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/30'
              }`}
            >
              {loading ? '...' : ext.status === 'enabled' ? 'Disable' : 'Enable'}
            </button>
            <button
              onClick={() => setExpanded(v => !v)}
              className="p-1.5 text-white/40 hover:text-white/70 transition-colors"
            >
              {expanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </button>
          </div>
        </div>
      </div>

      {expanded && (
        <div className="px-5 pb-5 border-t border-white/5 pt-4">
          <div className="grid grid-cols-2 gap-4 text-sm mb-4">
            <div>
              <p className="text-white/40 text-xs mb-1">Author</p>
              <p className="text-white/80">{ext.manifest?.author?.name}</p>
            </div>
            <div>
              <p className="text-white/40 text-xs mb-1">Extension ID</p>
              <p className="text-white/80 font-mono text-xs">{ext.id}</p>
            </div>
            <div>
              <p className="text-white/40 text-xs mb-1">AGNIV Compatibility</p>
              <p className="text-white/80 font-mono text-xs">{ext.manifest?.agniv_version}</p>
            </div>
            <div>
              <p className="text-white/40 text-xs mb-1">License</p>
              <p className="text-white/80">{ext.manifest?.license}</p>
            </div>
          </div>

          {ext.manifest?.permissions?.length > 0 && (
            <div className="mb-4">
              <p className="text-white/40 text-xs mb-2 flex items-center gap-1">
                <ShieldCheck size={12} /> Declared Permissions
              </p>
              <div className="flex flex-wrap gap-2">
                {ext.manifest.permissions.map((p: string) => (
                  <span key={p} className="text-[10px] font-mono px-2 py-1 bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 rounded">
                    {p}
                  </span>
                ))}
              </div>
            </div>
          )}

          {ext.error && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 mb-4">
              <p className="text-red-400 text-xs font-mono">{ext.error}</p>
            </div>
          )}

          {Object.keys(ext.metadata || {}).length > 0 && (
            <div className="mb-4">
              <p className="text-white/40 text-xs mb-2">Extension Metadata</p>
              <pre className="bg-black/50 rounded-lg p-3 text-xs text-white/70 overflow-x-auto font-mono">
                {JSON.stringify(ext.metadata, null, 2)}
              </pre>
            </div>
          )}

          <button
            onClick={handleUninstall}
            disabled={loading}
            className="text-red-400 hover:text-red-300 text-xs font-bold transition-colors disabled:opacity-50 flex items-center gap-1"
          >
            <XCircle size={12} /> Uninstall Extension
          </button>
        </div>
      )}
    </div>
  );
}

export const ExtensionsDashboard: React.FC = () => {
  const [extensions, setExtensions] = useState<any[]>([]);
  const [stats, setStats] = useState<any>({});
  const [scanning, setScanning] = useState(false);
  const [filterType, setFilterType] = useState<string>('all');

  const fetchData = useCallback(async () => {
    try {
      const [exts, st] = await Promise.all([api.listExtensions(), api.getExtensionStats()]);
      setExtensions(Array.isArray(exts) ? exts : []);
      setStats(st || {});
    } catch (e) {
      console.error(e);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleScan = async () => {
    setScanning(true);
    try {
      await api.scanExtensions();
      await fetchData();
    } finally {
      setScanning(false);
    }
  };

  const filtered = filterType === 'all'
    ? extensions
    : extensions.filter(e => e.manifest?.type === filterType);

  const statCards = [
    { label: 'Total', value: stats.total ?? 0, color: 'text-white' },
    { label: 'Enabled', value: stats.enabled ?? 0, color: 'text-emerald-400' },
    { label: 'Disabled', value: stats.disabled ?? 0, color: 'text-slate-400' },
    { label: 'Error', value: stats.error ?? 0, color: 'text-red-400' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto h-full flex flex-col pb-6">
      {/* Header */}
      <div className="flex justify-between items-end flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-500 flex items-center gap-3">
            <Code2 size={32} className="text-indigo-400" />
            Extension SDK
          </h1>
          <p className="text-white/50 mt-1">Drop extensions into the <span className="font-mono text-white/70">extensions/</span> folder and click Rescan to install.</p>
        </div>
        <button
          onClick={handleScan}
          disabled={scanning}
          className="flex items-center gap-2 px-5 py-2.5 bg-indigo-600/80 hover:bg-indigo-600 border border-indigo-500/50 text-white rounded-lg font-bold transition-all disabled:opacity-60"
        >
          <RefreshCw size={16} className={scanning ? 'animate-spin' : ''} />
          {scanning ? 'Scanning...' : 'Rescan extensions/'}
        </button>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-4 gap-4">
        {statCards.map(s => (
          <div key={s.label} className="glass-panel p-4 text-center">
            <p className={`text-3xl font-black ${s.color}`}>{s.value}</p>
            <p className="text-white/40 text-xs mt-1">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Filter by type */}
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setFilterType('all')}
          className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
            filterType === 'all' ? 'bg-white/15 text-white border border-white/20' : 'text-white/50 hover:text-white/70 border border-white/5'
          }`}
        >
          All
        </button>
        {Object.entries(TYPE_META).map(([k, v]) => {
          const Icon = v.icon;
          return (
            <button
              key={k}
              onClick={() => setFilterType(k)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                filterType === k ? 'bg-white/15 text-white border border-white/20' : 'text-white/50 hover:text-white/70 border border-white/5'
              }`}
            >
              <Icon size={12} /> {v.label}
            </button>
          );
        })}
      </div>

      {/* Extensions list */}
      <div className="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
        {filtered.length === 0 ? (
          <div className="glass-panel h-64 flex flex-col items-center justify-center text-white/30 text-center p-8">
            <Blocks size={48} className="mb-4 opacity-30" />
            <p className="text-lg font-bold mb-1">No extensions found</p>
            <p className="text-sm">
              Place an extension folder inside <span className="font-mono text-white/50">backend/extensions/</span> and click
              <span className="text-indigo-400 font-bold"> Rescan</span>.
            </p>
          </div>
        ) : (
          filtered.map(ext => (
            <ExtensionCard key={ext.id} ext={ext} onAction={fetchData} />
          ))
        )}
      </div>
    </div>
  );
};
