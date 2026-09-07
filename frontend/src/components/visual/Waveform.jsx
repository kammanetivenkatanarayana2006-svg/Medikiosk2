import React from 'react';
import './Waveform.css';

export default function Waveform() {
  return (
    <div className="waveform-container" aria-label="A.I. Voice Placeholder Waveform">
      {[40, 70, 30, 85, 50, 95, 45, 75, 35, 60, 90, 40, 80, 50, 30].map((height, idx) => (
        <span 
          key={idx} 
          className="waveform-bar" 
          style={{ 
            height: `${height}%`,
            animationDelay: `${idx * 0.1}s` 
          }} 
        />
      ))}
    </div>
  );
}