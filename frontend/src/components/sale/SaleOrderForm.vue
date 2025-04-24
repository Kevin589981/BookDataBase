<script setup>
import { ref, defineProps, defineEmits, onMounted } from 'vue'
import bookService from '@/services/book'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['submit', 'cancel'])

// 表单数据
const items = ref([{ book_isbn: '', quantity: 1, book_info: null, searchQuery: '' }])
const paymentMethod = ref('现金')
const totalAmount = ref(0)

// 书籍搜索
const searchResults = ref([])
const isSearching = ref(false)
const activeSearchIndex = ref(null)
// 添加防抖定时器
const searchDebounceTimer = ref(null)

// 表单验证
const validationErrors = ref({})

// 添加防抖搜索函数
const debouncedSearchBooks = (index) => {
  // 清除之前的定时器
  if (searchDebounceTimer.value) {
    clearTimeout(searchDebounceTimer.value)
  }
  
  // 设置新的定时器，1秒后执行搜索
  searchDebounceTimer.value = setTimeout(() => {
    searchBooks(index)
  }, 1000) // 1000毫秒 = 1秒
}

// 搜索书籍
const searchBooks = async (index) => {
  if (!items.value[index].searchQuery) {
    searchResults.value = []
    return
  }
  
  try {
    isSearching.value = true
    activeSearchIndex.value = index
    
    // 创建两个搜索请求
    const isbnSearchParams = {
      isbn: items.value[index].searchQuery,
      page: 1,
      page_size: 10
    }
    
    const titleSearchParams = {
      title: items.value[index].searchQuery,
      page: 1,
      page_size: 10
    }
    
    // 并行发起两个请求
    const [isbnResponse, titleResponse] = await Promise.all([
      bookService.getAllBooks(isbnSearchParams),
      bookService.getAllBooks(titleSearchParams)
    ])
    
    // 合并结果并去重
    const isbnResults = isbnResponse.items || []
    const titleResults = titleResponse.items || []
    
    // 使用Map去重，以ISBN为键
    const uniqueBooks = new Map()
    
    // 添加ISBN搜索结果
    isbnResults.forEach(book => {
      if (book.stock > 0) {
        uniqueBooks.set(book.isbn, book)
      }
    })
    
    // 添加标题搜索结果
    titleResults.forEach(book => {
      if (book.stock > 0) {
        uniqueBooks.set(book.isbn, book)
      }
    })
    
    // 转换回数组
    searchResults.value = Array.from(uniqueBooks.values())
  } catch (error) {
    console.error('搜索书籍失败:', error)
  } finally {
    isSearching.value = false
  }
}
// 选择书籍
const selectBook = (book, index) => {
  items.value[index].book_isbn = book.isbn
  items.value[index].book_info = book
  items.value[index].searchQuery = ''
  searchResults.value = []
  activeSearchIndex.value = null
  calculateTotal()
}

// 添加商品项
const addItem = () => {
  items.value.push({ book_isbn: '', quantity: 1, book_info: null, searchQuery: '' })
}

// 移除商品项
const removeItem = (index) => {
  if (items.value.length > 1) {
    items.value.splice(index, 1)
    calculateTotal()
  }
}

// 计算总金额
const calculateTotal = () => {
  totalAmount.value = items.value.reduce((sum, item) => {
    if (item.book_info && item.book_info.retail_price) {
      return sum + (item.book_info.retail_price * item.quantity)
    }
    return sum
  }, 0)
}

// 数量变更时重新计算总金额
const updateQuantity = (index) => {
  // 确保数量为正整数
  const qty = parseInt(items.value[index].quantity)
  items.value[index].quantity = qty > 0 ? qty : 1
  
  // 检查库存
  const item = items.value[index]
  if (item.book_info && item.quantity > item.book_info.stock) {
    items.value[index].quantity = item.book_info.stock
  }
  
  calculateTotal()
}

// 表单验证
const validateForm = () => {
  const errors = {}
  
  // 检查是否有商品
  if (items.value.length === 0) {
    errors.items = '请至少添加一件商品'
  }
  
  // 检查每个商品是否有效
  let hasInvalidItem = false
  items.value.forEach((item, index) => {
    if (!item.book_isbn || !item.book_info) {
      hasInvalidItem = true
    }
  })
  
  if (hasInvalidItem) {
    errors.items = '请确保所有商品都已正确选择'
  }
  
  validationErrors.value = errors
  return Object.keys(errors).length === 0
}

// 提交表单
const handleSubmit = () => {
  if (validateForm()) {
    // 修改：直接提交items数组，而不是包装在对象中
    const orderData = items.value.map(item => ({
      book_isbn: item.book_isbn,
      quantity: item.quantity
    }))
    
    // 将支付方式作为查询参数传递，而不是包含在请求体中
    emit('submit', { items: orderData, payment_method: paymentMethod.value })
  }
}

// 取消
const handleCancel = () => {
  emit('cancel')
}

// 监听数量变化
onMounted(() => {
  calculateTotal()
})
</script>

<template>
  <div class="sale-form">
    <div v-if="error" class="form-error">{{ error }}</div>
    
    <h3>创建销售订单</h3>
    
    <div class="items-section">
      <div class="section-header">
        <h4>商品列表</h4>
        <button type="button" class="add-item-btn" @click="addItem">
          <i class="fa fa-plus"></i> 添加商品
        </button>
      </div>
      
      <div v-if="validationErrors.items" class="field-error">{{ validationErrors.items }}</div>
      
      <div class="items-list">
        <div v-for="(item, index) in items" :key="index" class="item-row">
          <div class="item-search">
            <label :for="'book-search-' + index">书籍</label>
            <div class="search-container">
              <input 
                :id="'book-search-' + index"
                type="text"
                v-model="items[index].searchQuery"
                @focus="activeSearchIndex = index"
                @input="debouncedSearchBooks(index)"
                placeholder="输入ISBN或书名搜索"
              />
              <div v-if="isSearching && activeSearchIndex === index" class="search-loading">
                <i class="fa fa-spinner fa-spin"></i>
              </div>
              <div v-if="searchResults.length > 0 && activeSearchIndex === index" class="search-results">
                <div 
                  v-for="book in searchResults" 
                  :key="book.isbn" 
                  class="search-result-item"
                  @click="selectBook(book, index)"
                >
                  <div class="book-title">{{ book.title }}</div>
                  <div class="book-info">
                    <span>ISBN: {{ book.isbn }}</span>
                    <span>价格: ¥{{ book.retail_price }}</span>
                    <span>库存: {{ book.stock }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="item-details" v-if="item.book_info">
            <div class="book-info-display">
              <div class="book-title">{{ item.book_info.title }}</div>
              <div class="book-meta">
                <span>ISBN: {{ item.book_info.isbn }}</span>
                <span>单价: ¥{{ item.book_info.retail_price }}</span>
                <span>库存: {{ item.book_info.stock }}</span>
              </div>
            </div>
            
            <div class="quantity-control">
              <label :for="'quantity-' + index">数量</label>
              <input 
                :id="'quantity-' + index"
                type="number" 
                v-model="item.quantity" 
                min="1" 
                :max="item.book_info.stock"
                @change="updateQuantity(index)"
              />
            </div>
            
            <div class="item-amount">
              <span>金额: ¥{{ (item.book_info.retail_price * item.quantity).toFixed(2) }}</span>
            </div>
            
            <button type="button" class="remove-item-btn" @click="removeItem(index)">
              <i class="fa fa-trash"></i>
            </button>
          </div>
          
          <div class="item-placeholder" v-else>
            请搜索并选择书籍
          </div>
        </div>
      </div>
    </div>
    
    <div class="payment-section">
      <div class="form-group">
        <label for="payment-method">支付方式</label>
        <select id="payment-method" v-model="paymentMethod">
          <option value="现金">现金</option>
          <option value="移动支付">移动支付</option>
          <option value="银行卡">银行卡</option>
        </select>
      </div>
      
      <div class="total-amount">
        <span>总金额:</span>
        <span class="amount">¥{{ totalAmount.toFixed(2) }}</span>
      </div>
    </div>
    
    <div class="form-actions">
      <button 
        type="button" 
        class="submit-btn" 
        @click="handleSubmit" 
        :disabled="loading || totalAmount <= 0"
      >
        {{ loading ? '提交中...' : '提交订单' }}
      </button>
      <button 
        type="button" 
        class="cancel-btn" 
        @click="handleCancel" 
        :disabled="loading"
      >
        取消
      </button>
    </div>
  </div>
</template>

<style scoped>
.sale-form {
  padding: 1rem;
}

.form-error {
  background-color: #ffebee;
  color: #d32f2f;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.items-section {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h4 {
  margin: 0;
  color: #2c3e50;
}

.add-item-btn {
  background-color: #4caf50;
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

.add-item-btn:hover {
  background-color: #388e3c;
}

.field-error {
  color: #f44336;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.items-list {
  border: 1px solid #ddd;
  border-radius: 4px;
}

.item-row {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.item-row:last-child {
  border-bottom: none;
}

.item-search {
  margin-bottom: 1rem;
}

.search-container {
  position: relative;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus, select:focus {
  outline: none;
  border-color: #2196f3;
}

.search-loading {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 4px 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.search-result-item {
  padding: 0.75rem;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background-color: #f5f5f5;
}

.book-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.book-info {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.item-details {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.book-info-display {
  flex: 1;
}

.book-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.quantity-control {
  display: flex;
  flex-direction: column;
  width: 80px;
}

.quantity-control input {
  padding: 0.5rem;
}

.item-amount {
  width: 120px;
  text-align: right;
  font-weight: 500;
}

.remove-item-btn {
  background-color: #f44336;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-item-btn:hover {
  background-color: #d32f2f;
}

.item-placeholder {
  color: #999;
  font-style: italic;
  padding: 0.5rem 0;
}

.payment-section {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.form-group {
  min-width: 180px;
}

.total-amount {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2196f3;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.amount {
  color: #f44336;
  font-size: 1.5rem;
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
  background-color: #2196f3;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background-color: #1976d2;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
}

.cancel-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>