<template>
  <div>
    <h2 class="title">GAD-7 Anxiety Statistics Overview</h2>

    <Loader v-if="loading" />

    <div v-else class="grid gap-4">
      <!-- Stat Cards -->
      <div class="grid md:grid-cols-4 gap-4">
        <StatCard title="Total Responses" :value="stats.total" icon="fas fa-list" />
        <StatCard title="Average Score" :value="stats.average_score" icon="fas fa-chart-line" />
        <StatCard title="High Risk (≥15)" :value="stats.high_risk" icon="fas fa-exclamation-triangle" />
        <StatCard title="Last Submission" :value="formatDate(stats.last_updated)" icon="fas fa-clock" />
      </div>

      <!-- Charts -->
      <div class="grid md:grid-cols-2 gap-4 mt-4">
        <UserSexBarChart :data="stats.user_sex_chart" title="By User Type & Sex" />
        <AgeGroupBarChart :data="stats.age_group_chart" title="By Age Group" />
      </div>

      <div class="mt-4">
        <ScorePieChart :data="stats.score_ranges" title="Score Ranges" />
      </div>

      <!-- Table -->
      <div class="mt-6">
        <h3 class="table-title">10 Most Recent GAD-7 Assessments</h3>
        <RecentAssessmentTable :rows="stats.recent" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../services/api'

import Loader from '../components/ui/Loader.vue'
import StatCard from '../components/ui/StatCard.vue'
import UserSexBarChart from '../components/charts/UserSexBarChart.vue'
import AgeGroupBarChart from '../components/charts/AgeGroupBarChart.vue'
import ScorePieChart from '../components/charts/ScorePieChart.vue'
import RecentAssessmentTable from '../components/ui/RecentAssessmentTable.vue'

const stats = ref({})
const loading = ref(true)

const fetchStats = async () => {
  try {
    const res = await axios.get('/api/admin/gad7-stats/')
    stats.value = res.data
  } catch (err) {
    console.error('Error fetching GAD-7 stats', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (datetime) => {
  if (!datetime) return 'N/A'
  return new Date(datetime).toLocaleString()
}

onMounted(fetchStats)
</script>

<style scoped>
.title {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-red);
  margin-bottom: 1rem;
}
.table-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: var(--primary-red);
}
</style>
