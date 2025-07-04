<template>
  <div class="compose-container">
    <div v-if="!composing">
      <h2>Saved Draft Emails</h2>
      <button @click="startNewEmail">+ New Email</button>
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
          <tr v-for="email in savedDrafts" :key="email.id">
            <td>{{ email.title }}</td>
            <td>{{ email.layout }}</td>
            <td>{{ formatDate(email.created_at) }}</td>
            <td>{{ formatDate(email.updated_at) }}</td>
            <td class="actions">
              <button style="background-color: green;" @click="editDraft(email)">Edit</button>
              <button style="background-color: red;" @click="deleteDraft(email.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>

    <div v-else class="compose-view">
      <div class="compose-header">
        <input v-model="email.title" type="text" placeholder="Enter Email Title" />
        <select v-model="email.layout">
          <option disabled value="">Choose Layout</option>
          <option value="story">Story</option>
          <option value="dialogue">Dialogue</option>
          <option value="tips">Tips</option>
        </select>
        <button @click="saveDraft">Save Draft</button>
        <button @click="togglePreview">
          {{ previewMode ? 'Back to Editor' : 'Preview Email' }}
        </button>
        <button @click="cancelCompose">Cancel</button>
      </div>

      <div v-if="!previewMode">
        <div class="editor-toolbar">
          <button @click="format('bold')"><i class="fas fa-bold"></i></button>
          <button @click="format('italic')"><i class="fas fa-italic"></i></button>
          <button @click="format('heading')"><i class="fas fa-heading"></i></button>
          <button @click="format('quote')"><i class="fas fa-quote-left"></i></button>
          <button @click="format('list')"><i class="fas fa-list-ul"></i></button>
        </div>

        <textarea
          ref="editor"
          v-model="email.content"
          placeholder="Start composing your email..."
        ></textarea>
      </div>

      <EmailPreview
        v-else
        :title="email.title"
        :layout="email.layout"
        :content="email.content"
      />
    </div>
  </div>
</template>

<script>
import EmailPreview from '../components/EmailPreview.vue';

export default {
  name: 'ComposeEmail',
  components: { EmailPreview },
  data() {
    return {
      composing: false,
      previewMode: false,
      email: {
        id: null,
        title: '',
        layout: '',
        content: ''
      },
      savedDrafts: [
        {
          id: 1,
          title: 'Welcome to Cyber Tips!',
          layout: 'tips',
          content: 'Here are 5 ways to avoid scams...',
          created_at: '2025-05-21T10:00:00Z',
          updated_at: '2025-05-22T11:30:00Z'
        },
        {
          id: 2,
          title: 'Story of the Week',
          layout: 'story',
          content: 'Once upon a scam...',
          created_at: '2025-05-22T14:15:00Z',
          updated_at: '2025-05-22T15:45:00Z'
        }
      ]
    };
  },
  methods: {
    startNewEmail() {
      this.email = {
        id: null,
        title: '',
        layout: '',
        content: ''
      };
      this.composing = true;
      this.previewMode = false;
    },
    editDraft(draft) {
      this.email = { ...draft };
      this.composing = true;
      this.previewMode = false;
    },
    cancelCompose() {
      this.composing = false;
    },
    saveDraft() {
      if (!this.email.title || !this.email.layout || !this.email.content) {
        alert('Please fill in all fields.');
        return;
      }

      if (this.email.id) {
        // Update existing
        const index = this.savedDrafts.findIndex(d => d.id === this.email.id);
        if (index !== -1) {
          this.email.updated_at = new Date().toISOString();
          this.savedDrafts[index] = { ...this.email };
        }
      } else {
        // Save new
        this.email.id = Date.now(); // Simulate ID
        this.email.created_at = new Date().toISOString();
        this.email.updated_at = this.email.created_at;
        this.savedDrafts.push({ ...this.email });
      }

      alert('Draft saved.');
      this.composing = false;
    },
    deleteDraft(id) {
      if (confirm('Are you sure you want to delete this draft?')) {
        this.savedDrafts = this.savedDrafts.filter(email => email.id !== id);
      }
    },
    format(type) {
      const textarea = this.$refs.editor;
      const { selectionStart, selectionEnd } = textarea;
      let before = this.email.content.substring(0, selectionStart);
      let selected = this.email.content.substring(selectionStart, selectionEnd);
      let after = this.email.content.substring(selectionEnd);

      switch (type) {
        case 'bold':
          selected = `**${selected || 'bold text'}**`;
          break;
        case 'italic':
          selected = `*${selected || 'italic text'}*`;
          break;
        case 'heading':
          selected = `# ${selected || 'Heading'}`;
          break;
        case 'quote':
          selected = `> ${selected || 'Quote'}`;
          break;
        case 'list':
          selected = `- ${selected || 'List item'}`;
          break;
      }

      this.email.content = before + selected + after;
    },
    togglePreview() {
      this.previewMode = !this.previewMode;
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    }
  }
};
</script>

<style scoped>
.compose-container {
  padding: 1rem;
  color: white;
}
h2 {
    color: #00c6ff
}
.table-section {
  margin-top: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  background: white;
}
.compose-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

input[type="text"], select {
  padding: 0.5rem;
  border: 1px solid #00c6ff;
  border-radius: 9px;
  font-size: 0.9rem;
  flex: 1;
}

.editor-toolbar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.actions {
    display: flex;
    justify-content: space-around;
}
button {
  padding: 0.5rem;
  background-color: #2c5364;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

textarea {
  width: 90%;
  margin: 0 auto;
  min-height: 300px;
  padding: 1rem;
  font-family: monospace;
  font-size: 0.95rem;
  border-radius: 9px;
  border: 1px solid #00c6ff;
  background: #f0f4f8;
  color: #203a43;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  font-size: 12px;
  color: #203a43;
}

th, td {
  padding: 0.75rem;
  border-bottom: 1px solid #ccc;
  text-align: left;
}

th {
  background-color: #2c5364;
  color: white;
}
</style>
