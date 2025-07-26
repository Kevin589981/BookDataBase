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
        <label for="search-isbn">ISBN</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-isbn" 
            v-model="searchParams.isbn" 
            placeholder="13位数字ISBN"
            maxlength="13"
            pattern="[0-9]*"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-isbn" 
              v-model="searchParams.exact_isbn"
            />
            <label for="exact-isbn">精确匹配</label>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="search-title">书名</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-title" 
            v-model="searchParams.title" 
            placeholder="搜索书名"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-title" 
              v-model="searchParams.exact_title"
            />
            <label for="exact-title">精确匹配</label>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="search-author">作者</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-author" 
            v-model="searchParams.author" 
            placeholder="搜索作者"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-author" 
              v-model="searchParams.exact_author"
            />
            <label for="exact-author">精确匹配</label>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="search-publisher">出版社</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-publisher" 
            v-model="searchParams.publisher" 
            placeholder="搜索出版社"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-publisher" 
              v-model="searchParams.exact_publisher"
            />
            <label for="exact-publisher">精确匹配</label>
          </div>
        </div>
      </div>
      
      <!-- 价格范围输入框 -->
      <div class="form-group price-range">
        <label>价格范围</label>
        <div class="range-inputs">
          <input 
            type="number" 
            id="search-min-price" 
            v-model="searchParams.min_retail_price" 
            placeholder="最低价格"
            min="0"
            step="0.01"
          />
          <span class="range-separator">至</span>
          <input 
            type="number" 
            id="search-max-price" 
            v-model="searchParams.max_retail_price" 
            placeholder="最高价格"
            min="0"
            step="0.01"
          />
        </div>
      </div>
      
      <!-- 库存范围输入框 -->
      <div class="form-group stock-range">
        <label>库存范围</label>
        <div class="range-inputs">
          <input 
            type="number" 
            id="search-min-stock" 
            v-model="searchParams.min_stock" 
            placeholder="最小库存"
            min="0"
          />
          <span class="range-separator">至</span>
          <input 
            type="number" 
            id="search-max-stock" 
            v-model="searchParams.max_stock" 
            placeholder="最大库存"
            min="0"
          />
        </div>
      </div>
      
      <!-- 排序选项 -->
      <div class="form-group">
        <label for="search-sort-by">排序字段</label>
        <select id="search-sort-by" v-model="searchParams.sort_by">
          <option value="isbn">ISBN</option>
          <option value="title">书名</option>
          <option value="author">作者</option>
          <option value="publisher">出版社</option>
          <option value="retail_price">价格</option>
          <option value="stock">库存</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="search-sort-order">排序方向</label>
        <select id="search-sort-order" v-model="searchParams.sort_order">
          <option value="asc">升序</option>
          <option value="desc">降序</option>
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
.price-range, .stock-range {
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