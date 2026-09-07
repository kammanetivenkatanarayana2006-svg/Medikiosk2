const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class HistoryService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async getPatientHistory(page = 1, pageSize = 10, sortOrder = 'newest_first') {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(
        `${API_BASE_URL}/history?page=${page}&page_size=${pageSize}&sort_order=${sortOrder}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to load history' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async getConsultationDetail(consultationId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/history/consultations/${consultationId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to load consultation' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
}

export const historyService = new HistoryService();