const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class VoiceService {
  getToken() {
    return sessionStorage.getItem('medikiosk_access_token');
  }
  
  async transcribeAudio(interviewId, language, audioBlob, mimeType = 'audio/wav') {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const formData = new FormData();
      formData.append('interview_id', interviewId);
      formData.append('language', language);
      formData.append('file', audioBlob, `audio.${mimeType.split('/')[1] || 'wav'}`);
      
      const response = await fetch(`${API_BASE_URL}/voice/asr`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        return { success: false, error: data.detail || 'Transcription failed' };
      }
      
      return { success: true, transcription: data.data };
    } catch (error) {
      return { success: false, error: 'Network error. Voice transcription unavailable.' };
    }
  }
  
  async synthesizeSpeech(interviewId, text, language, voiceId = null) {
    const token = this.getToken();
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await fetch(`${API_BASE_URL}/voice/tts`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          interview_id: interviewId,
          text,
          language,
          voice_id: voiceId,
        }),
      });
      
      if (!response.ok) {
        const data = await response.json();
        return { success: false, error: data.detail || 'Speech synthesis failed' };
      }
      
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      
      return { success: true, audioUrl };
    } catch (error) {
      return { success: false, error: 'Network error. Voice playback unavailable.' };
    }
  }
}

export const voiceService = new VoiceService();