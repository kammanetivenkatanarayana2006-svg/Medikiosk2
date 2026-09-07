import React, { useEffect, useRef } from 'react';
import styles from './HeartbeatWave.module.css';

const HeartbeatWave = ({ 
  active = true, 
  reducedMotion = false,
  className = '',
  ...props 
}) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  
  useEffect(() => {
    if (!active || reducedMotion) return;
    
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const points = [];
    const numberOfPoints = 50;
    let animationId;
    
    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    
    const createWaveform = () => {
      points.length = 0;
      const width = canvas.width;
      const height = canvas.height;
      const segmentWidth = width / numberOfPoints;
      
      for (let i = 0; i <= numberOfPoints; i++) {
        points.push({
          x: i * segmentWidth,
          y: height / 2,
        });
      }
    };
    
    const animate = (timestamp) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const height = canvas.height;
      const midY = height / 2;
      
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      
      points.forEach((point, index) => {
        // Create heartbeat pattern
        const t = timestamp / 1000;
        const x = point.x;
        let y = midY;
        
        // Main wave
        y += Math.sin(x * 0.02 + t * 2) * 20;
        
        // Heartbeat spike
        const heartbeatPhase = (x * 0.05 + t * 3) % (Math.PI * 2);
        if (heartbeatPhase > 0 && heartbeatPhase < 0.5) {
          y -= Math.sin(heartbeatPhase * 12) * 30 * Math.exp(-heartbeatPhase * 3);
        }
        
        points[index].y = y;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      
      ctx.strokeStyle = 'var(--color-primary)';
      ctx.lineWidth = 2;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.shadowColor = 'var(--color-primary)';
      ctx.shadowBlur = 10;
      ctx.stroke();
      
      animationId = requestAnimationFrame(animate);
    };
    
    resizeCanvas();
    createWaveform();
    animate(0);
    
    window.addEventListener('resize', () => {
      resizeCanvas();
      createWaveform();
    });
    
    return () => {
      cancelAnimationFrame(animationId);
    };
  }, [active, reducedMotion]);
  
  return (
    <canvas
      ref={canvasRef}
      className={`${styles.waveform} ${className}`}
      aria-hidden="true"
      {...props}
    />
  );
};

export default HeartbeatWave;