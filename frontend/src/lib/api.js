import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' }
})

export function setAuthToken(token){
  if(token) api.defaults.headers.common['Authorization'] = `Token ${token}`
  else delete api.defaults.headers.common['Authorization']
}

export default api
