import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../components/loginPage.vue'
import ComparaisonFile from '../components/comparaisonFile.vue'
import AdminPage from '../components/adminPage.vue'
import signup from '../components/signinPage.vue'
import store from '../store'

const routes = [
  {
    path: '/signup',
    name: 'signup',
    component: signup
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/compare',
    name: 'Compare',
    component: ComparaisonFile,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.currentUser
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.meta.requiresAdmin

  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (requiresAdmin && store.state.currentUser?.role !== 'admin') {
    next('/login')
  } else {
    next()
  }
})

export default router