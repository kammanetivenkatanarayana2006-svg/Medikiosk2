import React, { createContext, useContext, useState, useCallback } from 'react';

const ConsultationContext = createContext(null);

export function ConsultationProvider({ children }) {
  const [consultationSetup, setConsultationSetup] = useState({
    language: 'english',
    consultation_type: null,
    consent_given: false,
  });
  const [consultationId, setConsultationId] = useState(null);
  
  const setLanguage = useCallback((language) => {
    setConsultationSetup(prev => ({ ...prev, language }));
  }, []);
  
  const setConsultationType = useCallback((type) => {
    setConsultationSetup(prev => ({ ...prev, consultation_type: type }));
  }, []);
  
  const setConsent = useCallback((consent) => {
    setConsultationSetup(prev => ({ ...prev, consent_given: consent }));
  }, []);
  
  const resetSetup = useCallback(() => {
    setConsultationSetup({
      language: 'english',
      consultation_type: null,
      consent_given: false,
    });
    setConsultationId(null);
  }, []);
  
  const value = {
    consultationSetup,
    consultationId,
    setConsultationId,
    setLanguage,
    setConsultationType,
    setConsent,
    resetSetup,
  };
  
  return (
    <ConsultationContext.Provider value={value}>
      {children}
    </ConsultationContext.Provider>
  );
}

export function useConsultation() {
  const context = useContext(ConsultationContext);
  if (!context) {
    throw new Error('useConsultation must be used within ConsultationProvider');
  }
  return context;
}