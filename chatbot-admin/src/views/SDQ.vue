<template>
  <div class="sdq-dashboard">
    <h2 class="title">Strengths and Difficulties Questionnaire (SDQ) - Child Assessment</h2>

    <Loader v-if="loading" />

    <div v-else class="dashboard-content">
      <!-- Stat Cards -->
      <div class="stats-grid">
        <StatCard title="Total Assessments" :value="stats.total" icon="check-circle" />
        <StatCard title="Average Score" :value="stats.average_score" icon="bar-chart-2" />
        <StatCard title="High Risk (≥ 17)" :value="stats.high_risk" icon="alert-triangle" />
        <StatCard title="Last Updated" :value="formatDate(stats.last_updated)" icon="clock" />
      </div>

      <!-- Charts -->
      <div class="charts-grid">
        <div class="chart-section">
          <UserSexBarChart :data="stats.user_sex_chart" title="User Type and Sex Distribution" />
        </div>
        <div class="chart-section">
          <AgeGroupBarChart :data="stats.age_group_chart" title="Age Group Distribution" />
        </div>
      </div>

      <div class="chart-section pie">
        <ScorePieChart :data="stats.score_ranges" title="Score Range Breakdown" />
      </div>

      <!-- Table -->
      <div class="raw-table">
        <h3 class="table-title">10 Most Recent SDQ Assessments</h3>
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

const formatDate = (d) => d ? new Date(d).toLocaleString() : 'N/A'

onMounted(async () => {
  try {
    const res = await axios.get('/api/admin/sdq-stats/')
    stats.value = res.data
  } catch (err) {
    console.error('Failed to fetch SDQ stats', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.sdq-dashboard {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.6s ease-in;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-red);
  margin-bottom: 1.5rem;
  text-align: center;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  gap: 1rem;
}

.stats-grid > * {
  flex: 1 1 180px;
  max-width: 220px;
}

.charts-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  gap: 1rem;
}

.chart-section {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
  padding: 1rem;
  flex: 1 1 300px;
  max-width: 500px;
  width: 100%;
}

.pie {
  max-width: 700px;
  margin: 0 auto;
  width: 100%;
  text-align: center;
}

.raw-table {
  background: #fff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.07);
  overflow-x: auto;
}

.table-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: var(--primary-red);
}

/* Responsive behavior */
@media (max-width: 768px) {
  .stats-grid,
  .charts-grid {
    flex-direction: column;
    align-items: center;
  }

  .stats-grid > *,
  .chart-section,
  .pie {
    width: 100%;
    max-width: 100%;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
