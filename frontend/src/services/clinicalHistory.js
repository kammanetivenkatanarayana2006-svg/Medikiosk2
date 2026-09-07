const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class ClinicalHistoryService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async getStructuredHistory(interviewId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/clinical-history/${interviewId}/structured`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to load history' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
}

export const clinicalHistoryService = new ClinicalHistoryService();