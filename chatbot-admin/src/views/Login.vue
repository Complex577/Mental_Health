<template>
  <div class="modal-overlay">
    <transition name="modal-grow" mode="out-in">
      <div class="modal" :class="{ 'shake': error }">
        <div class="header">
          <img src="/assets/logo_final.png" />
          <h3>Mental Health</h3>
        </div>

        <div class="login-form">
          <h3>Admin Pannel</h3>
          <div class="input-group" :class="{ filled: form.email }">
            <label>Email</label>
            <input
              v-model="form.email"
              type="email"
              @focus="focused.email = true"
              @blur="focused.email = false"
            />
            <span class="underline" :class="{ active: focused.email || form.email }"></span>
          </div>

          <div class="input-group" :class="{ filled: form.password }">
            <label>Password</label>
            <input
              v-model="form.password"
              type="password"
              @focus="focused.password = true"
              @blur="focused.password = false"
            />
            <span class="underline" :class="{ active: focused.password || form.password }"></span>
          </div>

          <div class="remember-container">
            <input type="checkbox" v-model="form.remember" id="remember" />
            <label for="remember">Remember Me</label>
          </div>

          <button :disabled="!form.email || !form.password || loading" @click="login">
            <span v-if="loading" class="spinner"></span>
            Login
          </button>

          <p v-if="error" class="error-msg">{{ error }}</p>
        </div>

        <div class="footer">
          <small>© 2025 PAWHA Mental Health Platform</small>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { useAuthStore } from '../store/auth.js'
import { useRouter } from 'vue-router'
import axios from '../services/api'

export default {
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    return {
      authStore,
      router
    }
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
        remember: false
      },
      focused: {
        email: false,
        password: false
      },
      loading: false,
      error: ''
    }
  },
  mounted() {
  this.checkSession();
    },
    methods: {
      async checkSession() {
        try {
          const res = await axios.get('/api/admin/auth/check/');
          const data = res.data;

          if (data.authenticated) {
            this.router.push('/admin/dashboard');
          }
        } catch (err) {
          console.error('Session check failed:', err);
        }
      },
    async login() {
      this.loading = true
      this.error = ''

      try {
        await this.authStore.login(this.form) // pass remember
        this.router.push('/admin/dashboard')
      } catch (err) {
        this.error = 'Invalid email or password.'
        setTimeout(() => {
          this.error = ''
        }, 3000)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: linear-gradient(to bottom right, #ffffff, #ffe6e6);
  border-radius: 20px;
  padding: 20px;
  width: 80%;
  max-width: 360px;
  height: 75vh;
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
  animation: scaleIn 0.4s ease;
  transition: transform 0.3s;
}
.modal.shake {
  animation: shake 0.4s;
}
.header {
  padding: 10px;
  width: 92%;
  margin: 0 auto 20px;
  background-color: var(--chat-header);
  color: var(--primary-red);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid var(--primary-red);
  border-radius: 8px;
}
img {
  width: 80px;
  height: 70px;
}
.login-form h3 {
  color: var(--primary-red);
  font-weight: bold;
  text-align: center;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.input-group {
  position: relative;
}
.input-group label {
  position: absolute;
  left: 12px;
  top: 12px;
  color: #888;
  font-size: 14px;
  pointer-events: none;
  transition: 0.2s ease;
}
.input-group.filled label,
.input-group input:focus + .underline + label {
  top: -10px;
  left: 10px;
  font-size: 12px;
  color: var(--primary-red);
  background: #fff6f6;
  padding: 0 5px;
}
.input-group input {
  width: 90%;
  margin: 0 auto;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 10px;
  outline: none;
  transition: border 0.3s;
}
.input-group input:focus {
  border-color: var(--primary-red);
  box-shadow: 0 0 0 2px rgba(255, 102, 102, 0.2);
}

.login-form button {
  margin-top: 10px;
  padding: 12px;
  background-color: var(--primary-red);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.1s ease;
}
.login-form button:hover {
  background-color: #e60000;
}
.login-form button:active {
  transform: scale(0.98);
}
.login-form button:disabled {
  background-color: #f4bfbf;
  cursor: not-allowed;
  opacity: 0.7;
}
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 6px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  vertical-align: middle;
}
.error-msg {
  color: red;
  font-size: 14px;
  text-align: center;
}
.modal-grow-enter-active,
.modal-grow-leave-active {
  transition: all 0.9s ease;
}
.modal-grow-enter-from,
.modal-grow-leave-to {
  opacity: 0;
  transform: scale(0.98);
}
@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  50% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
  100% { transform: translateX(0); }
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.remember-container {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: -10px;
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}
.remember-container input[type="checkbox"] {
  accent-color: var(--primary-red);
}
.footer {
  text-align: center;
  margin-top: 15px;
  font-size: 13px;
  color: #888;
}
</style>
