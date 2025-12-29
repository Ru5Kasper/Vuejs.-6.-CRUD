<template>
  <form @submit.prevent="handleSubmit" class="space-y-6 max-w-2xl mx-auto">
    <div>
      <label for="name" class="block text-sm font-medium text-gray-700">Название поста *</label>
      <input
        type="text"
        id="name"
        v-model="form.name"
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
      />
    </div>

    <div>
      <label for="content" class="block text-sm font-medium text-gray-700">Содержание *</label>
      <textarea
        id="content"
        v-model="form.content"
        required
        rows="6"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
      ></textarea>
    </div>

    <div>
      <label for="image_url" class="block text-sm font-medium text-gray-700"
        >Ссылка на изображение</label
      >
      <input
        type="url"
        id="image_url"
        v-model="form.image_url"
        placeholder="https://example.com/image.jpg"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
      />
    </div>

    <div>
      <label for="category_id" class="block text-sm font-medium text-gray-700">Категория *</label>
      <select
        id="category_id"
        v-model="form.category_id"
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
      >
        <option value="" disabled>Выберите категорию</option>
        <option v-for="category in categories" :key="category.id" :value="category.id">
          {{ category.name }}
        </option>
      </select>
    </div>

    <div v-if="error" class="text-red-500 text-sm p-3 bg-red-50 rounded-md">
      {{ error }}
    </div>

    <div class="flex space-x-4">
      <button
        type="submit"
        class="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      >
        {{ submitText }}
      </button>

      <router-link
        :to="{ name: 'posts' }"
        class="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 text-center"
      >
        Отмена
      </router-link>
    </div>
  </form>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      name: '',
      content: '',
      image_url: '',
      category_id: '',
    }),
  },
  categories: {
    type: Array,
    default: () => [],
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['submit'])

const form = ref({ ...props.initialData })

const submitText = computed(() => {
  return props.initialData.id ? 'Обновить пост' : 'Создать пост'
})

watch(
  () => props.initialData,
  (newVal) => {
    form.value = { ...newVal }
  },
  { deep: true },
)

const handleSubmit = () => {
  emit('submit', form.value)
}
</script>