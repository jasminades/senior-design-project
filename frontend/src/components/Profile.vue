<template>
  <div class="profile-page">
    <header class="navbar">
      <div class="logo">neuro<span>scan</span></div>
      <div class="nav-buttons">
        <v-btn text class="nav-text-btn" @click="$router.push({ name: 'Dashboard' })">
          Back to Dashboard
        </v-btn>
        <v-btn text class="nav-text-btn logout-btn" @click="logout">Logout</v-btn>
      </div>
    </header>

    <section class="hero-profile">
      <v-card class="profile-card mx-auto">
        <h2 class="card-title mb-3">Welcome, {{ fullName || "User" }}</h2>
        <p class="card-subtitle mb-4">
          Below is your analysis history. Each record includes the MRI upload date,
          AI prediction, and confidence score.

        </p>
        <history-table :history="history" />
      </v-card>
    </section>
  </div>
</template>

<script>
import HistoryTable from "./HistoryTable.vue";
import axios from "axios";

export default {
  components: { HistoryTable },
  data() {
    return {
      fullName: localStorage.getItem("full_name") || "User",
      history: [],
    };
  },
  async mounted() {
    await this.fetchHistory();
  },
  methods: {
    logout() {
      this.$router.push({ name: "Login" });
    },
    async fetchHistory() {
      const userId = localStorage.getItem("user_id");
      if (!userId) return;

      try {
        const response = await axios.get(`http://localhost:5001/history/${userId}`);
        this.history = response.data.map(r => ({
          date: r.date,
          prediction: r.prediction,
          confidence: r.confidence,
        }));
      } catch (err) {
        console.error("Error fetching history:", err);
      }
    },
    async runDummyAnalysis() {
      const userId = localStorage.getItem("user_id");
      if (!userId) return;

      try {
        const formData = new FormData();
        formData.append("user_id", userId);

        const response = await axios.post("http://localhost:5001/predict", formData);
        console.log("Prediction result:", response.data);

        await this.fetchHistory();
      } catch (err) {
        console.error("Error running analysis:", err);
      }
    },
  },
};
</script>

<style scoped>
.profile-page * {
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

.navbar .logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #b79df8;
}

.navbar .logo span {
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
  background: none;
  text-transform: none;
}

.nav-text-btn:hover {
  color: #b79df8;
}

.hero-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 2rem;
}

.profile-card {
  width: 80%;
  max-width: 1000px;
  background: linear-gradient(145deg, #f9f9ff, #eef1ff);
  border-radius: 2rem;
  padding: 2.5rem 2rem;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.profile-card:hover {
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

@media (max-width: 960px) {
  .profile-card {
    width: 95%;
    padding: 2rem 1.5rem;
  }

  .navbar {
    padding: 1.5rem 2rem;
  }
}
</style>
