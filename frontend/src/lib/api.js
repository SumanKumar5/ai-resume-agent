import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export const runPipeline = (formData) => api.post('/run', formData)
export const getTaskStatus = (taskId) => api.get(`/task/${taskId}`)
export const getRuns = () => api.get('/runs')
export const getRun = (id) => api.get(`/runs/${id}`)
export const getAnalytics = () => api.get('/analytics')
export const downloadPdf = (jobId) => `/api/download/${jobId}`

export default api