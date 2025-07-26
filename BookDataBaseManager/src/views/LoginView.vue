<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/auth'

const router = useRouter()
const errorMessage = ref('')
const loading = ref(false)

const formData = reactive({
  username: '',
  password: ''
})
// 登录函数
const login = async () => {
  if (!formData.username || !formData.password) {
    errorMessage.value = '请输入用户名和密码'
    return
  }

  try {
    loading.value = true
    errorMessage.value = ''
    
    // 使用认证服务登录
    await authService.login(formData.username, formData.password)
    
    // 登录成功后跳转到首页
    router.push('/dashboard')    // @/router/index.js里面的第10行
  } catch (error) {
    console.error('登录失败:', error)
    if (error.response) {
      // 处理服务器返回的错误
      if (error.response.status === 401) {
        errorMessage.value = '用户名或密码错误'
      } else if (error.response.status === 422) {
        errorMessage.value = '输入数据验证失败'
      } else {
        errorMessage.value = error.response.data.detail || '登录失败，请检查用户名和密码'
      }
    } else if (error.request) {
      // 请求发送但没有收到响应
      errorMessage.value = '服务器无响应，请稍后重试'
    } else {
      // 请求设置时出错
      errorMessage.value = '网络错误，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <h1>图书管理系统</h1>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="formData.username" 
            placeholder="请输入用户名"
            autocomplete="username"
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password" 
            placeholder="请输入密码"
            autocomplete="current-password"
          />
        </div>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>

        <div class="back-to-home">
          <router-link to="/">Home</router-link>
        </div>
      </form>
    </div>
    
  </div>
  <footer class="footer">
      <p>© 2025 图书管理系统 - 版权所有 Designed by Kevin</p>
    </footer>
</template>

<style scoped>
.footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
} 
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color:transparent;
  z-index:1;
}

.login-box {
  width: 400px;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: var(--color-text);
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: var(--color-border-hover);
}

button {
  padding: 0.75rem;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: hsla(160, 100%, 30%, 1);
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
  text-align: center;
}

.back-to-home {
  text-align: center;
  margin-top: 1rem;
  width: 100%; /* 新增 */
}
</style>