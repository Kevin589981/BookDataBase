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

const emit = defineEmits(['pay', 'return', 'arrive', 'change-page', 'change-page-size'])

const handlePageChange = (page) => {
  emit('change-page', page)
}

const handlePageSizeChange = () => {
  emit('change-page-size')
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 格式化金额
const formatCurrency = (amount) => {
  return `¥${parseFloat(amount).toFixed(2)}`
}

// 获取状态标签样式
const getStatusClass = (status) => {
  switch (status) {
    case '未付款': return 'status-unpaid'
    case '已付款': return 'status-paid'
    case '已退货': return 'status-returned'
    case '已到货': return 'status-arrived'
    default: return ''
  }
}

// 判断是否可以执行操作
const canPay = (order) => order.payment_status === '未付款'
const canReturn = (order) => order.payment_status === '未付款'
const canArrive = (order) => order.payment_status === '已付款'
</script>

<template>
  <div class="purchase-list">
    <div class="list-header">
      <div class="page-info">
        共 <span class="highlight">{{ totalOrders }}</span> 条记录
      </div>
      <div class="page-size-selector">
        每页显示:
        <select v-model="searchParams.page_size" @change="handlePageSizeChange">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>
    </div>
    
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>订单ID</th>
            <th>ISBN</th>
            <th>进货单价</th>
            <th>数量</th>
            <th>总金额</th>
            <th>订单日期</th>
            <th>状态</th>
            <th>下单操作员</th>
            <th>付款/退货操作员</th>
            <th>到货操作员</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr>
              <td colspan="11" class="loading-cell">加载中...</td>
            </tr>
          </template>
          <template v-else-if="orders.length === 0">
            <tr>
              <td colspan="11" class="empty-cell">暂无数据</td>
            </tr>
          </template>
          <template v-else>
            <tr v-for="order in orders" :key="order.id">
              <td>{{ order.id }}</td>
              <td>{{ order.book_isbn }}</td>
              <td>{{ formatCurrency(order.purchase_price) }}</td>
              <td>{{ order.quantity }}</td>
              <td>{{ formatCurrency(order.total_amount) }}</td>
              <td>{{ formatDate(order.order_date) }}</td>
              <td>
                <span :class="['status-badge', getStatusClass(order.payment_status)]">
                  {{ order.payment_status }}
                </span>
              </td>
              <td>{{ order.operator_id }}</td>
              <td>{{ order.operator_id2 || '-' }}</td>
              <td>{{ order.operator_id3 || '-' }}</td>
              <td class="actions-cell">
                <div class="actions-container">
                  <button 
                    v-if="canPay(order)" 
                    @click="emit('pay', order)" 
                    class="action-btn pay-btn"
                    :disabled="loading"
                  >
                    付款
                  </button>
                  <button 
                    v-if="canReturn(order)" 
                    @click="emit('return', order)" 
                    class="action-btn return-btn"
                    :disabled="loading"
                  >
                    退货
                  </button>
                  <button 
                    v-if="canArrive(order)" 
                    @click="emit('arrive', order)" 
                    class="action-btn arrive-btn"
                    :disabled="loading"
                  >
                    到货
                  </button>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    
    <!-- 分页控件 -->
    <div class="pagination" v-if="totalOrders > 0">
      <button 
        class="page-btn" 
        :disabled="currentPage === 1 || loading" 
        @click="handlePageChange(currentPage - 1)"
      >
        上一页
      </button>
      
      <div class="page-info">
        第 {{ currentPage }} 页，共 {{ Math.ceil(totalOrders / pageSize) }} 页
      </div>
      
      <button 
        class="page-btn" 
        :disabled="currentPage >= Math.ceil(totalOrders / pageSize) || loading" 
        @click="handlePageChange(currentPage + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<style scoped>
.purchase-list {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background-color: #f5f5f5;
  border-bottom: 1px solid #eee;
}

.highlight {
  color: #2196f3;
  font-weight: bold;
}

.page-size-selector select {
  margin-left: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.table-container {
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
  background-color: #f9f9f9;
  font-weight: 600;
  color: #333;
}

.loading-cell, .empty-cell {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-unpaid {
  background-color: #ffecb3;
  color: #ff8f00;
}

.status-paid {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status-returned {
  background-color: #ffebee;
  color: #d32f2f;
}

.status-arrived {
  background-color: #e8f5e9;
  color: #388e3c;
}

.actions-cell {
  padding: 0.5rem 1rem;
}

.actions-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  min-height: 28px;
  align-items: center;
}

.action-btn {
  padding: 0.25rem 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.3s;
  height: 28px; 
  line-height: 1; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center;
}

.pay-btn {
  background-color: #2196f3;
  color: white;
}

.pay-btn:hover:not(:disabled) {
  background-color: #1976d2;
}

.return-btn {
  background-color: #f44336;
  color: white;
}

.return-btn:hover:not(:disabled) {
  background-color: #d32f2f;
}

.arrive-btn {
  background-color: #4caf50;
  color: white;
}

.arrive-btn:hover:not(:disabled) {
  background-color: #388e3c;
}

.action-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background-color: #f5f5f5;
  border-top: 1px solid #eee;
}

.page-btn {
  padding: 0.5rem 1rem;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.page-btn:hover:not(:disabled) {
  background-color: #1976d2;
}

.page-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>