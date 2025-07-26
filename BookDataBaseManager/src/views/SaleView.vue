<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SaleOrderSearch from '@/components/sale/SaleOrderSearch.vue'
import SaleOrderList from '@/components/sale/SaleOrderList.vue'
import SaleOrderForm from '@/components/sale/SaleOrderForm.vue'
import Modal from '@/components/common/Modal.vue'
import saleService from '@/services/sale'

const router = useRouter()
const loading = ref(false)
const allOrders = ref([])
const totalOrders = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索参数
const searchParams = ref({
  transaction_no: '',
  payment_method: '',
  operator_id: '',
  min_amount: null,
  max_amount: null,
  start_date: null,
  end_date: null,
  sort_by: 'created_at',
  sort_order: 'desc',
  page: 1,
  page_size: 10,
  exact_transaction_no: false,
  exact_operator_id: false
})

// 重置搜索
const resetSearch = async () => {
  searchParams.value = {
    transaction_no: '',
    payment_method: '',
    operator_id: '',
    min_amount: null,
    max_amount: null,
    start_date: null,
    end_date: null,
    sort_by: 'created_at',
    sort_order: 'desc',
    page: 1,
    page_size: 10,
    exact_transaction_no: false,
    exact_operator_id: false
  }
  await loadAllOrders()
}

// 处理日期格式转换
const formatDateForAPI = (dateString) => {
  if (!dateString) return null;
  // 确保日期格式符合 API 要求 (ISO 格式)
  return new Date(dateString).toISOString();
}

// 修改搜索函数
const handleSearch = async () => {
  // 复制搜索参数并处理日期格式
  const params = { ...searchParams.value };
  
  // 转换日期格式
  if (params.start_date) {
    params.start_date = formatDateForAPI(params.start_date);
  }
  if (params.end_date) {
    // 设置为当天的结束时间
    const endDate = new Date(params.end_date);
    endDate.setHours(23, 59, 59, 999);
    params.end_date = endDate.toISOString();
  }
  
  searchParams.value = params;
  await loadAllOrders(); // 直接调用loadAllOrders函数，避免重复逻辑
}

// 模态框状态
const showCreateOrderModal = ref(false)
const showOrderDetailModal = ref(false)
const selectedOrder = ref(null)
const orderDetail = ref(null)
const createOrderError = ref('')

onMounted(async () => {
  // 加载所有销售订单
  await loadAllOrders()
})

// 加载所有销售订单
const loadAllOrders = async () => {
  try {
    loading.value = true;
    const response = await saleService.getAllSaleOrders(searchParams.value);
    
    // 统一处理响应格式
    if (response.items) {
      // 后端返回的是标准分页格式
      allOrders.value = response.items;
      totalOrders.value = response.total;
      currentPage.value = response.page;
      pageSize.value = response.page_size;
    } else if (response.data) {
      // 后端返回的是另一种格式
      allOrders.value = response.data;
      totalOrders.value = response.total;
      currentPage.value = response.page;
      pageSize.value = response.page_size;
    } else {
      // 直接返回的是数组
      allOrders.value = response;
      totalOrders.value = response.length;
      currentPage.value = 1;
      pageSize.value = response.length;
    }
  } catch (error) {
    console.error('获取销售订单列表失败:', error);
  } finally {
    loading.value = false; // 确保无论如何都会关闭加载状态
  }
}

// 搜索订单
const searchOrders = async () => {
  searchParams.value.page = 1
  await loadAllOrders()
}

// 切换页面
const changePage = async (page) => {
  searchParams.value.page = page
  await loadAllOrders()
}

// 切换每页显示数量
const changePageSize = async () => {
  searchParams.value.page = 1
  await loadAllOrders()
}

// 打开创建订单模态框
const openCreateOrderModal = () => {
  createOrderError.value = ''
  showCreateOrderModal.value = true
}

// 创建新订单
const createOrder = async (orderData) => {
  try {
    loading.value = true
    
    // 从orderData中提取items和payment_method
    const { items, payment_method } = orderData
    
    // 调用API时，直接传递items数组作为请求体，payment_method作为查询参数
    const response = await saleService.createSaleOrder(items, payment_method)
    
    showCreateOrderModal.value = false
    await loadAllOrders()
    alert(`销售订单创建成功！订单号: ${response.transaction_no}`)
  } catch (error) {
    console.error('创建销售订单失败:', error)
    createOrderError.value = error.response?.data?.detail || '创建销售订单失败'
  } finally {
    loading.value = false
  }
}

// 查看订单详情
const viewOrderDetail = async (order) => {
  try {
    loading.value = true
    selectedOrder.value = order
    const detail = await saleService.getSaleOrderDetail(order.id)
    orderDetail.value = detail
    showOrderDetailModal.value = true
  } catch (error) {
    console.error('获取订单详情失败:', error)
    alert('获取订单详情失败: ' + (error.response?.data?.detail || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 返回仪表盘
const backToDashboard = () => {
  router.push('/dashboard')
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
  <div class="sale-view">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="logo">
        <h1>销售管理</h1>
      </div>
      <div class="nav-actions">
        <button class="back-btn" @click="backToDashboard">
          <i class="fa fa-arrow-left"></i> 返回仪表盘
        </button>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="orders-section">
        <div class="section-header">
          <h2>销售订单列表</h2>
          <button class="create-order-btn" @click="openCreateOrderModal">
            <i class="fa fa-plus"></i> 创建销售订单
          </button>
        </div>
        
        <!-- 使用销售订单搜索组件 -->
        <SaleOrderSearch 
          :searchParams="searchParams" 
          :loading="loading"
          @search="searchOrders"
          @reset="resetSearch"
        />
        
        <!-- 使用销售订单列表组件 -->
        <SaleOrderList 
          :orders="allOrders" 
          :loading="loading"
          :totalOrders="totalOrders"
          :currentPage="currentPage"
          :pageSize="pageSize"
          :searchParams="searchParams"
          @view-detail="viewOrderDetail"
          @change-page="changePage"
          @change-page-size="changePageSize"
        />
      </div>
    </main>

    <!-- 创建销售订单模态框 -->
    <Modal 
      :show="showCreateOrderModal" 
      title="创建销售订单" 
      @close="showCreateOrderModal = false"
      :wide="true"
    >
      <SaleOrderForm 
        :loading="loading"
        :error="createOrderError"
        @submit="createOrder"
        @cancel="showCreateOrderModal = false"
      />
    </Modal>

    <!-- 订单详情模态框 -->
    <Modal 
      :show="showOrderDetailModal" 
      title="销售订单详情" 
      @close="showOrderDetailModal = false"
    >
      <div class="order-detail" v-if="orderDetail">
        <div class="order-header">
          <div class="order-info">
            <p><strong>订单ID:</strong> {{ orderDetail.id }}</p>
            <p><strong>交易流水号:</strong> {{ orderDetail.transaction_no }}</p>
            <p><strong>创建时间:</strong> {{ formatDateTime(orderDetail.created_at) }}</p>
          </div>
          <div class="order-meta">
            <p><strong>总金额:</strong> {{ formatAmount(orderDetail.total_amount) }}</p>
            <p><strong>支付方式:</strong> {{ orderDetail.payment_method || '-' }}</p>
            <p><strong>操作员:</strong> {{ orderDetail.operator_name || orderDetail.operator_id }}</p>
          </div>
        </div>
        
        <div class="order-items">
          <h4>订单商品</h4>
          <table class="items-table">
            <thead>
              <tr>
                <th>ISBN</th>
                <th>书名</th>
                <th>单价</th>
                <th>数量</th>
                <th>小计</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in orderDetail.items" :key="item.id">
                <td>{{ item.book_isbn }}</td>
                <td>{{ item.book_title || '-' }}</td>
                <td>{{ formatAmount(item.sold_price) }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ formatAmount(item.total_amount) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="4" class="total-label">总计</td>
                <td class="total-value">{{ formatAmount(orderDetail.total_amount) }}</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </Modal>
    <footer class="footer">
      <p>© 2025 图书管理系统 - 版权所有 Designed by Kevin</p>
    </footer>
  </div>
</template>

<style scoped>
.footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

.sale-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
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

.nav-actions {
  display: flex;
  gap: 1rem;
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
  flex: 1;
  padding: 2rem;
  background-color:transparent;
}

.orders-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  margin: 0;
  color: #2c3e50;
}

.create-order-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.create-order-btn:hover {
  background-color: #388e3c;
}

/* 订单详情样式 */
.order-detail {
  padding: 1rem;
}

.order-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.order-info, .order-meta {
  flex: 1;
}

.order-info p, .order-meta p {
  margin: 0.5rem 0;
}

.order-items h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
}

.items-table th, .items-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.items-table th {
  background-color: #f5f5f5;
  font-weight: 600;
}

.total-label {
  text-align: right;
  font-weight: 600;
}

.total-value {
  font-weight: 600;
  color: #f44336;
}
</style>