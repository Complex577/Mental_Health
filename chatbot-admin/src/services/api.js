// admin/src/services/api.js
import axios from 'axios'

const instance = axios.create({
  baseURL: 'https://mental-health-eaap.onrender.com', // your Django server URL
  withCredentials: true,            // important to send cookies
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  }
})

// Automatically include CSRF token if present
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('csrfToken')
  if (token && ['post', 'put', 'patch', 'delete'].includes(config.method)) {
    config.headers['X-CSRFToken'] = token
  }
  return config
})

export default instance
