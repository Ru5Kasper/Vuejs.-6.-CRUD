import apiClient from './axios'

export const postsApi = {
  getPosts(search = '') {
    const params = search ? { search } : {}
    return apiClient.get('/posts', { params })
  },

  getPost(slug) {
    return apiClient.get(`/posts/${slug}`)
  },

  createPost(postData) {
    return apiClient.post('/posts', postData)
  },

  updatePost(slug, postData) {
    return apiClient.put(`/posts/${slug}`, postData)
  },

  deletePost(slug) {
    return apiClient.delete(`/posts/${slug}`)
  }
}