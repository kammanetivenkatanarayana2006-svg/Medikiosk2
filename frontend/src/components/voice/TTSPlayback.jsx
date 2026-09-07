import React, { useState, useRef, useEffect } from 'react';
import Button from '../ui/Button';
import styles from './TTSPlayback.module.css';

const TTSPlayback = ({ 
  interviewId,
  text,
  language,
  className = '',
  ...props 
}) => {
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [playing, setPlaying] = useState(false);
  const audioRef = useRef(null);
  
  useEffect(() => {
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);
  
  const handlePlay = async () => {
    if (audioUrl && audioRef.current) {
      audioRef.current.play();
      setPlaying(true);
      return;
    }
    
    setLoading(true);
    setError(null);
    
    const result = await voiceService.synthesizeSpeech(
      interviewId,
      text,
      language,
    );
    
    setLoading(false);
    
    if (result.success) {
      setAudioUrl(result.audioUrl);
      // Auto-play after URL set
      setTimeout(() => {
        if (audioRef.current) {
          audioRef.current.src = result.audioUrl;
          audioRef.current.play();
          setPlaying(true);
        }
      }, 100);
    } else {
      setError(result.error);
    }
  };
  
  const handleStop = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setPlaying(false);
    }
  };
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <audio
        ref={audioRef}
        onEnded={() => setPlaying(false)}
        onPlay={() => setPlaying(true)}
        onPause={() => setPlaying(false)}
      />
      
      <Button
        variant="outline"
        size="medium"
        onClick={playing ? handleStop : handlePlay}
        loading={loading}
        aria-label={playing ? 'Stop question audio' : 'Play question audio'}
      >
        {playing ? '⏹ STOP' : '🔊 PLAY QUESTION'}
      </Button>
      
      {error && (
        <span className={styles.error} role="alert">
          {error}
        </span>
      )}
    </div>
  );
};

export default TTSPlayback;