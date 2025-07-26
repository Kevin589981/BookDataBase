<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue'
import api from '@/utils/api'

const props = defineProps({
  purchase: {
    type: Object,
    required: true
  },
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

const formData = ref({...props.purchase})
const isCheckingIsbn = ref(false)
const isbnError = ref('')

// 当外部purchase属性变化时，更新本地表单数据
watch(() => props.purchase, (newPurchase) => {
  formData.value = {...newPurchase}
}, { deep: true })

// 检查ISBN是否存在
const checkIsbnExists = async () => {
  if (!formData.value.isbn || !/^\d{13}$/.test(formData.value.isbn)) {
    return
  }
  
  try {
    isCheckingIsbn.value = true
    isbnError.value = ''
    
    // 调用API检查ISBN是否存在
    const response = await api.get(`/books/?isbn=${formData.value.isbn}`)
    
    // 检查返回的数据是否为空
    if (response.data && response.data.data && response.data.data.length > 0) {
      // 如果ISBN存在，则不需要填写新书信息
      formData.value.isNewBook = false
      formData.value.book_info = null
    } else {
      // 如果返回的数据为空，说明ISBN不存在
      formData.value.isNewBook = true
      formData.value.book_info = {
        title: '',
        author: '',
        publisher: '',
        retail_price: ''
      }
      isbnError.value = '该ISBN不存在于系统中，请填写新书信息'
    }
    
  } catch (error) {
    console.error('检查ISBN失败:', error)
    // 如果发生错误，默认需要填写新书信息
    formData.value.isNewBook = true
    formData.value.book_info = {
      title: '',
      author: '',
      publisher: '',
      retail_price: ''
    }
    isbnError.value = '检查ISBN失败，请填写新书信息'
  } finally {
    isCheckingIsbn.value = false
  }
}

// 表单验证
const validationErrors = ref({})

const validateForm = () => {
  const errors = {}
  
  // ISBN验证
  if (!formData.value.isbn) {
    errors.isbn = 'ISBN不能为空'
  } else if (!/^\d{13}$/.test(formData.value.isbn)) {
    errors.isbn = 'ISBN必须是13位数字'
  }
  
  // 数量验证
  if (!formData.value.quantity) {
    errors.quantity = '数量不能为空'
  } else if (isNaN(formData.value.quantity) || parseInt(formData.value.quantity) <= 0) {
    errors.quantity = '数量必须是大于0的整数'
  }
  
  // 单价验证
  if (!formData.value.purchase_price) {
    errors.purchase_price = '进货单价不能为空'
  } else if (isNaN(formData.value.purchase_price) || parseFloat(formData.value.purchase_price) <= 0) {
    errors.purchase_price = '进货单价必须是大于0的数字'
  }
  
  // 如果是新书，验证书籍信息
  if (formData.value.isNewBook) {
    if (!formData.value.book_info?.title) {
      errors.title = '新书标题不能为空'
    }
  }
  
  validationErrors.value = errors
  return Object.keys(errors).length === 0
}

const handleSubmit = () => {
  if (validateForm()) {
    // 转换数据类型
    const submitData = {
      isbn: formData.value.isbn,
      quantity: parseInt(formData.value.quantity),
      purchase_price: parseFloat(formData.value.purchase_price)
    }
    
    // 如果是新书，添加书籍信息
    if (formData.value.isNewBook && formData.value.book_info) {
      submitData.book_info = {
        title: formData.value.book_info.title,
        author: formData.value.book_info.author || null,
        publisher: formData.value.book_info.publisher || null,
        retail_price: formData.value.book_info.retail_price ? parseFloat(formData.value.book_info.retail_price) : null
      }
    }
    
    emit('submit', submitData)
  }
}

const handleCancel = () => {
  emit('cancel')
}

// 切换是否为新书
const toggleNewBook = () => {
  if (!formData.value.isNewBook) {
    // 初始化书籍信息
    formData.value.book_info = {
      title: '',
      author: '',
      publisher: '',
      retail_price: ''
    }
  } else {
    // 清除书籍信息
    formData.value.book_info = null
  }
}
</script>

<template>
  <div class="purchase-form">
    <div v-if="error" class="form-error">{{ error }}</div>
    
    <div class="form-group">
      <label for="isbn">ISBN <span class="required">*</span></label>
      <div class="isbn-input-group">
        <input 
          type="text" 
          id="isbn" 
          v-model="formData.isbn" 
          placeholder="13位数字ISBN"
          maxlength="13"
          @blur="checkIsbnExists"
        />
        <span v-if="isCheckingIsbn" class="isbn-checking">检查中...</span>
      </div>
      <div v-if="validationErrors.isbn" class="field-error">{{ validationErrors.isbn }}</div>
      <div v-else-if="isbnError" class="field-warning">{{ isbnError }}</div>
    </div>
    
    <div class="form-group">
      <label for="quantity">进货数量 <span class="required">*</span></label>
      <input 
        type="number" 
        id="quantity" 
        v-model="formData.quantity" 
        placeholder="进货数量"
        min="1"
      />
      <div v-if="validationErrors.quantity" class="field-error">{{ validationErrors.quantity }}</div>
    </div>
    
    <div class="form-group">
      <label for="purchase_price">进货单价 <span class="required">*</span></label>
      <input 
        type="number" 
        id="purchase_price" 
        v-model="formData.purchase_price" 
        placeholder="进货单价"
        min="0.01"
        step="0.01"
      />
      <div v-if="validationErrors.purchase_price" class="field-error">{{ validationErrors.purchase_price }}</div>
    </div>
    
    <!-- 新书信息表单 -->
    <div v-if="formData.isNewBook" class="new-book-info">
      <h3>新书信息</h3>
      
      <div class="form-group">
        <label for="book_title">书名 <span class="required">*</span></label>
        <input 
          type="text" 
          id="book_title" 
          v-model="formData.book_info.title" 
          placeholder="图书标题"
        />
        <div v-if="validationErrors.title" class="field-error">{{ validationErrors.title }}</div>
      </div>
      
      <div class="form-group">
        <label for="book_author">作者</label>
        <input 
          type="text" 
          id="book_author" 
          v-model="formData.book_info.author" 
          placeholder="图书作者"
        />
      </div>
      
      <div class="form-group">
        <label for="book_publisher">出版社</label>
        <input 
          type="text" 
          id="book_publisher" 
          v-model="formData.book_info.publisher" 
          placeholder="出版社名称"
        />
      </div>
      
      <div class="form-group">
        <label for="book_retail_price">零售价</label>
        <input 
          type="number" 
          id="book_retail_price" 
          v-model="formData.book_info.retail_price" 
          placeholder="图书零售价"
          min="0.01"
          step="0.01"
        />
      </div>
    </div>
    
    <div class="form-actions">
      <button 
        type="button" 
        class="submit-btn" 
        @click="handleSubmit" 
        :disabled="loading"
      >
        {{ loading ? '提交中...' : '创建订单' }}
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
.purchase-form {
  padding: 1rem;
}

.form-error {
  background-color: #ffebee;
  color: #d32f2f;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
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

.required {
  color: #f44336;
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

.field-error {
  color: #f44336;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.field-warning {
  color: #ff9800;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.isbn-input-group {
  display: flex;
  align-items: center;
}

.isbn-checking {
  margin-left: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.checkbox-group {
  margin-top: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
}

.new-book-info {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.new-book-info h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
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