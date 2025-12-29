<template>
  <form @submit.prevent="handleSubmit" class="space-y-4 max-w-md mx-auto">
    <div>
      <label for="name" class="block text-sm font-medium text-gray-700">Название категории</label>
      <input
        type="text"
        id="name"
        v-model="form.name"
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
      />
      <div v-if="error" class="text-red-500 text-sm mt-1">{{ error }}</div>
    </div>

    <button
      type="submit"
      class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
    >
      {{ submitText }}
    </button>
  </form>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({ name: '' }),
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['submit'])

const form = ref({ ...props.initialData })

const submitText = computed(() => {
  return props.initialData.id ? 'Обновить категорию' : 'Создать категорию'
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