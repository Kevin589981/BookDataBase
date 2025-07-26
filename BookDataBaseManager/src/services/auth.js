import api from '@/utils/api'
import router from '@/router'

/**
 * 用户认证相关服务
 */
export const authService = {
  /**
   * 用户登录
   * @param {string} username 用户名
   * @param {string} password 密码
   * @returns {Promise} 登录结果
   */
  async login(username, password) {
    try {
      const response = await api.post('/login', {
        username,
        password
      })
      
      // 保存令牌和用户信息到本地存储
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.user_info))
      localStorage.setItem('tokenExpiration', response.data.expiration_time)
      
      // // 设置axios默认请求头包含token api已经加了
      
      return response.data
    } catch (error) {
      throw error
    }
  },
  
  /**
   * 用户登出
   * @returns {Promise} 登出结果
   */
  async logout() {
    try {
      // 调用后端登出接口
      await api.post('/logout', {}, {})
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      // 无论成功失败，都清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('tokenExpiration')
      
      // 跳转到登录页
      router.push('/login')
    }
  },
  
  /**
   * 检查用户是否已登录
   * @returns {boolean} 是否已登录
   */
  isLoggedIn() {
    const token = localStorage.getItem('token')
    const expiration = localStorage.getItem('tokenExpiration')
    
    if (!token || !expiration) {
      return false
    }
    
    // 检查token是否过期
    const expirationTime = new Date(expiration)
    const now = new Date()
    
    return expirationTime > now
  },
  
  /**
   * 获取当前登录用户信息
   * @returns {Object|null} 用户信息
   */
  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    if (!userStr) {
      return null
    }
    
    try {
      return JSON.parse(userStr)
    } catch (e) {
      return null
    }
  }
}

export default authService