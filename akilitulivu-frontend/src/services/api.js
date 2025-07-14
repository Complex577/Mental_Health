// admin/src/services/api.js
import axios from 'axios'

const instance = axios.create({
  baseURL: 'https://mental-health-eaap.onrender.com',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  }
})


export default instance
