import api from '@/utils/api'

const API_URL = '/books/'

class BookService {
  // 获取所有图书
  async getAllBooks(params) {
    try {
      // 过滤掉空字符串参数
      const filteredParams = Object.entries(params).reduce((acc, [key, value]) => {
        // 如果值不为空且不为空字符串，则添加到参数中
        if (value !== null && value !== '' && value !== undefined) {
          acc[key] = value
        }
        return acc
      }, {})
      
      const response = await api.get('/books/', { 
        params: filteredParams,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      return {
        items: response.data.data || [], // 确保即使没有数据也返回空数组
        total: response.data.total || 0,
        page: response.data.page || 1,
        page_size: response.data.page_size || 10
      }
    } catch (error) {
      console.error('获取图书列表失败:', error)
      console.log(`Bearer ${localStorage.getItem('token')}`)
      throw error
    }
  }

  

  // 创建新图书
  async createBook(bookData) {
    try {
      const response = await api.post(API_URL, bookData, {
      })
      return response.data
    } catch (error) {
      console.error('创建图书失败:', error)
      throw error
    }
  }

  // 更新图书信息
  async updateBook(isbn, updateData) {
    try {
      const response = await api.put(`${API_URL}/${isbn}`, updateData, {
        
      })
      return response.data
    } catch (error) {
      console.error('更新图书信息失败:', error)
      throw error
    }
  }

  // 删除图书
  async deleteBook(isbn) {
    try {
      await api.delete(`${API_URL}/${isbn}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      return true
    } catch (error) {
      console.error('删除图书失败:', error)
      throw error
    }
  }
}

export default new BookService()