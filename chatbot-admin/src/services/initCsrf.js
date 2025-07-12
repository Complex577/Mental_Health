// admin/src/services/initCsrf.js
import axios from './api'

export async function initCsrf() {
  try {
    const res = await axios.get('/api/admin/csrf/')  // Django view that sets cookie and returns token
    console.log('CSRF Fetched')
  } catch (error) {
    console.error('Failed to fetch CSRF token', error)
  }
}
