<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  orders: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  totalOrders: {
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
  }
})

const emit = defineEmits(['view-detail', 'change-page', 'change-page-size'])

const viewOrderDetail = (order) => {
  emit('view-detail', order)
}

const changePage = (page) => {
  emit('change-page', page)
}

const changePageSize = () => {
  emit('change-page-size')
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
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
  if (amount === null || amount === undefined) return '-'
  return `¥${parseFloat(amount).toFixed(2)}`
}
</script>

<template>
  <div class="order-list">
    <div v-if="loading" class="loading-indicator">
      <i class="fa fa-spinner fa-spin"></i> 加载中...
    </div>
    
    <div v-else-if="orders.length === 0" class="no-data">
      <i class="fa fa-info-circle"></i> 没有找到匹配的销售订单
    </div>
    
    <table v-else class="orders-table">
      <thead>
        <tr>
          <th>订单ID</th>
          <th>交易流水号</th>
          <th>创建时间</th>
          <th>总金额</th>
          <th>支付方式</th>
          <th>操作员</th>
          <th>操作员工号</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.transaction_no }}</td>
          <td>{{ formatDateTime(order.created_at) }}</td>
          <td>{{ formatAmount(order.total_amount) }}</td>
          <td>{{ order.payment_method || '-' }}</td>
          <td>{{ order.operator_name  || '-' }}</td>
          <td>{{ order.operator_id || '-' }}</td>
          <td>
            <button class="view-btn" @click="viewOrderDetail(order)">
              <i class="fa fa-eye"></i> 查看详情
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    
    <!-- 分页控件 -->
    <div class="pagination" v-if="orders.length > 0">
      <div class="page-size">
        <span>每页显示:</span>
        <select v-model="searchParams.page_size" @change="changePageSize">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>
      
      <div class="page-info">
        显示 {{ (currentPage - 1) * pageSize + 1 }} - 
        {{ Math.min(currentPage * pageSize, totalOrders) }} 
        条，共 {{ totalOrders }} 条
      </div>
      
      <div class="page-controls">
        <button 
          class="page-btn" 
          :disabled="currentPage === 1" 
          @click="changePage(1)"
        >
          <i class="fa fa-angle-double-left"></i>
        </button>
        <button 
          class="page-btn" 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)"
        >
          <i class="fa fa-angle-left"></i>
        </button>
        
        <span class="page-current">{{ currentPage }}</span>
        
        <button 
          class="page-btn" 
          :disabled="currentPage >= Math.ceil(totalOrders / pageSize)" 
          @click="changePage(currentPage + 1)"
        >
          <i class="fa fa-angle-right"></i>
        </button>
        <button 
          class="page-btn" 
          :disabled="currentPage >= Math.ceil(totalOrders / pageSize)" 
          @click="changePage(Math.ceil(totalOrders / pageSize))"
        >
          <i class="fa fa-angle-double-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.order-list {
  margin-top: 1rem;
}

.loading-indicator, .no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
}

.loading-indicator i, .no-data i {
  margin-right: 0.5rem;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.orders-table th, .orders-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.orders-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.orders-table tr:hover {
  background-color: #f9f9f9;
}

.view-btn {
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
}

.view-btn:hover {
  background-color: #1976d2;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-top: 1px solid #eee;
}

.page-size {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-size select {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.page-info {
  color: #666;
}

.page-controls {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.page-btn {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  padding: 0.25rem 0.5rem;
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
  padding: 0.25rem 0.5rem;
  background-color: #2196f3;
  color: white;
  border-radius: 4px;
  min-width: 1.5rem;
  text-align: center;
}
</style>