<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BookSearch from '@/components/book/BookSearch.vue'
import BookList from '@/components/book/BookList.vue'
import BookForm from '@/components/book/BookForm.vue'
import Modal from '@/components/common/Modal.vue'
import bookService from '@/services/book'

const props = defineProps({
  defaultTab: {
    type: String,
    default: 'profile'
  }
})

const router = useRouter()
const loading = ref(false)
const allBooks = ref([])
const totalBooks = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索参数
const searchParams = ref({
  isbn: '',
  title: '',
  author: '',
  publisher: '',
  min_retail_price: null,
  max_retail_price: null,
  min_stock: null,
  max_stock: null,
  sort_by: 'title',
  sort_order: 'asc',
  page: 1,
  page_size: 10,
  exact_isbn: false,
  exact_title: false,
  exact_author: false,
  exact_publisher: false
})

// 模态框状态
const showCreateBookModal = ref(false)
const showEditBookModal = ref(false)
const showDeleteBookModal = ref(false)
const selectedBook = ref(null)

// 表单状态
const newBookForm = ref({
  isbn: '',
  title: '',
  author: '',
  publisher: '',
  retail_price: '',
  stock: 0
})
const editBookForm = ref({})
const createBookError = ref('')
const editBookError = ref('')

onMounted(async () => {
  // 加载所有图书
  await loadAllBooks()
})

// 加载所有图书
const loadAllBooks = async () => {
  try {
    loading.value = true
    console.log('调试信息 - searchParams:', searchParams.value);
    const response = await bookService.getAllBooks(searchParams.value)
    
    // console.log('调试信息 - allBooks:', response.items);
    // console.log('调试信息 - totalBooks:', response.total);

    allBooks.value = response.items
    totalBooks.value = response.total
    currentPage.value = response.page
    pageSize.value = response.page_size
    
  } catch (error) {
    console.error('获取图书列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索图书
const searchBooks = async () => {
  searchParams.value.page = 1
  await loadAllBooks()
}

// 重置搜索
const resetSearch = async () => {
  searchParams.value = {
    isbn: '',
    title: '',
    author: '',
    publisher: '',
    min_retail_price: null,
    max_retail_price: null,
    min_stock: null,
    max_stock: null,
    sort_by: 'title',
    sort_order: 'asc',
    page: 1,
    page_size: 10,
    exact_isbn: false,
    exact_title: false,
    exact_author: false,
    exact_publisher: false

  }
  await loadAllBooks()
}

// 切换页面
const changePage = async (page) => {
  searchParams.value.page = page
  await loadAllBooks()
}

// 切换每页显示数量
const changePageSize = async () => {
  searchParams.value.page = 1
  await loadAllBooks()
}

// 打开创建图书模态框
const openCreateBookModal = () => {
  // 重置表单
  newBookForm.value = {
    isbn: '',
    title: '',
    author: '',
    publisher: '',
    retail_price: '',
    stock: 0
  }
  createBookError.value = ''
  showCreateBookModal.value = true
}
// 创建新图书
const createBook = async (formData) => {
  try {
    // 验证表单
    if (!formData.isbn || !formData.title) {
      createBookError.value = '请填写所有必填字段'
      return
    }
    // 验证ISBN格式
    if (!/^\d{13}$/.test(formData.isbn)) {
      createBookError.value = 'ISBN必须是13位数字'
      return
    }
    loading.value = true
    await bookService.createBook({
      isbn: formData.isbn,
      title: formData.title,
      author: formData.author,
      publisher: formData.publisher,
      retail_price: parseFloat(formData.retail_price) || null,
      stock: parseInt(formData.stock || 0)
    })
    showCreateBookModal.value = false
    await loadAllBooks()
    alert('图书创建成功')
  } catch (error) {
    console.error('创建图书失败:', error)
    createBookError.value = error.response?.data?.detail || '创建图书失败'
  } finally {
    loading.value = false
  }
}
// 打开编辑图书模态框
const openEditBookModal = (book) => {
  selectedBook.value = book
  editBookForm.value = {
    isbn: book.isbn,
    title: book.title,
    author: book.author,
    publisher: book.publisher,
    retail_price: book.retail_price,
    stock: book.stock
  }
  editBookError.value = ''
  showEditBookModal.value = true
}


// 更新图书信息
const updateBook = async (formData) => {
  try {
    // if (!formData.title) {
    //   editBookError.value = '书名不能为空'
    //   return
    // }
    loading.value = true

    // 直接发送所有字段
    const updateData = {
      title: formData.title,
      author: formData.author,
      publisher: formData.publisher,
      retail_price: parseFloat(formData.retail_price) || null,
      stock: parseInt(formData.stock)
    }
    await bookService.updateBook(selectedBook.value.isbn, updateData)

    showEditBookModal.value = false
    await loadAllBooks()
    alert('图书更新成功')
  } catch (error) {
    console.error('更新图书失败:', error)
    editBookError.value = error.response?.data?.detail || '更新图书失败'
  } finally {
    loading.value = false
  }
}

// 打开删除图书确认模态框
const openDeleteBookModal = (book) => {
  selectedBook.value = book
  showDeleteBookModal.value = true
}
// 删除图书
const deleteBook = async () => {
  try {
    if (!selectedBook.value) return
    
    loading.value = true
    await bookService.deleteBook(selectedBook.value.isbn)
    
    // 关闭模态框
    showDeleteBookModal.value = false
    
    // 刷新图书列表
    await loadAllBooks()
    
    alert('图书删除成功')
  } catch (error) {
    console.error('删除图书失败:', error)
    alert('删除图书失败: ' + (error.response?.data?.detail || '未知错误'))
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
  <div class="books-view">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="logo">
        <h1>图书管理</h1>
      </div>
      <div class="nav-actions">
        <button class="back-btn" @click="backToDashboard">
          <i class="fa fa-arrow-left"></i> 返回仪表盘
        </button>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="books-section">
        <div class="section-header">
          <h2>图书列表</h2>
          <button class="create-book-btn" @click="openCreateBookModal">
            <i class="fa fa-plus"></i> 添加新图书
          </button>
        </div>
        
        <!-- 使用图书搜索组件 -->
        <BookSearch 
          :searchParams="searchParams" 
          :loading="loading"
          @search="searchBooks"
          @reset="resetSearch"
        />
        
        <!-- 使用图书列表组件 -->
        <BookList 
          :books="allBooks" 
          :loading="loading"
          :totalBooks="totalBooks"
          :currentPage="currentPage"
          :pageSize="pageSize"
          :searchParams="searchParams"
          @edit="openEditBookModal"
          @delete="openDeleteBookModal"
          @change-page="changePage"
          @change-page-size="changePageSize"
        />
      </div>
    </main>

    <!-- 创建图书模态框 -->
    <Modal 
      :show="showCreateBookModal" 
      title="添加新图书" 
      @close="showCreateBookModal = false"
    >
      <BookForm 
        :book="newBookForm" 
        :loading="loading"
        :error="createBookError"
        mode="create"
        @submit="createBook"
        @cancel="showCreateBookModal = false"
      />
    </Modal>

    <!-- 编辑图书模态框 -->
    <Modal 
      :show="showEditBookModal" 
      title="编辑图书信息" 
      @close="showEditBookModal = false"
    >
      <BookForm 
        :book="editBookForm" 
        :loading="loading"
        :error="editBookError"
        mode="edit"
        @submit="updateBook"
        @cancel="showEditBookModal = false"
      />
    </Modal>

    <!-- 删除图书确认模态框 -->
    <Modal 
      :show="showDeleteBookModal" 
      title="确认删除" 
      @close="showDeleteBookModal = false"
    >
      <div class="delete-confirmation">
        <p>确定要删除以下图书吗？此操作不可撤销。</p>
        <div class="book-info" v-if="selectedBook">
          <p><strong>ISBN:</strong> {{ selectedBook.isbn }}</p>
          <p><strong>书名:</strong> {{ selectedBook.title }}</p>
          <p><strong>作者:</strong> {{ selectedBook.author }}</p>
        </div>
        <div class="modal-actions">
          <button 
            class="delete-btn" 
            @click="deleteBook" 
            :disabled="loading"
          >
            {{ loading ? '删除中...' : '确认删除' }}
          </button>
          <button 
            class="cancel-btn" 
            @click="showDeleteBookModal = false" 
            :disabled="loading"
          >
            取消
          </button>
        </div>
      </div>
    </Modal>
    <footer class="footer">
      <p>© 2025 图书管理系统 - 版权所有 Designed by Kevin</p>
    </footer>
  </div>
</template>

<style scoped>
.books-view {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
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
  background-color: transparent;
}

.books-section {
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

.create-book-btn {
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

.create-book-btn:hover {
  background-color: #388e3c;
}

/* 删除确认模态框样式 */
.delete-confirmation {
  padding: 1rem;
}

.book-info {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.book-info p {
  margin: 0.5rem 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.delete-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-btn:hover {
  background-color: #d32f2f;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>