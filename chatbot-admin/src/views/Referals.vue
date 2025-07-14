<template>
  <div class="referrals">
    <h2 class="title">Referral Summary</h2>

    <div v-if="loading" class="loader-container">
      <Loader />
    </div>

    <div v-else>
      <StatCard label="Total Referrals" :value="summary.total" icon="📍" />

      <BarChart
        :chart-data="assessmentChart"
        title="Referrals by Assessment Type"
      />

      <h3 class="subtitle">Referral Details</h3>

      <table class="referral-table">
        <thead>
          <tr>
            <th>Assessment Type</th>
            <th>Score</th>
            <th>Location</th>
            <th>Contact Info</th>
            <th>Description</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in referrals" :key="item.id">
            <td>{{ item.assessment_type }}</td>
            <td :class="{ danger: item.score >= 15 }">{{ item.score }}</td>
            <td>{{ item.location }}</td>
            <td>{{ item.contact_info }}</td>
            <td>{{ item.description || '-' }}</td>
            <td>{{ new Date(item.created_at).toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination Controls -->
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="page === 1 || pageLoading">
            <span v-if="pageLoading && paginationDirection === 'prev'" class="loader-inline"></span>
            <span v-else>Previous</span>
        </button>

        <span>Page {{ page }} of {{ totalPages }}</span>

        <button @click="nextPage" :disabled="page === totalPages || pageLoading">
            <span v-if="pageLoading && paginationDirection === 'next'" class="loader-inline"></span>
            <span v-else>Next</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '../services/api'
import Loader from '../components/ui/Loader.vue'
import StatCard from '../components/ui/StatCard.vue'
import BarChart from '../components/charts/BarChart.vue'

const referrals = ref([])
const summary = ref({ total: 0, breakdown: {} })
const loading = ref(true)
const page = ref(1)
const totalPages = ref(1)

// Pagination specific loading state and direction
const pageLoading = ref(false)
const paginationDirection = ref(null)

const fetchSummaryAndData = async () => {
  loading.value = true
  try {
    const res = await axios.get(`/api/admin/referrals/?page=${page.value}`)
    referrals.value = res.data.results
    summary.value = {
      total: res.data.total,
      breakdown: res.data.breakdown
    }
    totalPages.value = res.data.total_pages
  } finally {
    loading.value = false
  }
}

// Separate pagination API call: only fetch page data, not summary or breakdown
const fetchPage = async (direction) => {
  if (pageLoading.value) return
  pageLoading.value = true
  paginationDirection.value = direction

  try {
    const res = await axios.get(`/api/admin/referrals/?page=${page.value}`)
    referrals.value = res.data.results
  } finally {
    pageLoading.value = false
    paginationDirection.value = null
  }
}

const nextPage = async () => {
  if (page.value < totalPages.value && !pageLoading.value) {
    page.value++
    await fetchPage('next')
  }
}

const prevPage = async () => {
  if (page.value > 1 && !pageLoading.value) {
    page.value--
    await fetchPage('prev')
  }
}

const assessmentChart = computed(() => {
  const labels = Object.keys(summary.value.breakdown)
  const data = Object.values(summary.value.breakdown)

  return {
    labels: [...labels],
    datasets: [
      {
        label: 'Referrals',
        backgroundColor: '#f87171',
        data: [...data]
      }
    ]
  }
})

onMounted(fetchSummaryAndData)
</script>

<style scoped>
.referrals {
  padding: 1rem;
}
.title {
  font-size: 1.5rem;
  color: var(--primary-red);
  margin-bottom: 1rem;
}
.subtitle {
  margin-top: 2rem;
  color: var(--primary-red);
}
.referral-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  margin-top: 1rem;
}
th, td {
  padding: 8px;
  border-bottom: 1px solid #eee;
}
th {
  background-color: var(--light-pink);
  color: var(--primary-red);
}
.danger {
  color: red;
  font-weight: bold;
}
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  gap: 1rem;
}
button {
  background: var(--primary-red);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}
/* Small inline spinner */
.loader-inline {
  border: 2px solid transparent;
  border-top: 2px solid white; /* spinner color, adjust to button text color */
  border-right: 2px solid white;
  border-radius: 50%;
  width: 14px;
  height: 14px;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}

/* Keyframes for spinning */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>
