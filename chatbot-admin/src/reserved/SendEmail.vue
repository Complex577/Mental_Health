<template>
  <div class="send-emails-view">
    <h2>Draft Emails</h2>
    <div class="table-section">
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Layout</th>
            <th>Created</th>
            <th>Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="email in emails" :key="email.id">
            <td>{{ email.title }}</td>
            <td>{{ email.layout }}</td>
            <td>{{ formatDate(email.created_at) }}</td>
            <td>{{ formatDate(email.updated_at) }}</td>
            <td>
              <button @click="previewEmail(email)">Preview</button>
              <button style="background-color: green;" @click="confirmSend(email)">Send</button>
              <button style="background-color: red;" @click="deleteDraft(email.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Preview -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>Mobile Preview</h3>
        <div class="mobile-frame">
          <EmailPreview
            :title="selectedEmail.title"
            :layout="selectedEmail.layout"
            :content="selectedEmail.content"
          />
        </div>
        <button @click="closeModal">Close</button>
      </div>
    </div>

    <!-- Send Dialog -->
    <div v-if="sendDialog" class="modal-overlay" @click.self="sendDialog = false">
      <div class="modal-content send-dialog">
        <h3>Send Email</h3>
        <div class="options">
        <label><input type="radio" v-model="sendOption" value="all" /> Send to All</label>
        <label><input type="radio" v-model="sendOption" value="some" /> Send to Selected</label>
        <label><input type="radio" v-model="sendOption" value="exclude" /> Send to All Except</label>
        </div>

        <div v-if="sendOption !== 'all'" class="email-selector">
          <input
            type="text"
            placeholder="Search subscribers by email..."
            v-model="searchTerm"
            @input="simulateSearch"
          />
          <div class="search-results">
            <div
              v-for="subscriber in filteredSubscribers"
              :key="subscriber.email"
              class="search-result-item"
            >
              <input
                type="checkbox"
                :value="subscriber.email"
                :checked="selectedEmailList.includes(subscriber.email)"
                @change="toggleEmailSelection(subscriber.email)"
              />
              <span>{{ subscriber.email }}</span>
              <small>{{ formatDate(subscriber.created_at) }}</small>
            </div>
          </div>
          <div class="selected-emails">
            <h4>Selected Emails:</h4>
            <ul>
              <li v-for="email in selectedEmailList" :key="email">{{ email }}</li>
            </ul>
          </div>
        </div>

        <button @click="sendEmail">Confirm Send</button>
        <button @click="sendDialog = false">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import EmailPreview from '../components/EmailPreview.vue';

export default {
  name: 'SendEmails',
  components: { EmailPreview },
  data() {
    return {
      emails: [
        {
          id: 1,
          title: 'Kua makini mwezi huu!',
          layout: 'story',
          content: '***Ni wakati amabo taasisi nyingi nchini Tanzania zimetangaza nafasi za kazi, kua makini usitume pesa ili kupata pesa!***',
          created_at: '2025-05-20T12:34:00Z',
          updated_at: '2025-05-22T15:10:00Z'
        },
        {
          id: 2,
          title: 'Viungo (Links) Hatarishi!',
          layout: 'tips',
          content: '- Hua vina majina yasiyoleta maana yakisomwa.',
          created_at: '2025-05-21T09:00:00Z',
          updated_at: '2025-05-23T10:45:00Z'
        }
      ],
      showModal: false,
      selectedEmail: null,
      sendDialog: false,
      emailToSend: null,
      sendOption: 'all',
      searchTerm: '',
      allSubscribers: [
        { email: 'alice@example.com', created_at: '2025-05-10T10:00:00Z' },
        { email: 'bob@example.com', created_at: '2025-05-11T11:00:00Z' },
        { email: 'charlie@example.com', created_at: '2025-05-12T12:00:00Z' },
        { email: 'dora@example.com', created_at: '2025-05-13T13:00:00Z' }
      ],
      filteredSubscribers: [],
      selectedEmailList: []
    };
  },
  methods: {
    previewEmail(email) {
      this.selectedEmail = email;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedEmail = null;
    },
    confirmSend(email) {
      this.emailToSend = email;
      this.sendDialog = true;
      this.sendOption = 'all';
      this.selectedEmailList = [];
      this.searchTerm = '';
      this.filteredSubscribers = [];
    },
    sendEmail() {
      const targets =
        this.sendOption === 'all'
          ? 'ALL subscribers'
          : this.selectedEmailList.join(', ');

      console.log('Sending email:', this.emailToSend.title);
      console.log('Send option:', this.sendOption);
      console.log('Targeted emails:', targets);

      alert('Email sending simulated. Check console for details.');
      this.sendDialog = false;
    },
    deleteDraft(id) {
      this.emails = this.emails.filter(email => email.id !== id);
    },
    formatDate(datetime) {
      return new Date(datetime).toLocaleString();
    },
    simulateSearch() {
      const term = this.searchTerm.toLowerCase();
      this.filteredSubscribers = this.allSubscribers.filter(s =>
        s.email.toLowerCase().includes(term)
      );
    },
    toggleEmailSelection(email) {
      const index = this.selectedEmailList.indexOf(email);
      if (index === -1) {
        this.selectedEmailList.push(email);
      } else {
        this.selectedEmailList.splice(index, 1);
      }
    }
  }
};
</script>

<style scoped>
.send-emails-view {
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

h2 {
  color: #00c6ff;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  margin-top: 1rem;
  color: #203a43;
}

th,
td {
  padding: 0.75rem;
  border-bottom: 1px solid #ccc;
  text-align: left;
}

th {
  background-color: #2c5364;
  color: rgb(143, 118, 118);
}

button {
  margin-right: 0.5rem;
  padding: 0.3rem 0.6rem;
  background-color: #00c6ff;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(20, 20, 20, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  color: #203a43;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  max-height: 90vh;
  overflow-y: auto;
}

.mobile-frame {
  border: 1px solid #ccc;
  border-radius: 12px;
  padding: 1rem;
  height: 500px;
  overflow-y: auto;
  background-color: #f0f4f8;
  margin-bottom: 1rem;
}

textarea,
input[type="text"] {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.options {
  display: flex;
  margin-bottom: 10px;
  justify-content: center;
  gap: 7px;
  flex-direction: column;
  
}

.search-results {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.5rem;
  background-color: #f8f8f8;
}

.search-result-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.25rem 0;
  font-size: 13px;
}

.search-result-item input {
  margin-right: 0.5rem;
}

.selected-emails {
  margin-top: 1rem;
}

.selected-emails h4 {
  margin-bottom: 0.5rem;
  font-size: 14px;
  color: #2c5364;
}

.selected-emails ul {
  list-style: disc;
  padding-left: 1.5rem;
  font-size: 13px;
  color: #203a43;
}
</style>
