<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  searchParams: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['search', 'reset'])

const handleSearch = () => {
  emit('search')
}

const handleReset = () => {
  emit('reset')
}
</script>

<template>
  <div class="search-bar">
    <div class="search-inputs">
      <div class="form-group">
        <label for="search-username">用户名</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-username" 
            v-model="searchParams.username" 
            placeholder="搜索用户名"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-username" 
              v-model="searchParams.exact_username"
            />
            <label for="exact-username">精确匹配</label>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="search-employee-id">工号</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-employee-id" 
            v-model="searchParams.employee_id" 
            placeholder="搜索工号"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-employee-id" 
              v-model="searchParams.exact_employee_id"
            />
            <label for="exact-employee-id">精确匹配</label>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="search-true-name">真实姓名</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-true-name" 
            v-model="searchParams.true_name" 
            placeholder="搜索真实姓名"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-true-name" 
              v-model="searchParams.exact_true_name"
            />
            <label for="exact-true-name">精确匹配</label>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="search-gender">性别</label>
        <select id="search-gender" v-model="searchParams.gender">
          <option value="">全部</option>
          <option value="male">男</option>
          <option value="female">女</option>
        </select>
      </div>
      
      <!-- 年龄范围输入框 -->
      <div class="form-group age-range">
        <label>年龄范围</label>
        <div class="age-inputs">
          <input 
            type="number" 
            id="search-min-age" 
            v-model="searchParams.min_age" 
            placeholder="最小年龄"
            min="0"
          />
          <span class="age-separator">至</span>
          <input 
            type="number" 
            id="search-max-age" 
            v-model="searchParams.max_age" 
            placeholder="最大年龄"
            min="0"
          />
        </div>
      </div>
    </div>
    
    <div class="search-actions">
      <button @click="handleSearch" :disabled="loading">
        <i class="fa fa-search"></i> 搜索
      </button>
      <button @click="handleReset" :disabled="loading">
        <i class="fa fa-refresh"></i> 重置
      </button>
    </div>
  </div>
</template>

<style scoped>
.search-bar {
  margin-bottom: 2rem;
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
}

.search-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-with-checkbox {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.checkbox-wrapper input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.checkbox-wrapper label {
  font-size: 0.85rem;
  font-weight: normal;
  margin: 0;
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

.search-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

button:hover {
  background-color: #1976d2;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 年龄范围输入框样式 */
.age-range {
  grid-column: span 2;
}

.age-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.age-separator {
  color: #666;
}

.age-inputs input {
  flex: 1;
  min-width: 0;
}
</style>