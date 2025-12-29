import apiClient from './axios'

export const categoriesApi = {
  getCategories() {
    return apiClient.get('/categories')
  },

  getCategory(id) {
    return apiClient.get(`/categories/${id}`)
  },

  createCategory(categoryData) {
    return apiClient.post('/categories', categoryData)
  },

  updateCategory(id, categoryData) {
    return apiClient.put(`/categories/${id}`, categoryData)
  },

  deleteCategory(id) {
    return apiClient.delete(`/categories/${id}`)
  }
}