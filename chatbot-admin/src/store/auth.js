// admin/store/auth.js
import { defineStore } from 'pinia'
import axios from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),
  actions: {
    async login(credentials) {
      const response = await axios.post('/api/admin/login/', credentials)
      this.user = response.data.user
      this.isAuthenticated = true
    },
    async checkSessionAndRedirect(router) {
      try {
        const res = await axios.get('api/admin/auth/check/')
        if (res.data.authenticated) {
          this.user = res.data.user
          this.isAuthenticated = true
          router.push('/admin/dashboard')
        }
      } catch (error) {
        console.warn('Auth check failed:', error)
      }
    },
    async logout() {
      await axios.post('/api/admin/logout/')
      this.user = null
      this.isAuthenticated = false
    },

    async fetchUser() {
      try {
        const res = await axios.get('/api/admin/user/')
        this.user = res.data
        this.isAuthenticated = true
      } catch {
        this.isAuthenticated = false
      }
    },

    async changePassword(payload) {
      /**
       * payload = {
       *   current_password: '...',
       *   new_password: '...'
       * }
       */
      await axios.post('/api/admin/change-password/', payload)
    }
  }
})
