import axios from 'axios'

// 创建axios实例，使用相对路径，会通过代理转发
const api = axios.create({
  baseURL: '/api',  // 修改为使用代理路径
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      // console.log(localStorage.getItem('token'))
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
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