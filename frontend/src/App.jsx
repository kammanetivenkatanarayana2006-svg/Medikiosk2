import React from "react";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { ThemeProvider } from "./contexts/ThemeContext";
import { AuthProvider } from "./contexts/AuthContext";
import { ConsultationProvider } from "./contexts/ConsultationContext";

import ProtectedRoute from "./components/auth/ProtectedRoute";

// Main Pages
import WelcomePage from "./pages/WelcomePage";
import PatientTypePage from "./pages/PatientTypePage";
import PatientOnboardingPage from "./pages/PatientOnboardingPage";
import ProfileConfirmationPage from "./pages/ProfileConfirmationPage";
import ReturningPatientPage from "./pages/ReturningPatientPage";
import OnboardingCompletePage from "./pages/OnboardingCompletePage";

// Authentication Pages
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import RegistrationSuccessPage from "./pages/RegistrationSuccessPage";
import OTPVerificationPage from "./pages/OTPVerificationPage";
import EmailVerificationPage from "./pages/EmailVerificationPage";

// Patient Pages
import PatientHomePlaceholder from "./pages/PatientHomePlaceholder";
import PatientProfilePage from "./pages/PatientProfilePage";
import PhotoConsentPage from "./pages/PhotoConsentPage";
import PhotoCapturePage from "./pages/PhotoCapturePage";
import ProfileFinalConfirmation from "./pages/ProfileFinalConfirmation";

// Layout
import Layout from "./layouts/MainLayout";

// Consultation Components
import LanguageSelection from "./components/consultation/LanguageSelection";
import ConsultationTypeSelection from "./components/consultation/ConsultationTypeSelection";
import ConsentStep from "./components/consultation/ConsentStep";
import ConsultationReady from "./components/consultation/ConsultationReady";
import InterviewPlaceholder from "./components/consultation/InterviewPlaceholder";
import InterviewPage from "./pages/InterviewPage";
import PatientHistoryPage from "./pages/PatientHistoryPage";
import ConsultationDetailPage from "./pages/ConsultationDetailPage";
import AYUSHForm from "./components/ayush/AYUSHForm";
function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <ConsultationProvider>
          <Router>
            <Layout>
              <Routes>
                {/* Main Pages */}
                <Route path="/" element={<WelcomePage />} />

                <Route path="/patient-type" element={<PatientTypePage />} />

                <Route path="/onboarding" element={<PatientOnboardingPage />} />

                <Route
                  path="/onboarding/confirm"
                  element={<ProfileConfirmationPage />}
                />

                <Route
                  path="/onboarding/complete"
                  element={<OnboardingCompletePage />}
                />

                <Route
                  path="/returning-patient"
                  element={<ReturningPatientPage />}
                />

                {/* Authentication */}
                <Route path="/register" element={<RegisterPage />} />

                <Route path="/login" element={<LoginPage />} />

                <Route
                  path="/registration-success"
                  element={<RegistrationSuccessPage />}
                />

                {/* Protected Patient Routes */}
                <Route
                  path="/patient/home"
                  element={
                    <ProtectedRoute>
                      <PatientHomePlaceholder />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/verify-phone"
                  element={
                    <ProtectedRoute>
                      <OTPVerificationPage />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/email-verification"
                  element={
                    <ProtectedRoute>
                      <EmailVerificationPage />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/patient-profile"
                  element={
                    <ProtectedRoute>
                      <PatientProfilePage />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/photo-consent"
                  element={
                    <ProtectedRoute>
                      <PhotoConsentPage />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/photo-capture"
                  element={
                    <ProtectedRoute>
                      <PhotoCapturePage />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/profile-confirmation"
                  element={
                    <ProtectedRoute>
                      <ProfileFinalConfirmation />
                    </ProtectedRoute>
                  }
                />

                {/* Consultation Routes */}
                <Route
                  path="/consultation/language"
                  element={
                    <ProtectedRoute>
                      <LanguageSelection />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/consultation/type"
                  element={
                    <ProtectedRoute>
                      <ConsultationTypeSelection />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/consultation/consent"
                  element={
                    <ProtectedRoute>
                      <ConsentStep />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/consultation/ready"
                  element={
                    <ProtectedRoute>
                      <ConsultationReady />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/consultation/interview-placeholder"
                  element={
                    <ProtectedRoute>
                      <InterviewPlaceholder />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/consultation/interview/:interviewId"
                  element={
                    <ProtectedRoute>
                      <InterviewPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/history"
                  element={
                    <ProtectedRoute>
                      <PatientHistoryPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/history/consultation/:consultationId"
                  element={
                    <ProtectedRoute>
                      <ConsultationDetailPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/consultation/:consultationId/ayush"
                  element={
                    <ProtectedRoute>
                      <AYUSHForm />
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </Layout>
          </Router>
        </ConsultationProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
