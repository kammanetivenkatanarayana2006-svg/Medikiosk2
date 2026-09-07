import React, { useState, useEffect } from 'react';
import Card from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import Input from '../ui/Input';
import { ayushService } from '../../services/ayush';
import styles from './AYUSHForm.module.css';

const PRAKRITI_OPTIONS = [
  'Vata', 'Pitta', 'Kapha', 'Vata-Pitta', 'Pitta-Kapha',
  'Vata-Kapha', 'Tridosha', 'Not assessed', 'Not recorded',
];

const AGNI_OPTIONS = ['Sama', 'Vishama', 'Tikshna', 'Manda', 'Not assessed', 'Not recorded'];

const KOSHTHA_OPTIONS = ['Mridu', 'Madhyama', 'Krura', 'Not assessed', 'Not recorded'];

const AYUSHForm = ({ 
  consultationId,
  onComplete = null,
  className = '',
  ...props 
}) => {
  const [formData, setFormData] = useState({
    prakriti: 'Not assessed',
    vikriti: '',
    agni: 'Not assessed',
    koshtha: 'Not assessed',
    ahara: '',
    vihara: '',
    nidra: '',
    dashavidha_pariksha: {
      sara: '',
      samhanana: '',
      pramana: '',
      satmya: '',
      satva: '',
      ahara_shakti: '',
      vyayama_shakti: '',
      vaya: '',
    },
    additional_information: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);
  
  useEffect(() => {
    loadRecord();
  }, [consultationId]);
  
  const loadRecord = async () => {
    setLoading(true);
    const result = await ayushService.getAYUSHRecord(consultationId);
    setLoading(false);
    
    if (result.success) {
      // Pre-populate from existing record
      const record = result.data;
      setFormData({
        prakriti: record.prakriti?.value || 'Not assessed',
        vikriti: record.vikriti?.value || '',
        agni: record.agni?.value || 'Not assessed',
        koshtha: record.koshtha?.value || 'Not assessed',
        ahara: record.ahara?.value || '',
        vihara: record.vihara?.value || '',
        nidra: record.nidra?.value || '',
        dashavidha_pariksha: record.dashavidha_pariksha || {
          sara: '', samhanana: '', pramana: '', satmya: '',
          satva: '', ahara_shakti: '', vyayama_shakti: '', vaya: '',
        },
        additional_information: record.additional_information?.value || '',
      });
    }
  };
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  const handleDashavidhaChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      dashavidha_pariksha: {
        ...prev.dashavidha_pariksha,
        [field]: value,
      },
    }));
  };
  
  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSaved(false);
    
    const result = await ayushService.updateAYUSHRecord(consultationId, formData);
    
    setSaving(false);
    
    if (result.success) {
      setSaved(true);
      if (onComplete) onComplete();
    } else {
      setError(result.error);
    }
  };
  
  if (loading) {
    return (
      <Card variant="glass" padding="large" className={styles.card}>
        <p className={styles.loading}>Loading AYUSH information...</p>
      </Card>
    );
  }
  
  return (
    <Card variant="glass" padding="xlarge" className={`${styles.card} ${className}`} {...props}>
      <h2 className={`${styles.title} text-h2`}>
        AYUSH / Ayurveda Information
      </h2>
      <p className={`${styles.subtitle} text-body`}>
        Please provide the following information if relevant to your consultation.
        Your responses will be available for clinician review.
      </p>
      
      {error && (
        <div className={styles.error} role="alert">{error}</div>
      )}
      
      {saved && (
        <div className={styles.saved} role="status">
          <Badge variant="success">Saved</Badge>
        </div>
      )}
      
      {/* Prakriti */}
      <div className={styles.fieldGroup}>
        <label className={styles.label}>Prakriti</label>
        <select
          value={formData.prakriti}
          onChange={handleChange}
          name="prakriti"
          className={styles.select}
          aria-label="Prakriti"
        >
          {PRAKRITI_OPTIONS.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>
      
      {/* Vikriti */}
      <div className={styles.fieldGroup}>
        <label className={styles.label}>Vikriti</label>
        <Input
          name="vikriti"
          value={formData.vikriti}
          onChange={handleChange}
          placeholder="Enter Vikriti information if known"
          size="large"
        />
      </div>
      
      {/* Agni */}
      <div className={styles.fieldGroup}>
        <label className={styles.label}>Agni</label>
        <select
          value={formData.agni}
          onChange={handleChange}
          name="agni"
          className={styles.select}
          aria-label="Agni"
        >
          {AGNI_OPTIONS.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>
      
      {/* Koshtha */}
      <div className={styles.fieldGroup}>
        <label className={styles.label}>Koshtha</label>
        <select
          value={formData.koshtha}
          onChange={handleChange}
          name="koshtha"
          className={styles.select}
          aria-label="Koshtha"
        >
          {KOSHTHA_OPTIONS.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>
      
      {/* Ahara */}
      <div className={styles.fieldGroup}>
        <label className={styles.label}>Ahara (Diet)</label>
        <textarea
          value={formData.ahara}
          onChange={handleChange}
          name="ahara"
          className={styles.textarea}
          rows={3}
          placeholder="Dietary pattern, meal frequency, food habits..."
          aria-label="Ahara"
        />
      </div>
      
      {/* Vihara */}
      <div className={styles.fieldGroup}>
        <label className={styles.label}>Vihara (Lifestyle)</label>
        <textarea
          value={formData.vihara}
          onChange={handleChange}
          name="vihara"
          className={styles.textarea}
          rows={3}
          placeholder="Daily routine, physical activity, lifestyle habits..."
          aria-label="Vihara"
        />
      </div>
      
      {/* Nidra */}
      <div className={styles.fieldGroup}>
        <label className={styles.label}>Nidra (Sleep)</label>
        <textarea
          value={formData.nidra}
          onChange={handleChange}
          name="nidra"
          className={styles.textarea}
          rows={3}
          placeholder="Sleep duration, quality, schedule..."
          aria-label="Nidra"
        />
      </div>
      
      {/* Dashavidha Pariksha */}
      <div className={styles.fieldGroup}>
        <h3 className={styles.sectionTitle}>Dashavidha Pariksha</h3>
        <div className={styles.dashavidhaGrid}>
          {['sara', 'samhanana', 'pramana', 'satmya', 'satva', 'ahara_shakti', 'vyayama_shakti', 'vaya'].map(field => (
            <div key={field} className={styles.dashavidhaItem}>
              <label className={styles.label}>
                {field.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
              </label>
              <Input
                value={formData.dashavidha_pariksha[field] || ''}
                onChange={(e) => handleDashavidhaChange(field, e.target.value)}
                placeholder="Not assessed"
                size="medium"
              />
            </div>
          ))}
        </div>
      </div>
      
      {/* Additional Information */}
      <div className={styles.fieldGroup}>
        <label className={styles.label}>Additional AYUSH Information</label>
        <textarea
          value={formData.additional_information}
          onChange={handleChange}
          name="additional_information"
          className={styles.textarea}
          rows={3}
          placeholder="Any additional information..."
          aria-label="Additional AYUSH information"
        />
      </div>
      
      <div className={styles.actions}>
        <Button
          variant="primary"
          size="large"
          onClick={handleSave}
          loading={saving}
        >
          SAVE & CONTINUE
        </Button>
      </div>
      
      <p className={styles.disclaimer}>
        AYUSH information captured for clinician review. Not a diagnosis or treatment recommendation.
      </p>
    </Card>
  );
};

export default AYUSHForm;