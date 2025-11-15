import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import Dashboard from './components/Dashboard.vue'
import Profile from './components/Profile.vue'
import StartingPage from './components/StartingPage.vue'
import PredictionsDetails from './components/PredictionsDetails.vue'

const routes = [
  { path: '/', redirect: '/start' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/start', name: 'Starting Page', component: StartingPage },
  { path: '/predictions', name: 'Prediction Details', component: PredictionsDetails },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
