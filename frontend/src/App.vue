<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Навигация -->
    <nav class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <h1 class="text-xl font-bold text-indigo-600">Blog Admin</h1>
            </div>
            <div class="sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                :to="{ name: 'posts' }"
                :class="[
                  $route.name === 'posts' 
                    ? 'border-indigo-500 text-gray-900' 
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
                  'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium'
                ]"
              >
                📝 Посты
              </router-link>
              <router-link
                :to="{ name: 'categories' }"
                :class="[
                  $route.name === 'categories' 
                    ? 'border-indigo-500 text-gray-900' 
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
                  'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium'
                ]"
              >
                🏷️ Категории
              </router-link>
            </div>
          </div>
          <div class="sm:ml-6 sm:flex sm:items-center">
            <span class="text-sm text-gray-500">Админ-панель</span>
          </div>
        </div>
      </div>
    </nav>

    <!-- Контент -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- Футер -->
    <footer class="bg-white shadow-lg mt-8">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <div class="text-center text-sm text-gray-500">
          © 2024 Blog Admin Panel. Все права защищены.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>