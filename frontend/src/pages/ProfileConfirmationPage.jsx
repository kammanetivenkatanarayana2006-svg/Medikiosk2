import React from "react";

import ProfileConfirmation from "../components/onboarding/ProfileConfirmation";
import OnboardingProgress from "../components/onboarding/OnboardingProgress";

import styles from "./ProfileConfirmationPage.module.css";

const ProfileConfirmationPage = () => {
  return (
    <main className={styles.page}>
      <div className={styles.progress}>
        <OnboardingProgress
          currentStep={3}
          totalSteps={3}
        />
      </div>

      <ProfileConfirmation />
    </main>
  );
};

export default ProfileConfirmationPage;