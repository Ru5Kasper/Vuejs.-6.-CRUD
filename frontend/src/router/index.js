import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: { name: 'posts' }
  },
  {
    path: '/posts',
    name: 'posts',
    component: () => import('@/views/PostsView.vue')
  },
  {
    path: '/posts/create',
    name: 'post-create',
    component: () => import('@/views/PostFormView.vue')
  },
  {
    path: '/posts/:slug/edit',
    name: 'post-edit',
    component: () => import('@/views/PostFormView.vue'),
    props: true
  },
  {
    path: '/categories',
    name: 'categories',
    component: () => import('@/views/CategoriesView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router