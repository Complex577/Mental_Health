<template>
  <div class="modal-overlay">
    <div class="modal">
      <div class="header">
        <img src="/assets/logo_final.png">
        <div class="header-buttons">
          <button class="reset-btn" @click="startNewChat">New Chat</button>
          <button class="close-btn" @click="$emit('close')">×</button>
        </div>
      </div>

      <div class="chat-body" ref="chatContainer">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.sender === 'user' ? 'user' : 'bot']"
        >
          <div class="bubble" v-html="renderMarkdown(msg.text)"></div>
        </div>

        <div v-if="isTyping" class="message bot">
          <div class="bubble typing-indicator">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <div class="input-wrapper">
          <textarea
            v-model="newMessage"
            ref="textarea"
            rows="1"
            maxlength="200"
            placeholder="Type your thoughts..."
            @input="autoResize"
            @keyup.enter.exact.prevent="sendMessage"
          ></textarea>
          <button class="send-btn" @click="sendMessage">➤</button>
          <span class="underline"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from "marked";
import axios from '../../services/api'

const SESSION_KEY = "akilitulivu_chat_session";
const SESSION_EXPIRY_KEY = "akilitulivu_chat_session_time";
const EXPIRY_HOURS = 24;

export default {
  emits: ["close"],
  data() {
    return {
      newMessage: "",
      messages: [],
      isTyping: false
    };
  },
  created() {
    const saved = localStorage.getItem(SESSION_KEY);
    const savedTime = localStorage.getItem(SESSION_EXPIRY_KEY);
    const now = new Date().getTime();

    if (saved && savedTime && now - Number(savedTime) < EXPIRY_HOURS * 3600 * 1000) {
      this.messages = JSON.parse(saved);
    } else {
      if (savedTime) {
        alert("Your previous session has expired after 24 hours.");
      }
      this.startNewChat();
    }
  },
  mounted() {
    this.scrollToBottom();
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() === "") return;

      const userText = this.newMessage;
      this.messages.push({ text: userText, sender: "user" });
      this.newMessage = "";
      this.autoResize();
      this.scrollToBottom();
      this.isTyping = true;

      try {
        const history = this.messages.slice(-10);
        const res = await axios.post("/api/chatbot/ask_akili/", {
            message: userText,
            history: history
        });

        const data = res.data;
        this.messages.push({ text: data.response || "Sorry, I couldn’t understand that.", sender: "bot" });
      } catch (error) {
        console.log(error);
        this.messages.push({ text: "Akili is currently unavailable. Please try again later.", sender: "bot" });
        
      } finally {
        this.isTyping = false;
        this.saveSession();
        this.scrollToBottom();
      }
    },

    renderMarkdown(text) {
      return marked.parse(text);
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        container.scrollTop = container.scrollHeight;
      });
    },

    autoResize() {
      const textarea = this.$refs.textarea;
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    },

    saveSession() {
      localStorage.setItem(SESSION_KEY, JSON.stringify(this.messages));
      localStorage.setItem(SESSION_EXPIRY_KEY, Date.now().toString());
    },

    startNewChat() {
      const welcome = {
        text: this.$t("welcome_chat"),
        sender: "bot"
      };
      this.messages = [welcome];
      this.saveSession();
      this.scrollToBottom();
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal {
  background: linear-gradient(to bottom right, #fffafa, #ffe6e6);
  border-radius: 16px;
  width: 1000%;
  max-width: 500px;
  height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.4s ease;
  overflow: hidden;
}

.header {
  padding: 10px 10px;
  width: 92%;
  margin: 5px auto;
  background-color: var(--chat-header);
  color: var(--primary-red);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid var(--primary-red);
  border-radius: 8px;
}
img {
  width: 80px;
  height: 70px;
}
.header-buttons {
  display: flex;
  gap: 10px;
}

.close-btn,
.reset-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  color: var(--primary-red);
  cursor: pointer;
  padding: 0.2rem 0.6rem;
  border-radius: 8px;
  transition: background 0.2s ease;
}
.reset-btn {
  background: var(--primary-red);
  color: white;
}
.close-btn {
  background: white;
  border: 1px solid var(--primary-red);
  color: var(--primary-red);
}
.reset-btn:hover,
.close-btn:hover {
  background: white;
  border: 1px solid var(--primary-red);
  color: var(--primary-red);
}

.chat-body {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  border-top-right-radius: 11px;
  border-top-left-radius: 11px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #fff5f5;
}

.message {
  display: flex;
  max-width: 85%;
  word-wrap: break-word;
}

.message.user {
  align-self: flex-end;
  justify-content: flex-end;
}

.message.bot {
  align-self: flex-start;
  justify-content: flex-start;
}

.bubble {
  background-color: white;
  padding: 10px 15px;
  border-radius: 16px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.user .bubble {
  background-color: var(--primary-red);
  color: white;
  padding: 1px 15px;
  border-bottom-right-radius: 0;
}

.bot .bubble {
  background-color: #fff;
  border-bottom-left-radius: 0;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 10px 15px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.typing-indicator .dot {
  width: 8px;
  height: 8px;
  background-color: var(--primary-red);
  border-radius: 50%;
  animation: bounceDot 1.2s infinite ease-in-out;
}

.typing-indicator .dot:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-indicator .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounceDot {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-6px);
  }
}

.bot .bubble em {
  font-style: italic;
}
.bot .bubble strong {
  font-weight: bold;
}
.bot .bubble a {
  color: var(--primary-red);
  text-decoration: underline;
}
.bot .bubble :deep(blockquote) {
  margin: 0.5rem 0;
  padding: 0.1rem 1rem;
  border-left: 4px solid var(--primary-red);
  background: #fff0f0;
  font-style: italic;
  color: #555;
  border-radius: 8px;
}

.chat-input {
  padding: 8px 2px;
  width: 100%;
  border-top: 1px solid #eee;
}

.input-wrapper {
  position: relative;
  width: 60%;
  margin: 0 auto;
  background: #fff;
  border-radius: 30px;
  border: 1px solid #ccc;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.15);
  padding: 10px 50px 10px 20px;
  display: flex;
  align-items: center;
  transition: box-shadow 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: var(--primary-red);
  box-shadow: 0 0 0 4px rgba(255, 0, 0, 0.15);
}

.input-wrapper textarea {
  width: 100%;
  resize: none;
  border: none;
  outline: none;
  font-size: 1rem;
  line-height: 1.2;
  font-family: Arial, Helvetica, sans-serif;
  background: transparent;
  color: #333;
  min-height: 70px;
  max-height: 80px;
  overflow-y: auto;
}

.input-wrapper .send-btn {
  position: absolute;
  bottom: 10px;
  top: 30x;
  right: 12px;
  background: var(--primary-red);
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  font-size: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.input-wrapper .send-btn:hover {
  background: #8a0000;
  transform: scale(1.05);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(40px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
