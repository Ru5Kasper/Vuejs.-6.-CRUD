<template>
  <div class="max-w-4xl mx-auto">
    <!-- Заголовок -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">
            {{ isEditMode ? 'Редактирование поста' : 'Создание нового поста' }}
          </h1>
          <p class="mt-2 text-gray-600">
            {{ isEditMode 
              ? 'Редактируйте информацию о посте' 
              : 'Заполните форму для создания нового поста' 
            }}
          </p>
        </div>
        <router-link
          :to="{ name: 'posts' }"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
        >
          ← Назад к списку
        </router-link>
      </div>
    </div>

    <!-- Форма поста -->
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Название поста -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Название поста *
            </label>
            <input
              type="text"
              id="name"
              v-model="formData.name"
              required
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
              placeholder="Введите название поста"
            />
          </div>

          <!-- Содержание -->
          <div>
            <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
              Содержание *
            </label>
            <textarea
              id="content"
              v-model="formData.content"
              required
              rows="6"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
              placeholder="Введите содержание поста"
            ></textarea>
          </div>

          <!-- Ссылка на изображение -->
          <div>
            <label for="image_url" class="block text-sm font-medium text-gray-700 mb-2">
              Ссылка на изображение
            </label>
            <input
              type="url"
              id="image_url"
              v-model="formData.image_url"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
              placeholder="https://example.com/image.jpg"
            />
            <p class="mt-1 text-sm text-gray-500">
              Введите URL изображения или оставьте поле пустым
            </p>
          </div>

          <!-- Категория -->
          <div>
            <label for="category_id" class="block text-sm font-medium text-gray-700 mb-2">
              Категория *
            </label>
            <select
              id="category_id"
              v-model="formData.category_id"
              required
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
            >
              <option value="" disabled>Выберите категорию</option>
              <option 
                v-for="category in categories" 
                :key="category.id" 
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Ошибка -->
          <div v-if="errorMessage" class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Ошибка
                </h3>
                <div class="mt-2 text-sm text-red-700">
                  <p>{{ errorMessage }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Кнопки -->
          <div class="flex justify-between pt-6 border-t border-gray-200">
            <div>
              <button
                v-if="isEditMode"
                type="button"
                @click="handleDelete"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition duration-150 ease-in-out"
              >
                Удалить пост
              </button>
            </div>
            
            <div class="flex space-x-3">
              <router-link
                :to="{ name: 'posts' }"
                class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
              >
                Отмена
              </router-link>
              <button
                type="submit"
                class="inline-flex items-center px-6 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
              >
                {{ isEditMode ? 'Обновить пост' : 'Создать пост' }}
              </button>
            </div>
          </div>
        </form>
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
            Вы уверены, что хотите удалить пост "{{ post?.name }}"?
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
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { postsApi } from '@/api/posts'
import { categoriesApi } from '@/api/categories'

const route = useRoute()
const router = useRouter()
const queryClient = useQueryClient()

const isEditMode = computed(() => route.name === 'post-edit')
const slug = computed(() => route.params.slug)

// Данные формы
const formData = ref({
  name: '',
  content: '',
  image_url: '',
  category_id: ''
})

// Получение категорий
const { data: categories } = useQuery({
  queryKey: ['categories'],
  queryFn: () => categoriesApi.getCategories().then(res => res.data)
})

// Получение данных поста
const { data: post } = useQuery({
  queryKey: ['post', slug],
  queryFn: () => postsApi.getPost(slug.value).then(res => res.data),
  enabled: isEditMode
})

// Обновление формы
watch(post, (newPost) => {
  if (newPost && isEditMode.value) {
    formData.value = {
      name: newPost.name,
      content: newPost.content,
      image_url: newPost.image_url || '',
      category_id: newPost.category_id
    }
  }
}, { immediate: true })

// Мутации
const createMutation = useMutation({
  mutationFn: (postData) => postsApi.createPost(postData),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] })
    // Перенаправляем на список постов после создания
    router.push({ name: 'posts' })
  }
})

const updateMutation = useMutation({
  mutationFn: ({ slug, data }) => postsApi.updatePost(slug, data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] })
    queryClient.invalidateQueries({ queryKey: ['post', slug] })
    // После обновления тоже можно перенаправить на список постов
    router.push({ name: 'posts' })
  }
})

const deleteMutation = useMutation({
  mutationFn: (slug) => postsApi.deletePost(slug),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] })
    router.push({ name: 'posts' })
  }
})

// Состояние UI
const showDeleteModal = ref(false)

// Обработчики
const handleSubmit = () => {
  if (isEditMode.value) {
    updateMutation.mutate({ slug: slug.value, data: formData.value })
  } else {
    createMutation.mutate(formData.value)
  }
}

const handleDelete = () => {
  showDeleteModal.value = true
}

const confirmDelete = () => {
  deleteMutation.mutate(slug.value)
  showDeleteModal.value = false
}

const errorMessage = computed(() => {
  return createMutation.error?.response?.data?.detail || 
         updateMutation.error?.response?.data?.detail ||
         deleteMutation.error?.response?.data?.detail ||
         ''
})
</script>