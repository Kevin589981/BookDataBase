// 环境配置文件

// 检测是否在Electron环境中
export const isElectron = () => {
  if (typeof window !== 'undefined') {
    return !!(window.process && window.process.type) || 
           !!(window.require) || 
           navigator.userAgent.toLowerCase().indexOf('electron') > -1
  }
  return false
}

// API配置
export const API_CONFIG = {
  // 后端服务器地址
  BACKEND_URL: 'http://localhost:8000',
  
  // 开发环境代理路径
  PROXY_PATH: '/api',
  
  // 请求超时时间
  TIMEOUT: 10000,
  
  // 获取基础URL
  getBaseURL() {
    return isElectron() ? this.BACKEND_URL : this.PROXY_PATH
  }
}

// 应用配置
export const APP_CONFIG = {
  // 应用名称
  APP_NAME: 'BookDataBaseManager',
  
  // 版本号
  VERSION: '0.0.0',
  
  // 是否开启调试模式
  DEBUG: true
}

export default {
  API_CONFIG,
  APP_CONFIG,
  isElectron
}