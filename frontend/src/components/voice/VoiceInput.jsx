import React, { useState, useRef, useEffect, useCallback } from 'react';
import Button from '../ui/Button';
import styles from './VoiceInput.module.css';

const VOICE_STATES = {
  IDLE: 'idle',
  REQUESTING_PERMISSION: 'requesting_permission',
  RECORDING: 'recording',
  PROCESSING: 'processing',
  TRANSCRIPTION_READY: 'transcription_ready',
  ERROR: 'error',
};

const VoiceInput = ({ 
  interviewId,
  language,
  onTranscriptionConfirmed,
  onTextFallback,
  disabled = false,
  className = '',
  ...props 
}) => {
  const [voiceState, setVoiceState] = useState(VOICE_STATES.IDLE);
  const [recordingTime, setRecordingTime] = useState(0);
  const [transcription, setTranscription] = useState('');
  const [error, setError] = useState(null);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);
  
  const stopMicrophone = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current = null;
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);
  
  useEffect(() => {
    return () => {
      stopMicrophone();
    };
  }, [stopMicrophone]);
  
  const startRecording = async () => {
    setError(null);
    setVoiceState(VOICE_STATES.REQUESTING_PERMISSION);
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];
      
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: mediaRecorder.mimeType || 'audio/webm' });
        chunksRef.current = [];
        stopMicrophone();
        await processAudio(audioBlob, mediaRecorder.mimeType || 'audio/webm');
      };
      
      mediaRecorder.start();
      setVoiceState(VOICE_STATES.RECORDING);
      setRecordingTime(0);
      
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      
    } catch (err) {
      stopMicrophone();
      setVoiceState(VOICE_STATES.ERROR);
      
      if (err.name === 'NotAllowedError') {
        setError('Microphone access was denied. Please use text input.');
        onTextFallback();
      } else if (err.name === 'NotFoundError') {
        setError('No microphone found. Please use text input.');
        onTextFallback();
      } else {
        setError('Microphone unavailable. Please use text input.');
        onTextFallback();
      }
    }
  };
  
  const stopRecording = () => {
    if (mediaRecorderRef.current && voiceState === VOICE_STATES.RECORDING) {
      mediaRecorderRef.current.stop();
      setVoiceState(VOICE_STATES.PROCESSING);
    }
  };
  
  const processAudio = async (audioBlob, mimeType) => {
    setVoiceState(VOICE_STATES.PROCESSING);
    
    const result = await voiceService.transcribeAudio(
      interviewId,
      language,
      audioBlob,
      mimeType,
    );
    
    if (result.success) {
      setTranscription(result.transcription.text);
      setVoiceState(VOICE_STATES.TRANSCRIPTION_READY);
    } else {
      setError(result.error);
      setVoiceState(VOICE_STATES.ERROR);
    }
  };
  
  const handleConfirm = () => {
    if (transcription.trim()) {
      onTranscriptionConfirmed(transcription.trim());
      resetToIdle();
    }
  };
  
  const handleRetry = () => {
    setTranscription('');
    setError(null);
    startRecording();
  };
  
  const resetToIdle = () => {
    setVoiceState(VOICE_STATES.IDLE);
    setTranscription('');
    setRecordingTime(0);
    setError(null);
  };
  
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      {voiceState === VOICE_STATES.IDLE && (
        <div className={styles.idleState}>
          <Button
            variant="primary"
            size="large"
            onClick={startRecording}
            disabled={disabled}
            aria-label="Start voice recording"
          >
            🎙 START SPEAKING
          </Button>
          <Button
            variant="ghost"
            size="medium"
            onClick={onTextFallback}
          >
            ⌨ Type instead
          </Button>
        </div>
      )}
      
      {voiceState === VOICE_STATES.REQUESTING_PERMISSION && (
        <div className={styles.stateMessage}>
          <p>Requesting microphone access...</p>
        </div>
      )}
      
      {voiceState === VOICE_STATES.RECORDING && (
        <div className={styles.recordingState}>
          <div className={styles.micIcon} aria-hidden="true">🎙</div>
          <p className={styles.recordingText} role="status">
            Listening...
          </p>
          <p className={styles.recordingTime}>{formatTime(recordingTime)}</p>
          <div className={styles.waveform} aria-hidden="true">
            {[...Array(5)].map((_, i) => (
              <div key={i} className={styles.waveBar} style={{ animationDelay: `${i * 0.1}s` }} />
            ))}
          </div>
          <Button
            variant="danger"
            size="large"
            onClick={stopRecording}
            aria-label="Stop recording"
          >
            STOP
          </Button>
        </div>
      )}
      
      {voiceState === VOICE_STATES.PROCESSING && (
        <div className={styles.stateMessage}>
          <div className={styles.spinner} aria-hidden="true" />
          <p role="status">Transcribing your response...</p>
        </div>
      )}
      
      {voiceState === VOICE_STATES.TRANSCRIPTION_READY && (
        <div className={styles.transcriptionState}>
          <p className={styles.confirmText}>Did we hear you correctly?</p>
          <div className={styles.transcriptionBox}>
            "{transcription}"
          </div>
          <div className={styles.transcriptionActions}>
            <Button
              variant="primary"
              size="large"
              onClick={handleConfirm}
            >
              USE THIS
            </Button>
            <Button
              variant="outline"
              size="large"
              onClick={handleRetry}
            >
              RECORD AGAIN
            </Button>
            <Button
              variant="ghost"
              size="medium"
              onClick={onTextFallback}
            >
              Type instead
            </Button>
          </div>
        </div>
      )}
      
      {voiceState === VOICE_STATES.ERROR && (
        <div className={styles.errorState}>
          <p className={styles.errorText} role="alert">{error}</p>
          <Button
            variant="outline"
            size="large"
            onClick={onTextFallback}
          >
            TYPE RESPONSE
          </Button>
        </div>
      )}
    </div>
  );
};

export default VoiceInput;