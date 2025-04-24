<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  bills: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  totalBills: {
    type: Number,
    required: true
  },
  currentPage: {
    type: Number,
    required: true
  },
  pageSize: {
    type: Number,
    required: true
  },
  searchParams: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['change-page', 'change-page-size'])

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  const date = new Date(dateTimeStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 格式化金额
const formatAmount = (amount) => {
  return `¥${parseFloat(amount).toFixed(2)}`
}

// 计算总页数
const totalPages = () => {
  return Math.ceil(props.totalBills / props.pageSize)
}

// 切换页码
const changePage = (page) => {
  if (page < 1 || page > totalPages() || page === props.currentPage) return
  emit('change-page', page)
}

// 切换每页显示数量
const changePageSize = (event) => {
  const newSize = parseInt(event.target.value)
  props.searchParams.page_size = newSize
  emit('change-page-size')
}
</script>

<template>
  <div class="bill-list">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-if="bills.length === 0 && !loading" class="no-data">
      <p>没有找到符合条件的账单记录</p>
    </div>
    
    <table v-else class="bills-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>账单类型</th>
          <th>金额</th>
          <th>交易时间</th>
          <th>关联订单</th>
          <th>操作员</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="bill in bills" :key="bill.id">
          <td>{{ bill.id }}</td>
          <td>
            <span 
              :class="['bill-type', bill.bill_type === '进货' ? 'purchase' : 'sale']"
            >
              {{ bill.bill_type }}
            </span>
          </td>
          <td>{{ formatAmount(bill.amount) }}</td>
          <td>{{ formatDateTime(bill.transaction_time) }}</td>
          <td>{{ bill.related_order ? `${bill.bill_type}单号：${bill.related_order}` : '无' }}</td>
          <td>{{ bill.operator_id || '未知' }}</td>
        </tr>
      </tbody>
    </table>
    
    <!-- 分页控件 -->
    <div v-if="bills.length > 0" class="pagination">
      <div class="page-info">
        共 {{ totalBills }} 条记录，每页
        <select v-model="searchParams.page_size" @change="changePageSize">
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="50">50</option>
          <option value="100">100</option>
        </select>
        条
      </div>
      
      <div class="page-controls">
        <button 
          class="page-btn" 
          @click="changePage(1)" 
          :disabled="currentPage === 1"
        >
          首页
        </button>
        <button 
          class="page-btn" 
          @click="changePage(currentPage - 1)" 
          :disabled="currentPage === 1"
        >
          上一页
        </button>
        <span class="page-current">{{ currentPage }} / {{ totalPages() }}</span>
        <button 
          class="page-btn" 
          @click="changePage(currentPage + 1)" 
          :disabled="currentPage === totalPages() || totalPages() === 0"
        >
          下一页
        </button>
        <button 
          class="page-btn" 
          @click="changePage(totalPages())" 
          :disabled="currentPage === totalPages() || totalPages() === 0"
        >
          末页
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bill-list {
  position: relative;
  min-height: 200px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #2196f3;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.bills-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.bills-table th, .bills-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.bills-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.bills-table tr:hover {
  background-color: #f9f9f9;
}

.bill-type {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.bill-type.purchase {
  background-color: #e3f2fd;
  color: #1976d2;
}

.bill-type.sale {
  background-color: #e8f5e9;
  color: #388e3c;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.page-info {
  color: #666;
}

.page-info select {
  margin: 0 0.5rem;
  padding: 0.25rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.page-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-btn {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-current {
  padding: 0.5rem 0.75rem;
  background-color: #2196f3;
  color: white;
  border-radius: 4px;
}
</style>