const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class FollowUpService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async getFollowUp(interviewId, responseId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/interviews/${interviewId}/follow-up`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ response_id: responseId }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to get follow-up' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. Follow-up unavailable.' };
    }
  }
}

export const followUpService = new FollowUpService();