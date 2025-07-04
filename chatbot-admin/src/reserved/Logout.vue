<template>
  <div class="profile-container">
    <div class="card profile-card">
      <h2>User Profile</h2>
      <div class="user-info" v-if="authStore.user">
        <p><strong>Name:</strong> {{ authStore.user.name }}</p>
        <p><strong>Email:</strong> {{ authStore.user.email }}</p>
        <p><strong>Joined:</strong> {{ formatDate(authStore.user.joined_at) }}</p>
      </div>
    </div>

    <div class="card password-card">
      <h3>Change Password</h3>
      <form @submit.prevent="submitPasswordChange">
        <input
          type="password"
          v-model="currentPassword"
          placeholder="Current Password"
          required
        />
        <input
          type="password"
          v-model="newPassword"
          placeholder="New Password"
          required
        />
        <input
          type="password"
          v-model="confirmPassword"
          placeholder="Confirm New Password"
          required
        />
        <button type="submit">Update Password</button>
      </form>
      <p v-if="passwordMessage" class="message">{{ passwordMessage }}</p>
    </div>

    <div class="card logout-card">
      <button class="logout-btn" @click="handleLogout">Logout</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import axios from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const passwordMessage = ref('')

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString()
}

async function submitPasswordChange() {
  if (newPassword.value !== confirmPassword.value) {
    passwordMessage.value = 'Passwords do not match.'
    return
  }

  try {
    await axios.post('/api/change-password/', {
      current_password: currentPassword.value,
      new_password: newPassword.value
    })
    passwordMessage.value = 'Password updated successfully.'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (error) {
    passwordMessage.value =
      error.response?.data?.message || 'Error updating password.'
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push('/admin/login')
}
</script>

<style scoped>
.profile-container {
  padding: 2rem;
  color: #203a43;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.profile-card h2,
.password-card h3 {
  color: #00c6ff;
  margin-bottom: 1rem;
}

.user-info p {
  font-size: 14px;
  margin: 0.3rem 0;
}

form input {
  width: 100%;
  padding: 0.6rem;
  margin: 0.5rem 0;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

form button {
  background: #00c6ff;
  color: white;
  padding: 0.5rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 1rem;
}

.message {
  margin-top: 0.5rem;
  font-size: 13px;
  color: #2c5364;
}

.logout-card {
  text-align: right;
}

.logout-btn {
  background: red;
  color: white;
  border: none;
  padding: 0.5rem 1.2rem;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
}
</style>
