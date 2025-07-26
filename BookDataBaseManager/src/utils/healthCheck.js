// 后端健康检查工具
import { API_CONFIG } from '@/config'

/**
 * 检查后端服务器是否可用
 * @returns {Promise<boolean>} 服务器是否可用
 */
export async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_CONFIG.BACKEND_URL}`, {
      method: 'GET',
      mode: 'no-cors'
    })
    return true // no-cors模式下无法检查response.ok，假设连接成功
  } catch (error) {
    console.warn('Backend health check failed:', error.message)
    return false
  }
}

/**
 * 检查后端连接并显示状态
 */
export async function displayBackendStatus() {
  console.log('🔍 检查后端连接状态...')
  
  const isHealthy = await checkBackendHealth()
  
  if (isHealthy) {
    console.log('✅ 后端服务器连接正常')
  } else {
    console.error('❌ 后端服务器连接失败')
    console.error(`请确保后端服务器运行在: ${API_CONFIG.BACKEND_URL}`)
    
    // 显示用户友好的错误提示
    if (typeof window !== 'undefined' && window.alert) {
      setTimeout(() => {
        window.alert(`无法连接到后端服务器！\n\n请确保后端服务器正在运行：\n${API_CONFIG.BACKEND_URL}\n\n检查控制台获取更多信息。`)
      }, 2000)
    }
  }
  
  return isHealthy
}

export default {
  checkBackendHealth,
  displayBackendStatus
}