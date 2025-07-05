<template>
  <div class="container">
    <div class="header">
      <img src="/assets/logo_final.png" />
    </div>
    <hr />
    <LanguageSelector />
    <h1 class="heading">{{ $t('title') }}</h1>
    <p>{{ $t('welcome') }}</p>
    <div class="grid">
      <DashboardCard :icon="'/assets/akili-assessment.png'" :title="$t('assessment_title')" :description="$t('PHQ9_description')" @click="modal = 'assessment'" />
      <DashboardCard :icon="'/assets/akili-chat.png'" :title="$t('nlp_chat')" :description="$t('nlp_description')" @click="openNLPModal" />
      <DashboardCard :icon="'/assets/akili-edu.png'" :title="$t('rule_chat')" :description="$t('rule_description')" @click="modal = 'rule'" />
      <DashboardCard :icon="'/assets/akili-assessment.png'" :title="$t('experts')" :description="$t('experts_description')" @click="modal = 'experts'" />
    </div>

    <!-- Modals -->
    <transition name="bot-modal">
      <NLPChatModal v-if="modal === 'nlp'" @close="modal = null" />
    </transition>
    <AssessmentModal v-if="modal === 'assessment'" @close="modal = null" />
    <AssessmentGAD7 v-if="modal === 'assessmentGAD7'" @close="modal = null" />
    <RuleChatModal v-if="modal === 'rule'" @close="modal = null" />
    <ExpertsModal v-if="modal === 'experts'" @close="modal = null" />

    <!-- Floating Bot Icon -->
    <div class="floating-bot" @click="openNLPModal">
      <div class="tooltip">
        <strong>{{ $t('nlp_chat') }}</strong><br />
        <small>{{ $t('nlp2_description') }}</small>
      </div>
      <svg
        class="bot-icon"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 64 64"
        width="48"
        height="48"
      >
        <circle cx="32" cy="32" r="30" fill="#ff6b6b" />
        <path
          d="M24 26c-2.2 0-4 1.8-4 4s1.8 4 4 4 4-1.8 4-4-1.8-4-4-4zm16 0c-2.2 0-4 1.8-4 4s1.8 4 4 4 4-1.8 4-4-1.8-4-4-4z"
          fill="#fff"
        />
        <path
          d="M32 44c4 0 7.5-2.5 8.7-6H23.3c1.2 3.5 4.7 6 8.7 6z"
          fill="#fff"
        />
      </svg>
    </div>
  </div>

  <div class="footer">
    <small style="text-align: center;">&copy; {{ new Date().getFullYear() }}. <a href="https://pawha.org" target="_blank">PAWHA</a> Mental Health.</small>
  </div>
</template>

<script>
import LanguageSelector from "@/components/LanguageSelector.vue";
import DashboardCard from "@/components/DashboardCard.vue";
import AssessmentModal from "@/components/overlays/AssessmentModal.vue";
import AssessmentModal2 from "@/components/overlays/AssessmentModal2.vue";
import AssessmentGAD7 from "@/components/overlays/AssessmentGAD7.vue";
import NLPChatModal from "@/components/overlays/NLPChatModal.vue";
import RuleChatModal from "@/components/overlays/RuleChatModal.vue";
import ExpertsModal from "@/components/overlays/ExpertsModal.vue";

export default {
  components: {
    LanguageSelector,
    DashboardCard,
    AssessmentModal,
    AssessmentModal2,
    AssessmentGAD7,
    NLPChatModal,
    RuleChatModal,
    ExpertsModal,
  },
  data() {
    return {
      modal: null,
      botSound: null,
    };
  },
  mounted() {
    this.botSound = new Audio('/sounds/bot-open.mp3');
  },
  methods: {
    openNLPModal() {
      this.modal = 'nlp';
      if (this.botSound) {
        this.botSound.currentTime = 0;
        this.botSound.play();
      }
    },
  },
};
</script>

<style scoped>
.container {
  padding: 1rem 2rem;
  max-width: 1100px;
  margin: auto;
}

p {
  text-align: center;
}

.header img {
  width: 80px;
  height: 70px;
}

.heading {
  text-align: center;
  font-size: 2.2rem;
  color: var(--primary-red);
  margin-bottom: 2rem;
}

hr {
  border: none;
  height: 2px;
  background-color: var(--primary-red);
  box-shadow: 2px 10px 8px 10px var(--light-pink);
}

.footer {
  text-align: center;
  margin-top: 2rem;
}
@media (min-width: 50px) {
  .grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(360px, 1fr));
    gap: 20px;
  }
}
.grid > * {
  height: 180px;
  width: 85%;
  max-width: 400px;
}
.grid {
  
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 20px;
}

/* Floating Bot Styles */
.floating-bot {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 999;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: transform 0.3s ease;
  animation: wave 2.5s infinite ease-in-out;
}

.floating-bot:hover {
  transform: translateY(-4px);
}

.bot-icon {
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  transition: transform 0.2s ease;
}
.bot-icon:hover {
  transform: scale(1.05);
}

/* Tooltip styling */
.tooltip {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 0.6rem 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  white-space: nowrap;
  opacity: 0;
  transform: translateX(10px);
  pointer-events: none;
  transition: all 0.3s ease;
  font-size: 14px;
  color: #333;
  position: absolute;
  right: 60px;
  bottom: 10px;
  max-width: 240px;
}

.floating-bot:hover .tooltip {
  opacity: 1;
  transform: translateX(0);
  pointer-events: auto;
}
/* Wave animation */
@keyframes wave {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}
</style>
