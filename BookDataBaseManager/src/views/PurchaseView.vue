<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PurchaseSearch from '@/components/purchase/PurchaseSearch.vue'
import PurchaseList from '@/components/purchase/PurchaseList.vue'
import PurchaseForm from '@/components/purchase/PurchaseForm.vue'
import Modal from '@/components/common/Modal.vue'
import purchaseService from '@/services/purchase'

const router = useRouter()
const loading = ref(false)
const allOrders = ref([])
const totalOrders = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索参数
const searchParams = ref({
  order_id: null,
  book_isbn: '',
  payment_status: '',
  operator_id: '',
  operator_id2: '',
  operator_id3: '',
  start_date: '',
  end_date: '',
  min_price: null,
  max_price: null,
  min_quantity: null,
  max_quantity: null,
  sort_by: 'order_date',
  sort_order: 'desc',
  page: 1,
  page_size: 10,
  exact_isbn: false,
  exact_operator_id: false,
  exact_operator_id2: false,
  exact_operator_id3: false
})

// 模态框状态
const showCreateOrderModal = ref(false)
const showArriveModal = ref(false)
const selectedOrder = ref(null)

// 表单状态
const newOrderForm = ref({
  isbn: '',
  quantity: 1,
  purchase_price: '',
  isNewBook: false
})
const retailPriceForm = ref({
  retail_price: ''
})
const createOrderError = ref('')
const arriveOrderError = ref('')

onMounted(async () => {
  // 加载所有进货订单
  await loadAllOrders()
})

// 加载所有进货订单
const loadAllOrders = async () => {
  try {
    loading.value = true
    const response = await purchaseService.getAllPurchaseOrders(searchParams.value)
    
    allOrders.value = response.items
    totalOrders.value = response.total
    currentPage.value = response.page
    pageSize.value = response.page_size
    
  } catch (error) {
    console.error('获取进货订单列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索订单
const searchOrders = async () => {
  searchParams.value.page = 1
  await loadAllOrders()
}

// 重置搜索
const resetSearch = async () => {
  searchParams.value = {
    order_id: null,
    book_isbn: '',
    payment_status: '',
    operator_id: '',
    operator_id2: '',
    operator_id3: '',
    start_date: '',
    end_date: '',
    min_price: null,
    max_price: null,
    min_quantity: null,
    max_quantity: null,
    sort_by: 'order_date',
    sort_order: 'desc',
    page: 1,
    page_size: 10,
    exact_isbn: false,
    exact_operator_id: false,
    exact_operator_id2: false,
    exact_operator_id3: false
  }
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
  // 重置表单
  newOrderForm.value = {
    isbn: '',
    quantity: 1,
    purchase_price: '',
    isNewBook: false
  }
  createOrderError.value = ''
  showCreateOrderModal.value = true
}

// 创建新订单
const createOrder = async (formData) => {
  try {
    loading.value = true
    await purchaseService.createPurchaseOrder(formData)
    showCreateOrderModal.value = false
    await loadAllOrders()
    alert('进货订单创建成功')
  } catch (error) {
    console.error('创建进货订单失败:', error)
    createOrderError.value = error.response?.data?.detail || '创建进货订单失败'
  } finally {
    loading.value = false
  }
}

// 支付订单
const payOrder = async (order) => {
  try {
    if (!confirm(`确定要支付订单 #${order.id} 吗？`)) return
    
    loading.value = true
    await purchaseService.payPurchaseOrder(order.id)
    await loadAllOrders()
    alert('订单支付成功')
  } catch (error) {
    console.error('支付订单失败:', error)
    alert('支付订单失败: ' + (error.response?.data?.detail || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 退货订单
const returnOrder = async (order) => {
  try {
    if (!confirm(`确定要退货订单 #${order.id} 吗？此操作不可撤销。`)) return
    
    loading.value = true
    await purchaseService.returnPurchaseOrder(order.id)
    await loadAllOrders()
    alert('订单退货成功')
  } catch (error) {
    console.error('退货订单失败:', error)
    alert('退货订单失败: ' + (error.response?.data?.detail || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 打开到货确认模态框
const openArriveModal = (order) => {
  selectedOrder.value = order
  retailPriceForm.value = {
    retail_price: ''
  }
  arriveOrderError.value = ''
  showArriveModal.value = true
}

// 确认到货
const confirmArrive = async () => {
  try {
    if (!selectedOrder.value) return
    
    loading.value = true
    const retailPrice = retailPriceForm.value.retail_price 
      ? parseFloat(retailPriceForm.value.retail_price) 
      : null
      
    await purchaseService.arrivePurchaseOrder(selectedOrder.value.id, retailPrice)
    showArriveModal.value = false
    await loadAllOrders()
    alert('确认到货成功')
  } catch (error) {
    console.error('确认到货失败:', error)
    arriveOrderError.value = error.response?.data?.detail || '确认到货失败'
  } finally {
    loading.value = false
  }
}

// 返回仪表盘
const backToDashboard = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="purchase-view">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="logo">
        <h1>进货管理</h1>
      </div>
      <div class="nav-actions">
        <button class="back-btn" @click="backToDashboard">
          <i class="fa fa-arrow-left"></i> 返回仪表盘
        </button>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="purchase-section">
        <div class="section-header">
          <h2>进货订单列表</h2>
          <button class="create-order-btn" @click="openCreateOrderModal">
            <i class="fa fa-plus"></i> 创建进货订单
          </button>
        </div>
        
        <!-- 使用进货订单搜索组件 -->
        <PurchaseSearch 
          :searchParams="searchParams" 
          :loading="loading"
          @search="searchOrders"
          @reset="resetSearch"
        />
        
        <!-- 使用进货订单列表组件 -->
        <PurchaseList 
          :orders="allOrders" 
          :loading="loading"
          :totalOrders="totalOrders"
          :currentPage="currentPage"
          :pageSize="pageSize"
          :searchParams="searchParams"
          @pay="payOrder"
          @return="returnOrder"
          @arrive="openArriveModal"
          @change-page="changePage"
          @change-page-size="changePageSize"
        />
      </div>
    </main>

    <!-- 模态框部分保持不变 -->
    <Modal 
      :show="showCreateOrderModal" 
      title="创建进货订单" 
      @close="showCreateOrderModal = false"
    >
      <PurchaseForm 
        :purchase="newOrderForm" 
        :loading="loading"
        :error="createOrderError"
        @submit="createOrder"
        @cancel="showCreateOrderModal = false"
      />
    </Modal>

    <Modal 
      :show="showArriveModal" 
      title="确认到货" 
      @close="showArriveModal = false"
    >
      <div class="arrive-form">
        <div v-if="arriveOrderError" class="form-error">{{ arriveOrderError }}</div>
        
        <div v-if="selectedOrder" class="order-info">
          <p><strong>订单ID:</strong> {{ selectedOrder.id }}</p>
          <p><strong>ISBN:</strong> {{ selectedOrder.book_isbn }}</p>
          <p><strong>数量:</strong> {{ selectedOrder.quantity }}</p>
          <p><strong>进货单价:</strong> ¥{{ selectedOrder.purchase_price.toFixed(2) }}</p>
        </div>
        
        <div class="form-group">
          <label for="retail_price">设置零售价 (可选)</label>
          <input 
            type="number" 
            id="retail_price" 
            v-model="retailPriceForm.retail_price" 
            placeholder="图书零售价"
            min="0.01"
            step="0.01"
          />
          <div class="field-hint">如不设置，将保持原有零售价</div>
        </div>
        
        <div class="form-actions">
          <button 
            type="button" 
            class="submit-btn" 
            @click="confirmArrive" 
            :disabled="loading"
          >
            {{ loading ? '处理中...' : '确认到货' }}
          </button>
          <button 
            type="button" 
            class="cancel-btn" 
            @click="showArriveModal = false" 
            :disabled="loading"
          >
            取消
          </button>
        </div>
      </div>
    </Modal>
    
  </div>
  <footer class="footer">
      <p>© 2025 图书管理系统 - 版权所有 Designed by Kevin</p>
    </footer>
</template>

<style scoped>
.footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
.purchase-view {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
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

.purchase-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h2 {
  margin: 0;
  color: #2c3e50;
}

.create-order-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
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

/* 到货确认表单样式 */
.arrive-form {
  padding: 1rem;
}

.form-error {
  background-color: #ffebee;
  color: #d32f2f;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.order-info {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.order-info p {
  margin: 0.5rem 0;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #2196f3;
}

.field-hint {
  color: #666;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-btn, .cancel-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn {
  background-color: #4caf50;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background-color: #388e3c;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
}

.cancel-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.submit-btn:disabled, .cancel-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>