<script setup>
import { ref, defineProps, defineEmits, watch, onMounted } from 'vue'

const props = defineProps({
  book: {
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
  },
  mode: {
    type: String,
    default: 'create', // 'create' 或 'edit'
    validator: (value) => ['create', 'edit'].includes(value)
  }
})

// 添加调试信息
onMounted(() => {
  console.log('当前API请求配置:', {
    token: localStorage.getItem('token') ? '已设置' : '未设置',
    baseURL: import.meta.env.VITE_API_BASE_URL || '未设置'
  })
})

const emit = defineEmits(['submit', 'cancel'])

const formData = ref({...props.book})

// 当外部book属性变化时，更新本地表单数据
watch(() => props.book, (newBook) => {
  formData.value = {...newBook}
}, { deep: true })

// 表单验证
const validationErrors = ref({})

const validateForm = () => {
  const errors = {}
  
  // ISBN验证
  if (props.mode === 'create') {
    if (!formData.value.isbn) {
      errors.isbn = 'ISBN不能为空'
    } else if (!/^\d{13}$/.test(formData.value.isbn)) {
      errors.isbn = 'ISBN必须是13位数字'
    }
  }
  
  // 书名验证
  if (!formData.value.title) {
    errors.title = '书名不能为空'
  } else if (formData.value.title.length > 100) {
    errors.title = '书名不能超过100个字符'
  }
  
  // 作者验证
  if (formData.value.author && formData.value.author.length > 50) {
    errors.author = '作者名不能超过50个字符'
  }
  
  // 出版社验证
  if (formData.value.publisher && formData.value.publisher.length > 100) {
    errors.publisher = '出版社名不能超过100个字符'
  }
  
  // 价格验证
  if (formData.value.retail_price !== null && formData.value.retail_price !== undefined && formData.value.retail_price !== '') {
    if (isNaN(formData.value.retail_price) || parseFloat(formData.value.retail_price) <= 0) {
      errors.retail_price = '价格必须是大于0的数字'
    }
  }
  
  // 库存验证
  if (formData.value.stock !== null && formData.value.stock !== undefined && formData.value.stock !== '') {
    if (isNaN(formData.value.stock) || parseInt(formData.value.stock) < 0) {
      errors.stock = '库存必须是非负整数'
    }
  }
  
  validationErrors.value = errors
  return Object.keys(errors).length === 0
}

const handleSubmit = () => {
  if (validateForm()) {
    // 转换数据类型
    const submitData = {
      ...formData.value,
      retail_price: formData.value.retail_price ? parseFloat(formData.value.retail_price) : null,
      stock: formData.value.stock !== null && formData.value.stock !== undefined && formData.value.stock !== '' 
        ? parseInt(formData.value.stock) 
        : 0
    }
    
    emit('submit', submitData)
  }
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<template>
  <div class="book-form">
    <div v-if="error" class="form-error">{{ error }}</div>
    
    <div class="form-group">
      <label for="isbn">ISBN</label>
      <input 
        type="text" 
        id="isbn" 
        v-model="formData.isbn" 
        :disabled="mode === 'edit'"
        placeholder="13位数字ISBN"
        maxlength="13"
      />
      <div v-if="validationErrors.isbn" class="field-error">{{ validationErrors.isbn }}</div>
    </div>
    
    <div class="form-group">
      <label for="title">书名 <span class="required">*</span></label>
      <input 
        type="text" 
        id="title" 
        v-model="formData.title" 
        placeholder="图书标题"
      />
      <div v-if="validationErrors.title" class="field-error">{{ validationErrors.title }}</div>
    </div>
    
    <div class="form-group">
      <label for="author">作者</label>
      <input 
        type="text" 
        id="author" 
        v-model="formData.author" 
        placeholder="图书作者"
      />
      <div v-if="validationErrors.author" class="field-error">{{ validationErrors.author }}</div>
    </div>
    
    <div class="form-group">
      <label for="publisher">出版社</label>
      <input 
        type="text" 
        id="publisher" 
        v-model="formData.publisher" 
        placeholder="出版社名称"
      />
      <div v-if="validationErrors.publisher" class="field-error">{{ validationErrors.publisher }}</div>
    </div>
    
    <div class="form-group">
      <label for="retail_price">零售价</label>
      <input 
        type="number" 
        id="retail_price" 
        v-model="formData.retail_price" 
        placeholder="图书零售价"
        min="0.01"
        step="0.01"
      />
      <div v-if="validationErrors.retail_price" class="field-error">{{ validationErrors.retail_price }}</div>
    </div>
    
    <div class="form-group">
      <label for="stock">库存</label>
      <input 
        type="number" 
        id="stock" 
        v-model="formData.stock" 
        placeholder="图书库存"
        min="0"
      />
      <div v-if="validationErrors.stock" class="field-error">{{ validationErrors.stock }}</div>
    </div>
    
    <div class="form-actions">
      <button 
        type="button" 
        class="submit-btn" 
        @click="handleSubmit" 
        :disabled="loading"
      >
        {{ loading ? '提交中...' : (mode === 'create' ? '创建' : '保存') }}
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
.book-form {
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

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>