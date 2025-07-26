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
        <label for="search-order-id">订单ID</label>
        <input 
          type="number" 
          id="search-order-id" 
          v-model="searchParams.order_id" 
          placeholder="订单ID"
          min="1"
        />
      </div>
      
      <div class="form-group">
        <label for="search-isbn">ISBN</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-isbn" 
            v-model="searchParams.book_isbn" 
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
        <label for="search-payment-status">付款状态</label>
        <select id="search-payment-status" v-model="searchParams.payment_status">
          <option value="">全部</option>
          <option value="未付款">未付款</option>
          <option value="已付款">已付款</option>
          <option value="已退货">已退货</option>
          <option value="已到货">已到货</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="search-operator-id">下单操作员工号</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-operator-id" 
            v-model="searchParams.operator_id" 
            placeholder="下单操作员工号"
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

      <!-- 新增：付款/退货操作员 -->
      <div class="form-group">
        <label for="search-operator-id2">付款/退货操作员</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-operator-id2" 
            v-model="searchParams.operator_id2" 
            placeholder="付款/退货操作员工号"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-operator-id2" 
              v-model="searchParams.exact_operator_id2"
            />
            <label for="exact-operator-id2">精确匹配</label>
          </div>
        </div>
      </div>

      <!-- 新增：到货操作员 -->
      <div class="form-group">
        <label for="search-operator-id3">到货操作员</label>
        <div class="input-with-checkbox">
          <input 
            type="text" 
            id="search-operator-id3" 
            v-model="searchParams.operator_id3" 
            placeholder="到货操作员工号"
          />
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              id="exact-operator-id3" 
              v-model="searchParams.exact_operator_id3"
            />
            <label for="exact-operator-id3">精确匹配</label>
          </div>
        </div>
      </div>
      
      <!-- 日期范围输入框 -->
      <div class="form-group date-range">
        <label>订单日期范围</label>
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
      
      <!-- 价格范围输入框 -->
      <div class="form-group price-range">
        <label>进货单价范围</label>
        <div class="range-inputs">
          <input 
            type="number" 
            id="search-min-price" 
            v-model="searchParams.min_price" 
            placeholder="最低单价"
            min="0"
            step="0.01"
          />
          <span class="range-separator">至</span>
          <input 
            type="number" 
            id="search-max-price" 
            v-model="searchParams.max_price" 
            placeholder="最高单价"
            min="0"
            step="0.01"
          />
        </div>
      </div>
      
      <!-- 数量范围输入框 -->
      <div class="form-group quantity-range">
        <label>进货数量范围</label>
        <div class="range-inputs">
          <input 
            type="number" 
            id="search-min-quantity" 
            v-model="searchParams.min_quantity" 
            placeholder="最小数量"
            min="1"
          />
          <span class="range-separator">至</span>
          <input 
            type="number" 
            id="search-max-quantity" 
            v-model="searchParams.max_quantity" 
            placeholder="最大数量"
            min="1"
          />
        </div>
      </div>
      
      <!-- 排序选项 -->
      <div class="form-group">
        <label for="search-sort-by">排序字段</label>
        <select id="search-sort-by" v-model="searchParams.sort_by">
          <option value="order_date">订单日期</option>
          <option value="purchase_price">进货单价</option>
          <option value="quantity">数量</option>
          <option value="total_amount">总金额</option>
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
.date-range, .price-range, .quantity-range {
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