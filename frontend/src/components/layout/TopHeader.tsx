import React from 'react';

export const TopHeader: React.FC = () => {
  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-white/5 backdrop-blur-sm z-20 shrink-0 select-none drag-region">
      <div className="flex-1" />
      <div className="text-xs text-white/40 font-mono">AGNIV OS Phase 1</div>
    </header>
  );
};
