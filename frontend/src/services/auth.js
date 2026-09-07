const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const TOKEN_KEY = 'medikiosk_access_token';

class AuthService {
  getToken() {
    return sessionStorage.getItem(TOKEN_KEY);
  }

  setToken(token) {
    sessionStorage.setItem(TOKEN_KEY, token);
  }

  clearToken() {
    sessionStorage.removeItem(TOKEN_KEY);
  }

  async register(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || 'Registration failed',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      console.error('Registration error:', error);

      return {
        success: false,
        error: 'Unable to connect to MediKiosk. Please try again.',
      };
    }
  }

  async login(email, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || 'Login failed',
        };
      }

      // Backend response:
      // {
      //   success: true,
      //   message: "Login successful",
      //   data: {
      //     access_token: "...",
      //     token_type: "bearer",
      //     expires_in: 1800,
      //     user: {...}
      //   },
      //   verification_required: false
      // }

      const token = data?.access_token;
      const user = data?.user;

      if (!token) {
        return {
          success: false,
          error: 'Login successful, but access token was not received.',
        };
      }

      // Store JWT token
      this.setToken(token);

      return {
        success: true,
        user,
        data: data.data,
        verification_required: data.verification_required ?? false,
      };
    } catch (error) {
      console.error('Login error:', error);

      return {
        success: false,
        error: 'Unable to connect to MediKiosk. Please try again.',
      };
    }
  }

  async getCurrentUser() {
    const token = this.getToken();

    if (!token) {
      throw new Error('No token found');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        this.clearToken();
        throw new Error(data.detail || 'Invalid token');
      }

      return data.user;
    } catch (error) {
      console.error('Get current user error:', error);
      throw error;
    }
  }

  logout() {
    this.clearToken();
  }

  async requestPhoneOTP() {
    const token = this.getToken();

    if (!token) {
      return {
        success: false,
        error: 'Not authenticated',
      };
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/request-phone-otp`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || 'Failed to send OTP',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      console.error('Request phone OTP error:', error);

      return {
        success: false,
        error: 'Network error. Please try again.',
      };
    }
  }

  async verifyPhone(otp) {
    const token = this.getToken();

    if (!token) {
      return {
        success: false,
        error: 'Not authenticated',
      };
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/verify-phone?otp=${encodeURIComponent(otp)}`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || 'Verification failed',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      console.error('Verify phone error:', error);

      return {
        success: false,
        error: 'Network error. Please try again.',
      };
    }
  }

  async resendVerificationEmail() {
    const token = this.getToken();

    if (!token) {
      return {
        success: false,
        error: 'Not authenticated',
      };
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/resend-verification-email`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || 'Failed to resend email',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      console.error('Resend verification email error:', error);

      return {
        success: false,
        error: 'Network error. Please try again.',
      };
    }
  }
}

export const authService = new AuthService();
