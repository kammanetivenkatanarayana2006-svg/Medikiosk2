import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import Card from "../ui/Card";
import Button from "../ui/Button";
import Input from "../ui/Input";

import styles from "./PatientIdentityForm.module.css";

const PatientIdentityForm = ({ className = "", ...props }) => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone: "",
    gender: "",
    age: "",
  });

  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const firstNameRef = useRef(null);

  useEffect(() => {
    firstNameRef.current?.focus();
  }, []);

  const validateField = (name, value) => {
    const newErrors = {};

    switch (name) {
      case "full_name": {
        const trimmedName = value.trim();

        if (!trimmedName) {
          newErrors.full_name = "Please enter your full name.";
        } else if (trimmedName.length < 2) {
          newErrors.full_name = "Name must be at least 2 characters.";
        } else if (trimmedName.length > 100) {
          newErrors.full_name =
            "Name must be less than 100 characters.";
        }

        break;
      }

      case "email": {
        const trimmedEmail = value.trim();

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!trimmedEmail) {
          newErrors.email = "Please enter your email address.";
        } else if (!emailRegex.test(trimmedEmail)) {
          newErrors.email = "Please enter a valid email address.";
        }

        break;
      }

      case "phone": {
        const phoneRegex = /^[6-9]\d{9}$/;

        if (!value) {
          newErrors.phone = "Please enter your mobile number.";
        } else if (!phoneRegex.test(value)) {
          newErrors.phone =
            "Enter a valid 10-digit mobile number.";
        }

        break;
      }

      case "gender": {
        if (!value) {
          newErrors.gender = "Please select your gender.";
        }

        break;
      }

      case "age": {
        if (value) {
          const ageNum = parseInt(value, 10);

          if (
            Number.isNaN(ageNum) ||
            ageNum < 0 ||
            ageNum > 150
          ) {
            newErrors.age = "Please enter a valid age.";
          }
        }

        break;
      }

      default:
        break;
    }

    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    let updatedValue = value;

    if (name === "phone") {
      updatedValue = value.replace(/\D/g, "").slice(0, 10);
    }

    if (name === "age") {
      updatedValue = value.replace(/\D/g, "").slice(0, 3);
    }

    setFormData((prev) => ({
      ...prev,
      [name]: updatedValue,
    }));

    if (errors[name]) {
      setErrors((prev) => {
        const updatedErrors = { ...prev };
        delete updatedErrors[name];
        return updatedErrors;
      });
    }
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;

    setTouched((prev) => ({
      ...prev,
      [name]: true,
    }));

    const fieldErrors = validateField(name, value);

    setErrors((prev) => ({
      ...prev,
      ...fieldErrors,
    }));
  };

  const handleGenderSelect = (gender) => {
    setFormData((prev) => ({
      ...prev,
      gender,
    }));

    setTouched((prev) => ({
      ...prev,
      gender: true,
    }));

    if (errors.gender) {
      setErrors((prev) => {
        const updatedErrors = { ...prev };
        delete updatedErrors.gender;
        return updatedErrors;
      });
    }
  };

  const validateForm = () => {
    const allErrors = {};

    Object.keys(formData).forEach((key) => {
      const fieldErrors = validateField(key, formData[key]);

      Object.assign(allErrors, fieldErrors);
    });

    setErrors(allErrors);

    setTouched({
      full_name: true,
      email: true,
      phone: true,
      gender: true,
      age: true,
    });

    return Object.keys(allErrors).length === 0;
  };

  const handleContinue = () => {
    const isValid = validateForm();

    if (!isValid) {
      const firstErrorField = Object.keys(formData).find(
        (field) => validateField(field, formData[field])[field]
      );

      if (firstErrorField) {
        const element = document.querySelector(
          `[name="${firstErrorField}"]`
        );

        element?.focus();
      }

      return;
    }

    sessionStorage.setItem(
      "medikiosk_onboarding",
      JSON.stringify(formData)
    );

    // Correct route from AppRoutes.jsx
    navigate("/onboarding/confirm");
  };

  const handleBack = () => {
    navigate("/patient-type");
  };

  return (
    <div
      className={`${styles.container} ${className}`}
      {...props}
    >
      <Card
        variant="glass"
        padding="xlarge"
        className={styles.card}
      >
        <h1 className={`${styles.title} text-h1`}>
          Your Details
        </h1>

        <p className={`${styles.subtitle} text-body-lg`}>
          Please provide your basic information
        </p>

        <form
          className={styles.form}
          onSubmit={(e) => {
            e.preventDefault();
            handleContinue();
          }}
        >
          <div className={styles.field}>
            <Input
              ref={firstNameRef}
              label="Full Name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              onBlur={handleBlur}
              error={touched.full_name && errors.full_name}
              placeholder="Enter your full name"
              size="large"
              autoComplete="name"
              required
            />
          </div>

          <div className={styles.field}>
            <Input
              label="Email Address"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              onBlur={handleBlur}
              error={touched.email && errors.email}
              placeholder="Enter your email address"
              size="large"
              autoComplete="email"
              required
            />
          </div>

          <div className={styles.field}>
            <Input
              label="Mobile Number"
              name="phone"
              type="tel"
              value={formData.phone}
              onChange={handleChange}
              onBlur={handleBlur}
              error={touched.phone && errors.phone}
              placeholder="10-digit mobile number"
              size="large"
              autoComplete="tel"
              hint="We'll use this for verification in the next step"
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label}>
              Gender
            </label>

            <div
              className={styles.genderOptions}
              role="radiogroup"
              aria-label="Gender selection"
            >
              {[
                "Male",
                "Female",
                "Other",
                "Prefer not to say",
              ].map((option) => (
                <button
                  key={option}
                  type="button"
                  className={`${styles.genderOption} ${
                    formData.gender === option
                      ? styles.selected
                      : ""
                  }`}
                  onClick={() => handleGenderSelect(option)}
                  role="radio"
                  aria-checked={formData.gender === option}
                  aria-label={option}
                >
                  {option}
                </button>
              ))}
            </div>

            {touched.gender && errors.gender && (
              <span
                className={styles.errorText}
                role="alert"
              >
                {errors.gender}
              </span>
            )}
          </div>

          <div className={styles.field}>
            <Input
              label="Age (Optional)"
              name="age"
              type="text"
              value={formData.age}
              onChange={handleChange}
              onBlur={handleBlur}
              error={touched.age && errors.age}
              placeholder="Enter your age"
              size="large"
              hint="Helps us personalize your experience"
            />
          </div>

          <div className={styles.actions}>
            <Button
              type="button"
              variant="outline"
              size="large"
              onClick={handleBack}
            >
              BACK
            </Button>

            <Button
              type="submit"
              variant="primary"
              size="large"
            >
              CONTINUE
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default PatientIdentityForm;