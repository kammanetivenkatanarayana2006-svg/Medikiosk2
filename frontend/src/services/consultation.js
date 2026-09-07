const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class ConsultationService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async createConsultation(consultationData) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/consultations`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(consultationData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to create consultation' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
}

export const consultationService = new ConsultationService();