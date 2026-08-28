import React from 'react';

export const Memory: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">Semantic Memory</h1>
      
      <div className="glass-panel p-12 text-center border-dashed border-2 border-white/20 bg-transparent">
        <div className="text-white/40 mb-2 font-medium">Memory system not initialized.</div>
        <p className="text-white/20 text-sm">This feature will be available in Phase 2.</p>
      </div>
    </div>
  );
};
