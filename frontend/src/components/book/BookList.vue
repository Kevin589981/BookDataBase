<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  books: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  totalBooks: {
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

const emit = defineEmits(['edit', 'delete', 'change-page', 'change-page-size'])

const handleEdit = (book) => {
  emit('edit', book)
}

const handleDelete = (book) => {
  emit('delete', book)
}

const changePage = (page) => {
  emit('change-page', page)
}

const changePageSize = (event) => {
  const newSize = parseInt(event.target.value)
  props.searchParams.page_size = newSize
  emit('change-page-size')
}

// 计算总页数
const totalPages = () => {
  return Math.ceil(props.totalBooks / props.pageSize)
}

// 生成页码数组
const pageNumbers = () => {
  const total = totalPages()
  const current = props.currentPage
  const pages = []
  
  // 显示当前页附近的5个页码
  const start = Math.max(1, current - 2)
  const end = Math.min(total, current + 2)
  
  if (start > 1) {
    pages.push(1)
    if (start > 2) pages.push('...')
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  if (end < total) {
    if (end < total - 1) pages.push('...')
    pages.push(total)
  }
  
  return pages
}
</script>

<template>
  <div class="book-list-container">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 无数据状态 -->
    <div v-else-if="books.length === 0" class="no-data">
      <i class="fa fa-exclamation-circle"></i>
      <p>没有找到符合条件的图书</p>
    </div>
    
    <!-- 数据表格 -->
    <div v-else class="table-container">
      <table class="book-table">
        <thead>
          <tr>
            <th>ISBN</th>
            <th>书名</th>
            <th>作者</th>
            <th>出版社</th>
            <th>价格</th>
            <th>库存</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.isbn">
            <td>{{ book.isbn }}</td>
            <td>{{ book.title }}</td>
            <td>{{ book.author || '未知' }}</td>
            <td>{{ book.publisher || '未知' }}</td>
            <td>¥{{ book.retail_price ? book.retail_price.toFixed(2) : '未定价' }}</td>
            <td>{{ book.stock }}</td>
            <td class="actions">
              <button class="edit-btn" @click="handleEdit(book)">
                <i class="fa fa-edit"></i>
              </button>
              <button class="delete-btn" @click="handleDelete(book)">
                <i class="fa fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <!-- 分页控件 -->
      <div class="pagination">
        <div class="page-info">
          共 {{ totalBooks }} 条记录，每页
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
            :disabled="currentPage === 1" 
            @click="changePage(currentPage - 1)"
          >
            <i class="fa fa-chevron-left"></i>
          </button>
          
          <button 
            v-for="page in pageNumbers()" 
            :key="page"
            class="page-btn" 
            :class="{ active: page === currentPage, ellipsis: page === '...' }"
            :disabled="page === '...'"
            @click="page !== '...' && changePage(page)"
          >
            {{ page }}
          </button>
          
          <button 
            class="page-btn" 
            :disabled="currentPage === totalPages()" 
            @click="changePage(currentPage + 1)"
          >
            <i class="fa fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-list-container {
  margin-top: 1.5rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #666;
}

.no-data i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #ccc;
}

.table-container {
  overflow-x: auto;
}

.book-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

.book-table th, .book-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.book-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.book-table tr:hover {
  background-color: #f9f9f9;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-btn {
  background-color: #2196f3;
  color: white;
}

.edit-btn:hover {
  background-color: #1976d2;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}

.delete-btn:hover {
  background-color: #d32f2f;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
}

.page-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-info select {
  padding: 0.25rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.page-controls {
  display: flex;
  gap: 0.25rem;
}

.page-btn {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  background-color: white;
  color: #333;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background-color: #f5f5f5;
}

.page-btn.active {
  background-color: #2196f3;
  color: white;
  border-color: #2196f3;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn.ellipsis {
  background-color: transparent;
  border: none;
}
</style>