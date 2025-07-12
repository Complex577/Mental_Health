import axios from 'axios'

// Utility to get a cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Your Django dev server
  withCredentials: true,
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  }
})

// Intercept requests to add CSRF token from cookie
instance.interceptors.request.use(config => {
  const token = getCookie('csrftoken')
  if (token && ['post', 'put', 'patch', 'delete'].includes(config.method)) {
    config.headers['X-CSRFToken'] = token
  }
  return config
})

export default instance
