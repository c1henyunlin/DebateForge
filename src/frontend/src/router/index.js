import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/angle-generation',
    name: 'AngleGeneration',
    component: () => import('../views/AngleGeneration.vue')
  },
  {
    path: '/debate',
    name: 'Debate',
    component: () => import('../views/Debate.vue')
  },
  {
    path: '/report/:sessionId',
    name: 'Report',
    component: () => import('../views/Report.vue')
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/History.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
