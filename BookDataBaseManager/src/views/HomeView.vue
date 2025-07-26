<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  router.push('/dashboard')
}
</script>

<template>
  <main class="home-container">
    <div class="welcome-card">
      <h1>欢迎登录图书管理系统</h1>
      <p>这是一个全面的图书管理解决方案，帮助您高效管理图书库存、销售和采购。</p>
      <button class="login-button" @click="goToLogin">
        <i class="fa fa-sign-in"></i> 登录系统
      </button>
    </div>
  </main>
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

.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;  /* 改为100vh使垂直方向也居中 */
  padding: 2rem;
  width: 100%;  /* 添加宽度100%确保占满整个视口 */
}

.welcome-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  max-width: 800px;  /* 增大最大宽度 */
  width: 90%;  /* 添加宽度90%使其更宽 */
  text-align: center;
  margin: 0 auto;  /* 确保水平居中 */
}

.welcome-card h1 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 2.5rem;
}

.welcome-card p {
  color: #666;
  margin-bottom: 2.5rem;
  line-height: 1.6;
  font-size: 1.2rem;
}

.login-button {
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 4px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.login-button:hover {
  background-color: #1976d2;
}
</style>
