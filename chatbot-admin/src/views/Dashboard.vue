<template>
  <div class="dashboard-view">
    <div class="card-grid">
      <div class="card" v-for="(value, key) in stats" :key="key">
        <h3>{{ key }}</h3>
        <h2>{{ value }}</h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {}
    }
  },
  mounted() {
    this.fetchStats()
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get('/api/dashboard-stats/')
        this.stats = response.data
      } catch (error) {
        console.error('Failed to load dashboard stats:', error)
      }
    }
  }
}
</script>

<style scoped>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
}

.card {
  background: linear-gradient(to bottom, #203a43, #2c5364);
  color: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

h2 {
  color: rgb(143, 118, 118);
}
</style>
