import { useState, useEffect, useCallback } from 'react';

const THEME_STORAGE_KEY = 'medikiosk-theme';

export function useTheme() {
  const [theme, setTheme] = useState(() => {
    // Get initial theme from localStorage or system preference
    const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    if (storedTheme) {
      return storedTheme;
    }
    
    if (window.matchMedia('(prefers-color-scheme: light)').matches) {
      return 'light';
    }
    
    return 'dark';
  });

  useEffect(() => {
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  }, []);

  const setSystemTheme = useCallback(() => {
    const isLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    setTheme(isLight ? 'light' : 'dark');
  }, []);

  return {
    theme,
    setTheme,
    toggleTheme,
    setSystemTheme,
    isDark: theme === 'dark',
  };
}