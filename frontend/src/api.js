import axios from 'axios'

const api = axios.create({
  baseURL: '',
  timeout: 30000,
})

export const fetchHealth       = () => api.get('/api/health')
export const fetchBuses        = () => api.get('/api/buses')
export const fetchLiveBuses    = () => api.get('/api/live-buses')
export const fetchBus          = (id) => api.get(`/api/buses/${id}`)
export const fetchRoutes       = () => api.get('/api/routes')
export const fetchRouteStops   = (id) => api.get(`/api/routes/${id}/stops`)
export const fetchStops        = () => api.get('/api/stops')
export const fetchRisk         = () => api.get('/api/risk')
export const fetchBusRisk      = (id, date) => api.get(`/api/risk/${id}`, { params: { date } })
export const fetchTraffic      = (id) => api.get(`/api/traffic/${id}`)
export const fetchAltRoutes    = (id) => api.get(`/api/alternate-routes/${id}`)
export const fetchAltBuses     = (id, date) => api.get(`/api/alternate-buses/${id}`, { params: { date } })
export const fetchRecommendation = (id, date) => api.get(`/api/recommendation/${id}`, { params: { date } })
export const fetchAlerts       = (date) => api.get('/api/alerts', { params: { date } })
export const fetchMLRisk       = (date, hour) => api.get('/api/ml/risk', { params: { date, hour } })
export const fetchMLBusRisk    = (id, date, hour) => api.get(`/api/ml/risk/${id}`, { params: { date, hour } })
export const postMLPredict     = (body) => api.post('/api/ml/predict', body)
export const postPredict       = (body) => api.post('/api/predict', body)

export default api
