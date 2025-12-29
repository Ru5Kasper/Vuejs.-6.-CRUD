import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'
import App from './App.vue'
import router from './router'
import './style.css'

// Создаем приложение
const app = createApp(App)

// Настраиваем Vue Query
VueQueryPlugin.install(app, {
  queryClientConfig: {
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        retry: 1,
        staleTime: 5 * 60 * 1000, // 5 минут
      },
    },
  },
})

// Используем плагины
app.use(createPinia())
app.use(router)

// Монтируем приложение
app.mount('#app')