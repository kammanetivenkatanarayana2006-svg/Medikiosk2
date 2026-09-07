import React from 'react';
import './AIOrb.css';

export default function AIOrb() {
  return (
    <div className="ai-orb-container" aria-hidden="true">
      <div className="ai-orb-core" />
      <div className="ai-orb-ring ring-1" />
      <div className="ai-orb-ring ring-2" />
      <div className="ai-orb-glow" />
    </div>
  );
}