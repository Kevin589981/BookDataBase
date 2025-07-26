<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'create', // 'create' 或 'edit'
    validator: (value) => ['create', 'edit'].includes(value)
  },
  error: {
    type: String,
    default: ''
  },
  isSuperAdmin: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

const handleSubmit = () => {
  emit('submit')
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="user-form">
    <div class="form-group">
      <label for="username">用户名 <span class="required" v-if="mode === 'create'">*</span></label>
      <input 
        type="text" 
        id="username" 
        v-model="user.username" 
        :disabled="mode === 'edit'"
        required
        placeholder="请输入用户名"
      />
    </div>
    
    <div class="form-group">
      <label for="employee_id">工号 <span class="required" v-if="mode === 'create'">*</span></label>
      <input 
        type="text" 
        id="employee_id" 
        v-model="user.employee_id" 
        :disabled="mode === 'edit' && !isSuperAdmin"
        required
        placeholder="请输入工号"
      />
    </div>
    
    <div class="form-group">
      <label for="true_name">真实姓名 <span class="required" v-if="mode === 'create'">*</span></label>
      <input 
        type="text" 
        id="true_name" 
        v-model="user.true_name" 
        required
        placeholder="请输入真实姓名"
      />
    </div>
    
    <div class="form-group">
      <label for="gender">性别</label>
      <select id="gender" v-model="user.gender">
        <option value="male">男</option>
        <option value="female">女</option>
      </select>
    </div>
    
    <div class="form-group">
      <label for="age">年龄</label>
      <input 
        type="number" 
        id="age" 
        v-model="user.age" 
        min="0"
      />
    </div>
    
    <template v-if="mode === 'create'">
      <div class="form-group">
        <label for="password">密码 <span class="required">*</span></label>
        <input 
          type="password" 
          id="password" 
          v-model="user.password" 
          required
          placeholder="请输入密码"
        />
      </div>
      
      <div class="form-group">
        <label for="confirm_password">确认密码 <span class="required">*</span></label>
        <input 
          type="password" 
          id="confirm_password" 
          v-model="user.confirm_password" 
          required
          placeholder="请再次输入密码"
        />
      </div>
    </template>
    
    
    <template v-else>
      <!-- 管理员编辑模式下的密码重置选项 -->
      <div class="form-group" v-if="isSuperAdmin">
        <label>重置密码</label>
        <div class="reset-password">
          <input 
            type="checkbox" 
            id="reset-password" 
            v-model="user.reset_password"
          />
          <label for="reset-password">重置密码为用户名</label>
        </div>
      </div>
      
      <!-- 其他表单字段 -->
      <div class="form-group" v-if="isSuperAdmin">
        <label for="is_super_admin">用户角色</label>
        <select 
          id="is_super_admin" 
          v-model="user.isSuperAdmin"
          :disabled="user.username === 'admin'"
        >
          <option :value="false">普通管理员</option>
          <option :value="true">超级管理员</option>
        </select>
      </div>
    </template>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div class="form-actions">
      <button type="submit" :disabled="loading">
        {{ loading ? '处理中...' : (mode === 'create' ? '创建用户' : '保存修改') }}
      </button>
      <button 
        type="button" 
        class="cancel-btn" 
        @click="handleCancel"
        :disabled="loading"
      >
        取消
      </button>
    </div>
  </form>
</template>

<style scoped>
.user-form {
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

.required {
  color: #f44336;
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
  margin-bottom: 1rem;
}

.error-message {
  grid-column: span 2;
  color: #f44336;
  margin-bottom: 1rem;
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

/* 添加重置密码选项的样式 */
.reset-password {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reset-password input[type="checkbox"] {
  width: auto;
  margin: 0;
}
</style>