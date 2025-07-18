import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'
import AdminLayout from '../layouts/Admin.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import axios from '../services/api'

const routes = [
  { path: '/login', component: Login },

  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', component: Dashboard }
    ]
  },

  { path: '/:catchAll(.*)', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ Global Navigation Guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Check session only if not already authenticated
  if (!authStore.isAuthenticated) {
    try {
      const res = await axios.get('api/admin/auth/check/', { credentials: 'include' })
      const data = res.data;

      if (data.authenticated) {
        authStore.user = data.user
        authStore.isAuthenticated = true
      } else {
        authStore.isAuthenticated = false
      }
    } catch (err) {
      console.error('Session check failed:', err)
      authStore.isAuthenticated = false
    }
  }

  const isAuth = authStore.isAuthenticated

  const isLoginPage = to.path === '/login'
  const isProtectedRoute = to.path.startsWith('/admin')

  if (!isAuth && isProtectedRoute) {
    // Not authenticated: redirect to login
    return next('/login')
  }

  if (isAuth && isLoginPage) {
    // Already authenticated: redirect to dashboard
    return next('/admin/dashboard')
  }

  return next()
})

export default router
