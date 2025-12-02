import api, { setAuthToken } from './api'

const TOKEN_KEY = 'univ_token'

export function saveToken(token){
  localStorage.setItem(TOKEN_KEY, token)
  setAuthToken(token)
}

export function getToken(){
  return localStorage.getItem(TOKEN_KEY)
}

export function clearToken(){
  localStorage.removeItem(TOKEN_KEY)
  setAuthToken(null)
}

export async function login(username, password){
  const resp = await api.post('/auth/login/', { username, password })
  const token = resp.data.token
  saveToken(token)
  return resp.data
}

export async function logout(){
  try{
    await api.post('/auth/logout/')
  }catch(e){ /* ignore */ }
  clearToken()
}
