import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import { historyService } from '../services/history';
import styles from './ConsultationDetailPage.module.css';

const ConsultationDetailPage = () => {
  const navigate = useNavigate();
  const { consultationId } = useParams();
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    loadDetail();
  }, [consultationId]);
  
  const loadDetail = async () => {
    setLoading(true);
    setError(null);
    
    const result = await historyService.getConsultationDetail(consultationId);
    
    setLoading(false);
    
    if (result.success) {
      setDetail(result.data);
    } else {
      setError(result.error);
    }
  };
  
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    });
  };
  
  const formatValue = (value) => {
    if (!value) return 'Not recorded';
    if (typeof value === 'string') return value;
    if (value.value) return value.value;
    return 'Not recorded';
  };
  
  const formatList = (list) => {
    if (!list || list.length === 0) return 'Not recorded';
    if (Array.isArray(list)) {
      return list.map(item => item.value || item).join(', ');
    }
    return 'Not recorded';
  };
  
  if (loading) {
    return (
      <div className={styles.container}>
        <Card variant="glass" padding="xlarge" className={styles.card}>
          <p className={styles.loading}>Loading consultation details...</p>
        </Card>
      </div>
    );
  }
  
  if (!detail) {
    return (
      <div className={styles.container}>
        <Card variant="glass" padding="xlarge" className={styles.card}>
          <p className={styles.error}>Consultation not found.</p>
          <Button variant="outline" onClick={() => navigate('/history')}>
            BACK
          </Button>
        </Card>
      </div>
    );
  }
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Consultation Details
        </h1>
        
        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}
        
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Consultation Information</h2>
          <div className={styles.infoGrid}>
            <div className={styles.infoItem}>
              <span className={styles.infoLabel}>Type</span>
              <span className={styles.infoValue}>
                {detail.consultation_type.replace(/_/g, ' ').toUpperCase()}
              </span>
            </div>
            <div className={styles.infoItem}>
              <span className={styles.infoLabel}>Language</span>
              <span className={styles.infoValue}>{detail.language}</span>
            </div>
            <div className={styles.infoItem}>
              <span className={styles.infoLabel}>Status</span>
              <span className={styles.infoValue}>{detail.status}</span>
            </div>
            <div className={styles.infoItem}>
              <span className={styles.infoLabel}>Date</span>
              <span className={styles.infoValue}>{formatDate(detail.created_at)}</span>
            </div>
          </div>
        </div>
        
        {detail.clinical_history && (
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Clinical Information</h2>
            <div className={styles.clinicalGrid}>
              <div className={styles.clinicalItem}>
                <span className={styles.infoLabel}>Chief Complaint</span>
                <span className={styles.infoValue}>{formatValue(detail.clinical_history.chief_complaint)}</span>
              </div>
              <div className={styles.clinicalItem}>
                <span className={styles.infoLabel}>Duration</span>
                <span className={styles.infoValue}>{formatValue(detail.clinical_history.duration)}</span>
              </div>
              <div className={styles.clinicalItem}>
                <span className={styles.infoLabel}>Symptoms</span>
                <span className={styles.infoValue}>{formatList(detail.clinical_history.symptoms)}</span>
              </div>
              <div className={styles.clinicalItem}>
                <span className={styles.infoLabel}>Severity</span>
                <span className={styles.infoValue}>{formatValue(detail.clinical_history.severity)}</span>
              </div>
            </div>
            <Badge variant="warning" size="small" className={styles.draftBadge}>
              AI-Assisted Draft
            </Badge>
          </div>
        )}
        
        {detail.documents.length > 0 && (
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Previous Documents</h2>
            <div className={styles.documentList}>
              {detail.documents.map((doc) => (
                <div key={doc.id} className={styles.documentItem}>
                  <span>📄 {doc.original_filename}</span>
                  <Badge variant={doc.ocr_status === 'completed' ? 'success' : 'warning'} size="small">
                    {doc.ocr_status}
                  </Badge>
                </div>
              ))}
            </div>
          </div>
        )}
        
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Verification</h2>
          <p className={styles.verificationText}>
            {detail.verification_status === 'not_verified' 
              ? 'Doctor verification pending.' 
              : detail.verification_status}
          </p>
          <p className={styles.disclaimer}>
            Historical information — doctor review required.
            AI/OCR extracted items are not verified medical conclusions.
          </p>
        </div>
        
        <Button
          variant="outline"
          size="large"
          onClick={() => navigate('/history')}
        >
          BACK TO HISTORY
        </Button>
      </Card>
    </div>
  );
};

export default ConsultationDetailPage;