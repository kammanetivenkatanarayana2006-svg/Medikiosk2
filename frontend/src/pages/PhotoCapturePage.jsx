import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { patientService } from '../services/patient';
import styles from './PhotoCapturePage.module.css';

const PhotoCapturePage = () => {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setCameraActive(false);
  }, []);
  
  const startCamera = useCallback(async () => {
    setError(null);
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' },
        audio: false,
      });
      
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setCameraActive(true);
    } catch (err) {
      if (err.name === 'NotAllowedError') {
        setError('Camera access was denied. Please allow camera access to continue.');
      } else if (err.name === 'NotFoundError') {
        setError('No camera device found. You can continue without a photo.');
      } else {
        setError('Camera access is unavailable. You can continue without a photo or try again.');
      }
    }
  }, []);
  
  useEffect(() => {
    startCamera();
    
    return () => {
      stopCamera();
    };
  }, [startCamera, stopCamera]);
  
  const handleCapture = () => {
    if (!videoRef.current || !cameraActive) return;
    
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0);
    
    const imageDataUrl = canvas.toDataURL('image/jpeg', 0.9);
    setCapturedImage(imageDataUrl);
    stopCamera();
  };
  
  const handleRetake = () => {
    setCapturedImage(null);
    startCamera();
  };
  
  const handleConfirm = async () => {
    if (!capturedImage) return;
    
    setLoading(true);
    setError(null);
    
    // Convert data URL to blob
    const response = await fetch(capturedImage);
    const blob = await response.blob();
    
    // Create form data
    const formData = new FormData();
    formData.append('file', blob, 'patient_photo.jpg');
    
    const result = await patientService.uploadPhoto(formData);
    
    setLoading(false);
    
    if (result.success) {
      navigate('/profile-confirmation');
    } else {
      setError(result.error);
    }
  };
  
  const handleSkip = () => {
    navigate('/profile-confirmation');
  };
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Capture Your Photo
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Face the camera, remain still, and ensure adequate lighting.
        </p>
        
        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}
        
        <div className={styles.cameraContainer}>
          {capturedImage ? (
            <img
              src={capturedImage}
              alt="Captured patient photo"
              className={styles.preview}
            />
          ) : (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className={styles.video}
              aria-label="Camera preview"
            />
          )}
          
          {cameraActive && !capturedImage && (
            <div className={styles.cameraIndicator}>
              <span className={styles.cameraDot} />
              Camera active
            </div>
          )}
        </div>
        
        <div className={styles.actions}>
          {!capturedImage ? (
            <>
              <Button
                variant="outline"
                size="large"
                onClick={() => navigate('/photo-consent')}
              >
                BACK
              </Button>
              <Button
                variant="primary"
                size="large"
                onClick={handleCapture}
                disabled={!cameraActive}
              >
                CAPTURE
              </Button>
              <Button
                variant="ghost"
                size="large"
                onClick={handleSkip}
              >
                SKIP
              </Button>
            </>
          ) : (
            <>
              <Button
                variant="outline"
                size="large"
                onClick={handleRetake}
              >
                RETAKE
              </Button>
              <Button
                variant="primary"
                size="large"
                onClick={handleConfirm}
                loading={loading}
              >
                CONFIRM PHOTO
              </Button>
            </>
          )}
        </div>
      </Card>
    </div>
  );
};

export default PhotoCapturePage;