const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

class HealthService {
  async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`)
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Health check error:', error)
      throw error
    }
  }

  async getApiInfo() {
    try {
      const response = await fetch(`${API_BASE_URL}/`)
      if (!response.ok) {
        throw new Error(`API info request failed: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('API info error:', error)
      throw error
    }
  }
}

export const healthService = new HealthService()