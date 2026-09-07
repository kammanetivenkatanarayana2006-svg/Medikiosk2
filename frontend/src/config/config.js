export const config = {
  appName: 'MediKiosk',
  version: '0.1.0',
  phase: 'Phase 4 - Frontend Foundation',
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api',
  
  // Theme
  defaultTheme: 'dark',
  themeStorageKey: 'medikiosk-theme',
  
  // Design System
  breakpoints: {
    mobile: 480,
    tablet: 768,
    laptop: 1024,
    desktop: 1280,
    kiosk: 1920,
  },
  
  // Touch targets
  touchTarget: {
    min: 44,
    comfortable: 48,
    large: 56,
  },
  
  // Animation
  animation: {
    fast: 150,
    base: 250,
    slow: 350,
  },
};