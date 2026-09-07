import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";

import { useAuth } from "../contexts/AuthContext";

import styles from "./LoginPage.module.css";

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    setErrors((prev) => {
      const updatedErrors = { ...prev };
      delete updatedErrors[name];
      return updatedErrors;
    });

    setApiError("");
  };

  const validate = () => {
    const newErrors = {};

    const email = formData.email.trim();

    if (!email) {
      newErrors.email = "Please enter your email address.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Please enter a valid email address.";
    }

    if (!formData.password) {
      newErrors.password = "Please enter your password.";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    try {
      setLoading(true);
      setApiError("");

      const result = await login(
        formData.email.trim(),
        formData.password
      );

      if (!result || !result.success) {
        setApiError(
          result?.error || "Invalid email or password."
        );
        return;
      }

      /*
       * If your backend/AuthContext returns verification_required,
       * redirect the user to the verification page.
       */
      if (result.verification_required) {
        navigate("/email-verification", {
          state: {
            email: formData.email.trim(),
          },
        });

        return;
      }

      // Correct route from AppRoutes.jsx
      navigate("/patient-home");
    } catch (error) {
      console.error("Login failed:", error);

      setApiError(
        error?.response?.data?.message ||
          error?.message ||
          "Unable to login. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = () => {
    navigate("/register");
  };

  return (
    <div className={styles.container}>
      <Card
        variant="glass"
        padding="xlarge"
        className={styles.card}
      >
        <h1 className={`${styles.title} text-h1`}>
          Welcome Back
        </h1>

        <p className={`${styles.subtitle} text-body-lg`}>
          Login to continue your clinical journey
        </p>

        {apiError && (
          <div
            className={styles.apiError}
            role="alert"
          >
            {apiError}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className={styles.form}
          noValidate
        >
          <Input
            label="Email Address"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
            placeholder="Enter your email address"
            size="large"
            autoComplete="email"
            required
          />

          <Input
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            placeholder="Enter your password"
            size="large"
            autoComplete="current-password"
            required
          />

          <Button
            type="submit"
            variant="primary"
            size="xlarge"
            fullWidth
            loading={loading}
            disabled={loading}
          >
            {loading ? "LOGGING IN..." : "LOGIN"}
          </Button>
        </form>

        <p className={styles.registerLink}>
          New to MediKiosk?{" "}
          <button
            type="button"
            className={styles.link}
            onClick={handleRegister}
          >
            Create an account
          </button>
        </p>
      </Card>
    </div>
  );
};

export default LoginPage;