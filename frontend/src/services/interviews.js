const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class InterviewService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async createInterview(consultationId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/interviews`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ consultation_id: consultationId }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to create interview' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async getInterview(interviewId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/interviews/${interviewId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to load interview' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async startInterview(interviewId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/interviews/${interviewId}/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to start interview' };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async submitResponse(interviewId, questionId, responseText, inputMethod = 'text') {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/interviews/${interviewId}/responses`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question_id: questionId,
          response_text: responseText,
          input_method: inputMethod,
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to submit response' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async pauseInterview(interviewId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/interviews/${interviewId}/pause`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to pause interview' };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async cancelInterview(interviewId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/interviews/${interviewId}/cancel`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to cancel interview' };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
}

export const interviewService = new InterviewService();