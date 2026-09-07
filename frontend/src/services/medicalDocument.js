const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class MedicalDocumentService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async uploadDocument(file, consultationId = null) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (consultationId) {
        formData.append('consultation_id', consultationId);
      }
      
      const response = await fetch(`${API_BASE_URL}/medical-documents`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Upload failed' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' };
    }
  }
  
  async getMyDocuments() {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/medical-documents`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to load documents' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
  
  async getDocumentOCR(documentId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/medical-documents/${documentId}/ocr`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to load OCR' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
  
  async deleteDocument(documentId) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/medical-documents/${documentId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to delete document' };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
}

export const medicalDocumentService = new MedicalDocumentService();