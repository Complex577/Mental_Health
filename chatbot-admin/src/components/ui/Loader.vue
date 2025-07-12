<template>
  <div class="loader-wrapper">
    <div class="spinner"></div>
    <p>Loading data...</p>
  </div>
</template>

<style scoped>
.loader-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: var(--primary-red);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-red);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
