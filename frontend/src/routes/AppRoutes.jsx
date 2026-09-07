import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import WelcomePage from "../pages/WelcomePage";
import RegisterPage from "../pages/RegisterPage";

import PatientTypePage from "../pages/PatientTypePage";
import PatientOnboardingPage from "../pages/PatientOnboardingPage";
import ProfileConfirmationPage from "../pages/ProfileConfirmationPage";
import OnboardingCompletePage from "../pages/OnboardingCompletePage";
import ReturningPatientPage from "../pages/ReturningPatientPage";

// Patient Home page
import PatientHomePage from "../pages/PatientHomePage";

const AppRoutes = () => {
  return (
    <Routes>
      {/* Home */}
      <Route
        path="/"
        element={<Navigate to="/welcome" replace />}
      />

      {/* Welcome */}
      <Route
        path="/welcome"
        element={<WelcomePage />}
      />

      {/* Register */}
      <Route
        path="/register"
        element={<RegisterPage />}
      />

      {/* Patient Type Selection */}
      <Route
        path="/patient-type"
        element={<PatientTypePage />}
      />

      {/* Patient Onboarding */}
      <Route
        path="/onboarding"
        element={<PatientOnboardingPage />}
      />

      {/* Profile Confirmation */}
      <Route
        path="/onboarding/confirm"
        element={<ProfileConfirmationPage />}
      />

      {/* Onboarding Complete */}
      <Route
        path="/onboarding/complete"
        element={<OnboardingCompletePage />}
      />

      {/* Returning Patient */}
      <Route
        path="/returning-patient"
        element={<ReturningPatientPage />}
      />

      {/* Patient Home */}
      <Route
        path="/patient-home"
        element={<PatientHomePage />}
      />

      {/* Unknown Route */}
      <Route
        path="*"
        element={<Navigate to="/welcome" replace />}
      />
    </Routes>
  );
};

export default AppRoutes;