import React, { useState, useRef } from 'react';
import Card from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { medicalDocumentService } from '../../services/medicalDocument';
import styles from './MedicalDocumentUpload.module.css';

const MedicalDocumentUpload = ({ 
  consultationId = null,
  onComplete = null,
  className = '',
  ...props 
}) => {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);
  
  const handleFileSelect = async (e) => {
    const files = Array.from(e.target.files);
    
    for (const file of files) {
      setUploading(true);
      setError(null);
      
      const result = await medicalDocumentService.uploadDocument(file, consultationId);
      
      if (result.success) {
        setDocuments(prev => [...prev, result.data]);
      } else {
        setError(result.error);
      }
    }
    
    setUploading(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  
  const handleRemove = async (documentId) => {
    const result = await medicalDocumentService.deleteDocument(documentId);
    
    if (result.success) {
      setDocuments(prev => prev.filter(d => d.id !== documentId));
    }
  };
  
  const getStatusBadge = (ocrStatus) => {
    switch (ocrStatus) {
      case 'completed':
        return <Badge variant="success" size="small">Processed</Badge>;
      case 'processing':
      case 'pending':
        return <Badge variant="warning" size="small">Processing...</Badge>;
      case 'failed':
        return <Badge variant="danger" size="small">Failed</Badge>;
      default:
        return <Badge variant="default" size="small">{ocrStatus}</Badge>;
    }
  };
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="large" className={styles.card}>
        <h2 className={`${styles.title} text-h2`}>
          Previous Medical Reports
        </h2>
        <p className={`${styles.subtitle} text-body`}>
          Upload previous medical reports to help organize your clinical history.
        </p>
        
        <div className={styles.uploadArea}>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            multiple
            onChange={handleFileSelect}
            className={styles.fileInput}
            aria-label="Upload medical documents"
          />
          <Button
            variant="primary"
            size="large"
            onClick={() => fileInputRef.current?.click()}
            loading={uploading}
          >
            📄 UPLOAD REPORT
          </Button>
          <p className={styles.supported}>
            Supported: PDF, JPG, JPEG, PNG (Max 10MB each)
          </p>
        </div>
        
        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}
        
        {documents.length > 0 && (
          <div className={styles.documentList}>
            {documents.map((doc) => (
              <div key={doc.id} className={styles.documentItem}>
                <span className={styles.documentIcon}>📄</span>
                <div className={styles.documentInfo}>
                  <span className={styles.documentName}>{doc.original_filename}</span>
                  <span className={styles.documentSize}>
                    {(doc.file_size / 1024).toFixed(1)} KB
                  </span>
                </div>
                {getStatusBadge(doc.ocr_status)}
                <button
                  className={styles.removeButton}
                  onClick={() => handleRemove(doc.id)}
                  aria-label={`Remove ${doc.original_filename}`}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}
        
        <div className={styles.actions}>
          <Button
            variant="ghost"
            size="medium"
            onClick={() => {
              if (onComplete) onComplete();
            }}
          >
            Skip / Continue
          </Button>
        </div>
        
        <p className={styles.disclaimer}>
          OCR/Extracted information is AI-assisted. Doctor review required.
        </p>
      </Card>
    </div>
  );
};

export default MedicalDocumentUpload;