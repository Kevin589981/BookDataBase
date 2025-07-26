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
        <label for="search-bill-type">账单类型</label>
        <select id="search-bill-type" v-model="searchParams.bill_type">
          <option value="">全部</option>
          <option value="进货">进货</option>
          <option value="零售">零售</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="search-operator-id">操作员工号</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-operator-id" 
            v-model="searchParams.operator_id" 
            placeholder="操作员工号"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-operator-id" 
              v-model="searchParams.exact_operator_id"
            />
            <label for="exact-operator-id">精确匹配</label>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="search-related-order">关联订单ID</label>
        <input 
          type="number" 
          id="search-related-order" 
          v-model="searchParams.related_order" 
          placeholder="关联订单ID"
          min="1"
        />
      </div>
      
      <!-- 金额范围输入框 -->
      <div class="form-group amount-range">
        <label>金额范围</label>
        <div class="range-inputs">
          <input 
            type="number" 
            id="search-min-amount" 
            v-model="searchParams.min_amount" 
            placeholder="最小金额"
            min="0"
            step="0.01"
          />
          <span class="range-separator">至</span>
          <input 
            type="number" 
            id="search-max-amount" 
            v-model="searchParams.max_amount" 
            placeholder="最大金额"
            min="0"
            step="0.01"
          />
        </div>
      </div>
      
      <!-- 日期范围输入框 -->
      <div class="form-group date-range">
        <label>交易日期范围</label>
        <div class="range-inputs">
          <input 
            type="date" 
            id="search-start-date" 
            v-model="searchParams.start_date" 
            placeholder="开始日期"
          />
          <span class="range-separator">至</span>
          <input 
            type="date" 
            id="search-end-date" 
            v-model="searchParams.end_date" 
            placeholder="结束日期"
          />
        </div>
      </div>
      
      <!-- 排序选项 -->
      <div class="form-group">
        <label for="search-sort-by">排序字段</label>
        <select id="search-sort-by" v-model="searchParams.sort_by">
          <option value="transaction_time">交易时间</option>
          <option value="amount">金额</option>
          <option value="bill_type">账单类型</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="search-sort-order">排序方向</label>
        <select id="search-sort-order" v-model="searchParams.sort_order">
          <option value="desc">降序</option>
          <option value="asc">升序</option>
        </select>
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

/* 范围输入框样式 */
.amount-range, .date-range {
  grid-column: span 2;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.range-separator {
  color: #666;
}

.range-inputs input {
  flex: 1;
  min-width: 0;
}
</style>