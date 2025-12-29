<template>
  <div>
    <!-- Заголовок и кнопка создания -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Управление постами</h1>
        <p class="mt-2 text-gray-600">Создавайте, редактируйте и управляйте постами блога</p>
      </div>
      <router-link
        :to="{ name: 'post-create' }"
        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
      >
        Создать пост
      </router-link>
    </div>

    <!-- Поиск -->
    <div class="mb-8">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
        <input
          type="text"
          v-model="searchQuery"
          @input="handleSearch"
          placeholder="Поиск по названию поста..."
          class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
        />
      </div>
    </div>

    <!-- Таблица постов -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div v-if="isLoading" class="p-8 text-center">
        <span class="text-gray-600">Загрузка постов...</span>
      </div>

      <div v-else-if="error" class="p-8 text-center">
        <div class="inline-flex flex-col items-center">
          <svg class="h-12 w-12 text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="text-gray-700 mb-2">Ошибка при загрузке постов</p>
          <button 
            @click="refetch"
            class="text-indigo-600 hover:text-indigo-800 font-medium"
          >
            Попробовать снова
          </button>
        </div>
      </div>

      <div v-else-if="!posts || posts.length === 0" class="p-8 text-center">
        <div class="inline-flex flex-col items-center">
          <svg class="h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="text-gray-700 mb-2">Пока нет ни одного поста</p>
          <router-link
            :to="{ name: 'post-create' }"
            class="text-indigo-600 hover:text-indigo-800 font-medium"
          >
            Создать первый пост
          </router-link>
        </div>
      </div>

      <div v-else>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Изображение
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Название
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Категория
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Дата создания
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Действия
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr 
                v-for="post in posts" 
                :key="post.id"
                class="hover:bg-gray-50 transition-colors duration-150"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex-shrink-0 h-10 w-10">
                    <img 
                      v-if="post.image_url" 
                      :src="post.image_url" 
                      :alt="post.name"
                      class="h-10 w-10 rounded-lg object-cover"
                    />
                    <div v-else class="h-10 w-10 rounded-lg bg-gray-200 flex items-center justify-center">
                      <span class="text-gray-400 text-xs">Нет фото</span>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm font-medium text-gray-900">
                    <router-link
                      :to="{ name: 'post-edit', params: { slug: post.slug } }"
                      class="hover:text-indigo-600 hover:underline transition-colors duration-150"
                    >
                      {{ post.name }}
                    </router-link>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    v-if="post.category"
                    class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-indigo-100 text-indigo-800"
                  >
                    {{ post.category.name }}
                  </span>
                  <span v-else class="text-gray-500 text-sm">Без категории</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(post.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex space-x-3">
                    <router-link
                      :to="{ name: 'post-edit', params: { slug: post.slug } }"
                      class="text-indigo-600 hover:text-indigo-900 transition-colors duration-150"
                      title="Редактировать"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                    </router-link>
                    <button
                      @click="handleDelete(post)"
                      class="text-red-600 hover:text-red-900 transition-colors duration-150"
                      title="Удалить"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Информация о количестве -->
        <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <div class="flex justify-between items-center">
            <div class="text-sm text-gray-700">
              Показано <span class="font-medium">{{ posts.length }}</span> постов
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <div class="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 text-center mb-2">
            Подтверждение удаления
          </h3>
          <p class="text-sm text-gray-500 text-center mb-6">
            Вы уверены, что хотите удалить пост "{{ postToDelete?.name }}"?
            Это действие нельзя отменить.
          </p>
          <div class="flex space-x-3">
            <button
              @click="showDeleteModal = false"
              class="flex-1 py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
            >
              Отмена
            </button>
            <button
              @click="confirmDelete"
              class="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition duration-150 ease-in-out"
            >
              Удалить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDebounceFn } from '@vueuse/core'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { postsApi } from '@/api/posts'

const router = useRouter()
const queryClient = useQueryClient()

// Поиск
const searchQuery = ref('')
const debouncedSearch = useDebounceFn((value) => {
  searchQuery.value = value
}, 500)

const handleSearch = (event) => {
  debouncedSearch(event.target.value)
}

// Получение постов
const { 
  data: posts, 
  isLoading, 
  error, 
  refetch 
} = useQuery({
  queryKey: ['posts', searchQuery],
  queryFn: () => postsApi.getPosts(searchQuery.value).then(res => res.data),
  staleTime: 60000
})

// Удаление поста
const showDeleteModal = ref(false)
const postToDelete = ref(null)

const deleteMutation = useMutation({
  mutationFn: (slug) => postsApi.deletePost(slug),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] })
    showDeleteModal.value = false
    postToDelete.value = null
  }
})

const handleDelete = (post) => {
  postToDelete.value = post
  showDeleteModal.value = true
}

const confirmDelete = () => {
  if (postToDelete.value) {
    deleteMutation.mutate(postToDelete.value.slug)
  }
}

// Форматирование даты
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>