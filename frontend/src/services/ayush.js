const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class AYUSHService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async getAYUSHRecord(consultationId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/consultations/${consultationId}/ayush`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to load AYUSH record' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
  
  async updateAYUSHRecord(consultationId, updateData) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/consultations/${consultationId}/ayush`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to update AYUSH record' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
}

export const ayushService = new AYUSHService();