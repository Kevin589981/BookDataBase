import axios from 'axios'

// 简单的Electron环境检测
const isElectron = () => {
  if (typeof window !== 'undefined') {
    return !!(window.process && window.process.type) || 
           !!(window.require) || 
           navigator.userAgent.toLowerCase().indexOf('electron') > -1
  }
  return false
}

// API配置
const BACKEND_URL = 'http://localhost:8000'
const PROXY_PATH = '/api'
const baseURL = isElectron() ? BACKEND_URL : PROXY_PATH

// 只在开发环境或需要调试时显示配置信息
const DEBUG = process.env.NODE_ENV === 'development' || localStorage.getItem('debug') === 'true'

if (DEBUG) {
  console.log('API Configuration:')
  console.log('- Electron detected:', isElectron())
  console.log('- Base URL:', baseURL)
  console.log('- Backend URL:', BACKEND_URL)
}

// 创建axios实例
const api = axios.create({
  baseURL: baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    if (DEBUG) {
      console.log('API Request:', {
        method: config.method?.toUpperCase(),
        url: config.url,
        baseURL: config.baseURL,
        fullURL: `${config.baseURL}${config.url}`
      })
    }
    
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    if (DEBUG) {
      console.log('API Response Success:', {
        status: response.status,
        url: response.config.url,
        dataType: typeof response.data,
        dataSize: JSON.stringify(response.data).length
      })
    }
    return response
  },
  error => {
    console.error('API Response Error:', {
      message: error.message,
      status: error.response?.status,
      url: error.config?.url,
      baseURL: error.config?.baseURL,
      fullURL: error.config ? `${error.config.baseURL}${error.config.url}` : 'unknown',
      errorData: error.response?.data
    })
    
    if (error.response && error.response.status === 401) {
      // 未授权，清除token并跳转到登录页
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('tokenExpiration')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api