import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "../ui/Card";
import Button from "../ui/Button";
import Badge from "../ui/Badge";
import { useConsultation } from "../../contexts/ConsultationContext";
import { consultationService } from "../../services/consultation";
import styles from "./ConsultationReady.module.css";

const LANGUAGE_LABELS = {
  english: "English",
  telugu: "తెలుగు (Telugu)",
  hindi: "हिन्दी (Hindi)",
  tamil: "தமிழ் (Tamil)",
  kannada: "ಕನ್ನಡ (Kannada)",
  malayalam: "മലയാളം (Malayalam)",
  marathi: "मराठी (Marathi)",
  bengali: "বাংলা (Bengali)",
};

const TYPE_LABELS = {
  general: "General Clinical Consultation",
  ayurveda: "Ayurveda / AYUSH Consultation",
  follow_up: "Follow-up Consultation",
};

const ConsultationReady = ({ className = "", ...props }) => {
  const navigate = useNavigate();
  const { consultationSetup, setConsultationId, resetSetup } =
    useConsultation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Update handleBegin:
  const handleBegin = async () => {
    setLoading(true);
    setError(null);

    const result = await consultationService.createConsultation({
      language: consultationSetup.language,
      consultation_type: consultationSetup.consultation_type,
      consent_given: consultationSetup.consent_given,
    });

    if (result.success) {
      setConsultationId(result.data.id);

      // Create interview session
      const interviewResult = await interviewService.createInterview(
        result.data.id,
      );

      if (interviewResult.success) {
        setLoading(false);
        navigate(
          `/consultation/interview/${interviewResult.data.interview_id}`,
        );
      } else {
        setLoading(false);
        setError(interviewResult.error);
      }
    } else {
      setLoading(false);
      setError(result.error);
    }
  };
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <div className={styles.icon}>✅</div>
        <Badge variant="success" size="large" className={styles.badge}>
          Ready
        </Badge>
        <h1 className={`${styles.title} text-h1`}>Consultation Ready</h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          You're ready to begin your consultation
        </p>

        <div className={styles.summary}>
          <div className={styles.summaryItem}>
            <span className={styles.summaryLabel}>Language</span>
            <span className={styles.summaryValue}>
              {LANGUAGE_LABELS[consultationSetup.language] ||
                consultationSetup.language}
            </span>
          </div>
          <div className={styles.summaryItem}>
            <span className={styles.summaryLabel}>Consultation Type</span>
            <span className={styles.summaryValue}>
              {TYPE_LABELS[consultationSetup.consultation_type] ||
                consultationSetup.consultation_type}
            </span>
          </div>
          <div className={styles.summaryItem}>
            <span className={styles.summaryLabel}>Consent</span>
            <span className={styles.summaryValue}>
              <Badge variant="success">Confirmed</Badge>
            </span>
          </div>
        </div>

        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}

        <div className={styles.actions}>
          <Button
            variant="outline"
            size="large"
            onClick={() => navigate("/consultation/consent")}
          >
            BACK
          </Button>
          <Button
            variant="primary"
            size="xlarge"
            onClick={handleBegin}
            loading={loading}
          >
            BEGIN CONSULTATION
          </Button>
        </div>

        <p className={styles.note}>
          The AI-assisted clinical interview will be available in the next
          phase.
        </p>
      </Card>
    </div>
  );
};

export default ConsultationReady;
