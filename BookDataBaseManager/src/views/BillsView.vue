<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BillSearch from '@/components/bill/BillSearch.vue'
import BillList from '@/components/bill/BillList.vue'
import BillChart from '@/components/bill/BillChart.vue'
import billService from '@/services/bill'

const router = useRouter()
const loading = ref(false)
const chartLoading = ref(false)
const allBills = ref([])
const totalBills = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const chartData = ref({
  dates: [],
  amounts: []
})

// 搜索参数
const searchParams = ref({
  bill_type: '',
  start_date: '',
  end_date: '',
  min_amount: null,
  max_amount: null,
  operator_id: '',
  exact_operator_id: false,
  related_order: null,
  sort_by: 'transaction_time',
  sort_order: 'desc',
  page: 1,
  page_size: 10
})

onMounted(async () => {
  // 加载所有账单
  await loadAllBills()
  // 加载图表数据
  await loadChartData()
})

// 加载所有账单
const loadAllBills = async () => {
  try {
    loading.value = true
    const response = await billService.getAllBills(searchParams.value)
    
    allBills.value = response.items
    totalBills.value = response.total
    currentPage.value = response.page
    pageSize.value = response.page_size
    
  } catch (error) {
    console.error('获取账单列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载图表数据
const loadChartData = async () => {
  try {
    chartLoading.value = true
    // 只传递日期和类型过滤条件
    const params = {
      bill_type: searchParams.value.bill_type,
      start_date: searchParams.value.start_date,
      end_date: searchParams.value.end_date,
      operator_id: searchParams.value.operator_id,
      exact_operator_id: searchParams.value.exact_operator_id,
      related_order: searchParams.value.related_order,
      min_amount: searchParams.value.min_amount,
      max_amount: searchParams.value.max_amount
    }
    const response = await billService.getBillTrends(params)
    chartData.value = response
  } catch (error) {
    console.error('获取账单趋势数据失败:', error)
  } finally {
    chartLoading.value = false
  }
}

// 搜索账单
const searchBills = async () => {
  searchParams.value.page = 1
  await loadAllBills()
  await loadChartData()
}

// 重置搜索
const resetSearch = async () => {
  searchParams.value = {
    bill_type: '',
    start_date: '',
    end_date: '',
    min_amount: null,
    max_amount: null,
    operator_id: '',
    exact_operator_id: false,
    related_order: null,
    sort_by: 'transaction_time',
    sort_order: 'desc',
    page: 1,
    page_size: 10
  }
  await loadAllBills()
  await loadChartData()
}

// 切换页面
const changePage = async (page) => {
  searchParams.value.page = page
  await loadAllBills()
}

// 切换每页显示数量
const changePageSize = async () => {
  searchParams.value.page = 1
  await loadAllBills()
}

// 返回仪表盘
const backToDashboard = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="bills-view">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="logo">
        <h1>财务管理</h1>
      </div>
      <div class="nav-actions">
        <button class="back-btn" @click="backToDashboard">
          <i class="fa fa-arrow-left"></i> 返回仪表盘
        </button>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="bills-section">
        <div class="section-header">
          <h2>账单列表</h2>
          <div class="summary-info">
            <div class="summary-item">
              <span class="label">总记录数:</span>
              <span class="value">{{ totalBills }}</span>
            </div>
          </div>
        </div>
        
        <!-- 使用账单搜索组件 -->
        <BillSearch 
          :searchParams="searchParams" 
          :loading="loading"
          @search="searchBills"
          @reset="resetSearch"
        />
        
        <!-- 账单流水趋势图 -->
        <div class="chart-section">
          <h3>账单流水趋势</h3>
          <BillChart 
            :chartData="chartData" 
            :loading="chartLoading"
          />
        </div>
        
        <!-- 使用账单列表组件 -->
        <BillList 
          :bills="allBills" 
          :loading="loading"
          :totalBills="totalBills"
          :currentPage="currentPage"
          :pageSize="pageSize"
          :searchParams="searchParams"
          @change-page="changePage"
          @change-page-size="changePageSize"
        />
      </div>
    </main>
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

.bills-view {
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

.bills-section {
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

.chart-section {
  margin-bottom: 2rem;
}

.chart-section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.2rem;
}

.summary-info {
  display: flex;
  gap: 1.5rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.summary-item .label {
  font-weight: 500;
  color: #666;
}

.summary-item .value {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.1rem;
}
</style>