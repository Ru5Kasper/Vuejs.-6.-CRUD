<template>
  <div>
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Управление категориями</h1>
      <p class="mt-2 text-gray-600">Создавайте и управляйте категориями для постов</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Левая колонка: Форма категории -->
      <div class="lg:col-span-1">
        <div class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              {{ editingCategory ? 'Редактирование категории' : 'Создание новой категории' }}
            </h3>
            
            <!-- Форма -->
            <form @submit.prevent="handleSubmit" class="space-y-6">
              <div>
                <label for="category-name" class="block text-sm font-medium text-gray-700 mb-2">
                  Название категории *
                </label>
                <input
                  type="text"
                  id="category-name"
                  v-model="formData.name"
                  required
                  :disabled="isLoading"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
                  placeholder="Введите название категории"
                />
                <p v-if="formError" class="mt-2 text-sm text-red-600">
                  {{ formError }}
                </p>
              </div>

              <div class="flex space-x-3">
                <button
                  type="submit"
                  :disabled="isLoading"
                  class="flex-1 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150 ease-in-out"
                >
                  <svg 
                    v-if="isLoading" 
                    class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" 
                    fill="none" 
                    viewBox="0 0 24 24"
                  >
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{{ editingCategory ? 'Обновить категорию' : 'Создать категорию' }}</span>
                </button>
                
                <button
                  v-if="editingCategory"
                  type="button"
                  @click="cancelEdit"
                  :disabled="isLoading"
                  class="flex-1 inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
                >
                  Отмена
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Подсказка -->
        <div class="mt-6 bg-blue-50 border-l-4 border-blue-400 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-blue-700">
                Категория не может быть удалена, если к ней привязаны посты.
                Сначала удалите все посты этой категории.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Правая колонка: Список категорий -->
      <div class="lg:col-span-1">
        <div class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              Список категорий
            </h3>

            <div v-if="isLoadingCategories" class="text-center py-8">
              <div class="inline-flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="text-gray-600">Загрузка категорий...</span>
              </div>
            </div>

            <div v-else-if="!categories || categories.length === 0" class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
              </svg>
              <p class="mt-2 text-sm text-gray-500">
                Категорий пока нет. Создайте первую категорию.
              </p>
            </div>

            <div v-else class="space-y-3">
              <div 
                v-for="category in categories" 
                :key="category.id"
                class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-150"
              >
                <div>
                  <div class="flex items-center">
                    <span class="text-lg font-medium text-gray-900">{{ category.name }}</span>
                    <span 
                      v-if="category.posts_count > 0"
                      class="ml-2 px-2 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800"
                    >
                      {{ category.posts_count }} пост{{ getPostsCountText(category.posts_count) }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-500 mt-1">
                    Создана: {{ formatDate(category.created_at) }}
                  </p>
                </div>
                
                <div class="flex space-x-2">
                  <button
                    @click="handleEdit(category)"
                    class="p-2 text-indigo-600 hover:text-indigo-900 hover:bg-indigo-50 rounded-full transition-colors duration-150"
                    title="Редактировать"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                  <button
                    @click="handleDelete(category)"
                    :disabled="category.posts_count > 0"
                    class="p-2 text-red-600 hover:text-red-900 hover:bg-red-50 rounded-full disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-150"
                    :title="category.posts_count > 0 ? 'Нельзя удалить (есть посты)' : 'Удалить'"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <!-- Заголовок и текст -->
          <div v-if="!showPhraseConfirmation">
            <div class="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900 text-center mb-2">
              Подтверждение удаления
            </h3>
            <p class="text-sm text-gray-500 text-center mb-6">
              {{ categoryToDelete?.posts_count > 0 
                ? `Категория "${categoryToDelete?.name}" содержит ${categoryToDelete?.posts_count} пост(ов). Вы не можете удалить категорию с постами.`
                : `Вы уверены, что хотите удалить категорию "${categoryToDelete?.name}"?`
              }}
            </p>
          </div>

          <!-- Подтверждение фразой (если есть посты) -->
          <div v-else>
            <div class="flex items-center justify-center w-12 h-12 mx-auto bg-yellow-100 rounded-full mb-4">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900 text-center mb-2">
              Опасное действие!
            </h3>
            <p class="text-sm text-gray-500 mb-4">
              Категория "{{ categoryToDelete?.name }}" содержит {{ categoryToDelete?.posts_count }} пост(ов). 
              При удалении категории все связанные посты будут также удалены.
            </p>
            <div class="mb-4">
              <p class="text-sm font-medium text-gray-700 mb-2">
                Для подтверждения введите фразу: <span class="font-bold text-red-600">{{ randomPhrase }}</span>
              </p>
              <input
                type="text"
                v-model="phraseInput"
                placeholder="Введите фразу точно как показано выше"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
              />
              <p v-if="phraseError" class="mt-1 text-sm text-red-600">
                {{ phraseError }}
              </p>
            </div>
          </div>

          <!-- Кнопки -->
          <div class="flex space-x-3">
            <button
              @click="cancelDelete"
              class="flex-1 py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
            >
              Отмена
            </button>
            <button
              @click="confirmDelete"
              :disabled="(showPhraseConfirmation && phraseInput !== randomPhrase) || isDeleting"
              class="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150 ease-in-out"
            >
              <span v-if="isDeleting">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Удаление...
              </span>
              <span v-else>
                {{ showPhraseConfirmation ? 'Удалить всё' : 'Удалить' }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { categoriesApi } from '@/api/categories'

const queryClient = useQueryClient()

// Форма категории
const editingCategory = ref(null)
const formData = ref({ name: '' })
const formError = ref('')

watch(editingCategory, (newVal) => {
  if (newVal) {
    formData.value = { name: newVal.name }
  } else {
    formData.value = { name: '' }
  }
  formError.value = ''
})

// Список категорий
const { data: categories, isLoading: isLoadingCategories } = useQuery({
  queryKey: ['categories'],
  queryFn: () => categoriesApi.getCategories().then(res => res.data)
})

// Мутации
const createMutation = useMutation({
  mutationFn: (categoryData) => categoriesApi.createCategory(categoryData),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['categories'] })
    resetForm()
  },
  onError: (error) => {
    formError.value = error.response?.data?.detail || 'Ошибка при создании категории'
  }
})

const updateMutation = useMutation({
  mutationFn: ({ id, data }) => categoriesApi.updateCategory(id, data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['categories'] })
    resetForm()
  },
  onError: (error) => {
    formError.value = error.response?.data?.detail || 'Ошибка при обновлении категории'
  }
})

// Удаление
const showDeleteModal = ref(false)
const showPhraseConfirmation = ref(false)
const categoryToDelete = ref(null)
const randomPhrase = ref('')
const phraseInput = ref('')
const phraseError = ref('')
const isDeleting = ref(false)

const deleteMutation = useMutation({
  mutationFn: (id) => categoriesApi.deleteCategory(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['categories'] })
    showDeleteModal.value = false
    categoryToDelete.value = null
    phraseInput.value = ''
    randomPhrase.value = ''
    isDeleting.value = false
  },
  onError: (error) => {
    phraseError.value = error.response?.data?.detail || 'Ошибка при удалении категории'
    isDeleting.value = false
  }
})

// Методы
const handleSubmit = () => {
  formError.value = ''
  
  if (editingCategory.value) {
    updateMutation.mutate({ id: editingCategory.value.id, data: formData.value })
  } else {
    createMutation.mutate(formData.value)
  }
}

const resetForm = () => {
  editingCategory.value = null
  formData.value = { name: '' }
  formError.value = ''
}

const cancelEdit = () => {
  resetForm()
}

const handleEdit = (category) => {
  editingCategory.value = category
}

const handleDelete = (category) => {
  categoryToDelete.value = category
  
  if (category.posts_count > 0) {
    showPhraseConfirmation.value = true
    const words = ['удалить', 'категорию', 'посты', 'все', 'навсегда', 'подтвердить']
    randomPhrase.value = Array.from({ length: 3 }, 
      () => words[Math.floor(Math.random() * words.length)]
    ).join(' ')
  } else {
    showPhraseConfirmation.value = false
  }
  
  showDeleteModal.value = true
  phraseInput.value = ''
  phraseError.value = ''
}

const confirmDelete = () => {
  if (showPhraseConfirmation.value) {
    if (phraseInput.value !== randomPhrase.value) {
      phraseError.value = 'Фраза введена неверно'
      return
    }
  }
  
  if (categoryToDelete.value) {
    isDeleting.value = true
    deleteMutation.mutate(categoryToDelete.value.id)
  }
}

const cancelDelete = () => {
  showDeleteModal.value = false
  categoryToDelete.value = null
  phraseInput.value = ''
  randomPhrase.value = ''
  phraseError.value = ''
  showPhraseConfirmation.value = false
  isDeleting.value = false
}

// Вспомогательные функции
const getPostsCountText = (count) => {
  if (count === 1) return ''
  if (count >= 2 && count <= 4) return 'а'
  return 'ов'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const isLoading = computed(() => {
  return createMutation.isPending || updateMutation.isPending
})
</script>