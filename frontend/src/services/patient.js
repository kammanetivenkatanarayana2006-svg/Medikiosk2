const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class PatientService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async getMyProfile() {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/patients/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to load profile' };
      }
      
      return { success: true, patient: data.patient };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async updateMyProfile(updateData) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/patients/me`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to update profile' };
      }
      
      return { success: true, patient: data.patient };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async uploadPhoto(formData) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/patients/me/photo`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to upload photo' };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
}

export const patientService = new PatientService();