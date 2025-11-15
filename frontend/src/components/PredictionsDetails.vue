<template>
  <div class="details-page">
    <header class="navbar">
      <div class="logo">neuro<span>scan</span></div>
      <div class="nav-buttons">
        <v-btn text class="nav-text-btn" @click="$router.push({ name: 'Dashboard' })">
          Back to Dashboard
        </v-btn>
        <v-btn text class="nav-text-btn logout-btn" @click="logout">
          Logout
        </v-btn>
      </div>
    </header>

    <section class="hero-details">
      <v-card class="details-card mx-auto">
        <h2 class="card-title mb-3">Prediction Details</h2>
        <p class="card-subtitle mb-6">
          View your original MRI scan, AI-generated heatmap, prediction label, and additional notes.
        </p>

        <v-row>
          <v-col cols="12" md="6">
            <h3 class="subtitle mb-2">Original MRI</h3>
            <v-img
              :src="prediction.original_image_path"
              class="rounded-xl image-box"
              height="280"
              contain
            />
          </v-col>

          <v-col cols="12" md="6">
            <h3 class="subtitle mb-2">Heatmap</h3>
            <v-img
              :src="prediction.heatmap_image_path"
              class="rounded-xl image-box"
              height="280"
              contain
            />
          </v-col>
        </v-row>

        <v-divider class="my-6"></v-divider>

        <v-row>
          <v-col cols="12" md="6">
            <p><strong>Label:</strong> {{ prediction.prediction_label }}</p>
            <p><strong>Confidence:</strong> {{ prediction.prediction_confidence }}%</p>
          </v-col>

          <v-col cols="12" md="6">
            <p><strong>Date:</strong> {{ prediction.created_at }}</p>
            <p><strong>Model Version:</strong> {{ prediction.model_version }}</p>
          </v-col>
        </v-row>

        <v-card class="notes-card pa-4 rounded-lg mt-6">
          <h3 class="subtitle mb-2">Notes</h3>

          <p v-if="!editingNotes" class="note-text">
            {{ prediction.notes || "No notes added." }}
          </p>

          <v-textarea
            v-if="editingNotes"
            v-model="notesDraft"
            rows="4"
            outlined
            class="mt-2"
          ></v-textarea>

          <div class="mt-3">
            <v-btn
              v-if="!editingNotes"
              color="primary"
              @click="startEditing"
            >
              Edit Notes
            </v-btn>

            <v-btn
              v-if="editingNotes"
              color="success"
              class="mr-2"
              @click="saveNotes"
            >
              Save
            </v-btn>

            <v-btn
              v-if="editingNotes"
              color="grey"
              @click="cancelEditing"
            >
              Cancel
            </v-btn>
          </div>
        </v-card>
      </v-card>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      prediction: {},
      editingNotes: false,
      notesDraft: "",
    };
  },

  async created() {
    const id = this.$route.params.id;

    const res = await axios.get(`http://localhost:5001/api/predictions/${id}`);
    this.prediction = res.data;
    this.notesDraft = this.prediction.notes;
  },

  methods: {
    logout() {
      this.$router.push({ name: "Login" });
    },

    startEditing() {
      this.editingNotes = true;
    },

    cancelEditing() {
      this.editingNotes = false;
      this.notesDraft = this.prediction.notes;
    },

    async saveNotes() {
      const id = this.$route.params.id;

      await axios.post(
        `http://localhost:5001/api/predictions/${id}/update-notes`,
        { notes: this.notesDraft }
      );

      this.prediction.notes = this.notesDraft;
      this.editingNotes = false;
    },
  },
};
</script>

<style scoped>
.details-page * {
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
  margin: 0;
  padding: 0;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 5rem;
  background: linear-gradient(to right, #fffdf9, #faf8ff);
  border-bottom: 1px solid #e0e0e0;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #b79df8;
}

.logo span {
  color: #7f73ef;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

.nav-text-btn {
  color: #7f73ef;
  font-weight: 600;
  font-size: 1rem;
  text-transform: none;
}

.nav-text-btn:hover {
  color: #b79df8;
}

.hero-details {
  padding: 4rem 2rem;
  display: flex;
  justify-content: center;
}

.details-card {
  width: 85%;
  max-width: 1000px;
  background: linear-gradient(145deg, #f9f9ff, #eef1ff);
  border-radius: 2rem;
  padding: 2.5rem 2rem;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.details-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.12);
}

.card-title {
  font-weight: 700;
  font-size: 1.8rem;
  color: #4a4a7b;
}

.card-subtitle {
  font-size: 1rem;
  color: #555;
  line-height: 1.6;
}

.subtitle {
  font-weight: 600;
  font-size: 1.1rem;
  color: #4a4a7b;
}

.image-box {
  border: 2px solid #eceaff;
  box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}

.notes-card {
  background: #fafaff;
  border: 1px solid #e6e1ff;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.note-text {
  color: #555;
  font-size: 0.95rem;
  line-height: 1.5;
}

@media (max-width: 960px) {
  .details-card {
    width: 95%;
    padding: 2rem 1.5rem;
  }

  .navbar {
    padding: 1.5rem 2rem;
  }
}
</style>
