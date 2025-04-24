<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/auth'

const router = useRouter()
const userInfo = ref({})
const isLoggingOut = ref(false)

// 当跳转到dashboard时，会挂载这个页面（onMounted）
onMounted(() => {
  // 从认证服务获取用户信息
  const user = authService.getCurrentUser()
  if (user) {
    userInfo.value = user
  } else {
    // 如果没有用户信息，重定向到登录页
    router.push('/login')
  }
})

// 退出登录
const logout = async () => {
  if (isLoggingOut.value) return
  
  isLoggingOut.value = true
  await authService.logout()
  isLoggingOut.value = false
}

// 导航到不同的管理页面
const navigateTo = (path) => {
  router.push(path)
}
</script>

<template>
  <div class="dashboard">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="logo">
        <h1>图书管理系统</h1>
      </div>
      <div class="user-info">
        <span v-if="userInfo.true_name">欢迎，{{ userInfo.true_name }}</span>
        <span v-else>欢迎，{{ userInfo.username }}</span>
        <button class="logout-btn" @click="logout" :disabled="isLoggingOut">
          <i class="fa fa-sign-out"></i> {{ isLoggingOut ? '登出中...' : '退出登录' }}
        </button>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="dashboard-title">
        <h2>系统功能</h2>
        <p>请选择您要使用的功能模块</p>
      </div>

      <div class="feature-cards">
        <!-- 用户管理卡片 - 修改为所有管理员都可见 -->
        <div class="card" @click="navigateTo('/users')">
          <div class="card-icon">
            <i class="fa fa-users fa-4x"></i>
          </div>
          <div class="card-content">
            <h3>用户管理</h3>
            <p>管理系统用户、权限设置</p>
          </div>
        </div>

        <!-- 书籍管理卡片 -->
        <div class="card" @click="navigateTo('/books')">
          <div class="card-icon">
            <i class="fa fa-book fa-4x"></i>
          </div>
          <div class="card-content">
            <h3>书籍管理</h3>
            <p>图书查询、增加、删除、修改</p>
          </div>
        </div>

        <!-- 进货管理卡片 -->
        <div class="card" @click="navigateTo('/purchase')">
          <div class="card-icon">
            <i class="fa fa-truck fa-4x"></i>
          </div>
          <div class="card-content">
            <h3>进货管理</h3>
            <p>图书采购、入库管理</p>
          </div>
        </div>

        <!-- 销售管理卡片 -->
        <div class="card" @click="navigateTo('/sale')">
          <div class="card-icon">
            <i class="fa fa-shopping-cart fa-4x"></i>
          </div>
          <div class="card-content">
            <h3>销售管理</h3>
            <p>图书销售、订单管理</p>
          </div>
        </div>

        <!-- 财务管理卡片 -->
        <div class="card" @click="navigateTo('/bills')">
          <div class="card-icon">
            <i class="fa fa-money fa-4x"></i>
          </div>
          <div class="card-content">
            <h3>财务管理</h3>
            <p>账单查询、财务报表</p>
          </div>
        </div>

        <!-- 个人信息卡片已移除 -->
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <p>© 2025 图书管理系统 - 版权所有 Designed by Kevin</p>
    </footer>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  background-color: transparent;
  color: white;
  border: 1px solid white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: transparent;
}

.dashboard-title {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-title h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.dashboard-title p {
  color: #7f8c8d;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card-icon {
  margin-bottom: 1.5rem;
  color: #3498db;
}

.card-content h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.card-content p {
  color: #7f8c8d;
}

.footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
</style>