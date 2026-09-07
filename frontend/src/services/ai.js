const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class AIService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async getAIStatus() {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/ai/status`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Failed to get AI status' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
  
  async getNextQuestion(interviewId, currentQuestionId, response) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/ai/interviews/${interviewId}/next-question`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          current_question_id: currentQuestionId,
          response,
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'AI request failed' };
      }
      
      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. AI unavailable.' };
    }
  }
}

export const aiService = new AIService();