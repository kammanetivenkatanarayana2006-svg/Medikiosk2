import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import { historyService } from '../services/history';
import styles from './PatientHistoryPage.module.css';

const PatientHistoryPage = () => {
  const navigate = useNavigate();
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  
  useEffect(() => {
    loadHistory();
  }, [page]);
  
  const loadHistory = async () => {
    setLoading(true);
    setError(null);
    
    const result = await historyService.getPatientHistory(page, 10, 'newest_first');
    
    setLoading(false);
    
    if (result.success) {
      setHistory(result.data);
    } else {
      setError(result.error);
    }
  };
  
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  };
  
  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <Badge variant="success" size="small">Completed</Badge>;
      case 'in_progress':
        return <Badge variant="primary" size="small">In Progress</Badge>;
      case 'paused':
        return <Badge variant="warning" size="small">Paused</Badge>;
      case 'cancelled':
        return <Badge variant="danger" size="small">Cancelled</Badge>;
      default:
        return <Badge variant="default" size="small">{status}</Badge>;
    }
  };
  
  if (loading) {
    return (
      <div className={styles.container}>
        <Card variant="glass" padding="xlarge" className={styles.card}>
          <p className={styles.loading}>Loading your clinical history...</p>
        </Card>
      </div>
    );
  }
  
  if (!history || history.total_consultations === 0) {
    return (
      <div className={styles.container}>
        <Card variant="glass" padding="xlarge" className={styles.card}>
          <div className={styles.icon}>📋</div>
          <h1 className={`${styles.title} text-h1`}>
            No Clinical History Yet
          </h1>
          <p className={`${styles.subtitle} text-body-lg`}>
            Your MediKiosk consultation history will appear here after your
            first completed consultation.
          </p>
          <Button
            variant="primary"
            size="large"
            onClick={() => navigate('/patient/home')}
          >
            START CONSULTATION
          </Button>
        </Card>
      </div>
    );
  }
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          My Clinical History
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Total Consultations: {history.total_consultations}
        </p>
        
        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}
        
        <div className={styles.timeline}>
          {history.consultations.map((consultation) => (
            <div key={consultation.id} className={styles.timelineItem}>
              <div className={styles.timelineDot} />
              <div className={styles.timelineCard}>
                <div className={styles.timelineHeader}>
                  <span className={styles.timelineDate}>
                    {formatDate(consultation.created_at)}
                  </span>
                  {getStatusBadge(consultation.status)}
                </div>
                <h3 className={styles.consultationType}>
                  {consultation.consultation_type.replace(/_/g, ' ').toUpperCase()}
                </h3>
                <div className={styles.consultationMeta}>
                  {consultation.has_clinical_history && (
                    <span className={styles.metaItem}>📝 Clinical History</span>
                  )}
                  {consultation.document_count > 0 && (
                    <span className={styles.metaItem}>📄 {consultation.document_count} Document(s)</span>
                  )}
                  {consultation.ocr_completed_count > 0 && (
                    <span className={styles.metaItem}>✅ OCR Processed</span>
                  )}
                </div>
                <Button
                  variant="outline"
                  size="small"
                  onClick={() => navigate(`/history/consultation/${consultation.id}`)}
                >
                  VIEW DETAILS
                </Button>
              </div>
            </div>
          ))}
        </div>
        
        {history.total_pages > 1 && (
          <div className={styles.pagination}>
            <Button
              variant="ghost"
              size="small"
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page <= 1}
            >
              ← PREV
            </Button>
            <span className={styles.pageInfo}>
              Page {page} of {history.total_pages}
            </span>
            <Button
              variant="ghost"
              size="small"
              onClick={() => setPage(p => Math.min(history.total_pages, p + 1))}
              disabled={page >= history.total_pages}
            >
              NEXT →
            </Button>
          </div>
        )}
        
        <p className={styles.disclaimer}>
          Historical information — doctor review required.
          AI/OCR extracted items are not verified medical conclusions.
        </p>
      </Card>
    </div>
  );
};

export default PatientHistoryPage;