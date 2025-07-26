<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  users: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  totalUsers: {
    type: Number,
    default: 0
  },
  currentPage: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 10
  },
  searchParams: {
    type: Object,
    required: true
  },
  isSuperAdmin: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['edit', 'delete', 'change-page', 'change-page-size'])

const handleEdit = (user) => {
  emit('edit', user)
}

const handleDelete = (user) => {
  emit('delete', user)
}

const changePage = (page) => {
  emit('change-page', page)
}

const changePageSize = () => {
  emit('change-page-size')
}
</script>

<template>
  <div>
    <!-- 用户列表 -->
    <div class="users-table">
      <table>
        <thead>
          <tr>
            <th>用户名</th>
            <th>工号</th>
            <th>真实姓名</th>
            <th>性别</th>
            <th>年龄</th>
            <th>角色</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="7" class="loading-row">加载中...</td>
          </tr>
          <tr v-else-if="users.length === 0">
            <td colspan="7" class="empty-row">暂无用户数据</td>
          </tr>
          <tr v-for="user in users" :key="user.username">
            <td>{{ user.username }}</td>
            <td>{{ user.employee_id }}</td>
            <td>{{ user.true_name }}</td>
            <td>{{ user.gender === 'male' ? '男' : '女' }}</td>
            <td>{{ user.age ? user.age : '-' }}</td>
            <td>{{ user.isSuperAdmin ? '超级管理员' : '普通管理员' }}</td>
            <td class="actions-cell">
              <button class="edit-btn" @click="handleEdit(user)">
                <i class="fa fa-edit"></i> 编辑
              </button>
              <button 
                class="delete-btn" 
                @click="handleDelete(user)"
                :disabled="user.isSuperAdmin"
                :title="user.isSuperAdmin ? '无法删除超级管理员' : ''"
              >
                <i class="fa fa-trash"></i> 删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 分页 -->
    <div class="pagination" v-if="totalUsers > 0">
      <div class="page-size-selector">
        <label for="page-size">每页显示：</label>
        <select id="page-size" v-model="searchParams.page_size" @change="changePageSize">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>
      <div class="page-controls">
        <button 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)"
        >
          上一页
        </button>
        <span>{{ currentPage }} / {{ Math.ceil(totalUsers / pageSize) }}</span>
        <button 
          :disabled="currentPage >= Math.ceil(totalUsers / pageSize)" 
          @click="changePage(currentPage + 1)"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.users-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #2c3e50;
}

.loading-row, .empty-row {
  text-align: center;
  color: #999;
  padding: 2rem;
}

.actions-cell {
  display: flex;
  gap: 0.8rem;
}

.edit-btn {
  background-color: #4caf50;
}

.edit-btn:hover {
  background-color: #388e3c;
}

.delete-btn {
  background-color: #f44336;
}

.delete-btn:hover {
  background-color: #d32f2f;
}

.delete-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button {
  padding: 0.5rem 0.8rem;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.page-size-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-size-selector select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.page-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-controls button {
  background-color: #2196f3;
}

.page-controls button:hover {
  background-color: #1976d2;
}

/* 表格列宽调整 */
th:nth-child(4), td:nth-child(4) { /* 性别列 */
  width: 10%;
  min-width: 80px;
}

th:nth-child(5), td:nth-child(5) { /* 年龄列 */
  width: 10%;
  min-width: 80px;
}

th:nth-child(6), td:nth-child(6) { /* 角色列 */
  width: 15%;
  min-width: 120px;
}

th:nth-child(7), td:nth-child(7) { /* 操作列 */
  width: 20%;
  min-width: 180px;
}
</style>