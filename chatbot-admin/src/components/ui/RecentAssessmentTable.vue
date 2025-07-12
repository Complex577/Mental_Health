<template>
  <table class="assessment-table">
    <thead>
      <tr>
        <th>User Type</th>
        <th>Sex</th>
        <th>Age Group</th>
        <th>Score</th>
        <th>Date</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, i) in rows" :key="i">
        <td>{{ row.user_type }}</td>
        <td>{{ row.sex }}</td>
        <td>{{ row.age_group }}</td>
        <td :class="{ danger: row.score >= 15 }">{{ row.score }}</td>
        <td>{{ new Date(row.created_at).toLocaleString() }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
defineProps(['rows'])
</script>

<style scoped>
.assessment-table {
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
