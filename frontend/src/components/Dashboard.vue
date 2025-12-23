<template>
  <div class="dashboard-page">
    <header class="navbar">
      <div class="logo">neuro<span>scan</span></div>
      <div class="nav-buttons">
        <v-btn text class="nav-text-btn" @click="$router.push({ name: 'Profile' })">Profile</v-btn>
        <v-btn text class="nav-text-btn" @click="logout">Logout</v-btn>
      </div>
    </header>

    <section class="hero-dashboard">
      <v-card class="upload-card pa-7 elevation-12 mx-auto">
        <h2 class="card-title mb-4 text-center">Upload MRI for Analysis</h2>

        <div
          class="dropzone"
          @dragover.prevent
          @dragenter.prevent
          @drop.prevent="handleDrop"
        >
          <div v-if="filePreview" class="preview-container">
            <v-img :src="filePreview" max-width="300" max-height="300" contain />
          </div>
          <v-icon v-else size="60" color="#b3a7f5">mdi-upload</v-icon>

          <p v-if="!filePreview">Drag & Drop your MRI file here</p>
          <p v-else>File Selected: <strong>{{ fileName }}</strong></p>

          <v-btn color="#b3a7f5" class="mt-5" @click="browseFile" small>
            Browse Files
          </v-btn>
          <input ref="fileInput" type="file" hidden accept="image/*" @change="handleFile" />
        </div>

        <div class="model-selector mt-4 text-center">
        <span class="selector-label">Choose Model:</span>
        <v-btn-toggle v-model="selectedModelObject" mandatory>
          <v-btn
            v-for="option in modelOptions"
            :key="option.value"
            :value="option.value"
            class="model-btn"
            rounded
            depressed
            color="#f0f0ff"
            :class="{ 'selected-btn': selectedModelObject === option.value }"
          >
            {{ option.label }}
          </v-btn>
        </v-btn-toggle>
      </div>

        <v-btn
          v-if="filePreview && !loading"
          color="#b3a7f5"
          block
          class="mt-4"
          @click="analyzeFile"
        >
          Analyze
        </v-btn>

        <div v-if="loading" class="text-center mt-3">
          <v-progress-circular :size="50" :width="5" indeterminate color="#7f73ef" />
          <p>Analyzing MRI image...</p>
        </div>

        <v-fade-transition>
          <div v-if="result" class="mt-5 text-center">
            <v-card class="pa-4 elevation-4 result-card mx-auto">
              <v-icon size="36" color="#7f73ef" class="mb-2">mdi-brain</v-icon>
              <h3 class="text-subtitle-1 font-weight-bold mb-1">Analysis Result</h3>
              <p><strong>Prediction:</strong> {{ result.prediction }}</p>
              <p><strong>Confidence:</strong> {{ result.confidence.toFixed(1) }}%</p>
              <v-btn
                color="#7f73ef"
                class="mt-1 text-caption px-3 py-2"
                style="width: 130px; border-radius: 10px;"
                v-if="result"
                @click="$router.push({ name: 'PredictionDetails', params: { id: result.prediction_id } })"
              >
                View Details
              </v-btn>

            </v-card>
          </div>

          
        </v-fade-transition>

        <div v-if="error" class="mt-4 text-center">
          <v-alert type="error" class="text-body-2 pa-2">{{ error }}</v-alert>
        </div>
      </v-card>

      <div class="info-cards-container mt-6 mx-auto">
        <v-card class="info-card pa-4 mb-4">
          <h3 class="card-title mb-2">Quick Tips</h3>
          <ul>
            <li>Make sure your MRI image is clear and properly cropped. It should be of size <b>64x64</b> for <b>CNN Model</b>, and <b>224x224</b> for <b>Transfer Learning Model</b>.</li>
            <li>The file should be of type <i>JPG</i> or <i>PNG</i>.</li>
            <li>File size should not exceed 10MB.</li>
            <li>Deep learning will analyze brain regions for early Alzheimer's detection and most likely dementia stage.</li>
            <li>Analysis will be completed in approximately 5–10 seconds, depending on server load.</li>
            <li>Files are processed securely and stored only on your <i>Profile page</i>. 
          Click <b>View Details</b> to see the generated heatmap.</li>
          </ul>
        </v-card>

        <v-card class="info-card pa-4">
          <h3 class="card-title mb-2">Important Notice</h3>
          <p>
            NeuroScan is an experimental tool and should <b>not</b> be used for actual medical diagnosis. Please consult a qualified healthcare professional for accurate guidance.
          </p>
        </v-card>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      file: null,
      fileName: null,
      filePreview: null,
      result: null,
      error: null,
      loading: false,
      selectedModelObject: "cnn", 
      modelOptions: [
        { label: "CNN (64x64)", value: "cnn" },
        { label: "TL (224x224)", value: "transfer" }
      ],
    };
  },

  methods: {
    handleDrop(e) {
      const file = e.dataTransfer.files[0];
      if (file) this.previewFile(file);
    },
    browseFile() {
      this.$refs.fileInput.click();
    },
    handleFile(e) {
      const file = e.target.files[0];
      if (file) this.previewFile(file);
    },
    previewFile(file) {
      this.file = file;
      this.fileName = file.name;
      const reader = new FileReader();
      reader.onload = (e) => (this.filePreview = e.target.result);
      reader.readAsDataURL(file);
      this.result = null;
      this.error = null;
    },
    async analyzeFile() {
      if (!this.file) return;
      this.loading = true;
      this.result = null;
      this.error = null;

      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("user_id", localStorage.getItem("user_id"));
      formData.append("model_type", this.selectedModelObject);


      try {
        const response = await axios.post("/predict", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        await new Promise((r) => setTimeout(r, 1500));
        this.result = response.data;
      } catch  {
        console.error("An error occurred during analysis.");
      } finally {
        this.loading = false;
      }
    },
    logout() {
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<style scoped>
.dashboard-page * {
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
  color: linear-gradient(to right, #fffdf9, #faf8ff);;
}

.nav-buttons v-btn {
  margin-left: 1rem;
}

.nav-text-btn {
  color: #7f73ef;
  background: none;
  font-weight: 600;
  font-size: 1rem;
  text-transform: none;
}
.nav-text-btn:hover {
  color: #b79df8;
}

.nav-text-btn::after {
  content: attr(data-label);
  position: absolute;
  left: 0;
  right: 0;
  color: black;
  background: linear-gradient(to right, #fffdf9, #faf8ff);
  -webkit-text-fill-color: transparent;
  pointer-events: none;
}

.nav-text-btn:hover::after {
  color: #b79df8;
}

.model-btn {
  margin-right: 20px;
  margin-left: 25px;
}

.hero-dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 2rem;
  gap: 2rem;
}

.upload-card {
  width: 80%; 
  height: 1000px;
  max-width: 1200px;
  border-radius: 2rem;
  background: white;
  box-shadow: 0 25px 50px rgba(0,0,0,0.1);
  transition: all 0.4s ease;
}

.upload-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 30px 60px rgba(0,0,0,0.15);
}

.dropzone {
  border: 2px dashed #b3a7f5;
  border-radius: 2rem;
  height: 500px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  background-color: #f8f7ff;
  transition: all 0.4s ease;
  min-height: 250px;
}

.dropzone:hover {
  background-color: #eef1ff;
  transform: scale(1.02);
}

.preview-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.result-card {
  border-radius: 1.5rem;
  background-color: #f9f9ff;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  width: 100%;
  margin-top: 10px;
}

.info-cards-container {
  width: 100%;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin: 2rem auto 0 auto;
}

.info-card {
  border-radius: 1.8rem;
  background: linear-gradient(145deg, #f9f9ff, #eef1ff);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 1.5rem 2rem;
  border-left: 6px solid #7f73ef;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.info-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.card-title {
  font-weight: 700;
  font-size: 1.4rem;
  margin-bottom: 0.75rem;
  color: #4a4a7b;
}

.info-card ul {
  list-style: disc inside;
  color: #555;
  line-height: 1.6;
}

.info-card p {
  color: #555;
  line-height: 1.6;
  font-size: 1rem;
}

@media (max-width: 600px) {
  .info-card {
    padding: 1rem 1.2rem;
  }
}

@media (max-width: 960px) {
  .upload-card,
  .info-cards-container {
    width: 100%;
  }
}
</style>
