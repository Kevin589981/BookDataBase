import api from '@/utils/api'

class UserService {
  // 获取当前用户信息
  async getCurrentUserInfo() {
    const response = await api.get('/me', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }

  // 更新当前用户信息
  async updateProfile(updateData) {
    const response = await api.patch('/me', updateData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }

  // 获取所有用户
  async getAllUsers(params) {
    // 处理搜索参数，移除空值
    const cleanParams = Object.entries(params).reduce((acc, [key, value]) => {
      // 如果值不为空且不为空字符串，则添加到参数中
      if (value !== null && value !== '' && value !== undefined) {
        acc[key] = value
      }
      return acc
    }, {})
    
    const response = await api.get('/users/all', {
      params: cleanParams,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }

  // 创建新用户
  async createUser(userData) {
    const response = await api.post('/users/register', userData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }

  // 删除用户
  async deleteUser(username) {
    const response = await api.delete(`/users/${username}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }

  // 更新用户信息
  async updateUser(username, userData) {
    const response = await api.patch(`/users/${username}`, userData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }
  
  // 更新用户密码
  async updatePassword(passwordData) {
    const response = await api.patch('/me/password', passwordData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }
  
  // 获取用户详情
  async getUserDetails(username) {
    const response = await api.get(`/users/${username}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }
  
  // 检查用户名是否可用
  async checkUsernameAvailability(username) {
    const response = await api.get(`/users/check-username?username=${username}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }
  
  // 检查工号是否可用
  async checkEmployeeIdAvailability(employeeId) {
    const response = await api.get(`/users/check-employee-id?employee_id=${employeeId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    return response.data
  }
  
  // 获取当前登录用户
  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      return JSON.parse(userStr)
    }
    return null
  }
  
  // 保存用户信息到本地存储
  saveUserToLocalStorage(user) {
    localStorage.setItem('user', JSON.stringify(user))
  }
  
  // 清除本地存储的用户信息
  clearUserFromLocalStorage() {
    localStorage.removeItem('user')
  }
}

export default new UserService()