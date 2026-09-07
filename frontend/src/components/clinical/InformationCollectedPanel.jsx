import React, { useEffect, useState } from 'react';
import Card from '../ui/Card';
import Badge from '../ui/Badge';
import { clinicalHistoryService } from '../../services/clinicalHistory';
import styles from './InformationCollectedPanel.module.css';

const InformationCollectedPanel = ({ 
  interviewId,
  className = '',
  ...props 
}) => {
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(false);
  
  useEffect(() => {
    if (interviewId && expanded) {
      loadHistory();
    }
  }, [interviewId, expanded]);
  
  const loadHistory = async () => {
    setLoading(true);
    const result = await clinicalHistoryService.getStructuredHistory(interviewId);
    setLoading(false);
    
    if (result.success) {
      setHistory(result.data.structured_history);
    }
  };
  
  const formatValue = (field) => {
    if (!field) return 'Not provided';
    if (typeof field === 'string') return field;
    if (field.value) return field.value;
    return 'Not provided';
  };
  
  const formatList = (list) => {
    if (!list || list.length === 0) return 'Not provided';
    return list.map(item => item.value || item).join(', ');
  };
  
  return (
    <Card variant="default" padding="medium" className={`${styles.panel} ${className}`} {...props}>
      <button
        className={styles.toggle}
        onClick={() => setExpanded(!expanded)}
        aria-expanded={expanded}
      >
        <span>📋 Information Collected</span>
        <Badge variant="primary" size="small">AI-assisted draft</Badge>
        <span className={styles.arrow}>{expanded ? '▲' : '▼'}</span>
      </button>
      
      {expanded && (
        <div className={styles.content}>
          {loading ? (
            <p className={styles.loading}>Loading...</p>
          ) : history ? (
            <div className={styles.fields}>
              <div className={styles.field}>
                <span className={styles.label}>Chief Complaint</span>
                <span className={styles.value}>{formatValue(history.chief_complaint)}</span>
              </div>
              <div className={styles.field}>
                <span className={styles.label}>Duration</span>
                <span className={styles.value}>{formatValue(history.duration)}</span>
              </div>
              <div className={styles.field}>
                <span className={styles.label}>Symptoms</span>
                <span className={styles.value}>{formatList(history.symptoms)}</span>
              </div>
              <div className={styles.field}>
                <span className={styles.label}>Severity</span>
                <span className={styles.value}>{formatValue(history.severity)}</span>
              </div>
              <div className={styles.field}>
                <span className={styles.label}>Medical History</span>
                <span className={styles.value}>{formatList(history.medical_history)}</span>
              </div>
              <div className={styles.field}>
                <span className={styles.label}>Medications</span>
                <span className={styles.value}>{formatList(history.medications)}</span>
              </div>
              <div className={styles.field}>
                <span className={styles.label}>Allergies</span>
                <span className={styles.value}>{formatList(history.allergies)}</span>
              </div>
            </div>
          ) : (
            <p className={styles.loading}>No structured information yet.</p>
          )}
          
          <p className={styles.disclaimer}>
            Draft generated from your responses. Not a diagnosis.
          </p>
        </div>
      )}
    </Card>
  );
};

export default InformationCollectedPanel;