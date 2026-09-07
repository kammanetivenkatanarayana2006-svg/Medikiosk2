import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authService } from '../services/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);
  
  useEffect(() => {
    // Check for existing token
    const token = authService.getToken();
    if (token) {
      // Validate token by fetching user info
      authService.getCurrentUser()
        .then(userData => {
          setUser(userData);
          setAuthenticated(true);
        })
        .catch(() => {
          authService.clearToken();
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);
  
  const login = useCallback(async (email, password) => {
    const result = await authService.login(email, password);
    if (result.success) {
      setUser(result.user);
      setAuthenticated(true);
    }
    return result;
  }, []);
  
  const register = useCallback(async (userData) => {
    const result = await authService.register(userData);
    return result;
  }, []);
  
  const logout = useCallback(() => {
    authService.logout();
    setUser(null);
    setAuthenticated(false);
  }, []);
  
  const value = {
    user,
    loading,
    authenticated,
    login,
    register,
    logout,
  };
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}