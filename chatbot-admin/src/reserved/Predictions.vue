<template>
  <div class="predictions-view">
    <h2>Predicted Messages</h2>

    <div class="table-section">
      <table>
        <thead>
          <tr>
            <th>Message</th>
            <th>Predicted</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="msg in messages" :key="msg.id">
            <td>{{ msg.text }}</td>
            <td>
              <span :class="msg.is_spam ? 'spam' : 'not-spam'">
                {{ msg.is_spam ? 'Spam' : 'Ham' }}
              </span>
            </td>
            <td>
              <button class="btn delete" @click="deleteMessage(msg.id)">Delete</button>
              <button class="btn add" @click="openModal(msg)">Add to Training</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL -->
    <div class="modal-overlay" v-if="showModal">
      <div class="modal">
        <h3>Label This Message</h3>
        <p>{{ selectedMessage.text }}</p>
        <div class="actions">
          <button @click="labelMessage('spam')">Spam</button>
          <button @click="labelMessage('ham')">Ham</button>
        </div>
        <button class="close" @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Predictions',
  data() {
    return {
      messages: [
        { id: 1, text: 'Free money waiting for you!', is_spam: true },
        { id: 2, text: 'Meeting rescheduled to 3PM', is_spam: false },
        { id: 3, text: 'Claim your lottery prize now', is_spam: true },
      ],
      showModal: false,
      selectedMessage: null,
    }
  },
  methods: {
    deleteMessage(id) {
      this.messages = this.messages.filter(msg => msg.id !== id);
      // Here you'd make an API call to delete the message from Django
    },
    openModal(msg) {
      this.selectedMessage = msg;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedMessage = null;
    },
    labelMessage(label) {
      // Simulate submitting the labeled message
      console.log(`Submitted for training: "${this.selectedMessage.text}" as ${label}`);
      // Here you'd send the message and label to the Django endpoint

      // Remove from current list after submission
      this.messages = this.messages.filter(msg => msg.id !== this.selectedMessage.id);
      this.closeModal();
    }
  }
}
</script>

<style scoped>
.predictions-view {
  padding: 1rem;
  color: white;
}

.table-section {
  margin-top: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  background: white;
}

table {
  width: 100%;
  border-collapse: collapse;
  color: #203a43;
  font-size: 12px;
}

th, td {
  text-align: left;
  padding: 0.75rem;
  border-bottom: 1px solid rgba(36, 157, 190, 0.2);
}

th {
  background-color: #2c5364;
  color: rgb(143, 118, 118);
}

.spam {
  color: red;
  font-weight: bold;
}

.not-spam {
  color: green;
  font-weight: bold;
}

.btn {
  padding: 0.3rem 0.6rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 11px;
  margin-right: 5px;
}

.delete {
  background-color: #e74c3c;
  color: white;
}

.add {
  background-color: #2980b9;
  color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  color: #203a43;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  text-align: center;
}

.modal h3 {
  margin-bottom: 1rem;
}
h2 {
    color: #00c6ff
}

.actions button {
  margin: 0 10px;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.actions button:first-child {
  background-color: red;
  color: white;
}

.actions button:last-child {
  background-color: green;
  color: white;
}

.close {
  margin-top: 1rem;
  background-color: #ccc;
  color: #2c5364;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
}
</style>
