import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Card from "../components/ui/Card";
import Button from "../components/ui/Button";

import { useAuth } from "../contexts/AuthContext";
import { authService } from "../services/auth";

import styles from "./EmailVerificationPage.module.css";

const EmailVerificationPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const registeredEmail =
    user?.email || "your registered email address";

  const handleResend = async () => {
    if (loading) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const result =
        await authService.resendVerificationEmail();

      if (result?.success) {
        setMessage(
          "Verification email sent. Please check your inbox."
        );
      } else {
        setError(
          result?.error ||
            "Unable to resend verification email. Please try again."
        );
      }
    } catch (err) {
      console.error(
        "Resend verification email failed:",
        err
      );

      setError(
        err?.response?.data?.message ||
          err?.message ||
          "Unable to resend verification email. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = () => {
    navigate("/patient-home");
  };

  return (
    <div className={styles.container}>
      <Card
        variant="glass"
        padding="xlarge"
        className={styles.card}
      >
        <div
          className={styles.icon}
          aria-hidden="true"
        >
          📧
        </div>

        <h1 className={`${styles.title} text-h1`}>
          Verify Your Email
        </h1>

        <p className={`${styles.subtitle} text-body-lg`}>
          We sent a verification link to{" "}
          <strong>{registeredEmail}</strong>. Please check
          your inbox and click the link to verify.
        </p>

        {message && (
          <div
            className={styles.success}
            role="status"
            aria-live="polite"
          >
            {message}
          </div>
        )}

        {error && (
          <div
            className={styles.error}
            role="alert"
            aria-live="assertive"
          >
            {error}
          </div>
        )}

        <div className={styles.actions}>
          <Button
            type="button"
            variant="outline"
            size="large"
            fullWidth
            onClick={handleResend}
            loading={loading}
            disabled={loading}
          >
            {loading ? "SENDING..." : "RESEND EMAIL"}
          </Button>

          <Button
            type="button"
            variant="primary"
            size="large"
            fullWidth
            onClick={handleContinue}
          >
            CONTINUE
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default EmailVerificationPage;