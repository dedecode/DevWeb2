import axios from 'axios'

const API_BASE_URL = 'http://localhost:8001/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/users/token/refresh/`, {
            refresh: refreshToken
          })
          
          const { access } = response.data
          localStorage.setItem('access_token', access)
          
          return api(originalRequest)
        } catch (refreshError) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }

    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (userData) => api.post('/users/register/', userData),
  login: (credentials) => api.post('/users/login/', credentials),
}

export const tasksAPI = {
  list: (params) => api.get('/tasks/', { params }),
  create: (taskData) => api.post('/tasks/', taskData),
  update: (id, taskData) => api.put(`/tasks/${id}/`, taskData),
  delete: (id) => api.delete(`/tasks/${id}/`),
  get: (id) => api.get(`/tasks/${id}/`),
}

export const dailySummariesAPI = {
  list: (params) => api.get('/summaries/daily/', { params }),
  create: (summaryData) => api.post('/summaries/daily/', summaryData),
  update: (id, summaryData) => api.put(`/summaries/daily/${id}/`, summaryData),
  delete: (id) => api.delete(`/summaries/daily/${id}/`),
  get: (id) => api.get(`/summaries/daily/${id}/`),
  currentWeek: () => api.get('/summaries/daily/current_week/'),
  lastWeek: () => api.get('/summaries/daily/last_week/'),
}

export const weeklySummariesAPI = {
  list: (params) => api.get('/summaries/weekly/', { params }),
  create: (summaryData) => api.post('/summaries/weekly/', summaryData),
  update: (id, summaryData) => api.put(`/summaries/weekly/${id}/`, summaryData),
  delete: (id) => api.delete(`/summaries/weekly/${id}/`),
  get: (id) => api.get(`/summaries/weekly/${id}/`),
}

export default api