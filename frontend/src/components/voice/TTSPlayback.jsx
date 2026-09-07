import React, { useState, useRef, useEffect } from 'react';
import Button from '../ui/Button';
import { voiceService } from '../../services/voice';
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

  const playAudio = () => {
    if (audioRef.current) {
      audioRef.current.play();
      setPlaying(true);
    }
  };
  
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
      setPlaying(true);
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
        src={audioUrl || undefined}
        onLoadedData={playAudio}
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