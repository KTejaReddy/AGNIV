import React, { useEffect, useRef } from 'react';
import { useRuntimeStore } from '../store/useRuntimeStore';
import '../styles/fireball.css';

export const Fireball: React.FC = () => {
  const { coreState, telemetry } = useRuntimeStore();
  const orbRef = useRef<HTMLDivElement>(null);

  // Telemetry is dynamically mapped to CSS variables for smooth GPU hardware-accelerated animations
  useEffect(() => {
    if (orbRef.current && telemetry) {
      const { distance, handSpeed, voiceVolume, headRotation } = telemetry;
      
      // Map distance (0-100) to scale (0.5 to 1.5)
      const scale = 0.5 + (distance / 100);
      
      // Map volume (0-100) to glow opacity and spread
      const glowSpread = 20 + (voiceVolume / 2);
      
      // Map hand speed (0-100) to animation duration (slower to faster)
      const speed = Math.max(0.5, 3 - (handSpeed / 33));

      // Head rotation mapped to 3D rotation
      const rotateX = headRotation?.x || 0;
      const rotateY = headRotation?.y || 0;

      orbRef.current.style.setProperty('--fb-scale', scale.toString());
      orbRef.current.style.setProperty('--fb-glow', `${glowSpread}px`);
      orbRef.current.style.setProperty('--fb-speed', `${speed}s`);
      orbRef.current.style.setProperty('--fb-rot-x', `${rotateX}deg`);
      orbRef.current.style.setProperty('--fb-rot-y', `${rotateY}deg`);
    }
  }, [telemetry]);

  return (
    <div className={`fireball-container state-${coreState}`} ref={orbRef}>
      <div className="fireball-core" />
      <div className="fireball-aura" />
      <div className="fireball-particles" />
    </div>
  );
};
