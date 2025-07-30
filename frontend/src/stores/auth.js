import { defineStore } from 'pinia'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    isLoading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(credentials) {
      this.isLoading = true
      this.error = null

      try {
        const response = await authAPI.login(credentials)
        const { access, refresh } = response.data

        this.accessToken = access
        this.refreshToken = refresh

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro no login'
        return false
      } finally {
        this.isLoading = false
      }
    },

    async register(userData) {
      this.isLoading = true
      this.error = null

      try {
        await authAPI.register(userData)
        return true
      } catch (error) {
        this.error = error.response?.data || 'Erro no registro'
        return false
      } finally {
        this.isLoading = false
      }
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },

    clearError() {
      this.error = null
    }
  }
})