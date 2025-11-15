<template>
  <div class="app">
    <header class="navbar">
      <div class="logo">neuro<span>scan</span></div>
      <nav>
        <ul>
          <li>Services</li>
          <li>Detection</li>
          <li>Treatement</li>
          <li>About us</li>
        </ul>
      </nav>
    </header>

    <section class="hero">
      <div class="hero-text">
        <h1>Early Alzheimer’s and Dementia Detection with AI</h1>

        <p class="description">
          Upload MRI scans and let our AI analyze them quickly and accurately. Track cognitive health and receive early insights.
        </p>

        <div class="buttons">
          <button class="start-btn" @click="$router.push({ name: 'Register' })">Start Detection →</button>
        </div>
      </div>

      <div class="hero-image">
        <img src="../assets/mri-illustration.jpg" alt="3D hand with flowers" />
      </div>
    </section>

    <v-container class="mt-12">
      <v-row justify="center" align="stretch" dense>
        <v-col cols="12" md="4" class="mb-6">
          <v-card class="pa-6 feature-card">
            <v-icon color="primary" size="48">mdi-brain</v-icon>
            <h3 class="font-weight-bold mt-4 mb-2">AI-Powered Analysis</h3>
            <p>Deep learning analyzes MRI scans to detect early signs of dementia accurately.</p>
          </v-card>
        </v-col>
        <v-col cols="12" md="4" class="mb-6">
          <v-card class="pa-6 feature-card">
            <v-icon color="primary" size="48">mdi-calendar-clock</v-icon>
            <h3 class="font-weight-bold mt-4 mb-2">Track Progress</h3>
            <p>Maintain a record of your scans and predictions over time.</p>
          </v-card>
        </v-col>
        <v-col cols="12" md="4" class="mb-6">
          <v-card class="pa-6 feature-card">
            <v-icon color="primary" size="48">mdi-lock-check</v-icon>
            <h3 class="font-weight-bold mt-4 mb-2">Secure & Private</h3>
            <p>All data is stored securely, and your privacy is our top priority.</p>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-container class="mt-16">
      <v-row justify="center">
        <v-col cols="12" md="10">
          <h2 class="text-center font-weight-bold mb-12">How It Works</h2>
          <v-timeline>
            <v-timeline-item
              color="primary"
              icon="mdi-upload"
            >
              <h3 class="font-weight-bold">Upload MRI</h3>
              <p>Select your MRI scan and upload it securely to the platform.<br></br></p>
            </v-timeline-item>

            <v-timeline-item
              color="primary"
              icon="mdi-robot"
            >
              <h3 class="font-weight-bold">AI Analysis</h3>
              <p>Our AI model analyzes the scan and predicts potential dementia stages.</p>
            </v-timeline-item>

            <v-timeline-item
              color="primary"
              icon="mdi-chart-line"
            >
              <h3 class="font-weight-bold">View History</h3>
              <p>Monitor your cognitive health trends and confidence scores over time.<br></br></p>
            </v-timeline-item>
          </v-timeline>
        </v-col>
      </v-row>
    </v-container>

    <v-container class="mt-16">
      <h2 class="text-center font-weight-bold mb-12">What Users Say</h2>
      <v-row justify="center" dense>
        <v-col cols="12" md="4" class="mb-6">
          <v-card class="pa-6 testimonial-card">
            <p>"The AI predictions helped me understand my risks early."</p>
            <strong>- John D.</strong>
          </v-card>
        </v-col>
        <v-col cols="12" md="4" class="mb-6">
          <v-card class="pa-6 testimonial-card">
            <p>"Easy to use and secure. I can track my MRI results over time."</p>
            <strong>- Jane D.</strong>
          </v-card>
        </v-col>
        <v-col cols="12" md="4" class="mb-6">
          <v-card class="pa-6 testimonial-card">
            <p>"Great insights and a calm, friendly interface. Highly recommended!"</p>
            <strong>- Jeremy D.</strong>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-container
        class="text-center my-16 py-12"
        style="background: linear-gradient(135deg, #d1c4f3, #ac97de); border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);"
        >
        <h2 class="font-weight-bold mb-6" style="font-size: 2.5rem; line-height: 1.3; color: white;">
            Start your journey to early detection today
        </h2>

        <v-hover v-slot="{ hover }">
            <v-btn
            :elevation="hover ? 12 : 6"
            color="white"
            dark
            large
            rounded
            class="px-8 py-4"
            @click="$router.push({ name: 'Register' })"
            style="transition: all 0.3s ease;"
            >
            Sign Up Now
            </v-btn>
        </v-hover>

        <p class="mt-6 mb-0" style="color: #333; font-size: 1.1rem; max-width: 600px; margin-left: auto; margin-right: auto;">
            Upload MRI scans, get AI-powered insights, and track cognitive health over time. Early detection has never been easier.
        </p>
    </v-container>
  </div>
</template>

<script>
import "../assets/startingpage.css"; 
</script>



