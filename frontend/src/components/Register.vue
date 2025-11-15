<template>
  <div class="register-page">
    <header class="navbar">
      <div class="logo">neuro<span>scan</span></div>
    </header>

    <section class="hero-register">
      <div class="hero-left">
        <img :src="mriImage" alt="MRI Illustration" class="hero-img" />
        <h1 class="hero-title">Early Alzheimer’s Detection with AI</h1>
        <p class="hero-desc">
          Upload MRI scans and let our AI analyze them quickly and accurately. Track cognitive health and receive early insights.
        </p>
      </div>

      <div class="hero-right">
        <v-card class="register-card pa-6 elevation-12">
          <h2 class="card-title mb-4">Create Your Account</h2>
          <v-form ref="registerForm" v-model="valid">
            <v-text-field
              v-model="full_name"
              placeholder="Full Name"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-account"
              class="mb-4"
            />

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
              :rules="[rules.required, rules.min]"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-lock"
              class="mb-4"
            />

            <v-text-field
              v-model="confirmPassword"
              placeholder="Confirm Password"
              type="password"
              :rules="[rules.required, rules.matchPassword]"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-lock-check"
              class="mb-6"
            />

           <div class="buttons-container text-center">
            <v-btn
              color="#a186f7"
              rounded
              :disabled="!valid"
              @click="register"
              class="mb-4"
            >
              Register
            </v-btn>

            <div class="text-center mb-2">or</div>

            <v-btn
              color="white"
              dark
              rounded
              @click="goLogin"
              class="sign-in-btn"
            >
              Sign In
            </v-btn>
          </div>
          </v-form>
        </v-card>
      </div>
    </section>
  </div>
</template>

<script>
import mriImage from "../assets/mri-illustration.jpg"; 
import "../assets/register.css"; 

export default {
  data() {
    return {
      mriImage,
      full_name: "",
      email: "",
      password: "",
      confirmPassword: "",
      valid: false,
      rules: {
        required: (v) => !!v || "This field is required",
        email: (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
        min: (v) => v.length >= 6 || "Password must be at least 6 characters",
        matchPassword: (v) => v === this.password || "Passwords must match",
      },
    };
  },
  methods: {
    async register() {
      if (this.$refs.registerForm.validate()) {
        try {
          const response = await fetch("http://localhost:5002/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              full_name: this.full_name,
              email: this.email,
              password: this.password,
            }),
          });

          const data = await response.json();
          if (response.ok) {
            alert("Account created! Please log in.");
            this.$router.push({ name: "Login" });
          } else {
            alert(data.error);
          }
        } catch (err) {
          alert("Server error. Try again later.");
        }
      }
    },
    goLogin() {
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<style lang="css" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
}

.register-page {
  background: linear-gradient(to right, #fffdf9, #faf8ff);
  min-height: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 5rem;
}

.navbar .logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #b79df8;
}

.navbar .logo span {
  color: #7f73ef;
}

.navbar nav ul {
  list-style: none;
  display: flex;
  gap: 2rem;
}

.navbar nav li {
  cursor: pointer;
  transition: 0.3s;
}

.navbar nav li:hover {
  color: #7f73ef;
}

.hero-register {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4rem;
  padding: 4rem 5rem;
}

.hero-left {
  max-width: 450px;
  text-align: center;
}

.hero-left .hero-img {
  width: 300px;
  border-radius: 1.5rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.12);
  margin-bottom: 2rem;
  transition: transform 0.4s ease;
}

.hero-left .hero-img:hover {
  transform: translateY(-10px);
}

.hero-left .hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.hero-left .hero-desc {
  color: #6a6a6a;
  font-size: 1.1rem;
  line-height: 1.6;
}

.hero-right {
  flex: 1;
  display: flex;
  justify-content: center;
}

.register-card {
  width: 100%;
  height:670px;
  max-width: 450px;
  border-radius: 2rem;
  background: white;
  box-shadow: 0 25px 50px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.register-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 30px 60px rgba(0,0,0,0.15);
}

.register-card .card-title {
  font-weight: 700;
  font-size: 1.8rem;
  text-align: center;
}

.register-card .v-text-field input {
  border-radius: 2rem;
  background: #f8f7ff;
  padding: 0.8rem 1rem;
}

.register-card .v-text-field input:focus {
  box-shadow: 0 0 8px rgba(127, 115, 239, 0.3);
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

.v-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
}

.v-btn.primary {
  background-color: #a186f7 !important;
  color: white !important;
}

.v-btn.primary:hover {
  background-color: #a186f7 !important;
}

.sign-in-btn {
  color: #7f73ef !important;
  border: 1px solid #7f73ef;
}

.sign-in-btn:hover {
  background-color: #a186f7 !important; 
  color: white !important;
}

.v-btn.secondary {
  background-color: #a186f7 !important;
  color: white !important;
}

.v-btn.secondary:hover {
  background-color: #a186f7 !important;
}

.v-field.v-field--variant-filled {
  border-radius: 2rem;
  margin-top: 3px;;
  padding: 0.5rem;
  background-color: #f8f7ff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.v-field.v-field--variant-filled input {
  border-radius: 2rem;
  padding: 0.5rem 1.2rem;
  font-size: 1rem;
  background: transparent;
  color: #1a1a1a;
}

.v-field.v-field--variant-filled:hover {
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

.v-field.v-field--variant-filled input:focus {
  box-shadow: 0 0 12px rgba(127, 115, 239, 0.4);
  outline: none;
}

.v-field__prepend-inner i {
  color: #7f73ef;
}

.v-field__field {
  border-radius: 2rem;
}

.v-field__outline {
  border-radius: 2rem;
}
.v-field.v-field--variant-filled .v-field__outline {
  display: none !important;
}

@media (max-width: 960px) {
  .hero-register {
    flex-direction: column;
    gap: 2rem;
    padding: 2rem;
  }

  .hero-left, .hero-right {
    max-width: 100%;
  }

  .hero-left .hero-title {
    font-size: 2rem;
  }
}
</style>