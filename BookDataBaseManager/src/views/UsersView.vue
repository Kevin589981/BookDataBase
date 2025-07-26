<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import UserSearch from '@/components/user/UserSearch.vue'
import UserList from '@/components/user/UserList.vue'
import UserForm from '@/components/user/UserForm.vue'
import Modal from '@/components/common/Modal.vue'
import userService from '@/services/user'

const props = defineProps({
  defaultTab: {
    type: String,
    default: 'profile'
  }
})

const router = useRouter()
const userInfo = ref({})
const isAdmin = ref(false)
const activeTab = ref(props.defaultTab)
const allUsers = ref([])
const loading = ref(false)
const totalUsers = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索参数
const searchParams = ref({
  username: '',
  employee_id: '',
  true_name: '',
  gender: '',
  min_age: null,
  max_age: null,
  sort_by: 'username',
  sort_order: 'asc',
  page: 1,
  page_size: 10,
  exact_username: false,
  exact_employee_id: false,
  exact_true_name: false
})

// 模态框状态
const showCreateUserModal = ref(false)
const showEditUserModal = ref(false)
const showDeleteUserModal = ref(false)
const selectedUser = ref(null)

// 表单状态
const newUserForm = ref({
  username: '',
  employee_id: '',
  true_name: '',
  gender: 'male',
  age: 18,
  password: '',
  confirm_password: '',
  isSuperAdmin: false
})
const editUserForm = ref({})
const createUserError = ref('')
const editUserError = ref('')

// 个人信息编辑状态
const editMode = ref(false)
const originalUserInfo = ref({})
const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})
const passwordError = ref('')

onMounted(async () => {
  // 从本地存储获取用户信息
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    userInfo.value = JSON.parse(storedUser)
    isAdmin.value = userInfo.value.isSuperAdmin
    
    // 如果是管理员，加载所有用户
    if (isAdmin.value && activeTab.value === 'users') {
      await loadAllUsers()
    }
  } else {
    // 如果没有用户信息，重定向到登录页
    router.push('/login')
  }
})

// 加载所有用户
const loadAllUsers = async () => {
  try {
    loading.value = true
    const response = await userService.getAllUsers(searchParams.value)
    
    // console.log('调试信息 - allBooks:', response.items);
    // console.log('调试信息 - totalBooks:', response.total);

    allUsers.value = response.items
    totalUsers.value = response.total
    currentPage.value = response.page
    pageSize.value = response.page_size
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索用户
const searchUsers = async () => {
  searchParams.value.page = 1
  await loadAllUsers()
}

// 重置搜索
const resetSearch = async () => {
  searchParams.value = {
    username: '',
    employee_id: '',
    true_name: '',
    gender: '',
    min_age: null,
    max_age: null,
    sort_by: 'username',
    sort_order: 'asc',
    page: 1,
    page_size: 10,
    page_size: 10,
    exact_username: false,
    exact_employee_id: false,
    exact_true_name: false
  }
  await loadAllUsers()
}

// 切换页面
const changePage = async (page) => {
  searchParams.value.page = page
  await loadAllUsers()
}

// 切换每页显示数量
const changePageSize = async () => {
  searchParams.value.page = 1
  await loadAllUsers()
}

// 切换标签
const switchTab = (tab) => {
  activeTab.value = tab
  
  // 如果切换到用户管理标签且是管理员，加载用户列表
  if (tab === 'users' && isAdmin.value) {
    loadAllUsers()
  }
}

// 切换编辑模式
const toggleEditMode = () => {
  if (editMode.value) {
    // 如果当前是编辑模式，则退出编辑模式并恢复原始数据
    if (!confirm('确定要取消编辑吗？所有未保存的修改将丢失。')) {
      return
    }
    userInfo.value = JSON.parse(JSON.stringify(originalUserInfo.value))
    editMode.value = false
  } else {
    // 如果当前不是编辑模式，则进入编辑模式并保存原始数据
    originalUserInfo.value = JSON.parse(JSON.stringify(userInfo.value))
    editMode.value = true
  }
}

// 更新个人信息
const updateProfile = async () => {
  try {
    // 验证密码输入
    if ((passwordForm.value.current_password && !passwordForm.value.new_password) || 
        (!passwordForm.value.current_password && passwordForm.value.new_password)) {
      alert('请同时输入原密码和新密码，或者都不输入')
      return
    }
    
    loading.value = true
    const updateData = {
      true_name: userInfo.value.true_name,
      gender: userInfo.value.gender,
      age: userInfo.value.age
    }

    // 如果是超级管理员，允许修改工号和管理员状态
    if (userInfo.value.isSuperAdmin) {
      updateData.employee_id = userInfo.value.employee_id
      updateData.isSuperAdmin = userInfo.value.isSuperAdmin
    }
    
    // 如果输入了密码，添加到更新数据中
    if (passwordForm.value.current_password && passwordForm.value.new_password) {
      updateData.current_password = passwordForm.value.current_password
      updateData.new_password = passwordForm.value.new_password
    }

    const response = await userService.updateProfile(updateData)
    
    // 更新本地存储的用户信息
    localStorage.setItem('user', JSON.stringify(response))
    userInfo.value = response
    editMode.value = false
    
    // 清空密码表单
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
    
    alert('个人信息更新成功')
  } catch (error) {
    console.error('更新个人信息失败:', error)
    alert('更新个人信息失败: ' + (error.response?.data?.detail || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 打开创建用户模态框
const openCreateUserModal = () => {
  // 重置表单
  newUserForm.value = {
    username: '',
    employee_id: '',
    true_name: '',
    gender: 'male',
    age: 18,
    password: '',
    confirm_password: '',
    isSuperAdmin: false
  }
  createUserError.value = ''
  showCreateUserModal.value = true
}

// 创建新用户
const createUser = async () => {
  try {
    // 验证表单
    if (!newUserForm.value.username || !newUserForm.value.employee_id || 
        !newUserForm.value.true_name || !newUserForm.value.password) {
      createUserError.value = '请填写所有必填字段'
      return
    }
    
    if (newUserForm.value.password !== newUserForm.value.confirm_password) {
      createUserError.value = '两次输入的密码不一致'
      return
    }
    
    loading.value = true
    await userService.createUser({
      username: newUserForm.value.username,
      employee_id: newUserForm.value.employee_id,
      true_name: newUserForm.value.true_name,
      gender: newUserForm.value.gender,
      age: Number(newUserForm.value.age),
      password: newUserForm.value.password,
      isSuperAdmin: newUserForm.value.isSuperAdmin
    })
    
    // 关闭模态框
    showCreateUserModal.value = false
    
    // 刷新用户列表
    await loadAllUsers()
    
    alert('用户创建成功')
  } catch (error) {
    console.error('创建用户失败:', error)
    createUserError.value = error.response?.data?.detail || '创建用户失败'
  } finally {
    loading.value = false
  }
}

// 打开编辑用户模态框
const openEditUserModal = (user) => {
  selectedUser.value = user
  editUserForm.value = {
    username: user.username,
    employee_id: user.employee_id,
    true_name: user.true_name,
    gender: user.gender,
    age: user.age,
    isSuperAdmin: user.isSuperAdmin,
    reset_password: false // 添加重置密码选项
  }
  editUserError.value = ''
  showEditUserModal.value = true
}

// 修改updateUser方法
const updateUser = async () => {
  try {
    // 验证表单
    if (!editUserForm.value.true_name) {
      editUserError.value = '真实姓名不能为空'
      return
    }
    
    loading.value = true
    const updateData = {
      true_name: editUserForm.value.true_name,
      gender: editUserForm.value.gender,
      age: Number(editUserForm.value.age),
      reset_password: editUserForm.value.reset_password // 添加重置密码选项
    }
    
    // 如果是超级管理员，允许修改工号和管理员状态
    if (userInfo.value.isSuperAdmin) {
      updateData.employee_id = editUserForm.value.employee_id
      updateData.isSuperAdmin = editUserForm.value.isSuperAdmin
    }
    
    await userService.updateUser(selectedUser.value.username, updateData)
    
    // 关闭模态框
    showEditUserModal.value = false
    
    // 刷新用户列表
    await loadAllUsers()
    
    alert('用户信息更新成功')
  } catch (error) {
    console.error('更新用户信息失败:', error)
    // 检查是否是唯一约束错误（工号已存在）
    if (error.response?.data?.detail && 
        (error.response.data.detail.includes('UNIQUE constraint failed: users.employee_id') ||
         error.response.data.detail.includes('IntegrityError'))) {
      editUserError.value = '工号已存在，请更换工号'
    } else {
      editUserError.value = error.response?.data?.detail || '更新用户信息失败'
    }
    
  } finally {
    loading.value = false
  }
}

// 打开删除用户确认模态框
const openDeleteUserModal = (user) => {
  selectedUser.value = user
  showDeleteUserModal.value = true
}

// 删除用户
const deleteUser = async () => {
  try {
    loading.value = true
    await userService.deleteUser(selectedUser.value.username)
    
    // 关闭模态框
    showDeleteUserModal.value = false
    
    // 刷新用户列表
    await loadAllUsers()
    
    alert('用户删除成功')
  } catch (error) {
    console.error('删除用户失败:', error)
    alert('删除用户失败: ' + (error.response?.data?.detail || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 返回仪表盘
const backToDashboard = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="users-view">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="logo">
        <h1>用户管理</h1>
      </div>
      <div class="nav-actions">
        <button class="back-btn" @click="backToDashboard">
          <i class="fa fa-arrow-left"></i> 返回仪表盘
        </button>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="sidebar">
        <div class="sidebar-item" 
             :class="{ active: activeTab === 'profile' }" 
             @click="switchTab('profile')">
          <i class="fa fa-user"></i> 个人信息管理
        </div>
        <div class="sidebar-item" 
             :class="{ active: activeTab === 'users', disabled: !isAdmin }" 
             @click="isAdmin && switchTab('users')">
          <i class="fa fa-users"></i> 所有用户管理
          <span v-if="!isAdmin" class="admin-only">(仅管理员)</span>
        </div>
      </div>

      <div class="content-area">
        <!-- 个人信息管理 -->
        <div v-if="activeTab === 'profile'" class="profile-section">
          <h2>个人信息</h2>
          <form @submit.prevent="updateProfile" class="profile-form">
            <div class="form-group">
              <label for="username">用户名</label>
              <input 
                type="text" 
                id="username" 
                v-model="userInfo.username" 
                disabled
              />
            </div>
            
            <div class="form-group">
              <label for="employee_id">工号</label>
              <input 
                type="text" 
                id="employee_id" 
                v-model="userInfo.employee_id" 
                :disabled="!editMode || !userInfo.isSuperAdmin"
              />
            </div>
            
            <div class="form-group">
              <label for="true_name">真实姓名</label>
              <input 
                type="text" 
                id="true_name" 
                v-model="userInfo.true_name" 
                :disabled="!editMode"
              />
            </div>
            
            <div class="form-group">
              <label for="gender">性别</label>
              <select 
                id="gender" 
                v-model="userInfo.gender" 
                :disabled="!editMode"
              >
                <option value="male">男</option>
                <option value="female">女</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="age">年龄</label>
              <input 
                type="number" 
                id="age" 
                v-model="userInfo.age" 
                :disabled="!editMode"
                min="0"
              />
            </div>
            
            <div class="form-group">
              <label for="role">角色</label>
              <select 
                id="role" 
                v-model="userInfo.isSuperAdmin" 
                :disabled="!editMode || !userInfo.isSuperAdmin"
              >
                <option :value="true">超级管理员</option>
                <option :value="false">普通管理员</option>
              </select>
            </div>
            
            <!-- 在角色选择框之后添加密码修改部分 -->
            <div class="form-group" v-if="editMode">
              <label for="current_password">原密码</label>
              <input 
                type="password" 
                id="current_password" 
                v-model="passwordForm.current_password" 
                placeholder="留空则不修改密码"
              />
            </div>
            
            <div class="form-group" v-if="editMode">
              <label for="new_password">新密码</label>
              <input 
                type="password" 
                id="new_password" 
                v-model="passwordForm.new_password" 
                placeholder="留空则不修改密码"
              />
            </div>
            
            <div class="password-hint" v-if="editMode">
              注意：修改密码需同时输入原密码和新密码，或者都不输入
            </div>
            
            <!-- 然后是表单操作按钮 -->
            <div class="form-actions">
              <button 
                v-if="!editMode" 
                type="button" 
                @click="toggleEditMode"
              >
                编辑信息
              </button>
              <template v-else>
                <button type="submit" :disabled="loading">
                  {{ loading ? '保存中...' : '保存修改' }}
                </button>
                <button 
                  type="button" 
                  class="cancel-btn" 
                  @click="toggleEditMode"
                  :disabled="loading"
                >
                  取消
                </button>
              </template>
            </div>
          </form>
        </div>

        <!-- 所有用户管理 -->
        <div v-if="activeTab === 'users'" class="users-section">
          <h2>用户管理</h2>
          
          <!-- 添加创建用户按钮 -->
          <div class="users-actions" v-if="userInfo.isSuperAdmin">
            <button class="create-user-btn" @click="openCreateUserModal">
              <i class="fa fa-user-plus"></i> 创建新用户
            </button>
          </div>
          
          <!-- 使用用户搜索组件 -->
          <UserSearch 
            :searchParams="searchParams" 
            :loading="loading"
            @search="searchUsers"
            @reset="resetSearch"
          />
          
          <!-- 使用用户列表组件 -->
          <UserList 
            :users="allUsers" 
            :loading="loading"
            :totalUsers="totalUsers"
            :currentPage="currentPage"
            :pageSize="pageSize"
            :searchParams="searchParams"
            @edit="openEditUserModal"
            @delete="openDeleteUserModal"
            @change-page="changePage"
            @change-page-size="changePageSize"
          />
        </div>
      </div>
    </main>
    
    <!-- 创建用户模态框 -->
    <Modal 
      :show="showCreateUserModal" 
      title="创建新用户"
      @close="showCreateUserModal = false"
    >
      <UserForm 
        :user="newUserForm"
        mode="create"
        :loading="loading"
        :error="createUserError"
        :isSuperAdmin="userInfo.isSuperAdmin"
        @submit="createUser"
        @cancel="showCreateUserModal = false"
      />
    </Modal>
    
    <!-- 编辑用户模态框 -->
    <Modal 
      :show="showEditUserModal" 
      title="编辑用户信息"
      @close="showEditUserModal = false"
    >
      <UserForm 
        :user="editUserForm"
        mode="edit"
        :loading="loading"
        :error="editUserError"
        :isSuperAdmin="userInfo.isSuperAdmin"
        @submit="updateUser"
        @cancel="showEditUserModal = false"
      />
    </Modal>
    
    <!-- 删除用户确认模态框 -->
    <Modal 
      :show="showDeleteUserModal" 
      title="确认删除"
      @close="showDeleteUserModal = false"
    >
      <div class="delete-confirmation">
        <p>确定要删除用户 <strong>{{ selectedUser?.username }}</strong> 吗？此操作不可撤销。</p>
        <div class="form-actions">
          <button 
            @click="deleteUser" 
            :disabled="loading" 
            class="delete-btn"
          >
            {{ loading ? '删除中...' : '确认删除' }}
          </button>
          <button 
            @click="showDeleteUserModal = false" 
            :disabled="loading" 
            class="cancel-btn"
          >
            取消
          </button>
        </div>
      </div>
    </Modal>
    <footer class="footer">
      <p>© 2025 图书管理系统 - 版权所有 Designed by Kevin</p>
    </footer>
  </div>
</template>

<style scoped>
footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
.users-view {
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

.back-btn {
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

.back-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.main-content {
  display: flex;
  flex: 1;
  background-color:transparent;
}

.sidebar {
  width: 250px;
  background-color: white;
  padding: 2rem 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
}

.sidebar-item {
  padding: 1rem 2rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sidebar-item:hover {
  background-color: #f5f5f5;
}

.sidebar-item.active {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
  color: #2196f3;
}

.sidebar-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.admin-only {
  font-size: 0.8rem;
  color: #999;
  margin-left: 0.5rem;
}

.content-area {
  flex: 1;
  padding: 2rem;
}

.profile-section, .users-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

h2 {
  margin-top: 0;
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.profile-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: #2c3e50;
}

input, select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus, select:focus {
  outline: none;
  border-color: #2196f3;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.password-hint {
  grid-column: span 2;
  color: #666;
  font-size: 0.9rem;
  margin-top: -0.5rem;
}

.form-actions {
  grid-column: span 2;
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1976d2;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}

.delete-btn {
  background-color: #f44336;
}

.delete-btn:hover {
  background-color: #d32f2f;
}

/* 用户管理操作按钮 */
.users-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.create-user-btn {
  background-color: #4caf50;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.create-user-btn:hover {
  background-color: #388e3c;
}

/* 删除确认样式 */
.delete-confirmation {
  text-align: center;
  padding: 1rem;
}

.delete-confirmation p {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}
</style>