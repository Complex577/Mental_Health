<template>
  <div class="dashboard">
    <h1 class="title">Admin Dashboard</h1>

    <div class="stats-cards">
      <StatCard
        title="Total PHQ-9 Assessments"
        :value="summary.phq9.total"
        icon="🧠"
      />
      <StatCard
        title="Total GAD-7 Assessments"
        :value="summary.gad7.total"
        icon="😰"
      />
      <StatCard
        title="Total SDQ Assessments"
        :value="summary.sdq.total"
        icon="👶"
      />
      <StatCard
        title="Total Referrals"
        :value="summary.referrals.total"
        icon="📍"
      />
    </div>

    <div class="charts-section">
      <div class="chart-box">
        <BarChart
          :chart-data="summary.phq9.score_distribution"
          title="PHQ-9 Score Distribution"
        />
      </div>

      <div class="chart-box">
        <BarChart
          :chart-data="summary.gad7.score_distribution"
          title="GAD-7 Score Distribution"
        />
      </div>

      <div class="chart-box">
        <BarChart
          :chart-data="summary.sdq.score_distribution"
          title="SDQ Score Distribution"
        />
      </div>

      <div class="chart-box">
        <BarChart
          :chart-data="summary.referrals.breakdown"
          title="Referrals by Assessment Type"
        />
      </div>
    </div>

    <div class="recent-section">
      <h2>Recent High Risk Assessments (Score ≥ 15)</h2>
      <table class="recent-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Score</th>
            <th>Location</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in summary.recent_high_risk" :key="item.id">
            <td>{{ item.assessment_type }}</td>
            <td class="danger">{{ item.score }}</td>
            <td>{{ item.location }}</td>
            <td>{{ new Date(item.created_at).toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../services/api'
import StatCard from '../components/ui/StatCard.vue'
import BarChart from '../components/charts/BarChart.vue'

const summary = ref({
  phq9: { total: 0, score_distribution: { labels: [], datasets: [] } },
  gad7: { total: 0, score_distribution: { labels: [], datasets: [] } },
  sdq: { total: 0, score_distribution: { labels: [], datasets: [] } },
  referrals: { total: 0, breakdown: { labels: [], datasets: [] } },
  recent_high_risk: []
})

const fetchDashboard = async () => {
  try {
    const res = await axios.get('/api/admin/dashboard/')
    summary.value = res.data
  } catch (error) {
    console.error('Failed to fetch dashboard data', error)
  }
}

onMounted(fetchDashboard)
</script>

<style scoped>
.dashboard {
  padding: 1rem;
  max-width: 1200px;
  margin: auto;
}
.title {
  font-size: 2rem;
  color: var(--primary-red);
  margin-bottom: 1.5rem;
  text-align: left;
}
.stats-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  gap: 16px;
  margin-bottom: 1.5rem;
}
.stats-cards > * {
  flex: 1 1 180px;
  max-width: 220px;
}
.chart-box {
  width: 48%;
  min-height: 300px;
  margin-bottom: 2rem;
}
.referral-breakdown {
  width: 100%;
}
.charts-section {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.recent-section {
  margin-top: 3rem;
}
.recent-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
th {
  text-align: left;
  padding: 8px;
  background: var(--light-pink);
  color: var(--primary-red);
}
td {
  padding: 8px;
  border-bottom: 1px solid #eee;
}
.danger {
  color: red;
  font-weight: bold;
}
</style>
