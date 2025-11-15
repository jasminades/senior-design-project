<template>
  <div class="login-page">
    <header class="navbar">
      <div class="logo">neuro<span>scan</span></div>
    </header>
    <section class="hero-login">
      <div class="hero-left">
        <v-card class="login-card pa-7 elevation-12">
          <h2 class="card-title mb-4">Welcome Back!</h2>
          <v-form ref="loginForm" v-model="valid">
            <v-text-field
              v-model="email"
              placeholder="Email"
              :rules="[rules.required, rules.email]"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-email"
              class="mb-4"
            />

            <v-text-field
              v-model="password"
              placeholder="Password"
              type="password"
              :rules="[rules.required]"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-lock"
              class="mb-4"
            />

            <div class="buttons-container text-center">
              <v-btn
                color="#a186f7"
                rounded
                :disabled="!valid"
                @click="login"
                class="mb-4"
              >
                Login
              </v-btn>

              <div class="text-center mb-2">or</div>

              <v-btn
                color="white"
                dark
                rounded
                @click="goRegister"
                class="sign-in-btn"
              >
                Create an account
              </v-btn>
            </div>
          </v-form>
        </v-card>
      </div>

      <div class="hero-right">
        <v-img
          :src="mriImage"
          alt="MRI Illustration"
          width="300"
          height="300"
          contain
          class="hero-img mb-4"
        />
        <h1 class="hero-title">AI-Driven Early Alzheimer’s Detection</h1>
        <p class="hero-desc">
          Upload MRI scans and let our AI analyze them quickly and accurately.
          Track cognitive health and get early insights.
        </p>
      </div>
    </section>
  </div>
</template>

<script>
import mriImage from "../assets/mri-illustration.jpg";
export default {
  data() {
    return {
      mriImage,
      email: "",
      password: "",
      valid: false,
      rules: {
        required: (v) => !!v || "This field is required",
        email: (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      },
    };
  },
  methods: {
    async login() {
      if (this.$refs.loginForm.validate()) {
        try {
          const response = await fetch("http://localhost:5002/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: this.email, password: this.password }),
          });

          const data = await response.json();
          if (response.ok) {
            localStorage.setItem("user_id", data.user.id);
            localStorage.setItem("full_name", data.user.full_name);
            this.$router.push({ path: "/dashboard" });
          } else {
            alert(data.error);
          }
        } catch {
          alert("Server error. Try again later.");
        }
      }
    },
    forgotPassword() {
      console.log("Redirect to forgot password page");
    },
    goRegister() {
      this.$router.push({ name: "Register" });
    },
  },
};
</script>

<style scoped>
.hero-login {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 4rem;
  padding: 4rem 5rem;
}

.hero-left {
  flex: 0 0 auto;
  display: flex;
  justify-content: center;
}

.login-card {
  width: 500px;
  border-radius: 2rem;
  background: white;
  box-shadow: 0 25px 50px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 30px 60px rgba(0,0,0,0.15);
}

.login-card .v-text-field input {
  border-radius: 2rem;
  background: #f8f7ff;
  padding: 0.8rem 1rem;
}

.card-title {
  font-weight: 700;
  font-size: 1.8rem;
  text-align: center;
  margin-bottom: 1rem;
}

.v-btn {
  border-radius: 2rem !important;
  width: 200px !important;
  height: 48px !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  text-transform: none !important;
  transition: all 0.3s ease !important;
  display: inline-flex !important;
  justify-content: center !important;
  align-items: center !important;
}

.sign-in-btn {
  color: #7f73ef !important;
  border: 1px solid #7f73ef;
}

.sign-in-btn:hover {
  background-color: #a186f7 !important; 
  color: white !important;
}

.hero-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-img {
  width: 300px;
  border-radius: 1.5rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.12);
  margin-bottom: 2rem;
  transition: transform 0.4s ease;
}

.hero-img:hover {
  transform: translateY(-10px);
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.3;
  text-align: center;
}

.hero-desc {
  color: #6a6a6a;
  font-size: 1.1rem;
  line-height: 1.6;
  text-align: center;
}

@media (max-width: 960px) {
  .hero-login {
    flex-direction: column;
    gap: 2rem;
    padding: 2rem;
  }

  .hero-left,
  .hero-right {
    max-width: 100%;
  }

  .hero-title {
    font-size: 2rem;
  }

  .login-card {
    width: 100%;
  }
}
</style>
