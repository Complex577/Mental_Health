<template>
  <div class="modal-overlay">
    <div class="modal">
      <h2>{{ $t('assessment') }}</h2>
      

      <!-- Progress Bar -->
      <div class="progress-wrapper">
        <div class="progress-text">{{ step }} / {{ questions.length }}</div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: (step / questions.length * 100) + '%' }"></div>
        </div>
      </div>
      

      <!-- Question -->
      <transition name="fade">
        <div class="question" v-if="step < questions.length">
          <P class="guide">{{ $t('assessment_guide') }}</P>
          <p>{{ questions[step].text }}</p>
          <div class="options">
            <button v-for="(option, index) in questions[step].options" :key="index" @click="select(option.score)">
              {{ option.text }}
            </button>
          </div>
        </div>
      </transition>

      <!-- Result -->
      <transition name="slide">
        <div class="result" v-if="step >= questions.length">
          <p class="score">Your Score: {{ totalScore }} / 27</p>
          <p v-if="totalScore <= 7" class="recomendations good">😊 You're doing well. Keep caring for your mind.</p>
          <p v-else-if="totalScore <= 18" class="recomendations average">😐 You may be under some stress. Take action early.</p>
          <p v-else class="recomendations bad">😟 You're likely facing high stress or anxiety. Please seek support.</p>
        </div>
      </transition>

      <!-- Close Button -->
      <div class="actions">
        <button @click="close">{{ $t('close') }}</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  emits: ["close"],
  data() {
    return {
      step: 0,
      totalScore: 0,
      questions: [
        { text: this.$t('PHQ-9_1'), options: this.opts() },
        { text: this.$t('PHQ-9_2'), options: this.opts() },
        { text: this.$t('PHQ-9_3'), options: this.opts() },
        { text: this.$t('PHQ-9_4'), options: this.opts() },
        { text: this.$t('PHQ-9_5'), options: this.opts() },
        { text: this.$t('PHQ-9_6'), options: this.opts() },
        { text: this.$t('PHQ-9_7'), options: this.opts() },
        { text: this.$t('PHQ-9_8'), options: this.opts() },
        { text: this.$t('PHQ-9_9'), options: this.opts() },
      ]
    };
  },
  methods: {
    opts() {
      return [
        { text: this.$t('PHQ-Option_1'), score: 0 },
        { text: this.$t('PHQ-Option_2'), score: 1 },
        { text: this.$t('PHQ-Option_3'), score: 2 },
        { text: this.$t('PHQ-Option_4'), score: 3 },
      ];
    },
    select(score) {
      this.totalScore += score;
      this.step++;
    },
    close() {
      this.$emit("close");
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}
.modal {
  background: linear-gradient(to bottom right, #ffffff, #ffe6e6);
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
  animation: scaleIn 0.4s ease;
}

h2 {
  margin-top: 0;
  color: var(--primary-red);
  text-align: center;
}

/* Progress Bar */
.progress-wrapper {
  margin-bottom: 1.5rem;
}
.progress-text {
  text-align: center;
  font-weight: bold;
  margin-bottom: 6px;
}
.progress-bar {
  background-color: #f1c6c6;
  border-radius: 10px;
  height: 12px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background-color: var(--primary-red);
  transition: width 0.3s ease;
}

.question p {
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 1rem;
}
.question .guide {
  margin: 3px 0;
  padding: 3px 6px;
  border-left: 4px solid var(--primary-red);
  background: #fff0f0;
  font-style: italic;
  font-size: 14px;
  color: #555;
  border-radius: 8px;
}
.recomendations {
  margin: 3px 0;
  padding: 3px 6px;
  background: #fff0f0;
  font-style: italic;
  font-size: 14px;
  
  color: #555;
  border-radius: 8px;
}
.good {
  background-color: rgb(146, 192, 146);
  border-left: 5px solid green;
  border-right: 5px solid green;
  
}
.average {
  border-left: 4px solid var(--primary-red);
  border-right: 4px solid var(--primary-red);
}
.bad {
  border-left: 4px solid var(--primary-red);
  border-right: 4px solid var(--primary-red);
}
.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.options button {
  background-color: #fff0f0;
  border: 1px solid var(--primary-red);
  padding: 10px 15px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.options button:hover {
  background-color: var(--primary-red);
  color: white;
}
.score {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-red);
  margin-bottom: 1rem;
}
.result p {
  font-size: 1rem;
  text-align: center;
}
.actions {
  text-align: center;
  margin-top: 20px;
}
.actions button {
  padding: 10px 20px;
  background-color: var(--primary-red);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.slide-enter-active {
  transition: transform 0.4s ease;
}
.slide-enter-from {
  transform: translateY(20px);
  opacity: 0;
}

@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}
@keyframes scaleIn {
  from {transform: scale(0.9); opacity: 0;}
  to {transform: scale(1); opacity: 1;}
}
</style>
